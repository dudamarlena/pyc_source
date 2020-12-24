# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/trachet/esc.py
# Compiled at: 2014-07-01 10:29:06
import seqdb, template
_DB = seqdb.get()

def get_mnemonic(direction, i, f):
    key = '%s ESC %s%s' % (direction, i, f)
    if key in _DB:
        mnemonic = _DB[key]
    else:
        mnemonic = '<Unknown>'
    return mnemonic


def format_seq(intermediate, final, is_input, tracer, controller):
    i = ('').join([ chr(c) for c in intermediate ]).replace(' ', '<SP>')
    f = chr(final)
    if is_input:
        direction = '<'
    else:
        direction = '>'
    mnemonic = get_mnemonic(direction, i, f)
    if mnemonic[0] == '!':
        return eval(mnemonic[1:])
    return template.getesc() % (i, f, mnemonic)


if __name__ == '__main__':
    import doctest
    doctest.testmod()