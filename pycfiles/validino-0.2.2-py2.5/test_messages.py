# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-ppc/egg/validino/tests/test_messages.py
# Compiled at: 2007-12-06 13:09:46
from __future__ import with_statement
import validino as V
from validino.messages import msg, getMessages
from util import assert_invalid

def test_msg():
    messages = dict(integer='hey, I said use a number')
    with msg(messages):
        assert messages == getMessages()
        assert_invalid(lambda : V.integer()('lump'), messages['integer'])
    assert getMessages() != messages
    assert_invalid(lambda : V.integer()('lump'), 'not an integer')