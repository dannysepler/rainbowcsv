import csv
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
        self._col_lengths: Dict[int, int] = {}

    @property
    def col_lengths(self) -> Dict[int, int]:
        if self._col_lengths:
            return self._col_lengths

        lengths: Dict[int, int] = {}
        with open(self.path) as f:
            reader = csv.reader(f, delimiter=self.delimiter)
            for row in reader:
                for i, val in enumerate(row):
                    col_len = len(val)
                    if col_len > lengths.get(i, 0):
                        lengths[i] = col_len
        self._col_lengths = lengths
        return lengths

    @property
    def last_col(self) -> int:
        return max(self.col_lengths.keys())


def write_header(
    writer: Any,
    row: List[str],
    details: CsvDetails,
) -> None:
    if not details.pretty:
        writer.writerow(row)
        print()  # new line
        return

    for i, val in enumerate(row):
        n_spaces = details.col_lengths[i] - len(val)
        n_spaces += len(colors[i % len(colors)])
        row[i] = ' ' + val + Style.RESET_ALL + (' ' * n_spaces) + ' '

    print('|', end='')
    writer.writerow(row)
    print('|')

    tilde_row = []
    print('|', end='')
    for i, length in details.col_lengths.items():
        tilde_row.append(' ' + ('~' * length) + ' ')
    writer.writerow(tilde_row)
    print('|')


def fmt_row(row: List[str], details: CsvDetails) -> List[str]:
    if details.pretty:
        for i, val in enumerate(row):
            n_spaces = details.col_lengths[i] - len(val)
            n_spaces += len(colors[i % len(colors)])
            row[i] = ' ' + val + Style.RESET_ALL + (' ' * n_spaces) + ' '
    return row


def rainbow_csv(details: CsvDetails) -> None:
    out_delim = '|' if details.pretty else details.delimiter

    with open(details.path) as f:
        reader = csv.reader(f, delimiter=details.delimiter)
        writer = csv.writer(
            sys.stdout,
            delimiter=out_delim,
            quoting=csv.QUOTE_MINIMAL,
            lineterminator='',
        )
        for i_r, row in enumerate(reader):
            out = []
            for i_c, col in enumerate(row):
                out.append(f'{colors[i_c % len(colors)]}{col}')

            # clear the color at the end of each line
            if i_r == 0:
                write_header(writer, out, details)
            else:
                if details.pretty:
                    print('|', end='')
                out = fmt_row(out, details)
                writer.writerow(out)
                if details.pretty:
                    print('|')
                else:
                    print()  # new line


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
