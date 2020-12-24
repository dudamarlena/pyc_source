# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/cherrypy/cherrypy/tutorial/tut03_get_and_post.py
# Compiled at: 2018-07-11 18:15:31
"""
Tutorial - Passing variables

This tutorial shows you how to pass GET/POST variables to methods.
"""
import cherrypy

class WelcomePage:

    def index(self):
        return '\n            <form action="greetUser" method="GET">\n            What is your name?\n            <input type="text" name="name" />\n            <input type="submit" />\n            </form>'

    index.exposed = True

    def greetUser(self, name=None):
        if name:
            return "Hey %s, what's up?" % name
        else:
            if name is None:
                return 'Please enter your name <a href="./">here</a>.'
            else:
                return 'No, really, enter your name <a href="./">here</a>.'

            return

    greetUser.exposed = True


import os.path
tutconf = os.path.join(os.path.dirname(__file__), 'tutorial.conf')
if __name__ == '__main__':
    cherrypy.quickstart(WelcomePage(), config=tutconf)
else:
    cherrypy.tree.mount(WelcomePage(), config=tutconf)