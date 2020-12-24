# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/filecatalog/io.py
# Compiled at: 2008-05-16 08:54:15
"""
File Catalog Input/Output
=========================

Reading and writing of YAML files into/from a tree structure.

:copyright: 2006-2008 Jochen Kupperschmidt
:license: GNU General Public License, version 2; see LICENSE for details
"""
from __future__ import with_statement
import yaml

class DocumentProcessingError(Exception):
    """Indicating that reading, parsing or traversing the document failed."""
    pass


def load_file(filename):
    """Load tree structure from a file."""
    with open(filename, 'rb') as (f):
        try:
            data = yaml.safe_load(f)
            if not data:
                raise DocumentProcessingError('No data found.')
        except Exception, exc:
            raise DocumentProcessingError('Error reading file.')

    if not isinstance(data, dict):
        raise DocumentProcessingError('Invalid data. Expected hash/mapping/dictionary structure.')
    return data


def dump(data):
    """Dump data into a format suitable for file storage."""
    return yaml.safe_dump(data, default_flow_style=False)