# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/d/Sandbox/huru-server/.venv/lib/python2.7/site-packages/data_importer/core/exceptions.py
# Compiled at: 2020-04-17 10:46:24
from __future__ import unicode_literals

class StopImporter(Exception):
    """
    Stop interator and raise error message
    """
    pass


class UnsuportedFile(Exception):
    """
    Unsuported file type
    """
    pass


class InvalidModel(Exception):
    """
    Invalid model in descriptor
    """
    pass


class InvalidDescriptor(Exception):
    """
    Invalid Descriptor File
    Descriptor must be one valid JSON
    """
    pass