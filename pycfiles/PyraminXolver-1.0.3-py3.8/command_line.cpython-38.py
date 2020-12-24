# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\pyraminxolver\command_line.py
# Compiled at: 2019-10-26 16:03:57
# Size of source mod 2**32: 1833 bytes
import sys, argparse
from . import PyraminXolver
import pyraminxolver.setup as graph_setup
parser = argparse.ArgumentParser()
parser.add_argument('--input-file', help='Path to file with a bunch of pyraminx scrambles')
parser.add_argument('--output-file', help='Path to output solutions')
parser.add_argument('--scramble', help='Scamble wrapped in "". e.g. "L R U L"')
parser.add_argument('--slack', default=0, type=int, help='Maximum distance to optimal solution for all solutions')
parser.add_argument('--verbose', type=bool, help='Get more details')
args = parser.parse_args()

def main():
    print('Loading up pyraminx graph')
    pyra = PyraminXolver()
    print('Graph loaded, ready to solve')
    slack = args.slack
    scrambles = []
    if args.input_file:
        with open(args.input_file, 'r') as (f):
            for line in f:
                scrambles.append(line.replace('\n', ''))

    else:
        scrambles = [
         args.scramble]
    for scramble in scrambles:
        if args.output_file:
            with open(args.output_file, 'a') as (f):
                f.write(f"Solving: {scramble}\n")
        else:
            print(f"Solving: {scramble}")
        solutions = pyra.search_scramble(scramble, slack)
        for solution, length, time, path in solutions:
            if args.output_file:
                with open(args.output_file, 'a') as (f):
                    f.write(f"{solution}\n")
            else:
                print(f"{solution} ({length} moves found in {time // 1000000}ms)")

        if args.output_file:
            with open(args.output_file, 'a') as (f):
                f.write('\n')
        else:
            print('')


def setup():
    print('Setting up the initial pyraminx graph')
    graph_setup()
    print('Pyraminx graph generated, PyraminXolver is now ready for use!')