# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/util/management/classmgr/PythonTypeSignatures.py
# Compiled at: 2019-11-11 07:06:07
# Size of source mod 2**32: 682 bytes
""" Class description goes here. """
import os.path
from dataclay.util.PropertiesFilesLoader import PropertyFile
__author__ = 'Alex Barcelo <alex.barcelo@bsc.es>'
__copyright__ = '2015 Barcelona Supercomputing Center (BSC-CNS)'

class PythonTypeSignatures(PropertyFile):
    __doc__ = 'Property holder for the "python_type_signatures.properties" file.'

    def __init__(self, property_path, python_type_name='python_type_signatures.properties'):
        super(PythonTypeSignatures, self).__init__(os.path.join(property_path, python_type_name))

    def _process_line(self, key, value):
        """The signatures are plain strings."""
        self.__dict__[key] = value