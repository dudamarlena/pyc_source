# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/patricia/patricia/modppi/./src/SBI/beans/File.py
# Compiled at: 2018-02-02 06:38:50
"""File

author: jbonet
date:   02/2013

@oliva's lab
"""
import os, math, gzip, warnings
from SBI.error import FileError
from SBI import SBIglobals

class File(object):
    """The File class manages certain aspects of the IO process

        File allows to seamless control some aspects about working with files.
        Namely, it will allow to:
            - work with both regular and gzipped files.
            - quickly obtain paths, file name, extension...
            - check the viability reading/writing a given file
            - avoid/ignore overwrite an existing file
            - split a file into several

        Initializing parameters
            + file_name : [M] Name of the file
            + action    : Intention.
                          Available options are (r, rb) to read and (w, wb) to write
                          @Default: 'r'
            + overwrite : On write mode, ignores if a file with the same name existed before
                          @Default: False
            @Raises FileError

        Attributes:
            > full      : Returns a full path to the file.
            > dir       : Returns the path UP TO the file.
            > lastdir   : Returns ONLY the last dir containing the file.
            > name      : Returns ONLY the file name.
            > prefix    : Returns everything EXCEPT the last extension of the file. (exclude gzip)
            > first_prefix: Returns the absolute firts part of the file
            > extension : Returns the LAST extension of the file. (exclude gzip)
            > descriptor: Opens (first call) and returns the file-descriptor
            * action    : Defines what to do with the file.
                          Available options are listed in the available_action global variable.
                          When changing the action, the file's possibilities are rechecked
                          @Raises FileError
        Booleans:
            > is_gziped : Evaluates whether the file is/has to be compressed.
                          Evaluation based SOLELY on the '.gz' termination.

        Methods:
            - close()   : Closes the filehandle
                            - clean (bool):   deletes the file if size 0.
                                    @Default: False
                          @Raises FileError

            > split()   : Splits a given file in multiple files
                            - start_separator (string):  Line startswith. Is a line to mark the line that starts the new file
                                              @Default:  None, only other parameters are considered
                            - end_separator   (string):  Line startswith. Is a line to mark the line that ends the new file
                                              @Default:  None, only other parameters are considered
                            - size            (int):     Max allowed file size. IN BYTES
                                              @Default:  1073741824 (1GB)
                            - sections        (int):     Number of sections to split file into. Overwrites 'size'
                                              @Default:  None
                            - overwrite       (bool):    Overwrite previous files of the same name
                          @Returns an array with the File object of each created file.
                          @Raises FileError
                          @Raises AttributeError if both start_separator and end_separator are defined

        Requirements:
            * os, sys, math, gzip, warnings
            < SBI.error.FileError
            < SBI.SBIglobals

        Usage:
            from SBI.beans.File import File
            newReadFile = File(file_name = 'test.txt', action = 'r')
            for line in newReadFile.descriptor:
                //DO STUFF
            newReadFile.close()
            newWriteFile = File(file_name = 'test.txt', action = 'w', overwrite = True)
            newWriteFile.write(//STUFF)
            newWriteFile.close()
    """
    write_action = set(['w', 'a', 'ar', 'wb'])
    read_action = set(['r', 'rb'])
    available_action = write_action.union(read_action)

    def __init__(self, file_name=None, action='r', overwrite=None):
        if file_name is None:
            raise FileError(0)
        self._file = file_name
        SBIglobals.alert('debug', self, ('Preparing File: {0}').format(self.full))
        self._action = None
        self._check_action(action.lower())
        self._fd = None
        self._overwrite = SBIglobals.decide_overwrite(overwrite)
        self._check_file()
        return

    @property
    def full(self):
        return os.path.abspath(self._file)

    @property
    def dir(self):
        return os.path.split(self.full)[0]

    @property
    def lastdir(self):
        return os.path.basename(self.dir)

    @property
    def name(self):
        return os.path.split(self.full)[(-1)]

    @property
    def prefix(self):
        if self.is_gziped:
            return os.path.splitext(os.path.splitext(self.name)[0])[0]
        else:
            return os.path.splitext(self.name)[0]

    @property
    def first_prefix(self):
        return self.name.split('.')[0]

    @property
    def extension(self):
        if self.is_gziped:
            return os.path.splitext(os.path.splitext(self.name)[(-1)])[(-1)]
        else:
            return os.path.splitext(self.name)[(-1)]

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, value):
        self._check_action(value.lower())
        self._check_file()

    @property
    def descriptor(self):
        if self._fd == None:
            if not self.is_gziped:
                self._fd = open(self.full, self.action)
            else:
                self._fd = gzip.open(self.full, self.action)
        return self._fd

    @property
    def is_gziped(self):
        return os.path.splitext(self.name)[(-1)] == '.gz'

    def close(self, clean=False):
        if self._fd is not None:
            self._fd.close()
            self._fd = None
            if clean and os.path.getsize(self.full) == 0:
                warnings.warn("The output file %s is empty and it's going to be deleted" % self.full)
                os.unlink(self.full)
        return

    def write(self, line):
        if self._action not in self.write_action:
            raise FileError(6)
        if self._fd is None:
            if not self.is_gziped:
                self._fd = open(self.full, self.action)
            else:
                self._fd = gzip.open(self.full, self.action)
        self._fd.write(line)
        return

    def split(self, start_separator=None, end_separator=None, size=1073741824, sections=None, overwrite=None):
        """
            > split()   : Splits a given file in multiple files
                            - start_separator (string):  Line startswith. Is a line to mark the line that starts the new file
                                              @Default:  None, only other parameters are considered
                            - end_separator   (string):  Line startswith. Is a line to mark the line that ends the new file
                                              @Default:  None, only other parameters are considered
                            - size            (int):     Max allowed file size. IN BYTES
                                              @Default:  1073741824 (1GB)
                            - sections        (int):     Number of sections to split file into. Overwrites 'size'
                                              @Default:  None
                            - overwrite       (bool):    Overwrite previous files of the same name
                          @Returns an array with the File object of each created file.
                          @Raises FileError
                          @Raises AttributeError if both start_separator and end_separator are defined
        """
        counter = 1
        newfiles = []
        if size is None and sections is None or not isinstance(size, int):
            raise FileError(5, self.__name__, 'split')
        if start_separator is not None and end_separator is not None:
            raise AttributeError('Both start and end separators can not be defined simultaniously\n')
        if sections is not None:
            size = math.ceil(os.path.getsize(self.full) / float(sections))
        else:
            sections = math.ceil(os.path.getsize(self.full) / size)
        outputfile = os.path.join(self.dir, self.prefix + '.{0:003d}' + self.extension)
        if self.is_gziped:
            outputfile += '.gz'
        overwrite = SBIglobals.decide_overwrite(overwrite)
        SBIglobals.alert('verbose', self, ('Dividing {0.full} into {1} files (aprox.)').format(self, sections))
        newfiles.append(File(file_name=outputfile.format(counter), action='w', overwrite=overwrite))
        for line in self.descriptor:
            if (start_separator is None or line.startswith(start_separator)) and os.path.getsize(newfiles[(-1)].full) >= size:
                newfiles[(-1)].close()
                counter += 1
                newfiles.append(File(file_name=outputfile.format(counter), action='w', overwrite=overwrite))
            newfiles[(-1)].write(line)
            if (end_separator is None or line.startswith(end_separator)) and os.path.getsize(newfiles[(-1)].full) >= size:
                newfiles[(-1)].close()
                counter += 1
                newfiles.append(File(file_name=outputfile.format(counter), action='w', overwrite=overwrite))

        newfiles[(-1)].close()
        self.close()
        return newfiles

    def _check_action(self, action):
        if action not in self.available_action:
            raise File(1, action, self.available_action)
        if self.is_gziped and not action.endswith('b'):
            action += 'b'
        self._action = action
        SBIglobals.alert('debug', self, ('\tAction {0} is OK...').format(self._action))

    def _check_file(self):
        if self._action.startswith('r'):
            if not os.path.isfile(self.full):
                raise FileError(3, self.full, 'noexists')
            if not os.access(self.full, os.R_OK):
                raise FileError(4, self.full, 'read')
        if self._action.startswith('w') or self._action.startswith('a'):
            if os.path.isfile(self.full):
                if not self._overwrite:
                    raise FileError(3, self.full, 'exists')
            if not os.path.isdir(self.dir):
                raise FileError(4, self.dir, 'nodir')
            if not os.access(self.dir, os.W_OK):
                raise FileError(4, self.dir, 'write')
        SBIglobals.alert('debug', self, '\tFile is OK...')

    def __repr__(self):
        return ('[{0.__class__}]: {0.full}').format(self)