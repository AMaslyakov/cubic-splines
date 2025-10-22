# Уравнений будет составлено по количеству отрезков x_i - x_(i-1)
# если задано 6 точек, то отрезков будет 5

# Поиск a_i
import logging
from collections import namedtuple

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
        logger.debug(f"{segment=}")
        diff = segment.x_r - segment.x_l
        h_i.append(diff)
    return h_i


def get_a_i(y) -> list[float]:
   return y[:-1]


def tridiagonal_coefficients(y, h_i)-> list[Coefficient_c_i]:
    '''
        
    '''

    #n - количество отрезков и уравнений в системе
    n = len(h_i)

    coefficients = []
    for i in range(1, n):
        main_diagonal = h_i[i - 1] + h_i[i]
        down_diagonal = h_i[i - 1]
        upper_diagonal = h_i[i]

        # в массиве h индексы начинаются с 0, как и в массиве y
        # поэтому индексы массива Y понижены на 1 для того чтобы формула коэффициентов значений, была корректной
        answer = 3 * (((y[i + 1] - y[i]) / h_i[i]) - ((y[i] - y[i - 1]) / h_i[i - 1]))
        if i == 1:
            coeff = Coefficient_c_i(0, main_diagonal, upper_diagonal, answer)
            # coeff = {"p":0,
            #          "q": main_diagonal,
            #          "l": upper_diagonal,
            #          "s": answer}
            # coefficients.append({"p":0, "q": main_diagonal, "l": upper_diagonal, "s": answer})
        elif i == n - 1:
            coeff = Coefficient_c_i(down_diagonal, main_diagonal, 0, answer)
            # coeff = {"p":down_diagonal,
            #          "q": main_diagonal,
            #          "l": 0,
            #          "s": answer}
            # coefficients.append({"p":down_diagonal, "q": main_diagonal, "l": 0, "s": answer})
        else:
            coeff = Coefficient_c_i(down_diagonal, main_diagonal, upper_diagonal, answer)
            # coeff = {"p":down_diagonal,
            #          "q": main_diagonal,
            #          "l": upper_diagonal,
            #          "s": answer}
            # coefficients.append({"p":down_diagonal, "q": main_diagonal, "l": upper_diagonal, "s": answer})
        coefficients.append(coeff)
    return coefficients

def calculate_U(coefficients: list[Coefficient_c_i]):
    u1 = -coefficients[0].l/ coefficients[0].q
    U = [u1]
    for i, coeff in enumerate(coefficients[1:], start=1):
        u_i = -coeff.l/(coeff.p * U[i-1] + coeff.q)
        U.append(u_i)
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
    U = calculate_U(coefficients)
    V = calculate_V(coefficients)

    n = len(U)
    c = [0.0]  # c_0 = 0 для естественного сплайна
    
    # Обратный ход прогонки: c_i = U_i * c_{i+1} + V_i
    for i in range(n):
        c_i = U[i] * c[i] + V[i]
        c.append(c_i)
    return c

def calculate_d_i(c_i, h_i):
    n = len(h_i)
    d = []
    for i in range(n - 1):
        d_i = (c_i[i + 1] - c_i[i]) / (3 * h_i[i])
        d.append(d_i)
    d_n = -c_i[-1] / (3 * h_i[-1])
    d.append(d_n)
    return d

def calculate_b_i(c, h, y):
    n = len(h)
    b = []
    for i in range(n-1):
        b_i = (y[i+1] - y[i]) / h[i] - h[i] * (c[i + 1] + 2 * c[i]) / 3
        b.append(b_i)
    b_n = (y[-1]-y[-2])/h[-1] - (2 * h[-1] * c[-1]) / 3
    b.append(b_n)
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
        spline_func = create_spline_function(a[i], b[i], c[i], d[i], x[i])
        functions.append([segment, spline_func])
    return functions

def build_cubic_spline(input_data, step_x=0.01):
    y = list(map(lambda c: c[1], input_data))
    x = list(map(lambda c: c[0], input_data))
    segments:list[Segment] = select_segments(x)
    h_i = calculate_h_i(segments)

    a_i = get_a_i(y)
    c_i = calculate_c_i(y, h_i)
    d_i = calculate_d_i(c_i, h_i)
    b_i = calculate_b_i(c_i, h_i, y)

    polynomials = assembly_cubic_polynomial(x, a_i, b_i, c_i, d_i)

    result = []
    x_coordinate = x[0]
    for polynom in polynomials:
        segment:Segment = polynom[0]
        cubic_polynom = polynom[1]
        while segment.x_l <= x_coordinate < segment.x_r:
            y_coordinate = cubic_polynom(x_coordinate)
            result.append((x_coordinate, y_coordinate))
            x_coordinate += step_x
    return result


if __name__ == '__main__':
    test_data = [(1.0, 3.8), (1.2, 3.2), (1.4, 2.9), (1.6, 3.0), (1.8, 4.2), (2.0, 4.8)]
    result =  build_cubic_spline(test_data, step_x=0.01)

    logger.debug(f"{len(result)=};\n{result}")

