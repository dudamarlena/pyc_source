# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Documents and Settings\Jean-Lou Dupont\My Documents\workspace_gae\pypp\trunk\pypp\loader.py
# Compiled at: 2009-03-02 13:16:38
__doc__ = ' Module Loader class\n    project: pypp\n    \n    @author: Jean-Lou Dupont\n'
__author__ = 'Jean-Lou Dupont'
__version__ = '$Id: loader.py 5 2009-03-02 18:16:37Z jeanlou.dupont $'
__all__ = [
 'Loader']
import os, imp, sys

class Loader(object):
    """ Loads a .pypp file in place of the usual .py
    """

    def __init__(self, name, file, path, desc, global_scope):
        self.name = name
        self.file = file
        self.path = path
        self.desc = desc
        self.global_scope = global_scope

    def load_module(self, fullname):
        isfile = self.file is not None
        try:
            mod = imp.load_module(self.name, self.file, self.path, self.desc)
        finally:
            if self.file:
                self.file.close()

        sys.modules[fullname] = mod
        return mod