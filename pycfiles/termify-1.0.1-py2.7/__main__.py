# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/src/__main__.py
# Compiled at: 2017-11-04 13:47:51
from termify import *
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--translation', help='show the translation of the lyrics')
    return parser.parse_args()


def main():
    """Display lyrics"""
    try:
        args = get_args()
        if args.translation:
            get_lyrics_translate(args.translation)
        else:
            get_lyrics()
    except Exception as e:
        print AsciiTable([[e_lyrics_not_found], ['Cause: ' + str(e)]], 'Error').table