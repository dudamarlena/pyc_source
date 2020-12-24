# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/requests/requests/packages/chardet/chardetect.py
# Compiled at: 2018-07-11 18:15:32
"""
Script which takes one or more file paths and reports on their detected
encodings

Example::

    % chardetect somefile someotherfile
    somefile: windows-1252 with confidence 0.5
    someotherfile: ascii with confidence 1.0

If no paths are provided, it takes its input from stdin.

"""
from __future__ import absolute_import, print_function, unicode_literals
import argparse, sys
from io import open
from chardet import __version__
from chardet.universaldetector import UniversalDetector

def description_of(lines, name=b'stdin'):
    """
    Return a string describing the probable encoding of a file or
    list of strings.

    :param lines: The lines to get the encoding of.
    :type lines: Iterable of bytes
    :param name: Name of file or collection of lines
    :type name: str
    """
    u = UniversalDetector()
    for line in lines:
        u.feed(line)

    u.close()
    result = u.result
    if result[b'encoding']:
        return (b'{0}: {1} with confidence {2}').format(name, result[b'encoding'], result[b'confidence'])
    else:
        return (b'{0}: no result').format(name)


def main(argv=None):
    """
    Handles command line arguments and gets things started.

    :param argv: List of arguments, as if specified on the command-line.
                 If None, ``sys.argv[1:]`` is used instead.
    :type argv: list of str
    """
    parser = argparse.ArgumentParser(description=b'Takes one or more file paths and reports their detected                      encodings', formatter_class=argparse.ArgumentDefaultsHelpFormatter, conflict_handler=b'resolve')
    parser.add_argument(b'input', help=b'File whose encoding we would like to determine.', type=argparse.FileType(b'rb'), nargs=b'*', default=[
     sys.stdin])
    parser.add_argument(b'--version', action=b'version', version=(b'%(prog)s {0}').format(__version__))
    args = parser.parse_args(argv)
    for f in args.input:
        if f.isatty():
            print(b'You are running chardetect interactively. Press ' + b'CTRL-D twice at the start of a blank line to signal the ' + b'end of your input. If you want help, run chardetect ' + b'--help\n', file=sys.stderr)
        print(description_of(f, f.name))


if __name__ == b'__main__':
    main()