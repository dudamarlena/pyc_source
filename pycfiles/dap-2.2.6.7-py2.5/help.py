# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dap/responses/help.py
# Compiled at: 2008-03-31 07:43:18
from paste.request import construct_url
from dap.lib import __dap__

def build(self, constraints=None, message=''):
    """Help response."""
    headers = [
     (
      'XDODS-Server', 'dods/%s' % ('.').join([ str(i) for i in __dap__ ])),
     ('Content-type', 'text/html')]
    if message:
        output = [
         message]
    else:
        location = construct_url(self.environ, with_query_string=False)[:-len('.help')]
        output = ['<p>To access this file, use the URL <code>%s</code>.</p>' % location]
    return (headers, output)