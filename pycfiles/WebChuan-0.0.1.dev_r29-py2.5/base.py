# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\webchuan\base.py
# Compiled at: 2008-10-22 09:14:05
import logging, cStringIO
from twisted.internet import reactor
from twisted.web.client import getPage
from lxml import etree
import element
log = logging.getLogger(__name__)

class GetPage(element.Element):
    """Element for getting web page from internet
    
    """

    def __init__(self, name=None, defaultKwargs=None, *args, **kwargs):
        """
        
        @param name: name of element
        @param defaultKwargs: Default key arguments pass to getPage function
        """
        element.Element.__init__(self, name, *args, **kwargs)
        self.defaultKwargs = defaultKwargs or {}

    def handleData(self, data, **kwargs):
        """input url to get page
        
        @param data: url data to get page
        """
        from twisted.web.client import getPage
        kwargsCopy = self.defaultKwargs.copy()
        if kwargs.get('getPage_kwargs') is not None:
            kwargsCopy.update(kwargs['getPage_kwargs'])
        d = getPage(data, **kwargsCopy)
        d.addCallbacks(self.outputAndRequire, self.handleFailure, callbackKeywords=kwargs, errbackArgs=(self, data), errbackKeywords=kwargs)
        return

    def handleFailure(self, failure, element, data, **kwargs):
        excInfo = (failure.value, failure.type, failure.tb)
        self.failAndRequire(excInfo, data, **kwargs)


class Parser(element.Element):
    """Element for parsing html with lxml
    
    """

    def __init__(self, name=None, encoding=None, handler=None, *args, **kwargs):
        """
        
        @param encoding: Encoding of html to decode
        @param handler: Function to handle parsed tree and return data to output
        """
        element.Element.__init__(self, name, *args, **kwargs)
        self.encoding = encoding
        self.handler = handler

    def handleData(self, data, **kwargs):
        """input html to parse
        
        @param data: html data to get page
        """
        html = data
        parser = etree.HTMLParser(encoding=self.encoding)
        tree = etree.parse(cStringIO.StringIO(html), parser)
        if self.handler:
            self.outputAndRequire(self.handler(tree, kwargs), **kwargs)
        else:
            self.outputAndRequire(tree, **kwargs)


class If(element.Element):
    """Element output to different ports by checking condition 
    
    """

    def __init__(self, name=None, condition=None, elsePort='else', *args, **kwargs):
        """
        
        @param condition: Function to decide which port to output, 
            return True to output to "output"port
            return False to output to elsePort
        @param elsePort: The port to output when the condition is Flse
        """
        element.Element.__init__(self, name, *args, **kwargs)
        self.condition = condition
        self.elsePort = elsePort

    def handleData(self, data, **kwargs):
        if self.condition(data, **kwargs):
            self.outputAndRequire(data, **kwargs)
        else:
            self.outputAndRequire(data, self.elsePort, **kwargs)


class DoNothing(element.Element):
    """An element do nothing but just pass data along
    
    """

    def handleData(self, data, **kwargs):
        self.outputAndRequire(data, **kwargs)


class FunctionHandler(element.Element):
    """Call a given function to handle input data
    
    """

    def __init__(self, name=None, function=None, *args, **kwargs):
        """

        """
        element.Element.__init__(self, name, *args, **kwargs)
        self.function = function

    def handleData(self, data, **kwargs):
        self.outputAndRequire(self.function(data, kwargs), **kwargs)