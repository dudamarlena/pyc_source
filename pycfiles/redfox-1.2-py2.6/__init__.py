# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/redfox/__init__.py
# Compiled at: 2009-10-20 11:31:07
"""Redfox provides a simple, declarative routing mechanism for creating
WSGI entry points into applications. It's broadly similar to
microframeworks like juno_ or CherryPy_.
"""
import redfox.meta
from redfox.routing import route, get, post, put, delete
__all__ = [
 'WebApplication',
 'route',
 'get',
 'post',
 'delete',
 'rule_map']

class WebApplication(object):
    """Web application classes should extend this class, rather than
    using the ``redfox.meta.WebApplication`` metaclass. The following
    example is a Hello World application::
    
        from redfox import WebApplication, get
        from werkzeug import Response
        
        class Example(WebApplication):
            @get('/')
            def index(self, request):
                return Response('Hello, world!')
    
    """
    __metaclass__ = redfox.meta.WebApplication


rule_map = redfox.meta.WebApplication.rule_map