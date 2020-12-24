# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\censor\test_badword.py
# Compiled at: 2016-03-08 18:42:10
from tests.plugins.censor import Detection_TestCase

class Test_Censor_badword(Detection_TestCase):
    """
    Test that bad words are detected.
    """

    def test_word(self):

        def my_info(text):
            print 'INFO\t%s' % text

        self.p._badNames = []
        self.assert_chat_is_not_penalized('Joe')
        self.p._badNames = []
        self.p._add_bad_word(rulename='ass', word='ass')
        self.assert_chat_is_penalized('ass')
        self.assert_chat_is_penalized('dumb ass!')
        self.assert_chat_is_penalized('what an ass')
        self.assert_chat_is_not_penalized('nice one!')

    def test_regexp(self):

        def my_info(text):
            print 'INFO\t%s' % text

        self.p._badWords = []
        self.assert_chat_is_not_penalized('Joe')
        self.p._badWords = []
        self.p._add_bad_word(rulename='ass', regexp='\\b[a@][s$]{2}\\b')
        self.assert_chat_is_penalized('what an ass!')
        self.assert_chat_is_penalized('a$s')
        self.assert_chat_is_penalized('in your a$s! noob')
        self.assert_chat_is_penalized('kI$$ my a$s n00b')
        self.assert_chat_is_penalized('right in the ass')
        self.p._badWords = []
        self.p._add_bad_word(rulename='ass', regexp='f[u\\*]+ck')
        self.assert_chat_is_penalized('fuck')
        self.assert_chat_is_penalized(' fuck ')
        self.assert_chat_is_penalized(' fuck !')
        self.assert_chat_is_penalized('fuck!')
        self.assert_chat_is_penalized('fuck#*!')
        self.assert_chat_is_penalized('you fat fuck')
        self.assert_chat_is_penalized('f*ck u')
        self.assert_chat_is_penalized('f*****ck')
        self.assert_chat_is_penalized('f*uu**ck')