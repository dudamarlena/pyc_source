# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/of/schemas/validation.py
# Compiled at: 2016-12-01 18:02:10
# Size of source mod 2**32: 1594 bytes
"""
This module holds Optimal Framework-specific JSON schema functionality

Created on Jan 22, 2016

@author: Nicklas Boerjesson
"""
import json, os
from urllib.parse import urlparse
__author__ = 'Nicklas Borjesson'
script_dir = os.path.dirname(os.path.abspath(__file__))

def general_uri_handler(_uri, _folder):
    """
    This function looks up a JSON schema that matches the URL in the given folder
    :param _uri: The _uri to handle
    :return: The schema
    """
    _netloc = urlparse(_uri).netloc
    _filename = _netloc.replace('.', '/')
    _file_location = os.path.abspath(os.path.join(_folder, 'namespaces', _filename + '.json'))
    with open(_file_location, 'r', encoding='utf-8') as (_schema_file):
        _json = json.load(_schema_file)
    return _json


def of_uri_handler(_uri):
    """
    This function is given as call back to JSON schema tools to handle the of:// namespace references
    :param _uri:
    :return: The schema
    """
    return general_uri_handler(_uri, script_dir)


def of_schema_folder():
    return os.path.join(script_dir, 'namespaces')


def parse_name_parts(_import):
    """
    Parses a string of the namespace.namespace.localname structure and returns a tuple with the namespace and the local name.
    :param _import: The string to parse
    :return: a tuple with the namespace and the local name
    """
    _scheme, _netloc, _path = urlparse(_import).netloc.split('.')