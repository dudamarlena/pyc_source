# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kghose/.venvs/benten/lib/python3.7/site-packages/benten/code/requirements.py
# Compiled at: 2019-09-13 12:05:46
# Size of source mod 2**32: 350 bytes
from .intelligence import IntelligenceNode
from .intelligencecontext import IntelligenceContext

class Requirements(IntelligenceContext):

    def __init__(self, req_types):
        self.req_types = req_types

    def get_completer(self):
        return IntelligenceNode(completions=(self.req_types))