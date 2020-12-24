# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/cherrypy/cherrypy/tutorial/tut01_helloworld.py
# Compiled at: 2018-07-11 18:15:31
"""
Tutorial - Hello World

The most basic (working) CherryPy application possible.
"""
import cherrypy

class HelloWorld:
    """ Sample request handler class. """

    def index(self):
        return 'Hello world!'

    index.exposed = True


import os.path
tutconf = os.path.join(os.path.dirname(__file__), 'tutorial.conf')
if __name__ == '__main__':
    cherrypy.quickstart(HelloWorld(), config=tutconf)
else:
    cherrypy.tree.mount(HelloWorld(), config=tutconf)