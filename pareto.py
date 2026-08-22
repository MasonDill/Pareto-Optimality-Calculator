import argparse as ap
import csv
from decimal import Decimal, InvalidOperation
import logging
from pathlib import Path
import sys
from typing import Iterable, Sequence


LOGGER = logging.getLogger(__name__)


def _as_decimal(value, row_number: int, column_number: int) -> Decimal:
    try:
        number = Decimal(str(value).strip())
    except (InvalidOperation, ValueError) as error:
        raise ValueError(
            f"row {row_number}, column {column_number}: {value!r} is not numeric"
        ) from error
    if not number.is_finite():
        raise ValueError(
            f"row {row_number}, column {column_number}: values must be finite"
        )
    return number


def normalize_data(data: Iterable[Sequence[object]]) -> list[tuple[Decimal, ...]]:
    """Validate points and convert their coordinates to exact decimals."""
    points: list[tuple[Decimal, ...]] = []
    dimensions = None

    for row_number, row in enumerate(data, start=1):
        point = tuple(
            _as_decimal(value, row_number, column_number)
            for column_number, value in enumerate(row, start=1)
        )
        if not point:
            raise ValueError(f"row {row_number}: an outcome must have at least one value")
        if dimensions is None:
            dimensions = len(point)
        elif len(point) != dimensions:
            raise ValueError(
                f"row {row_number}: expected {dimensions} values, found {len(point)}"
            )
        points.append(point)

    if not points:
        raise ValueError("no outcomes were found")
    return points


def dominates(candidate: Sequence[Decimal], outcome: Sequence[Decimal]) -> bool:
    """Return whether candidate is no worse everywhere and better somewhere."""
    return all(left >= right for left, right in zip(candidate, outcome)) and any(
        left > right for left, right in zip(candidate, outcome)
    )


def find_pareto(data, verbose=False):
    """Return the unique, non-dominated points, preserving input order."""
    points = normalize_data(data)
    unique_points = list(dict.fromkeys(points))
    optimal_solutions = []

    for outcome in unique_points:
        LOGGER.debug("Analyzing outcome: %s", outcome)
        dominator = next(
            (candidate for candidate in unique_points if dominates(candidate, outcome)),
            None,
        )
        if dominator is None:
            optimal_solutions.append(outcome)
            LOGGER.debug("  Pareto optimal")
        else:
            LOGGER.debug("  Dominated by %s", dominator)

    return optimal_solutions


def read_file(file_name, has_header=False):
    """Read numeric CSV rows, allowing blank lines and # comments."""
    rows = []
    header_pending = has_header

    with Path(file_name).open("r", encoding="utf-8", newline="") as source:
        for line_number, raw_line in enumerate(source, start=1):
            content = raw_line.split("#", 1)[0].strip()
            if not content:
                continue
            try:
                row = next(csv.reader([content], strict=True))
            except csv.Error as error:
                raise ValueError(f"line {line_number}: invalid CSV: {error}") from error
            if header_pending:
                header_pending = False
                continue
            rows.append((line_number, row))

    if header_pending:
        raise ValueError("the input contains no header row")
    if not rows:
        raise ValueError("no outcomes were found")

    dimensions = len(rows[0][1])
    normalized = []
    for line_number, row in rows:
        if len(row) != dimensions:
            raise ValueError(
                f"line {line_number}: expected {dimensions} values, found {len(row)}"
            )
        normalized.append(
            tuple(
                _as_decimal(value, line_number, column_number)
                for column_number, value in enumerate(row, start=1)
            )
        )
    return normalized


def format_number(number: Decimal) -> str:
    return format(number, "f")

if __name__ == "__main__":
    parser = ap.ArgumentParser(description='Find Pareto optimal solutions from a CSV file.')
    parser.add_argument('input_file', help='Input CSV file containing the data')
    parser.add_argument(
        "--header", action="store_true", help="Skip the first non-comment row"
    )
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Enable verbose comparison output')
    
    args = parser.parse_args()
    
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.WARNING,
        format="%(message)s",
    )
    try:
        data = read_file(args.input_file, has_header=args.header)
        solutions = find_pareto(data, args.verbose)
    except (OSError, ValueError) as error:
        parser.error(str(error))

    writer = csv.writer(sys.stdout, lineterminator="\n")
    for solution in solutions:
        writer.writerow(format_number(value) for value in solution)
