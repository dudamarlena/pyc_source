# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/progtools/__init__.py
# Compiled at: 2009-10-15 11:10:49
"""Various utilities for stand-alone command-line programs."""
__author__ = 'Ross Light'
__date__ = 'February 5, 2006'
__docformat__ = 'reStructuredText'
__license__ = 'MIT'
__version__ = '0.2.2'
__all__ = [
 'command',
 'errors',
 'path',
 'program',
 'expandpath',
 'open_input_file',
 'open_output_file',
 'get_program_name',
 'status',
 'saferun',
 'catchexits',
 'reportexits',
 'StatusMixIn',
 'OptionParser',
 'UsageError']
from progtools import command
from progtools import errors
from progtools import path
from progtools import program
from progtools.errors import UsageError
from progtools.path import expandpath, open_input_file, open_output_file
from progtools.program import get_program_name, status, saferun, catchexits, reportexits, StatusMixIn, OptionParser