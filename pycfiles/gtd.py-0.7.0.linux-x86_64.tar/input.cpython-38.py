# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/delucks/.pyenv/versions/3.8.1/lib/python3.8/site-packages/todo/input.py
# Compiled at: 2020-02-21 23:12:22
# Size of source mod 2**32: 1821 bytes
"""Helper functions that retrieve user input"""
import sys, tty, string, termios

def prompt_for_confirmation(message, default=False):
    options = ' (Y/n)' if default else ' (y/N)'
    print((message.strip() + options), end='', flush=True)
    choice = getch()
    print()
    if not choice == 'y':
        if not choice == 'n':
            if choice == '\r':
                break
            else:
                print('Input was not y, nor was it n. Enter is OK')
    if choice != '\r':
        return choice == 'y'
    return default


def getch():
    """override terminal settings to read a single character from stdin"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == '\x03':
            raise KeyboardInterrupt
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return ch


def single_select(options):
    """A faster selection interface.
    Assigns a one-char identifier to each option and reads only one
    character from stdin. Return the option assigned to that identifier.
    Downside: you can only have 30ish options

    :param iterable options: choices you want the user to select between
    """
    lookup = {}
    preferred_keys = [
     'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'"]
    remainder = list(set(string.ascii_lowercase) - set(preferred_keys))
    all_keys = preferred_keys + remainder
    for idx, chunk in enumerate(options):
        assigned = all_keys[idx]
        lookup[assigned] = idx
        print(f"[{assigned}] {chunk}")
    else:
        print('Press the character corresponding to your choice, selection will happen immediately. Ctrl+D to cancel')
        result = lookup.get(getch(), None)
        if result is not None:
            return list(options)[int(result)]


# NOTE: have internal decompilation grammar errors.
# Use -t option to show full context.
# not in loop:
#	break
#      L.  15        70  BREAK_LOOP           84  'to 84'