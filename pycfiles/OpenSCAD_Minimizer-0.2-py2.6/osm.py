# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/osm/osm.py
# Compiled at: 2010-10-17 09:32:20
"""OpenSCAD Minimizer - Reduce the size of your .scad file
<http://github.com/l0b0/OpenSCAD-Minimizer>

Default syntax:

osm < input_file

Description:

Removes unnecessary whitespace and comments.

Examples:

osm < old.scad > new.scad
    Minimize old.scad and save the result in new.scad.

Bugs:

Please email bug reports including a minimal test file (if applicable) to
victor dot engmark at gmail dot com.
"""
__author__ = 'Victor Engmark'
__email__ = 'victor.engmark@gmail.com'
__copyright__ = 'Copyright (C) 2010 Victor Engmark'
__license__ = 'GPLv3'
from re import compile, sub, DOTALL, MULTILINE
from signal import signal, SIGPIPE, SIG_DFL
import sys
COMMENT_RE = compile('(^)?[^\\S\\n]*/(?:\\*(.*?)\\*/[^\\S\\n]*|/[^\\n]*)($)?', DOTALL | MULTILINE)
signal(SIGPIPE, SIG_DFL)

def _comment_replacer(match):
    (start, mid, end) = match.group(1, 2, 3)
    if mid is None:
        return ''
    else:
        if start is not None or end is not None:
            return ''
        else:
            if '\n' in mid:
                return '\n'
            return ' '
        return


def remove_comments(text):
    """
    Remove single- and multi-line comments.

    Thanks to MizardX for the code
    <http://stackoverflow.com/questions/844681/python-regex-question-stripping-multi-line-comments-but-maintaining-a-line-break/844721#844721>.
    """
    return COMMENT_RE.sub(_comment_replacer, text)


def remove_empty_start_end(text):
    """Remove empty lines of text in the input."""
    text = sub('\\A\\n+', '', text)
    text = sub('\\n+\\Z', '', text)
    return text


def remove_multiple_whitespace(text):
    """."""
    text = sub('(\\s)\\s+', '\\1', text)
    return text


def remove_whitespace(text):
    """Whitespace around operators, commas, braces, parentheses, and line
    endings."""
    text = sub('\\s*([+*/=,{}();-])\\s*', '\\1', text)
    return text


def osm(stream):
    """Run the minimizations."""
    text = stream.read()
    text = remove_comments(text)
    text = remove_empty_start_end(text)
    text = remove_multiple_whitespace(text)
    text = remove_whitespace(text)
    return text


def main(argv=None):
    result = osm(sys.stdin)
    print result


if __name__ == '__main__':
    sys.exit(main())