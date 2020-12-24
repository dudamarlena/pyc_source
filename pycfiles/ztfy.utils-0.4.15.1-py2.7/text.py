# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/utils/text.py
# Compiled at: 2012-06-20 10:07:04
__docformat__ = 'restructuredtext'
from zope.component import createObject, queryMultiAdapter
from ztfy.utils.request import getRequest

def textStart(text, length, max=0):
    """Get first words of given text with maximum given length
    
    If @max is specified, text is shortened only if remaining text is longer than @max
    
    @param text: initial text
    @param length: maximum length of resulting text
    @param max: if > 0, @text is shortened only if remaining text is longer than max
    """
    result = text or ''
    if length > len(result):
        return result
    index = length - 1
    text_length = len(result)
    while index > 0 and result[index] != ' ':
        index -= 1

    if index > 0 and text_length > index + max:
        return result[:index] + '&#133;'
    return text


def textToHTML(text, renderer='zope.source.plaintext', request=None):
    if request is None:
        request = getRequest()
    formatter = createObject(renderer, text)
    renderer = queryMultiAdapter((formatter, request), name='')
    return renderer.render()


class Renderer(object):

    def __init__(self, context):
        self.context = context

    def render(self, renderer, request=None):
        if not self.context:
            return ''
        return textToHTML(self.context, renderer, request)