# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/twisted_goodies/simpleserver/http/util.py
# Compiled at: 2007-07-25 20:51:02
"""
Utility stuff
"""
import traceback
from twisted.web2 import static

def showException(theTraceback=None):
    """
    Returns a C{static.Data} resource showing details about the last
    exception.

    """
    if theTraceback is None:
        theTraceback = traceback.format_exc()
    title = 'Error importing index.py'
    html = ['<html>']
    html.append('<head><title>%s</title></head>' % title)
    html.append('<body><h1>%s</h1>' % title)
    html.append('<p><pre>%s</pre></p>' % theTraceback)
    html.append('</body></html>')
    exceptionResource = static.Data(data=('\n').join(html), type='text/html')
    exceptionResource.addSlash = True
    return exceptionResource