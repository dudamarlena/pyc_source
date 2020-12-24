# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/terminal/gwt/server/http_servlet_request_listener.py
# Compiled at: 2013-04-04 15:36:36
"""Request start and end listener"""

class IHttpServletRequestListener(object):
    """L{Application} that implements this interface gets notified
    of request start and end by terminal.

    Interface can be used for several helper tasks including:

      - Opening and closing database connections
      - Implementing L{ThreadLocal}
      - Setting/Getting L{Cookie}

    Alternatives for implementing similar features are are Servlet
    L{Filter}s and L{TransactionListener}s in Muntjac.
    """

    def onRequestStart(self, request, response):
        """This method is called before L{Terminal} applies the
        request to Application.
        """
        raise NotImplementedError

    def onRequestEnd(self, request, response):
        """This method is called at the end of each request.
        """
        raise NotImplementedError