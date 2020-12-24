# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synthesis/reader.py
# Compiled at: 2011-01-03 14:39:55
"""Parser interface for input data.  Reads in data from wire formats and stores them persistently."""
from zope.interface import Interface

class Reader(Interface):
    """Interface documentation"""

    def read(self, input_file):
        """Method interface for reading in an input file to memory"""
        pass

    def process_data(self):
        """Method interface for processing, translating and storing        data read into memory by reader()"""
        pass