# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\webchuan\interface.py
# Compiled at: 2008-10-19 04:07:41


class ElementHandler(object):
    """Interface that define handler function for element
    
    """

    def handleOutput(self, element, data, port, **kwargs):
        """Called to handle elements' output
        
        @param element: element that output
        @param data: data to handle
        @param port: output port 
        """
        raise NotImplementedError

    def handleRequest(self, element):
        """Called to handle element's request
        
        @param element: element that required
        """
        raise NotImplementedError

    def handleFailure(self, element, excInfo, data, **kwargs):
        """Called to handle element's failure
        
        @param element: element that failed
        @param excInfo: a (type, value, traceback) tuple
        @param data: input data
        """
        raise NotImplementedError