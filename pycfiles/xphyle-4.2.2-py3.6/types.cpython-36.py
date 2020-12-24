# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/xphyle/types.py
# Compiled at: 2019-12-13 16:21:40
# Size of source mod 2**32: 14891 bytes
"""Type checking support. Defines commonly used types.
"""
from abc import ABCMeta, abstractmethod
import collections
from enum import Enum
from io import IOBase, UnsupportedOperation
import os
from pathlib import PurePath
import stat
from typing import Dict, Sequence, List, Tuple, Set, Iterator, Iterable, Text, Union, Any, IO, Pattern, TypeVar, cast

class ModeAccess(Enum):
    __doc__ = 'Enumeration of the access modes allowed when opening files.\n\n    See Also:\n        https://docs.python.org/3/library/functions.html#open\n    '
    READ = 'r'
    WRITE = 'w'
    READWRITE = 'r+'
    TRUNCATE_READWRITE = 'w+'
    APPEND = 'a'
    EXCLUSIVE = 'x'

    @property
    def readable(self):
        """Whether this is readable mode.
        """
        return any(char in self.value for char in ('r', '+'))

    @property
    def writable(self):
        """Whether this is writable mode.
        """
        return any(char in self.value for char in ('w', '+', 'a', 'x'))


ModeAccessArg = Union[(str, ModeAccess)]

class ModeCoding(Enum):
    __doc__ = 'Enumeration of file open modes (text or binary).\n\n    See Also:\n        https://docs.python.org/3/library/functions.html#open\n    '
    TEXT = 't'
    BINARY = 'b'


ModeCodingArg = Union[(str, ModeCoding)]
FILE_MODE_CACHE = {}
FILE_MODE_CACHE: Dict[(Tuple[(str, ModeAccessArg, ModeCodingArg)], 'FileMode')]

class FileMode(object):
    __doc__ = 'Definition of a file mode as composed of a :class:`ModeAccess` and a\n    :class:`ModeCoding`.\n\n    Args:\n        mode: Specify the mode as a string; mutually exclusive with `access`\n            and `coding`.\n        access: The file access mode (default: :attribute:`ModeAccess.READ`).\n        coding: The file open mode (default: :attribute:`ModeCoding.TEXT`).\n    '

    def __new__(cls, mode=None, access=None, coding=None):
        key = (
         mode, access, coding)
        if key not in FILE_MODE_CACHE:
            FILE_MODE_CACHE[key] = super().__new__(cls)
        return FILE_MODE_CACHE[key]

    def __init__(self, mode: str=None, access: ModeAccessArg=None, coding: ModeCodingArg=None) -> None:
        if mode:
            access_val = None
            for a in ModeAccess:
                if a.value in mode:
                    access_val = a
                    break

            coding_val = None
            for e in ModeCoding:
                if e.value in mode:
                    coding_val = e
                    break

        else:
            if isinstance(access, str):
                access_val = ModeAccess(access)
            else:
                access_val = cast(ModeAccess, access)
            if isinstance(coding, str):
                coding_val = ModeCoding(coding)
            else:
                coding_val = cast(ModeCoding, coding)
        self.access = access_val or ModeAccess.READ
        self.coding = coding_val or ModeCoding.TEXT
        self.value = '{}{}'.format(self.access.value, self.coding.value)
        if mode:
            diff = set(mode) - set(str(self) + 'U')
            if diff:
                raise ValueError('Invalid characters in mode string: {}'.format(''.join(diff)))

    @property
    def readable(self):
        """Whether this is readable mode.
        """
        return self.access.readable

    @property
    def writable(self):
        """Whether this is writable mode.
        """
        return self.access.writable

    @property
    def binary(self):
        """Whether this is binary mode.
        """
        return self.coding == ModeCoding.BINARY

    @property
    def text(self):
        """Whether this is text mode.
        """
        return self.coding == ModeCoding.TEXT

    def __contains__(self, value: Union[(str, ModeAccess, ModeCoding)]) -> bool:
        if isinstance(value, ModeAccess):
            return self.access == value
        else:
            if isinstance(value, ModeCoding):
                return self.coding == value
            for v in cast(str, value):
                if v not in self.access.value:
                    if v not in self.coding.value:
                        return False

            return True

    def __eq__(self, other):
        return isinstance(other, FileMode) and self.access == other.access and self.coding == other.coding

    def __repr__(self):
        return self.value


OS_ALIASES = dict(r=(os.R_OK), w=(os.W_OK), x=(os.X_OK), t=0)
STAT_ALIASES = dict(r=(stat.S_IREAD),
  w=(stat.S_IWRITE),
  x=(stat.S_IEXEC),
  t=(stat.S_ISVTX),
  f=(stat.S_IFREG),
  d=(stat.S_IFDIR),
  fifo=(stat.S_IFIFO))

class Permission(Enum):
    __doc__ = "Enumeration of file permission flags ('r', 'w', 'x', 't'). Note that\n    this isn't a full enumeration of all flags, just those pertaining to the\n    permissions of the current user.\n    "
    READ = 'r'
    WRITE = 'w'
    EXECUTE = 'x'
    STICKY = 't'

    @property
    def stat_flag(self):
        """Returns the :module:`stat` flag.
        """
        return STAT_ALIASES[self.value]

    @property
    def os_flag(self):
        """Returns the :module:`os` flag.
        """
        return OS_ALIASES[self.value]


PermissionArg = Union[(str, int, Permission, ModeAccess)]
PERMISSION_SET_CACHE = {}
PERMISSION_SET_CACHE: Dict[(Union[(PermissionArg, Iterable[PermissionArg])], 'PermissionSet')]

class PermissionSet(object):
    __doc__ = "A set of :class:`Permission`s.\n\n    Args:\n        flags: Sequence of flags as string ('r', 'w', 'x'), int,\n            :class:`ModeAccess`, or :class:`Permission`.\n    "

    def __new__(cls, flags=None):
        if flags not in PERMISSION_SET_CACHE:
            PERMISSION_SET_CACHE[flags] = super().__new__(cls)
        return PERMISSION_SET_CACHE[flags]

    def __init__(self, flags: Union[(PermissionArg, Iterable[PermissionArg])]=None) -> None:
        self.flags = set()
        if flags:
            if isinstance(flags, str) or is_iterable(flags):
                self.update(cast(Iterable[PermissionArg], flags))
            else:
                self.add(cast(Union[(int, Permission, ModeAccess)], flags))

    def add(self, flag: PermissionArg) -> None:
        """Add a permission.

        Args:
            flag: Permission to add.
        """
        if isinstance(flag, str):
            self.flags.add(Permission(flag))
        else:
            if isinstance(flag, int):
                for f in Permission:
                    if f.stat_flag & flag or f.os_flag & flag:
                        self.flags.add(f)

            else:
                if isinstance(flag, ModeAccess):
                    if flag.readable:
                        self.add(Permission.READ)
                    if flag.writable:
                        self.add(Permission.WRITE)
                else:
                    self.flags.add(flag)

    def update(self, flags: Union[('PermissionSet', Iterable[PermissionArg])]) -> None:
        """Add all flags in `flags` to this `PermissionSet`.

        Args:
            flags: Flags to add.
        """
        for flag in flags:
            self.add(flag)

    @property
    def stat_flags(self) -> int:
        """Returns the binary OR of the :module:`stat` flags corresponding to
        the flags in this `PermissionSet`.
        """
        flags = 0
        for f in self.flags:
            flags |= f.stat_flag

        return flags

    @property
    def os_flags(self) -> int:
        """Returns the binary OR of the :module:`os` flags corresponding to
        the flags in this `PermissionSet`.
        """
        flags = 0
        for f in self.flags:
            flags |= f.os_flag

        return flags

    def __iter__(self) -> Iterable[Permission]:
        """Iterate over flags in the same order they appear in
        :class:`Permission`.
        """
        for f in Permission:
            if f in self.flags:
                yield f

    def __eq__(self, other):
        return isinstance(other, PermissionSet) and self.flags == other.flags

    def __contains__(self, access_flag: PermissionArg) -> bool:
        if isinstance(access_flag, str):
            access_flag = Permission(access_flag)
        return access_flag in self.flags

    def __repr__(self) -> str:
        return ''.join(f.value for f in Permission if f in self.flags)


class FileType(Enum):
    __doc__ = 'Enumeration of types of files that can be opened by\n    :method:`xphyle.xopen`.\n    '
    STDIO = 'std'
    LOCAL = 'local'
    URL = 'url'
    PROCESS = 'ps'
    FILELIKE = 'filelike'
    BUFFER = 'buffer'


class EventType(Enum):
    __doc__ = 'Enumeration of event types that can be registered on an\n    :class:`EventManager`.\n    '
    CLOSE = 'close'


AnyChar = Union[(bytes, Text)]

class FileLikeInterface(IO, Iterable[AnyChar], metaclass=ABCMeta):
    __doc__ = 'This is a marker interface for classes that implement methods (listed\n    below) to make them behave like python file objects. Provides a subset of\n    methods from typing.io.IO, plus next() and __iter__.\n\n    See Also:\n        https://docs.python.org/3/tutorial/inputoutput.html#methods-of-file-objects\n    '

    @abstractmethod
    def next(self) -> AnyChar:
        pass


class FileLikeBase(FileLikeInterface):

    def flush(self) -> None:
        pass

    def close(self) -> None:
        pass

    def readable(self) -> bool:
        return False

    def read(self, n: int=-1) -> AnyChar:
        raise UnsupportedOperation()

    def readline(self, hint: int=-1) -> AnyChar:
        raise UnsupportedOperation()

    def readlines(self, sizehint: int=-1) -> List[AnyChar]:
        raise UnsupportedOperation()

    def writable(self) -> bool:
        return False

    def write(self, string: AnyChar) -> int:
        raise UnsupportedOperation()

    def writelines(self, lines: Iterable[AnyChar]) -> None:
        raise UnsupportedOperation()

    def seek(self, offset, whence: int=0) -> int:
        if self.seekable():
            raise UnsupportedOperation()
        else:
            raise ValueError('Cannot call seek on a non-seekable object')

    def seekable(self) -> bool:
        return False

    def tell(self) -> int:
        if self.seekable():
            raise UnsupportedOperation()
        else:
            raise ValueError('Cannot call tell on a non-seekable object')

    def isatty(self) -> bool:
        return False

    def fileno(self) -> int:
        return -1

    def truncate(self, size: int=None) -> int:
        if self.seekable():
            raise UnsupportedOperation()
        else:
            raise ValueError('Cannot call truncate on a non-seekable object')

    def __enter__(self) -> Any:
        return self

    def __exit__(self, exception_type, exception_value, traceback) -> bool:
        self.close()
        return False

    def __iter__(self) -> Iterator[AnyChar]:
        raise UnsupportedOperation()

    def __next__(self) -> AnyChar:
        raise UnsupportedOperation()

    def next(self) -> AnyChar:
        return self.__next__()


class PathType(Enum):
    __doc__ = 'Enumeration of supported path types (file, directory, FIFO).\n    '
    FILE = 'f'
    DIR = 'd'
    FIFO = '|'


FileLike = Union[(IO, IOBase, FileLikeInterface)]
PathLike = Union[(os.PathLike, PurePath)]
PathOrFile = Union[(PathLike, PurePath, FileLike)]
Range = Tuple[(int, int)]
Regexp = Union[(str, Pattern)]
CharMode = TypeVar('CharMode', bytes, Text)
BinMode = b'b'
TextMode = 't'
PermissionSetArg = Union[(PermissionSet, Sequence[PermissionArg])]
ModeArg = Union[(str, FileMode)]
PathTypeArg = Union[(str, PathType)]
EventTypeArg = Union[(str, EventType)]
CompressionArg = Union[(bool, str)]

def is_iterable(obj: Any, include_str: bool=False) -> bool:
    """Test whether an object is iterable.

    Args:
        obj: The object to test.
        include_str: Whether a string should be considered an iterable
            (default: False).

    Returns:
        True if the object is iterable.
    """
    return isinstance(obj, collections.abc.Iterable) and (include_str or not isinstance(obj, str))