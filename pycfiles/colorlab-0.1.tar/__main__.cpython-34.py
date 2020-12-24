# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.4/site-packages/colorize_pinyin/__main__.py
# Compiled at: 2016-01-23 23:36:15
# Size of source mod 2**32: 1362 bytes
from __future__ import print_function
import sys, colorize_pinyin

def usage():
    print('usage:')
    print('\t%s [--] "string with chinese pinyin"' % sys.argv[0])
    print('\t%s [-h | --help]  # display this help' % sys.argv[0])
    print('\t%s -v | --version  # print version' % sys.argv[0])
    print('')
    print('prints colorized HTML string to stdout.')
    print('if no pinyin found, prints nothing and exits with code 2')
    return 1


def version():
    print(colorize_pinyin.__version__)
    return 0


def _main():
    if not sys.argv[1:]:
        return 2
    line = ' '.join(sys.argv[1:])
    colored = colorize_pinyin.colorized_HTML_string_from_string(line)
    if not colored:
        return 2
    print(colored)
    return 0


def main():
    if not sys.argv[1:]:
        return usage()
    if sys.argv[1] in ('-h', '--help'):
        usage()
        return 0
    if sys.argv[1] in ('-v', '--version'):
        return version()
    if sys.argv[1] == '--':
        del sys.argv[1]
    return _main()


if __name__ == '__main__':
    sys.argv[0] = 'python -m colorize_pinyin'
    exit(main())