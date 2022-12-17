import json
import sys
from pprint import pprint

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.collections import LineCollection
from scipy import stats


class Plotter:
    def __init__(self, sma_days=7):
        self.sma_days = sma_days

    def __parse_session_id(self, session_id: str):
        items = session_id.split(sep='_')
        k = items[1]
        f = items[2]
        trial = items[3]

        params = dict()

        if k == 'hk':
            params.update({'k_type': 'hetero'})
        else:
            params.update({'k_type': 'homo', 'k_val': int(k[1:])})

        if f == 'hf':
            params.update({'f_type': 'hetero'})
        elif f == 'af':
            params.update({'f_type': 'adaptive'})
        else:
            params.update({'f_type': 'homo', 'f_val': float(f[1] + '.' + f[2:])})

        params.update({'trial': trial})
        return params

    def __get_total_pps(self, df: pd.DataFrame, trader_type: str, trader_ids: list):
        """
        Finds the total profit per second (PPS) of any traders that match the specified type and ids.

        trader_type: 'B' | 'S' | 'T' - buyer, seller and total respectively
        trader_ids: [int] - if empty, use all ids
        """
        n_rows = df.shape[0]
        n_cols = df.shape[1]

        days = df[1].map(lambda x: x / (60 * 60 * 24))
        total_pps = pd.Series([0 for _ in range(n_rows)])

        for i in range(n_cols):
            if df[i][0] == ' id=':
                t_type = df[i+1][0][0]
                t_value = int(df[i+1][0][1:])
                if (trader_type == 'T' or t_type == trader_type) and (not trader_ids or t_value in trader_ids):
                    total_pps = total_pps.add(df[i + 6])

        return days, total_pps

    def __get_cols(self, df: pd.DataFrame, trader_type: str, trader_ids: list, metric: str):
        """
        Extracts the columns that match the given traders and metric

        trader_type: 'B' | 'S' | 'T' - buyer, seller, total respectively
        trader_ids: [int] - if empty, use all ids
        metric: 'PPS' | 'strategy'
        """
        cols = []
        for i in range(df.shape[1]):
            if df[i][0] == ' id=':
                t_type = df[i + 1][0][0]
                t_value = int(df[i + 1][0][1:])
                if (trader_type == 'T' or t_type == trader_type) and (not trader_ids or t_value in trader_ids):
                    if metric == 'PPS':
                        cols.append(df[i+6])
                    elif metric == 'strategy':
                        cols.append(df[i+4])
        return cols

    def __get_strat_grid(self, days: pd.Series, cols: list):
        """
        Creates a 2D grid of the strategy space for the given columns

        cols: [pd.Series]
        """

        n_days = int(days.iloc[-1]) + 1
        n_traders = len(cols)

        grid = np.array([[.0 for _ in range(n_days)] for _ in range(40)])
        for col in cols:
            for i in range(col.shape[0]):
                strategy = col[i]
                if pd.isna(strategy):
                    continue
                day = int(days[i])
                bin = int((2 - (strategy + 1)) * 19.5)
                grid[bin][day] += 1

        grid = (5 * grid) / n_traders

        return grid

    def __plot_graph(self, title: str, lines: list, grouped: bool):
        """
        Plots a line graph of PPS against time.

        lines: [(days, PPS, label)] : [(pd.Series, pd.Series, str)]
        """
        if not grouped:
            plt.xlabel('days')
            plt.ylabel('PPS')
            plt.title(title)
            for days, line, label, style in lines:
                plt.plot(days, line, style, label=label)
            plt.legend()
            plt.show()

        else:
            x_lim = [10000, 0]
            y_lim = [1000, 0]

            collections = dict()
            for line in lines:
                if line[2] in collections:
                    collections[line[2]].append(line)
                else:
                    collections[line[2]] = [line]

                x_lim[0] = min(x_lim[0], line[0].min())
                x_lim[1] = max(x_lim[1], line[0].max())
                y_lim[0] = min(y_lim[0], line[1].min())
                y_lim[1] = max(y_lim[1], line[1].max())

            f, ax = plt.subplots(1, 1)
            plt.xlabel('days')
            plt.ylabel('PPS')
            plt.title(title)
            for collection in collections.values():
                lines = LineCollection([list(zip(line[0], line[1])) for line in collection], colors=[collection[0][3] for _ in range(len(collection))], label=collection[0][2])
                ax.add_collection(lines)
            ax.legend(loc='lower right')

            x_lim[0] = 6
            y_lim[0] -= 5
            y_lim[1] += 5
            ax.set_xlim(x_lim)
            ax.set_ylim(y_lim)
            plt.show()

    def __sma(self, series):
        series_sma = series.rolling(self.sma_days * 24).mean()
        return series_sma

    def __unpack_json(self, exp_file: str):
        try:
            f = open(exp_file, 'r')
            data = json.load(f)
            title = data['title']
            metric = data['metric']
            lines = data['lines']
            plot_lines = []
            for line in lines:
                label = line['label']
                session = line['session']
                filepath = line['filepath']
                trader = line['trader']
                ids = line['ids']
                df = pd.read_csv(filepath + session + '_strats.csv', header=None)
                if metric == 'PPS':
                    days, total_pps = self.__get_total_pps(df, trader, ids)
                    total_pps = self.__sma(total_pps)
                    plot_lines.append((days, total_pps, label))
            return title, plot_lines
        except FileNotFoundError as e:
            raise e

    def __unpack_chart(self, chart):
        lines = []
        for line in chart.lines:
            filename = line.filepath + line.session + '_strats.csv'
            df = pd.read_csv(filename, header=None)
            days, total_pps = self.__get_total_pps(df, line.trader, line.ids)
            total_pps = self.__sma(total_pps)
            lines.append((days, total_pps, line.label, line.style))
        return chart.title, lines, chart.grouped

    def visualise(self, json_file: str):
        """
        Visualises a given experiment.

        json_file: the name of a JSON file containing an experiment schema.
        """
        title, lines = self.__unpack_json(json_file)
        self.__plot_graph(title, lines)

    def plot(self, chart):
        """
        Plot a given line chart.

        chart: a Chart object.
        """
        title, lines, grouped = self.__unpack_chart(chart)
        self.__plot_graph(title, lines, grouped)

    def __is_normally_distributed(self, data):
        s, p = stats.shapiro(data)
        print('p: ', p)
        return p >= 0.05

    def box_plot(self, chart):
        title, lines, grouped = self.__unpack_chart(chart)
        pps = [line[1] for line in lines]
        df = pd.concat(pps, axis=1)
        labels = [line[2] for line in lines]
        df.set_axis(labels, axis=1, inplace=True)
        sns.boxplot(data=df)
        plt.title(title)
        plt.ylabel('PPS')
        plt.xlabel('k')
        plt.show()

    def stat_test(self, chart):
        title, lines, grouped = self.__unpack_chart(chart)
        pps = [line[1] for line in lines]
        for p in pps:
            n = p.count()
            m = p.mean()
            s = p.std()
            print('n: ', n)
            print('mean: ', m)
            print('std: ', s)
            print('normal: ', self.__is_normally_distributed(p))
        statistic, pvalue = stats.f_oneway(pps[0].dropna(), pps[1].dropna(), pps[2].dropna(), pps[3].dropna(), pps[4].dropna())
        print('p value: ', pvalue)
        if pvalue < 0.05:
            print('Reject H0 - different means')
        else:
            print('can\'t reject H0')


def stat_test_2():
    path = 'PRAD/PRAD k4 p0.1 sd60 140/'
    total_profit_02 = []
    for i in range(1, 16):
        if i in [4, 5, 8, 12]:
            continue
        df = pd.read_csv(path + f'bse_k04_af_%04d_avg_balance.csv' % i, header=None)
        total_profit_02.append(df[5][0])
    avg_profit_02 = sum(total_profit_02) / len(total_profit_02)
    s, p = stats.shapiro(total_profit_02)
    print(p >= 0.05)

    path = 'PRAD/PRAD k15 p0.2 sd60 140/'
    total_profit_06 = []
    for i in range(1, 16):
        if i in [4, 5, 8, 12]:
            continue
        df = pd.read_csv(path + f'bse_k15_af_%04d_avg_balance.csv' % i, header=None)
        total_profit_06.append(df[5][0])
    avg_profit_06 = sum(total_profit_06) / len(total_profit_06)
    s, p = stats.shapiro(total_profit_06)
    print(p >= 0.05)

    path = 'PRAD/PRDE k4 f0.8 sd60 140/'
    total_profit_10 = []
    for i in range(1, 16):
        if i in [4, 5, 8, 12]:
            continue
        df = pd.read_csv(path + f'bse_k04_f08_%04d_avg_balance.csv' % i, header=None)
        total_profit_10.append(df[5][0])
    avg_profit_10 = sum(total_profit_10) / len(total_profit_10)
    s, p = stats.shapiro(total_profit_10)
    print(p >= 0.05)

    statistic, pvalue = stats.f_oneway(total_profit_02, total_profit_06, total_profit_10)
    print('p value: ', pvalue)
    if pvalue < 0.05:
        print('Reject H0 - different means')
    else:
        print('can\'t reject H0')

    pprint([['PRAD 4', 'PRAD 15', 'PRDE 4'],
            [avg_profit_02, avg_profit_06, avg_profit_10],
            [np.std(total_profit_02), np.std(total_profit_06), np.std(total_profit_10)]])


if __name__ == '__main__':
    stat_test_2()


class Line:
    def __init__(self, label, session, filepath, trader, ids, style):
        self.label = label
        self.session = session
        self.filepath = filepath
        self.trader = trader
        self.ids = ids
        self.style = style


class Chart:
    def __init__(self, title, metric, lines, grouped):
        self.title = title
        self.metric = metric
        self.lines = lines
        self.grouped = grouped
