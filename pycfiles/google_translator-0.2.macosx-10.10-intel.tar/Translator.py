# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/google_translator/Translator.py
# Compiled at: 2015-04-23 04:23:22
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from google_translator import GoogleConmunication
import Lang

class Translator(object):

    def translate(self, content=None):
        if not content:
            return content
        return self.__google_conmunication.translate(source_lang=self.get_source_lang(), target_lang=self.get_target_lang(), content=content)

    def get_target_lang(self):
        return self.__target_lang

    def set_target_lang(self, target_lang):
        self.__target_lang = target_lang

    def get_source_lang(self):
        return self.__source_lang

    def set_source_lang(self, source_lang):
        self.__source_lang = source_lang

    def __init__(self, target_lang):
        self.__target_lang = None
        self.__source_lang = 'auto'
        self.__google_conmunication = GoogleConmunication.GoogleConmunication()
        if target_lang:
            self.set_target_lang(target_lang)
        return


if __name__ == '__main__':
    content = sys.argv[1]
    t = Translator(Lang.Lang.chinese_simplified)
    print t.translate(content)