# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/src/interactions.py
# Compiled at: 2018-01-03 04:41:52
# Size of source mod 2**32: 783 bytes
import argparse
from api_connections import translate

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('text', type=str, help='text to translate')
    parser.add_argument('-s', '--src', default=None, help='origin language of the text')
    parser.add_argument('-d', '--dest', default=None, help='destiny language of the translation')
    parser.add_argument('-v', '--verbose', help='show more information', action='store_true')
    args = parser.parse_args()
    tr = translate(args.text, args.src, args.dest)
    if args.verbose:
        print('original text: %s' % tr.origin)
        print('translated text: %s' % tr.text)
        print('origin language: %s' % tr.src)
        print('destiny language: %s' % tr.dest)
    else:
        print(tr.text)