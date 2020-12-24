# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyjon/descriptors/tests/test_utils.py
# Compiled at: 2015-01-20 10:15:48
import six
from xml.etree import cElementTree as ET
from pyjon.descriptors import Descriptor
basetestdir = 'pyjon/descriptors/tests/'

def get_descriptor(xml_schemafile, encoding, buffersize=16384):
    """helper function to construct a descriptor instance from
    a schema file to help test implementations

    @param xml_schemafile: the filename that contains the xml schema
    that should normally be in the database but is in a static file
    for test purposes
    @type xml_schemafile: string object (unicode on Python 2)

    @param encoding: the encoding of the stream to read (ie: 'utf-8')
    @type encoding: string

    @param buffersize: the size of the buffer in bytes for the read operation.
    This will be used by the readers that perform buffering themselves
    @type buffersize: int
    """
    payload_tree = ET.parse(xml_schemafile)
    return Descriptor(payload_tree, encoding, buffersize=buffersize)


def open_file(path, flags):
    """Open the specified file. Compatible with Python 2 & 3: the "b" flag has
    more meanings in Python 3; the "newline" parameter doesn't exist in Python
    2.
    """
    if flags and 'b' in flags:
        return open(path, flags)
    if six.PY2:
        return open(path, flags + 'b')
    return open(path, flags, newline='')