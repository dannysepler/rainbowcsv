import pytest
from colorama import Style

from rainbowcsv.__main__ import colors, run

C = colors
RESET = Style.RESET_ALL


@pytest.fixture
def f(tmp_path):
    return tmp_path / 'f.csv'


def out_lines(capsys):
    captured = capsys.readouterr()
    return captured.out.splitlines()


def test_run(f, capsys):
    f.write_text('a,b,c\n1,2,3')
    run(str(f))

    lines = out_lines(capsys)
    assert len(lines) == 2
    for line in lines:
        assert len(line.split('|')) == 1


def test_run_contents(f, capsys):
    f.write_text('a,b,c\n1,2,3')
    run(str(f))

    assert out_lines(capsys) == [
        f'{C[0]}a,{C[1]}b,{C[2]}c',
        f'{C[0]}1,{C[1]}2,{C[2]}3',
    ]


def test_pretty(f, capsys):
    f.write_text('a,b,c\n1,2,3')
    run(str(f), pretty=True)

    lines = out_lines(capsys)
    assert len(lines) == 3  # adds tilde line
    for line in lines:
        assert len(line.split('|')) == 3 + 2


def test_pretty_contents(f, capsys):
    f.write_text('a,b,c\n1,2,3')
    run(str(f), pretty=True)

    assert out_lines(capsys) == [
        f'| {C[0]}a{RESET} | {C[1]}b{RESET} | {C[2]}c{RESET} |',
        '| ~ | ~ | ~ |',
        f'| {C[0]}1{RESET} | {C[1]}2{RESET} | {C[2]}3{RESET} |',
    ]


def test_pretty_contents_on_different_col_lengths(f, capsys):
    f.write_text('a,b,ccc\n11,2,3')
    run(str(f), pretty=True)

    assert out_lines(capsys) == [
        # note the spaces after each header
        f'| {C[0]}a{RESET}  | {C[1]}b{RESET} | {C[2]}ccc{RESET} |',
        # note the number of tildes
        '| ~~ | ~ | ~~~ |',
        # note the spaces after each column
        f'| {C[0]}11{RESET} | {C[1]}2{RESET} | {C[2]}3{RESET}   |',
    ]


def test_using_incorrect_delim_on_non_comma_out(f, capsys):
    f.write_text('a&b&c\n1&2&3')
    run(str(f), pretty=True)

    for line in out_lines(capsys):
        assert len(line.split('|')) == 1 + 2


def test_using_proper_delim_on_non_comma_out(f, capsys):
    f.write_text('a&b&c\n1&2&3')
    run(str(f), pretty=True, delimiter='&')

    for line in out_lines(capsys):
        assert len(line.split('|')) == 3 + 2


def test_long_entry_is_truncated(f, capsys):
    f.write_text('entry\na really really really long entry')
    run(str(f), pretty=True, max_width=10)

    assert out_lines(capsys) == [
        f'| {C[0]}entry{RESET}      |',
        f"| {'~' * 10} |",
        f'| {C[0]}a really …{RESET} |',
    ]


def test_long_entry_is_not_truncated_when_no_max(f, capsys):
    entry = 'a really really really long entry'
    f.write_text(f'entry\n{entry}')
    run(str(f), pretty=True)

    assert out_lines(capsys) == [
        f'| {C[0]}entry{RESET}                             |',
        f"| {'~' * len(entry)} |",
        f'| {C[0]}a really really really long entry{RESET} |',
    ]


def test_long_entry_is_truncated_when_not_pretty(f, capsys):
    f.write_text('entry\na really really really long entry')
    run(str(f), max_width=10)

    assert out_lines(capsys) == [
        f'{C[0]}entry',
        f'{C[0]}a really …',
    ]
