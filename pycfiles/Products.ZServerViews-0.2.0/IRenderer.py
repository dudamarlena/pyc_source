# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/Zpydoc/interfaces/IRenderer.py
# Compiled at: 2011-09-28 02:31:46
from zope.interface import Interface

class IZpydocRenderer(Interface):
    """
    this is our renderer quasi-ZClass

    note that each renderer MUST implement this interface, and MUST
    supply a global function of the form manage_add<__classname__>Renderer(self, REQUEST=None)
    for our factory generator
    """

    def __init__(self):
        """
        a default ctor IS required ie no parameters ...
        """
        pass

    def page(self, object):
        """
        handle publishing a package/module...
        """
        pass

    def builtins(self):
        """
        handle publishing builtin functions
        """
        pass

    def index(self, path, seen):
        """
        build a list of package modules for the main index page
        """
        pass