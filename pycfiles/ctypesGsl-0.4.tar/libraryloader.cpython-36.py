# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/alanr/monitor/ctypesgen-davidjamesca/ctypesgen/ctypesgen/libraryloader.py
# Compiled at: 2019-12-10 16:20:40
# Size of source mod 2**32: 12258 bytes
import os.path, re, sys, glob, platform, ctypes, ctypes.util

def _environ_path(name):
    if name in os.environ:
        return os.environ[name].split(':')
    else:
        return []


class LibraryLoader(object):
    name_formats = [
     '%s']

    class Lookup(object):
        mode = ctypes.DEFAULT_MODE

        def __init__(self, path):
            super(LibraryLoader.Lookup, self).__init__()
            self.access = dict(cdecl=(ctypes.CDLL(path, self.mode)))

        def get(self, name, calling_convention='cdecl'):
            if calling_convention not in self.access:
                raise LookupError("Unknown calling convention '{}' for function '{}'".format(calling_convention, name))
            return getattr(self.access[calling_convention], name)

        def has(self, name, calling_convention='cdecl'):
            if calling_convention not in self.access:
                return False
            else:
                return hasattr(self.access[calling_convention], name)

        def __getattr__(self, name):
            return getattr(self.access['cdecl'], name)

    def __init__(self):
        self.other_dirs = []

    def __call__(self, libname):
        """Given the name of a library, load it."""
        paths = self.getpaths(libname)
        for path in paths:
            try:
                return self.Lookup(path)
            except:
                pass

        raise ImportError('Could not load %s.' % libname)

    def getpaths(self, libname):
        """Return a list of paths where the library might be found."""
        if os.path.isabs(libname):
            yield libname
        else:
            for dir_i in self.other_dirs:
                for fmt in self.name_formats:
                    yield os.path.join(dir_i, fmt % libname)

            for fmt in self.name_formats:
                yield os.path.abspath(os.path.join(os.path.dirname(__file__), fmt % libname))

            for fmt in self.name_formats:
                path = ctypes.util.find_library(fmt % libname)
                if path:
                    yield path

            for path in self.getplatformpaths(libname):
                yield path

            for fmt in self.name_formats:
                yield os.path.abspath(os.path.join(os.path.curdir, fmt % libname))

    def getplatformpaths(self, libname):
        return []


class DarwinLibraryLoader(LibraryLoader):
    name_formats = [
     'lib%s.dylib',
     'lib%s.so',
     'lib%s.bundle',
     '%s.dylib',
     '%s.so',
     '%s.bundle',
     '%s']

    class Lookup(LibraryLoader.Lookup):
        mode = ctypes.RTLD_GLOBAL

    def getplatformpaths(self, libname):
        if os.path.pathsep in libname:
            names = [
             libname]
        else:
            names = [format % libname for format in self.name_formats]
        for dir in self.getdirs(libname):
            for name in names:
                yield os.path.join(dir, name)

    def getdirs(self, libname):
        """Implements the dylib search as specified in Apple documentation:

        http://developer.apple.com/documentation/DeveloperTools/Conceptual/
            DynamicLibraries/Articles/DynamicLibraryUsageGuidelines.html

        Before commencing the standard search, the method first checks
        the bundle's ``Frameworks`` directory if the application is running
        within a bundle (OS X .app).
        """
        dyld_fallback_library_path = _environ_path('DYLD_FALLBACK_LIBRARY_PATH')
        if not dyld_fallback_library_path:
            dyld_fallback_library_path = [
             os.path.expanduser('~/lib'), '/usr/local/lib', '/usr/lib']
        else:
            dirs = []
            if '/' in libname:
                dirs.extend(_environ_path('DYLD_LIBRARY_PATH'))
            else:
                dirs.extend(_environ_path('LD_LIBRARY_PATH'))
                dirs.extend(_environ_path('DYLD_LIBRARY_PATH'))
        if hasattr(sys, 'frozen'):
            if sys.frozen == 'macosx_app':
                dirs.append(os.path.join(os.environ['RESOURCEPATH'], '..', 'Frameworks'))
        dirs.extend(dyld_fallback_library_path)
        return dirs


class PosixLibraryLoader(LibraryLoader):
    _ld_so_cache = None
    _include = re.compile('^\\s*include\\s+(?P<pattern>.*)')

    class _Directories(dict):

        def __init__(self):
            self.order = 0

        def add(self, directory):
            if len(directory) > 1:
                directory = directory.rstrip(os.path.sep)
            else:
                if not os.path.exists(directory):
                    return
                o = self.setdefault(directory, self.order)
                if o == self.order:
                    self.order += 1

        def extend(self, directories):
            for d in directories:
                self.add(d)

        def ordered(self):
            return (i[0] for i in sorted((self.items()), key=(lambda D: D[1])))

    def _get_ld_so_conf_dirs(self, conf, dirs):
        """
        Recursive funtion to help parse all ld.so.conf files, including proper
        handling of the `include` directive.
        """
        try:
            with open(conf) as (f):
                for D in f:
                    D = D.strip()
                    if not D:
                        pass
                    else:
                        m = self._include.match(D)
                        if not m:
                            dirs.add(D)
                        else:
                            for D2 in glob.glob(m.group('pattern')):
                                self._get_ld_so_conf_dirs(D2, dirs)

        except IOError:
            pass

    def _create_ld_so_cache(self):
        directories = self._Directories()
        for name in ('LD_LIBRARY_PATH', 'SHLIB_PATH', 'LIBPATH', 'LIBRARY_PATH'):
            if name in os.environ:
                directories.extend(os.environ[name].split(os.pathsep))

        self._get_ld_so_conf_dirs('/etc/ld.so.conf', directories)
        bitage = platform.architecture()[0]
        unix_lib_dirs_list = []
        if bitage.startswith('64'):
            unix_lib_dirs_list += ['/lib64', '/usr/lib64']
        unix_lib_dirs_list += ['/lib', '/usr/lib']
        if sys.platform.startswith('linux'):
            if bitage.startswith('32'):
                unix_lib_dirs_list += ['/lib/i386-linux-gnu', '/usr/lib/i386-linux-gnu']
            else:
                if bitage.startswith('64'):
                    unix_lib_dirs_list += ['/lib/x86_64-linux-gnu', '/usr/lib/x86_64-linux-gnu']
                else:
                    unix_lib_dirs_list += glob.glob('/lib/*linux-gnu')
        directories.extend(unix_lib_dirs_list)
        cache = {}
        lib_re = re.compile('lib(.*)\\.s[ol]')
        ext_re = re.compile('\\.s[ol]$')
        for dir in directories.ordered():
            try:
                for path in glob.glob('%s/*.s[ol]*' % dir):
                    file = os.path.basename(path)
                    cache_i = cache.setdefault(file, set())
                    cache_i.add(path)
                    match = lib_re.match(file)
                    if match:
                        library = match.group(1)
                        cache_i = cache.setdefault(library, set())
                        cache_i.add(path)

            except OSError:
                pass

        self._ld_so_cache = cache

    def getplatformpaths(self, libname):
        if self._ld_so_cache is None:
            self._create_ld_so_cache()
        result = self._ld_so_cache.get(libname, set())
        for i in result:
            yield i


class WindowsLibraryLoader(LibraryLoader):
    name_formats = [
     '%s.dll', 'lib%s.dll', '%slib.dll', '%s']

    class Lookup(LibraryLoader.Lookup):

        def __init__(self, path):
            super(WindowsLibraryLoader.Lookup, self).__init__(path)
            self.access['stdcall'] = ctypes.windll.LoadLibrary(path)


loaderclass = {'darwin':DarwinLibraryLoader, 
 'cygwin':WindowsLibraryLoader, 
 'win32':WindowsLibraryLoader, 
 'msys':WindowsLibraryLoader}
load_library = loaderclass.get(sys.platform, PosixLibraryLoader)()

def add_library_search_dirs(other_dirs):
    """
    Add libraries to search paths.
    If library paths are relative, convert them to absolute with respect to this
    file's directory
    """
    for F in other_dirs:
        if not os.path.isabs(F):
            F = os.path.abspath(F)
        load_library.other_dirs.append(F)


del loaderclass