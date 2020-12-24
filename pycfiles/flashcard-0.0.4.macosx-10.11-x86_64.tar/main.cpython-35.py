# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sotetsuk/.pyenv/versions/3.5.1/lib/python3.5/site-packages/flashcard/main.py
# Compiled at: 2016-05-13 18:20:18
# Size of source mod 2**32: 2753 bytes
"""Simple flashcard in your terminal

Usage:
  flashcard [--hint=<hint_rate>] <flashcard>
  flashcard (-h | --help)
  flashcard --version

Options:
  --hint=<hint_rate>    Show hint. p = 1 will show every character and p=0 will hide all.
  -h --help             Show this screen.
  --version             Show version.
"""
from typing import Tuple
from termcolor import colored
import difflib
from random import random
from docopt import docopt
from flashcard.property import Flashcard
from flashcard.sources import fetch_google_spreadsheet

def run(flashcard: Flashcard, hint_rate=None):
    n = len(flashcard)
    num_collect = 0
    for i, card in enumerate(flashcard):
        problem = card[0]
        expected = card[1]
        print('# {:02d}'.format(i + 1), problem)
        if hint_rate is not None:
            print(colored('hint', 'blue'), hint(expected, hint_rate))
        ans = input('>>>> ')
        if expected == ans.strip():
            num_collect += 1
            print(colored('GOOD', 'green'), colored(expected, 'green'))
        else:
            expected_with_mistake, ans_with_mistake = get_diff_with_color(expected, ans)
            print(colored('MISS', 'red'), expected_with_mistake)
            print('    ', ans_with_mistake)
        print('*' * 100)

    print('{}/{}'.format(num_collect, n))


def get_diff_with_color(expected: str, ans: str) -> Tuple[(str, str)]:
    d = difflib.Differ()
    diff = d.compare(expected, ans)
    expected_with_mistake = ''
    ans_with_mistake = ''
    for e in diff:
        if e.startswith('+'):
            ans_with_mistake += colored(e[(-1)], 'red')
        elif e.startswith('-'):
            expected_with_mistake += colored(e[(-1)], 'green')
        else:
            expected_with_mistake += e[(-1)]
            ans_with_mistake += e[(-1)]

    return (
     expected_with_mistake, ans_with_mistake)


def hint(expected: str, hint_rate=0.5) -> str:
    ret = ''
    for c in expected:
        if c in (' ', ',', '.', '?', '!', '"', "'", '-'):
            ret += c
        else:
            if random() > hint_rate:
                ret += '*'
            else:
                ret += c

    return ret


def main():
    args = docopt(__doc__, version='flashcard 0.0.4')
    if args['<flashcard>'].startswith('https://docs.google.com/spreadsheets/'):
        flashcard = fetch_google_spreadsheet(args['<flashcard>'])
    else:
        print('<flashcard> should be URL of Google Spreadsheet (other sources are TBA)')
        exit(1)
    hint_rate = None
    if args['--hint'] is not None:
        hint_rate = float(args['--hint'])
        assert 0.0 <= hint_rate <= 1.0, 'hint rate should satisfy 0.0 <= hint_rate <= 1.0'
    run(flashcard, hint_rate)


if __name__ == '__main__':
    main()