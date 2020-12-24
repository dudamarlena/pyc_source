# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/core/impl/processor/render/text.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Jan 25, 2012\n\n@package: ally core\n@copyright: 2011 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProvides the text encoder processor handler that creates text objects to be encoded.\n'
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