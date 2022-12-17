from analyser import Plotter, Chart, Line


def main():
    lines = []

    # Add PRDE lines
    for k in range(1, 16):
        label = 'PRDE, k=4'
        session = 'bse_k04_f08_%04d' % k
        filepath = 'PRAD/PRDE k4 f0.8 sd60 140/'
        trader = 'T'
        ids = []
        style = (.2, .2, .7)
        line = Line(label, session, filepath, trader, ids, style)
        lines.append(line)

    # Add PRAD lines with k=4
    for k in range(1, 16):
        label = 'PRAD, k=4'
        session = 'bse_k04_af_%04d' % k
        filepath = 'PRAD/PRAD k4 p0.1 sd60 140/'
        trader = 'T'
        ids = []
        style = (.7, .2, .2)
        line = Line(label, session, filepath, trader, ids, style)
        lines.append(line)

    # Add PRAD lines with k=15
    for k in range(1, 16):
        label = 'PRAD, k=15'
        session = 'bse_k15_af_%04d' % k
        filepath = 'PRAD/PRAD k15 p0.2 sd60 140/'
        trader = 'T'
        ids = []
        style = (.2, .7, .2)
        line = Line(label, session, filepath, trader, ids, style)
        lines.append(line)

    title = 'Homogeneous set of 20 traders'
    metric = 'PPS'
    chart = Chart(title, metric, lines)
    p = Plotter()
    p.plot(chart)


if __name__ == "__main__":
    main()
