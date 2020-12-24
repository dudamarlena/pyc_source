# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/transform/docbook/html_to_docbook.py
# Compiled at: 2009-03-11 14:45:14
from Products.PortalTransforms.interfaces import itransform
from html2docbook import Html2DocBook

def _safe_unicode(text):
    if not isinstance(text, unicode):
        text = unicode(text, 'utf-8', 'ignore')
    return text


class HtmlToDocBook:
    """Transform to take HTML and turn it into DocBook"""
    __module__ = __name__
    __implements__ = itransform
    __name__ = 'html_to_docbook'
    inputs = ('text/html', )
    output = 'application/docbook+xml'

    def __init__(self, name=None, inputs=('text/html', ), tab_width=4):
        self.config = {'inputs': inputs, 'tab_width': 4}
        self.config_metadata = {'inputs': ('list', 'Inputs', 'Input(s) MIME type. Change with care.'), 'tab_width': ('string', 'Tab width', 'Number of spaces for a tab in the input')}
        if name:
            self.__name__ = name

    def name(self):
        return self.__name__

    def __getattr__(self, attr):
        if attr in self.config:
            return self.config[attr]
        raise AttributeError(attr)

    def convert(self, orig, data, **kwargs):
        h2d = Html2DocBook()
        text = h2d.transform(orig)
        data.setData(text)
        return data


def register():
    return HtmlToDocBook()