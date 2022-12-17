from analyser import Plotter, Chart, Line


def analyse(trial):
    lines = []
    for k in range(5, 30, 5):
        label = f'{k}'
        session = 'bse_k%02d_f08_%04d' % (k, trial)
        filepath = 'PRDE/PRDE k5-25 f0.8 sd50 150/'
        trader = 'T'
        ids = []
        line = Line(label, session, filepath, trader, ids, '-')
        lines.append(line)
    title = 'Homogeneous set of 20 PRDE traders, f=0.8'
    metric = 'PPS'
    chart = Chart(title, metric, lines, False)
    p = Plotter()
    # p.plot(chart)
    # p.box_plot(chart)
    p.stat_test(chart)


def main():
    for t in range(1, 6):
        analyse(t)


if __name__ == "__main__":
    main()
