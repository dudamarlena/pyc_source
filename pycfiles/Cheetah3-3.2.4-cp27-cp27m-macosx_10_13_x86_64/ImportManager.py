# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.macosx-10.13-x86_64-2.7/Cheetah/ImportManager.py
# Compiled at: 2019-09-22 10:12:27
"""
Provides an emulator/replacement for Python's standard import system.

@@TR: Be warned that Import Hooks are in the deepest, darkest corner of
Python's jungle.  If you need to start hacking with this, be prepared to get
lost for a while. Also note, this module predates the newstyle import hooks in
Python 2.3 http://www.python.org/peps/pep-0302.html.

This is a hacked/documented version of Gordon McMillan's iu.py. I have:

  - made it a little less terse

  - added docstrings and explanatations

  - standardized the variable naming scheme

  - reorganized the code layout to enhance readability
"""
import marshal, py_compile, sys
from Cheetah.compat import PY2, string_type, new_module, get_suffixes, load_module_from_file, RecursionError
if PY2:
    import imp
else:
    import importlib.machinery
_installed = False
_os_stat = _os_path_join = _os_getcwd = _os_path_dirname = None

def _os_bootstrap():
    """
    Set up 'os' module replacement functions for use during import bootstrap
    """
    global _os_getcwd
    global _os_path_dirname
    global _os_path_join
    global _os_stat
    names = sys.builtin_module_names
    join = dirname = None
    if 'posix' in names:
        sep = '/'
        from posix import stat, getcwd
    elif 'nt' in names:
        sep = '\\'
        from nt import stat, getcwd
    elif 'dos' in names:
        sep = '\\'
        from dos import stat, getcwd
    elif 'os2' in names:
        sep = '\\'
        from os2 import stat, getcwd
    elif 'mac' in names:
        from mac import stat, getcwd

        def join(a, b):
            if a == '':
                return b
            if ':' not in a:
                a = ':' + a
            if a[-1:] != ':':
                a = a + ':'
            return a + b

    else:
        raise ImportError('no os specific module found')
    if join is None:

        def join(a, b, sep=sep):
            if a == '':
                return b
            lastchar = a[-1:]
            if lastchar == '/' or lastchar == sep:
                return a + b
            return a + sep + b

    if dirname is None:

        def dirname(a, sep=sep):
            for i in range(len(a) - 1, -1, -1):
                c = a[i]
                if c == '/' or c == sep:
                    return a[:i]

            return ''

    _os_stat = stat
    _os_path_join = join
    _os_path_dirname = dirname
    _os_getcwd = getcwd
    return


_os_bootstrap()

def packageName(s):
    for i in range(len(s) - 1, -1, -1):
        if s[i] == '.':
            break
    else:
        return ''

    return s[:i]


def nameSplit(s):
    rslt = []
    i = j = 0
    for j in range(len(s)):
        if s[j] == '.':
            rslt.append(s[i:j])
            i = j + 1

    if i < len(s):
        rslt.append(s[i:])
    return rslt


def getPathExt(fnm):
    for i in range(len(fnm) - 1, -1, -1):
        if fnm[i] == '.':
            return fnm[i:]

    return ''


def pathIsDir(pathname):
    """Local replacement for os.path.isdir()."""
    try:
        s = _os_stat(pathname)
    except OSError:
        return

    return s[0] & 61440 == 16384


def getDescr(fnm):
    ext = getPathExt(fnm)
    for suffix, mode, typ in get_suffixes():
        if suffix == ext:
            return (suffix, mode, typ)


class Owner:
    """An Owner does imports from a particular piece of turf That is, there's
    an Owner for each thing on sys.path There are owners for directories and
    .pyz files.  There could be owners for zip files, or even URLs.  A
    shadowpath (a dictionary mapping the names in sys.path to their owners) is
    used so that sys.path (or a package's __path__) is still a bunch of
    strings.
    """

    def __init__(self, path):
        self.path = path

    def __str__(self):
        return self.path

    def getmod(self, nm):
        return


class DirOwner(Owner):

    def __init__(self, path):
        if path == '':
            path = _os_getcwd()
        if not pathIsDir(path):
            raise ValueError('%s is not a directory' % path)
        Owner.__init__(self, path)

    def getmod(self, nm, getsuffixes=get_suffixes, loadco=marshal.loads, newmod=new_module):
        pth = _os_path_join(self.path, nm)
        possibles = [
         (
          pth, 0, None)]
        if pathIsDir(pth):
            possibles.insert(0, (_os_path_join(pth, '__init__'), 1, pth))
        py = pyc = None
        for pth, ispkg, pkgpth in possibles:
            for ext, mode, typ in getsuffixes():
                attempt = pth + ext
                try:
                    st = _os_stat(attempt)
                except Exception:
                    pass
                else:
                    if typ == 3:
                        return load_module_from_file(nm, nm, attempt)
                    if typ == 1:
                        py = (
                         attempt, st)
                    else:
                        pyc = (
                         attempt, st)

            if py or pyc:
                break

        if py is None and pyc is None:
            return
        else:
            while True:
                if pyc is None or py and pyc[1][8] < py[1][8]:
                    try:
                        with open(py[0], 'r') as (py_code_file):
                            py_code = py_code_file.read()
                        co = compile(py_code + '\n', py[0], 'exec')
                        try:
                            py_compile.compile(py[0])
                        except IOError:
                            pass

                        __file__ = py[0]
                        break
                    except SyntaxError as e:
                        print 'Invalid syntax in %s' % py[0]
                        print e.args
                        raise

                elif pyc:
                    with open(pyc[0], 'rb') as (pyc_file):
                        stuff = pyc_file.read()
                    try:
                        co = loadco(stuff[8:])
                        __file__ = pyc[0]
                        break
                    except (ValueError, EOFError):
                        pyc = None

                else:
                    return

            mod = newmod(nm)
            mod.__file__ = __file__
            if ispkg:
                mod.__path__ = [
                 pkgpth]
                subimporter = PathImportDirector(mod.__path__)
                mod.__importsub__ = subimporter.getmod
            mod.__co__ = co
            return mod


class ImportDirector(Owner):
    """ImportDirectors live on the metapath There's one for builtins, one for
    frozen modules, and one for sys.path Windows gets one for modules gotten
    from the Registry Mac would have them for PY_RESOURCE modules etc.  A
    generalization of Owner - their concept of 'turf' is broader"""
    pass


class BuiltinImportDirector(ImportDirector):
    """Directs imports of builtin modules"""

    def __init__(self):
        self.path = 'Builtins'

    def getmod(self, nm):
        if nm in sys.builtin_module_names:
            try:
                importfunc = __oldimport__
            except NameError:
                importfunc = __import__

            return importfunc(nm)
        else:
            return


class FrozenImportDirector(ImportDirector):
    """Directs imports of frozen modules"""

    def __init__(self):
        self.path = 'FrozenModules'

    def getmod(self, nm):
        mod = None
        if PY2:
            if imp.is_frozen(nm):
                mod = imp.load_module(nm, None, nm, ('', '', imp.PY_FROZEN))
        elif importlib.machinery.FrozenImporter.find_spec(nm):
            mod = importlib.machinery.FrozenImporter.load_module(nm)
        if mod and hasattr(mod, '__path__'):
            mod.__importsub__ = lambda name, pname=nm, owner=self: owner.getmod(pname + '.' + name)
        return mod


class RegistryImportDirector(ImportDirector):
    """Directs imports of modules stored in the Windows Registry"""

    def __init__(self):
        self.path = 'WindowsRegistry'
        self.map = {}
        try:
            import win32api
        except ImportError:
            pass

        HKEY_CURRENT_USER = -2147483647
        HKEY_LOCAL_MACHINE = -2147483646
        KEY_ALL_ACCESS = 983103
        subkey = 'Software\\Python\\PythonCore\\%s\\Modules' % sys.winver
        for root in (HKEY_CURRENT_USER, HKEY_LOCAL_MACHINE):
            try:
                hkey = win32api.RegOpenKeyEx(root, subkey, 0, KEY_ALL_ACCESS)
            except Exception:
                pass
            else:
                numsubkeys, numvalues, lastmodified = win32api.RegQueryInfoKey(hkey)
                for i in range(numsubkeys):
                    subkeyname = win32api.RegEnumKey(hkey, i)
                    hskey = win32api.RegOpenKeyEx(hkey, subkeyname, 0, KEY_ALL_ACCESS)
                    val = win32api.RegQueryValueEx(hskey, '')
                    desc = getDescr(val[0])
                    self.map[subkeyname] = (val[0], desc)
                    hskey.Close()

                hkey.Close()
                break

    def getmod(self, nm):
        stuff = self.map.get(nm)
        if stuff:
            fnm = stuff[0]
            return load_module_from_file(nm, nm, fnm)
        else:
            return


class PathImportDirector(ImportDirector):
    """Directs imports of modules stored on the filesystem."""

    def __init__(self, pathlist=None, importers=None, ownertypes=None):
        if pathlist is None:
            self.path = sys.path
        else:
            self.path = pathlist
        if ownertypes is None:
            self._ownertypes = _globalOwnerTypes
        else:
            self._ownertypes = ownertypes
        if importers:
            self._shadowPath = importers
        else:
            self._shadowPath = {}
        self._inMakeOwner = False
        self._building = {}
        return

    def getmod(self, nm):
        mod = None
        for thing in self.path:
            if isinstance(thing, string_type):
                owner = self._shadowPath.get(thing, -1)
                if owner == -1:
                    owner = self._shadowPath[thing] = self._makeOwner(thing)
                if owner:
                    mod = owner.getmod(nm)
            else:
                mod = thing.getmod(nm)
            if mod:
                break

        return mod

    def _makeOwner(self, path):
        if self._building.get(path):
            return
        else:
            self._building[path] = 1
            owner = None
            for klass in self._ownertypes:
                try:
                    owner = klass(path)
                except Exception:
                    pass
                else:
                    break

            del self._building[path]
            return owner


UNTRIED = -1

class ImportManager:

    def __init__(self):
        self.metapath = [
         BuiltinImportDirector(),
         FrozenImportDirector(),
         RegistryImportDirector(),
         PathImportDirector()]
        self.threaded = 0
        self.rlock = None
        self.locker = None
        self.setThreaded()
        return

    def setThreaded(self):
        thread = sys.modules.get('thread', None)
        if thread and not self.threaded:
            self.threaded = 1
            self.rlock = thread.allocate_lock()
            self._get_ident = thread.get_ident
        return

    def install(self):
        try:
            import builtins as builtin
        except ImportError:
            import __builtin__ as builtin

        builtin.__import__ = self.importHook
        builtin.reload = self.reloadHook

    def importHook(self, name, globals=None, locals=None, fromlist=None, level=-1):
        """
        NOTE: Currently importHook will accept the keyword-argument "level"
        but it will *NOT* use it. Details about the "level" keyword
        argument can be found here:
        https://docs.python.org/2/library/functions.html#__import__
        """
        _sys_modules_get = sys.modules.get
        contexts = [None]
        if globals:
            importernm = globals.get('__name__', '')
            if importernm:
                if hasattr(_sys_modules_get(importernm), '__path__'):
                    contexts.insert(0, importernm)
                else:
                    pkgnm = packageName(importernm)
                    if pkgnm:
                        contexts.insert(0, pkgnm)
        nmparts = nameSplit(name)
        _self_doimport = self.doimport
        threaded = self.threaded
        for context in contexts:
            ctx = context
            for i in range(len(nmparts)):
                nm = nmparts[i]
                if ctx:
                    fqname = ctx + '.' + nm
                else:
                    fqname = nm
                if threaded:
                    self._acquire()
                mod = _sys_modules_get(fqname, UNTRIED)
                if mod is UNTRIED:
                    mod = _self_doimport(nm, ctx, fqname)
                if threaded:
                    self._release()
                if mod:
                    ctx = fqname
                else:
                    break
            else:
                i = i + 1

            if i:
                break

        if i < len(nmparts):
            if ctx and hasattr(sys.modules[ctx], nmparts[i]):
                return sys.modules[nmparts[0]]
            del sys.modules[fqname]
            raise ImportError('No module named %s' % fqname)
        if fromlist is None:
            if context:
                return sys.modules[(context + '.' + nmparts[0])]
            return sys.modules[nmparts[0]]
        else:
            bottommod = sys.modules[ctx]
            if hasattr(bottommod, '__path__'):
                fromlist = list(fromlist)
                i = 0
                while i < len(fromlist):
                    nm = fromlist[i]
                    if nm == '*':
                        fromlist[i:(i + 1)] = list(getattr(bottommod, '__all__', []))
                        if i >= len(fromlist):
                            break
                        nm = fromlist[i]
                    i = i + 1
                    if not hasattr(bottommod, nm):
                        if self.threaded:
                            self._acquire()
                        mod = self.doimport(nm, ctx, ctx + '.' + nm)
                        if self.threaded:
                            self._release()
                        if not mod:
                            raise ImportError('%s not found in %s' % (nm, ctx))

            return bottommod

    def doimport(self, nm, parentnm, fqname):
        if parentnm:
            parent = sys.modules[parentnm]
            if hasattr(parent, '__path__'):
                importfunc = getattr(parent, '__importsub__', None)
                if not importfunc:
                    subimporter = PathImportDirector(parent.__path__)
                    importfunc = parent.__importsub__ = subimporter.getmod
                mod = importfunc(nm)
                if mod:
                    setattr(parent, nm, mod)
            else:
                return
        else:
            for director in self.metapath:
                try:
                    mod = director.getmod(nm)
                except RecursionError:
                    mod = __oldimport__(nm)

                if mod:
                    break

        if mod:
            mod.__name__ = fqname
            sys.modules[fqname] = mod
            if hasattr(mod, '__co__'):
                co = mod.__co__
                del mod.__co__
                exec co in mod.__dict__
            if fqname == 'thread' and not self.threaded:
                self.setThreaded()
        else:
            sys.modules[fqname] = None
        return mod

    def reloadHook(self, mod):
        fqnm = mod.__name__
        nm = nameSplit(fqnm)[(-1)]
        parentnm = packageName(fqnm)
        newmod = self.doimport(nm, parentnm, fqnm)
        mod.__dict__.update(newmod.__dict__)

    def _acquire(self):
        if self.rlock.locked():
            if self.locker == self._get_ident():
                self.lockcount = self.lockcount + 1
                return
        self.rlock.acquire()
        self.locker = self._get_ident()
        self.lockcount = 0

    def _release(self):
        if self.lockcount:
            self.lockcount = self.lockcount - 1
        else:
            self.rlock.release()


_globalOwnerTypes = [
 DirOwner,
 Owner]