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

    pretty_header = []
    for i, val in enumerate(row):
        spaces_to_add = details.col_lengths[i] - len(val)
        spaces_to_add += len(colors[i % len(colors)])
        pretty_header.append(
            ' ' + val + Style.RESET_ALL +
            (' ' * spaces_to_add) + ' ',
        )

    print('|', end='')
    writer.writerow(pretty_header)
    print('|')

    tilde_row = []
    print('|', end='')
    for i, length in details.col_lengths.items():
        spaces_to_add = length
        tilde_row.append(' ' + ('~' * spaces_to_add) + ' ')
    writer.writerow(tilde_row)
    print('|')


def fmt_row(row: List[str], details: CsvDetails) -> List[str]:
    if details.pretty:
        pretty_row = []
        for i, val in enumerate(row):
            spaces_to_add = details.col_lengths[i] - len(val)
            spaces_to_add += len(colors[i % len(colors)])
            if i == details.last_col:
                spaces_to_add += len(Style.RESET_ALL)
            pretty_row.append(
                ' ' + val + Style.RESET_ALL +
                (' ' * spaces_to_add) + ' ',
            )
    else:
        pretty_row = row
    return pretty_row


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
            out[-1] = out[-1] + Style.RESET_ALL
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


def run(path: str = '', delimiter: str = ',', pretty: bool = False) -> None:
    if not path:
        tmp = tempfile.NamedTemporaryFile()
        path = tmp.name
        Path(path).write_text(sys.stdin.read())

    details = CsvDetails(path, delimiter, pretty)
    rainbow_csv(details)


def main() -> None:
    try:
        fire.Fire(run)
    except (BrokenPipeError, OSError):
        pass


if __name__ == '__main__':
    main()
