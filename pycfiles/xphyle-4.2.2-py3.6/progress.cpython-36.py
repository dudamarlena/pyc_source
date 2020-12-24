# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/xphyle/progress.py
# Compiled at: 2019-11-20 14:25:37
# Size of source mod 2**32: 6551 bytes
"""Common interface to enable operations to be wrapped in a progress bar.
By default, pokrok is used for python-level operations and pv for system-level
operations.
"""
from os import PathLike
import shlex
from subprocess import Popen, PIPE
from typing import Iterable, Union, Callable, Tuple, Sequence, Optional
from pokrok import progress_iter
from xphyle.paths import EXECUTABLE_CACHE, check_path
from xphyle.types import PathType, Permission, FileLike

class IterableProgress:
    __doc__ = 'Manages the python-level wrapper.\n\n    Args:\n        default_wrapper: Callable (typically a class) that returns a Callable\n            with the signature of ``wrap``.\n    '

    def __init__(self, default_wrapper: Callable=progress_iter) -> None:
        self.enabled = False
        self.wrapper = None
        self.default_wrapper = default_wrapper

    def update(self, enable: Optional[bool]=None, wrapper: Optional[Callable[(..., Iterable)]]=None) -> None:
        """Enable the python progress bar and/or set a new wrapper.

        Args:
            enable: Whether to enable use of a progress wrapper.
            wrapper: A callable that takes three arguments, itr, desc, size,
                and returns an iterable.
        """
        if enable is not None:
            self.enabled = enable
        else:
            if wrapper:
                self.wrapper = wrapper
            elif self.enabled:
                if not self.wrapper:
                    try:
                        self.wrapper = self.default_wrapper()
                    except ImportError as err:
                        raise ValueError('Could not create default python wrapper; valid wrapper must be specified') from err

    def wrap(self, itr: Iterable, desc: Optional[str]=None, size: Optional[int]=None) -> Iterable:
        """Wrap an iterable in a progress bar.

        Args:
            itr: The Iterable to wrap.
            desc: Optional description.
            size: Optional max value of the progress bar.

        Returns:
            The wrapped Iterable.
        """
        if self.enabled:
            return self.wrapper(itr, desc=desc, size=size)
        else:
            return itr


ITERABLE_PROGRESS = IterableProgress()

def system_progress_command(exe: Union[(str, PathLike)], *args, require: bool=False) -> Tuple:
    """Resolve a system-level progress bar command.

    Args:
        exe: The executable name or absolute path.
        args: A list of additional command line arguments.
        require: Whether to raise an exception if the command does not exist.

    Returns:
        A tuple of (executable_path, *args).
    """
    executable_path = EXECUTABLE_CACHE.get_path(exe)
    if executable_path is not None:
        check_path(executable_path, PathType.FILE, Permission.EXECUTE)
    else:
        if require:
            raise IOError('pv is not available on the path')
    return (
     executable_path,) + tuple(args)


def pv_command(require: bool=False) -> Tuple:
    """Default system wrapper command.
    """
    return system_progress_command('pv', '-pre', require=require)


class ProcessProgress:
    __doc__ = 'Manage the system-level progress wrapper.\n\n    Args:\n        default_wrapper: Callable that returns the argument list for the\n            default wrapper command.\n    '

    def __init__(self, default_wrapper: Callable=pv_command) -> None:
        self.enabled = False
        self.wrapper = None
        self.default_wrapper = default_wrapper

    def update(self, enable: Optional[bool]=None, wrapper: Optional[Union[(str, Sequence[str])]]=None) -> None:
        """Enable the python system progress bar and/or set the wrapper
        command.

        Args:
            enable: Whether to enable use of a progress wrapper.
            wrapper: A command string or sequence of command arguments.
        """
        if enable is not None:
            self.enabled = enable
        else:
            if wrapper:
                if isinstance(wrapper, str):
                    self.wrapper = tuple(shlex.split(wrapper))
                else:
                    self.wrapper = wrapper
            elif self.enabled:
                if not self.wrapper:
                    try:
                        self.wrapper = self.default_wrapper()
                    except IOError as err:
                        raise ValueError('Could not create default system wrapper; valid wrapper must be specified') from err

    def wrap(self, cmd: Sequence[str], stdin: FileLike, stdout: FileLike, **kwargs) -> Popen:
        """Pipe a system command through a progress bar program.

        For the process to be wrapped, one of ``stdin``, ``stdout`` must not be
        None.

        Args:
            cmd: Command arguments.
            stdin: File-like object to read into the process stdin, or None to
                use `PIPE`.
            stdout: File-like object to write from the process stdout, or None
                to use `PIPE`.
            kwargs: Additional arguments to pass to Popen.

        Returns:
            Open process.
        """
        if not self.enabled or stdin is None and stdout is None:
            return Popen(cmd, stdin=stdin, stdout=stdout, **kwargs)
        else:
            if stdin is not None:
                proc1 = Popen((self.wrapper), stdin=stdin, stdout=PIPE)
                proc2 = Popen(cmd, stdin=(proc1.stdout), stdout=stdout)
            else:
                proc1 = Popen(cmd, stdout=PIPE)
                proc2 = Popen((self.wrapper), stdin=(proc1.stdout), stdout=stdout)
            proc1.stdout.close()
            return proc2


PROCESS_PROGRESS = ProcessProgress()

def iter_file_chunked(fileobj: FileLike, chunksize: int=1024) -> Iterable:
    """Returns a progress bar-wrapped iterator over a file that reads
    fixed-size chunks.

    Args:
        fileobj: A file-like object.
        chunksize: The maximum size in bytes of each chunk.

    Returns:
        An iterable over the chunks of the file.
    """

    def _itr():
        while True:
            data = fileobj.read(chunksize)
            if data:
                yield data
            else:
                break

    name = None
    if hasattr(fileobj, 'name'):
        name = getattr(fileobj, 'name')
    return ITERABLE_PROGRESS.wrap((_itr()), desc=name)