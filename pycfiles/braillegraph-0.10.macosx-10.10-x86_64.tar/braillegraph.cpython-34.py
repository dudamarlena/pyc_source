# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/site-packages/braillegraph/braillegraph.py
# Compiled at: 2014-12-01 14:54:10
# Size of source mod 2**32: 9868 bytes
"""A library for creating graphs using Unicode braille characters.

https://pypi.python.org/pypi/braillegraph

Someone on reddit posted a screenshot of their xmobar setup, which used braille
characters to show the loads of their four processor cores, as well as several
other metrics. I was impressed that you could fit so much data into a single
line. I immediately set out to implement braille bar graphs for myself.

The characters this script outputs are in the Unicode Braille Patterns section,
code points 0x2800 through 0x28FF. Not all fonts support these characters, so
if you can't see the examples below check your font settings.

There are two ways to use this package: imported in Python code, or as a
command line script.

To use the package in Python, import it and use the vertical_graph and
horizontal_graph functions.

    >>> from braillegraph import vertical_graph, horizontal_graph
    >>> vertical_graph([3, 1, 4, 1])
    '⡯⠥'
    >>> horizontal_graph([3, 1, 4, 1])
    '⣆⣇'

To use the package as a script, run it as

    % python -m braillegraph vertical 3 1 4 1 5 9 2 6
    ⡯⠥
    ⣿⣛⣓⠒⠂
    % python -m braillegraph horizontal 3 1 4 1 5 9 2 6
    ⠀⠀⢀
    ⠀⠀⣸⢠
    ⣆⣇⣿⣼

For a description of the arguments and flags, run

    % python -m braillegraph --help
"""
import itertools
__all__ = [
 'vertical_graph', 'horizontal_graph']
_BRAILLE_EMPTY_BLOCK = 10240
_BRAILLE_HALF_ROW = [
 1, 2, 4, 64]
_BRAILLE_FULL_ROW = [9, 18, 36, 192]
_BRAILLE_FULL_COL = [
 71, 184]
_BRAILLE_PARTIAL_COL = [
 [
  64, 68, 70],
 [
  128, 160, 176]]

def _chunk(iterable, size):
    """Split an iterable into chunks of a fixed size."""
    args = (
     iter(iterable),) * size
    return (itertools.takewhile(lambda x: x is not None, group) for group in itertools.zip_longest(*args))


def _matrix_add_column(matrix, column, default=0):
    """Given a matrix as a list of lists, add a column to the right, filling in
    with a default value if necessary.
    """
    height_difference = len(column) - len(matrix)
    width = max(len(row) for row in matrix) if matrix else 0
    offset = 0
    if height_difference > 0:
        for _ in range(height_difference):
            matrix.insert(0, [default] * width)

    if height_difference < 0:
        offset = -height_difference
    for index, value in enumerate(column):
        row_index = index + offset
        row = matrix[row_index]
        width_difference = width - len(row)
        row.extend([default] * width_difference)
        row.append(value)


def vertical_graph(*args, sep='\n'):
    r"""Consume an iterable of integers and produce a vertical bar graph using
    braille characters.

    The graph is vertical in that its dependent axis is the vertical axis. Thus
    each value is represented as a row running left to right, and values are
    listed top to bottom.

    If the iterable contains more than four integers, it will be chunked into
    groups of four, separated with newlines by default.

        >>> vertical_graph([1, 2, 3, 4])
        '⣷⣄'
        >>> vertical_graph([1, 2, 3, 4, 5, 6])
        '⣷⣄\n⠛⠛⠓'
        >>> print(vertical_graph([1, 2, 3, 4, 5, 6]))
        ⣷⣄
        ⠛⠛⠓

    Alternately, the arguments can be passed directly:

        >>> vertical_graph(1, 2, 3, 4)
        '⣷⣄'

    The optional sep parameter controls how groups are separated. If sep is not
    passed (or if it is None), they are put on their own lines. For example, to
    keep everything on one line, space could be used:

        >>> vertical_graph(3, 1, 4, 1, 5, 9, 2, 6, sep=' ')
        '⡯⠥ ⣿⣛⣓⠒⠂'

    """
    lines = []
    if len(args) == 1:
        bars = args[0]
    else:
        bars = args
    if sep is None:
        sep = '\n'
    for bar_group in _chunk(bars, 4):
        line = []
        for braille_row, bar_value in enumerate(bar_group):
            full_blocks_needed = bar_value // 2
            blocks_needed = full_blocks_needed + bar_value % 2
            extra_blocks_needed = blocks_needed - len(line)
            if extra_blocks_needed > 0:
                line.extend([_BRAILLE_EMPTY_BLOCK] * extra_blocks_needed)
            for block_index in range(full_blocks_needed):
                line[block_index] += _BRAILLE_FULL_ROW[braille_row]

            if bar_value % 2:
                line[full_blocks_needed] += _BRAILLE_HALF_ROW[braille_row]
                continue

        lines.append(''.join(chr(code) for code in line))

    return sep.join(lines)


def horizontal_graph(*args):
    r"""Consume an iterable of integers and produce a horizontal bar graph using
    braille characters.

    The graph is horizontal in that its dependent axis is the horizontal axis.
    Thus each value is represented as a column running bottom to top, and
    values are listed left to right.

    The graph is anchored to the bottom, so columns fill in from the bottom of
    the current braille character and the next character is added on top when
    needed. For columns with no dots, the blank braille character is used, not
    a space character.

        >>> horizontal_graph([1, 2, 3, 4])
        '⣠⣾'
        >>> horizontal_graph([1, 2, 3, 4, 5, 6])
        '⠀⠀⣠\n⣠⣾⣿'
        >>> print(horizontal_graph([1, 2, 3, 4, 5, 6]))
        ⠀⠀⣠
        ⣠⣾⣿

    Alternately, the arguments can be passed directly:

        >>> horizontal_graph(1, 2, 3, 4)
        '⣠⣾'

    """
    lines = []
    if len(args) == 1:
        bars = args[0]
    else:
        bars = args
    for bar_group in _chunk(bars, 2):
        column = []
        for braille_col, bar_value in enumerate(bar_group):
            full_blocks_needed = bar_value // 4
            blocks_needed = full_blocks_needed + (1 if bar_value % 4 else 0)
            extra_blocks_needed = blocks_needed - len(column)
            column = [
             _BRAILLE_EMPTY_BLOCK] * extra_blocks_needed + column
            for block_index in range(-full_blocks_needed, 0, 1):
                column[block_index] += _BRAILLE_FULL_COL[braille_col]

            if bar_value % 4:
                partial_index = bar_value % 4 - 1
                column[(-blocks_needed)] += _BRAILLE_PARTIAL_COL[braille_col][partial_index]
                continue

        _matrix_add_column(lines, column, default=_BRAILLE_EMPTY_BLOCK)

    return '\n'.join(''.join(chr(code) for code in line) for line in lines)