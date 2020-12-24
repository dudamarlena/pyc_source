# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cantools/db/shared.py
# Compiled at: 2020-04-07 04:07:19
import operator, base64, json, hashlib
from datetime import datetime
from six import string_types
modbulkers = {}
modelsubs = {}
operators = {'==': operator.__eq__, 
   '>=': operator.__ge__, 
   '<=': operator.__le__, 
   '!=': operator.__ne__, 
   '>': operator.__gt__, 
   '<': operator.__lt__}

def get_bulker(modelName):
    return modbulkers.get(modelName.lower(), None)


def reg_bulker(modelName, func):
    modbulkers[modelName.lower()] = func


def get_model(modelName):
    return modelsubs.get(modelName.lower(), None)


def get_schema(modname=None):
    if modname:
        if not isinstance(modname, string_types):
            modname = modname.__name__
        return modelsubs[modname.lower()]._schema
    s = {}
    for key, val in list(modelsubs.items()):
        if key not in ('modelbase', 'ctrefcount'):
            s[key] = val._schema

    return s


def dprep(obj, schema=None):
    schema = schema or get_schema(obj['modelName'])
    o = {}
    for key, prop in list(schema.items()):
        if key in obj:
            if prop == 'datetime' and obj[key]:
                o[key] = datetime.strptime(obj[key].replace('T', ' ').replace('Z', ''), '%Y-%m-%d %X')
            elif key != '_label':
                o[key] = obj[key]

    return o


def pad_key(compkey):
    if compkey[-3:-1] == 'CT':
        compkey = compkey[:-3] + int(compkey[(-1)]) * '='
    return compkey


def unpad_key(compkey):
    val = compkey and compkey.strip('=')
    if val != compkey:
        val += 'CT' + str(len(compkey) - len(val))
    return val


def ct_key(modelName, index):
    return unpad_key(base64.b64encode(json.dumps({'index': index, 
       'model': modelName}).encode()).decode())


def merge_schemas(bases, label=None):
    kinds = {}
    schema = {'index': 'immutable', 'key': 'key_immutable'}
    for base in bases:
        if hasattr(base, '_schema'):
            schema.update(base._schema)
            kinds.update(base._schema['_kinds'])

    schema['_kinds'] = kinds
    if label:
        schema['_label'] = label
    return schema


def hashpass(password, date):
    return hashlib.md5((password + str(date.date()).replace('-', '')).encode()).hexdigest()