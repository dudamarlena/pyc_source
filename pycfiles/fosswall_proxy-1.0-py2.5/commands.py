# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/fosswallproxy/commands.py
# Compiled at: 2008-03-03 06:09:58
import pkg_resources
pkg_resources.require('TurboGears')
from os.path import *
import os, sys

def start():
    from turbogears import update_config, start_server
    import cherrypy
    cherrypy.lowercase_api = True
    if len(sys.argv) > 1:
        update_config(configfile=sys.argv[1], modulename='fosswallproxy.config')
    elif exists(join(os.getcwd(), 'setup.py')):
        update_config(configfile='dev.cfg', modulename='fosswallproxy.config')
    else:
        update_config(configfile='prod.cfg', modulename='fosswallproxy.config')
    from fosswallproxy.controllers import Root
    start_server(Root())