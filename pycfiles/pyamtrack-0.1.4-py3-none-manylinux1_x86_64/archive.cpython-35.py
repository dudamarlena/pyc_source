# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_file/interfaces/archive.py
# Compiled at: 2019-12-19 10:46:04
# Size of source mod 2**32: 997 bytes
__doc__ = 'PyAMS_file.interfaces.archive module\n\nThis module provides a single helper interface to handle archives.\n'
from zope.interface import Interface
__docformat__ = 'restructuredtext'

class IArchiveExtractor(Interface):
    """IArchiveExtractor"""

    def initialize(self, data, mode='r'):
        """Initialize extractor for given data"""
        pass

    def get_contents(self):
        """Get iterator over archive contents

        Each iteration is a tuple containing data and file name.
        """
        pass