# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/luto/snotes20/osf.py/venv/lib/python3.4/site-packages/osf/parse.py
# Compiled at: 2015-08-23 11:29:24
# Size of source mod 2**32: 1645 bytes
from .grammar import Line
from .classes import Header
from modgrammar import ParseError
LineParser = Line.parser()

def parse_line(line):
    line = line.strip()
    if not line:
        return
    return LineParser.parse_string(line)


def parse_header_line(line, header):
    if len(line) == 0:
        return
    colon_pos = line.find(':')
    if colon_pos == -1:
        header.v.append(line)
    else:
        k = line[:colon_pos].lower()
        v = line[colon_pos + 1:].strip()
        header.kv[k] = v


def parse_header(lines):
    header_start = -1
    header_end = -1
    header = None
    num = -1
    for line in lines:
        line = line.strip()
        num += 1
        if line == 'HEADER' or line == 'HEAD':
            header_start = num
            header = Header()
            continue
        elif line == '/HEADER' or line == '/HEAD':
            if header_start != -1:
                header_end = num
                break
        if header_start != -1:
            parse_header_line(line, header)
            continue

    if header_start == -1 or header_end == -1:
        header_start = -1
        header = None
    return (header_start, header_end, header)


def parse_lines(lines):
    num = 0
    llines = []
    h_start, h_end, header = parse_header(lines)
    if h_start != -1:
        lines = lines[h_end + 1:]
    for line in lines:
        num += 1
        lline = None
        try:
            lline = parse_line(line)
        except ParseError as e:
            e.line = num
            llines.append(e)

        if lline:
            llines.append(lline)
            lline._line = num
            continue

    return (
     header, llines)