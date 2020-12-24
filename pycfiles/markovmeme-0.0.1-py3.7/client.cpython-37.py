# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/markovmeme/client.py
# Compiled at: 2019-12-29 16:42:14
# Size of source mod 2**32: 3433 bytes
"""

Copyright (C) 2019-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
from markovmeme.utils import list_corpus
from markovmeme.main import MemeImage
from markovmeme.text import generate_text
import argparse, random, sys, os

def get_parser():
    parser = argparse.ArgumentParser(description='Markov Meme Generator')
    description = 'actions for Markov Meme Generator'
    subparsers = parser.add_subparsers(help='markovmeme actions',
      title='actions',
      description=description,
      dest='command')
    generate = subparsers.add_parser('generate', help='generate a meme')
    generate.add_argument('--outfile',
      dest='outfile',
      help='the output file to save the image (defaults to randomly generated png)',
      type=str,
      default=None)
    generate.add_argument('--fontsize',
      dest='fontsize',
      help='font size of text (if desired) defaults to 16',
      type=int,
      default=36)
    generate.add_argument('--font',
      dest='font',
      help='choice of font (defaults to open sans)',
      type=str,
      choices=[
     'OpenSans-Regular', 'Pacifico-Regular', 'Anton-Regular'],
      default='Anton-Regular')
    generate.add_argument('--corpus',
      dest='corpus',
      choices=(list_corpus()),
      help='the corpus to use to generate the meme, matches to images.',
      type=str,
      default=None)
    generate.add_argument('--custom-corpus',
      dest='custom_corpus',
      help='A custom corpus file, full path',
      type=str,
      default=None)
    generate.add_argument('--image',
      dest='custom_image',
      help='A custom image file, full path',
      type=str,
      default=None)
    generate.add_argument('--no-model',
      dest='no_model',
      help="Don't generate a sentence from corpus, just randomly select sentence.",
      default=False,
      action='store_true')
    return parser


def main():
    """main is the entrypoint to the markov meme client.
    """
    parser = get_parser()
    args, extra = parser.parse_known_args()
    if args.command == 'generate':
        font = args.font
        if not args.font.endswith('.ttf'):
            font = '%s.ttf' % font
        corpus = args.corpus
        if corpus is None:
            corpus = random.choice(list_corpus())
        if args.custom_corpus:
            if os.path.exists(args.custom_corpus):
                corpus = args.custom_corpus
        text = generate_text(corpus=corpus, use_model=(not args.no_model), size=10)
        meme = MemeImage(image=(args.custom_image), corpus=corpus)
        meme.write_text(text, fontsize=(args.fontsize), font=font)
        meme.save_image(args.outfile)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()