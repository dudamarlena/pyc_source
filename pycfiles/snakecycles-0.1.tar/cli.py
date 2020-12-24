# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/flanker/Developer/Github/SnakeCycles/snakecycles/cli.py
# Compiled at: 2016-09-26 13:40:34
"""Core shell application.
Parse arguments and logger, use translated strings.
"""
from __future__ import unicode_literals
import codecs, re, sys
from networkx import DiGraph, simple_cycles
__author__ = b'mgallet'
__all__ = [
 b'main']

def str_or_none(value):
    if value == b'None':
        return None
    else:
        return value[1:-1]


def parse_line(line):
    """Parse a single output line
    looks like "(('/home/user/projects/name', 'script.py'), (None, None))"

    :param line:
    :return:
    """
    matcher = re.match(b"\\(\\(('.*'|None), ('.*'|None)\\), \\(('.*'|None), ('.*'|None)\\)\\)", line)
    if not matcher:
        raise ValueError(b'Invalid line: %s' % line)
    values = matcher.groups()
    return (str_or_none(x) for x in values)


def main():
    graph = DiGraph()
    stdin = sys.stdin
    if sys.version_info[0] == 2 and sys.stdin.encoding:
        stdin = codecs.getreader(sys.stdin.encoding)(sys.stdin)
    for line in stdin:
        src_dir, src_file, dst_dir, dst_file = parse_line(line)
        if None in (src_dir, src_file, dst_dir, dst_file):
            continue
        src = b'%s/%s' % (src_dir, src_file)
        dst = b'%s/%s' % (dst_dir, dst_file)
        graph.add_edge(src, dst)

    cycles = simple_cycles(graph)
    for cycle in cycles:
        print (b' -- ').join(cycle)

    return


if __name__ == b'__main__':
    import doctest
    doctest.testmod()