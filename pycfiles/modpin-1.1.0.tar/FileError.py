# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/patricia/patricia/modppi/./src/SBI/error/FileError.py
# Compiled at: 2018-02-02 06:38:50
"""FileError

author: jbonet
date:   09/2013

@oliva's lab
"""

class FileError(Exception):
    """Manages different errors produced by File when trying to Read/Write"""

    def __init__(self, code, choice=None, options=None):
        """Init. Defines kinds of error"""
        self._code = code
        self._choice = choice
        self._options = options

    def _code_to_message(self):
        """Pick and choose message"""
        if self._code == 0:
            return 'File object initialization error. A file_name must be given.'
        if self._code == 1:
            return ('The requested action {0} is not implemented.\n').format(self._choice) + ('The implemented actions are {0}.\n').format(self._options)
        if self._code == 2:
            return ('Trying to close a filehandle that was not open for file {0}\n').format(self._choice)
        if self._code == 3:
            if self._options == 'noexists':
                return ('The file {0} does not exist.\n').format(self._choice)
            if self._options == 'exists':
                return ('The file {0} already exists.\n').format(self._choice)
            if self._options == 'dirnoexists':
                return ('The dir {0} does not exist.\n').format(self._choice)
            if self._options == 'filewithname':
                return ('A file {0} already exists. Can not create directory.\n').format(self._choice)
        if self._code == 4:
            if self._options == 'read':
                return ('Unable to read {0}. No permissions.\n').format(self._choice)
            if self._options == 'write':
                return ('Unable to write in {0}. No permissions.\n').format(self._choice)
            if self._options == 'nodir':
                return ('Unable to write in {0}. Directory does not exist.\n').format(self._choice)
        if self._code == 5:
            return ('Attribute Error on object {0}, function {1}\n').format(self._choice, self._options)
        if self._code == 6:
            return "Unable to write. File not in 'write' mode.\n"

    def __str__(self):
        """Final error reply"""
        return self._code_to_message()