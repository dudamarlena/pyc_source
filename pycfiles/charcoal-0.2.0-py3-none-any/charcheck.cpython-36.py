# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\charcheck\charcheck.py
# Compiled at: 2017-07-07 05:04:05
# Size of source mod 2**32: 1052 bytes
import sys, getopt
from .lib import *

def main():
    source_file = ''
    target_file = ''
    output_file = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hs:t:o:', ['source=', 'target=', 'output='])
    except getopt.GetoptError:
        print('Charcheck -s<source file path> -t<target file path> -o<output file path>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('Charcheck -s<source file path> -t<target file path> -o<output file path>')
            sys.exit()
        else:
            if opt in ('-s', '--source'):
                source_file = arg
            else:
                if opt in ('-t', '--target'):
                    target_file = arg
                else:
                    if opt in ('-o', '--output'):
                        output_file = arg

    if source_file != '' or target_file != '':
        if output_file == '':
            process(source_file, target_file)
        else:
            process(source_file, target_file, output_file)
    else:
        print('You are missing target or source file name.')
        sys.exit()