# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\wsgiref\__init__.py
# Compiled at: 2006-06-05 13:45:25
"""wsgiref -- a WSGI (PEP 333) Reference Library

Current Contents:

* util -- Miscellaneous useful functions and wrappers

* headers -- Manage response headers

* handlers -- base classes for server/gateway implementations

* simple_server -- a simple BaseHTTPServer that supports WSGI

* validate -- validation wrapper that sits between an app and a server
  to detect errors in either

To-Do:

* cgi_gateway -- Run WSGI apps under CGI (pending a deployment standard)

* cgi_wrapper -- Run CGI apps under WSGI

* router -- a simple middleware component that handles URL traversal
"""