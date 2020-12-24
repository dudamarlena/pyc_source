# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summermvc/mvc/handler.py
# Compiled at: 2018-05-30 05:31:20
"""
Handler对象包含page handler和若干个exception handler
"""

class Handler(object):

    def __init__(self):
        self._page_handler = None
        self._matches = None
        self._exception_handlers = {}
        return

    def __nonzero__(self):
        return self.page_handler is not None

    def invoke(self, *a, **kw):
        if self.page_handler is None:
            raise RuntimeError
        return self.page_handler(*a, **kw)

    def add_page_handler(self, page_handler, matches=None):
        self._page_handler = page_handler
        self._matches = matches

    def add_exception_handler(self, exception, exception_handler, matches=None):
        self._exception_handlers[exception] = (exception_handler, matches)

    @property
    def page_handler(self):
        return self._page_handler

    @property
    def matches(self):
        return self._matches

    @property
    def exception_handlers(self):
        return self._exception_handlers