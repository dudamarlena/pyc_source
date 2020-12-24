# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\CODE\VScode\autowork\ymm-automation\ymmuim-library\YmmuimLibrary\keywords\_element.py
# Compiled at: 2019-07-01 08:39:53
# Size of source mod 2**32: 896 bytes
from YmmuimLibrary.action.actioner import Actioner
from .keywordgroup import KeywordGroup
import robot.libraries.BuiltIn as BuiltIn
import ast
from unicodedata import normalize
try:
    basestring

    def isstr(s):
        return isinstance(s, basestring)


except NameError:

    def isstr(s):
        return isinstance(s, str)


class _YmmiumKeywords(KeywordGroup):

    def __init__(self):
        self._element_actioner = Actioner()
        self._bi = BuiltIn()

    def click_element(self, name):
        """ Click element identified by `locator`. """
        self._click_action(name)

    def _click_action(self, name):
        try:
            print(name)
        except Exception as e:
            try:
                raise 'Cannot click the element with name "%s"' % name
            finally:
                e = None
                del e