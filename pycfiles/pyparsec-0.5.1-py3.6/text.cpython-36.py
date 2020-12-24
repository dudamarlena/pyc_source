# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/parsec/text.py
# Compiled at: 2015-08-28 01:15:53
# Size of source mod 2**32: 500 bytes
from parsec.error import ParsecError
from parsec import Parsec

def string(s):

    @Parsec
    def call(st):
        for chr in s:
            c = st.next()
            if chr != c:
                raise ParsecError(st, "Expect '{0}' but got {1}".format(s, c))
        else:
            return s

    return call


@Parsec
def space(state):
    c = state.next()
    if c.isspace():
        return c
    raise ParsecError(st, 'Expect a space but got {0}'.format(c))