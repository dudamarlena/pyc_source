# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/pb/598z8h910dvf2wrvwnbyl_2m0000gn/T/pip-install-65c3rg8f/chardet/chardet/cli/chardetect.py
# Compiled at: 2019-11-10 08:27:46
# Size of source mod 2**32: 2738 bytes
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
from chardet import __version__
from chardet.compat import PY2
from chardet.universaldetector import UniversalDetector

def description_of(lines, name='stdin'):
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
        line = bytearray(line)
        u.feed(line)
        if u.done:
            break

    u.close()
    result = u.result
    if PY2:
        name = name.decode(sys.getfilesystemencoding(), 'ignore')
    if result['encoding']:
        return '{0}: {1} with confidence {2}'.format(name, result['encoding'], result['confidence'])
    return '{0}: no result'.format(name)


def main(argv=None):
    """
    Handles command line arguments and gets things started.

    :param argv: List of arguments, as if specified on the command-line.
                 If None, ``sys.argv[1:]`` is used instead.
    :type argv: list of str
    """
    parser = argparse.ArgumentParser(description='Takes one or more file paths and reports their detected                      encodings')
    parser.add_argument('input', help='File whose encoding we would like to determine.                               (default: stdin)',
      type=(argparse.FileType('rb')),
      nargs='*',
      default=[
     sys.stdin if PY2 else sys.stdin.buffer])
    parser.add_argument('--version', action='version', version=('%(prog)s {0}'.format(__version__)))
    args = parser.parse_args(argv)
    for f in args.input:
        if f.isatty():
            print('You are running chardetect interactively. Press CTRL-D twice at the start of a blank line to signal the end of your input. If you want help, run chardetect --help\n',
              file=(sys.stderr))
        print(description_of(f, f.name))


if __name__ == '__main__':
    main()