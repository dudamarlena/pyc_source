# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/readlif/utilities.py
# Compiled at: 2019-05-29 17:17:34
# Size of source mod 2**32: 822 bytes
from readlif.reader import _check_magic, _check_mem, _read_int
import xml.etree.ElementTree as ET

def get_xml(filename):
    """
    Given a lif file, returns two values (xml_root, xml_header) where
    xml_root is an ElementTree root, and xml_header is the text.

    This is useful for debugging.

    Some private functions are used from readlif.reader.

    Args:
        filename (string): what file to open?
    """
    f = open(filename, 'rb')
    _check_magic(f)
    f.seek(8)
    _check_mem(f)
    header_len = _read_int(f)
    xml_header = f.read(header_len * 2).decode('utf-16')
    xml_root = ET.fromstring(xml_header)
    f.close()
    return (xml_root, xml_header)