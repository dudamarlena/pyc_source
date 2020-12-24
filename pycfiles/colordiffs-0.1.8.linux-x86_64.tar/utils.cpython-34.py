# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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