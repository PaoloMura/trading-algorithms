from analyser import Plotter, Chart, Line


def plot_all():
    lines = []
    for k in range(5, 30, 5):
        for t in range(1, 11):
            label = f'k={k}'
            session = 'bse_k%02d_f08_%04d_1toM' % (k, t)
            filepath = 'PRDE/PRDE k5-25 f0.8 sd50 150 1toM/'
            trader = 'T'
            ids = []
            style = (k / 30, 1 - k / 30, k / 30)
            line = Line(label, session, filepath, trader, ids, style)
            lines.append(line)
    title = '1 PRDE trader amongst 19 ZIC traders, f=0.8'
    metric = 'PPS'
    chart = Chart(title, metric, lines, True)
    p = Plotter()
    p.plot(chart)


def plot_one(trial):
    lines = []
    for k in range(5, 30, 5):
        label = f'{k}'
        session = 'bse_k%02d_f08_%04d_1toM' % (k, trial)
        filepath = 'PRDE/PRDE k5-25 f0.8 sd50 150 1toM/'
        trader = 'T'
        ids = []
        line = Line(label, session, filepath, trader, ids, '-')
        lines.append(line)
    title = '1 PRDE trader, 19 ZIC traders, f=0.8'
    metric = 'PPS'
    chart = Chart(title, metric, lines, False)
    p = Plotter()
    p.box_plot(chart)


def main():
    for i in range(1, 11):
        plot_one(i)


if __name__ == "__main__":
    main()
