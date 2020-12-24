# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/chips/git/boilerplate/src/boilerplate/inputs.py
# Compiled at: 2016-03-24 07:04:49
# Size of source mod 2**32: 632 bytes


def yn_input(text, yes='yes', no='no', default='yes'):
    """Asks a yes/no question and return the answer."""
    suffix = ' [%s/%s] ' % (yes[0].upper(), no[0])
    while True:
        ans = input(text + suffix).lower()
        if ans in (yes, no):
            return ans
        if not ans:
            return default
        if ans[0] == yes[0]:
            return yes
        if ans[0] == no[0]:
            return no
        text = '    - please enter %r or %r' % (yes, no)


def ny_input(text, yes='yes', no='no'):
    """Like yn_input, but the default choice is 'no'."""
    return yn_input(text, yes, no, default=no)