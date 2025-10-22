# Уравнений будет составлено по количеству отрезков x_i - x_(i-1)
# если задано 6 точек, то отрезков будет 5

# Поиск a_i
import logging
from collections import namedtuple
from typing import Any

Points = namedtuple("Points", ["x", "y"])

Segment = namedtuple("Segment", ["x_l", "x_r"])

Coefficient_c_i = namedtuple("Coefficient_c_i", ["p", "q", "l", "s"])

CoefficientPolynom = namedtuple("CoefficientPolynom", ["a", "b", "c", "d"])


logger = logging.getLogger("spline-lib")
logging.basicConfig(level=logging.DEBUG,
                    format="%(name)s - %(funcName)s - [%(levelname)s]: %(message)s")


def select_segments(x):
    length = len(x)
    segments = []
    for i in range(length - 1):
        # segment = (x[i], x[i+1])
        segment = Segment(x[i], x[i+1])
        segments.append(segment)
    return segments


def calculate_h_i(segments:list[Segment]):
    h_i = []
    logger.debug(f"{segments=}")
    for segment in segments:
        # logger.debug(f"{segment=}")
        diff = segment.x_r - segment.x_l
        # logger.debug(f"{diff=}")
        h_i.append(diff)
    return h_i


def get_a_i(y) -> list[float]:
   return y[:-1]


def tridiagonal_coefficients(y, h_i)-> list[Coefficient_c_i]:
    """
    Формирует коэффициенты тридиагональной системы для естественного сплайна
    c_0 = 0 и c_n = 0
    """

    #n - количество отрезков и уравнений в системе
    n = len(h_i)

    coefficients = []
    for i in range(0, n):
        # Правильная формула для три диагональной системы
        main_diagonal = 2 * (h_i[i - 1] + h_i[i])
        down_diagonal = h_i[i - 1]
        upper_diagonal = h_i[i]

        # Правая часть уравнения
        answer = 3 * (((y[i + 1] - y[i]) / h_i[i]) - ((y[i] - y[i - 1]) / h_i[i - 1]))
        
        # Отладочная информация для точки x=1.4 (i=2)
        if i == 1:
            # Первое уравнение: учитываем c_0 = 0
            coeff = Coefficient_c_i(0, main_diagonal, upper_diagonal, answer)
        elif i == n - 1:
            # Последнее уравнение: учитываем c_n = 0
            coeff = Coefficient_c_i(down_diagonal, main_diagonal, 0, answer)
        else:
            coeff = Coefficient_c_i(down_diagonal, main_diagonal, upper_diagonal, answer)
        coefficients.append(coeff)
    logger.debug(f"{len(coefficients)=}")
    return coefficients

def calculate_U(coefficients: list[Coefficient_c_i]):
    u1 = -coefficients[0].l/ coefficients[0].q
    U = [u1]
    for i, coeff in enumerate(coefficients[1:], start=1):
        u_i = -coeff.l/(coeff.p * U[i-1] + coeff.q)
        U.append(u_i)
    logger.debug(f"{U=}")
    return U


def calculate_V(coefficients):
    v1 = coefficients[0].s/coefficients[0].q
    V = [v1]
    U = calculate_U(coefficients)
    for i, coeff in enumerate(coefficients[1:], start=1):
       v_i = (coeff.s - coeff.p * V[i-1])/(coeff.p * U[i-1] + coeff.q)
       V.append(v_i)
    return V


def calculate_c_i(y, h_i):
    """
    Нахождение коэффициентов c_i кубических полиномов
    :param y:
    :param h_i:
    :return: коэффициенты кубического полинома c_i
    """
    coefficients = tridiagonal_coefficients(y, h_i)
    logger.debug(f"{len(coefficients)=}")
    U = calculate_U(coefficients)
    V = calculate_V(coefficients)

    logger.debug(f"{len(U)=}")
    n = len(h_i)
    c = [0.0] * (n + 1)
    logger.debug(f"{len(c)=}; {c=}")
    c[-1] = V[-1]
    for i in range(n-1, 0, -1):
        c_i = U[i] * c[i+1] + V[i]  # Используем c[i+1] вместо c[i]
        c[i] = c_i  # Записываем в правильную позицию
        logger.debug(f"{c_i=}")
    logger.debug(f"{len(c)=}; {c=}")
    return c

def calculate_d_i(c_i, h_i):
    n = len(h_i)
    d = []
    for i in range(n):
        d_i = (c_i[i + 1] - c_i[i]) / (3 * h_i[i])
        d.append(d_i)
    logger.debug(f"{d}")
    return d

def calculate_b_i(c, h, y):
    n = len(h)
    b = []
    for i in range(n):
        b_i = (y[i+1] - y[i]) / h[i] - h[i] * (c[i + 1] + 2 * c[i]) / 3
        b.append(b_i)
    return b


def create_spline_function(a_coeff, b_coeff, c_coeff, d_coeff, x_start):
    """
    Создает функцию сплайна с зафиксированными коэффициентами.
    Использует замыкание для захвата коэффициентов из внешней области видимости.
    """
    def spline_function(x_coordinate):
        return (a_coeff + 
                b_coeff * (x_coordinate - x_start) + 
                c_coeff * (x_coordinate - x_start) ** 2 + 
                d_coeff * (x_coordinate - x_start) ** 3)
    return spline_function

def assembly_cubic_polynomial(x, a, b, c, d):
    segments:list[Segment] = select_segments(x)
    functions = []
    for i, segment in enumerate(segments):
        # Создаем замыкание с зафиксированными коэффициентами
        # Используем x[i] как базовую точку для i-го сегмента
        spline_func = create_spline_function(a[i], b[i], c[i], d[i], x[i])
        functions.append([segment, spline_func])
    return functions

def build_cubic_spline(input_data: list[Points], step_x=0.01):
    x, y = extract_x_y(input_data)
    segments:list[Segment] = select_segments(x)

    a_i, b_i, c_i, d_i = get_all_cubic_polynom_coefficients(segments, y)

    logger.debug(f"{len(a_i)=}; {len(c_i)=}; {len(b_i)=}; {len(d_i)=}")
    polynomials = assembly_cubic_polynomial(x, a_i, b_i, c_i[:-1], d_i)

    result = generate_spline_points(polynomials, step_x, x)

    return result


def generate_spline_points(polynomials: list[Any], step_x: float, x: list[Any]) -> list[Any]:
    result = []
    x_coordinate = x[0]
    
    for polynom in polynomials:
        segment: Segment = polynom[0]
        cubic_polynom = polynom[1]
        
        # Генерируем точки для текущего сегмента
        while x_coordinate < segment.x_r:
            y_coordinate = cubic_polynom(x_coordinate)
            result.append(Points(x_coordinate, y_coordinate))
            x_coordinate += step_x
            
            # Проверяем, не вышли ли за границы
            if x_coordinate > x[-1]:
                break
    
    # Добавляем последнюю точку, если она не была добавлена
    if not result or result[-1].x < x[-1]:
        last_polynom = polynomials[-1][1]
        result.append(Points(x[-1], last_polynom(x[-1])))
    
    return result


def get_all_cubic_polynom_coefficients(segments: list[Segment], y: list[float]) -> tuple[
    list[float], list[float], list[float], list[float]]:
    h_i = calculate_h_i(segments)

    a_i = get_a_i(y)
    logger.debug(f"{len(a_i)=}")
    c_i = calculate_c_i(y, h_i)
    d_i = calculate_d_i(c_i, h_i)
    b_i = calculate_b_i(c_i, h_i, y)
    return a_i, b_i, c_i, d_i


def extract_x_y(input_data:list[Points]) :
    y = list(map(lambda c: c.y, input_data))
    x = list(map(lambda c: c.x, input_data))
    return x, y


if __name__ == '__main__':
    test_data = [ Points(1.0, 3.8), Points(1.2, 3.2), Points(1.4, 2.9), Points(1.6, 3.0), Points(1.8, 4.2), Points(2.0, 4.8)]
    result =  build_cubic_spline(test_data, step_x=0.01)

    # logger.debug(f"{len(result)=};\n{result}")

