# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dbtexmf/dblatex/grubber/xetex.py
# Compiled at: 2017-04-03 18:58:57
"""
XeTeX support for Rubber.
"""
from plugins import TexModule

class Module(TexModule):

    def __init__(self, doc, dict):
        doc.program = 'xelatex'
        doc.engine = 'dvipdfmx'
        doc.encoding = 'utf8'
        doc.set_format('pdf')