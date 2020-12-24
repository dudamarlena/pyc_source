# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-9.6.0-i386/egg/astrogrid/webserver.py
# Compiled at: 2007-05-22 05:33:39
import os, cherrypy, kid

class Root:
    __module__ = __name__

    @cherrypy.expose
    def index(self):
        page = kid.Template('templates/main.kid')
        return page.serialize(output='xhtml')


cherrypy.quickstart(Root())