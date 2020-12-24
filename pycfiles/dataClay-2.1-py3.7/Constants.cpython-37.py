# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/util/Constants.py
# Compiled at: 2019-11-11 07:06:07
# Size of source mod 2**32: 831 bytes
""" Class description goes here. """
from dataclay.exceptions.ErrorDefs import ErrorCodes
import dataclay.util.management.classmgr.PythonTypeSignatures as PythonTypeSignatures
from . import properties
__author__ = 'Alex Barcelo <alex.barcelo@bsc.es>'
__copyright__ = '2015 Barcelona Supercomputing Center (BSC-CNS)'
PROPERTIES_DIR = properties.__path__[0]
global_properties = PythonTypeSignatures(PROPERTIES_DIR)
error_codes = ErrorCodes(PROPERTIES_DIR)