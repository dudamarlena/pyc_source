# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mafju/current/icm/removing_madis_from_code/avroknife/avroknife/utils.py
# Compiled at: 2015-09-04 08:27:04
import json, base64, os, errno
from collections import OrderedDict

def to_byte_string(obj):
    """
    Converts an object into to a Python byte string
    """
    if isinstance(obj, unicode):
        return obj.encode('utf-8')
    else:
        return str(obj)


class EncapsulatedString:

    def __init__(self, string):
        self.string = string


def encapsulate_strings(python_object):
    """Converts every Python string (_not_ Unicode) to an EncapsulatedString

    Avro DataFileReader yields binary data as a Python string. To be able to jsonify it
    with a custom function we need to convert all strings to an object not understood by
    the JSON encoder. This is a kind of a hack, but on the same time the only solution found
    """
    if isinstance(python_object, str):
        return EncapsulatedString(python_object)
    if isinstance(python_object, list):
        return [ encapsulate_strings(e) for e in python_object ]
    if isinstance(python_object, OrderedDict):
        new_dict = OrderedDict()
        for k, v in python_object.iteritems():
            new_dict[k] = encapsulate_strings(v)

        return new_dict
    if isinstance(python_object, dict):
        return {k:encapsulate_strings(v) for k, v in python_object.iteritems()}
    return python_object


class _AvroJSONEncoder(json.JSONEncoder):
    """Custom JSON dumping class for correct handling of Avro bytes fields"""

    def default(self, python_object):
        """Serializes binary data which is otherwise impossible to dump as JSON"""
        if isinstance(python_object, EncapsulatedString):
            return base64.b64encode(python_object.string)
        else:
            return super(_AvroJSONEncoder, self).default(python_object)


def dict_to_json(python_dict, pretty_print=False):
    """Dumps a Python dictionary to JSON format

    Args:
        python_dict: a Python dictionary containing Avro data_store
    Returns:
        A string being a valid JSON with binary data encoded with Base64
    """
    if pretty_print:
        return _AvroJSONEncoder(indent=4).encode(python_dict)
    else:
        return _AvroJSONEncoder().encode(python_dict)


class FileAlreadyExistsException(Exception):

    def __init__(self, message):
        Exception.__init__(self, message)