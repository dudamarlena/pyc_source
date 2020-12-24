# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mastermind/mastermind.py
# Compiled at: 2020-02-20 02:55:47
# Size of source mod 2**32: 5815 bytes
""" play mastermind """
from __future__ import print_function
try:
    import __builtin__
    input = getattr(__builtin__, 'raw_input', input)
except ImportError:
    pass

from . import params
import os, sys, random, itertools
from collections import Counter, defaultdict
import binascii
from colorama import init, Style, Fore

def generate_board():
    return [random.choice(list(params.color_dict.keys())) for x in range(params.count_boxes)]


def make_guess(msg, master):
    guess = input(msg).lower().strip()
    if guess.startswith('!h'):
        print_instructions()
        return
    if guess.startswith('!q'):
        print('You chose to quit. The solution is:')
        print_colors(master, params.guess_peg, True)
        exit(0)
    else:
        if len(guess) != params.count_boxes:
            print('Invalid guess. Must be', str(params.count_boxes), 'colors.', '\n')
            return
        else:
            all([x in params.color_dict.keys() for x in list(guess)]) or print('Invalid guess. Must include only letters: ' + print_color_choices() + '\n')
            return
        return guess


def print_colors(inp, guess_char, tf_master):
    print(('  '.join([params.color_dict.get(x) + guess_char for x in inp])), end='\t')
    if tf_master:
        print((Style.RESET_ALL), end='\n')
    else:
        print((Style.RESET_ALL), end='\t')


def print_instructions():
    print('Puzzle contains ' + str(params.count_boxes) + ' boxes. Each turn you choose from ' + str(params.count_colors) + ' colors.')
    print('Color choices: ' + print_color_choices())
    print('Example turn: rybg')
    print('Response:')
    print(params.answer_dict.get('1') + '  :  correct color in correct position')
    print(params.answer_dict.get('2') + '  :  correct color in incorrect position')
    print(params.answer_dict.get('9') + '  :  incorrect color')
    print()
    print('The order of the response tiles does not necessarily match the colored characters.')
    print('Type !h to read these instructions again.')
    print('Type !q to quit and show solution.')
    print()


def print_color_choices():
    return ' '.join([v + k + Style.RESET_ALL for k, v in params.color_dict.items()])


def print_results(inp):
    grid = [Fore.WHITE + Style.BRIGHT + params.answer_dict.get(x) for x in inp]
    print(' '.join(grid))
    print(Style.RESET_ALL)


def get_results(guess, master):
    response = []
    correct_colors = sum((Counter(guess) & Counter(master)).values())
    correct_locations = sum((g == m for g, m in zip(guess, master)))
    correct_results = max(0, correct_colors - correct_locations)
    incorrect_results = max(0, params.count_boxes - correct_colors)
    result = '1' * correct_locations + '2' * correct_results + '9' * incorrect_results
    if params.debug:
        print(result)
    if len(result) != params.count_boxes:
        print('🚀 Houston. We have a problem.')
        exit(0)
    return result


def validate_puzzle(t):
    if len(t) != params.count_boxes:
        print('Incorrect number of boxes. Needs to be {} boxes.'.format(params.count_boxes))
        exit(0)
    else:
        if any([x for x in t if x not in params.color_dict.keys()]):
            print('Incorrect color selected. Choose from {}.'.format(print_color_choices()))
            exit(0)
        else:
            return True


def generate_code():
    xx = defaultdict(int)
    all_combos = [p for p in itertools.product((params.color_dict.keys()), repeat=(params.count_boxes))]
    for aa in all_combos:
        t = ''.join(aa)
        z = binascii.crc_hqx(t.encode('ascii'), 0)
        xx[str(z).zfill(5)] = t

    return xx


def main():
    init()
    dd = generate_code()
    master = None
    if len(sys.argv) < 2:
        master = generate_board()
    else:
        if len(sys.argv) > 2:
            print('Incorrect number of system arguments.')
            exit(0)
        else:
            if sys.argv[1] in dd:
                master = list(dd.get(sys.argv[1]))
            else:
                if validate_puzzle(sys.argv[1]):
                    rd = dict(map(reversed, dd.items()))
                    if sys.argv[1] in rd:
                        print('Your code to play {} is {}'.format(sys.argv[1], rd.get(sys.argv[1])))
                        exit(0)
                else:
                    exit(0)
    os.system('clear')
    if params.debug:
        print_colors(master, params.guess_peg, True)
    print_instructions()
    guess_list = []
    for i in range(params.count_turns):
        guess = None
        while not guess:
            if i + 1 < params.count_turns:
                msg = 'Turn '
            else:
                msg = 'Last turn! '
            msg += str(i + 1) + ' of ' + str(params.count_turns) + '. Your guess: '
            guess = make_guess(msg, master)

        print_colors(guess, params.guess_peg, False)
        guess_list.append(guess)
        result = get_results(guess, master)
        print_results(result)
        if result == '1' * params.count_boxes:
            print('🎉 Congrats mastermind! You found the solution:')
            print_colors(master, params.guess_peg, True)
            print()
            exit(0)
        if len(guess_list) >= params.count_turns:
            print('Too many turns! The solution is:')
            print_colors(master, params.guess_peg, True)
            exit(0)


if __name__ == '__main__':
    main()