# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/xphyle/paths.py
# Compiled at: 2019-12-19 13:30:24
# Size of source mod 2**32: 53973 bytes
"""Convenience functions for working with file paths.

Stdin, stdout, and stderr are treated as acceptable paths in most cases, which
is why the PurePath type (Union[str, os.PurePath]) is used. String paths are
still accepted as inputs, but all outputs will subclasses of os.PurePath.
"""
from abc import ABCMeta, abstractmethod
import errno, functools, inspect, os
from pathlib import PurePath, Path, WindowsPath, PosixPath
import re, shutil, stat, sys, tempfile
from typing import Any, Callable, Dict, Generic, Iterable, List, Match, Optional, Pattern, Sequence, Tuple, TypeVar, Union, cast, overload
import warnings
from xphyle.types import FileMode, ModeArg, ModeAccess, ModeAccessArg, Permission, PermissionSet, PermissionArg, PermissionSetArg, PathType, PathTypeArg, Regexp
from xphyle.urls import parse_url
STDIN_OR_STDOUT_STR = '-'
STDERR_STR = '_'
STDIN_OR_STDOUT = PurePath(STDIN_OR_STDOUT_STR)
STDIN = PurePath('/dev/stdin')
STDOUT = PurePath('/dev/stdout')
STDERR = PurePath('/dev/stderr')
BACKCOMPAT = os.getenv('XPHYLE_BACKCOMPAT') != '0'
IndexOrName = Union[(int, str)]

def deprecated_str_to_path(*args_to_convert: IndexOrName, list_args: Optional[Sequence[IndexOrName]]=None, dict_args: Optional[Sequence[IndexOrName]]=None) -> Callable:
    """Decorator for a function that used to take paths as strings and now only
    takes them as os.PurePath objects. A deprecation warning is issued, and
    the string arguments are converted to paths before calling the function.

    Backward compatibility can be disabled by the XPHYLE_BACKCOMPAT environment
    variable. If set to false (0), the `func` is returned immediately.
    """

    def decorate(func):
        if not BACKCOMPAT:
            return func
        else:

            @functools.wraps(func)
            def new_func(*args, **kwargs):
                warn = False
                new_args = list(args)
                for idx in args_to_convert:
                    if isinstance(idx, int):
                        if len(args) > idx and isinstance(args[idx], str):
                            warn = True
                            new_args[idx] = as_pure_path(args[idx])
                    else:
                        if isinstance(idx, str):
                            if idx in kwargs and isinstance(kwargs[idx], str):
                                warn = True
                                kwargs[idx] = as_pure_path(kwargs[idx])
                        else:
                            raise ValueError("'args_to_convert' must be ints or strings")

                if list_args is not None:

                    def convert_list_arg(l):
                        global warn
                        for i in range(len(l)):
                            if isinstance(l[i], str):
                                warn = True
                                l[i] = as_pure_path(l[i])

                    for idx in list_args:
                        if isinstance(idx, int):
                            if len(args) > idx:
                                if isinstance(args[idx], list):
                                    convert_list_arg(new_args[idx])
                        else:
                            if isinstance(idx, str):
                                if idx in kwargs and isinstance(kwargs[idx], list):
                                    convert_list_arg(kwargs[idx])
                            else:
                                raise ValueError("'list_args' must be ints or strings")

                if dict_args is not None:

                    def convert_dict_arg(d):
                        global warn
                        for key in d.keys():
                            if isinstance(d[key], str):
                                warn = True
                                d[key] = as_pure_path(d[key])

                    for idx in dict_args:
                        if isinstance(idx, int):
                            if len(args) > idx:
                                if isinstance(args[idx], dict):
                                    convert_dict_arg(args[idx])
                        else:
                            if isinstance(idx, str):
                                if idx in kwargs:
                                    if isinstance(kwargs[idx], dict):
                                        convert_dict_arg(kwargs[idx])
                            else:
                                raise ValueError("'dict_args' must be ints or strings")

                if warn:
                    caller = inspect.stack()[3]
                    deprecated(f"Use of {func.__name__} with string path arguments is deprected (lineno {caller[1]}:{caller[2]})")
                return func(*new_args, **kwargs)

            return new_func

    return decorate


def deprecated(msg: str):
    """
    Issues a deprecation warning:

    Args:
        msg: The warning message to display.
    """
    warnings.simplefilter('always', DeprecationWarning)
    warnings.warn(msg, category=DeprecationWarning, stacklevel=2)
    warnings.simplefilter('default', DeprecationWarning)


def as_pure_path(path: Union[(str, PurePath)], access: Optional[ModeAccessArg]=None) -> PurePath:
    """
    Converts a string to a PurePath.

    Args:
        path: String to convert. May be a string path, a stdin/stdout/stderr
            placeholder, or file:// URL. If it is already a PurePath, it is
            returned without modification.
        access: The file access mode, to disambiguate stdin/stdout when `path`
            is the placeholder ('-').

    Returns:
        A PurePath instance. Except with 'path' is a PurePath or
        stdin/stdout/stderr placeholder, the actual return type is a Path
        instance.
    """
    if isinstance(path, str):
        path = convert_std_placeholder(path, access)
    if isinstance(path, PurePath):
        return cast(PurePath, path)
    else:
        url = parse_url(path)
        if url:
            if url.scheme == 'file':
                return Path(url.path)
            raise IOError(f"Cannot convert URL {path} to path", path)
        return Path(path)


def convert_std_placeholder(path: str, access: Optional[Union[(ModeArg, ModeAccessArg)]]=None) -> Union[(str, PurePath)]:
    if path == STDERR_STR:
        return STDERR
    else:
        if path == STDIN_OR_STDOUT_STR:
            if access:
                if isinstance(access, str):
                    access_val = FileMode(access)
                else:
                    if isinstance(access, FileMode):
                        access_val = cast(FileMode, access)
                    else:
                        access_val = cast(ModeAccess, access)
                if access_val.readable:
                    return STDIN
                return STDOUT
            else:
                return STDIN_OR_STDOUT
        else:
            return path


def as_path(path: Union[(str, PurePath)], access: Optional[ModeAccessArg]=None) -> Path:
    """
    Converts a string to a Path. Note that trying to use STDIN/STDOUT/STDERR
    as actual paths on Windows will result in an error.

    Args:
        path: String to convert. May be a string path, a stdin/stdout/stderr
            placeholder, or file:// URL. If it is already a Path, it is
            returned without modification.
        access: The file access mode, to disambiguate stdin/stdout when `path`
            is the placeholder ('-').

    Returns:
        A Path instance.

    Raises:
        ValueError if 'path' is a stdin/stdout placeholder and 'access' is None.
    """
    pure_path = as_pure_path(path, access)
    if pure_path == STDIN_OR_STDOUT:
        raise ValueError("Cannot convert stdin/stdout placeholder ('-') to a path without the access mode.")
    return Path(pure_path)


@deprecated_str_to_path(0, 'path')
def check_std(path: PurePath, error: bool=False) -> bool:
    """
    Checks whether the path is '-' (stdout) or '_' (stderr).

    Args:
        path: The path to check.
        error: Whether an error should be raised if `path` is stdout or stderr.

    Returns:
        True if path is stdout or stderr.

    Raises:
        ValueError if path is stdout or stderr and `error` is True.
    """
    if path in {STDIN_OR_STDOUT, STDIN, STDOUT, STDERR}:
        if error:
            raise ValueError(f"Invalid path: {path}")
        else:
            return True
    return False


@deprecated_str_to_path(0, 'path')
def get_permissions(path: PurePath) -> PermissionSet:
    """
    Gets the permissions of a file/directory.

    Args:
        path: Path of file/directory.

    Returns:
        An PermissionSet.

    Raises:
        IOError if the file/directory doesn't exist.
    """
    return PermissionSet(as_path(path).stat().st_mode)


@deprecated_str_to_path(0, 'path')
def set_permissions(path: PurePath, permissions: PermissionSetArg) -> PermissionSet:
    """
    Sets file stat flags (using chmod).

    Args:
        path: The file to chmod.
        permissions: Stat flags (any of 'r', 'w', 'x', or an
            :class:`PermissionSet`).

    Returns:
        An :class:`PermissionSet`.
    """
    if not isinstance(permissions, PermissionSet):
        permissions = PermissionSet(permissions)
    as_path(path).chmod(permissions.stat_flags)
    return permissions


@deprecated_str_to_path(0, 'path')
def check_access(path: PurePath, permissions: Union[(PermissionArg, PermissionSetArg)]) -> PermissionSet:
    """
    Check that `path` is accessible with the given set of permissions.

    Args:
        path: The path to check.
        permissions: Access specifier (string/int/:class:`ModeAccess`).

    Raises:
        IOError if the path cannot be accessed according to `permissions`.
    """
    if isinstance(permissions, PermissionSet):
        permission_set = cast(PermissionSet, permissions)
    else:
        permission_set = PermissionSet(cast(Union[(PermissionArg, Sequence[PermissionArg])], permissions))
    if check_std(path):
        if path == STDIN_OR_STDOUT:
            if not any(flag in permission_set for flag in {Permission.READ, Permission.WRITE}):
                raise IOError(errno.EACCES, 'STDIN_OR_STDOUT permissions must be r or w', path)
        if path == STDIN:
            if Permission.READ not in permission_set:
                raise IOError(errno.EACCES, 'STDIN permissions must be r', path)
        if path in {STDOUT, STDERR}:
            if Permission.WRITE not in permission_set:
                raise IOError(errno.EACCES, 'STDOUT/STDERR permissions must be w', path)
    else:
        if not os.access(path, permission_set.os_flags):
            raise IOError(errno.EACCES, f"{path} not accessable", path)
    return permission_set


@deprecated_str_to_path(0, 'path')
def abspath(path: PurePath, strict: bool=False) -> PurePath:
    """
    Returns the fully resolved path associated with `path`.

    Args:
        path: Relative or absolute path
        strict: Whether to raise an exception if the path does not exist.

    Returns:
        A PurePath - typically a pathlib.Path, but may be STDOUT or STDERR.

    Examples:
        abspath('foo') # -> /path/to/curdir/foo
        abspath('~/foo') # -> /home/curuser/foo
    """
    if check_std(path):
        return path
    else:
        return as_path(path).expanduser().resolve(strict=strict)


@deprecated_str_to_path(0, 'path')
def get_root(path: Optional[PurePath]=None) -> str:
    """
    Gets the root directory.

    Args:
        path: A path, or '.' to get the root of the working directory, or None
            to get the root of the path to the script. Stdout and stderr are
            not valid arguments.

    Returns:
        A string path to the root directory.
    """
    if path is None:
        path = sys.executable
    else:
        check_std(path, error=True)
    return as_pure_path(path).anchor


@deprecated_str_to_path(0, 'path')
def split_path(path: PurePath, keep_seps: bool=True, resolve: bool=True) -> Tuple[(str, ...)]:
    """
    Splits a path into a (parent_dir, name, *ext) tuple.

    Args:
        path: The path. Stdout and stderr are not valid arguments.
        keep_seps: Whether the extension separators should be kept as part
            of the file extensions
        resolve: Whether to resolve the path before splitting

    Returns:
        A tuple of length >= 2, in which the first element is the parent
        directory, the second element is the file name, and the remaining
        elements are file extensions.

    Examples:
        split_path('myfile.foo.txt', False)
        # -> ('/current/dir', 'myfile', 'foo', 'txt')
        split_path('/usr/local/foobar.gz', True)
        # -> ('/usr/local', 'foobar', '.gz')
    """
    path = as_path(path)
    if resolve:
        path = path.resolve()
    file_parts = tuple(path.name.split(os.extsep))
    if len(file_parts) == 1:
        seps = ()
    else:
        seps = file_parts[1:]
    if keep_seps:
        seps = tuple(f"{os.extsep}{ext}" for ext in file_parts[1:])
    return (
     path.parent, file_parts[0]) + seps


@deprecated_str_to_path(0, 'path')
def filename(path: PurePath) -> str:
    """

    Equivalent to `split_path(path)[1]`.

    Args:
        The path

    Returns:
        The filename part of `path` (without any extensions).
    """
    return split_path(path)[1]


@deprecated_str_to_path(0, 'path')
def resolve_path(path: PurePath, parent: PurePath=None) -> PurePath:
    """
    Resolves the absolute path of the specified file and ensures that the
    file/directory exists.

    Args:
        path: Path to resolve.
        parent: The directory containing `path` if `path` is relative.

    Returns:
        The absolute path.

    Raises:
        IOError: if the path does not exist or is invalid.
    """
    if check_std(path):
        return path
    else:
        if parent:
            path = abspath(parent) / path
        else:
            path = abspath(path)
        path = as_path(path)
        if not path.exists():
            raise IOError(errno.ENOENT, f"{path} does not exist", path)
        return path


@deprecated_str_to_path(0, 'path')
def check_path(path: PurePath, path_type: PathTypeArg=None, permissions: Union[(PermissionArg, PermissionSetArg)]=None) -> PurePath:
    """
    Resolves the path (using `resolve_path`) and checks that the path is of the
    specified type and allows the specified access.

    Args:
        path: The path to check.
        path_type: A string or :class:`PathType` ('f' or 'd').
        permissions: Access flag (string, int, Permission, or PermissionSet).

    Returns:
        The fully resolved path.

    Raises:
        IOError if the path does not exist, is not of the specified type,
        or doesn't allow the specified access.
    """
    path = resolve_path(path)
    if path_type:
        if isinstance(path_type, str):
            path_type = PathType(path_type)
        if not check_std(path):
            path = cast(Path, path)
            is_dir = path.resolve().is_dir()
            if path_type == PathType.FILE:
                if is_dir:
                    raise IOError(errno.EISDIR, f"{path} not a file", path)
            if path_type == PathType.DIR:
                if not is_dir:
                    raise IOError(errno.ENOTDIR, f"{path} not a directory", path)
        elif path_type is not PathType.FILE:
            raise IOError(errno.EISDIR, f"{path} not a file", path)
    if permissions is not None:
        check_access(path, permissions)
    return path


@deprecated_str_to_path(0, 'path')
def check_readable_file(path: PurePath) -> PurePath:
    """
    Checks that `path` exists and is readable.

    Args:
        path: The path to check

    Returns:
        The fully resolved path of `path`
    """
    return check_path(path, PathType.FILE, ModeAccess.READ)


@deprecated_str_to_path(0, 'path')
def check_writable_file(path: PurePath, mkdirs: bool=True) -> PurePath:
    """
    If `path` exists, check that it is writable, otherwise check that its parent
    directory exists and is writable.

    Args:
        path: The path to check.
        mkdirs: Whether to create any missing directories (True).

    Returns:
        The fully resolved path.
    """
    if check_std(path):
        return check_path(path, PathType.FILE, Permission.WRITE)
    else:
        path = as_path(path)
        if path.exists():
            return check_path(path, PathType.FILE, Permission.WRITE)
        path = cast(Path, abspath(path))
        dirpath = path.parent
        if dirpath.exists():
            check_path(dirpath, PathType.DIR, Permission.WRITE)
        else:
            if mkdirs:
                dirpath.mkdir(parents=True)
        return path


@deprecated_str_to_path(0, 'path')
def safe_check_path(path: PurePath, *args, **kwargs) -> Optional[PurePath]:
    """
    Safe vesion of `check_path`. Returns None rather than throw an exception.
    """
    try:
        return check_path(path, *args, **kwargs)
    except IOError:
        return


@deprecated_str_to_path(0, 'path')
def safe_check_readable_file(path: PurePath) -> Optional[PurePath]:
    """
    Safe vesion of `check_readable_file`. Returns None rather than throw an exception.
    """
    try:
        return check_readable_file(path)
    except IOError:
        return


@deprecated_str_to_path(0, 'path')
def safe_check_writable_file(path: PurePath) -> Optional[PurePath]:
    """Safe vesion of `check_writable_file`. Returns None rather than throw
    an exception.
    """
    try:
        return check_writable_file(path)
    except IOError:
        return


@overload
def find(root: PurePath, pattern: Regexp, return_matches: True, **kwargs) -> Sequence[Tuple[(PurePath, Match)]]:
    pass


@overload
def find(root: PurePath, pattern: Regexp, return_matches: False, **kwargs) -> Sequence[PurePath]:
    pass


@deprecated_str_to_path(0, 'root')
def find(root: PurePath, pattern: Regexp, path_types: Sequence[PathTypeArg]='f', recursive: bool=True, return_matches: bool=False) -> Union[(Sequence[PurePath], Sequence[Tuple[(PurePath, Match)]])]:
    """Find all paths under `root` that match `pattern`.

    Args:
        root: Directory at which to start search.
        pattern: File name pattern to match (string or re object).
        path_types: Types to return -- files ('f'), directories ('d' or
            both ('fd').
        recursive: Whether to search directories recursively.
        return_matches: Whether to return regular expression match for each
            file.

    Returns:
        List of matching paths. If `return_matches` is True, each item will be
        a (path, Match) tuple.
    """
    if isinstance(pattern, str):
        pat = re.compile(pattern)
    else:
        pat = cast(Pattern, pattern)
    path_type_set = {PathType(p) if isinstance(p, str) else p for p in path_types}
    fullmatch = os.sep in pat.pattern

    def get_matching(names, _parent):
        """Get all names that match the pattern."""
        _parent = as_pure_path(_parent)
        if fullmatch:
            names = (_parent / name for name in names)
        matching = []
        for name in names:
            match = pat.fullmatch(str(name))
            if match:
                path = Path(name) if fullmatch else _parent / name
                matching.append((path, match))

        return matching

    found = []
    for parent, dirs, files in os.walk(root):
        if PathType.DIR in path_type_set:
            found.extend(get_matching(dirs, parent))
        if any(t in path_type_set for t in (PathType.FILE, PathType.FIFO)):
            matching_files = get_matching(files, parent)
            if PathType.FILE not in path_type_set:
                found.extend(f for f in matching_files if stat.S_ISFIFO(f[0].stat().st_mode))
            else:
                found.extend(matching_files)
            if not recursive:
                break

    if return_matches:
        return tuple(found)
    else:
        return tuple(f[0] for f in found)


DEFAULT_EXEC_PATH = tuple(Path(path) for path in os.get_exec_path())

class ExecutableCache(object):
    __doc__ = 'Lookup and cache executable paths.\n\n    Args:\n        default_path: The default executable path\n    '

    def __init__(self, default_path: Optional[Iterable[PurePath]]=None) -> None:
        self.cache = {}
        self.search_path = None
        self.reset_search_path(default_path)

    def add_search_path(self, paths: Union[(str, PurePath, Iterable[PurePath])]) -> None:
        """Add directories to the beginning of the executable search path.

        Args:
            paths: List of paths, or a string with directories separated by
                `os.pathsep`.
        """

        def _as_path(p):
            check_std(p, error=True)
            s = str(p)
            if '"' in s:
                p = s.strip('"')
            return as_path(p)

        if isinstance(paths, str):
            paths = tuple(_as_path(path) for path in paths.split(os.pathsep))
        else:
            if isinstance(paths, PurePath):
                paths = (
                 paths,)
            else:
                paths = tuple(paths)
        self.search_path = paths + self.search_path

    @deprecated_str_to_path(list_args=(0, 'default_path'))
    def reset_search_path(self, default_path: Iterable[PurePath]=None) -> None:
        """Reset the search path to `default_path`.

        Args:
            default_path: The default executable path.
        """
        if default_path is None:
            default_path = DEFAULT_EXEC_PATH
        self.search_path = ()
        if default_path:
            self.add_search_path(default_path)

    def get_path(self, executable: Union[(str, PurePath)]) -> Path:
        """Get the full path of `executable`.

        Args:
            executable: A executable name or path.

        Returns:
            The full path of `executable`, or None if the path cannot be
            found.
        """
        if executable in self.cache:
            return self.cache[executable]
        else:
            if isinstance(executable, str):
                if executable in (STDIN_OR_STDOUT_STR, STDERR_STR):
                    raise ValueError(f"Invalid executable: {executable}")
                else:
                    check_std(executable, error=True)
                exe_file = safe_check_path(Path(executable), PathType.FILE, Permission.EXECUTE)
                if not exe_file:
                    for path in self.search_path:
                        exe_file = safe_check_path(path / executable, PathType.FILE, Permission.EXECUTE)
                        if exe_file:
                            break

            else:
                exe_name = executable
                if exe_file:
                    exe_file = cast(Path, exe_file)
                    exe_name = exe_file.name
                    if exe_name not in self.cache:
                        self.cache[exe_name] = exe_file
            self.cache[exe_name] = exe_file
            return exe_file

    def resolve_exe(self, names: Iterable[str]) -> Optional[Tuple[(Path, str)]]:
        """Given an iterable of command names, find the first that resolves to
        an executable.

        Args:
            names: An iterable of command names.

        Returns:
            A tuple (path, name) of the first command to resolve, or None if
            none of the commands resolve.
        """
        for cmd in names:
            exe = self.get_path(cmd)
            if exe:
                return (
                 exe, cmd)


EXECUTABLE_CACHE = ExecutableCache(default_path=DEFAULT_EXEC_PATH)

class TempPath(metaclass=ABCMeta):
    __doc__ = "Base class for temporary files/directories.\n\n    Args:\n        parent: The parent directory.\n        permissions: The access permissions.\n        path_type: 'f' = file, 'd' = directory.\n    "

    @deprecated_str_to_path(1, 'parent')
    def __init__(self, parent: Union[(Path, 'TempPath')]=None, permissions: Optional[PermissionSetArg]='rwx', path_type: PathTypeArg='d', root: Optional['TempPathManager']=None) -> None:
        if isinstance(parent, Path):
            if root:
                parent = root[parent]
            else:
                raise ValueError(f"Cannot resolve {parent} without 'root'.")
        else:
            self.parent = parent
            if isinstance(path_type, str):
                path_type = PathType(path_type)
            self.path_type = path_type
            self._permissions = None
            if permissions:
                self._set_permissions_value(permissions)

    @property
    @abstractmethod
    def absolute_path(self) -> Path:
        """The absolute path.
        """
        pass

    @property
    @abstractmethod
    def relative_path(self) -> Path:
        """The relative path.
        """
        pass

    @property
    def exists(self) -> bool:
        """Whether the directory exists.
        """
        return self.absolute_path.exists()

    @property
    def permissions(self) -> PermissionSet:
        """The permissions of the path. Defaults to the parent's mode.
        """
        if not self._permissions:
            if self.parent:
                self._permissions = self.parent.permissions
            else:
                raise IOError("Cannot determine permissions without 'parent'")
        return self._permissions

    def set_permissions(self, permissions: Optional[PermissionSetArg]=None, set_parent: bool=False, additive: bool=False) -> Optional[PermissionSet]:
        """Set the permissions for the path.

        Args:
            permissions: The new flags to set. If None, the existing flags are
                used.
            set_parent: Whether to recursively set the permissions of all
                parents. This is done additively.
            additive: Whether permissions should be additive (e.g.
                if `permissions == 'w'` and `self.permissions == 'r'`, the new
                mode is 'rw').

        Returns:
            The PermissionSet representing the flags that were set.
        """
        if not self.exists:
            return
        else:
            if permissions:
                permissions = self._set_permissions_value(permissions, additive)
            else:
                permissions = self.permissions
            if set_parent:
                if self.parent:
                    self.parent.set_permissions(permissions, True, True)
            if self.path_type == PathType.DIR:
                if Permission.EXECUTE not in permissions:
                    permissions.add(Permission.EXECUTE)
            set_permissions(self.absolute_path, permissions)
            return permissions

    def _set_permissions_value(self, permissions: PermissionSetArg, additive: bool=False) -> PermissionSet:
        if not isinstance(permissions, PermissionSet):
            permissions = PermissionSet(permissions)
        elif additive and (self._permissions or self.parent):
            self.permissions.update(permissions)
        else:
            self._permissions = permissions
        return permissions


class TempPathDescriptor(TempPath):
    __doc__ = "Describes a temporary file or directory within a TempDir.\n\n    Args:\n        name: The file/directory name.\n        parent: The parent directory, a TempPathDescriptor.\n        permissions: The permissions mode.\n        suffix, prefix: The suffix and prefix to use when calling\n            `mkstemp` or `mkdtemp`.\n        path_type: 'f' (for file), 'd' (for directory), or '|' (for FIFO).\n    "

    @deprecated_str_to_path(2, 'parent')
    def __init__(self, name=None, parent=None, permissions=None, suffix='', prefix='', contents='', path_type='f', root=None):
        if isinstance(path_type, str):
            path_type = PathType(path_type)
        if contents:
            if path_type != PathType.FILE:
                raise ValueError("'contents' only valid for files")
        super().__init__(parent, permissions, path_type, root=root)
        self.name = name
        self.prefix = prefix
        self.suffix = suffix
        self.contents = contents
        self._abspath = None
        self._relpath = None

    @property
    def absolute_path(self) -> Path:
        """The absolute path.
        """
        if self._abspath is None:
            self._init_path()
        return self._abspath

    @property
    def relative_path(self) -> Path:
        """The relative path.
        """
        if self._relpath is None:
            self._init_path()
        return self._relpath

    def _init_path(self) -> None:
        if self.parent is None:
            raise IOError("Cannot determine absolute path without 'root'")
        self._relpath = self.parent.relative_path / self.name
        self._abspath = self.parent.absolute_path / self.name

    def create(self, apply_permissions: bool=True) -> None:
        """Create the file/directory.

        Args:
            apply_permissions: Whether to set permissions according to
                `self.permissions`.
        """
        if self.path_type != PathType.DIR:
            if self.path_type == PathType.FIFO:
                if self.absolute_path.exists():
                    self.absolute_path.unlink()
                os.mkfifo(str(self.absolute_path))
            if self.path_type != PathType.FIFO:
                with open(self.absolute_path, 'wt') as (outfile):
                    outfile.write(self.contents or '')
        else:
            if not os.path.exists(self.absolute_path):
                self.absolute_path.mkdir()
        if apply_permissions:
            self.set_permissions()

    def __str__(self):
        return f"TempPathDescriptor({self.name}, {self.path_type})"


class TempPathManager:
    __doc__ = 'Base for classes that manage mapping between paths and\n    TempPathDescriptors.\n    '

    def __init__(self) -> None:
        self.paths = {}

    @deprecated_str_to_path(1, 'path')
    def __getitem__(self, path: Path) -> TempPathDescriptor:
        return self.paths[path]

    def __setitem__(self, path: Path, desc: TempPathDescriptor):
        self.paths[path] = desc

    def __contains__(self, path: Path) -> bool:
        return path in self.paths

    def __iter__(self):
        yield from self.paths.values()
        if False:
            yield None

    def clear(self):
        self.paths.clear()


class TempDir(TempPathManager, TempPath):
    __doc__ = 'Context manager that creates a temporary directory and cleans it up\n    upon exit.\n\n    Args:\n        mode: Access mode to set on temp directory. All subdirectories and\n            files will inherit this mode unless explicity set to be different.\n        path_descriptors: Iterable of TempPathDescriptors.\n        kwargs: Additional arguments passed to tempfile.mkdtemp.\n\n    By default all subdirectories and files inherit the mode of the temporary\n    directory. If TempPathDescriptors are specified, the paths are created\n    before permissions are set, enabling creation of a read-only temporary file\n    system.\n    '

    def __init__(self, permissions: Optional[PermissionSetArg]='rwx', path_descriptors: Iterable[TempPathDescriptor]=None, **kwargs) -> None:
        TempPathManager.__init__(self)
        TempPath.__init__(self, permissions=permissions)
        self._absolute_path = as_path(abspath(Path((tempfile.mkdtemp)(**kwargs))))
        self._relative_path = Path('')
        if path_descriptors:
            (self.make_paths)(*path_descriptors)
        self.set_permissions()

    @property
    def absolute_path(self) -> Path:
        return self._absolute_path

    @property
    def relative_path(self) -> Path:
        return self._relative_path

    def __enter__(self) -> 'TempDir':
        return self

    def __exit__(self, exception_type, exception_value, traceback) -> None:
        self.close()

    def close(self) -> None:
        """Delete the temporary directory and all files/subdirectories within.
        """
        if not self.exists:
            return
        for path in iter(self):
            path.set_permissions('rwx', True)

        shutil.rmtree(str(self.absolute_path))
        self.clear()

    def make_path(self, desc: TempPathDescriptor=None, apply_permissions: bool=True, **kwargs) -> Path:
        """Create a file or directory within the TempDir.

        Args:
            desc: A TempPathDescriptor.
            apply_permissions: Whether permissions should be applied to
                the new file/directory.
            kwargs: Arguments to TempPathDescriptor. Ignored unless `desc`
                is None.

        Returns:
            The absolute path to the new file/directory.
        """
        if not desc:
            desc = TempPathDescriptor(root=self, **kwargs)
        else:
            if desc.parent:
                desc.parent = self[desc.parent.absolute_path]
            else:
                desc.parent = self
            if not desc.name:
                parent = desc.parent.absolute_path
                if desc.path_type == PathType.DIR:
                    path = tempfile.mkdtemp(prefix=(desc.prefix),
                      suffix=(desc.suffix),
                      dir=(str(parent)))
                    desc.name = os.path.basename(path)
                else:
                    path = tempfile.mkstemp(prefix=(desc.prefix),
                      suffix=(desc.suffix),
                      dir=(str(parent)))[1]
                    desc.name = os.path.basename(path)
        desc.create(apply_permissions)
        self[desc.absolute_path] = desc
        self[desc.relative_path] = desc
        return desc.absolute_path

    def make_paths(self, *path_descriptors: TempPathDescriptor) -> Sequence[Path]:
        """Create multiple files/directories at once. The paths are created
        before permissions are set, enabling creation of a read-only temporary
        file system.

        Args:
            path_descriptors: One or more TempPathDescriptor.

        Returns:
            A list of the created paths.
        """
        paths = [self.make_path(desc, apply_permissions=False) for desc in path_descriptors]
        for desc in path_descriptors:
            desc.set_permissions()

        return paths

    def make_file(self, desc: TempPathDescriptor=None, apply_permissions: bool=True, **kwargs) -> Path:
        """Convenience method; calls `make_path` with path_type='f'.
        """
        kwargs['path_type'] = 'f'
        return (self.make_path)(desc, apply_permissions, **kwargs)

    def make_fifo(self, desc: TempPathDescriptor=None, apply_permissions: bool=True, **kwargs) -> Path:
        """Convenience method; calls `make_path` with path_type='|'.
        """
        kwargs['path_type'] = '|'
        return (self.make_path)(desc, apply_permissions, **kwargs)

    def make_directory(self, desc: TempPathDescriptor=None, apply_permissions: bool=True, **kwargs) -> Path:
        """Convenience method; calls `make_path` with `path_type='d'`.
        """
        kwargs['path_type'] = 'd'
        return (self.make_path)(desc, apply_permissions, **kwargs)

    def make_empty_files(self, num_files: int, **kwargs) -> Sequence[Path]:
        """Create randomly-named undefined files.

        Args:
            num_files: The number of files to create.
            kwargs: Arguments to pass to TempPathDescriptor.

        Returns:
            A sequence of paths.
        """
        desc = list(TempPathDescriptor(root=self, **kwargs) for _ in range(num_files))
        return (self.make_paths)(*desc)


PATH_CLASS = WindowsPath if os.name == 'nt' else PosixPath

class PathInst(PATH_CLASS):
    __doc__ = 'A path-like that has a slot for variable values.\n    '
    __slots__ = 'values'

    def joinpath(self, *other):
        """Join two path-like objects, including merging 'values' dicts.
        """
        new_path = (super().joinpath)(*other)
        new_values = dict(self.values)
        for oth in other:
            if isinstance(oth, PathInst):
                new_values.update(oth.values)

        return path_inst(new_path, new_values)

    def __getitem__(self, name: str) -> Any:
        return self.values[name]

    def __eq__(self, other):
        return isinstance(other, PathInst) and super().__eq__(other) and self.values == other.values


def path_inst(path: Union[(str, PurePath)], values: dict=None) -> PathInst:
    """Create a PathInst from a path and values dict.

    Args:
        path: The path.
        values: The values dict.

    Returns:
        A PathInst.
    """
    pathinst = PathInst(path)
    pathinst.values = values or {}
    return pathinst


T = TypeVar('T')

class PathVar(Generic[T]):
    __doc__ = 'Describes part of a path, used in PathSpec.\n\n    Args:\n        name: Path variable name\n        optional: Whether this part of the path is optional\n        default: A default value for this path variable\n        undefined: The value to use when the variable is undefined\n        pattern: A pattern that the value must match\n        valid: Iterable of valid values\n        invalid: Iterable of invalid values\n\n    If `valid` is specified, `invalid` and `pattern` are ignored. Otherwise,\n    values are first checked against `pattern` (if one is specified), then\n    checked against `invalid` (if specified).\n    '

    def __init__(self, name: str, optional: bool=False, default: Optional[T]=None, undefined: T=None, pattern: Regexp=None, valid: Iterable[T]=None, invalid: Iterable[T]=None, datatype: Callable[([str], T)]=None) -> None:
        self.name = name
        self.optional = optional
        self.default = default
        self.undefined = undefined
        self.valid = self.invalid = self.pattern = None
        if pattern:
            if isinstance(pattern, str):
                self.pattern = re.compile(pattern)
        else:
            self.pattern = cast(Pattern, pattern)
        if valid:
            self.valid = set(valid)
        else:
            if invalid:
                self.invalid = set(invalid)
        self.datatype = datatype

    def __call__(self, value: str=None) -> T:
        """Validate a value.

        Args:
            The value to validate. If None, the default value is used.

        Raises:
            ValueError if any validations fail.
        """
        if value is None:
            if self.default:
                value = self.default
            else:
                if self.optional:
                    return self.undefined
                raise ValueError(f"{self.name} is required")
        if self.valid:
            if value not in self.valid:
                raise ValueError(f"{value} is not in list of valid values")
        else:
            if self.pattern:
                if not self.pattern.fullmatch(str(value)):
                    raise ValueError(f"{value} does not match pattern {self.pattern}")
        if self.invalid:
            if value in self.invalid:
                raise ValueError(f"{value} is in list of invalid values")
        if self.datatype:
            return self.datatype(value)
        else:
            return value

    def as_pattern(self) -> str:
        """Format this variable as a regular expression capture group.
        """
        pattern = self.pattern.pattern if self.pattern else '.*'
        return '(?P<{name}>{pattern}){optional}'.format(name=(self.name),
          pattern=pattern,
          optional=('?' if self.optional else ''))

    def __str__(self) -> str:
        return 'PathVar<{}, optional={}, default={}>'.format(self.name, self.optional, self.default)


class StrPathVar(PathVar[str]):

    def __init__(self, name, undefined='', **kwargs):
        (super().__init__)(name, undefined=undefined, **kwargs)


class PathPathVar(PathVar[Path]):

    def __init__(self, name, undefined=Path(''), datatype=Path, **kwargs):
        (super().__init__)(name, undefined=undefined, datatype=datatype, **kwargs)


def match_to_dict(match: Match, path_vars: Dict[(str, PathVar)], errors: bool=True) -> Optional[Dict[(str, Any)]]:
    """Convert a regular expression Match to a dict of (name, value) for
    all PathVars.

    Args:
        match: A re.Match.
        path_vars: A dict of PathVars.
        errors: If True, raise an exception on validation error, otherwise
            return None.

    Returns:
        A (name, value) dict.

    Raises:
        ValueError if any values fail validation.
    """
    match_groups = match.groupdict()
    try:
        return dict((name, var(match_groups.get(name, None))) for name, var in path_vars.items())
    except ValueError:
        if errors:
            raise
        else:
            return


class SpecBase(metaclass=ABCMeta):
    __doc__ = 'Base class for :class:`DirSpec` and :class:`FileSpec`.\n\n    Args:\n        path_vars: Named variables with which to associate parts of a path.\n        template: Format string for creating paths from variables.\n        pattern: Regular expression for identifying matching paths.\n    '

    def __init__(self, *path_vars: PathVar, template: str=None, pattern: Regexp=None) -> None:
        self.path_vars = dict((v.name, v) for v in path_vars)
        if template is None:
            template = '{{{}}}'.format(self.default_var_name)
            self.path_vars[self.default_var_name] = PathVar((self.default_var_name),
              pattern=(self.default_pattern))
        self.template = template

        def escape(strng: str, chars: Iterable[str]):
            """Escape special characters in a string.
            """
            for char in chars:
                strng = strng.replace(char, f"\\{char}")

            return strng

        def template_to_pattern(_template):
            """Convert a template string to a regular expression.
            """
            _pattern = escape(_template, ('\\', '.', '*', '+', '?', '[', ']', '(',
                                          ')', '<', '>'))
            _pattern += '$'
            pattern_args = dict((name, var.as_pattern()) for name, var in self.path_vars.items())
            _pattern = (_pattern.format)(**pattern_args)
            return escape(_pattern, ('{', '}'))

        if pattern is None:
            pattern = template_to_pattern(template)
        if isinstance(pattern, str):
            pattern = re.compile(pattern)
        self.pattern = pattern

    @property
    @abstractmethod
    def default_var_name(self) -> str:
        """The default variable name used for string formatting.
        """
        pass

    @property
    @abstractmethod
    def default_pattern(self) -> str:
        """The default filename pattern.
        """
        pass

    @property
    @abstractmethod
    def path_type(self) -> PathType:
        """The PathType.
        """
        pass

    def construct(self, **kwargs) -> PathInst:
        """Create a new PathInst from this spec using values in `kwargs`.

        Args:
            kwargs: Specify values for path variables.

        Returns:
            A PathInst.
        """
        values = dict((name, var(kwargs.get(name, None))) for name, var in self.path_vars.items())
        path = (self.template.format)(**values)
        return path_inst(as_pure_path(path), values)

    def __call__(self, **kwargs) -> PathInst:
        return (self.construct)(**kwargs)

    def parse(self, path: Union[(str, PurePath)], fullpath: bool=False) -> PathInst:
        """Extract PathVar values from `path` and create a new PathInst.

        Args:
            path: The path to parse.
            fullpath: Whether to extract the fully-resolved path.

        Returns: a PathInst.
        """
        if isinstance(path, str):
            if path in {STDIN_OR_STDOUT, STDERR}:
                raise ValueError(f"Cannot parse {path}")
            else:
                check_std(path, error=True)
        else:
            path = as_path(path)
            if fullpath:
                path = self.path_part(path.expanduser())
            match = self.pattern.fullmatch(str(path))
            raise match or ValueError(f"{path} does not match {self}")
        return path_inst(path, self._match_to_dict(match))

    def _match_to_dict(self, match: Match, errors: bool=True) -> Dict[(str, Any)]:
        """Convert a regular expression Match to a dict of (name, value) for
        all PathVars.

        Args:
            match: A :class:`re.Match`.
            errors: If True, raise an exception for validation failure,
                otherwise return None.

        Returns:
            A (name, value) dict.

        Raises:
            ValueError if any values fail validation.
        """
        return match_to_dict(match, self.path_vars, errors)

    def find(self, root: Optional[PurePath]=None, recursive: bool=False) -> Sequence[PathInst]:
        """Find all paths in `root` matching this spec.

        Args:
            root: Directory in which to begin the search.
            recursive: Whether to search recursively.

        Returns:
            A sequence of PathInst.
        """
        if root is None:
            root = self.default_search_root()
        find_results = find(root,
          (self.pattern),
          path_types=[
         self.path_type],
          recursive=recursive,
          return_matches=True)
        matches = dict((path, self._match_to_dict(match, errors=False)) for path, match in cast(Sequence[Tuple[(str, Match[str])]], find_results))
        return [path_inst(path, match) for path, match in matches.items() if match is not None]

    def __str__(self) -> str:
        return '{}<{}, template={}, pattern={}>'.format(self.__class__.__name__, ','.join(str(var) for var in self.path_vars.values()), self.template, self.pattern)

    @abstractmethod
    def path_part(self, path: Path) -> str:
        """Return the part of the absolute path corresponding to the spec type.
        """
        pass

    def default_search_root(self) -> PurePath:
        """Get the default root directory for searcing.
        """
        raise ValueError("'root' must be specified for FileSpec.find()")


class DirSpec(SpecBase):
    __doc__ = 'Spec for the directory part of a path.\n    '

    @property
    def default_var_name(self) -> str:
        return 'dir'

    @property
    def default_pattern(self) -> str:
        return '.*'

    @property
    def path_type(self) -> PathType:
        return PathType.DIR

    def path_part(self, path: Path) -> str:
        return path.parent

    def default_search_root(self) -> PurePath:
        try:
            idx1 = self.template.index('{')
        except ValueError:
            return Path(self.template)
        else:
            try:
                idx2 = self.template.rindex(os.sep, 0, idx1)
                return Path(self.template[0:idx2])
            except ValueError:
                return Path(get_root())


class FileSpec(SpecBase):
    __doc__ = "Spec for the filename part of a path.\n\n    Examples:\n        spec = FileSpec(\n            PathVar('id', pattern='[A-Z0-9_]+'),\n            PathVar('ext', pattern=r'[^.]+'),\n            template='{id}.{ext}'\n        )\n\n        # get a single file\n        path = spec(id='ABC123', ext='txt') # => PathInst('ABC123.txt')\n        print(path['id']) # => 'ABC123'\n\n        # get the variable values for a path\n        path = spec.parse('ABC123.txt')\n        print(path['id']) # => 'ABC123'\n\n        # find all files that match a FileSpec in the user's home directory\n        all_paths = spec.find('~') # => [PathInst...]\n    "

    @property
    def default_var_name(self) -> str:
        return 'file'

    @property
    def default_pattern(self) -> str:
        return '[^{}]*'.format(os.sep)

    @property
    def path_type(self) -> PathType:
        return PathType.FILE

    def path_part(self, path: Path) -> str:
        return path.name


class PathSpec:
    __doc__ = 'Specifies a path in terms of a template with named components ("path\n    variables").\n\n    Args:\n        dir_spec: A PurePath if the directory is fixed, otherwise a DirSpec.\n        file_spec: A string if the filename is fixed, otherwise a FileSpec.\n    '

    def __init__(self, dir_spec: Union[(PurePath, DirSpec)], file_spec: Union[(str, FileSpec)]) -> None:
        self.fixed_dir = self.fixed_file = False
        if not isinstance(dir_spec, DirSpec):
            dir_spec = path_inst(dir_spec)
            self.fixed_dir = True
        if not isinstance(file_spec, FileSpec):
            file_spec = path_inst(file_spec)
            self.fixed_file = True
        self.dir_spec = dir_spec
        self.file_spec = file_spec
        if self.fixed_dir:
            dir_spec_str = str(dir_spec)
        else:
            dir_spec_str = dir_spec.pattern.pattern
        if dir_spec_str.endswith('$'):
            dir_spec_str = dir_spec_str[:-1]
        self.pattern = os.path.join(dir_spec_str, file_spec if self.fixed_file else file_spec.pattern.pattern)
        self.path_vars = {}
        if not self.fixed_dir:
            self.path_vars.update(self.dir_spec.path_vars)
        if not self.fixed_file:
            self.path_vars.update(self.file_spec.path_vars)

    def construct(self, **kwargs) -> PathInst:
        """Create a new PathInst from this PathSpec using values in `kwargs`.

        Args:
            kwargs: Specify values for path variables.

        Returns:
            A PathInst
        """
        if self.fixed_dir:
            dir_part = cast(PathInst, self.dir_spec)
        else:
            dir_part = (self.dir_spec.construct)(**kwargs)
        if self.fixed_file:
            file_part = cast(PathInst, self.file_spec)
        else:
            file_part = (self.file_spec.construct)(**kwargs)
        return dir_part.joinpath(file_part)

    def __call__(self, **kwargs) -> PathInst:
        return (self.construct)(**kwargs)

    def parse(self, path: PurePath) -> PathInst:
        """Extract PathVar values from `path` and create a new PathInst.

        Args:
            path: The path to parse

        Returns: a PathInst
        """

        def parse_part(part, spec, fixed):
            """Parse part of path using 'spec'. Returns 'spec' if fixed is True.
            """
            if fixed:
                inst = spec
                if str(inst) != str(part):
                    raise ValueError(f"{part} doesn't match {spec}")
            else:
                inst = spec.parse(part)
            return inst

        dir_part = path.parent
        file_part = path.name
        dir_inst = file_inst = None
        if dir_part:
            dir_inst = parse_part(dir_part, self.dir_spec, self.fixed_dir)
        if file_part:
            file_inst = parse_part(file_part, self.file_spec, self.fixed_file)
        if dir_inst:
            return dir_inst.joinpath(file_inst)
        else:
            return file_inst

    @deprecated_str_to_path(1, 'root')
    def find(self, root: Optional[PurePath]=None, path_types: Sequence[PathTypeArg]='f', recursive: bool=False) -> Sequence[PathInst]:
        """Find all paths matching this PathSpec. The search starts in 'root'
        if it is not None, otherwise it starts in the deepest fixed directory
        of this PathSpec's DirSpec.

        Args:
            root: Directory in which to begin the search.
            path_types: Types to return -- files ('f'), directories ('d') or
                both ('fd').
            recursive: Whether to search recursively.

        Returns:
            A sequence of PathInst.
        """
        if root is None:
            if self.fixed_dir:
                root = self.dir_spec
            else:
                root = self.dir_spec.default_search_root()
        files = find(root,
          (self.pattern),
          path_types=path_types,
          recursive=recursive,
          return_matches=True)
        return [path_inst(path, match_to_dict(match, self.path_vars)) for path, match in cast(Sequence[Tuple[(PurePath, Match[str])]], files)]