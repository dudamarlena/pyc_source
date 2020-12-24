# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/wduss/src/github.com/dalloriam/engel/engel/widgets/abstract.py
# Compiled at: 2017-01-06 15:18:40
# Size of source mod 2**32: 1597 bytes
"""
.. note::
  All widgets in this package are not meant to be used directly. They are mostly used by the framework, or subclassed
  into usable widgets.
"""
from .base import BaseElement
from ..utils import html_property

class HeadLink(BaseElement):
    __doc__ = '\n    Widget representing links described in the ``<head>`` section of a typical HTML document.\n    This widget is used by the framework to generate links to stylesheets and auto-generated javascript files.\n    '
    html_tag = 'link'
    target = html_property('href')
    link_type = html_property('rel')

    def build(self, link_type, path):
        super(HeadLink, self).build()
        self.target = path
        self.link_type = link_type
        self.autoclosing = True


class PageTitle(BaseElement):
    __doc__ = '\n    Widget representing the title of the page.\n    This widget is used by :meth:`~.application.View.render`.\n    '
    html_tag = 'title'

    def build(self, text):
        super(PageTitle, self).build()
        self.content = text


class Script(BaseElement):
    __doc__ = '\n    Widget representing a script element.\n    '
    html_tag = 'script'
    source = html_property('src')

    def build(self, js_path):
        super(Script, self).build()
        self.source = js_path