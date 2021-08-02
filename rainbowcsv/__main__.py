import csv
from functools import lru_cache
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List

import fire
from colorama import Fore, Style

colors = [
    Fore.RED,
    Fore.GREEN,
    Fore.YELLOW,
    Fore.BLUE,
    Fore.MAGENTA,
    Fore.CYAN,
]


class CsvDetails:
    def __init__(self, path: str, delimiter: str, pretty: bool):
        self.path = Path(path)
        self.delimiter = delimiter
        self.pretty = pretty

    @property
    @lru_cache()
    def col_widths(self) -> Dict[int, int]:
        widths: Dict[int, int] = {}
        with open(self.path) as f:
            reader = csv.reader(f, delimiter=self.delimiter)
            for row in reader:
                for i, val in enumerate(row):
                    cur_max = widths.get(i, 0)
                    widths[i] = max(widths.get(i, 0), len(val))
        return widths


def pretty_row(
    writer: Any,
    row: List[str],
    details: CsvDetails,
) -> None:
    for i, val in enumerate(row):
        n_spaces = details.col_widths[i] - len(val)
        n_spaces += len(colors[i % len(colors)])
        row[i] = ' ' + val + Style.RESET_ALL + (' ' * n_spaces) + ' '

    # insert '|' at start and end
    writer.writerow([''] + row + [''])


def pretty_tildes(writer: Any, details: CsvDetails) -> None:
    row = [f" {'~' * width} " for width in details.col_widths.values()]

    # insert '|' at start and end
    writer.writerow([''] + row + [''])


def rainbow_csv(details: CsvDetails) -> None:
    out_delim = '|' if details.pretty else details.delimiter

    with open(details.path) as f:
        reader = csv.reader(f, delimiter=details.delimiter)
        writer = csv.writer(
            sys.stdout,
            delimiter=out_delim,
            quoting=csv.QUOTE_MINIMAL,
        )
        for row_no, row in enumerate(reader):
            for col_no, col in enumerate(row):
                color = colors[col_no % len(colors)]
                row[col_no] = color + col

            if details.pretty:
                pretty_row(writer, row, details)
                if row_no == 0:
                    pretty_tildes(writer, details)
            else:
                writer.writerow(row)


def run(file: str = '', delimiter: str = ',', pretty: bool = False) -> None:
    if not file:
        tmp = tempfile.NamedTemporaryFile()
        file = tmp.name
        Path(file).write_text(sys.stdin.read())

    details = CsvDetails(file, delimiter, pretty)
    rainbow_csv(details)


def main() -> None:
    try:
        fire.Fire(run)
    except (BrokenPipeError, OSError):
        pass


if __name__ == '__main__':
    main()
