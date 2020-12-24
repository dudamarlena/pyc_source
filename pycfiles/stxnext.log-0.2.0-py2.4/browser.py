# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/stxnext/log/browser.py
# Compiled at: 2009-03-26 10:03:35
from logger import STXNextLogger
try:
    from Products.Five import BrowserView
    IN_ZOPE = True
except ImportError:
    IN_ZOPE = False
    BrowserView = object

class STXNextLoggerView(BrowserView):
    """
    View class for STXNextLogger

    @author: Wojciech Lichota <wojciech.lichota[at]stxnext.pl>
    """
    __module__ = __name__

    def __call__(self):
        """
        Get STXNextLogger instance.
        
        @return: logger object
        @rtype: STXNextLogger
        
        <tal:block tal:define="log context/@@STXNextLogger;
                               result python: log.setFilename('logger_filename.log');
                               result python: log.setName('logger name');">
            <tal:block tal:define="result python: log('log this text')" />
            <tal:block tal:define="result python: log('log another text', printit=True)" />  
            <pre tal:replace="structure log/getLoggedTextAsHtml" />
        </tal:block>
        """
        return STXNextLogger()