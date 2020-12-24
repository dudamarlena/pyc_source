# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/opentargets_validator/helpers.py
# Compiled at: 2020-01-16 04:41:30
from __future__ import unicode_literals
from builtins import object
import logging, requests, jsonschema as jss, pkg_resources as res, simplejson as json, os, rfc3987, opentargets_validator
from collections import OrderedDict
import hashlib

def file_handler(uri):
    schema = None
    uri_split = rfc3987.parse(uri)
    with open(os.path.abspath(os.path.join(uri_split[b'authority'], uri_split[b'path'])), b'r') as (schema_file):
        schema = json.load(schema_file)
    return schema


def generate_validator_from_schema(schema_uri):
    schema = None
    uri_split = rfc3987.parse(schema_uri)
    if uri_split[b'scheme'] in ('http', 'https'):
        schema = requests.get(schema_uri).json()
    elif uri_split[b'scheme'] == b'file':
        with open(os.path.abspath(os.path.join(uri_split[b'authority'], uri_split[b'path'])), b'r') as (schema_file):
            schema = json.load(schema_file)
    else:
        raise ValueError(b'schema uri must have file or url scheme')
    handlers = dict(file=file_handler)
    resolver = jss.RefResolver(schema_uri, schema, handlers=handlers, store={})
    validator = jss.Draft7Validator(schema=schema, resolver=resolver)
    return validator


def file_or_resource(fname=None):
    """get filename and check if in getcwd then get from
    the package resources folder
    """
    if fname is not None:
        filename = os.path.expanduser(fname)
        resource_package = opentargets_validator.__name__
        resource_path = os.path.sep.join((b'resources', filename))
        abs_filename = (os.path.isabs(filename) or os.path.join)(os.path.abspath(os.getcwd()), filename) if 1 else filename
        if os.path.isfile(abs_filename):
            return abs_filename
        return res.resource_filename(resource_package, resource_path)
    else:
        return