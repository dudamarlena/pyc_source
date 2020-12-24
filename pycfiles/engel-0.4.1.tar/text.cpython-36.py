# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/wduss/src/github.com/dalloriam/engel/engel/widgets/text.py
# Compiled at: 2017-01-06 15:18:40
# Size of source mod 2**32: 1396 bytes
from .base import BaseElement
from ..utils import html_property

class Title(BaseElement):
    __doc__ = '\n    Title widget analogous to the HTML <h{n}> elements.\n    '

    def build(self, text, size=1):
        """
        :param text: Text of the widget
        :param size: Size of the text (Higher size = smaller title)
        """
        super(Title, self).build()
        self.content = text
        self.size = size

    def _get_html_tag(self):
        return 'h{0}'.format(self.size)


class Paragraph(BaseElement):
    __doc__ = '\n    Simple paragraph widget\n    '
    html_tag = 'p'

    def build(self, text):
        super(Paragraph, self).build()
        self.content = text


class Span(BaseElement):
    __doc__ = '\n    Simple span widget\n    '
    html_tag = 'span'

    def build(self, text):
        super(Span, self).build()
        self.content = text


class TextLink(BaseElement):
    __doc__ = '\n    Text widget linking to an external URL.\n    '
    html_tag = 'a'
    target = html_property('href')

    def build(self, text, url):
        super(TextLink, self).build()
        self.target = url
        self.content = text