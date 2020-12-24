# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/src/main.py
# Compiled at: 2018-01-03 04:38:50
# Size of source mod 2**32: 1229 bytes
import argparse
from googletrans import Translator
translator = Translator()

def translate(text, src_lng=None, dest_lng=None):
    if src_lng and dest_lng:
        translated = translator.translate(text, src=src_lng, dest=dest_lng)
    else:
        if src_lng:
            translated = translator.translate(text, src=src_lng)
        else:
            if dest_lng:
                translated = translator.translate(text, dest=dest_lng)
            else:
                translated = translator.translate(text)
    return translated


def test():
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