# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/xmlreport.py
# Compiled at: 2015-09-01 07:17:44
"""A collection of tools for rendering information about xml (typically errors)"""
from __future__ import unicode_literals
from __future__ import print_function

def extract_lines(code, line, padding=2):
    """Extracts a number of lines from code surrounding a given line number,
    returns a list of tuples that contain the line number (1 indexed) and the line text.

    """
    lines = code.splitlines()
    start = max(0, line - padding - 1)
    end = min(len(lines), line + padding - 1)
    showlines = lines[start:end + 1]
    linenos = [ n + 1 for n in range(start, end + 1) ]
    return zip(linenos, showlines)


def extract(code, line, padding=3):
    lines = extract_lines(code, line, padding)
    start = lines[0][0]
    text = (b'\n').join(l[1] for l in lines)
    return (start, text)


def number(code, linestart=1, highlight_line=-1, number_wrap=None):
    if number_wrap is None:
        number_wrap = lambda n: n
    lines = code.splitlines()
    max_line = max(6, max(len(str(len(l))) for l in lines))
    out_lines = []
    for lineno, line in zip(range(linestart, linestart + len(lines)), lines):
        if lineno == highlight_line:
            number = (b'*%i ' % lineno).rjust(max_line)
        else:
            number = (b'%i ' % lineno).rjust(max_line)
        out_lines.append(number + line)

    return (b'\n').join(out_lines)


def column_to_spaces(line, col):
    """Returns the number of space required to reach a point in a string"""
    spaces = 0
    for colno, char in enumerate(line):
        spaces += 4 if col == b'\t' else 1
        if colno + 1 == col:
            return spaces

    return spaces


def render_error(code, show_lineno, padding=3, col=None, colors=False, col_text=b'here'):
    lines = extract_lines(code, show_lineno, padding=padding)
    linenos = [ str(lineno) for lineno, _ in lines ]
    maxlineno = max(len(l) for l in linenos)
    render_lines = []
    for lineno, line in lines:
        if lineno == show_lineno:
            fmt = b'*%s %s'
        else:
            fmt = b' %s %s'
        render_lines.append(fmt % (str(lineno).ljust(maxlineno), line))
        if col is not None and lineno == show_lineno:
            point_at = column_to_spaces(line, col)
            pad = b' ' * (maxlineno + 1)
            if point_at > len(col_text) + 1:
                render_lines.append(pad + (col_text + b' ^').rjust(point_at + 1))
            else:
                render_lines.append(pad + (b'^').rjust(point_at + 1) + b' ' + col_text)

    return (b'\n').join(line.replace(b'\t', b'    ') for line in render_lines)


if __name__ == b'__main__':
    xml = b'<moya xmlns="http://moyaproject.com">\n\n<mountpoint name="testmount" libname="root">\n    <url name="article" url="/{year}/{month}/{day}/{slug}/" methods="GET" target="viewpost">\n        <debug>url main: ${url.year}, ${url.month}, ${url.day}, ${url.slug}</debug>\n    </url>\n    <url name="front" url="/" methods="GET">\n        <debug>Front...</debug>\n        <return><str>Front</str></return>\n    </url>\n</mountpoint>\n\n<macro docname="viewpost">\n    <debugIn viewpost</debug>\n    <return><str>Hello, World</str></return>\n    <return>\n        <response template="birthday.html">\n            <str dst="title">My Birthday</str>\n            <str dst="body">It was my birthday today!</str>\n        </response>\n    </return>\n</macro>\n\n<!--\n<macro libname="showapp">\n    <debug>App is ${app}</debug>\n</macro>\n\n<macro libname="blogmacro">\n    <debug>Called blogmacro in blog lib</debug>\n</macro>\n\n<macro libname="blogmacro2">\n    <debug>Called blogmacro2 with app: ${debug:app}</debug>\n</macro>\n-->\n\n</moya>'
    print(render_error(xml, 14, col=5))