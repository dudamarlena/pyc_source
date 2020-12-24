# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/i3visiotools/darkfy/darkfy-launcher.py
# Compiled at: 2014-12-25 06:48:18
""" 
darkfy.py Copyright (C) F. Brezo and Y. Rubio (i3visio) 2014
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it under certain conditions.
For details, run:
        python darkfy-launcher.py --license
"""
__author__ = 'Felix Brezo, Yaiza Rubio '
__copyright__ = 'Copyright 2014, i3visio'
__credits__ = ['Felix Brezo', 'Yaiza Rubio']
__license__ = 'GPLv3'
__version__ = 'v0.2.1'
__maintainer__ = 'Felix Brezo, Yaiza Rubio'
__email__ = 'contacto@i3visio.com'
import argparse, i3visiotools.darkfy.lib.processing as processing
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='darkfy - darkfy a GPLv3 tool that searches a word in different platforms.', prog='darkfy.py', epilog='', add_help=False)
    parser._optionals.title = 'Input options (one required)'
    general = parser.add_mutually_exclusive_group(required=True)
    general.add_argument('-l', '--list', metavar='<path_to_nick_list>', action='store', type=argparse.FileType('r'), help='path to the file where the list of words to verify is stored (one per line).')
    general.add_argument('-w', '--words', metavar='<word>', nargs='+', action='store', help='the list of words to process (at least one is required).')
    groupProcessing = parser.add_argument_group('Processing arguments', 'Arguments related to the performance of the program.')
    groupProcessing.add_argument('-o', '--output', required=False, action='store', default='./results.json', help='filepath of the results folder.')
    groupAbout = parser.add_argument_group('About arguments', 'Showing additional information about this program.')
    groupAbout.add_argument('--license', required=False, action='store_true', default=False, help='shows the GPLv3 license and exists.')
    groupAbout.add_argument('--version', action='version', version='%(prog)s 0.2.0', help='shows the version of the program and exists.')
    groupAbout.add_argument('-h', '--help', action='help', help='shows this help and exists.')
    groupAbout.add_argument('-v', '--verbose', metavar='<verbosity>', choices=[0, 1, 2], required=False, action='store', default=1, help='select the verbosity level: 0 - none; 1 - normal (default); 2 - debug.', type=int)
    args = parser.parse_args()
    processing.darkfy_main(args)