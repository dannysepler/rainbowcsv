rainbowcsv
==========

Outputs csv columns in easy-to-discern colors in the terminal.

## Installation

`pip install rainbowcsv`

## Usage

Use on a file

`rainbowcsv path/to/file.csv`

or use with pipes

`curl https://raw.githubusercontent.com/dannysepler/rainbowcsv/main/resources/movies.csv | rainbowcsv`

![Simple rainbowcsv output](https://raw.githubusercontent.com/dannysepler/rainbowcsv/main/resources/simple_screenshot.png)

## Options

`rainbowcsv --help`

## How it works

`rainbowcsv` uses the colorama library to wrap csv columns with color escape sequences.

## Usage advice

[csvkit](https://csvkit.readthedocs.io/en/latest/) is a lovely library, and we recommend using this in conjunction with it.

The `csvlook` command doesn't play well with rainbow csv, because it doesn't ignore color-changing characters. That's why the `--table` (`-t` for short) option is available in `rainbowcsv`, it creates a similar-looking table.

`curl https://raw.githubusercontent.com/dannysepler/rainbowcsv/main/resources/movies.csv | rainbowcsv --table`

![Simple rainbowcsv output](https://raw.githubusercontent.com/dannysepler/rainbowcsv/main/resources/table_screenshot.png)

You can also pipe to `less` if you display raw control characters, via `less -r` or `less -R`
