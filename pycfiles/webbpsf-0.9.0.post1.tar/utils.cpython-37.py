# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rgeda/project/repo/webbpsf/astropy_helpers/astropy_helpers/utils.py
# Compiled at: 2019-07-20 17:47:20
# Size of source mod 2**32: 25574 bytes
from __future__ import absolute_import, unicode_literals
import contextlib, functools, imp, inspect, os, sys, glob, textwrap, types, warnings
try:
    from importlib import machinery as import_machinery
    if not hasattr(import_machinery, 'SourceLoader'):
        import_machinery = None
except ImportError:
    import_machinery = None

from importlib import invalidate_caches

class AstropyWarning(Warning):
    __doc__ = '\n    The base warning class from which all Astropy warnings should inherit.\n\n    Any warning inheriting from this class is handled by the Astropy logger.\n    '


class AstropyDeprecationWarning(AstropyWarning):
    __doc__ = '\n    A warning class to indicate a deprecated feature.\n    '


class AstropyPendingDeprecationWarning(PendingDeprecationWarning, AstropyWarning):
    __doc__ = '\n    A warning class to indicate a soon-to-be deprecated feature.\n    '


def _get_platlib_dir(cmd):
    """
    Given a build command, return the name of the appropriate platform-specific
    build subdirectory directory (e.g. build/lib.linux-x86_64-2.7)
    """
    plat_specifier = '.{0}-{1}'.format(cmd.plat_name, sys.version[0:3])
    return os.path.join(cmd.build_base, 'lib' + plat_specifier)


def get_numpy_include_path():
    """
    Gets the path to the numpy headers.
    """
    import builtins
    if hasattr(builtins, '__NUMPY_SETUP__'):
        del builtins.__NUMPY_SETUP__
    import imp, numpy
    imp.reload(numpy)
    try:
        numpy_include = numpy.get_include()
    except AttributeError:
        numpy_include = numpy.get_numpy_include()

    return numpy_include


class _DummyFile(object):
    __doc__ = 'A noop writeable object.'
    errors = ''

    def write(self, s):
        pass

    def flush(self):
        pass


@contextlib.contextmanager
def silence():
    """A context manager that silences sys.stdout and sys.stderr."""
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = _DummyFile()
    sys.stderr = _DummyFile()
    exception_occurred = False
    try:
        yield
    except:
        exception_occurred = True
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        raise

    if not exception_occurred:
        sys.stdout = old_stdout
        sys.stderr = old_stderr


if sys.platform == 'win32':
    import ctypes

    def _has_hidden_attribute(filepath):
        """
        Returns True if the given filepath has the hidden attribute on
        MS-Windows.  Based on a post here:
        http://stackoverflow.com/questions/284115/cross-platform-hidden-file-detection
        """
        if isinstance(filepath, bytes):
            filepath = filepath.decode(sys.getfilesystemencoding())
        try:
            attrs = ctypes.windll.kernel32.GetFileAttributesW(filepath)
            assert attrs != -1
            result = bool(attrs & 2)
        except (AttributeError, AssertionError):
            result = False

        return result


else:

    def _has_hidden_attribute(filepath):
        return False


def is_path_hidden(filepath):
    """
    Determines if a given file or directory is hidden.

    Parameters
    ----------
    filepath : str
        The path to a file or directory

    Returns
    -------
    hidden : bool
        Returns `True` if the file is hidden
    """
    name = os.path.basename(os.path.abspath(filepath))
    if isinstance(name, bytes):
        is_dotted = name.startswith(b'.')
    else:
        is_dotted = name.startswith('.')
    return is_dotted or _has_hidden_attribute(filepath)


def walk_skip_hidden(top, onerror=None, followlinks=False):
    """
    A wrapper for `os.walk` that skips hidden files and directories.

    This function does not have the parameter `topdown` from
    `os.walk`: the directories must always be recursed top-down when
    using this function.

    See also
    --------
    os.walk : For a description of the parameters
    """
    for root, dirs, files in os.walk(top,
      topdown=True, onerror=onerror, followlinks=followlinks):
        dirs[:] = [d for d in dirs if not is_path_hidden(d)]
        files[:] = [f for f in files if not is_path_hidden(f)]
        yield (root, dirs, files)


def write_if_different(filename, data):
    """Write `data` to `filename`, if the content of the file is different.

    Parameters
    ----------
    filename : str
        The file name to be written to.
    data : bytes
        The data to be written to `filename`.
    """
    if not isinstance(data, bytes):
        raise AssertionError
    elif os.path.exists(filename):
        with open(filename, 'rb') as (fd):
            original_data = fd.read()
    else:
        original_data = None
    if original_data != data:
        with open(filename, 'wb') as (fd):
            fd.write(data)


def import_file(filename, name=None):
    """
    Imports a module from a single file as if it doesn't belong to a
    particular package.

    The returned module will have the optional ``name`` if given, or else
    a name generated from the filename.
    """
    mode = 'r'
    if name is None:
        basename = os.path.splitext(filename)[0]
        name = '_'.join(os.path.relpath(basename).split(os.sep)[1:])
    elif import_machinery:
        loader = import_machinery.SourceFileLoader(name, filename)
        mod = loader.load_module()
    else:
        with open(filename, mode) as (fd):
            mod = imp.load_module(name, fd, filename, ('.py', mode, 1))
    return mod


def resolve_name(name):
    """Resolve a name like ``module.object`` to an object and return it.

    Raise `ImportError` if the module or name is not found.
    """
    parts = name.split('.')
    cursor = len(parts) - 1
    module_name = parts[:cursor]
    attr_name = parts[(-1)]
    while cursor > 0:
        try:
            ret = __import__(('.'.join(module_name)), fromlist=[attr_name])
            break
        except ImportError:
            if cursor == 0:
                raise
            cursor -= 1
            module_name = parts[:cursor]
            attr_name = parts[cursor]
            ret = ''

    for part in parts[cursor:]:
        try:
            ret = getattr(ret, part)
        except AttributeError:
            raise ImportError(name)

    return ret


def extends_doc(extended_func):
    """
    A function decorator for use when wrapping an existing function but adding
    additional functionality.  This copies the docstring from the original
    function, and appends to it (along with a newline) the docstring of the
    wrapper function.

    Examples
    --------

        >>> def foo():
        ...     '''Hello.'''
        ...
        >>> @extends_doc(foo)
        ... def bar():
        ...     '''Goodbye.'''
        ...
        >>> print(bar.__doc__)
        Hello.

        Goodbye.

    """

    def decorator(func):
        if not extended_func.__doc__ is None:
            if not func.__doc__ is None:
                func.__doc__ = '\n\n'.join([extended_func.__doc__.rstrip('\n'),
                 func.__doc__.lstrip('\n')])
        return func

    return decorator


def deprecated(since, message='', name='', alternative='', pending=False, obj_type=None):
    """
    Used to mark a function or class as deprecated.

    To mark an attribute as deprecated, use `deprecated_attribute`.

    Parameters
    ----------
    since : str
        The release at which this API became deprecated.  This is
        required.

    message : str, optional
        Override the default deprecation message.  The format
        specifier ``func`` may be used for the name of the function,
        and ``alternative`` may be used in the deprecation message
        to insert the name of an alternative to the deprecated
        function. ``obj_type`` may be used to insert a friendly name
        for the type of object being deprecated.

    name : str, optional
        The name of the deprecated function or class; if not provided
        the name is automatically determined from the passed in
        function or class, though this is useful in the case of
        renamed functions, where the new function is just assigned to
        the name of the deprecated function.  For example::

            def new_function():
                ...
            oldFunction = new_function

    alternative : str, optional
        An alternative function or class name that the user may use in
        place of the deprecated object.  The deprecation warning will
        tell the user about this alternative if provided.

    pending : bool, optional
        If True, uses a AstropyPendingDeprecationWarning instead of a
        AstropyDeprecationWarning.

    obj_type : str, optional
        The type of this object, if the automatically determined one
        needs to be overridden.
    """
    method_types = (
     classmethod, staticmethod, types.MethodType)

    def deprecate_doc(old_doc, message):
        if not old_doc:
            old_doc = ''
        old_doc = textwrap.dedent(old_doc).strip('\n')
        new_doc = '\n.. deprecated:: %(since)s\n    %(message)s\n\n' % {'since':since, 
         'message':message.strip()} + old_doc
        if not old_doc:
            new_doc += '\\ '
        return new_doc

    def get_function(func):
        if isinstance(func, method_types):
            func = func.__func__
        return func

    def deprecate_function(func, message):
        if isinstance(func, method_types):
            func_wrapper = type(func)
        else:
            func_wrapper = lambda f: f
        func = get_function(func)

        def deprecated_func(*args, **kwargs):
            if pending:
                category = AstropyPendingDeprecationWarning
            else:
                category = AstropyDeprecationWarning
            warnings.warn(message, category, stacklevel=2)
            return func(*args, **kwargs)

        if type(func) != type(str.__dict__['__add__']):
            deprecated_func = functools.wraps(func)(deprecated_func)
        deprecated_func.__doc__ = deprecate_doc(deprecated_func.__doc__, message)
        return func_wrapper(deprecated_func)

    def deprecate_class(cls, message):
        members = cls.__dict__.copy()
        members.update({'__doc__':deprecate_doc(cls.__doc__, message), 
         '__init__':deprecate_function(get_function(cls.__init__), message)})
        return type(cls.__name__, cls.__bases__, members)

    def deprecate(obj, message=message, name=name, alternative=alternative, pending=pending):
        if obj_type is None:
            if isinstance(obj, type):
                obj_type_name = 'class'
            elif inspect.isfunction(obj):
                obj_type_name = 'function'
            elif inspect.ismethod(obj) or isinstance(obj, method_types):
                obj_type_name = 'method'
            else:
                obj_type_name = 'object'
        else:
            obj_type_name = obj_type
        if not name:
            name = get_function(obj).__name__
        else:
            altmessage = ''
            if not message or type(message) == type(deprecate):
                if pending:
                    message = 'The %(func)s %(obj_type)s will be deprecated in a future version.'
                else:
                    message = 'The %(func)s %(obj_type)s is deprecated and may be removed in a future version.'
                if alternative:
                    altmessage = '\n        Use %s instead.' % alternative
        message = message % {'func':name, 
         'name':name, 
         'alternative':alternative, 
         'obj_type':obj_type_name} + altmessage
        if isinstance(obj, type):
            return deprecate_class(obj, message)
        return deprecate_function(obj, message)

    if type(message) == type(deprecate):
        return deprecate(message)
    return deprecate


def deprecated_attribute(name, since, message=None, alternative=None, pending=False):
    """
    Used to mark a public attribute as deprecated.  This creates a
    property that will warn when the given attribute name is accessed.
    To prevent the warning (i.e. for internal code), use the private
    name for the attribute by prepending an underscore
    (i.e. ``self._name``).

    Parameters
    ----------
    name : str
        The name of the deprecated attribute.

    since : str
        The release at which this API became deprecated.  This is
        required.

    message : str, optional
        Override the default deprecation message.  The format
        specifier ``name`` may be used for the name of the attribute,
        and ``alternative`` may be used in the deprecation message
        to insert the name of an alternative to the deprecated
        function.

    alternative : str, optional
        An alternative attribute that the user may use in place of the
        deprecated attribute.  The deprecation warning will tell the
        user about this alternative if provided.

    pending : bool, optional
        If True, uses a AstropyPendingDeprecationWarning instead of a
        AstropyDeprecationWarning.

    Examples
    --------

    ::

        class MyClass:
            # Mark the old_name as deprecated
            old_name = misc.deprecated_attribute('old_name', '0.1')

            def method(self):
                self._old_name = 42
    """
    private_name = '_' + name

    @deprecated(since, name=name, obj_type='attribute')
    def get(self):
        return getattr(self, private_name)

    @deprecated(since, name=name, obj_type='attribute')
    def set(self, val):
        setattr(self, private_name, val)

    @deprecated(since, name=name, obj_type='attribute')
    def delete(self):
        delattr(self, private_name)

    return property(get, set, delete)


def minversion(module, version, inclusive=True, version_path='__version__'):
    """
    Returns `True` if the specified Python module satisfies a minimum version
    requirement, and `False` if not.

    By default this uses `pkg_resources.parse_version` to do the version
    comparison if available.  Otherwise it falls back on
    `distutils.version.LooseVersion`.

    Parameters
    ----------

    module : module or `str`
        An imported module of which to check the version, or the name of
        that module (in which case an import of that module is attempted--
        if this fails `False` is returned).

    version : `str`
        The version as a string that this module must have at a minimum (e.g.
        ``'0.12'``).

    inclusive : `bool`
        The specified version meets the requirement inclusively (i.e. ``>=``)
        as opposed to strictly greater than (default: `True`).

    version_path : `str`
        A dotted attribute path to follow in the module for the version.
        Defaults to just ``'__version__'``, which should work for most Python
        modules.

    Examples
    --------

    >>> import astropy
    >>> minversion(astropy, '0.4.4')
    True
    """
    if isinstance(module, types.ModuleType):
        module_name = module.__name__
    else:
        if isinstance(module, str):
            module_name = module
            try:
                module = resolve_name(module_name)
            except ImportError:
                return False

        else:
            raise ValueError('module argument must be an actual imported module, or the import name of the module; got {0!r}'.format(module))
    if '.' not in version_path:
        have_version = getattr(module, version_path)
    else:
        have_version = resolve_name('.'.join([module.__name__, version_path]))
    try:
        from pkg_resources import parse_version
    except ImportError:
        import distutils.version as parse_version

    if inclusive:
        return parse_version(have_version) >= parse_version(version)
    return parse_version(have_version) > parse_version(version)


class classproperty(property):
    __doc__ = '\n    Similar to `property`, but allows class-level properties.  That is,\n    a property whose getter is like a `classmethod`.\n\n    The wrapped method may explicitly use the `classmethod` decorator (which\n    must become before this decorator), or the `classmethod` may be omitted\n    (it is implicit through use of this decorator).\n\n    .. note::\n\n        classproperty only works for *read-only* properties.  It does not\n        currently allow writeable/deleteable properties, due to subtleties of how\n        Python descriptors work.  In order to implement such properties on a class\n        a metaclass for that class must be implemented.\n\n    Parameters\n    ----------\n    fget : callable\n        The function that computes the value of this property (in particular,\n        the function when this is used as a decorator) a la `property`.\n\n    doc : str, optional\n        The docstring for the property--by default inherited from the getter\n        function.\n\n    lazy : bool, optional\n        If True, caches the value returned by the first call to the getter\n        function, so that it is only called once (used for lazy evaluation\n        of an attribute).  This is analogous to `lazyproperty`.  The ``lazy``\n        argument can also be used when `classproperty` is used as a decorator\n        (see the third example below).  When used in the decorator syntax this\n        *must* be passed in as a keyword argument.\n\n    Examples\n    --------\n\n    ::\n\n        >>> class Foo(object):\n        ...     _bar_internal = 1\n        ...     @classproperty\n        ...     def bar(cls):\n        ...         return cls._bar_internal + 1\n        ...\n        >>> Foo.bar\n        2\n        >>> foo_instance = Foo()\n        >>> foo_instance.bar\n        2\n        >>> foo_instance._bar_internal = 2\n        >>> foo_instance.bar  # Ignores instance attributes\n        2\n\n    As previously noted, a `classproperty` is limited to implementing\n    read-only attributes::\n\n        >>> class Foo(object):\n        ...     _bar_internal = 1\n        ...     @classproperty\n        ...     def bar(cls):\n        ...         return cls._bar_internal\n        ...     @bar.setter\n        ...     def bar(cls, value):\n        ...         cls._bar_internal = value\n        ...\n        Traceback (most recent call last):\n        ...\n        NotImplementedError: classproperty can only be read-only; use a\n        metaclass to implement modifiable class-level properties\n\n    When the ``lazy`` option is used, the getter is only called once::\n\n        >>> class Foo(object):\n        ...     @classproperty(lazy=True)\n        ...     def bar(cls):\n        ...         print("Performing complicated calculation")\n        ...         return 1\n        ...\n        >>> Foo.bar\n        Performing complicated calculation\n        1\n        >>> Foo.bar\n        1\n\n    If a subclass inherits a lazy `classproperty` the property is still\n    re-evaluated for the subclass::\n\n        >>> class FooSub(Foo):\n        ...     pass\n        ...\n        >>> FooSub.bar\n        Performing complicated calculation\n        1\n        >>> FooSub.bar\n        1\n    '

    def __new__(cls, fget=None, doc=None, lazy=False):
        if fget is None:

            def wrapper(func):
                return cls(func, lazy=lazy)

            return wrapper
        return super(classproperty, cls).__new__(cls)

    def __init__(self, fget, doc=None, lazy=False):
        self._lazy = lazy
        if lazy:
            self._cache = {}
        fget = self._wrap_fget(fget)
        super(classproperty, self).__init__(fget=fget, doc=doc)
        if doc is not None:
            self.__doc__ = doc

    def __get__(self, obj, objtype=None):
        if self._lazy:
            if objtype in self._cache:
                return self._cache[objtype]
        elif objtype is not None:
            val = self.fget.__wrapped__(objtype)
        else:
            val = super(classproperty, self).__get__(obj, objtype=objtype)
        if self._lazy:
            if objtype is None:
                objtype = obj.__class__
            self._cache[objtype] = val
        return val

    def getter(self, fget):
        return super(classproperty, self).getter(self._wrap_fget(fget))

    def setter(self, fset):
        raise NotImplementedError('classproperty can only be read-only; use a metaclass to implement modifiable class-level properties')

    def deleter(self, fdel):
        raise NotImplementedError('classproperty can only be read-only; use a metaclass to implement modifiable class-level properties')

    @staticmethod
    def _wrap_fget(orig_fget):
        if isinstance(orig_fget, classmethod):
            orig_fget = orig_fget.__func__

        @functools.wraps(orig_fget)
        def fget(obj):
            return orig_fget(obj.__class__)

        fget.__wrapped__ = orig_fget
        return fget


def find_data_files(package, pattern):
    """
    Include files matching ``pattern`` inside ``package``.

    Parameters
    ----------
    package : str
        The package inside which to look for data files
    pattern : str
        Pattern (glob-style) to match for the data files (e.g. ``*.dat``).
        This supports the``**``recursive syntax. For example, ``**/*.fits``
        matches all files ending with ``.fits`` recursively. Only one
        instance of ``**`` can be included in the pattern.
    """
    return glob.glob((os.path.join(package, pattern)), recursive=True)