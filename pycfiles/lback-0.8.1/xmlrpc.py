# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mdipierro/make_web2py/web2py/gluon/xmlrpc.py
# Compiled at: 2013-10-14 11:16:25
"""
This file is part of the web2py Web Framework
Copyrighted by Massimo Di Pierro <mdipierro@cs.depaul.edu>
License: LGPLv3 (http://www.gnu.org/licenses/lgpl.html)
"""
from SimpleXMLRPCServer import SimpleXMLRPCDispatcher

def handler(request, response, methods):
    response.session_id = None
    dispatcher = SimpleXMLRPCDispatcher(allow_none=True, encoding=None)
    for method in methods:
        dispatcher.register_function(method)

    dispatcher.register_introspection_functions()
    response.headers['Content-Type'] = 'text/xml'
    dispatch = getattr(dispatcher, '_dispatch', None)
    return dispatcher._marshaled_dispatch(request.body.read(), dispatch)