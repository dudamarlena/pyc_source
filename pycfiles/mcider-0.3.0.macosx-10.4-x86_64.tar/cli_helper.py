# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ogom/.pyenv/versions/2.7.6/lib/python2.7/site-packages/mcider/cli_helper.py
# Compiled at: 2014-12-15 07:23:39
""" mcider - cli helper
Copyright(c) 2012-2014 ogom

Parser for command line options.
"""
import argparse
parser = argparse.ArgumentParser(description='\n        mCider is markdown converter for slideshow.\n    ')
parser.add_argument('--version', action='version', version='%(prog)s 0.3.0')
parser.add_argument('file', metavar='FILE', type=argparse.FileType('r'), help='Contents of the markdown.')
parser.add_argument('--theme', '-t', default='io2012', help='Theme of the slide. (io2012, io2011, ...)')
parser.add_argument('--output', '-o', metavar='FILE', type=argparse.FileType('w+'), help='File to output slide.')
parser.add_argument('--extensions', '-x', metavar='EXTENSION', nargs='*', help='\n        Provided to expand the base syntax.\n        (extra, fenced_code, tables, ...)\n    ')
parser.add_argument('--browser', '-b', action='store_true', default=False, help='View in Web Browser.')
parser.add_argument('--clean', '-c', action='store_true', default=False, help='Theme was to clean the output.')
parser.add_argument('--presenter', action='store_true', default=False, help='Presenter mode.')
parser.add_argument('--themes', metavar='PATH', help='Path of the custom themes')