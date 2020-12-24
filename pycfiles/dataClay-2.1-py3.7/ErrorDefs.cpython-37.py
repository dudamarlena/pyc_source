# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/exceptions/ErrorDefs.py
# Compiled at: 2019-10-28 11:50:26
# Size of source mod 2**32: 757 bytes
""" Class description goes here. """
import os.path
from dataclay.util.PropertiesFilesLoader import PropertyFile
__author__ = 'Alex Barcelo <alex.barcelo@bsc.es>'
__copyright__ = '2015 Barcelona Supercomputing Center (BSC-CNS)'

class ErrorCodes(PropertyFile):
    __doc__ = 'Property holder for the "errorcodes.properties" file.'

    def __init__(self, property_path, error_codes_name='errorcodes.properties'):
        self.error_codes = {}
        super(ErrorCodes, self).__init__(os.path.join(property_path, error_codes_name))

    def _process_line(self, key, value):
        """The error codes are ints, and reverse lookup is useful."""
        error_code = int(value)
        self.__dict__[key] = error_code
        self.error_codes[error_code] = key