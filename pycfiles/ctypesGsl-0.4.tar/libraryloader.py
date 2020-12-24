# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/alanr/monitor/ctypesgen-davidjamesca/ctypesgen/ctypesgen/libraryloader.py
# Compiled at: 2019-08-18 21:39:19
import os.path, re, sys, glob, platform, ctypes, ctypes.util

def _environ_path(name):
    if name in os.environ:
        return os.environ[name].split(':')
    else:
        return []


class LibraryLoader(object):

    def __init__(self):
        self.other_dirs = []

    def load_library(self, libname):
        """Given the name of a library, load it."""
        paths = self.getpaths(libname)
        for path in paths:
            if os.path.exists(path):
                return self.load(path)

        raise ImportError('%s not found.' % libname)

    def load(self, path):
        """Given a path to a library, load it."""
        try:
            if sys.platform == 'darwin':
                return ctypes.CDLL(path, ctypes.RTLD_GLOBAL)
            else:
                return ctypes.cdll.LoadLibrary(path)

        except OSError as e:
            raise ImportError(e)

    def getpaths(self, libname):
        """Return a list of paths where the library might be found."""
        if os.path.isabs(libname):
            yield libname
        else:
            for path in self.getplatformpaths(libname):
                yield path

        path = ctypes.util.find_library(libname)
        if path:
            yield path

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

    def getplatformpaths(self, libname):
        if os.path.pathsep in libname:
            names = [
             libname]
        else:
            names = [ format % libname for format in self.name_formats ]
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
        dirs = []
        if '/' in libname:
            dirs.extend(_environ_path('DYLD_LIBRARY_PATH'))
        else:
            dirs.extend(_environ_path('LD_LIBRARY_PATH'))
            dirs.extend(_environ_path('DYLD_LIBRARY_PATH'))
        dirs.extend(self.other_dirs)
        dirs.append('.')
        dirs.append(os.path.dirname(__file__))
        if hasattr(sys, 'frozen') and sys.frozen == 'macosx_app':
            dirs.append(os.path.join(os.environ['RESOURCEPATH'], '..', 'Frameworks'))
        dirs.extend(dyld_fallback_library_path)
        return dirs


class PosixLibraryLoader(LibraryLoader):
    _ld_so_cache = None

    def _create_ld_so_cache(self):
        directories = []
        for name in ('LD_LIBRARY_PATH', 'SHLIB_PATH', 'LIBPATH', 'LIBRARY_PATH'):
            if name in os.environ:
                directories.extend(os.environ[name].split(os.pathsep))

        directories.extend(self.other_dirs)
        directories.append('.')
        directories.append(os.path.dirname(__file__))
        try:
            with open('/etc/ld.so.conf') as (f):
                directories.extend([ dir.strip() for dir in f ])
        except IOError:
            pass

        unix_lib_dirs_list = [
         '/lib', '/usr/lib', '/lib64', '/usr/lib64']
        if sys.platform.startswith('linux'):
            bitage = platform.architecture()[0]
            if bitage.startswith('32'):
                unix_lib_dirs_list += ['/lib/i386-linux-gnu', '/usr/lib/i386-linux-gnu']
            elif bitage.startswith('64'):
                unix_lib_dirs_list += ['/lib/x86_64-linux-gnu', '/usr/lib/x86_64-linux-gnu']
            else:
                unix_lib_dirs_list += glob.glob('/lib/*linux-gnu')
        directories.extend(unix_lib_dirs_list)
        cache = {}
        lib_re = re.compile('lib(.*)\\.s[ol]')
        ext_re = re.compile('\\.s[ol]$')
        for dir in directories:
            try:
                for path in glob.glob('%s/*.s[ol]*' % dir):
                    file = os.path.basename(path)
                    if file not in cache:
                        cache[file] = path
                    match = lib_re.match(file)
                    if match:
                        library = match.group(1)
                        if library not in cache:
                            cache[library] = path

            except OSError:
                pass

        self._ld_so_cache = cache

    def getplatformpaths(self, libname):
        if self._ld_so_cache is None:
            self._create_ld_so_cache()
        result = self._ld_so_cache.get(libname)
        if result:
            yield result
        path = ctypes.util.find_library(libname)
        if path:
            yield os.path.join('/lib', path)
        return


class _WindowsLibrary(object):

    def __init__(self, path):
        self.cdll = ctypes.cdll.LoadLibrary(path)
        self.windll = ctypes.windll.LoadLibrary(path)

    def __getattr__(self, name):
        try:
            return getattr(self.cdll, name)
        except AttributeError:
            try:
                return getattr(self.windll, name)
            except AttributeError:
                raise


class WindowsLibraryLoader(LibraryLoader):
    name_formats = [
     '%s.dll', 'lib%s.dll', '%slib.dll']

    def load_library(self, libname):
        try:
            result = LibraryLoader.load_library(self, libname)
        except ImportError:
            result = None
            if os.path.sep not in libname:
                for name in self.name_formats:
                    try:
                        result = getattr(ctypes.cdll, name % libname)
                        if result:
                            break
                    except WindowsError:
                        result = None

            if result is None:
                try:
                    result = getattr(ctypes.cdll, libname)
                except WindowsError:
                    result = None

            if result is None:
                raise ImportError('%s not found.' % libname)

        return result

    def load(self, path):
        return _WindowsLibrary(path)

    def getplatformpaths(self, libname):
        if os.path.sep not in libname:
            for name in self.name_formats:
                dll_in_current_dir = os.path.abspath(name % libname)
                if os.path.exists(dll_in_current_dir):
                    yield dll_in_current_dir
                path = ctypes.util.find_library(name % libname)
                if path:
                    yield path


loaderclass = {'darwin': DarwinLibraryLoader, 
   'cygwin': WindowsLibraryLoader, 
   'win32': WindowsLibraryLoader}
loader = loaderclass.get(sys.platform, PosixLibraryLoader)()

def add_library_search_dirs(other_dirs):
    """
    Add libraries to search paths.
    If library paths are relative, convert them to absolute with respect to this
    file's directory
    """
    for F in other_dirs:
        if not os.path.isabs(F):
            F = os.path.abspath(F)
        loader.other_dirs.append(F)


load_library = loader.load_library
del loaderclass