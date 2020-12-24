# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/shabti/templates/moinmoin/+package+/public/moin_static/applets/FCKeditor/editor/filemanager/connectors/py/wsgi.py
# Compiled at: 2010-02-28 10:28:47
"""
FCKeditor - The text editor for Internet - http://www.fckeditor.net
Copyright (C) 2003-2009 Frederico Caldeira Knabben

== BEGIN LICENSE ==

Licensed under the terms of any of the following licenses at your
choice:

 - GNU General Public License Version 2 or later (the "GPL")
   http://www.gnu.org/licenses/gpl.html

 - GNU Lesser General Public License Version 2.1 or later (the "LGPL")
   http://www.gnu.org/licenses/lgpl.html

 - Mozilla Public License Version 1.1 or later (the "MPL")
   http://www.mozilla.org/MPL/MPL-1.1.html

== END LICENSE ==

Connector/QuickUpload for Python (WSGI wrapper).

See config.py for configuration settings

"""
from connector import FCKeditorConnector
from upload import FCKeditorQuickUpload
import cgitb
from cStringIO import StringIO

def App(environ, start_response):
    """WSGI entry point. Run the connector"""
    if environ['SCRIPT_NAME'].endswith('connector.py'):
        conn = FCKeditorConnector(environ)
    elif environ['SCRIPT_NAME'].endswith('upload.py'):
        conn = FCKeditorQuickUpload(environ)
    else:
        start_response('200 Ok', [('Content-Type', 'text/html')])
        yield 'Unknown page requested: '
        yield environ['SCRIPT_NAME']
        return
    try:
        data = conn.doResponse()
        start_response('200 Ok', conn.headers)
        yield data
    except:
        start_response('500 Internal Server Error', [('Content-type', 'text/html')])
        file = StringIO()
        cgitb.Hook(file=file).handle()
        yield file.getvalue()