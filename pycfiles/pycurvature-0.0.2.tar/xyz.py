# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pycurry\test\xyz.py
# Compiled at: 2009-02-15 08:52:19
__doc__ = 'Todo.\n\nCopyright (c) 2008 Fons Dijkstra\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in\nall copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN\nTHE SOFTWARE.\n'
import pycurry.dbc as dbc
dbc.level.set(dbc.level.max())

class structor(object):
    __metaclass__ = dbc.dbc_class

    def __new__(cls):
        return super(structor, cls).__new__(cls)

    def __del__(cls):
        pass


with dbc.level(None):

    class none(object):
        """
        invariant: False
        """
        __metaclass__ = dbc.dbc_class

        def foo(self):
            """
            require: False
            ensure: False
            """
            pass


with dbc.level(dbc.level.require):

    class require(object):
        """
        invariant: False
        """
        __metaclass__ = dbc.dbc_class

        def foo(self, pre=True):
            """
            require: pre
            ensure: False
            """
            pass


with dbc.level(dbc.level.ensure):

    class ensure(object):
        """
        invariant: False
        """
        __metaclass__ = dbc.dbc_class

        def foo(self, pre=True, post=True):
            """
            require: pre
            ensure: post
            """
            pass


with dbc.level(dbc.level.invariant):

    class invariant(object):
        """
        invariant: self.inv
        """
        __metaclass__ = dbc.dbc_class

        def __init__(self, inv=True):
            self.inv = inv

        def foo(self, pre=True, post=True):
            """
            require: pre
            ensure: post
            """
            pass