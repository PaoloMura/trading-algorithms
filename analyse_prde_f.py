from analyser import Plotter, Chart, Line


def analyse(trial):
    lines = []

    for i in range(5):
        f = 0.2 + 0.4 * i
        ff = int(f * 10)
        label = f'{round(f, 2)}'
        session = 'bse_k04_f%02d_%04d' % (ff, trial)
        filepath = 'PRDE/PRDE k4 f0.2-1.8 sd50 150/'
        trader = 'T'
        ids = []
        style = '-'
        line = Line(label, session, filepath, trader, ids, style)
        lines.append(line)

    title = 'Homogeneous set of 20 PRDE traders, k=4'
    metric = 'PPS'
    chart = Chart(title, metric, lines, False)
    p = Plotter()
    p.box_plot(chart)


def main():
    for t in range(1, 6):
        analyse(t)


if __name__ == "__main__":
    main()
