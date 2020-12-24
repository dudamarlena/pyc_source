# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/shakespeare/tests/test_textutils.py
# Compiled at: 2008-10-29 17:02:17
import StringIO, shakespeare.textutils

class TestTextUtils:
    inStr = "THE PHOENIX AND THE TURTLE\n\nby William Shakespeare\n\n\n\n\nLet the bird of loudest lay,\nOn the sole Arabian tree,\nHerald sad and trumpet be,\nTo whose sound chaste wings obey.\n\nBut thou, shrieking harbinger,\nFoul pre-currer of the fiend,\nAugur of the fever's end,\nTo this troop come thou not near."
    inFileObj = StringIO.StringIO(inStr)

    def test_get_snippet(self):
        exp = '...Arabian tree,\nHerald sad and trumpet be,\nTo whose sound chaste wing...'
        out = shakespeare.textutils.get_snippet(self.inFileObj, 125)
        assert exp == out