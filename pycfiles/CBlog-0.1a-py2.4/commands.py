# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/cblog/commands.py
# Compiled at: 2006-12-15 15:12:38
import os, sys
from os.path import *
import pkg_resources
pkg_resources.require('TurboGears')
import turbogears

def start():
    """Start the CherryPy application server."""
    import cherrypy
    cherrypy.lowercase_api = True
    from cblog.cachecontrol import ExpiresFilter
    curdir = os.getcwd()
    if len(sys.argv) > 1:
        turbogears.update_config(configfile=sys.argv[1], modulename='cblog.config')
    elif exists(join(curdir, 'setup.py')):
        turbogears.update_config(configfile='dev.cfg', modulename='cblog.config')
    else:
        turbogears.update_config(configfile='prod.cfg', modulename='cblog.config')
    from cblog.controllers import Root
    root = Root()
    cherrypy.root = root
    cherrypy.root._cp_filters = [ExpiresFilter()]
    turbogears.start_server(root)