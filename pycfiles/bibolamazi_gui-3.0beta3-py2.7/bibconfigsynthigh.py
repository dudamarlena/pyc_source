# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/bibolamazi_gui/bibconfigsynthigh.py
# Compiled at: 2015-05-11 05:40:29
import re
from collections import namedtuple
import bibolamazi.init
from bibolamazi.core.bibfilter import factory as filters_factory
from PyQt4.QtCore import *
from PyQt4.QtGui import *
rxsrc = re.compile('^\\s*(?P<src>src:)', re.MULTILINE)
rxfilter = re.compile('^\\s*(?P<filter>filter:)\\s+(?P<filtername>[-:\\w]+)', re.MULTILINE)
rxcomment = re.compile('^\\s*%%.*$', re.MULTILINE)
_rx_not_odd_num_backslashes = '(((?<=[^\\\\])|^)(\\\\\\\\)*)'
rxstring1 = re.compile(_rx_not_odd_num_backslashes + '(?P<str>\\"([^"\\\\]|\\\\\\\\|\\\\\\")*\\")', re.MULTILINE)
rxstring2 = re.compile(_rx_not_odd_num_backslashes + "(?P<str>\\'[^']*\\')", re.MULTILINE)

class BibolamaziConfigSyntaxHighlighter(QSyntaxHighlighter):

    def __init__(self, parent=None):
        super(BibolamaziConfigSyntaxHighlighter, self).__init__(parent)
        self.fmt_src = QTextCharFormat()
        self.fmt_src.setFontWeight(QFont.Bold)
        self.fmt_src.setForeground(QColor(0, 127, 127))
        self.fmt_filter = QTextCharFormat()
        self.fmt_filter.setFontWeight(QFont.Bold)
        self.fmt_filter.setForeground(QColor(127, 0, 0))
        self.fmt_filtername = QTextCharFormat()
        self.fmt_filtername.setForeground(QColor(0, 0, 127))
        self.fmt_filtername_nonex = QTextCharFormat(self.fmt_filtername)
        self.fmt_filtername_nonex.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)
        self.fmt_comment = QTextCharFormat()
        self.fmt_comment.setForeground(QColor(127, 127, 127))
        self.fmt_comment.setFontItalic(True)
        self.fmt_string = QTextCharFormat()
        self.fmt_string.setForeground(QColor(0, 127, 0))

    def highlightBlock(self, text):
        blockno = self.currentBlock().blockNumber()
        for m in rxsrc.finditer(text):
            self.setFormat(m.start('src'), len(m.group('src')), self.fmt_src)

        for m in rxfilter.finditer(text):
            self.setFormat(m.start('filter'), len(m.group('filter')), self.fmt_filter)
            fmtname = self.fmt_filtername
            try:
                filtmodule = filters_factory.get_module(m.group('filtername'))
            except (filters_factory.NoSuchFilter, filters_factory.NoSuchFilterPackage):
                fmtname = self.fmt_filtername_nonex

            self.setFormat(m.start('filtername'), len(m.group('filtername')), fmtname)

        for m in rxstring1.finditer(text):
            self.setFormat(m.start('str'), len(m.group('str')), self.fmt_string)

        for m in rxstring2.finditer(text):
            self.setFormat(m.start('str'), len(m.group('str')), self.fmt_string)

        for m in rxcomment.finditer(text):
            self.setFormat(m.start(), len(m.group()), self.fmt_comment)