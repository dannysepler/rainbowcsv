import pytest

from rainbowcsv.__main__ import run


@pytest.fixture
def f(tmp_path):
    return tmp_path / 'f.csv'


def test_run(f, capsys):
    f.write_text('a,b,c\n1,2,3')
    run(str(f))

    captured = capsys.readouterr()
    lines = captured.out.splitlines()
    assert len(lines) == 2
    for line in lines:
        assert len(line.split('|')) == 1


def test_pretty(f, capsys):
    f.write_text('a,b,c\n1,2,3')
    run(str(f), pretty=True)

    captured = capsys.readouterr()
    lines = captured.out.splitlines()
    assert len(lines) == 3  # adds tilde line
    for line in lines:
        assert len(line.split('|')) == 3 + 2


def test_using_comma_delim_on_non_comma_out(f, capsys):
    f.write_text('a&b&c\n1&2&3')
    run(str(f), pretty=True)

    captured = capsys.readouterr()
    for line in captured.out.splitlines():
        assert len(line.split('|')) == 1 + 2


def test_using_non_comma_delim_on_non_comma_out(f, capsys):
    f.write_text('a&b&c\n1&2&3')
    run(str(f), pretty=True, delimiter='&')

    captured = capsys.readouterr()
    for line in captured.out.splitlines():
        assert len(line.split('|')) == 3 + 2
