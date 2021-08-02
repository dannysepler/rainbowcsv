rainbowcsv
==========

Outputs csv columns in easy-to-discern colors in the terminal.

## Installation

`pip install rainbowcsv`

## Usage

Use on a file

`rainbowcsv path/to/file.csv`

or use with pipes

`cat path/to/file.csv | rainbowcsv`

## Options

Append `--help` to show available arguments.

## How it works

`rainbowcsv` uses the colorama library to append extra color-changing characters around each csv column.

## Usage advice

[csvkit](https://csvkit.readthedocs.io/en/latest/) is a lovely library, and we recommend using this in conjunction with it.

The `csvlook` command doesn't play well with rainbow csv, because it doesn't know to ignore color-changing characters. That's why the `--pretty` option is available in `rainbowcsv`, it creates a similar-looking table.
