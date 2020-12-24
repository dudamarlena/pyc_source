# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\bogglesolver\cli.py
# Compiled at: 2014-08-13 18:06:35
# Size of source mod 2**32: 2077 bytes
"""Command-line interface for boggle solver."""
import argparse, time
from bogglesolver.solve_boggle import SolveBoggle

def main(args=None):
    """
    Main entry point for the Command-line-interface.

    Looking at this for good idea of command line interface.
    http://manpages.ubuntu.com/manpages/trusty/man6/boggle.6.html
    """
    min_length = 3
    column = 4
    row = 4
    game_time = 180
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--play', action='store_true', help='True if you want to play boggle.')
    parser.add_argument('-t', '--time', type=int, help='int game time in seconds.')
    parser.add_argument('-l', '--length', type=int, help='Change the minimum word length.')
    parser.add_argument('-w', '--words', type=str, help='Get all words for a given list of letters.')
    parser.add_argument('-c', '--columns', type=int, help='Set the number of columns.')
    parser.add_argument('-r', '--rows', type=int, help='Set the number of rows.')
    args = parser.parse_args(args=args)
    if args.columns:
        column = args.columns
    if args.rows:
        row = args.rows
    if args.words:
        solver = SolveBoggle(args.words, column, row)
        print(solver.solve(False))
    if args.time:
        game_time = args.time
    if args.length:
        min_length = args.length
    if args.play:
        solver = SolveBoggle()
        solver.set_board(column, row)
        words = solver.solve()
        print(solver.boggle)
        print('Play Boggle!!')
        time.sleep(game_time)
        i = 0
        for i, word in enumerate(words):
            if len(word) >= min_length:
                print(word)
                continue

        print(str(i) + ' words found.')
        exit()


if __name__ == '__main__':
    main()