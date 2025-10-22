import logging
import  matplotlib.pyplot as plt

logger = logging.getLogger("plots")
logging.basicConfig(level=logging.DEBUG,
                    format="%(name)s - %(funcName)s - [%(levelname)s]: %(message)s")

def set_plot_limits(ax, x_data, y_data, xlim=None, ylim=None, margin=0.1):
    """Установка границ графика с автоматическим расчетом или заданными значениями"""
    if xlim is None:
        xlim = (min(x_data) - margin, max(x_data) + margin)
    if ylim is None:
        ylim = (min(y_data) - margin, max(y_data) + margin)
    
    ax.set(xlim=xlim, ylim=ylim)
    return xlim, ylim

def ploting(points, source_points=None, xlim=None, ylim=None):
    plt.style.use('_mpl-gallery')

    # make the data
    x = list(map(lambda p: p.x, points))
    y = list(map(lambda p: p.y, points))
    
    # plot
    fig, ax = plt.subplots()

    # Plot all points with dark blue color and smaller size
    ax.scatter(x, y, s=2, c='darkblue', alpha=0.8)
    
    # Highlight source points in red with larger size if they exist
    if source_points is not None:
        source_x = list(map(lambda p: p.x, source_points))
        source_y = list(map(lambda p: p.y, source_points))
        ax.scatter(source_x, source_y, s=15, c='red', alpha=0.9)

    # Установка области построения
    set_plot_limits(ax, x, y, xlim, ylim, margin=0.2)
    
    # Установка соотношения осей 1:1
    ax.set_aspect('auto')
    
    # Уменьшение размера надписей
    ax.tick_params(labelsize=8)
    ax.set_xlabel('x', fontsize=8)
    ax.set_ylabel('y', fontsize=8)

    # Сохранить в файл вместо показа
    plt.savefig('spline_plot.png', dpi=600, bbox_inches='tight')
    plt.show()  # Раскомментируйте для показа
    


if __name__ == "__main__":
    from splines import Points, build_cubic_spline
    test_data = [ Points(1.0, 3.8), Points(1.2, 3.2), Points(1.4, 2.9), Points(1.6, 3.0), Points(1.8, 4.2), Points(2.0, 4.8)]
    points = build_cubic_spline(test_data, 0.001)
    logger.debug(f"{points}")

    ploting(points, source_points=test_data)