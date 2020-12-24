# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/core/impl/processor/render/text.py
# Compiled at: 2013-10-02 09:54:40
"""
Created on Jan 25, 2012

@package: ally core
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the text encoder processor handler that creates text objects to be encoded.
"""
from .base import RenderBaseHandler
from ally.container.ioc import injected
from ally.core.spec.transform.render import RenderToObject
from ally.support.util_io import IOutputStream
from codecs import getwriter

@injected
class RenderTextHandler(RenderBaseHandler):
    """
    Provides the text object encoding.
    @see: RenderBaseHandler
    """
    rendererTextObject = None
    encodingError = 'backslashreplace'

    def __init__(self):
        assert callable(self.rendererTextObject), 'Invalid callable renderer %s' % self.rendererTextObject
        assert isinstance(self.encodingError, str), 'Invalid string %s' % self.encodingError
        super().__init__()

    def renderFactory(self, charSet, output):
        """
        @see: RenderBaseHandler.renderFactory
        """
        assert isinstance(charSet, str), 'Invalid char set %s' % charSet
        outputb = getwriter(charSet)(output, self.encodingError)
        return RenderTextObject(self.rendererTextObject, charSet, outputb)


class RenderTextObject(RenderToObject):
    """
    Renderer for text objects.
    """
    __slots__ = ('renderer', 'charSet', 'output')

    def __init__(self, renderer, charSet, output):
        """
        Construct the text object renderer.
        
        @param handler: RenderTextHandler
            The handler of the renderer.
        """
        assert callable(renderer), 'Invalid renderer %s' % renderer
        assert isinstance(charSet, str), 'Invalid character set %s' % charSet
        assert isinstance(output, IOutputStream), 'Invalid output stream %s' % output
        super().__init__()
        self.renderer = renderer
        self.charSet = charSet
        self.output = output

    def objectEnd(self):
        """
        @see: RenderToObject.objectEnd
        """
        super().objectEnd()
        if not self.processing:
            self.renderer(self.obj, self.charSet, self.output)

    def collectionEnd(self):
        """
        @see: RenderToObject.collectionEnd
        """
        super().collectionEnd()
        if not self.processing:
            self.renderer(self.obj, self.charSet, self.output)