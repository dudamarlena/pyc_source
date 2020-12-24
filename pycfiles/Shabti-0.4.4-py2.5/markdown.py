# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/shabti/templates/moinmoin/data/moin/data/plugin/parser/markdown.py
# Compiled at: 2010-04-25 12:11:22
from markdown import Markdown

class Parser:

    def __init__(self, raw, request, **kw):
        self.raw = raw
        self.request = request

    def format(self, formatter):
        self.request.write(Markdown(self.raw).toString())