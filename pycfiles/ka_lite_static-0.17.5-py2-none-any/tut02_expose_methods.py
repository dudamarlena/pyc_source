# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/cherrypy/cherrypy/tutorial/tut02_expose_methods.py
# Compiled at: 2018-07-11 18:15:31
"""
Tutorial - Multiple methods

This tutorial shows you how to link to other methods of your request
handler.
"""
import cherrypy

class HelloWorld:

    def index(self):
        return 'We have an <a href="show_msg">important message</a> for you!'

    index.exposed = True

    def show_msg(self):
        return 'Hello world!'

    show_msg.exposed = True


import os.path
tutconf = os.path.join(os.path.dirname(__file__), 'tutorial.conf')
if __name__ == '__main__':
    cherrypy.quickstart(HelloWorld(), config=tutconf)
else:
    cherrypy.tree.mount(HelloWorld(), config=tutconf)