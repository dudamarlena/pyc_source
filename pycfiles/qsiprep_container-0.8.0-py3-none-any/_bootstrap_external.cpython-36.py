# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/circleci/.pyenv/versions/3.6.5/lib/python3.6/_bootstrap_external.py
# Compiled at: 2019-03-22 00:31:38
# Size of source mod 2**32: 54487 bytes
"""Core implementation of path-based import.

This module is NOT meant to be directly imported! It has been designed such
that it can be bootstrapped into Python as the implementation of import. As
such it requires the injection of specific modules and attributes in order to
work. One should use importlib as the public-facing version of this module.

"""
_CASE_INSENSITIVE_PLATFORMS_STR_KEY = ('win', )
_CASE_INSENSITIVE_PLATFORMS_BYTES_KEY = ('cygwin', 'darwin')
_CASE_INSENSITIVE_PLATFORMS = _CASE_INSENSITIVE_PLATFORMS_BYTES_KEY + _CASE_INSENSITIVE_PLATFORMS_STR_KEY

def _make_relax_case():
    if sys.platform.startswith(_CASE_INSENSITIVE_PLATFORMS):
        if sys.platform.startswith(_CASE_INSENSITIVE_PLATFORMS_STR_KEY):
            key = 'PYTHONCASEOK'
        else:
            key = b'PYTHONCASEOK'

        def _relax_case():
            return key in _os.environ

    else:

        def _relax_case():
            """True if filenames must be checked case-insensitively."""
            return False

    return _relax_case


def _w_long(x):
    """Convert a 32-bit integer to little-endian."""
    return (int(x) & 4294967295).to_bytes(4, 'little')


def _r_long(int_bytes):
    """Convert 4 bytes in little-endian to an integer."""
    return int.from_bytes(int_bytes, 'little')


def _path_join(*path_parts):
    """Replacement for os.path.join()."""
    return path_sep.join([part.rstrip(path_separators) for part in path_parts if part])


def _path_split(path):
    """Replacement for os.path.split()."""
    if len(path_separators) == 1:
        front, _, tail = path.rpartition(path_sep)
        return (
         front, tail)
    else:
        for x in reversed(path):
            if x in path_separators:
                front, tail = path.rsplit(x, maxsplit=1)
                return (front, tail)

        return (
         '', path)


def _path_stat(path):
    """Stat the path.

    Made a separate function to make it easier to override in experiments
    (e.g. cache stat results).

    """
    return _os.stat(path)


def _path_is_mode_type(path, mode):
    """Test whether the path is the specified mode type."""
    try:
        stat_info = _path_stat(path)
    except OSError:
        return False
    else:
        return stat_info.st_mode & 61440 == mode


def _path_isfile(path):
    """Replacement for os.path.isfile."""
    return _path_is_mode_type(path, 32768)


def _path_isdir(path):
    """Replacement for os.path.isdir."""
    if not path:
        path = _os.getcwd()
    return _path_is_mode_type(path, 16384)


def _write_atomic(path, data, mode=438):
    """Best-effort function to write data to a path atomically.
    Be prepared to handle a FileExistsError if concurrent writing of the
    temporary file is attempted."""
    path_tmp = '{}.{}'.format(path, id(path))
    fd = _os.open(path_tmp, _os.O_EXCL | _os.O_CREAT | _os.O_WRONLY, mode & 438)
    try:
        with _io.FileIO(fd, 'wb') as (file):
            file.write(data)
        _os.replace(path_tmp, path)
    except OSError:
        try:
            _os.unlink(path_tmp)
        except OSError:
            pass

        raise


_code_type = type(_write_atomic.__code__)
MAGIC_NUMBER = (3379).to_bytes(2, 'little') + b'\r\n'
_RAW_MAGIC_NUMBER = int.from_bytes(MAGIC_NUMBER, 'little')
_PYCACHE = '__pycache__'
_OPT = 'opt-'
SOURCE_SUFFIXES = [
 '.py']
BYTECODE_SUFFIXES = [
 '.pyc']
DEBUG_BYTECODE_SUFFIXES = OPTIMIZED_BYTECODE_SUFFIXES = BYTECODE_SUFFIXES

def cache_from_source(path, debug_override=None, *, optimization=None):
    """Given the path to a .py file, return the path to its .pyc file.

    The .py file does not need to exist; this simply returns the path to the
    .pyc file calculated as if the .py file were imported.

    The 'optimization' parameter controls the presumed optimization level of
    the bytecode file. If 'optimization' is not None, the string representation
    of the argument is taken and verified to be alphanumeric (else ValueError
    is raised).

    The debug_override parameter is deprecated. If debug_override is not None,
    a True value is the same as setting 'optimization' to the empty string
    while a False value is equivalent to setting 'optimization' to '1'.

    If sys.implementation.cache_tag is None then NotImplementedError is raised.

    """
    if debug_override is not None:
        _warnings.warn("the debug_override parameter is deprecated; use 'optimization' instead", DeprecationWarning)
        if optimization is not None:
            message = 'debug_override or optimization must be set to None'
            raise TypeError(message)
        optimization = '' if debug_override else 1
    else:
        path = _os.fspath(path)
        head, tail = _path_split(path)
        base, sep, rest = tail.rpartition('.')
        tag = sys.implementation.cache_tag
        if tag is None:
            raise NotImplementedError('sys.implementation.cache_tag is None')
        almost_filename = ''.join([base if base else rest, sep, tag])
        if optimization is None:
            if sys.flags.optimize == 0:
                optimization = ''
            else:
                optimization = sys.flags.optimize
        optimization = str(optimization)
        if optimization != '':
            if not optimization.isalnum():
                raise ValueError('{!r} is not alphanumeric'.format(optimization))
            almost_filename = '{}.{}{}'.format(almost_filename, _OPT, optimization)
    return _path_join(head, _PYCACHE, almost_filename + BYTECODE_SUFFIXES[0])


def source_from_cache(path):
    """Given the path to a .pyc. file, return the path to its .py file.

    The .pyc file does not need to exist; this simply returns the path to
    the .py file calculated to correspond to the .pyc file.  If path does
    not conform to PEP 3147/488 format, ValueError will be raised. If
    sys.implementation.cache_tag is None then NotImplementedError is raised.

    """
    if sys.implementation.cache_tag is None:
        raise NotImplementedError('sys.implementation.cache_tag is None')
    else:
        path = _os.fspath(path)
        head, pycache_filename = _path_split(path)
        head, pycache = _path_split(head)
        if pycache != _PYCACHE:
            raise ValueError('{} not bottom-level directory in {!r}'.format(_PYCACHE, path))
        dot_count = pycache_filename.count('.')
        if dot_count not in frozenset({2, 3}):
            raise ValueError('expected only 2 or 3 dots in {!r}'.format(pycache_filename))
        elif dot_count == 3:
            optimization = pycache_filename.rsplit('.', 2)[(-2)]
            if not optimization.startswith(_OPT):
                raise ValueError('optimization portion of filename does not start with {!r}'.format(_OPT))
            opt_level = optimization[len(_OPT):]
            if not opt_level.isalnum():
                raise ValueError('optimization level {!r} is not an alphanumeric value'.format(optimization))
    base_filename = pycache_filename.partition('.')[0]
    return _path_join(head, base_filename + SOURCE_SUFFIXES[0])


def _get_sourcefile(bytecode_path):
    """Convert a bytecode file path to a source path (if possible).

    This function exists purely for backwards-compatibility for
    PyImport_ExecCodeModuleWithFilenames() in the C API.

    """
    if len(bytecode_path) == 0:
        return
    else:
        rest, _, extension = bytecode_path.rpartition('.')
        if not rest or extension.lower()[-3:-1] != 'py':
            return bytecode_path
        try:
            source_path = source_from_cache(bytecode_path)
        except (NotImplementedError, ValueError):
            source_path = bytecode_path[:-1]

        if _path_isfile(source_path):
            return source_path
        return bytecode_path


def _get_cached(filename):
    if filename.endswith(tuple(SOURCE_SUFFIXES)):
        try:
            return cache_from_source(filename)
        except NotImplementedError:
            pass

    else:
        if filename.endswith(tuple(BYTECODE_SUFFIXES)):
            return filename
        else:
            return


def _calc_mode(path):
    """Calculate the mode permissions for a bytecode file."""
    try:
        mode = _path_stat(path).st_mode
    except OSError:
        mode = 438

    mode |= 128
    return mode


def _check_name(method):
    """Decorator to verify that the module being requested matches the one the
    loader can handle.

    The first argument (self) must define _name which the second argument is
    compared against. If the comparison fails then ImportError is raised.

    """

    def _check_name_wrapper(self, name=None, *args, **kwargs):
        if name is None:
            name = self.name
        else:
            if self.name != name:
                raise ImportError(('loader for %s cannot handle %s' % (
                 self.name, name)),
                  name=name)
        return method(self, name, *args, **kwargs)

    try:
        _wrap = _bootstrap._wrap
    except NameError:

        def _wrap(new, old):
            for replace in ('__module__', '__name__', '__qualname__', '__doc__'):
                if hasattr(old, replace):
                    setattr(new, replace, getattr(old, replace))

            new.__dict__.update(old.__dict__)

    _wrap(_check_name_wrapper, method)
    return _check_name_wrapper


def _find_module_shim(self, fullname):
    """Try to find a loader for the specified module by delegating to
    self.find_loader().

    This method is deprecated in favor of finder.find_spec().

    """
    loader, portions = self.find_loader(fullname)
    if loader is None:
        if len(portions):
            msg = 'Not importing directory {}: missing __init__'
            _warnings.warn(msg.format(portions[0]), ImportWarning)
    return loader


def _validate_bytecode_header(data, source_stats=None, name=None, path=None):
    """Validate the header of the passed-in bytecode against source_stats (if
    given) and returning the bytecode that can be compiled by compile().

    All other arguments are used to enhance error reporting.

    ImportError is raised when the magic number is incorrect or the bytecode is
    found to be stale. EOFError is raised when the data is found to be
    truncated.

    """
    exc_details = {}
    if name is not None:
        exc_details['name'] = name
    else:
        name = '<bytecode>'
    if path is not None:
        exc_details['path'] = path
    magic = data[:4]
    raw_timestamp = data[4:8]
    raw_size = data[8:12]
    if magic != MAGIC_NUMBER:
        message = 'bad magic number in {!r}: {!r}'.format(name, magic)
        _bootstrap._verbose_message('{}', message)
        raise ImportError(message, **exc_details)
    else:
        if len(raw_timestamp) != 4:
            message = 'reached EOF while reading timestamp in {!r}'.format(name)
            _bootstrap._verbose_message('{}', message)
            raise EOFError(message)
        else:
            if len(raw_size) != 4:
                message = 'reached EOF while reading size of source in {!r}'.format(name)
                _bootstrap._verbose_message('{}', message)
                raise EOFError(message)
    if source_stats is not None:
        try:
            source_mtime = int(source_stats['mtime'])
        except KeyError:
            pass
        else:
            if _r_long(raw_timestamp) != source_mtime:
                message = 'bytecode is stale for {!r}'.format(name)
                _bootstrap._verbose_message('{}', message)
                raise ImportError(message, **exc_details)
            try:
                source_size = source_stats['size'] & 4294967295
            except KeyError:
                pass
            else:
                if _r_long(raw_size) != source_size:
                    raise ImportError(('bytecode is stale for {!r}'.format(name)), **exc_details)
    return data[12:]


def _compile_bytecode(data, name=None, bytecode_path=None, source_path=None):
    """Compile bytecode as returned by _validate_bytecode_header()."""
    code = marshal.loads(data)
    if isinstance(code, _code_type):
        _bootstrap._verbose_message('code object from {!r}', bytecode_path)
        if source_path is not None:
            _imp._fix_co_filename(code, source_path)
        return code
    raise ImportError(('Non-code object in {!r}'.format(bytecode_path)), name=name,
      path=bytecode_path)


def _code_to_bytecode(code, mtime=0, source_size=0):
    """Compile a code object into bytecode for writing out to a byte-compiled
    file."""
    data = bytearray(MAGIC_NUMBER)
    data.extend(_w_long(mtime))
    data.extend(_w_long(source_size))
    data.extend(marshal.dumps(code))
    return data


def decode_source(source_bytes):
    """Decode bytes representing source code and return the string.

    Universal newline support is used in the decoding.
    """
    import tokenize
    source_bytes_readline = _io.BytesIO(source_bytes).readline
    encoding = tokenize.detect_encoding(source_bytes_readline)
    newline_decoder = _io.IncrementalNewlineDecoder(None, True)
    return newline_decoder.decode(source_bytes.decode(encoding[0]))


_POPULATE = object()

def spec_from_file_location(name, location=None, *, loader=None, submodule_search_locations=_POPULATE):
    """Return a module spec based on a file location.

    To indicate that the module is a package, set
    submodule_search_locations to a list of directory paths.  An
    empty list is sufficient, though its not otherwise useful to the
    import system.

    The loader must take a spec as its only __init__() arg.

    """
    if location is None:
        location = '<unknown>'
        if hasattr(loader, 'get_filename'):
            try:
                location = loader.get_filename(name)
            except ImportError:
                pass

        else:
            location = _os.fspath(location)
    else:
        spec = _bootstrap.ModuleSpec(name, loader, origin=location)
        spec._set_fileattr = True
        if loader is None:
            for loader_class, suffixes in _get_supported_file_loaders():
                if location.endswith(tuple(suffixes)):
                    loader = loader_class(name, location)
                    spec.loader = loader
                    break
            else:
                return

        if submodule_search_locations is _POPULATE:
            if hasattr(loader, 'is_package'):
                try:
                    is_package = loader.is_package(name)
                except ImportError:
                    pass
                else:
                    if is_package:
                        spec.submodule_search_locations = []
        else:
            spec.submodule_search_locations = submodule_search_locations
    if spec.submodule_search_locations == []:
        if location:
            dirname = _path_split(location)[0]
            spec.submodule_search_locations.append(dirname)
    return spec


class WindowsRegistryFinder:
    __doc__ = 'Meta path finder for modules declared in the Windows registry.'
    REGISTRY_KEY = 'Software\\Python\\PythonCore\\{sys_version}\\Modules\\{fullname}'
    REGISTRY_KEY_DEBUG = 'Software\\Python\\PythonCore\\{sys_version}\\Modules\\{fullname}\\Debug'
    DEBUG_BUILD = False

    @classmethod
    def _open_registry(cls, key):
        try:
            return _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, key)
        except OSError:
            return _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, key)

    @classmethod
    def _search_registry(cls, fullname):
        if cls.DEBUG_BUILD:
            registry_key = cls.REGISTRY_KEY_DEBUG
        else:
            registry_key = cls.REGISTRY_KEY
        key = registry_key.format(fullname=fullname, sys_version=('%d.%d' % sys.version_info[:2]))
        try:
            with cls._open_registry(key) as (hkey):
                filepath = _winreg.QueryValue(hkey, '')
        except OSError:
            return
        else:
            return filepath

    @classmethod
    def find_spec(cls, fullname, path=None, target=None):
        filepath = cls._search_registry(fullname)
        if filepath is None:
            return
        try:
            _path_stat(filepath)
        except OSError:
            return
        else:
            for loader, suffixes in _get_supported_file_loaders():
                if filepath.endswith(tuple(suffixes)):
                    spec = _bootstrap.spec_from_loader(fullname, (loader(fullname, filepath)),
                      origin=filepath)
                    return spec

    @classmethod
    def find_module(cls, fullname, path=None):
        """Find module named in the registry.

        This method is deprecated.  Use exec_module() instead.

        """
        spec = cls.find_spec(fullname, path)
        if spec is not None:
            return spec.loader
        else:
            return


class _LoaderBasics:
    __doc__ = 'Base class of common code needed by both SourceLoader and\n    SourcelessFileLoader.'

    def is_package(self, fullname):
        """Concrete implementation of InspectLoader.is_package by checking if
        the path returned by get_filename has a filename of '__init__.py'."""
        filename = _path_split(self.get_filename(fullname))[1]
        filename_base = filename.rsplit('.', 1)[0]
        tail_name = fullname.rpartition('.')[2]
        return filename_base == '__init__' and tail_name != '__init__'

    def create_module(self, spec):
        """Use default semantics for module creation."""
        pass

    def exec_module(self, module):
        """Execute the module."""
        code = self.get_code(module.__name__)
        if code is None:
            raise ImportError('cannot load module {!r} when get_code() returns None'.format(module.__name__))
        _bootstrap._call_with_frames_removed(exec, code, module.__dict__)

    def load_module(self, fullname):
        """This module is deprecated."""
        return _bootstrap._load_module_shim(self, fullname)


class SourceLoader(_LoaderBasics):

    def path_mtime(self, path):
        """Optional method that returns the modification time (an int) for the
        specified path, where path is a str.

        Raises IOError when the path cannot be handled.
        """
        raise IOError

    def path_stats(self, path):
        """Optional method returning a metadata dict for the specified path
        to by the path (str).
        Possible keys:
        - 'mtime' (mandatory) is the numeric timestamp of last source
          code modification;
        - 'size' (optional) is the size in bytes of the source code.

        Implementing this method allows the loader to read bytecode files.
        Raises IOError when the path cannot be handled.
        """
        return {'mtime': self.path_mtime(path)}

    def _cache_bytecode(self, source_path, cache_path, data):
        """Optional method which writes data (bytes) to a file path (a str).

        Implementing this method allows for the writing of bytecode files.

        The source path is needed in order to correctly transfer permissions
        """
        return self.set_data(cache_path, data)

    def set_data(self, path, data):
        """Optional method which writes data (bytes) to a file path (a str).

        Implementing this method allows for the writing of bytecode files.
        """
        pass

    def get_source(self, fullname):
        """Concrete implementation of InspectLoader.get_source."""
        path = self.get_filename(fullname)
        try:
            source_bytes = self.get_data(path)
        except OSError as exc:
            raise ImportError('source not available through get_data()', name=fullname) from exc

        return decode_source(source_bytes)

    def source_to_code(self, data, path, *, _optimize=-1):
        """Return the code object compiled from source.

        The 'data' argument can be any object type that compile() supports.
        """
        return _bootstrap._call_with_frames_removed(compile, data, path, 'exec', dont_inherit=True,
          optimize=_optimize)

    def get_code(self, fullname):
        """Concrete implementation of InspectLoader.get_code.

        Reading of bytecode requires path_stats to be implemented. To write
        bytecode, set_data must also be implemented.

        """
        source_path = self.get_filename(fullname)
        source_mtime = None
        try:
            bytecode_path = cache_from_source(source_path)
        except NotImplementedError:
            bytecode_path = None
        else:
            try:
                st = self.path_stats(source_path)
            except IOError:
                pass
            else:
                source_mtime = int(st['mtime'])
        try:
            data = self.get_data(bytecode_path)
        except OSError:
            pass
        else:
            try:
                bytes_data = _validate_bytecode_header(data, source_stats=st,
                  name=fullname,
                  path=bytecode_path)
            except (ImportError, EOFError):
                pass
            else:
                _bootstrap._verbose_message('{} matches {}', bytecode_path, source_path)
                return _compile_bytecode(bytes_data, name=fullname, bytecode_path=bytecode_path,
                  source_path=source_path)
            source_bytes = self.get_data(source_path)
            code_object = self.source_to_code(source_bytes, source_path)
            _bootstrap._verbose_message('code object from {}', source_path)
            if not sys.dont_write_bytecode:
                if bytecode_path is not None:
                    if source_mtime is not None:
                        data = _code_to_bytecode(code_object, source_mtime, len(source_bytes))
                        try:
                            self._cache_bytecode(source_path, bytecode_path, data)
                            _bootstrap._verbose_message('wrote {!r}', bytecode_path)
                        except NotImplementedError:
                            pass

            return code_object


class FileLoader:
    __doc__ = 'Base file loader class which implements the loader protocol methods that\n    require file system usage.'

    def __init__(self, fullname, path):
        """Cache the module name and the path to the file found by the
        finder."""
        self.name = fullname
        self.path = path

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(self.name) ^ hash(self.path)

    @_check_name
    def load_module(self, fullname):
        return super(FileLoader, self).load_module(fullname)

    @_check_name
    def get_filename(self, fullname):
        """Return the path to the source file as found by the finder."""
        return self.path

    def get_data(self, path):
        """Return the data from path as raw bytes."""
        with _io.FileIO(path, 'r') as (file):
            return file.read()


class SourceFileLoader(FileLoader, SourceLoader):
    __doc__ = 'Concrete implementation of SourceLoader using the file system.'

    def path_stats(self, path):
        """Return the metadata for the path."""
        st = _path_stat(path)
        return {'mtime':st.st_mtime,  'size':st.st_size}

    def _cache_bytecode(self, source_path, bytecode_path, data):
        mode = _calc_mode(source_path)
        return self.set_data(bytecode_path, data, _mode=mode)

    def set_data(self, path, data, *, _mode=438):
        """Write bytes data to a file."""
        parent, filename = _path_split(path)
        path_parts = []
        while parent and not _path_isdir(parent):
            parent, part = _path_split(parent)
            path_parts.append(part)

        for part in reversed(path_parts):
            parent = _path_join(parent, part)
            try:
                _os.mkdir(parent)
            except FileExistsError:
                continue
            except OSError as exc:
                _bootstrap._verbose_message('could not create {!r}: {!r}', parent, exc)
                return

        try:
            _write_atomic(path, data, _mode)
            _bootstrap._verbose_message('created {!r}', path)
        except OSError as exc:
            _bootstrap._verbose_message('could not create {!r}: {!r}', path, exc)


class SourcelessFileLoader(FileLoader, _LoaderBasics):
    __doc__ = 'Loader which handles sourceless file imports.'

    def get_code(self, fullname):
        path = self.get_filename(fullname)
        data = self.get_data(path)
        bytes_data = _validate_bytecode_header(data, name=fullname, path=path)
        return _compile_bytecode(bytes_data, name=fullname, bytecode_path=path)

    def get_source(self, fullname):
        """Return None as there is no source code."""
        pass


EXTENSION_SUFFIXES = []

class ExtensionFileLoader(FileLoader, _LoaderBasics):
    __doc__ = 'Loader for extension modules.\n\n    The constructor is designed to work with FileFinder.\n\n    '

    def __init__(self, name, path):
        self.name = name
        self.path = path

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(self.name) ^ hash(self.path)

    def create_module(self, spec):
        """Create an unitialized extension module"""
        module = _bootstrap._call_with_frames_removed(_imp.create_dynamic, spec)
        _bootstrap._verbose_message('extension module {!r} loaded from {!r}', spec.name, self.path)
        return module

    def exec_module(self, module):
        """Initialize an extension module"""
        _bootstrap._call_with_frames_removed(_imp.exec_dynamic, module)
        _bootstrap._verbose_message('extension module {!r} executed from {!r}', self.name, self.path)

    def is_package(self, fullname):
        """Return True if the extension module is a package."""
        file_name = _path_split(self.path)[1]
        return any(file_name == '__init__' + suffix for suffix in EXTENSION_SUFFIXES)

    def get_code(self, fullname):
        """Return None as an extension module cannot create a code object."""
        pass

    def get_source(self, fullname):
        """Return None as extension modules have no source code."""
        pass

    @_check_name
    def get_filename(self, fullname):
        """Return the path to the source file as found by the finder."""
        return self.path


class _NamespacePath:
    __doc__ = "Represents a namespace package's path.  It uses the module name\n    to find its parent module, and from there it looks up the parent's\n    __path__.  When this changes, the module's own path is recomputed,\n    using path_finder.  For top-level modules, the parent module's path\n    is sys.path."

    def __init__(self, name, path, path_finder):
        self._name = name
        self._path = path
        self._last_parent_path = tuple(self._get_parent_path())
        self._path_finder = path_finder

    def _find_parent_path_names(self):
        """Returns a tuple of (parent-module-name, parent-path-attr-name)"""
        parent, dot, me = self._name.rpartition('.')
        if dot == '':
            return ('sys', 'path')
        else:
            return (
             parent, '__path__')

    def _get_parent_path(self):
        parent_module_name, path_attr_name = self._find_parent_path_names()
        return getattr(sys.modules[parent_module_name], path_attr_name)

    def _recalculate(self):
        parent_path = tuple(self._get_parent_path())
        if parent_path != self._last_parent_path:
            spec = self._path_finder(self._name, parent_path)
            if spec is not None:
                if spec.loader is None:
                    if spec.submodule_search_locations:
                        self._path = spec.submodule_search_locations
            self._last_parent_path = parent_path
        return self._path

    def __iter__(self):
        return iter(self._recalculate())

    def __setitem__(self, index, path):
        self._path[index] = path

    def __len__(self):
        return len(self._recalculate())

    def __repr__(self):
        return '_NamespacePath({!r})'.format(self._path)

    def __contains__(self, item):
        return item in self._recalculate()

    def append(self, item):
        self._path.append(item)


class _NamespaceLoader:

    def __init__(self, name, path, path_finder):
        self._path = _NamespacePath(name, path, path_finder)

    @classmethod
    def module_repr(cls, module):
        """Return repr for the module.

        The method is deprecated.  The import machinery does the job itself.

        """
        return '<module {!r} (namespace)>'.format(module.__name__)

    def is_package(self, fullname):
        return True

    def get_source(self, fullname):
        return ''

    def get_code(self, fullname):
        return compile('', '<string>', 'exec', dont_inherit=True)

    def create_module(self, spec):
        """Use default semantics for module creation."""
        pass

    def exec_module(self, module):
        pass

    def load_module(self, fullname):
        """Load a namespace module.

        This method is deprecated.  Use exec_module() instead.

        """
        _bootstrap._verbose_message('namespace module loaded with path {!r}', self._path)
        return _bootstrap._load_module_shim(self, fullname)


class PathFinder:
    __doc__ = 'Meta path finder for sys.path and package __path__ attributes.'

    @classmethod
    def invalidate_caches(cls):
        """Call the invalidate_caches() method on all path entry finders
        stored in sys.path_importer_caches (where implemented)."""
        for finder in sys.path_importer_cache.values():
            if hasattr(finder, 'invalidate_caches'):
                finder.invalidate_caches()

    @classmethod
    def _path_hooks(cls, path):
        """Search sys.path_hooks for a finder for 'path'."""
        if sys.path_hooks is not None:
            if not sys.path_hooks:
                _warnings.warn('sys.path_hooks is empty', ImportWarning)
        for hook in sys.path_hooks:
            try:
                return hook(path)
            except ImportError:
                continue

        else:
            return

    @classmethod
    def _path_importer_cache(cls, path):
        """Get the finder for the path entry from sys.path_importer_cache.

        If the path entry is not in the cache, find the appropriate finder
        and cache it. If no finder is available, store None.

        """
        if path == '':
            try:
                path = _os.getcwd()
            except FileNotFoundError:
                return

        try:
            finder = sys.path_importer_cache[path]
        except KeyError:
            finder = cls._path_hooks(path)
            sys.path_importer_cache[path] = finder

        return finder

    @classmethod
    def _legacy_get_spec(cls, fullname, finder):
        if hasattr(finder, 'find_loader'):
            loader, portions = finder.find_loader(fullname)
        else:
            loader = finder.find_module(fullname)
            portions = []
        if loader is not None:
            return _bootstrap.spec_from_loader(fullname, loader)
        else:
            spec = _bootstrap.ModuleSpec(fullname, None)
            spec.submodule_search_locations = portions
            return spec

    @classmethod
    def _get_spec(cls, fullname, path, target=None):
        """Find the loader or namespace_path for this module/package name."""
        namespace_path = []
        for entry in path:
            if not isinstance(entry, (str, bytes)):
                pass
            else:
                finder = cls._path_importer_cache(entry)
                if finder is not None:
                    if hasattr(finder, 'find_spec'):
                        spec = finder.find_spec(fullname, target)
                    else:
                        spec = cls._legacy_get_spec(fullname, finder)
                    if spec is None:
                        pass
                    else:
                        if spec.loader is not None:
                            return spec
                        portions = spec.submodule_search_locations
                        if portions is None:
                            raise ImportError('spec missing loader')
                        namespace_path.extend(portions)
        else:
            spec = _bootstrap.ModuleSpec(fullname, None)
            spec.submodule_search_locations = namespace_path
            return spec

    @classmethod
    def find_spec(cls, fullname, path=None, target=None):
        """Try to find a spec for 'fullname' on sys.path or 'path'.

        The search is based on sys.path_hooks and sys.path_importer_cache.
        """
        if path is None:
            path = sys.path
        else:
            spec = cls._get_spec(fullname, path, target)
            if spec is None:
                return
            if spec.loader is None:
                namespace_path = spec.submodule_search_locations
                if namespace_path:
                    spec.origin = 'namespace'
                    spec.submodule_search_locations = _NamespacePath(fullname, namespace_path, cls._get_spec)
                    return spec
                else:
                    return
            else:
                return spec

    @classmethod
    def find_module(cls, fullname, path=None):
        """find the module on sys.path or 'path' based on sys.path_hooks and
        sys.path_importer_cache.

        This method is deprecated.  Use find_spec() instead.

        """
        spec = cls.find_spec(fullname, path)
        if spec is None:
            return
        else:
            return spec.loader


class FileFinder:
    __doc__ = 'File-based finder.\n\n    Interactions with the file system are cached for performance, being\n    refreshed when the directory the finder is handling has been modified.\n\n    '

    def __init__(self, path, *loader_details):
        """Initialize with the path to search on and a variable number of
        2-tuples containing the loader and the file suffixes the loader
        recognizes."""
        loaders = []
        for loader, suffixes in loader_details:
            loaders.extend((suffix, loader) for suffix in suffixes)

        self._loaders = loaders
        self.path = path or '.'
        self._path_mtime = -1
        self._path_cache = set()
        self._relaxed_path_cache = set()

    def invalidate_caches(self):
        """Invalidate the directory mtime."""
        self._path_mtime = -1

    find_module = _find_module_shim

    def find_loader(self, fullname):
        """Try to find a loader for the specified module, or the namespace
        package portions. Returns (loader, list-of-portions).

        This method is deprecated.  Use find_spec() instead.

        """
        spec = self.find_spec(fullname)
        if spec is None:
            return (None, [])
        else:
            return (
             spec.loader, spec.submodule_search_locations or [])

    def _get_spec(self, loader_class, fullname, path, smsl, target):
        loader = loader_class(fullname, path)
        return spec_from_file_location(fullname, path, loader=loader, submodule_search_locations=smsl)

    def find_spec(self, fullname, target=None):
        """Try to find a spec for the specified module.

        Returns the matching spec, or None if not found.
        """
        is_namespace = False
        tail_module = fullname.rpartition('.')[2]
        try:
            mtime = _path_stat(self.path or _os.getcwd()).st_mtime
        except OSError:
            mtime = -1

        if mtime != self._path_mtime:
            self._fill_cache()
            self._path_mtime = mtime
        else:
            if _relax_case():
                cache = self._relaxed_path_cache
                cache_module = tail_module.lower()
            else:
                cache = self._path_cache
                cache_module = tail_module
        if cache_module in cache:
            base_path = _path_join(self.path, tail_module)
            for suffix, loader_class in self._loaders:
                init_filename = '__init__' + suffix
                full_path = _path_join(base_path, init_filename)
                if _path_isfile(full_path):
                    return self._get_spec(loader_class, fullname, full_path, [base_path], target)
            else:
                is_namespace = _path_isdir(base_path)

        for suffix, loader_class in self._loaders:
            full_path = _path_join(self.path, tail_module + suffix)
            _bootstrap._verbose_message('trying {}', full_path, verbosity=2)
            if cache_module + suffix in cache:
                if _path_isfile(full_path):
                    return self._get_spec(loader_class, fullname, full_path, None, target)

        if is_namespace:
            _bootstrap._verbose_message('possible namespace for {}', base_path)
            spec = _bootstrap.ModuleSpec(fullname, None)
            spec.submodule_search_locations = [base_path]
            return spec

    def _fill_cache(self):
        """Fill the cache of potential modules and packages for this directory."""
        path = self.path
        try:
            contents = _os.listdir(path or _os.getcwd())
        except (FileNotFoundError, PermissionError, NotADirectoryError):
            contents = []

        if not sys.platform.startswith('win'):
            self._path_cache = set(contents)
        else:
            lower_suffix_contents = set()
            for item in contents:
                name, dot, suffix = item.partition('.')
                if dot:
                    new_name = '{}.{}'.format(name, suffix.lower())
                else:
                    new_name = name
                lower_suffix_contents.add(new_name)

            self._path_cache = lower_suffix_contents
        if sys.platform.startswith(_CASE_INSENSITIVE_PLATFORMS):
            self._relaxed_path_cache = {fn.lower() for fn in contents}

    @classmethod
    def path_hook(cls, *loader_details):
        """A class method which returns a closure to use on sys.path_hook
        which will return an instance using the specified loaders and the path
        called on the closure.

        If the path called on the closure is not a directory, ImportError is
        raised.

        """

        def path_hook_for_FileFinder(path):
            if not _path_isdir(path):
                raise ImportError('only directories are supported', path=path)
            return cls(path, *loader_details)

        return path_hook_for_FileFinder

    def __repr__(self):
        return 'FileFinder({!r})'.format(self.path)


def _fix_up_module(ns, name, pathname, cpathname=None):
    loader = ns.get('__loader__')
    spec = ns.get('__spec__')
    if not loader:
        if spec:
            loader = spec.loader
        else:
            if pathname == cpathname:
                loader = SourcelessFileLoader(name, pathname)
            else:
                loader = SourceFileLoader(name, pathname)
    if not spec:
        spec = spec_from_file_location(name, pathname, loader=loader)
    try:
        ns['__spec__'] = spec
        ns['__loader__'] = loader
        ns['__file__'] = pathname
        ns['__cached__'] = cpathname
    except Exception:
        pass


def _get_supported_file_loaders():
    """Returns a list of file-based module loaders.

    Each item is a tuple (loader, suffixes).
    """
    extensions = (
     ExtensionFileLoader, _imp.extension_suffixes())
    source = (SourceFileLoader, SOURCE_SUFFIXES)
    bytecode = (SourcelessFileLoader, BYTECODE_SUFFIXES)
    return [extensions, source, bytecode]


def _setup(_bootstrap_module):
    """Setup the path-based importers for importlib by importing needed
    built-in modules and injecting them into the global namespace.

    Other components are extracted from the core bootstrap module.

    """
    global _bootstrap
    global _imp
    global sys
    _bootstrap = _bootstrap_module
    sys = _bootstrap.sys
    _imp = _bootstrap._imp
    self_module = sys.modules[__name__]
    for builtin_name in ('_io', '_warnings', 'builtins', 'marshal'):
        if builtin_name not in sys.modules:
            builtin_module = _bootstrap._builtin_from_name(builtin_name)
        else:
            builtin_module = sys.modules[builtin_name]
        setattr(self_module, builtin_name, builtin_module)

    os_details = (
     (
      'posix', ['/']), ('nt', ['\\', '/']))
    for builtin_os, path_separators in os_details:
        assert all(len(sep) == 1 for sep in path_separators)
        path_sep = path_separators[0]
        if builtin_os in sys.modules:
            os_module = sys.modules[builtin_os]
            break
        else:
            try:
                os_module = _bootstrap._builtin_from_name(builtin_os)
                break
            except ImportError:
                continue

    else:
        raise ImportError('importlib requires posix or nt')

    setattr(self_module, '_os', os_module)
    setattr(self_module, 'path_sep', path_sep)
    setattr(self_module, 'path_separators', ''.join(path_separators))
    try:
        thread_module = _bootstrap._builtin_from_name('_thread')
    except ImportError:
        thread_module = None

    setattr(self_module, '_thread', thread_module)
    weakref_module = _bootstrap._builtin_from_name('_weakref')
    setattr(self_module, '_weakref', weakref_module)
    if builtin_os == 'nt':
        winreg_module = _bootstrap._builtin_from_name('winreg')
        setattr(self_module, '_winreg', winreg_module)
    setattr(self_module, '_relax_case', _make_relax_case())
    EXTENSION_SUFFIXES.extend(_imp.extension_suffixes())
    if builtin_os == 'nt':
        SOURCE_SUFFIXES.append('.pyw')
        if '_d.pyd' in EXTENSION_SUFFIXES:
            WindowsRegistryFinder.DEBUG_BUILD = True


def _install(_bootstrap_module):
    """Install the path-based import components."""
    _setup(_bootstrap_module)
    supported_loaders = _get_supported_file_loaders()
    sys.path_hooks.extend([(FileFinder.path_hook)(*supported_loaders)])
    sys.meta_path.append(PathFinder)