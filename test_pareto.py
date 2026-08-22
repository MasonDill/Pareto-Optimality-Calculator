from decimal import Decimal
import os
import tempfile
import unittest

from pareto import dominates, find_pareto, read_file


class ParetoTests(unittest.TestCase):
    def test_dominance_requires_one_strict_improvement(self):
        point = (Decimal("1"), Decimal("2"))
        self.assertFalse(dominates(point, point))
        self.assertTrue(dominates((Decimal("2"), Decimal("2")), point))
        self.assertFalse(dominates((Decimal("2"), Decimal("1")), point))

    def test_finds_frontier_in_input_order(self):
        data = [[-1, -1], [-5, 0], [0, -5], [-2, -2]]
        self.assertEqual(
            find_pareto(data),
            [
                (Decimal("-1"), Decimal("-1")),
                (Decimal("-5"), Decimal("0")),
                (Decimal("0"), Decimal("-5")),
            ],
        )

    def test_numeric_duplicates_are_returned_once(self):
        self.assertEqual(
            find_pareto([["1", "1.0"], ["01", "1.00"]]),
            [(Decimal("1"), Decimal("1.0"))],
        )

    def test_decimal_values_are_supported(self):
        self.assertEqual(
            find_pareto([["1.5", "2"], ["1.25", "2"]]),
            [(Decimal("1.5"), Decimal("2"))],
        )

    def test_mismatched_dimensions_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "expected 1 values, found 2"):
            find_pareto([[1], [2, 3]])

    def test_non_finite_values_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "finite"):
            find_pareto([["NaN", 1]])

    def test_reader_handles_header_comments_and_blank_lines(self):
        contents = "name_a,name_b\n\n1.5,2 # first outcome\n3, 4\n"
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "points.csv")
            with open(path, "w", encoding="utf-8") as output:
                output.write(contents)
            self.assertEqual(
                read_file(path, has_header=True),
                [(Decimal("1.5"), Decimal("2")), (Decimal("3"), Decimal("4"))],
            )

    def test_reader_reports_physical_line_for_invalid_number(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "points.csv")
            with open(path, "w", encoding="utf-8") as output:
                output.write("\n1,nope\n")
            with self.assertRaisesRegex(ValueError, "row 2, column 2"):
                read_file(path)


if __name__ == "__main__":
    unittest.main()
