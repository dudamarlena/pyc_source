# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/turicas/software/pyenv/versions/rows/lib/python3.6/site-packages/rows/plugins/txt.py
# Compiled at: 2019-02-13 03:47:25
# Size of source mod 2**32: 8764 bytes
from __future__ import unicode_literals
import re, unicodedata
from collections import defaultdict
from rows.plugins.utils import create_table, export_data, get_filename_and_fobj, serialize
single_frame_prefix = 'BOX DRAWINGS LIGHT'
double_frame_prefix = 'BOX DRAWINGS DOUBLE'
frame_parts = [name.strip() for name in '\n    VERTICAL, HORIZONTAL, DOWN AND RIGHT, DOWN AND LEFT,\n    UP AND RIGHT, UP AND LEFT, VERTICAL AND LEFT, VERTICAL AND RIGHT,\n    DOWN AND HORIZONTAL, UP AND HORIZONTAL,\n    VERTICAL AND HORIZONTAL'.split(',')]
SINGLE_FRAME = {name.strip():unicodedata.lookup(' '.join((single_frame_prefix, name.strip()))) for name in frame_parts}
DOUBLE_FRAME = {name.strip():unicodedata.lookup(' '.join((double_frame_prefix, name.strip()))) for name in frame_parts}
ASCII_FRAME = {name:'+' for name in frame_parts}
ASCII_FRAME['HORIZONTAL'] = '-'
ASCII_FRAME['VERTICAL'] = '|'
NONE_FRAME = defaultdict(lambda : ' ')
FRAMES = {'none':NONE_FRAME, 
 'ascii':ASCII_FRAME, 
 'single':SINGLE_FRAME, 
 'double':DOUBLE_FRAME}
del single_frame_prefix
del double_frame_prefix
del frame_parts
del NONE_FRAME
del ASCII_FRAME
del SINGLE_FRAME
del DOUBLE_FRAME
FRAME_SENTINEL = object()

def _parse_frame_style(frame_style):
    if frame_style is None:
        frame_style = 'None'
    try:
        FRAMES[frame_style.lower()]
    except KeyError:
        raise ValueError("Invalid frame style '{}'. Use one of 'None', 'ASCII', 'single' or 'double'.".format(frame_style))

    return frame_style


def _guess_frame_style(contents):
    first_line_chars = set(contents.split('\n')[0].strip())
    for frame_style, frame_dict in FRAMES.items():
        if first_line_chars <= set(frame_dict.values()):
            return frame_style

    return 'None'


def _parse_col_positions(frame_style, header_line):
    """Find the position for each column separator in the given line

    If frame_style is 'None', this won work
    for column names that _start_ with whitespace
    (which includes non-lefthand aligned column titles)
    """
    separator = re.escape(FRAMES[frame_style.lower()]['VERTICAL'])
    if frame_style == 'None':
        separator = '[\\s]{2}[^\\s]'
    col_positions = []
    re.sub(separator, lambda group: col_positions.append(group.start()), header_line)
    if frame_style == 'None':
        col_positions.append(len(header_line) - 1)
    return col_positions


def _max_column_sizes(field_names, table_rows):
    columns = zip(*[field_names] + table_rows)
    return {field_name:max(len(value) for value in column) for field_name, column in zip(field_names, columns)}


def import_from_txt(filename_or_fobj, encoding='utf-8', frame_style=FRAME_SENTINEL, *args, **kwargs):
    """Return a rows.Table created from imported TXT file."""
    filename, fobj = get_filename_and_fobj(filename_or_fobj, mode='rb')
    raw_contents = fobj.read().decode(encoding).rstrip('\n')
    if frame_style is FRAME_SENTINEL:
        frame_style = _guess_frame_style(raw_contents)
    else:
        frame_style = _parse_frame_style(frame_style)
    contents = raw_contents.splitlines()
    del raw_contents
    if frame_style != 'None':
        contents = contents[1:-1]
        del contents[1]
    else:
        if not contents[1].strip():
            del contents[1]
    col_positions = _parse_col_positions(frame_style, contents[0])
    table_rows = [[row[start + 1:end].strip() for start, end in zip(col_positions, col_positions[1:])] for row in contents]
    meta = {'imported_from':'txt', 
     'filename':filename, 
     'encoding':encoding, 
     'frame_style':frame_style}
    return create_table(table_rows, *args, meta=meta, **kwargs)


def export_to_txt(table, filename_or_fobj=None, encoding=None, frame_style='ASCII', safe_none_frame=True, *args, **kwargs):
    """Export a `rows.Table` to text.

    This function can return the result as a string or save into a file (via
    filename or file-like object).

    `encoding` could be `None` if no filename/file-like object is specified,
    then the return type will be `six.text_type`.
    `frame_style`: will select the frame style to be printed around data.
    Valid values are: ('None', 'ASCII', 'single', 'double') - ASCII is default.
    Warning: no checks are made to check the desired encoding allows the
    characters needed by single and double frame styles.

    `safe_none_frame`: bool, defaults to True. Affects only output with
    frame_style == "None":
    column titles are left-aligned and have
    whitespace replaced for "_".  This enables
    the output to be parseable. Otherwise, the generated table will look
    prettier but can not be imported back.
    """
    frame_style = _parse_frame_style(frame_style)
    frame = FRAMES[frame_style.lower()]
    serialized_table = serialize(table, *args, **kwargs)
    field_names = next(serialized_table)
    table_rows = list(serialized_table)
    max_sizes = _max_column_sizes(field_names, table_rows)
    dashes = [frame['HORIZONTAL'] * (max_sizes[field] + 2) for field in field_names]
    if frame_style != 'None' or not safe_none_frame:
        header = [field.center(max_sizes[field]) for field in field_names]
    else:
        header = [field.replace(' ', '_').ljust(max_sizes[field]) for field in field_names]
    header = '{0} {1} {0}'.format(frame['VERTICAL'], ' {} '.format(frame['VERTICAL']).join(header))
    top_split_line = frame['DOWN AND RIGHT'] + frame['DOWN AND HORIZONTAL'].join(dashes) + frame['DOWN AND LEFT']
    body_split_line = frame['VERTICAL AND RIGHT'] + frame['VERTICAL AND HORIZONTAL'].join(dashes) + frame['VERTICAL AND LEFT']
    botton_split_line = frame['UP AND RIGHT'] + frame['UP AND HORIZONTAL'].join(dashes) + frame['UP AND LEFT']
    result = []
    if frame_style != 'None':
        result += [top_split_line]
    result += [header, body_split_line]
    for row in table_rows:
        values = [value.rjust(max_sizes[field_name]) for field_name, value in zip(field_names, row)]
        row_data = ' {} '.format(frame['VERTICAL']).join(values)
        result.append('{0} {1} {0}'.format(frame['VERTICAL'], row_data))

    if frame_style != 'None':
        result.append(botton_split_line)
    result.append('')
    data = '\n'.join(result)
    if encoding is not None:
        data = data.encode(encoding)
    return export_data(filename_or_fobj, data, mode='wb')