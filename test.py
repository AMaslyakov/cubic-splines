import unittest
import csv
import logging
logging.basicConfig(level=logging.CRITICAL)
from splines import *

def read_data(file):
    with open(file, "r", encoding="utf8") as f:
        reader = csv.DictReader(f, delimiter=',')
        result = [Points(float(row["x"]), float(row["y"])) for row in reader]
        return result

class TestSplines(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.CSV_FILE = "input_data.csv"
        cls.test_data = read_data(cls.CSV_FILE)
        cls.y = list(map(lambda p: p.y, cls.test_data))
        cls.x = list(map(lambda p: p.x, cls.test_data))
        cls.segments = select_segments(cls.x)
        cls.h_i = calculate_h_i(cls.segments)
        cls.coefficients = tridiagonal_coefficients(cls.y, cls.h_i)
        cls.U = calculate_U(cls.coefficients)
        cls.V = calculate_V(cls.coefficients)
        cls.c_i = calculate_c_i(cls.y, cls.h_i)

    def test_variant(self):
        """Тест проверяет корректность загрузки исходных данных из CSV файла"""
        print(f"\n=== Тест загрузки данных ===")
        print(f"Загруженные данные из {self.CSV_FILE}:")
        for i, point in enumerate(self.test_data):
            print(f"  Точка {i+1}: x={point.x}, y={point.y}")
        
        source_data = [
            Points(1.0, 3.8),
            Points(1.2, 3.2),
            Points(1.4, 2.9),
            Points(1.6, 3.0),
            Points(1.8, 4.2),
            Points(2.0, 4.8),
        ]
        
        print(f"Ожидаемые данные:")
        for i, point in enumerate(source_data):
            print(f"  Точка {i+1}: x={point.x}, y={point.y}")
        
        self.assertListEqual(self.test_data, source_data)
        print("✓ Данные загружены корректно")

    @unittest.skip
    def test_get_ai(self):
        """Тест проверяет корректность вычисления коэффициентов a_i"""
        print(f"\n=== Тест вычисления коэффициентов a_i ===")
        
        test_a_i = get_a_i(self.y)
        expected_a_i = [3.8, 3.2, 2.9, 3.0, 4.2]
        
        print(f"Исходные значения y: {self.y}")
        print(f"Вычисленные a_i: {test_a_i}")
        print(f"Ожидаемые a_i: {expected_a_i}")
        
        for i, (computed, expected) in enumerate(zip(test_a_i, expected_a_i)):
            print(f"  a_{i} = {computed} (ожидается {expected})")
        
        self.assertListEqual(test_a_i, expected_a_i)
        print("✓ Коэффициенты a_i вычислены корректно")

    @unittest.skip
    def test_coefficient_0(self):
        """Тест проверяет первый коэффициент тридиагональной системы"""
        print(f"\n=== Тест коэффициента 0 ===")
        
        expected_coeff = Coefficient_c_i(0, 0.8, 0.2, 4.5)
        actual_coeff = self.coefficients[0]
        
        print(f"Ожидаемый коэффициент: p={expected_coeff.p}, q={expected_coeff.q}, l={expected_coeff.l}, s={expected_coeff.s}")
        print(f"Фактический коэффициент: p={actual_coeff.p}, q={actual_coeff.q}, l={actual_coeff.l}, s={actual_coeff.s}")
        
        self.assertAlmostEqual(actual_coeff.p, expected_coeff.p, places=3, msg="Коэффициент p не совпадает")
        self.assertAlmostEqual(actual_coeff.q, expected_coeff.q, places=3, msg="Коэффициент q не совпадает")
        self.assertAlmostEqual(actual_coeff.l, expected_coeff.l, places=3, msg="Коэффициент l не совпадает")
        self.assertAlmostEqual(actual_coeff.s, expected_coeff.s, places=3, msg="Коэффициент s не совпадает")
        print("✓ Коэффициент 0 корректен")

    @unittest.skip
    def test_coefficient_1(self):
        """Тест проверяет второй коэффициент тридиагональной системы"""
        print(f"\n=== Тест коэффициента 1 ===")
        
        expected_coeff = Coefficient_c_i(0.2, 0.8, 0.2, 6)
        actual_coeff = self.coefficients[1]
        
        print(f"Ожидаемый коэффициент: p={expected_coeff.p}, q={expected_coeff.q}, l={expected_coeff.l}, s={expected_coeff.s}")
        print(f"Фактический коэффициент: p={actual_coeff.p}, q={actual_coeff.q}, l={actual_coeff.l}, s={actual_coeff.s}")
        
        self.assertAlmostEqual(actual_coeff.p, expected_coeff.p, places=3, msg="Коэффициент p не совпадает")
        self.assertAlmostEqual(actual_coeff.q, expected_coeff.q, places=3, msg="Коэффициент q не совпадает")
        self.assertAlmostEqual(actual_coeff.l, expected_coeff.l, places=3, msg="Коэффициент l не совпадает")
        self.assertAlmostEqual(actual_coeff.s, expected_coeff.s, places=3, msg="Коэффициент s не совпадает")
        print("✓ Коэффициент 1 корректен")

    @unittest.skip
    def test_coefficient_2(self):
        """Тест проверяет третий коэффициент тридиагональной системы"""
        print(f"\n=== Тест коэффициента 2 ===")
        
        expected_coeff = Coefficient_c_i(0.2, 0.8, 0.2, 16.5)
        actual_coeff = self.coefficients[2]
        
        print(f"Ожидаемый коэффициент: p={expected_coeff.p}, q={expected_coeff.q}, l={expected_coeff.l}, s={expected_coeff.s}")
        print(f"Фактический коэффициент: p={actual_coeff.p}, q={actual_coeff.q}, l={actual_coeff.l}, s={actual_coeff.s}")
        
        self.assertAlmostEqual(actual_coeff.p, expected_coeff.p, places=3, msg="Коэффициент p не совпадает")
        self.assertAlmostEqual(actual_coeff.q, expected_coeff.q, places=3, msg="Коэффициент q не совпадает")
        self.assertAlmostEqual(actual_coeff.l, expected_coeff.l, places=3, msg="Коэффициент l не совпадает")
        self.assertAlmostEqual(actual_coeff.s, expected_coeff.s, places=3, msg="Коэффициент s не совпадает")
        print("✓ Коэффициент 2 корректен")

    @unittest.skip
    def test_coefficient_3(self):
        """Тест проверяет четвертый коэффициент тридиагональной системы"""
        print(f"\n=== Тест коэффициента 3 ===")
        
        expected_coeff = Coefficient_c_i(0.2, 0.8, 0, -9)
        actual_coeff = self.coefficients[3]
        
        print(f"Ожидаемый коэффициент: p={expected_coeff.p}, q={expected_coeff.q}, l={expected_coeff.l}, s={expected_coeff.s}")
        print(f"Фактический коэффициент: p={actual_coeff.p}, q={actual_coeff.q}, l={actual_coeff.l}, s={actual_coeff.s}")
        
        self.assertAlmostEqual(actual_coeff.p, expected_coeff.p, places=3, msg="Коэффициент p не совпадает")
        self.assertAlmostEqual(actual_coeff.q, expected_coeff.q, places=3, msg="Коэффициент q не совпадает")
        self.assertAlmostEqual(actual_coeff.l, expected_coeff.l, places=3, msg="Коэффициент l не совпадает")
        self.assertAlmostEqual(actual_coeff.s, expected_coeff.s, places=3, msg="Коэффициент s не совпадает")
        print("✓ Коэффициент 3 корректен")

    @unittest.skip
    def test_segments_calculation(self):
        """Тест проверяет корректность вычисления сегментов"""
        print(f"\n=== Тест вычисления сегментов ===")
        
        print(f"Исходные точки x: {self.x}")
        print(f"Вычисленные сегменты:")
        for i, segment in enumerate(self.segments):
            print(f"  Сегмент {i}: [{segment.x_l}, {segment.x_r}]")
        
        print(f"Вычисленные h_i: {self.h_i}")
        for i, h in enumerate(self.h_i):
            print(f"  h_{i} = {h}")
        
        # Проверяем, что сегменты вычислены корректно
        expected_segments = [
            Segment(1.0, 1.2),
            Segment(1.2, 1.4),
            Segment(1.4, 1.6),
            Segment(1.6, 1.8),
            Segment(1.8, 2.0)
        ]
        
        self.assertEqual(len(self.segments), len(expected_segments))
        for i, (actual, expected) in enumerate(zip(self.segments, expected_segments)):
            self.assertEqual(actual.x_l, expected.x_l, f"Левая граница сегмента {i} не совпадает")
            self.assertEqual(actual.x_r, expected.x_r, f"Правая граница сегмента {i} не совпадает")
        
        print("✓ Сегменты вычислены корректно")

    def test_U_2(self):
        u2 = -0.25
        self.assertAlmostEqual(u2, self.U[0], places=3, msg=f"u2 test:  {u2} != {self.U[0]}")
        print(f"u2: {u2} == {self.U[0]}")

    def test_U_3(self):
        u3 = -0.267
        self.assertAlmostEqual(u3, self.U[1], places=3, msg=f"u3 test:  {u3} != {self.U[1]}")
        print(f"u3: {u3} == {self.U[1]}")

    def test_U_4(self):
        u4 = -0.268
        self.assertAlmostEqual(u4, self.U[2], places=3, msg=f"u3 test:  {u4} != {self.U[2]}")
        print(f"u4: {u4} == {self.U[2]}")

    def test_U_5(self):
        u5 = 0
        self.assertEqual(u5, self.U[3], msg=f"u5 test:  {u5} != {self.U[3]}")
        print(f"u5: {u5} == {self.U[3]}")

# -------- V --------
    def test_V_2(self):
        v2 = 5.625
        self.assertAlmostEqual(v2, self.V[0], places=3, msg=f"v2 test:  {v2} != {self.V[0]}")
        print(f"v2: {v2} == {self.V[0]}")

    def test_V_3(self):
        v3 = 6.5
        self.assertAlmostEqual(v3, self.V[1], places=3, msg=f"v3 test:  {v3} != {self.V[1]}")
        print(f"v3: {v3} == {self.V[1]}")

    def test_V_4(self):
        v4 = 20.35896
        self.assertAlmostEqual(v4, self.V[2], places=2, msg=f"v3 test:  {v4} != {self.V[2]}")
        print(f"v4: {v4} == {self.V[2]}")

    def test_V_5(self):
        v5 = -17.513
        self.assertAlmostEqual(v5, self.V[3], places=2, msg=f"v5 test:  {v5} != {self.V[3]}")
        print(f"v5: {v5} == {self.V[3]}")

    def test_c_1(self):
        self.assertEqual(0.0, self.c_i[0])
        print(f"c1: {0.0} == {self.c_i[0]}")

    def test_c_2(self):
        c2 = 5.672
        self.assertAlmostEqual(c2, self.c_i[1], places=2)
        print(f"c2: {c2} == {self.c_i[1]}")
        
    def test_c_3(self):
        c3 = -0.18
        self.assertAlmostEqual(c3, self.c_i[2], places=2)
        print(f"c3: {c3} == {self.c_i[2]}")

    def test_c_4(self):
        c4 = 25.05
        self.assertAlmostEqual(c4, self.c_i[3], places=2)
        print(f"c4: {c4} == {self.c_i[3]}")

    def test_c_5(self):
        c5 = -17.51
        self.assertAlmostEqual(c5, self.c_i[4], places=2)
        print(f"c4: {c5} == {self.c_i[4]}")

if __name__ == "__main__":
    unittest.main(verbosity=2)


