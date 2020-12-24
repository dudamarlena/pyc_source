# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/reload.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 16989 bytes
"""
Magic Reload Library
Luke Campagnola   2010

Python reload function that actually works (the way you expect it to)
 - No re-importing necessary
 - Modules can be reloaded in any order
 - Replaces functions and methods with their updated code
 - Changes instances to use updated classes
 - Automatically decides which modules to update by comparing file modification times
 
Does NOT:
 - re-initialize exting instances, even if __init__ changes
 - update references to any module-level objects
   ie, this does not reload correctly:
       from module import someObject
       print someObject
   ..but you can use this instead: (this works even for the builtin reload)
       import module
       print module.someObject
"""
import inspect, os, sys, gc, traceback
try:
    import __builtin__ as builtins
except ImportError:
    import builtins

from .debug import printExc

def reloadAll(prefix=None, debug=False):
    """Automatically reload everything whose __file__ begins with prefix.
    - Skips reload if the file has not been updated (if .pyc is newer than .py)
    - if prefix is None, checks all loaded modules
    """
    failed = []
    changed = []
    for modName, mod in list(sys.modules.items()):
        if not inspect.ismodule(mod):
            continue
        if modName == '__main__':
            continue
        if hasattr(mod, '__file__'):
            if os.path.splitext(mod.__file__)[1] not in ('.py', '.pyc'):
                continue
            else:
                if prefix is not None:
                    if mod.__file__[:len(prefix)] != prefix:
                        continue
                py = os.path.splitext(mod.__file__)[0] + '.py'
                pyc = py + 'c'
                if py not in changed:
                    if os.path.isfile(pyc):
                        if os.path.isfile(py) and os.stat(pyc).st_mtime >= os.stat(py).st_mtime:
                            continue
            changed.append(py)
            try:
                reload(mod, debug=debug)
            except:
                printExc('Error while reloading module %s, skipping\n' % mod)
                failed.append(mod.__name__)

    if len(failed) > 0:
        raise Exception('Some modules failed to reload: %s' % ', '.join(failed))


def reload(module, debug=False, lists=False, dicts=False):
    """Replacement for the builtin reload function:
    - Reloads the module as usual
    - Updates all old functions and class methods to use the new code
    - Updates all instances of each modified class to use the new class
    - Can update lists and dicts, but this is disabled by default
    - Requires that class and function names have not changed
    """
    if debug:
        print('Reloading %s' % str(module))
    oldDict = module.__dict__.copy()
    builtins.reload(module)
    newDict = module.__dict__
    if hasattr(module, '__reload__'):
        module.__reload__(oldDict)
    for k in oldDict:
        old = oldDict[k]
        new = newDict.get(k, None)
        if old is new or new is None:
            continue
        if inspect.isclass(old):
            if debug:
                print('  Updating class %s.%s (0x%x -> 0x%x)' % (module.__name__, k, id(old), id(new)))
            updateClass(old, new, debug)
        elif inspect.isfunction(old):
            depth = updateFunction(old, new, debug)
            if debug:
                extra = ''
                if depth > 0:
                    extra = ' (and %d previous versions)' % depth
                print('  Updating function %s.%s%s' % (module.__name__, k, extra))
        elif lists and isinstance(old, list):
            l = old.len()
            old.extend(new)
            for i in range(l):
                old.pop(0)

        elif dicts and isinstance(old, dict):
            old.update(new)
            for k in old:
                if k not in new:
                    del old[k]


def updateFunction(old, new, debug, depth=0, visited=None):
    old.__code__ = new.__code__
    old.__defaults__ = new.__defaults__
    if visited is None:
        visited = []
    elif old in visited:
        return
        visited.append(old)
        if hasattr(old, '__previous_reload_version__'):
            maxDepth = updateFunction((old.__previous_reload_version__), new, debug, depth=(depth + 1), visited=visited)
    else:
        maxDepth = depth
    if depth == 0:
        new.__previous_reload_version__ = old
    return maxDepth


def updateClass(old, new, debug):
    refs = gc.get_referrers(old)
    for ref in refs:
        try:
            if isinstance(ref, old) and ref.__class__ is old:
                ref.__class__ = new
                if debug:
                    print('    Changed class for %s' % safeStr(ref))
            elif inspect.isclass(ref):
                if issubclass(ref, old):
                    if old in ref.__bases__:
                        ind = ref.__bases__.index(old)
                        ref.__bases__ = ref.__bases__[:ind] + (new, old) + ref.__bases__[ind + 1:]
                        if debug:
                            print('    Changed superclass for %s' % safeStr(ref))
        except:
            print('Error updating reference (%s) for class change (%s -> %s)' % (safeStr(ref), safeStr(old), safeStr(new)))
            raise

    for attr in dir(old):
        oa = getattr(old, attr)
        if inspect.ismethod(oa):
            try:
                na = getattr(new, attr)
            except AttributeError:
                if debug:
                    print('    Skipping method update for %s; new class does not have this attribute' % attr)
                continue

            if hasattr(oa, 'im_func') and hasattr(na, 'im_func') and oa.__func__ is not na.__func__:
                depth = updateFunction(oa.__func__, na.__func__, debug)
                if debug:
                    extra = ''
                    if depth > 0:
                        extra = ' (and %d previous versions)' % depth
                    print('    Updating method %s%s' % (attr, extra))

    for attr in dir(new):
        if not hasattr(old, attr):
            if debug:
                print('    Adding missing attribute %s' % attr)
            setattr(old, attr, getattr(new, attr))

    if hasattr(old, '__previous_reload_version__'):
        updateClass(old.__previous_reload_version__, new, debug)


def safeStr(obj):
    try:
        s = str(obj)
    except:
        try:
            s = repr(obj)
        except:
            s = '<instance of %s at 0x%x>' % (safeStr(type(obj)), id(obj))

    return s


if __name__ == '__main__':
    doQtTest = True
    try:
        from PyQt4 import QtCore
        if not hasattr(QtCore, 'Signal'):
            QtCore.Signal = QtCore.pyqtSignal

        class Btn(QtCore.QObject):
            sig = QtCore.Signal()

            def emit(self):
                self.sig.emit()


        btn = Btn()
    except:
        raise
        print('Error; skipping Qt tests')
        doQtTest = False

    import os
    if not os.path.isdir('test1'):
        os.mkdir('test1')
    open('test1/__init__.py', 'w')
    modFile1 = 'test1/test1.py'
    modCode1 = '\nimport sys\nclass A(object):\n    def __init__(self, msg):\n        object.__init__(self)\n        self.msg = msg\n    def fn(self, pfx = ""):\n        print(pfx+"A class: %%s %%s" %% (str(self.__class__), str(id(self.__class__))))\n        print(pfx+"  %%s: %d" %% self.msg)\n\nclass B(A):\n    def fn(self, pfx=""):\n        print(pfx+"B class:", self.__class__, id(self.__class__))\n        print(pfx+"  %%s: %d" %% self.msg)\n        print(pfx+"  calling superclass.. (%%s)" %% id(A) )\n        A.fn(self, "  ")\n'
    modFile2 = 'test2.py'
    modCode2 = '\nfrom test1.test1 import A\nfrom test1.test1 import B\n\na1 = A("ax1")\nb1 = B("bx1")\nclass C(A):\n    def __init__(self, msg):\n        #print "| C init:"\n        #print "|   C.__bases__ = ", map(id, C.__bases__)\n        #print "|   A:", id(A)\n        #print "|   A.__init__ = ", id(A.__init__.im_func), id(A.__init__.im_func.__code__), id(A.__init__.im_class)\n        A.__init__(self, msg + "(init from C)")\n        \ndef fn():\n    print("fn: %s")\n'
    open(modFile1, 'w').write(modCode1 % (1, 1))
    open(modFile2, 'w').write(modCode2 % 'message 1')
    import test1.test1 as test1
    import test2
    print('Test 1 originals:')
    A1 = test1.A
    B1 = test1.B
    a1 = test1.A('a1')
    b1 = test1.B('b1')
    a1.fn()
    b1.fn()
    from test2 import fn, C
    if doQtTest:
        print('Button test before:')
        btn.sig.connect(fn)
        btn.sig.connect(a1.fn)
        btn.emit()
        print('')
    print('Test2 before reload:')
    fn()
    oldfn = fn
    test2.a1.fn()
    test2.b1.fn()
    c1 = test2.C('c1')
    c1.fn()
    os.remove(modFile1 + 'c')
    open(modFile1, 'w').write(modCode1 % (2, 2))
    print('\n----RELOAD test1-----\n')
    reloadAll((os.path.abspath(__file__)[:10]), debug=True)
    print('Subclass test:')
    c2 = test2.C('c2')
    c2.fn()
    os.remove(modFile2 + 'c')
    open(modFile2, 'w').write(modCode2 % 'message 2')
    print('\n----RELOAD test2-----\n')
    reloadAll((os.path.abspath(__file__)[:10]), debug=True)
    if doQtTest:
        print('Button test after:')
        btn.emit()
    print('Test2 after reload:')
    fn()
    test2.a1.fn()
    test2.b1.fn()
    print('\n==> Test 1 Old instances:')
    a1.fn()
    b1.fn()
    c1.fn()
    print('\n==> Test 1 New instances:')
    a2 = test1.A('a2')
    b2 = test1.B('b2')
    a2.fn()
    b2.fn()
    c2 = test2.C('c2')
    c2.fn()
    os.remove(modFile1 + 'c')
    os.remove(modFile2 + 'c')
    open(modFile1, 'w').write(modCode1 % (3, 3))
    open(modFile2, 'w').write(modCode2 % 'message 3')
    print('\n----RELOAD-----\n')
    reloadAll((os.path.abspath(__file__)[:10]), debug=True)
    if doQtTest:
        print('Button test after:')
        btn.emit()
    print('Test2 after reload:')
    fn()
    test2.a1.fn()
    test2.b1.fn()
    print('\n==> Test 1 Old instances:')
    a1.fn()
    b1.fn()
    print('function IDs  a1 bound method: %d a1 func: %d  a1 class: %d  b1 func: %d  b1 class: %d' % (id(a1.fn), id(a1.fn.__func__), id(a1.fn.__self__.__class__), id(b1.fn.__func__), id(b1.fn.__self__.__class__)))
    print('\n==> Test 1 New instances:')
    a2 = test1.A('a2')
    b2 = test1.B('b2')
    a2.fn()
    b2.fn()
    print('function IDs  a1 bound method: %d a1 func: %d  a1 class: %d  b1 func: %d  b1 class: %d' % (id(a1.fn), id(a1.fn.__func__), id(a1.fn.__self__.__class__), id(b1.fn.__func__), id(b1.fn.__self__.__class__)))
    os.remove(modFile1)
    os.remove(modFile2)
    os.remove(modFile1 + 'c')
    os.remove(modFile2 + 'c')
    os.system('rm -r test1')