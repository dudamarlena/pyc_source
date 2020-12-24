# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/xphyle/utils.py
# Compiled at: 2020-01-02 10:11:18
# Size of source mod 2**32: 45338 bytes
"""A collection of convenience methods for reading, writing, and otherwise
managing files. All of these functions are 'safe', meaning that if you pass
``errors=False`` and there is a problem opening the file, the error will be
handled gracefully.
"""
from abc import ABCMeta, abstractmethod
from collections import OrderedDict, Sized
import copy, csv
from itertools import cycle
import os
from pathlib import PurePath, Path
import shutil, sys
from typing import Generator, Callable, Dict, List, Tuple, Any, Sequence, Generic, Iterable, Iterator, Union, Optional, cast
from xphyle import open_, xopen, FileWrapper, Process, popen, EventListener
from xphyle.formats import FORMATS
from xphyle.paths import STDIN, STDOUT, deprecated_str_to_path
from xphyle.progress import iter_file_chunked
from xphyle.types import PathOrFile, FileLike, FileMode, ModeAccessArg, CharMode, TextMode, BinMode, CompressionArg, AnyChar, is_iterable

@deprecated_str_to_path(0, 'path_or_file')
def read_lines(path_or_file: PathOrFile, convert: Optional[Callable[([str], Any)]]=None, strip_linesep: bool=True, **kwargs) -> Generator[(str, None, None)]:
    """Iterate over lines in a file.

    Args:
        path_or_file: Path to the file, or a file-like object.
        convert: Function to call on each line in the file.
        strip_linesep: Whether to strip off trailing line separators.
        kwargs: Additional arguments to pass to :method:`xphyle.open_`.

    Yields:
        Lines of a file, with line endings stripped.
    """
    with open_(path_or_file, **kwargs) as (fileobj):
        if fileobj is None:
            return
        else:
            itr = cast(Iterator[str], fileobj)
            if strip_linesep:
                itr = (line.rstrip() for line in itr)
            if convert:
                itr = (convert(line) for line in itr)
        yield from itr
    if False:
        yield None


@deprecated_str_to_path(0, 'path_or_file')
def read_bytes(path_or_file: PathOrFile, chunksize: int=1024, **kwargs) -> Generator[(bytes, None, None)]:
    """Iterate over a file in chunks. The mode will always be overridden
    to 'rb'.

    Args:
        path_or_file: Path to the file, or a file-like object.
        chunksize: Number of bytes to read at a time.
        kwargs: Additional arguments to pass top :method:`xphyle.open_`.

    Yields:
        Chunks of the input file as bytes. Each chunk except the last should
        be of size `chunksize`.
    """
    kwargs['mode'] = 'rb'
    with open_(path_or_file, **kwargs) as (fileobj):
        if fileobj is None:
            return
        yield from iter_file_chunked(fileobj, chunksize)
    if False:
        yield None


@deprecated_str_to_path(1, 'path_or_file')
def write_lines(iterable: Iterable[str], path_or_file: PathOrFile, linesep: Optional[str]='\n', convert: Callable[([Any], str)]=str, **kwargs) -> int:
    r"""Write delimiter-separated strings to a file.

    Args:
        iterable: An iterable.
        path_or_file: Path to the file, or a file-like object.
        linesep: The delimiter to use to separate the strings, or
            `os.linesep` if None (defaults to '\n').
        convert: Function that converts a value to a string.
        kwargs: Additional arguments to pass top :method:`xphyle.open_`.

    Returns:
        Total number of bytes written, or -1 if `errors=False` and there was
        a problem opening the file.
    """
    if linesep is None:
        linesep = os.linesep
    if 'mode' not in kwargs:
        kwargs['mode'] = 'wt'
    written = 0
    with open_(path_or_file, **kwargs) as (fileobj):
        if fileobj is None:
            return -1
        for line in iterable:
            if written > 0:
                written += fileobj.write(linesep)
            written += fileobj.write(convert(line))

    return written


def to_bytes(value: Any, encoding: str='utf-8'):
    """Convert an arbitrary value to bytes.

    Args:
        value: Some value.
        encoding: The byte encoding to use.

    Returns:
        x converted to a string and then encoded as bytes.
    """
    if isinstance(value, bytes):
        return value
    else:
        return str(value).encode(encoding)


@deprecated_str_to_path(1, 'path_or_file')
def write_bytes(iterable: Iterable, path_or_file: PathOrFile, sep: Optional[bytes]=b'', convert: Callable[([Any], bytes)]=to_bytes, **kwargs) -> int:
    """Write an iterable of bytes to a file.

    Args:
        iterable: An iterable.
        path_or_file: Path to the file, or a file-like object.
        sep: Separator between items.
        convert: Function that converts a value to bytes.
        kwargs: Additional arguments to pass top :method:`xphyle.open_`.

    Returns:
        Total number of bytes written, or -1 if ``errors=False`` and there was
        a problem opening the file.
    """
    if sep is None:
        sep = convert(os.linesep)
    if 'mode' not in kwargs:
        kwargs['mode'] = 'wb'
    written = 0
    with open_(path_or_file, **kwargs) as (fileobj):
        if fileobj is None:
            return -1
        for chunk in iterable:
            if written > 0:
                written += fileobj.write(sep)
            written += fileobj.write(convert(chunk))

    return written


FromStrFunc = Callable[([str], Any)]
ToStrFunc = Callable[([Any], str)]
RowFunc = Callable[([Sequence[str]], Any)]

@deprecated_str_to_path(0, 'path_or_file')
def read_dict(path_or_file: PathOrFile, sep: str='=', convert: Optional[FromStrFunc]=None, ordered: bool=False, **kwargs) -> Dict[(str, Any)]:
    """Read lines from simple property file (key=value). Comment lines (starting
    with '#') are ignored.

    Args:
        path_or_file: Property file, or a list of properties.
        sep: Key-value delimiter (defaults to '=').
        convert: Function to call on each value.
        ordered: Whether to return an OrderedDict.
        kwargs: Additional arguments to pass top `:method:`xphyle.open_`.

    Returns:
        An OrderedDict, if 'ordered' is True, otherwise a dict.
    """

    def _parse_line(line):
        line = line.strip()
        if len(line) == 0 or line[0] == '#':
            return
        else:
            return line.split(sep)

    lines = ((line[0], convert(line[1]) if convert else line[1]) for line in read_lines(path_or_file, convert=_parse_line, **kwargs) if line is not None)
    if ordered:
        return OrderedDict(lines)
    else:
        return dict(lines)


@deprecated_str_to_path(1, 'path_or_file')
def write_dict(dictobj: Dict[(str, Any)], path_or_file: PathOrFile, sep: str='=', linesep: Optional[str]='\n', convert: ToStrFunc=str, **kwargs) -> int:
    r"""Write a dict to a file as name=value lines.

    Args:
        dictobj: The dict (or dict-like object).
        path_or_file: Path to the file, or a file-like object.
        sep: The delimiter between key and value (defaults to '=').
        linesep: The delimiter between values, or ``os.linesep`` if None
            (defaults to '\n').
        convert: Function that converts a value to a string.

    Returns:
        Total number of bytes written, or -1 if ``errors=False`` and there was
        a problem opening the file.
    """
    if linesep is None:
        linesep = os.linesep
    lines = ('{}{}{}'.format(key, sep, convert(val)) for key, val in dictobj.items())
    return write_lines(lines, path_or_file, linesep=linesep, **kwargs)


@deprecated_str_to_path(0, 'path_or_file')
def read_delimited(path_or_file: PathOrFile, sep: str='\t', header: Union[(bool, Sequence[str])]=False, converters: Optional[Union[(FromStrFunc, Iterable[FromStrFunc])]]=None, yield_header: bool=True, row_type: Union[(str, RowFunc)]='list', **kwargs) -> Generator[(Union[(Tuple, Dict, Any)], None, None)]:
    """Iterate over rows in a delimited file.

    Args:
        path_or_file: Path to the file, or a file-like object.
        sep: The field delimiter.
        header: Either True or False to specifiy whether the file has a header,
            or a sequence of column names.
        converters: callable, or iterable of callables, to call on each value.
        yield_header: If header == True, whether the first row yielded should be
            the header row.
        row_type: The collection type to return for each row:
            tuple, list, or dict.
        kwargs: additional arguments to pass to `csv.reader`.

    Yields:
        Rows of the delimited file. If `header==True`, the first row yielded
        is the header row, and its type is always a list. Converters are not
        applied to the header row.
    """
    if row_type == 'dict':
        if not header:
            raise ValueError('Header must be specified for row_type=dict')
    with open_(path_or_file, **kwargs) as (fileobj):
        if fileobj is None:
            return
        else:
            reader = (csv.reader)(fileobj, delimiter=sep, **kwargs)
            header_row = None
            if header:
                header_row = next(reader)
                if yield_header:
                    yield header_row
            if converters:
                if is_iterable(converters):
                    converter_itr = cast(Iterable[FromStrFunc], converters)
                else:
                    if callable(converters):
                        converter_itr = cycle([converters])
                    else:
                        raise ValueError("'converters' must be iterable or callable")
                reader = ([fn(x) if fn else x for fn, x in zip(converter_itr, row)] for row in reader)
            if row_type == 'tuple':
                reader = (tuple(row) for row in reader)
            else:
                if row_type == 'dict':
                    if header_row is not None:
                        reader = (dict(zip(header_row, row)) for row in reader)
                elif callable(row_type):
                    reader = (row_type(row) for row in reader)
        yield from reader


@deprecated_str_to_path(0, 'path_or_file')
def read_delimited_as_dict(path_or_file: PathOrFile, sep: str='\t', header: Union[(bool, Sequence[str])]=False, key: Union[(int, str, RowFunc)]=0, **kwargs) -> Dict[(Any, Any)]:
    """Parse rows in a delimited file and add rows to a dict based on a a
    specified key index or function.

    Args:
        path_or_file: Path to the file, or a file-like object.
        sep: Field delimiter.
        header: If True, read the header from the first line of the file,
            otherwise a list of column names.
        key: The column to use as a dict key, or a function to extract the key
          from the row. If a string value, header must be specified. All values
          must be unique, or an exception is raised.
        kwargs: Additional arguments to pass to `read_delimited`.

    Returns:
        A dict with as many element as rows in the file.

    Raises:
        Exception if a duplicte key is generated.
    """
    itr = None
    if isinstance(key, str):
        if not header:
            raise ValueError("'header' must be specified if 'key' is a column name")
        else:
            if header is True:
                kwargs['yield_header'] = True
                itr = read_delimited(path_or_file, sep, True, **kwargs)
                header_seq = tuple(str(h) for h in next(itr))
            else:
                header_seq = tuple(cast(Sequence[str], header))
        key = header_seq.index(key)
    else:
        if isinstance(key, int):

            def keyfn(_row):
                return _row[key]

        else:
            if callable(key):
                keyfn = key
            else:
                raise ValueError("'key' must be an column name, index, or callable")
    if itr is None:
        kwargs['yield_header'] = False
        itr = read_delimited(path_or_file, sep, header, **kwargs)
    objects = {}
    for row in itr:
        k = keyfn(row)
        if k in objects:
            raise Exception('Duplicate key {}'.format(k))
        objects[k] = row

    return objects


@deprecated_str_to_path(0, 'source_file', 1, 'compressed_file')
def compress_file(source_file: PathOrFile, compressed_file: PathOrFile=None, compression: CompressionArg=None, keep: bool=True, compresslevel: int=None, use_system: bool=True, **kwargs) -> Path:
    """Compress an existing file, either in-place or to a separate file.

    Args:
        source_file: Path or file-like object to compress.
        compressed_file: The compressed path or file-like object. If None,
            compression is performed in-place. If True, file name is determined
            from ``source_file`` and the decompressed file is retained.
        compression: If True, guess compression format from the file
            name, otherwise the name of any supported compression format.
        keep: Whether to keep the source file.
        compresslevel: Compression level.
        use_system: Whether to try to use system-level compression.
        kwargs: Additional arguments to pass to the open method when
            opening the compressed file.

    Returns:
        The path to the compressed file.
    """
    if not isinstance(compression, str):
        if compressed_file:
            if isinstance(compressed_file, PurePath):
                name = str(compressed_file)
            else:
                name = cast(FileLike, compressed_file).name
            compression = FORMATS.guess_compression_format(name)
        else:
            raise ValueError("'compressed_file' or 'compression' must be specified")
    fmt = FORMATS.get_compression_format(compression)
    return (fmt.compress_file)(
     source_file, compressed_file, keep, compresslevel, use_system, **kwargs)


@deprecated_str_to_path(0, 'compressed_file', 1, 'dest_file')
def decompress_file(compressed_file: PathOrFile, dest_file: PathOrFile=None, compression: CompressionArg=None, keep: bool=True, use_system: bool=True, **kwargs) -> Path:
    """Decompress an existing file, either in-place or to a separate file.

    Args:
        compressed_file: Path or file-like object to decompress.
        dest_file: Path or file-like object for the decompressed file.
            If None, file will be decompressed in-place. If True, file will be
            decompressed to a new file (and the compressed file retained) whose
            name is determined automatically.
        compression: None or True, to guess compression format from the file
            name, or the name of any supported compression format.
        keep: Whether to keep the source file.
        use_system: Whether to try to use system-level compression
        kwargs: Additional arguments to pass to the open method when
            opening the compressed file.

    Returns:
        The path of the decompressed file.
    """
    if not isinstance(compression, str):
        if not isinstance(compressed_file, PurePath):
            source_path = Path(getattr(compressed_file, 'name'))
        else:
            source_path = cast(PurePath, compressed_file)
        compression = FORMATS.guess_compression_format(source_path)
    fmt = FORMATS.get_compression_format(compression)
    return (fmt.decompress_file)(compressed_file, dest_file, keep, use_system, **kwargs)


@deprecated_str_to_path(0, 'source_file', 1, 'dest_file')
def transcode_file(source_file: PathOrFile, dest_file: PathOrFile, source_compression: CompressionArg=True, dest_compression: CompressionArg=True, use_system: bool=True, source_open_args: Optional[dict]=None, dest_open_args: Optional[dict]=None) -> None:
    """Convert from one file format to another.

    Args:
        source_file: The path or file-like object to read from. If a file, it
            must be opened in mode 'rb'.
        dest_file: The path or file-like object to write to. If a file, it
            must be opened in binary mode.
        source_compression: The compression type of the source file. If True,
            guess compression format from the file name, otherwise the name of
            any supported compression format.
        dest_compression: The compression type of the dest file. If True,
            guess compression format from the file name, otherwise the name of
            any supported compression format.
        use_system: Whether to use system-level compression.
        source_open_args: Additional arguments to pass to xopen for the source
            file.
        dest_open_args: Additional arguments to pass to xopen for the
            destination file.
    """
    src_args = copy.copy(source_open_args) if source_open_args else {}
    if 'mode' not in src_args:
        src_args['mode'] = 'rb'
    dst_args = copy.copy(dest_open_args) if dest_open_args else {}
    if 'mode' not in dst_args:
        dst_args['mode'] = 'wb'
    with open_(source_file, compression=source_compression, use_system=use_system, **src_args) as (src):
        with open_(
 dest_file, compression=dest_compression, use_system=use_system, **dst_args) as (dst):
            for chunk in iter_file_chunked(src):
                dst.write(chunk)


@deprecated_str_to_path(0, 'source_file', 1, 'dest_file')
def uncompressed_size(path: PurePath, compression: CompressionArg=None) -> Optional[int]:
    """Get the uncompressed size of the compressed file.

    Args:
        path: The path to the compressed file.
        compression: None or True, to guess compression format from the file
            name, or the name of any supported compression format.

    Returns:
        The uncompressed size of the file in bytes, or None if the uncompressed
        size could not be determined (without actually decompressing the file).

    Raises:
        ValueError if the compression format is not supported.
    """
    if compression is not False:
        if not isinstance(compression, str):
            compression = FORMATS.guess_compression_format(path)
        if compression is not None:
            fmt = FORMATS.get_compression_format(compression)
            return fmt.uncompressed_size(path)
    return Path(path).stat().st_size


class CompressOnClose(EventListener[FileWrapper]):
    __doc__ = 'Compress a file after it is closed.\n    '
    compressed_path = None

    def execute(self, wrapper: FileWrapper, **kwargs) -> None:
        self.compressed_path = compress_file((wrapper.path), **kwargs)


class MoveOnClose(EventListener[FileWrapper]):
    __doc__ = 'Move a file after it is closed.\n    '

    def execute(self, wrapper: FileWrapper, dest: PurePath=None, **kwargs) -> None:
        shutil.move(wrapper.path, str(dest))


class RemoveOnClose(EventListener[FileWrapper]):
    __doc__ = 'Remove a file after it is closed.\n    '

    def execute(self, wrapper: FileWrapper, **kwargs) -> None:
        os.remove(wrapper.path)


def exec_process(*args, inp: AnyChar=None, timeout: int=None, **kwargs) -> Process:
    """Shortcut to execute a process, wait for it to terminate, and return the
    results.

    Args:
        args: Positional arguments to popen.
        inp: String/bytes to write to process input stream.
        timeout: Time to wait for process to complete.
        kwargs: Keyword arguments to popen.

    Returns:
        A terminated :class:`Process`. The contents of stdout and stderr are
        recorded in the `stdout` and `stderr` attributes.
    """
    with popen(*args, **kwargs) as (process):
        process.communicate(inp, timeout)
    return process


FilesArg = Iterable[Union[(PathOrFile, Tuple[(Any, PathOrFile)])]]
FileOrFilesArg = Optional[Union[(PathOrFile, FilesArg)]]

class FileManager(Sized):
    __doc__ = 'Dict-like container for files. Files are opened lazily (upon first\n    request) using `xopen`.\n\n    Args:\n        files: An iterable of files to add. Each item can either be a string\n            path or a (key, fileobj) tuple.\n        header: A header to write when opening writable files.\n        kwargs: Default arguments to pass to xopen.\n    '

    @deprecated_str_to_path(1, 'files')
    def __init__(self, files: FilesArg=None, header=None, **kwargs) -> None:
        self._files = OrderedDict()
        self._paths = {}
        self.header = header
        self.default_open_args = kwargs
        if files:
            self.add_all(files)

    def __enter__(self) -> 'FileManager':
        return self

    def __exit__(self, exception_type, exception_value, traceback) -> None:
        self.close()

    def __del__(self) -> None:
        self.close()

    def __len__(self) -> int:
        return len(self._files)

    def __getitem__(self, key: Any) -> FileLike:
        fileobj = self.get(key)
        if not fileobj:
            raise KeyError(key)
        return fileobj

    @deprecated_str_to_path(2, 'path_or_file')
    def __setitem__(self, key: Any, path_or_file: PathOrFile) -> None:
        """Add a file.

        Args:
            key: Dict key.
            path_or_file: Path or file object. If this is a path, the file will
                be opened with mode 'r'.
        """
        self.add(path_or_file, key)

    def __contains__(self, key: Any):
        return key in self._files

    @deprecated_str_to_path(1, 'path_or_file')
    def add(self, path_or_file: PathOrFile, key: Optional[Any]=None, **kwargs) -> None:
        """Add a file.

        Args:
            path_or_file: Path or file object. If this is a path, the file will
                be opened with the specified mode.
            key: Dict key. Defaults to the file name.
            kwargs: Arguments to pass to xopen. These override any keyword
                arguments passed to the FileManager's constructor.
        """
        if isinstance(path_or_file, PurePath):
            path = path_or_file
            fileobj = copy.copy(self.default_open_args)
            fileobj.update(kwargs)
        else:
            path = Path(getattr(path_or_file, 'name'))
            fileobj = cast(FileLike, path_or_file)
        if key is None:
            key = path
        if key in self._files:
            raise ValueError('Already tracking file with key {}'.format(key))
        self._files[key] = fileobj
        self._paths[key] = path

    @deprecated_str_to_path(1, 'files', dict_args=(1, 'files'))
    def add_all(self, files: Union[(FilesArg, Dict[(Any, PathOrFile)])], **kwargs) -> None:
        """Add all files from an iterable or dict.

        Args:
            files: An iterable or dict of files to add. If an iterable, each
                item can either be a string path or a (key, fileobj) tuple.
            kwargs: Additional arguments to pass to `add`.
        """
        if isinstance(files, dict):
            for key, path_or_file in files.items():
                self.add(path_or_file, key=key)

        else:
            for fileobj in files:
                if isinstance(fileobj, PurePath):
                    (self.add)(fileobj, **kwargs)
                else:
                    key, path_or_file = cast(Tuple[(Any, PathOrFile)], fileobj)
                    (self.add)(path_or_file, key=key, **kwargs)

    def get(self, key: Any) -> Optional[FileLike]:
        """Get the file object associated with a path. If the file is not
        already open, it is first opened with `xopen`.

        Args:
            key: The file name/key.

        Returns:
            The opened file.
        """
        fileobj = self._files.get(key, None)
        if fileobj is None:
            if isinstance(key, int):
                if len(self) > key:
                    key = list(self.keys)[key]
                    fileobj = self._files[key]
            else:
                return
        if isinstance(fileobj, dict):
            path = self._paths[key]
            fileobj['context_wrapper'] = True
            fileobj = xopen(path, **fileobj)
            if self.header:
                if fileobj.writable():
                    fileobj.write(self.header)
            self._files[key] = fileobj
        return fileobj

    def get_path(self, key: Any) -> PurePath:
        """Returns the file path associated with a key.

        Args:
            key: The key to resolve.

        Returns:
            The file path.
        """
        if isinstance(key, int):
            if len(self) > int(key):
                key = list(self.keys)[key]
        return self._paths[key]

    @property
    def keys(self) -> Sequence[Any]:
        """Returns a list of all keys in the order they were added.
        """
        return tuple(self._files.keys())

    @property
    def paths(self) -> Sequence[PurePath]:
        """Returns a list of all paths in the order they were added.
        """
        return list(self._paths[key] for key in self.keys)

    def iter_files(self) -> Generator[(Tuple[(Any, FileLike)], None, None)]:
        """Iterates over all (key, file) pairs in the order they were added.
        """
        yield from ((key, self.get(key)) for key in list(self.keys))
        if False:
            yield None

    def close(self) -> None:
        """Close all files being tracked.
        """
        if not hasattr(self, '_files'):
            return
        for fileobj in self._files.values():
            if fileobj and not (isinstance(fileobj, dict) or fileobj.closed):
                fileobj.close()


class FileInput(FileManager, Generic[CharMode], Iterator[CharMode]):
    __doc__ = "Similar to python's :module:`fileinput` that uses `xopen` to open files.\n    Currently only supports sequential line-oriented access via `next` or\n    `readline`.\n\n    Args:\n        files: List of files.\n        char_mode: text or binary mode.\n\n    Notes:\n        Default values are not allowed for generically typed parameters. In\n        a future version, `char_mode` will default to None and it will be\n        required to specify the mode, or use one of the convenience methods\n        (:method:`textinput` or :method:`byteinput`).\n    "

    @deprecated_str_to_path(1, 'files')
    def __init__(self, files=None, char_mode=None):
        super().__init__(mode=('rt' if char_mode is TextMode else 'rb'))
        self.char_mode = char_mode
        self.fileno = -1
        self._startlineno = 0
        self.filelineno = 0
        self._pending = True
        self._nextline = None
        if files:
            self.add_all(files)

    @property
    def filekey(self) -> Any:
        """The key of the file currently being read.
        """
        if self.fileno < 0:
            return
        else:
            return list(self.keys)[self.fileno]

    @property
    def filename(self) -> Optional[PurePath]:
        """The name of the file currently being read.
        """
        if self.fileno < 0:
            return
        else:
            return self.get_path(self.fileno)

    @property
    def lineno(self) -> int:
        """The total number of lines that have been read so far from all files.
        """
        return self._startlineno + self.filelineno

    @property
    def finished(self) -> bool:
        """Whether all data has been read from all files.
        """
        return self.fileno >= len(self)

    @deprecated_str_to_path(1, 'path_or_file')
    def add(self, path_or_file, key=None, **kwargs):
        """Overrides FileManager.add() to prevent file-specific open args.
        """
        if self.finished:
            self._pending = True
            self.fileno -= 1
        super().add(path_or_file, key)

    def __iter__(self) -> 'FileInput':
        return self

    def __next__(self) -> CharMode:
        while True:
            if not self._ensure_file():
                raise StopIteration()
            try:
                line = cast(CharMode, self._nextline())
                self.filelineno += 1
                return line
            except StopIteration:
                self._pending = True

    def _ensure_file(self) -> bool:
        if self._pending:
            self.fileno += 1
            self._startlineno += self.filelineno
            self.filelineno = 0
            if not self.finished:
                curfile = self.get(self.fileno)
                if is_iterable(curfile):
                    self._nextline = lambda : next(curfile)
                else:
                    raise Exception("File associated with key {} is not iterable and does not have a 'readline' method".format(self.filekey))
            self._pending = False
        return not self.finished

    def readline(self) -> CharMode:
        """Read the next line from the current file (advancing to the next
        file if necessary and possible).

        Returns:
            The next line, or the undefined string if `self.finished==True`.
        """
        try:
            return next(self)
        except StopIteration:
            return cast(CharMode, b'' if self.char_mode == BinMode else '')


@deprecated_str_to_path(0, 'files')
def fileinput(files: FileOrFilesArg=None, char_mode: CharMode=None) -> FileInput[CharMode]:
    """Convenience method that creates a new ``FileInput``.

    Args:
        files: The files to open. If None, files passed on the command line are
            used, or STDIN if there are no command line arguments.
        char_mode: The default read mode ('t' for text or b'b' for binary).

    Returns:
        A FileInput instance.

    Notes:
        Default values are not allowed for generically typed parameters.
        Use :method:`textinput` or :method:`byteinput` instead.
    """
    if not files:
        files = sys.argv[1:] or (STDIN,)
    else:
        if isinstance(files, PurePath):
            files = (
             files,)
    return FileInput(files, char_mode)


@deprecated_str_to_path(0, 'files')
def textinput(files: FileOrFilesArg=None):
    """Convenience method that creates a new ``FileInput`` in text mode.

    Args:
        files: The files to open. If None, files passed on the command line are
            used, or STDIN if there are no command line arguments.

    Returns:
        A FileInput[Text] instance.
    """
    return fileinput(files, TextMode)


@deprecated_str_to_path(0, 'files')
def byteinput(files: FileOrFilesArg=None):
    """Convenience method that creates a new ``FileInput`` in bytes mode.

    Args:
        files: The files to open. If None, files passed on the command line are
            used, or STDIN if there are no command line arguments.

    Returns:
        A FileInput[bytes] instance.
    """
    return fileinput(files, BinMode)


class FileOutput(FileManager, Generic[CharMode], metaclass=ABCMeta):
    __doc__ = "Base class for file manager that writes to multiple files.\n\n    Args:\n        files: The list of files to open.\n        char_mode: The CharMode.\n        access: How to open the output files ('w', 'a', 'x').\n        linesep: The line separator (type must match `char_mode`).\n        encoding: Default character encoding to use.\n        header: Default file header to write when opening output files.\n\n    Notes:\n        Default values for generically typed parameters are not allowed. In a\n        future version, `char_mode` and `linesep` will default to None and\n        must be explicitly defined.\n    "

    @deprecated_str_to_path(1, 'files')
    def __init__(self, files=None, access='w', char_mode=None, linesep=None, encoding='utf-8', header=None):
        super().__init__(mode=FileMode(access=access, coding=('t' if char_mode == TextMode else 'b')),
          header=header)
        self.access = access
        self.char_mode = char_mode
        self._empty = cast(CharMode, b'' if char_mode == BinMode else '')
        self.encoding = encoding
        self.num_lines = 0
        self.linesep = linesep
        self._linesep_len = len(linesep)
        if files:
            self.add_all(files)

    def write(self, data: Any, detect_newlines: bool=True) -> int:
        """Writes data to the output.

        Args:
            data: The data to write; will be converted to string/bytes.
            detect_newlines: If True, `data` is split on :attr:`linesep` and the
                resulting lines are written using :method:`writelines`,
                otherwise data is writen using :method:`writeline`.

        Returns:
            The number of characters written.
        """
        if not isinstance(data, (str, bytes)):
            data = str(data)
        else:
            if detect_newlines:
                result = self.writelines(data.rstrip().split(self.linesep))
            else:
                result = self.writeline(data)
        return result[1]

    def writelines(self, lines: Iterable[AnyChar]) -> Tuple[(int, int)]:
        """Write an iterable of lines to the output(s).

        Args:
            lines: An iterable of lines to write.

        Returns:
            The tuple (lines_written, chars_written).
        """
        line_counts, char_counts = zip(*list(self.writeline(line) for line in lines))
        return (sum(line_counts), sum(char_counts))

    def writeline(self, line: Optional[AnyChar]=None) -> Tuple[(int, int)]:
        """Write a line to the output(s).

        Args:
            line: The line to write.

        Returns:
            The tuple (lines_written, chars_written).
        """
        char_count = self._writeline(self._encode(line))
        self.num_lines += 1
        return (1, char_count)

    @abstractmethod
    def _writeline(self, line: CharMode) -> int:
        """Does the work of writing a line to the output(s). Must be implemented
        by subclasses.

        Args:
            line: The line to write.

        Returns:
            The number of characters written.
        """
        pass

    def _encode(self, line: AnyChar) -> CharMode:
        is_binary = isinstance(line, bytes)
        if self.char_mode is BinMode:
            if not is_binary:
                line = cast(str, line).encode(self.encoding)
        if self.char_mode is not BinMode:
            if is_binary:
                line = cast(bytes, line).decode(self.encoding)
        return cast(CharMode, line)

    def _write_to_file(self, fileobj: FileLike, line: CharMode) -> int:
        """Writes a line to a file, gracefully handling the (rare? nonexistant?)
        case where the file has a `writelines` but not a `write` method.

        Args:
            fileobj: The file in which to write the line.
            line: The line to write.

        Returns:
            The number of bytes/characters written.
        """
        try:
            if line:
                fileobj.write(line)
            fileobj.write(self.linesep)
        except AttributeError:
            fileobj.writelines((line + self.linesep,))

        return len(line) + self._linesep_len


class TeeFileOutput(Generic[CharMode], FileOutput[CharMode]):
    __doc__ = 'Write output to mutliple files simultaneously.\n    '

    def _writeline(self, line: CharMode=None) -> int:
        char_count = None
        for _, fileobj in self.iter_files():
            file_char_count = self._write_to_file(fileobj, line)
            if char_count:
                assert char_count == file_char_count
            else:
                char_count = file_char_count

        return char_count


class CycleFileOutput(FileOutput):
    __doc__ = 'Alternate each line between files.\n\n    Args:\n        files: A list of files.\n        char_mode: The character mode.\n    '

    @deprecated_str_to_path(1, 'files')
    def __init__(self, files=None, char_mode=None, **kwargs):
        (super().__init__)(files=files, char_mode=char_mode, **kwargs)

    def _writeline(self, line: CharMode=None) -> int:
        return self._write_to_file(self.get(self.num_lines % len(self)), line)


class NCycleFileOutput(FileOutput):
    __doc__ = 'Alternate output lines between files.\n\n    Args:\n        files: A list of files.\n        char_mode: The character mode.\n        num_lines: How many lines to write to a file before moving on to the\n            next file.\n    '

    @deprecated_str_to_path(1, 'files')
    def __init__(self, files=None, char_mode=None, lines_per_file=1, **kwargs):
        (super().__init__)(files=files, char_mode=char_mode, **kwargs)
        self.lines_per_file = lines_per_file

    def _writeline(self, line: CharMode=None) -> int:
        file_idx = self.num_lines // self.lines_per_file % len(self)
        return self._write_to_file(self.get(file_idx), line)


class TokenFileOutput(FileOutput):
    __doc__ = "Generate file names according to a pattern.\n\n    Args:\n        filename_pattern: The pattern of file names to create. Should have a\n            single token ('{}' or '{0}') that is replaced with the file index.\n        char_mode: The character mode.\n        kwargs: Additional args.\n    "

    def __init__(self, filename_pattern=None, char_mode=None, **kwargs):
        (super().__init__)(char_mode=char_mode, **kwargs)
        self.filename_pattern = filename_pattern

    def _writeline(self, line: CharMode=None) -> int:
        tokens = self._get_outfile_tokens(line)
        path = Path((self.filename_pattern.format)(**tokens))
        if path not in self:
            self.add(path)
        return self._write_to_file(self.get(path), line)

    @abstractmethod
    def _get_outfile_tokens(self, line: CharMode=None) -> dict:
        """Get the tokens that determine 1) the file key and 2) the file name.

        Args:
            line: The line from the file.

        Returns:
            A dict of tokens.
        """
        pass


class PatternFileOutput(TokenFileOutput):
    __doc__ = "Use a callable to generate filenames based on data in lines.\n\n    Args:\n        filename_pattern: The pattern of file names to create. Should have a\n            single token ('{}' or '{0}') that is replaced with the file index.\n        char_mode: The character mode.\n        token_func: Function to extract token(s) from lines in file. By default\n            this is the identity function, which is almost never what you want.\n        kwargs: Additional args.\n    "

    def __init__(self, filename_pattern=None, char_mode=None, token_func=lambda x: {x: x}, **kwargs):
        if not isinstance(filename_pattern, str):
            filename_pattern = cast(Tuple[(Any, PathOrFile)], filename_pattern)[0]
        (super().__init__)(filename_pattern, char_mode, **kwargs)
        self.token_func = token_func

    def _get_outfile_tokens(self, line: CharMode=None) -> dict:
        return self.token_func(line)


class RollingFileOutput(TokenFileOutput):
    __doc__ = "Write up to ``num_lines`` lines to a file before opening the next file.\n    File names are created from a pattern.\n\n    Args:\n        filename_pattern: The pattern of file names to create. Should have a\n            single token ('{}' or '{0}') that is replaced with the file index.\n        char_mode: The character mode.\n        num_lines: The max number of lines to write to each file.\n        kwargs: Additional args.\n    "

    def __init__(self, filename_pattern=None, char_mode=None, lines_per_file=1, **kwargs):
        if isinstance(filename_pattern, str):
            filepat_str = filename_pattern
        else:
            filepat_str = tuple(filename_pattern)[0]
        (super().__init__)(filepat_str, char_mode, **kwargs)
        self.lines_per_file = lines_per_file

    def _get_outfile_tokens(self, line: CharMode=None) -> dict:
        return {'index': self.num_lines // self.lines_per_file}


PatternOrFileOrFilesArg = Optional[Union[(str, PathOrFile, FilesArg)]]

def fileoutput(files: PatternOrFileOrFilesArg=None, char_mode: CharMode=None, linesep: CharMode=None, encoding: str='utf-8', file_output_type: Callable[(..., FileOutput[CharMode])]=TeeFileOutput[CharMode], **kwargs) -> FileOutput[CharMode]:
    """Convenience function to create a fileoutput.

    Args:
        files: The files to write to. Can include '-'/'_' for stdout/stderr.
        char_mode: The write mode ('t' or b'b').
        linesep: The separator to use when writing lines.
        encoding: The default file encoding to use.
        file_output_type: The specific subclass of FileOutput to create.
        kwargs: additional arguments to pass to the FileOutput constructor.

    Returns:
        A FileOutput instance.

    Notes:
        Default values are not allowed for generically typed parameters.
        Use :method:`textoutput` or :method:`byteoutput` instead.
    """
    if not files:
        files = sys.argv[1:] or (STDOUT,)
    elif isinstance(files, PurePath):
        files = (
         files,)
    else:
        if linesep or char_mode == TextMode:
            linesep = cast(CharMode, os.linesep)
        else:
            linesep = cast(CharMode, os.linesep.encode(encoding))
    return file_output_type(
 files, char_mode=char_mode, linesep=linesep, encoding=encoding, **kwargs)


def textoutput(files: FileOrFilesArg=None, file_output_type: Callable[(..., FileOutput[str])]=TeeFileOutput[str], **kwargs) -> FileOutput[str]:
    """Convenience function to create a fileoutput in text mode.

    Args:
        files: The files to write to.
        file_output_type: The specific subclass of FileOutput to create.
        kwargs: additional arguments to pass to the FileOutput constructor.

    Returns:
        A FileOutput instance.
    """
    return fileoutput(
 files, char_mode=TextMode, 
     linesep=os.linesep, 
     file_output_type=file_output_type, **kwargs)


def byteoutput(files: FileOrFilesArg=None, file_output_type: Callable[(..., FileOutput[bytes])]=TeeFileOutput[bytes], **kwargs) -> FileOutput[bytes]:
    """Convenience function to create a fileoutput in bytes mode.

    Args:
        files: The files to write to.
        file_output_type: The specific subclass of FileOutput to create.
        kwargs: additional arguments to pass to the FileOutput constructor.

    Returns:
        A FileOutput instance.
    """
    return fileoutput(
 files, char_mode=BinMode, 
     linesep=os.linesep.encode(), 
     file_output_type=file_output_type, **kwargs)


@deprecated_str_to_path(1, 'path_or_file')
def linecount(path_or_file: PathOrFile, linesep: Optional[bytes]=None, buffer_size: int=1048576, **kwargs) -> int:
    r"""Fastest pythonic way to count the lines in a file.

    Args:
        path_or_file: File object, or path to the file.
        linesep: Line delimiter, specified as a byte string (e.g. b'\n').
        buffer_size: How many bytes to read at a time (1 Mb by default).
        kwargs: Additional arguments to pass to the file open method.

    Returns:
        The number of lines in the file. Blank lines (including the last line
        in the file) are included.
    """
    if buffer_size < 1:
        raise ValueError("'buffer_size' must be >= ")
    else:
        if linesep is None:
            linesep = os.linesep.encode()
        if 'mode' not in kwargs:
            kwargs['mode'] = 'rb'
        elif FileMode(kwargs['mode']).value != 'rb':
            raise ValueError("File must be opened with mode 'rb'")
    with open_(path_or_file, **kwargs) as (fileobj):
        if fileobj is None:
            return -1
        else:
            read_f = fileobj.read
            buf = read_f(buffer_size)
            if len(buf) == 0:
                return 0
            lines = 1
            while buf:
                lines += buf.count(linesep)
                buf = read_f(buffer_size)

            return lines