# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/util/ConfigurationFlags.py
# Compiled at: 2019-10-28 11:50:26
# Size of source mod 2**32: 547 bytes
""" Class description goes here. """
from dataclay.util.PropertiesFilesLoader import PropertyFile
__author__ = 'Alex Barcelo <alex.barcelo@bsc.es>'
__copyright__ = '2015 Barcelona Supercomputing Center (BSC-CNS)'

class ConfigurationFlags(PropertyFile):
    __doc__ = 'Property holder for the "global.properties" file.'

    def __init__(self, property_path):
        super(ConfigurationFlags, self).__init__(property_path)

    def _process_line(self, key, value):
        """The signatures are plain strings."""
        self.__dict__[key] = value