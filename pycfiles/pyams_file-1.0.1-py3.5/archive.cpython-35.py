# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_file/interfaces/archive.py
# Compiled at: 2019-12-19 10:46:04
# Size of source mod 2**32: 997 bytes
"""PyAMS_file.interfaces.archive module

This module provides a single helper interface to handle archives.
"""
from zope.interface import Interface
__docformat__ = 'restructuredtext'

class IArchiveExtractor(Interface):
    __doc__ = 'Archive contents extractor'

    def initialize(self, data, mode='r'):
        """Initialize extractor for given data"""
        pass

    def get_contents(self):
        """Get iterator over archive contents

        Each iteration is a tuple containing data and file name.
        """
        pass