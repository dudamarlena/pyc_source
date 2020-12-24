# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/trachet/ss3.py
# Compiled at: 2014-07-01 10:29:06
from __future__ import print_function
import seqdb, template
_DB = seqdb.get()

def get_mnemonic(direction, f):
    """
    >>> _create_mock_db()
    >>> get_mnemonic('<', 'A')
    'Cursor key(application keypad): up arrow'
    >>> get_mnemonic('>', 'B')
    '<unknown>'
    >>> get_mnemonic('<', '[')
    'alternate escape key'
    """
    global _DB
    key = '%s ESC O %s' % (direction, f)
    if key in _DB:
        mnemonic = _DB[key]
    else:
        mnemonic = '<unknown>'
    return mnemonic


def format_seq(final, is_input, tracer, controller):
    r"""
    >>> _create_mock_db()
    >>> template.enable_color()
    >>> format_seq(0x42, True, None, None)
    '\x1b[0;1;36;44m ESC O B \x1b[0;1;31m\r\x1b[30CCursor key(application keypad): down arrow'
    >>> template.disable_color()
    >>> format_seq(0x42, True, None, None)
    ' ESC O B   Cursor key(application keypad): down arrow'
    >>> format_seq(0x42, False, None, None)
    ' ESC O B   <unknown>'
    >>> import sys
    >>> format_seq(0x74, True, sys, None)
    test
    """
    f = chr(final)
    if is_input:
        direction = '<'
    else:
        direction = '>'
    mnemonic = get_mnemonic(direction, f)
    if mnemonic[0] == '!':
        eval(mnemonic[1:])
        return None
    else:
        context = []
        if f:
            context.append(f)
        result = template.getss3() % ((' ').join(context), mnemonic)
        return result


def _test():
    """
    >>> _test()
    test
    <unknown>
    """
    global _DB
    _DB = {'> ESC O O': 'test'}
    print(get_mnemonic('>', 'O'))
    print(get_mnemonic('>', 'A'))


def _create_mock_db():
    global _DB
    _DB = {'> ESC O': 'SS3', 
       '< ESC O': 'SS3', 
       '< ESC O A': 'Cursor key(application keypad): up arrow', 
       '< ESC O B': 'Cursor key(application keypad): down arrow', 
       '< ESC O C': 'Cursor key(application keypad): right arrow', 
       '< ESC O D': 'Cursor key(application keypad): left arrow', 
       '< ESC O P': 'F1 key (xterm)', 
       '< ESC O Q': 'F2 key (xterm)', 
       '< ESC O R': 'F3 key (xterm)', 
       '< ESC O S': 'F4 key (xterm)', 
       '< ESC O t': '!tracer.stdout.write("test")', 
       '< ESC O [': 'alternate escape key'}


if __name__ == '__main__':
    import doctest
    doctest.testmod()