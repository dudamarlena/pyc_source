# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/mffpy/mffdir.py
# Compiled at: 2020-01-29 20:14:20
# Size of source mod 2**32: 6161 bytes
"""
Copyright 2019 Brain Electrophysiology Laboratory Company LLC

Licensed under the ApacheLicense, Version 2.0(the "License");
you may not use this module except in compliance with the License.
You may obtain a copy of the License at:

http: // www.apache.org / licenses / LICENSE - 2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
ANY KIND, either express or implied.
"""
import re
from os import listdir
from os.path import join, exists, splitext, basename, isdir
from collections import defaultdict, namedtuple
from typing import Dict, List, Tuple, IO
from . import zipfile
SignalAndInfo = namedtuple('SignalAndInfo', 'signal info')
SignalAndInfo: Tuple[(IO[bytes], str)]

class MFFDirBase:
    __doc__ = '.mff directory path\n\n    An `MFFDirBase` is able to access and spawn all file in an mff directory\n    container.\n    '
    _extensions = ('.mff', '.mfz')
    _extensions: Tuple[(str, ...)]
    _ext_err = 'Unknown file type ["%s"]'
    _re_nu = re.compile('\\d+')

    def __init__(self, filename: str):
        """initialize new .mff directory instance

        **Parameters:**
        `filename` (str) - the full path to the .mff directory.
        """
        self._mffname = filename
        self._find_files_by_type()
        self._check()

    def listdir(self) -> List[str]:
        raise NotImplementedError

    def __contains__(self, filename: str) -> bool:
        raise NotImplementedError

    def filepointer(self, basename: str) -> IO[bytes]:
        raise NotImplementedError

    def filename(self, basename: str) -> str:
        raise NotImplementedError

    def _find_files_by_type(self) -> None:
        """Reads the .mff directory and sorts filenames by extensions

        The sorted names are saved in property `files_by_type`.
        """
        self.files_by_type = defaultdict(list)
        for fbase, ext in (splitext(it) for it in self.listdir()):
            self.files_by_type[ext].append(fbase)

    def info(self, i: int=None) -> IO[bytes]:
        """return file or data info

        If `i is None`, it returns `<self.filename>/file.xml` else
        `<self.filename>/file<i>.xml`
        """
        return self.filepointer('info' + (str(i) if i else ''))

    def signals_with_info(self) -> List[SignalAndInfo]:
        ans = []
        for signalfile in self.files_by_type['.bin']:
            matches = self._re_nu.search(basename(signalfile))
            assert matches is not None, f"Something went wrong in {signalfile}"
            bin_num = int(matches.group())
            ans.append(SignalAndInfo(signal=(self.filepointer(signalfile)),
              info=('info%s' % bin_num)))

        return ans

    def _check(self):
        """Checks the .mff directory for completeness
        """
        assert splitext(self._mffname)[1] in self._extensions, self._ext_err % super().__str__()
        for signalfile in self.files_by_type['.bin']:
            if not 'signal' in signalfile:
                raise AssertionError('Unknown file "%s"' % signalfile)
            else:
                matches = self._re_nu.search(signalfile)
                assert matches is not None, f"\n            signal file {signalfile} has invalid file name"
            bin_num = int(matches.group())
            assert self.filename('info%s' % bin_num) in self, f"\n            No info found [{self.info(bin_num)}]"

    def __str__(self) -> str:
        ans = '---\n'
        ans += '# .mff directory "%s/"\n' % self._mffname
        ans += '---\n'
        ans += '## List of files\n'
        for ext, files in self.files_by_type.items():
            ans += '\n### Files of type %s\n\n' % ext
            for filename in files:
                ans += '  * %s\n' % (filename + ext)

        ans += '---'
        return ans


class MFFDirectory(MFFDirBase):
    __doc__ = 'system-level .mff directory'

    def listdir(self) -> List[str]:
        return listdir(self._mffname)

    def filepointer(self, basename: str) -> IO[bytes]:
        return open(self.filename(basename), 'rb')

    def filename(self, basename):
        for ext, files in self.files_by_type.items():
            if basename in files:
                return join(self._mffname, basename) + ext
        else:
            raise ValueError(f"No file with basename {basename}                     in directory {super().__str__()}.")

    def __contains__(self, filename: str) -> bool:
        return exists(filename)


class ZippedMFFDirectory(MFFDirBase):
    __doc__ = 'zipped .mff directory\n\n    Note: Compression on the zip file has to be 0, i.e. `ZIP_STORE`.\n    Create the zip file like\n    ```bash\n    $ zip -Z store -r -j zipped_example.mff ./example.mff\n    ```\n    '

    def __init__(self, filename):
        self.root = zipfile.ZipFile(filename)
        super().__init__(filename)

    def __del__(self):
        self.root.close()

    def listdir(self) -> List[str]:
        return self.root.namelist()

    def filepointer(self, basename: str) -> IO[bytes]:
        return self.root.open(self.filename(basename))

    def filename(self, basename):
        for ext, files in self.files_by_type.items():
            if basename in files:
                return basename + ext
        else:
            raise ValueError(f"No file with basename {basename}                     in directory {super().__str__()}.")

    def __contains__(self, filename: str) -> bool:
        return filename in self.listdir()


def get_directory(filename: str) -> MFFDirBase:
    """return either a system-level or a zipped .mff directory"""
    if not exists(filename):
        raise AssertionError(f"'{filename}' does not exist")
    else:
        if isdir(filename):
            return MFFDirectory(filename)
        if zipfile.is_zipfile(filename):
            return ZippedMFFDirectory(filename)
    raise ValueError(f"'{filename}' is likely a corrupted zip file")