# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kghose/.venvs/benten/lib/python3.7/site-packages/benten/code/schemadef.py
# Compiled at: 2019-10-10 14:53:54
# Size of source mod 2**32: 1872 bytes
from ruamel.yaml import YAML
from ruamel.yaml.parser import ParserError
from ruamel.yaml.scanner import ScannerError
from cwl.lib import resolve_file_path
fast_load = YAML(typ='safe')

def extract_schemadef(doc_uri: str, cwl: dict):
    _req = cwl.get('requirements')
    _types = []
    types_dict = {}
    if isinstance(_req, dict):
        if 'SchemaDefRequirement' in _req:
            _types = _req.get('SchemaDefRequirement', {}).get('types')
    elif isinstance(_req, list):
        for _this_req in _req:
            if isinstance(_this_req, dict) and _this_req.get('class') == 'SchemaDefRequirement':
                _types = _this_req.get('types')

    if isinstance(_types, list):
        for _type in _types:
            if isinstance(_type, dict):
                name = None
                if list(_type.keys()) == ['$import']:
                    path = _type.get('$import')
                    _type = load_typedefs_from_file(doc_uri, path)
                    if isinstance(_type, dict) and 'name' in _type:
                        name = path + '#' + _type.pop('name')
                else:
                    name = _type.pop('name', None)
                if name is not None:
                    types_dict[name] = _type

    return types_dict


def load_typedefs_from_file(doc_uri, path):
    linked_file = resolve_file_path(doc_uri, path)
    type_def = {}
    if linked_file.exists() and linked_file.is_file():
        try:
            type_def = fast_load.load(linked_file.open('r').read())
        except (ParserError, ScannerError) as e:
            try:
                type_def = {}
            finally:
                e = None
                del e

    else:
        return type_def