# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dap/responses/version.py
# Compiled at: 2008-03-31 07:43:18
"""Version response."""
from dap.lib import __dap__, __version__

def build(self, constraints=None):
    headers = [('XDODS-Server', 'dods/%s' % ('.').join([ str(i) for i in __dap__ ])),
     ('Content-type', 'text/plain')]
    output = [
     'Core version: dods/%s\n' % ('.').join([ str(i) for i in __dap__ ]),
     'Server version: pydap/%s\n' % ('.').join([ str(i) for i in __version__ ])]
    return (
     headers, output)