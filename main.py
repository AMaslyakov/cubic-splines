from pydoc import cli
import click
import csv
import logging
import sys
from typing import List, Optional

from splines import Points, build_cubic_spline

CSV_FILE = "input_data.csv"

# Настройка логирования
def setup_logging():
    """Настройка системы логирования"""
    # Старая настройка (закомментирована)
    # logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.NOTSET)
    
    # Новая настройка логирования
    logging.basicConfig(
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        level=logging.INFO,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('cubic_splines.log', encoding='utf-8')
        ]
    )

logger = logging.getLogger("cubic_splines")
logger.setLevel(logging.DEBUG)

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
        raise
    except (ValueError, KeyError) as e:
        logger.error(f"Ошибка парсинга данных в файле {file_name}: {e}")
        raise
   

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
    
    try:
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
        
    except Exception as e:
        logger.error(f"Ошибка при вводе данных пользователем: {e}")
        raise

def load_data_from_file(file_path: str) -> List[Points]:
    """Загрузка данных из файла"""
    logger.info(f"Загружаем данные из файла: {file_path}")
    try:
        data = read_data(file_path)
        click.echo(f"Загружены данные из файла {file_path}")
        return data
    except FileNotFoundError as e:
        logger.error(f"Файл не найден {file_path}: {e}")
        click.echo(f"Файл не найден {file_path}: {e}")
        

def load_default_data() -> Optional[List[Points]]:
    """Загрузка данных по умолчанию"""
    logger.info(f"Попытка загрузки данных по умолчанию из файла: {CSV_FILE}")
    try:
        data = read_data(CSV_FILE)
        click.echo(f"Загружены данные из файла {CSV_FILE}")
        return data
    except FileNotFoundError:
        logger.warning(f"Файл {CSV_FILE} не найден!")
        click.echo(f"Файл {CSV_FILE} не найден!")
        return None
   

def build_spline(data: List[Points]) -> List[Points]:
    """Построение кубического сплайна"""
    logger.info("Начинаем построение кубического сплайна")
    click.echo("Строим кубический сплайн...")
    
    try:
        spline_points = build_cubic_spline(data)
        logger.info(f"Сплайн успешно построен с {len(spline_points)} точками")
        return spline_points
    except Exception as e:
        logger.error(f"Ошибка при построении сплайна: {e}")
        raise

def display_results(spline_points: List[Points], input_data: List[Points]):
    """Отображение результатов"""
    logger.info("Отображение результатов")
    
    # Старые логи (закомментированы)
    # logger.debug(f"Input data: {data}")
    # logger.debug(f"Spline points: {spline_points}")
    
    # Новые улучшенные логи
    logger.debug(f"Исходные данные ({len(input_data)} точек): {[(p.x, p.y) for p in input_data]}")
    logger.debug(f"Точки сплайна ({len(spline_points)} точек): {[(p.x, p.y) for p in spline_points[:10]]}...")
    
    click.echo(f"Построен сплайн с {len(spline_points)} точками")
    click.echo("Первые 5 точек сплайна:")
    for i, point in enumerate(spline_points[:5]):
        click.echo(f"  x={point.x:.3f}, y={point.y:.3f}")
        logger.debug(f"Точка сплайна {i}: x={point.x:.3f}, y={point.y:.3f}")

def handle_file_mode(input_data: str) -> List[Points]:
    """Обработка режима с файлом данных"""
    logger.info(f"Режим с файлом данных: {input_data}")
    return load_data_from_file(input_data)

def handle_interactive_mode() -> Optional[List[Points]]:
    """Обработка интерактивного режима"""
    logger.info("Запуск интерактивного режима")
    
    # Опрос 1: Использовать данные по умолчанию?
    use_default = click.confirm(f"Использовать данные по умолчанию из файла: {CSV_FILE}?", default=True)
    
    if use_default:
        data = load_default_data()
        if data is not None:
            return data
        # Если данные по умолчанию не загрузились, переходим к ручному вводу
    
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
    setup_logging()
    logger.info("=== Запуск программы построения кубических сплайнов ===")
    click.echo("=== Программа построения кубических сплайнов ===")
    
    try:
        # Загрузка данных
        if input_data:
            data = handle_file_mode(input_data)
        else:
            data = handle_interactive_mode()
            if data is None:
                return
        
        # Построение сплайна
        spline_points = build_spline(data)
        
        # Отображение результатов
        display_results(spline_points, data)
        
        logger.info("Программа успешно завершена")
        
    except Exception as e:
        logger.error(f"Критическая ошибка в программе: {e}")
        click.echo(f"Произошла ошибка: {e}")
        raise

if __name__ == "__main__":
    main()
