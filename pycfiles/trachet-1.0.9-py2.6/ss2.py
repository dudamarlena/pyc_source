# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/trachet/ss2.py
# Compiled at: 2014-07-01 10:29:06
from __future__ import print_function
import seqdb, template
_DB = seqdb.get()

def get_mnemonic(direction, f):
    """
    >>> get_mnemonic('=', 'O')
    '<unknown>'
    """
    global _DB
    key = '%s ESC N %s' % (direction, f)
    if key in _DB:
        mnemonic = _DB[key]
    else:
        mnemonic = '<unknown>'
    return mnemonic


def format_seq(final, is_input, tracer, controller):
    f = chr(final)
    if is_input:
        direction = '<'
    else:
        direction = '>'
    mnemonic = get_mnemonic(direction, f)
    if mnemonic[0] == '!':
        return eval(mnemonic[1:])
    context = []
    if f:
        context.append(f)
    result = template.getss2() % ((' ').join(context), mnemonic)
    return result


def _test():
    """
    >>> _test()
    test
    <unknown>
    """
    global _DB
    _DB = {'> ESC N O': 'test'}
    print(get_mnemonic('>', 'O'))
    print(get_mnemonic('>', 'A'))


if __name__ == '__main__':
    import doctest
    doctest.testmod()