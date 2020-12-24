# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/LeslieZhu/.pyenv/versions/2.7.15/Python.framework/Versions/2.7/lib/python2.7/site-packages/orgnote/markdown.py
# Compiled at: 2019-11-25 07:03:32
import re

class Markdown(object):
    """ re-implementation of markdown for OrgNote

    Perl version by John Gruber: 
    - https://raw.githubusercontent.com/mundimark/markdown.pl/master/Markdown.pl
    """

    def __init__(self, text=''):
        self.empty_element_suffix = ' >'
        self.tab_width = 4
        self.text = text
        self.urls = ()
        self.titles = ()
        self.html_blocks = ()

    def mk2html(self):
        self.text = re.sub('\\r\\n', '\\n', self.text)
        self.text = re.sub('\\r', '\\n', self.text)
        self.text += '\n\n'
        self.text = self._DeTab(self.text)
        return self.text

    def _DeTab(self, text):
        return re.sub('\\t', ' ' * self.tab_width, text)

    def _HashHTMLBlocks(self, text):
        self.less_than_tab = self.tab_width - 1
        self.block_tags_a = 'p|div|h[1-6]|blockquote|pre|table|dl|ol|ul|script|noscript|form|fieldset|iframe|math|ins|del'
        self.block_tags_b = 'p|div|h[1-6]|blockquote|pre|table|dl|ol|ul|script|noscript|form|fieldset|iframe|math'