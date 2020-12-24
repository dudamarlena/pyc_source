# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/libreary/metadata/sqlite3.py
# Compiled at: 2020-03-19 14:48:15
# Size of source mod 2**32: 14442 bytes
import sqlite3, os, json
from typing import List
import logging
from libreary.exceptions import ResourceNotIngestedException, NoSuchMetadataFieldExeption
logger = logging.getLogger(__name__)

class SQLite3MetadataManager(object):
    __doc__ = 'docstring for SQLite3MetadataManager\n\n    SQLite3 Metadata Manager is the most basic.\n\n    It expects a SQLite3 file, formatted as described in\n    the LIBREary documentation.\n    '

    def __init__(self, config: dict):
        """
        Constructor for the MedadataManager object. This object can be created manually, but
        in most cases, it will be constructed by the LIBRE-ary main object. It expects a python dict
        :param config, which should be structured as follows:
        ```{json}
        {
        "db_file": "path to SQLite3 DB file for metadata"
        }
        ```
        """
        try:
            self.metadata_db = os.path.realpath(config.get('db_file'))
            self.conn = sqlite3.connect(self.metadata_db)
            self.cursor = self.conn.cursor()
            self.type = config.get('manager_type')
            logger.debug('Metadata Manager Configuration Valid. Creating Metadata Manager')
        except KeyError:
            logger.error('Ingester Configuration Invalid')
            raise KeyError

    def verify_db_structure(self) -> bool:
        pass

    def add_level(self, name: str, frequency: int, adapters: List[dict], copies=1) -> None:
        """
        Add a level to the metadata database.

        :param name - name for the level
        :param frequency - check frequency for level. Currently unimplemented
        :param adapters - dict object specifying adapters the level uses. Example:
            ```{json}
            [
                {
                "id": "local1",
                "type":"LocalAdapter"
                },
                {
                "id": "local2",
                "type":"LocalAdapter"
                }
            ]

            ```
        :param copies - copies to store for each adapter. Currently, only 1 is supported
        """
        logger.debug(f"Adding level {name}")
        str_adapters = json.dumps(adapters)
        self.cursor.execute('insert into levels values (?, ?, ?, ?, ?)', (
         None,
         name,
         frequency,
         str_adapters,
         copies))
        self.conn.commit()

    def delete_level--- This code section failed: ---

 L.  89         0  LOAD_GLOBAL              logger
                2  LOAD_METHOD              debug
                4  LOAD_STR                 'Deleting level '
                6  LOAD_FAST                'name'
                8  FORMAT_VALUE          0  ''
               10  BUILD_STRING_2        2 
               12  CALL_METHOD_1         1  ''
               14  POP_TOP          

 L.  90        16  LOAD_FAST                'self'
               18  LOAD_ATTR                cursor
               20  LOAD_METHOD              execute

 L.  91        22  LOAD_STR                 'delete from levels where name=?'

 L.  92        24  LOAD_FAST                'name'
               26  BUILD_TUPLE_1         1 

 L.  90        28  CALL_METHOD_2         2  ''
               30  POP_TOP          

 L.  93        32  LOAD_FAST                'self'
               34  LOAD_ATTR                conn
               36  LOAD_METHOD              commit
               38  CALL_METHOD_0         0  ''
               40  POP_TOP          

 L.  94        42  LOAD_FAST                'self'
               44  LOAD_METHOD              list_resources
               46  CALL_METHOD_0         0  ''
               48  STORE_FAST               'resources'

 L.  96        50  LOAD_FAST                'resources'
               52  GET_ITER         
               54  FOR_ITER            180  'to 180'
               56  STORE_FAST               'resource'

 L.  97        58  LOAD_FAST                'resource'
               60  LOAD_CONST               5
               62  BINARY_SUBSCR    
               64  STORE_FAST               'uuid'

 L.  98        66  SETUP_FINALLY        96  'to 96'

 L.  99        68  LOAD_FAST                'resource'
               70  LOAD_CONST               2
               72  BINARY_SUBSCR    
               74  LOAD_METHOD              split
               76  LOAD_STR                 ','
               78  CALL_METHOD_1         1  ''
               80  STORE_FAST               'levels'

 L. 100        82  LOAD_FAST                'levels'
               84  LOAD_METHOD              remove
               86  LOAD_FAST                'name'
               88  CALL_METHOD_1         1  ''
               90  POP_TOP          
               92  POP_BLOCK        
               94  JUMP_FORWARD        142  'to 142'
             96_0  COME_FROM_FINALLY    66  '66'

 L. 101        96  DUP_TOP          
               98  LOAD_GLOBAL              IndexError
              100  COMPARE_OP               exception-match
              102  POP_JUMP_IF_FALSE   118  'to 118'
              104  POP_TOP          
              106  POP_TOP          
              108  POP_TOP          

 L. 102       110  POP_EXCEPT       
              112  JUMP_BACK            54  'to 54'
              114  POP_EXCEPT       
              116  JUMP_FORWARD        142  'to 142'
            118_0  COME_FROM           102  '102'

 L. 103       118  DUP_TOP          
              120  LOAD_GLOBAL              ValueError
              122  COMPARE_OP               exception-match
              124  POP_JUMP_IF_FALSE   140  'to 140'
              126  POP_TOP          
              128  POP_TOP          
              130  POP_TOP          

 L. 104       132  POP_EXCEPT       
              134  JUMP_BACK            54  'to 54'
              136  POP_EXCEPT       
              138  JUMP_FORWARD        142  'to 142'
            140_0  COME_FROM           124  '124'
              140  END_FINALLY      
            142_0  COME_FROM           138  '138'
            142_1  COME_FROM           116  '116'
            142_2  COME_FROM            94  '94'

 L. 105       142  LOAD_GLOBAL              print
              144  LOAD_FAST                'levels'
              146  CALL_FUNCTION_1       1  ''
              148  POP_TOP          

 L. 106       150  LOAD_FAST                'self'
              152  LOAD_ATTR                cursor
              154  LOAD_METHOD              execute

 L. 107       156  LOAD_STR                 'update resources set levels=? where uuid=?'

 L. 107       158  LOAD_GLOBAL              json
              160  LOAD_METHOD              dumps
              162  LOAD_FAST                'levels'
              164  CALL_METHOD_1         1  ''
              166  LOAD_GLOBAL              str
              168  LOAD_FAST                'uuid'
              170  CALL_FUNCTION_1       1  ''
              172  BUILD_TUPLE_2         2 

 L. 106       174  CALL_METHOD_2         2  ''
              176  POP_TOP          
              178  JUMP_BACK            54  'to 54'

Parse error at or near `POP_EXCEPT' instruction at offset 114

    def ingest_to_db(self, canonical_adapter_locator: str, levels: str, filename: str, checksum: str, obj_uuid: str, description: str) -> None:
        """
        Ingest an object's metadata to the metadata database.

        :param canonical_adapter_locator - locator from the canonical adapter.
               usually something like a file path or object ID
        :param levels - list of strings, each the name of a level the object should be stored at
        :param filename - the filename of the object to be ingested
        :param checksum - the checksum of object to be ingested
        :param UUID - the UUID to be tagged with the object
        :param description - a friendly, searchable description of the object
        """
        logger.debug(f"Ingesting object {obj_uuid} with name {filename}")
        self.cursor.execute('insert into resources values (?, ?, ?, ?, ?, ?, ?)', (
         None, canonical_adapter_locator, levels, filename, checksum, obj_uuid, description))
        self.conn.commit()

    def list_resources(self) -> List[List[str]]:
        """
        Return a list of summaries of each resource. This summary includes:

        `id`, `path`, `levels`, `file name`, `checksum`, `object uuid`, `description`

        This method trusts the metadata database. There should be a separate method to
        verify the metadata db so that we know we can trust this info
        """
        return self.cursor.execute('select * from resources').fetchall()

    def get_resource_info(self, r_id: str) -> List[str]:
        """
        Get all of the resource metadata for a resource That summary includes:

        `id`, `path`, `levels`, `file name`, `checksum`, `object uuid`, `description`

        This method trusts the metadata database. There should be a separate method to
        verify the metadata db so that we know we can trust this info

        This returns metadata that's kept in the `resources` table, not the `copies` table
        """
        return self.cursor.execute('select * from resources where uuid=?', (r_id,)).fetchall()

    def delete_resource(self, r_id: str) -> None:
        """
        Delete a resource's metadata from the `resources` table

        :param r_id - the resource's uuid
        """
        self.cursor.execute('delete from resources where uuid=?', (r_id,))
        self.conn.commit()

    def minimal_test_ingest(self, locator: str, real_checksum: str, r_id: str):
        """
        Minimally ingest a resource for adapter testing

        Adapters depend on certain information in the `resources` table.

        In order for adapter manager to test adapters, it needs to have minimally ingested them.
        This testing has predefined levels, filenames, and descriptions.

        In general, I don't advise running this method yourself. Allow the adapter manager to do it.

        :param locator - locator of the copy you're testing
        :param real_checksum - object checksum
        :param r_id - r_id of test resource
        """
        self.cursor.execute('insert into resources values (?, ?, ?, ?, ?, ?, ?)', (
         None, locator, 'low,', 'libreary_test_file.txt', real_checksum, r_id, 'A resource for testing LIBREary adapters with'))
        self.conn.commit()

    def get_levels(self):
        """
        Return all configured levels
        """
        return self.cursor.execute('select * from levels').fetchall()

    def update_resource_levels(self, r_id: str, new_levels: List[str]):
        """
        Change a resource's levels

        :param r_id - resource id of resource to update
        :param new_levels - list of names of new levels
        """
        sql = 'update resources set levels = ? where uuid=?'
        self.cursor.execute(sql, (r_id, ','.join([l for l in new_levels])))
        self.conn.commit()

    def summarize_copies(self, r_id: str) -> List[List[str]]:
        """
        Get a summary of all copies of a single resource. That summary includes:

        `copy_id`, `resource_id`, `adapter_identifier`, `locator`, `checksum`, `adapter type`, `canonical (bool)`
        for each copy

        This method trusts the metadata database. There should be a separate method to
        verify the metadata db so that we know we can trust this info

        :param r_id - UUID of resource you'd like to learn about
        """
        sql = 'select * from copies where resource_id = ?'
        return self.cursor.execute(sql, (r_id,)).fetchall()

    def get_canonical_copy_metadata(self, r_id: str) -> List[List[str]]:
        """
        Get a summary of the canonical copy of an object's medatada. That summary includes:
        `copy_id`, `resource_id`, `adapter_identifier`, `locator`, `checksum`, `adapter type`, `canonical (bool)`

        :param r_id - UUID of resource you'd like to learn about
        """
        sql = 'select * from copies where resource_id = ? and canonical=1'
        return self.cursor.execute(sql, (
         r_id,)).fetchall()

    def get_copy_info(self, r_id: str, adapter_id: str):
        """
        Get a summary of a copy of an object. Can be canonical or not.

        :param r_id - object you want to learn about
        :param adapter_id - adapter storing the copy
        """
        return self.cursor.execute('select * from copies where resource_id=? and adapter_identifier=?', [
         r_id, adapter_id]).fetchall()

    def delete_copy_metadata(self, copy_id: int):
        """
        Delete object metadata for a single copy

        :param copy_id -  The copy id (not resource uuid) to delete
        """
        print(copy_id)
        self.cursor.execute('delete from copies where copy_id=?', (
         copy_id,))
        self.conn.commit()

    def add_copy(self, r_id: str, adapter_id: str, new_location: str, sha1Hashed: str, adapter_type: str, canonical: bool=False):
        """
        Add a copy of an object to the metadata database

        """
        self.cursor.execute('insert into copies values ( ?, ?, ?, ?, ?, ?, ?)', [
         None, r_id, adapter_id, new_location, sha1Hashed, adapter_type, canonical])
        self.conn.commit()

    def search(self, search_term: str):
        """
        Search the metadata db for information about resources.

        :param search_term - a string with which to search against the metadata db.
            Can match UUID, filename, original path, or description.
        """
        search_term = '%' + search_term + '%'
        return self.cursor.execute('select * from resources where name like ? or path like ? or uuid like ? or description like ?', (
         search_term, search_term, search_term, search_term)).fetchall()

    def list_object_metadata_schema--- This code section failed: ---

 L. 278         0  SETUP_FINALLY        42  'to 42'

 L. 279         2  LOAD_FAST                'self'
                4  LOAD_ATTR                cursor
                6  LOAD_METHOD              execute

 L. 280         8  LOAD_STR                 'select md_schema from object_metadata_schema where object_id=?'

 L. 280        10  LOAD_FAST                'r_id'
               12  BUILD_TUPLE_1         1 

 L. 279        14  CALL_METHOD_2         2  ''
               16  LOAD_METHOD              fetchall
               18  CALL_METHOD_0         0  ''

 L. 280        20  LOAD_CONST               0

 L. 279        22  BINARY_SUBSCR    

 L. 280        24  LOAD_CONST               0

 L. 279        26  BINARY_SUBSCR    
               28  STORE_FAST               'text_fields'

 L. 281        30  LOAD_GLOBAL              json
               32  LOAD_METHOD              loads
               34  LOAD_FAST                'text_fields'
               36  CALL_METHOD_1         1  ''
               38  POP_BLOCK        
               40  RETURN_VALUE     
             42_0  COME_FROM_FINALLY     0  '0'

 L. 282        42  DUP_TOP          
               44  LOAD_GLOBAL              IndexError
               46  COMPARE_OP               exception-match
               48  POP_JUMP_IF_FALSE    64  'to 64'
               50  POP_TOP          
               52  POP_TOP          
               54  POP_TOP          

 L. 283        56  BUILD_LIST_0          0 
               58  ROT_FOUR         
               60  POP_EXCEPT       
               62  RETURN_VALUE     
             64_0  COME_FROM            48  '48'
               64  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 52

    def set_object_metadata_schema(self, r_id: str, md_schema: str) -> None:
        """
        insert a list of all of the object metadata fields related to the object.

        These fields live in the "object_metadata_schema" table, and the related
            data lives in the "object_metadata" table

        :param r_id - object uuid for looking up
        :param md_schema - list of field names and types
        """
        md_schema_text = json.dumps(md_schema)
        self.cursor.execute('insert into object_metadata_schema values ( ?, ?, ?)', [
         None, r_id, md_schema_text])
        self.conn.commit()

    def set_object_metadata_field(self, r_id: str, field: str, value: str) -> None:
        """
        Set a single metadata field.

        These fields live in the "object_metadata_schema" table, and the related
            data lives in the "object_metadata" table

        :param r_id - object uuid for looking up
        :param md_schema - list of field names and types
        """
        try:
            list_of_fields = self.list_object_metadata_schema(r_id)
        except Exception:
            raise ResourceNotIngestedException
        else:
            if field not in list_of_fields:
                raise NoSuchMetadataFieldExeption
            self.cursor.execute('insert into object_metadata values ( ?, ?, ?, ?)', [
             None, r_id, field, value])
            self.conn.commit()

    def set_all_object_metadata(self, r_id: str, metadata: List[dict]) -> None:
        """
        Set all metadata fields.

        These fields live in the "object_metadata_schema" table, and the related
            data lives in the "object_metadata" table

        :param r_id - object uuid for looking up
        :param md_schema - list of field names and types
        """
        try:
            self.list_object_metadata_schema(r_id)
        except Exception:
            raise ResourceNotIngestedException
        else:
            for field in metadata:
                self.set_object_metadata_field(r_id, field['field'], field['value'])

    def delete_object_metadata(self, r_id: str) -> None:
        """
        Delete object metadata - remove all fields from the "object_metadata" table

        :param r_id - orbect uuid for deletion
        """
        try:
            list_of_fields = self.list_object_metadata_schema(r_id)
        except Exception:
            raise ResourceNotIngestedException
        else:
            for field in list_of_fields:
                self.delete_object_metadata_field(r_id, field)

    def delete_object_metadata_field(self, r_id: str, field: str) -> None:
        """
        Delete object metadata - remove single fields from the "object_metadata" table

        :param r_id - orbect uuid for deletion
        :param field - field to delete
        """
        self.cursor.execute('delete from object_metadata where object_id=? and key=?', (r_id, field))
        self.conn.commit()

    def delete_object_metadata_schema(self, r_id: str):
        """
        Delete object metadata schema - remove entry from the "object_metadata_schema" table

        :param r_id - orbect uuid for deletion
        """
        self.cursor.execute('delete from object_metadata_schema where object_id=?', (r_id,))
        self.conn.commit()

    def delete_object_metadata_entirely(self, r_id: str) -> None:
        """
        Delete object metadata schema and all associated metadata

        :param r_id - orbect uuid for deletion
        """
        self.delete_object_metadata(r_id)
        self.delete_object_metadata_schema(r_id)