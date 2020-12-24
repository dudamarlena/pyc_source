# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/gratia/tools/gratia_web_dev.py
# Compiled at: 2008-02-15 09:40:27
import cherrypy
from pkg_resources import resource_filename
from graphtool.web import WebHost

def main():
    filename = resource_filename('gratia.config', 'website-devel.xml')
    WebHost(file=filename)
    cherrypy.server.quickstart()
    cherrypy.engine.start()


if __name__ == '__main__':
    main()