# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synthesis/writer.py
# Compiled at: 2010-08-05 11:04:07
"""XML interface for output data.  Writes out data from database and into 3 formats (HMISXMLV2.8, VendorXML, CSV ).  Other formats could be added in the future."""
from zope.interface import Interface

class Writer(Interface):
    """Interface documentation"""

    def write(input_file):
        """Method interface for writing in an output file from db"""
        pass