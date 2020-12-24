# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mbe/schema.py
# Compiled at: 2015-09-06 05:54:36
# Size of source mod 2**32: 8652 bytes
"""
Created on Mar 6, 2015

@author: Nicklas Boerjesson
@note: The schema tools

"""
from copy import deepcopy
from json.decoder import JSONArray
import os, json
from urllib.parse import urlparse
from jsonschema.validators import RefResolver
from jsonschema.exceptions import SchemaError
from mbe.misc.schema_mongodb import MongodbValidator

class SchemaTools:
    __doc__ = '\n        The schema tools class does all the handling, validation and transformation of schemas in MBE.\n    '
    json_schema_objects = None
    json_schema_folders = None
    resolver = None
    uri_handlers = None
    mongodb_validator = None

    def mbe_uri_handler(self, uri):
        """
        # TODO: Memoize.

        Handle the mbe:// namespace references

        :param uri: The uri to handle
        :return: The schema
        """
        _file_location = os.path.abspath(os.path.join(self._mbe_schema_folder, urlparse(uri).netloc))
        _schema_file = open(_file_location, 'r', encoding='utf-8')
        _json = json.loads(_schema_file.read())
        _schema_file.close()
        return _json

    def __init__(self, _json_schema_folders=[], _uri_handlers=None):
        """
        Initiate the SchemaTools class

        :param _json_schema_folders: A list of folders where schema files are stored
        :param : _uri_handlers: A dict of mbe_uri_handlers, resolves a URI prefix to a actual schema.

        """
        if not _json_schema_folders:
            _json_schema_folders = []
        if not _uri_handlers:
            self.uri_handlers = {}
        else:
            self.uri_handlers = _uri_handlers
        self.uri_handlers.update({'mbe': self.mbe_uri_handler})
        self.resolver = RefResolver(base_uri='', handlers=self.uri_handlers, referrer=None, cache_remote=True)
        self.mongodb_validator = MongodbValidator(resolver=self.resolver)
        self.json_schema_objects = {}
        self._mbe_schema_folder = os.path.join(os.path.dirname(__file__), 'schemas')
        self.load_schemas_from_directory(self._mbe_schema_folder)
        for _curr_folder in _json_schema_folders:
            self.load_schemas_from_directory(os.path.abspath(_curr_folder))

        for curr_schemaid, curr_schema in self.json_schema_objects.items():
            self.json_schema_objects[curr_schemaid] = self.resolveSchema(curr_schema)
            print('Resolved ' + str(self.json_schema_objects[curr_schemaid]))

    @staticmethod
    def check_schema_fields(_curr_schema_obj, _curr_file):
        """ Check so all mandatory fields are in the schema
        :param _curr_schema_obj: Schema to check
        :param _curr_file: File name use in error message

        """

        def raise_field_error(_collection):
            raise Exception('MongoBackend.load_schemas_from_directory: The "' + _collection + '"' + ' field is not in the schema-"' + _curr_file + '"')

        if 'collection' not in _curr_schema_obj:
            raise_field_error('collection')
        else:
            if 'schemaId' not in _curr_schema_obj:
                raise_field_error('schemaId')
            elif 'version' not in _curr_schema_obj:
                raise_field_error('version')

    def load_schema_from_file(self, _file_name):
        """
        Loads a specifield schema from a file, checks it and stores it in the schema cache.

        :param _file_name: The name of the schema file

        """
        try:
            _curr_file = open(_file_name, 'r')
        except Exception as e:
            raise Exception('load_schemas_from_directory: Error loading "' + _file_name + '": ' + str(e))

        try:
            _json_schema_obj = json.load(_curr_file)
        except Exception as e:
            raise Exception('load_schemas_from_directory: Error parsing "' + _file_name + '"' + str(e))

        _curr_file.close()
        try:
            self.check_schema_fields(_json_schema_obj, _file_name)
        except SchemaError as scherr:
            raise Exception('MongoSchema: Init, schema SchemaError in ' + _file_name + ' at path:' + str(scherr.path) + '\nMessage:\n' + str(scherr.message))
        except Exception as e:
            raise Exception('MongoSchema: Init, schema validation in ' + _file_name + ', error :' + str(e))

        self.json_schema_objects[_json_schema_obj['schemaId']] = _json_schema_obj

    def load_schemas_from_directory(self, _schema_folder):
        """
        Load and validate all schemas in a folder, add to json_schema_objects

        :param _schema_folder: Where to look

        """
        _only_files = [f for f in os.listdir(_schema_folder) if os.path.isfile(os.path.join(_schema_folder, f)) and f[-5:].lower() == '.json']
        for _file in _only_files:
            self.load_schema_from_file(os.path.join(_schema_folder, _file))

    def apply(self, _data, _schema_id=None):
        """
        Validate the JSON in _data against a JSON schema.

        :param _data: The JSON data to validate
        :param _schema_id: If set, validate against the specified schema, and not the one in the data.
        :return: the schema object that was validated against.

        """
        if _schema_id is not None:
            _json_schema_obj = self.json_schema_objects[_schema_id]
        else:
            _json_schema_obj = self.json_schema_objects[_data['schemaId']]
        self.mongodb_validator.apply(_data, _json_schema_obj)
        return (_data, _json_schema_obj)

    def validate(self, _data, _schema_id=None):
        """
        Validate the JSON in _data against a JSON schema.

        :param _data: The JSON data to validate
        :param _schema_id: If set, validate against the specified schema, and not the one in the data.
        :return: the schema object that was validated against.

        """
        if _schema_id is not None:
            _json_schema_obj = self.json_schema_objects[_schema_id]
        else:
            _json_schema_obj = self.json_schema_objects[_data['schemaId']]
        self.mongodb_validator.validate(_data, _json_schema_obj)
        return (_data, _json_schema_obj)

    def resolveSchema(self, schema):
        """
        Recursively resolve all I{$ref} JSON references in a JSON Schema.
        :param schema: A L{dict} with a JSON Schema.
        :return: The resolved JSON Schema, a L{dict}.
        """
        result = deepcopy(schema)

        def resolve(obj):
            if isinstance(obj, list):
                for item in obj:
                    resolve(item)

                return
            if isinstance(obj, dict):
                if '$ref' in obj:
                    with self.resolver.resolving(obj['$ref']) as (resolved):
                        resolve(resolved)
                        del obj['$ref']
                        obj.update(resolved)
                else:
                    for value in obj.values():
                        resolve(value)

        try:
            resolve(result)
        except Exception as e:
            raise Exception('schemaTools.resolveSchema: Error resolving schema:' + str(e) + 'Schema ' + json.dumps(schema, indent=4))

        if 'allOf' in result:
            _new_properties = {}
            for _curr_properties in result['allOf']:
                _new_properties.update(_curr_properties['properties'])

            result['properties'] = _new_properties
            del result['allOf']
        result['$schema'] = 'http://json-schema.org/draft-04/schema#'
        try:
            self.mongodb_validator.check_schema(result)
        except Exception as e:
            raise Exception('schemaTools.resolveSchema: error validating resolved schema:' + str(e) + 'Schema ' + json.dumps(result, indent=4))

        return result