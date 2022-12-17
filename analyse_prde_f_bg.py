from analyser import Plotter, Chart, Line


def plot_all():
    lines = []
    for i in range(5):
        f = 0.2 + 0.4 * i
        ff = int(f * 10)
        for t in range(1, 6):
            label = f'F={f}'
            session = 'bse_k04_f%02d_%04d_BG' % (ff, t)
            filepath = 'PRDE/PRDE k4 f0.2-1.8 sd50 150 bg/'
            trader = 'T'
            ids = []
            style = (f / 2, 1 - f / 2, f / 2)
            line = Line(label, session, filepath, trader, ids, style)
            lines.append(line)
    title = '10 PRDE traders, 10 ZIC traders, k=4'
    metric = 'PPS'
    chart = Chart(title, metric, lines, True)
    p = Plotter()
    p.plot(chart)


def plot_one(trial):
    lines = []
    for i in range(5):
        f = 0.2 + 0.4 * i
        ff = int(f * 10)
        label = f'{round(f, 2)}'
        session = 'bse_k04_f%02d_%04d_BG' % (ff, trial)
        filepath = 'PRDE/PRDE k4 f0.2-1.8 sd50 150 bg/'
        trader = 'T'
        ids = []
        line = Line(label, session, filepath, trader, ids, '-')
        lines.append(line)
    title = '10 PRDE traders, 10 ZIC traders, k=4'
    metric = 'PPS'
    chart = Chart(title, metric, lines, False)
    p = Plotter()
    p.box_plot(chart)


def main():
    # plot_all()
    for i in range(1, 6):
        plot_one(i)


if __name__ == "__main__":
    main()
