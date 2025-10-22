import logging
import  matplotlib.pyplot as plt
import numpy as np

logger = logging.getLogger("plots")
logging.basicConfig(level=logging.DEBUG,
                    format="%(name)s - %(funcName)s - [%(levelname)s]: %(message)s")

def ploting(points):
    plt.style.use('_mpl-gallery')

    # make the data
    x = list(map(lambda p: p.x, points))
    y = list(map(lambda p: p.y, points))
    # size and color:
    sizes = np.random.uniform(20, 25, len(x))
    colors = np.random.uniform(70, 80, len(x))

    # plot
    fig, ax = plt.subplots()

    ax.scatter(x, y, s=sizes, c=colors, vmin=0, vmax=100)

    ax.set(xlim=(0, 2.0), xticks=np.arange(1, 2),
        ylim=(0, 6), yticks=np.arange(1, 7))

    plt.show()
    


if __name__ == "__main__":
    from splines import Points, build_cubic_spline
    test_data = [ Points(1.0, 3.8), Points(1.2, 3.2), Points(1.4, 2.9), Points(1.6, 3.0), Points(1.8, 4.2), Points(2.0, 4.8)]
    points = build_cubic_spline(test_data)
    logger.debug(f"{points}")

    ploting(points)