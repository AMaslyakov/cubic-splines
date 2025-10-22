import click
import csv
import logging
import sys
from typing import List, Optional

from spline_plot import ploting
from splines import Points, build_cubic_spline

CSV_FILE = "input_data.csv"


logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('cubic_splines.log', encoding='utf-8')
        ]
    )

logger = logging.getLogger("cubic_splines")
logger.setLevel(logging.INFO)

def read_data(file_name: str) -> List[Points]:
    """Чтение данных из CSV файла"""
    logger.info(f"Начинаем чтение данных из файла: {file_name}")
    
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=',')
            result = [Points(float(row["x"]), float(row["y"])) for row in reader]
            logger.info(f"Успешно загружено {len(result)} точек из файла {file_name}")
            return result
    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_name}")

   

def generate_x_points(x0: float, num_points: int, step: float) -> List[float]:
    """Генерирует возрастающие x точки начиная с x0"""
    logger.debug(f"Генерируем {num_points} точек начиная с x0={x0}, шаг={step}")
    
    x_points = []
    for i in range(num_points):
        x_points.append(x0 + i * step)
    
    logger.debug(f"Сгенерированы x точки: {x_points}")
    return x_points

def input_user_data() -> List[Points]:
    """Интерактивный ввод данных пользователем"""
    logger.info("Запуск интерактивного режима ввода данных")
    click.echo("Введите параметры для генерации точек:")
    
    x0 = click.prompt("Введите x0", type=float)
    num_points = click.prompt("Введите количество точек", type=int)
    step = click.prompt("Введите шаг", type=float)

    logger.debug(f"Пользователь ввел: x0={x0}, num_points={num_points}, step={step}")

    # Генерируем x точки
    x_points = generate_x_points(x0, num_points, step)
    click.echo(f"Сгенерированы x точки: {x_points}")

    # Вводим y точки
    y_points = []
    for i, x in enumerate(x_points):
        y = click.prompt(f"Введите y{i} для x={x}", type=float)
        y_points.append(y)
        logger.debug(f"Введена точка {i}: x={x}, y={y}")

    # Создаем список точек
    points = [Points(x, y) for x, y in zip(x_points, y_points)]
    logger.info(f"Создано {len(points)} точек пользователем")
    return points


def display_results(spline_points: List[Points], source_points=None):
    """Отображение результатов"""
    logger.info("Отображение результатов")

    click.echo(f"Построен сплайн с {len(spline_points)} точками")
    click.echo("Первые 5 точек сплайна:")

    xlim = (1, 2.5)
    ylim = (1, 6)
    if source_points is not None:
        x = list(map(lambda p: p.x, source_points))
        y = list(map(lambda p: p.y, source_points))
        # Добавляем отступы для лучшей визуализации
        x_range = max(x) - min(x)
        y_range = max(y) - min(y)
        xlim = (min(x) - 0.1 * x_range, max(x) + 0.1 * x_range)
        ylim = (min(y) - 0.1 * y_range, max(y) + 0.1 * y_range)

    ploting(spline_points, source_points, xlim, ylim)

def handle_interactive_mode() -> Optional[List[Points]]:
    """Обработка интерактивного режима"""
    logger.info("Запуск интерактивного режима")
    
    # Опрос 1: Использовать данные по умолчанию?
    use_default = click.confirm(f"Использовать данные по умолчанию из файла: {CSV_FILE}?", default=True)
    
    if use_default:
        data = read_data(CSV_FILE)
        if data is not None:
            return data

    # Опрос 2: Хотите ввести данные?
    input_manually = click.confirm("Хотите ввести данные вручную?", default=True)
    
    if input_manually:
        return input_user_data()
    else:
        logger.info("Пользователь выбрал завершение программы")
        click.echo("Программа завершена.")
        return None

@click.command()
@click.argument('input_data', required=False, type=click.Path(exists=True))
def main(input_data):
    """Программа построения кубических сплайнов.
    
    Если указан файл данных - загружает данные и строит сплайн.
    Если файл не указан - запускает интерактивный режим.
    """
    # Инициализация логирования
    click.echo("=== Программа построения кубических сплайнов ===")
    
    if input_data:
        data = read_data(input_data)
    else:
         data = handle_interactive_mode()
         if data is None:
             return

    spline_points = build_cubic_spline(data, 0.001)

    display_results(spline_points, source_points=data)

    logger.info("Программа успешно завершена")

if __name__ == "__main__":
    main()
