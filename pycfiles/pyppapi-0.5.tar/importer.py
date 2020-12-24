# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pypp\importer.py
# Compiled at: 2009-03-07 10:40:11
__doc__ = ' Module Importer class\n    project: pypp\n    \n    @author: Jean-Lou Dupont\n'
__author__ = 'Jean-Lou Dupont'
__version__ = '$Id: importer.py 13 2009-03-07 15:40:10Z jeanlou.dupont $'
__all__ = [
 'Importer']
import imp, os, sys
from types import *

class Importer(object):
    __slots__ = [
     'callback_import_module']

    def __init__(self):
        self.callback_import_module = None
        return

    def find_module(self, fullname, path=None):
        """
        Case1:  X  where X is package thus X.__init__ is module
        Case2:  X  where X is module
        
        Case3:  X.Y where X is package & Y is package thus X.Y.__init__ is module
        Case4:  X.Y where X is package & Y is module
                
        We have to go through some hoops because imp.find_module
        does not handle the X.Y case directly. The package X must
        have been dealt with prior to calling imp.find_module;
        thus, when X.Y is encountered, we first make sure the package
        isn't loaded yet and then we process X.__init__ module
        (assuming it can be found in the filesystem).
        """
        origName = fullname
        lookupName = None
        if '.' in fullname:
            (pkg_name, name) = fullname.rsplit('.', 1)
            mod = sys.modules.get(pkg_name, None)
            if type(mod) is ModuleType:
                path = mod.__path__ if hasattr(mod, '__path__') else path
                lookupName = name
            else:
                lookupName = fullname
        else:
            lookupName = fullname
        try:
            (file, rpath, desc) = imp.find_module(lookupName, path)
        except:
            return

        _isdir = os.path.isdir(rpath)
        _isfile = os.path.isfile(rpath)
        _ispkg = _isdir
        _ismod = _isfile
        if _ispkg:
            return self._handlePkg(origName, rpath, file, desc)
        if _ismod:
            return self._handleMod(origName, rpath, rpath, file, desc)
        return

    def _handlePkg(self, name, rpath, file, desc):
        """ Handles package loading
        
            rpath: filesystem path to package where __init__ should be found
        """
        mod_path = os.path.join(rpath, '__init__.py')
        return self._handleMod(name, rpath, mod_path, file, desc)

    def _handleMod(self, name, rpath, path, file, desc):
        """ Handles module loading
        
            path: filesystem path to the module (i.e. mod-name.py)
        """
        frame = sys._getframe(1)
        global_scope = frame.f_globals
        return self.callback_import_module(name, rpath, path, file, desc, global_scope)