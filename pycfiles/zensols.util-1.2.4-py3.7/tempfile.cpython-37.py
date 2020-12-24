# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/zensols/util/tempfile.py
# Compiled at: 2020-05-11 00:54:36
# Size of source mod 2**32: 3312 bytes
import logging
from pathlib import Path
import tempfile as tf
logger = logging.getLogger(__name__)

class TemporaryFileName(object):
    __doc__ = 'Create a temporary file names on the file system.  Note that this does not\n    create the file object itself, only the file names.  In addition, the\n    generated file names are tracked and allow for deletion.  Specified\n    directories are also created, which is only needed for non-system temporary\n    directories.\n\n    The object is iterable, so usage with ``itertools.islice`` can be used to\n    get as many temporary file names as desired.  Calling instances (no\n    arguments) generate a single file name.\n\n    '

    def __init__(self, directory: str=None, file_fmt: str='{name}', create: bool=False, remove: bool=True):
        """Initialize with file system data.

        :param directory: the parent directory of the generated file
        :param file_fmt: a file format that substitutes ``name`` for the create
                         temporary file name; defaults to ``{name}``
        :param create: if ``True``, create ``directory`` if it doesn't exist
        :param remove: if ``True``, remove tracked generated file names if they
                       exist

        :see tempfile:

        """
        if directory is None:
            self.directory = Path(tf._get_default_tempdir())
        else:
            self.directory = Path(directory)
        self.file_fmt = file_fmt
        self.create = create
        self.remove = remove
        self.created = []

    def __iter__(self):
        return self

    def __next__(self):
        fname = next(tf._get_candidate_names())
        fname = (self.file_fmt.format)(**{'name': fname})
        if self.create:
            if not self.directory.exists():
                logger.info(f"creating directory {self.directory}")
                self.directory.mkdir(parents=True, exist_ok=True)
        path = Path(self.directory, fname)
        self.created.append(path)
        return path

    def __call__(self):
        return next(self)

    def clean(self):
        """Remove any files generated from this instance.  Note this only deletes the
        files, not the parent directory (if it was created).

        This does nothing if ``remove`` is ``False`` in the initializer.

        """
        if self.remove:
            for path in self.created:
                logger.debug(f"delete candidate: {path}")
                if path.exists():
                    logger.info(f"removing temorary file {path}")
                    path.unlink()


class tempfile(object):
    __doc__ = 'Generate a temporary file name and return the name in the ``with``\n    statement.  Arguments to the form are the same as ``TemporaryFileName``.\n    The temporary file is deleted after completion (see ``TemporaryFileName``).\n\n    Example:\n\n        with tempfile(\'./tmp\', create=True) as fname:\n            print(f\'writing to {fname}\')\n            with open(fname, \'w\') as f:\n                f.write("this file will be deleted, but left with ./tmp\n")\n\n    '

    def __init__(self, *args, **kwargs):
        self.temp = TemporaryFileName(*args, **kwargs)

    def __enter__(self):
        self.path = self.temp()
        return self.path

    def __exit__(self, type, value, traceback):
        self.temp.clean()