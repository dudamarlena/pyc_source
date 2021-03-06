# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/runner/runners/2.169.1/work/MetaWards/MetaWards/tests/../build/lib.macosx-10.14-x86_64-3.7/metawards/_outputfiles.py
# Compiled at: 2020-05-10 15:00:16
# Size of source mod 2**32: 16186 bytes
from pathlib import Path as _Path
__all__ = [
 'OutputFiles']

def _get_bool(arg):
    """Simple function to make sure that flags that are supposed
       to be true/false are actually stored as bools
    """
    if arg:
        return True
    return False


def _is_empty(outdir):
    """Simple function that checks whether or not the passed directory
       is empty
    """
    import os
    if os.path.isfile(outdir):
        return False
    if os.path.isdir(outdir):
        return len(os.listdir(outdir)) == 0
    return True


def _rmdir(directory):
    """Function modified from one copied from 'mitch' on stackoverflow
       https://stackoverflow.com/questions/13118029/deleting-folders-in-python-recursively
    """
    directory = _Path(directory)
    if directory == _Path.home():
        raise FileExistsError(f"We WILL NOT remove your home directory ${directory}")
    if directory == _Path('/'):
        raise FileExistsError(f"We WILL NOT remove the root directory {directory}")
    if directory == _Path.home().parent:
        raise FileExistsError(f"We WILL NOT remove the users/home directory {directory}")
    if not directory.is_dir():
        directory.unlink()
        return
    for item in directory.iterdir():
        if item.is_dir():
            _rmdir(item)
        else:
            print(f"removing file {item}")
            item.unlink()

    print(f"removing directory {directory}")
    directory.rmdir()


def _check_remove(outdir, prompt):
    """Function to check if the user wants to remove the directory,
       giving them the option to continue, quit or remove all files
    """
    if prompt is None:
        raise FileExistsError(f"Cannot continue as {outdir} already exists!")
    y = prompt(f"{outdir} already exists.\nDo you want to remove it? (y/n) ")
    y = y.strip().lower()
    if len(y) > 0:
        if y == 'y':
            print(f"Removing all files in {outdir}")
            _rmdir(_Path(outdir))
            return
    y = prompt(f"Continuing with this run will mix its output with\nthe files already in {outdir}.\nDo you want to continue with this run? (y/n) ")
    y = y.strip().lower()
    if len(y) == 0 or y != 'y':
        print('Exiting the program as we cannot run any more.')
        import sys
        sys.exit(-1)


def _force_remove(outdir, prompt):
    """Function to force the removal of a directory, using the
       passed prompt to double-check with the user. If 'prompt'
       is None, then we go ahead
    """
    import os
    if not os.path.exists(outdir):
        return
    if prompt:
        y = prompt(f"{outdir} already exists.\nDo you want to remove it? (y/n) ")
        y = y.strip().lower()
        if len(y) == 0 or y != 'y':
            raise FileExistsError(f"Cannot continue as {outdir} already exists")
    print(f"Removing all files in {outdir}")
    _rmdir(_Path(outdir))


def _expand(path):
    """Expand all variables and user indicators in the passed path"""
    import os
    return os.path.expanduser(os.path.expandvars(path))


class OutputFiles:
    __doc__ = 'This is a class that manages all of the output files that\n       are written to during a model outbreak. This object is used\n       to hold the \'FILE\' objects for open files, and will\n       ensure that these files are closed and written to disk\n       as needed. It will also ensure that files are written\n       to the correct output directory, and that they are only\n       opened when they are needed (e.g. only the first call\n       to open the file will actually open it - subsequent\n       calls will return the already-open file handler)\n\n       Examples\n       --------\n       >>> output = OutputFiles(output_dir="output", check_empty=True)\n       >>> FILE = output.open("output.txt")\n       >>> FILE.write("some output\\n")\n       >>> FILE = output.open("something.csv.bz2", auto_bzip=True)\n       >>> FILE.write("something,else,is,here\\n")\n       >>> output.flush()\n       >>> FILE = output.open("output.txt")\n       >>> FILE.write("some more output\\n")\n       >>> output.close()\n\n       Note that you can also use OutputFiles in a contexthandler, to\n       ensure that all output files are automatically closed, e.g.\n\n       >>> with OutputFiles(output_dir="output") as output:\n       >>>     FILE = output.open("output.txt")\n       >>>     FILE.write("something\\n")\n    '

    def __init__(self, output_dir: str='output', check_empty: bool=True, force_empty: bool=False, prompt=input, auto_bzip: bool=False):
        """Construct a set of OutputFiles. These will all be written
           to 'output_dir'.

           Parameters
           ----------
           output_dir: str
             The directory in which to create all of the output files.
             This directory will be created automatically if it doesn't
             exist
           check_empty: bool
             Whether or not to check if the directory is empty before
             continuing. If the directory is not empty, then the user
             will be prompted to make a decision to either keep going,
             choose a different directory, remove existing output
             or exit
           force_empty: bool
             Force the output directory to be empty. BE CAREFUL as this
             will remove all files in that directory! There are checks
             to stop you doing something silly, but these are not
             fool-proof. The user will be prompted to confirm that
             the files should be removed
           prompt:
             This is the function that should be called to prompt the
             user for input, e.g. to confirm whether or not files
             should be deleted. This defaults to `input`. Set this
             to None if you *really* want MetaWards to remove files
             silently (e.g. useful if you are running batch jobs
             on a cluster and you really know what you are doing)
           auto_bzip: bool
             The default flag for `auto_bzip` when opening files. If
             this is true then all files will be automatically bzipped
             (compressed) as they are written, unless the code opening
             the file has explicitly asked otherwise
        """
        self._check_empty = _get_bool(check_empty)
        self._force_empty = _get_bool(force_empty)
        self._auto_bzip = _get_bool(auto_bzip)
        self._prompt = prompt
        self._output_dir = output_dir
        self._is_open = False
        self._open_files = {}
        self._filenames = {}
        self._open_dir()

    def __enter__(self):
        self._open_dir()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._close_dir()

    def _open_dir(self):
        """Internal function used to open the directory in which
           all output files will be placed
        """
        if not self._is_open:
            if self._output_dir is None:
                return
            import os
            if self._output_dir is None:
                raise ValueError('You cannot open an empty OutputFiles!')
            outdir = _expand(self._output_dir)
            if os.path.exists(outdir):
                outdir = os.path.abspath(outdir)
                if self._check_empty and not _is_empty(outdir):
                    if self._force_empty:
                        _force_remove(outdir, self._prompt)
                    else:
                        _check_remove(outdir, self._prompt)
                    try:
                        os.makedirs(outdir)
                    except FileExistsError:
                        pass

                    if not os.path.isdir(outdir):
                        print(f"Cannot open {outdir} as it is not a directory!")
                        raise FileExistsError(f"{outdir} is an existing file!")
        else:
            try:
                os.makedirs(outdir)
            except FileExistsError as e:
                try:
                    if not os.path.isdir(outdir):
                        raise e
                finally:
                    e = None
                    del e

        self._output_dir = str(_Path(outdir).absolute().resolve())
        self._is_open = True

    def _close_dir(self):
        """Internal function used to close all of the output files"""
        if not self._is_open:
            return
        errors = []
        for filename, handle in self._open_files.items():
            try:
                handle.close()
            except Exception as e:
                try:
                    errors.append(f"Could not close {filename}: {e.__class__} {e}")
                finally:
                    e = None
                    del e

        self._is_open = False
        self._open_files = {}
        self._filenames = {}

    @staticmethod
    def remove(path, prompt=input):
        """Remove the passed filename or directory

           Parameters
           ----------
           path: str
             The path to the file or directory or remove
           prompt:
             Prompt to use to ask the user - if None then no checks!
        """
        path = _Path(_expand(path)).absolute().resolve()
        _force_remove(path, prompt)

    def is_open(self):
        """Return whether or not the output files are open"""
        return self._is_open

    def is_closed(self):
        """Return whether or not the output files are closed"""
        return not self.is_open()

    def output_dir(self):
        """Return the absolute path of the directory to which
           the output files will be written
        """
        return self._output_dir

    def open(self, filename: str, auto_bzip=None, mode='t', headers=None, sep=' '):
        """Open the file called 'filename' in the output directory,
           returning a handle to that file. Note that this will
           open the file once, and will return the already-open
           file handle on all subsequent calls.

           Parameters
           ----------
           filename: str
             The name of the file to open. This must be relative
             to the output directory, and within that directory.
             It is an error to try to open a file that is
             not contained within this directory.
           auto_bzip: bool
             Whether or not to open the file in auto-bzip (compression)
             mode. If this is True then the file will be automatically
             compressed as it is written. The filename will have
             '.bz2' automatically appended so that this is clear.
             If this is False then the file will be written uncompressed.
             If 'None' is passed (the default) then the value of
             `auto_bzip` that was passed to the constructor of
             this OutputFiles will be used. Note that this flag is
             ignored if the file is already open.
           mode: str
             The mode of opening the file, e.g. 't' for text mode, and
             'b' for binary mode. The default is text mode
           headers: list[str] or plain str
             The headers to add to the top of the file, e.g. if it will
             contain column data. This will be written to the first line
             when the file is opened. If a list is passed, then this
             will be written joined together using 'sep'. If a plain
             string is passed then this will be written.
             If nothing is passed then no headers will be written.
           sep: str
             The separator used for the headers (e.g. " " or "," are good
             choices). By default things are space-separated

           Returns
           -------
           file
             The handle to the open file
        """
        import os
        self._open_dir()
        outdir = self._output_dir
        p = _Path(_expand(filename))
        if not p.is_absolute():
            p = _Path(os.path.join(outdir, filename))
        filename = str(p.absolute().resolve())
        prefix = os.path.commonprefix([outdir, filename])
        if prefix != outdir:
            raise ValueError(f"You cannot try to open {filename} as this is not in the output directory {outdir} - common prefix is {prefix}")
        if filename in self._open_files:
            return self._open_files[filename]
        if auto_bzip is None:
            auto_bzip = self._auto_bzip
        else:
            auto_bzip = _get_bool(auto_bzip)
            if auto_bzip:
                import bz2
                if not filename.endswith('.bz2'):
                    suffix = '.bz2'
                else:
                    suffix = ''
                FILE = bz2.open(f"{filename}{suffix}", f"w{mode}")
                self._open_files[filename] = FILE
                self._filenames[filename] = f"{filename}{suffix}"
            else:
                FILE = open(filename, f"w{mode}")
                self._open_files[filename] = FILE
                self._filenames[filename] = filename
            if headers is not None:
                if isinstance(headers, str):
                    FILE.write(headers)
                    FILE.write('\n')
                else:
                    FILE.write(sep.join([str(x) for x in headers]))
                    FILE.write('\n')
        return FILE

    def open_subdir(self, dirname):
        """Create and open a sub-directory in this OutputFiles
           called 'dirname'. This will inherit all properties,
           e.g. check_empty, auto_bzip etc from this OutputFiles

           Parameters
           ----------
           dirname: str
             The name of the subdirectory to open

           Returns
           -------
           subdir: OutputFiles
             The open subdirectory
        """
        import os
        self._open_dir()
        outdir = self._output_dir
        p = _Path(_expand(dirname))
        if not p.is_absolute():
            p = _Path(os.path.join(outdir, dirname))
        subdir = str(p.absolute().resolve())
        prefix = os.path.commonprefix([outdir, subdir])
        if prefix != outdir:
            raise ValueError(f"You cannot try to open {dirname} as this is not in the output directory {outdir} - common prefix is {prefix}")
        return OutputFiles(output_dir=subdir, check_empty=(self._check_empty), force_empty=(self._force_empty),
          prompt=(self._prompt),
          auto_bzip=(self._auto_bzip))

    def auto_bzip(self):
        """Return whether the default is to automatically bzip2 files"""
        return self._auto_bzip

    def get_path(self):
        """Return the full expanded path to this directory"""
        return self._output_dir

    def get_filename(self, filename):
        """Return the full expanded filename for 'filename'"""
        import os
        self._open_dir()
        outdir = self._output_dir
        p = _Path(_expand(filename))
        if not p.is_absolute():
            p = _Path(os.path.join(outdir, filename))
        filename = str(p.absolute().resolve())
        if filename in self._filenames:
            return self._filenames[filename]
        raise FileNotFoundError(f"No open file {filename}")

    def close(self):
        """Close all of the files and this directory"""
        self._close_dir()

    def flush(self):
        """Flush the contents of all files to disk"""
        for filename, handle in self._open_files.items():
            try:
                handle.flush()
            except Exception:
                pass