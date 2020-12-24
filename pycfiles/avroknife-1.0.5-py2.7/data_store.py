# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mafju/current/icm/removing_madis_from_code/avroknife/avroknife/data_store.py
# Compiled at: 2015-09-04 08:27:04
import fnmatch, avro
from avro.datafile import DataFileReader
from avro.io import DatumReader, SchemaResolutionException
from collections import OrderedDict
from avroknife.error import error

class _FieldsOrderPreservingDatumReader(DatumReader):
    """DatumReader that preserves the order of the fields as defined in schema. 
    
    This is a "hacked" version of the DatumReader class available in Avro 1.7.5
    in package `io`. The only difference is that the `read_record` variable
    is defined as `OrderedDict` object instead of `dict`.
    """

    def read_record(self, writers_schema, readers_schema, decoder):
        readers_fields_dict = readers_schema.fields_dict
        read_record = OrderedDict()
        for field in writers_schema.fields:
            readers_field = readers_fields_dict.get(field.name)
            if readers_field is not None:
                field_val = self.read_data(field.type, readers_field.type, decoder)
                read_record[field.name] = field_val
            else:
                self.skip_data(field.type, decoder)

        if len(readers_fields_dict) > len(read_record):
            writers_fields_dict = writers_schema.fields_dict
            for field_name, field in readers_fields_dict.items():
                if not writers_fields_dict.has_key(field_name):
                    if field.has_default:
                        field_val = self._read_default_value(field.type, field.default)
                        read_record[field.name] = field_val
                    else:
                        fail_msg = 'No default value for field %s' % field_name
                        raise SchemaResolutionException(fail_msg, writers_schema, readers_schema)

        return read_record


class DataStore:
    """Avro data store.
    
    Avro data store is a directory with many Avro files where each one has the
    same schema. All these files are treated as if they were a single,
    concatenated Avro file. They are virtually "concatenated" along with the
    increasing order of the paths to these files.
    """

    def __init__(self, datastore_path, schema_path=None):
        """
        Args:
            datastore_path: a FileSystemPath object. Path to a directory 
                containing Avro files, all of them need to have the same schema.
            schema_path: a FileSystemPath object. Path to file containing
                JSON Avro reader schema.
        """
        self._datastore_path = datastore_path
        self._schema_path = schema_path
        self._schema = None
        return

    def get_schema(self):
        """Lazy accessor for data store schema

        If schema is given as a run parameter, then returns this schema.
        Otherwise extracts the schema from the Avro data store files.
        """
        if self._schema:
            return self._schema
        if not self._schema_path:
            paths = self.__get_paths_to_avro_files()
            with DataFileReader(paths[0].open('r'), _FieldsOrderPreservingDatumReader()) as (reader):
                self._schema = avro.schema.parse(reader.get_meta('avro.schema'))
                return self._schema
        else:
            try:
                self._schema = avro.schema.parse(self._schema_path.open('r').read())
                return self._schema
            except TypeError:
                error('supplied schema cannot be parsed!')
                raise

    def __iter__(self):
        paths = self.__get_paths_to_avro_files()
        prev_global_record_index = 0
        for path in paths:
            with DataFileReader(path.open('r'), _FieldsOrderPreservingDatumReader(readers_schema=self.get_schema())) as (reader):
                prev_local_record_index = 0
                try:
                    for record in reader:
                        yield record
                        prev_global_record_index = prev_global_record_index + 1
                        prev_local_record_index = prev_local_record_index + 1

                except Exception:
                    error(('processing record with index {} failed. This record comes from "{}" Avro file and in this file it has local index equal {}.').format(prev_global_record_index + 1, path, prev_local_record_index + 1))
                    raise

    def __get_paths_to_avro_files(self):
        paths = []
        for file_name in self._datastore_path.ls():
            if not (fnmatch.fnmatch(file_name, '_*') or fnmatch.fnmatch(file_name, '.*')):
                path = self._datastore_path.append(file_name)
                paths.append(path)

        if len(paths) == 0:
            raise error('Specified data store path is empty or is not valid')
        paths.sort()
        return paths