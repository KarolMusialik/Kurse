import matplotlib.pyplot as plt
import numpy as np

class ZeichnePie():

    def __init__(self, paramDict):

        print(paramDict)
        def func(pct, allvals):
            absolute = int(np.round(pct / 100. * np.sum(allvals)))
            return f"{pct:.1f}%\n({absolute:d})"

        labels = paramDict.get('labels')
        sizes = paramDict.get('sizes')

        fig, ax = plt.subplots()

        wedges, texts = ax.pie(sizes,
                               wedgeprops=dict(width=1.0),
                               counterclock=True,
                               colors=None,
                               startangle=0
                               )
        bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
        kw = dict(arrowprops=dict(arrowstyle='-'),bbox=bbox_props, zorder=0, va="center")

        for i, p in enumerate(wedges):
            ang = (p.theta2 - p.theta1) / 2. + p.theta1
            y = np.sin(ang / 180. * np.pi)
            x = 1.35 * np.sign(np.cos(ang / 180. * np.pi))
            horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
            connectionstyle = f"angle,angleA=0,angleB={ang}"
            kw["arrowprops"].update({"connectionstyle": connectionstyle})
            plt.annotate(str(labels[i])[0:20], xy=(0, 0), xytext=(x, 1.2*y), horizontalalignment=horizontalalignment, **kw)

        ax.pie(sizes, autopct=lambda pct: func(pct, sizes))
        if paramDict.get('title') != '':
            plt.title(paramDict.get('title'))

        if paramDict.get('file'):
            plt.savefig(paramDict.get('file'))
        else:
            plt.show()


