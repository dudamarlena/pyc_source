# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/util/taurusropepatch.py
# Compiled at: 2019-08-19 15:09:30
"""[DEPRECATED] Rope patch for better performance.
Based on spyder.rope_patch"""
__all__ = [
 'apply']
__docformat__ = 'restructuredtext'
from taurus.core.util.log import deprecated
deprecated(dep='taurusropepatch module', rel='4.0.1')

def apply():
    """Monkey patching rope for better performances"""
    import rope
    if rope.VERSION not in ('0.9.3', '0.9.2'):
        raise ImportError("rope %s can't be patched" % rope.VERSION)
    from rope.base import pycore

    class PatchedPyCore(pycore.PyCore):

        def get_module(self, name, folder=None):
            """Returns a `PyObject` if the module was found."""
            pymod = self._builtin_module(name)
            if pymod is not None:
                return pymod
            else:
                module = self.find_module(name, folder)
                if module is None:
                    raise pycore.ModuleNotFoundError('Module %s not found' % name)
                return self.resource_to_pyobject(module)

    pycore.PyCore = PatchedPyCore
    from rope.base import builtins, pyobjects
    from spyder.utils.dochelpers import getargs

    class PatchedBuiltinFunction(builtins.BuiltinFunction):

        def __init__(self, returned=None, function=None, builtin=None, argnames=[], parent=None):
            builtins._BuiltinElement.__init__(self, builtin, parent)
            pyobjects.AbstractFunction.__init__(self)
            self.argnames = argnames
            if not argnames and builtin:
                self.argnames = getargs(self.builtin)
            if self.argnames is None:
                self.argnames = []
            self.returned = returned
            self.function = function
            return

    builtins.BuiltinFunction = PatchedBuiltinFunction
    from rope.base import libutils
    import inspect

    class PatchedBuiltinName(builtins.BuiltinName):

        def _pycore(self):
            p = self.pyobject
            while p.parent is not None:
                p = p.parent

            if isinstance(p, builtins.BuiltinModule) and p.pycore is not None:
                return p.pycore
            else:
                return

        def get_definition_location(self):
            if not inspect.isbuiltin(self.pyobject):
                _lines, lineno = inspect.getsourcelines(self.pyobject.builtin)
                path = inspect.getfile(self.pyobject.builtin)
                pycore = self._pycore()
                if pycore and pycore.project:
                    resource = libutils.path_to_resource(pycore.project, path)
                    module = pyobjects.PyModule(pycore, None, resource)
                    return (
                     module, lineno)
            return (None, None)

    builtins.BuiltinName = PatchedBuiltinName