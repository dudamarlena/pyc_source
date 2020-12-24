# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/vagrant/.virtualenvs/temp3/lib/python3.4/site-packages/colordiffs/utils.py
# Compiled at: 2015-06-20 22:18:44
# Size of source mod 2**32: 213 bytes
from pygments.lexer import Lexer
from pygments.token import Text

class NoneLexer(Lexer):

    def analyse_text(text):
        return 2

    def get_tokens_unprocessed(sef, text):
        return [
         (
          0, Text, text)]