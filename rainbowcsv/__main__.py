import csv
import sys
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional, TypeVar

import fire
from colorama import Fore, Style

if TYPE_CHECKING:
    # https://github.com/python/mypy/issues/5107#issuecomment-529372406
    F = TypeVar('F')
    def lru_cache() -> F: pass
else:
    from functools import lru_cache


colors = [
    Fore.RED,
    Fore.GREEN,
    Fore.YELLOW,
    Fore.BLUE,
    Fore.MAGENTA,
    Fore.CYAN,
]


class CsvDetails:
    def __init__(
        self,
        path: str,
        delimiter: str,
        pretty: bool,
        max_width: Optional[int],
    ):
        self.path = Path(path)
        self.delimiter = delimiter
        self.pretty = pretty
        self.max_width = max_width

    @property  # type: ignore
    @lru_cache()
    def col_widths(self) -> Any:
        widths: Dict[int, int] = {}
        with open(self.path) as f:
            reader = csv.reader(f, delimiter=self.delimiter)
            for row in reader:
                for i, val in enumerate(row):
                    widths[i] = max(widths.get(i, 0), len(val))

        for i, width in widths.items():
            if self.max_width and self.max_width < width:
                widths[i] = self.max_width
        return widths


def pretty_row(
    writer: Any,
    row: List[str],
    details: CsvDetails,
) -> None:
    for i, val in enumerate(row):
        len_color = len(colors[i % len(colors)])
        n_spaces = details.col_widths[i] - len(val) + len_color
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
                col = color + col

                if details.max_width and len(col) > details.max_width:
                    col = col[:details.max_width + len(color) - 1]
                    col += '…'  # special one-char ellipsis
                row[col_no] = col

            if details.pretty:
                pretty_row(writer, row, details)
                if row_no == 0:
                    pretty_tildes(writer, details)
            else:
                writer.writerow(row)

    # reset color at end, helps for the next prompt
    print(Style.RESET_ALL, end='')


def run(
    file: str = '',
    delimiter: str = ',',
    pretty: bool = False,
    max_width: Optional[int] = None,
) -> None:
    if not file:
        tmp = tempfile.NamedTemporaryFile()
        file = tmp.name
        Path(file).write_text(sys.stdin.read())

    details = CsvDetails(file, delimiter, pretty, max_width)
    rainbow_csv(details)


def main() -> None:
    try:
        fire.Fire(run)
    except (BrokenPipeError, OSError):
        pass


if __name__ == '__main__':
    main()
