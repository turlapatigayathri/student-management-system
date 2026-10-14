import unittest
from app import calculate_results


class GradeCalculationTests(unittest.TestCase):
    def test_high_marks(self):
        self.assertEqual(calculate_results(90, 90, 90), (270, 90.0, "A+"))

    def test_average_grade(self):
        self.assertEqual(calculate_results(80, 70, 60), (210, 70.0, "B"))

    def test_fail_grade(self):
        self.assertEqual(calculate_results(30, 40, 50), (120, 40.0, "F"))


if __name__ == "__main__":
    unittest.main()
