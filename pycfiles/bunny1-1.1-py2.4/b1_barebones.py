# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bunny1/b1_barebones.py
# Compiled at: 2009-02-22 16:55:43
__author__ = 'ccheever'
__doc__ = '\nA barebones bunny1 server that should be easy to modify for your own use\n'
__date__ = 'Thu Feb 12 09:05:40 PST 2009'
import urlparse, bunny1
from bunny1 import cherrypy
from bunny1 import Content
from bunny1 import q
from bunny1 import qp
from bunny1 import expose
from bunny1 import dont_expose
from bunny1 import escape
from bunny1 import HTML

class MyCommands(bunny1.Bunny1Commands):
    __module__ = __name__

    def your_command_here(self, arg):
        """this is where a description of your command goes"""
        return 'http://www.example.com/?' % qp(arg)

    def another_command(self, arg):
        """this example will send content to the browser rather than redirecting"""
        raise HTML('some <u>html</u> ' + escape('with some <angle brackets>'))


class MyBunny(bunny1.Bunny1):
    __module__ = __name__

    def __init__(self):
        bunny1.Bunny1.__init__(self, MyCommands(), bunny1.Bunny1Decorators())


if __name__ == '__main__':
    bunny1.main(MyBunny())