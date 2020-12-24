# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/cherrypy/cherrypy/tutorial/tut04_complex_site.py
# Compiled at: 2018-07-11 18:15:31
"""
Tutorial - Multiple objects

This tutorial shows you how to create a site structure through multiple
possibly nested request handler objects.
"""
import cherrypy

class HomePage:

    def index(self):
        return '\n            <p>Hi, this is the home page! Check out the other\n            fun stuff on this site:</p>\n\n            <ul>\n                <li><a href="/joke/">A silly joke</a></li>\n                <li><a href="/links/">Useful links</a></li>\n            </ul>'

    index.exposed = True


class JokePage:

    def index(self):
        return '\n            <p>"In Python, how do you create a string of random\n            characters?" -- "Read a Perl file!"</p>\n            <p>[<a href="../">Return</a>]</p>'

    index.exposed = True


class LinksPage:

    def __init__(self):
        self.extra = ExtraLinksPage()

    def index(self):
        return '\n            <p>Here are some useful links:</p>\n\n            <ul>\n                <li>\n                    <a href="http://www.cherrypy.org">The CherryPy Homepage</a>\n                </li>\n                <li>\n                    <a href="http://www.python.org">The Python Homepage</a>\n                </li>\n            </ul>\n\n            <p>You can check out some extra useful\n            links <a href="./extra/">here</a>.</p>\n\n            <p>[<a href="../">Return</a>]</p>\n        '

    index.exposed = True


class ExtraLinksPage:

    def index(self):
        return '\n            <p>Here are some extra useful links:</p>\n\n            <ul>\n                <li><a href="http://del.icio.us">del.icio.us</a></li>\n                <li><a href="http://www.cherrypy.org">CherryPy</a></li>\n            </ul>\n\n            <p>[<a href="../">Return to links page</a>]</p>'

    index.exposed = True


root = HomePage()
root.joke = JokePage()
root.links = LinksPage()
import os.path
tutconf = os.path.join(os.path.dirname(__file__), 'tutorial.conf')
if __name__ == '__main__':
    cherrypy.quickstart(root, config=tutconf)
else:
    cherrypy.tree.mount(root, config=tutconf)