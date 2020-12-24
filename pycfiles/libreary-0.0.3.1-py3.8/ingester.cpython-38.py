# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/libreary/ingester.py
# Compiled at: 2020-03-19 14:48:15
# Size of source mod 2**32: 5804 bytes
import os, hashlib, uuid
from typing import List
import logging
from libreary.adapter_manager import AdapterManager
from libreary.exceptions import ChecksumMismatchException
from libreary.adapters import LocalAdapter
from libreary.metadata import SQLite3MetadataManager
from libreary.exceptions import NoCopyExistsException
logger = logging.getLogger(__name__)

class Ingester:

    def __init__(self, config: dict, metadata_man: object=None):
        """
        Constructor for the Ingester object. This object can be created manually, but
        in most cases, it will be constructed by the LIBRE-ary main object. It expects a python dict
        :param config, which should be structured as follows:
        ```{json}
        {
                "metadata": {
                    "db_file": "path to SQLite3 DB file for metadata"
                },
                "adapters": # List of adapters - each entry should look like:
                [{
                    "type":"AdapterType (name of class)",
                    "id": "Adapter Identifier"
                }],
                "options": {
                    "dropbox_dir": "Path to dropbox directory, where files you want to ingest should be placed",
                    "output_dir": "Path to directory you want files to be retrieved to",
                    "config_dir": "Path to config directory"
                },
                "canonical_adapter":"Adapter Identifier for Canonical Adapter"
            }
        ```
        """
        try:
            self.config = config
            self.dropbox_dir = config['options']['dropbox_dir']
            self.canonical_adapter_id = config['canonical_adapter']
            self.canonical_adapter_type = config['canonical_adapter_type']
            self.config_dir = config['options']['config_dir']
            self.metadata_man = metadata_man
            if self.metadata_man is None:
                raise KeyError
            logger.debug('Ingester configuration valid, creating Ingester.')
        except KeyError as e:
            try:
                logger.error('Ingester Configuration Invalid')
                raise e
            finally:
                e = None
                del e

    def ingest(self, current_file_path: str, levels: List[str], description: str, delete_after_store: bool=False, metadata_schema: List=[], metadata: List=[]) -> str:
        """
        Ingest an object to LIBREary. This method:
        - Creates the canonical copy of the object
        - Creates the entry in the `resources` table describing the resource
        - Optionally, delete the file out of the dropbox dir.

        :param current_file_path -
        """
        filename = current_file_path.split('/')[(-1)]
        sha1Hash = hashlib.sha1(open(current_file_path, 'rb').read())
        checksum = sha1Hash.hexdigest()
        canonical_adapter = AdapterManager.create_adapter(self.canonical_adapter_type, self.canonical_adapter_id, self.config_dir, self.config['metadata'])
        obj_uuid = str(uuid.uuid4())
        logger.debug(f"Ingesting resource {obj_uuid} with filename {filename}")
        canonical_adapter_locator = canonical_adapter._store_canonical(current_file_path, obj_uuid, checksum, filename)
        levels = ','.join([str(l) for l in levels])
        self.metadata_man.ingest_to_db(canonical_adapter_locator, levels, filename, checksum, obj_uuid, description)
        if len(metadata_schema) == len(metadata):
            if len(metadata_schema) != 0:
                self.metadata_man.set_object_metadata_schema(obj_uuid, metadata_schema)
                self.metadata_man.set_all_object_metadata(obj_uuid, metadata)
        if delete_after_store:
            os.remove(current_file_path)
        return obj_uuid

    def verify_ingestion(self, r_id: str) -> bool:
        """
        Make sure an object has been properly ingested.

        :param r_id - the UUID of the resource you are verifying
        """
        pass

    def list_resources(self) -> List[List[str]]:
        """
        Return a list of summaries of each resource. This summary includes:

        `id`, `path`, `levels`, `file name`, `checksum`, `object uuid`, `description`

        This method trusts the metadata database. There should be a separate method to
        verify the metadata db so that we know we can trust this info
        """
        return self.metadata_man.list_resources()

    def delete_resource--- This code section failed: ---

 L. 135         0  SETUP_FINALLY        30  'to 30'

 L. 136         2  LOAD_FAST                'self'
                4  LOAD_ATTR                metadata_man
                6  LOAD_METHOD              get_resource_info
                8  LOAD_FAST                'r_id'
               10  CALL_METHOD_1         1  ''
               12  LOAD_CONST               0
               14  BINARY_SUBSCR    
               16  STORE_FAST               'resource_info'

 L. 137        18  LOAD_FAST                'resource_info'
               20  LOAD_CONST               4
               22  BINARY_SUBSCR    
               24  STORE_FAST               'canonical_checksum'
               26  POP_BLOCK        
               28  JUMP_FORWARD         66  'to 66'
             30_0  COME_FROM_FINALLY     0  '0'

 L. 138        30  DUP_TOP          
               32  LOAD_GLOBAL              IndexError
               34  COMPARE_OP               exception-match
               36  POP_JUMP_IF_FALSE    64  'to 64'
               38  POP_TOP          
               40  POP_TOP          
               42  POP_TOP          

 L. 139        44  LOAD_GLOBAL              logger
               46  LOAD_METHOD              debug
               48  LOAD_STR                 'Already deleted '
               50  LOAD_FAST                'r_id'
               52  FORMAT_VALUE          0  ''
               54  BUILD_STRING_2        2 
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          
               60  POP_EXCEPT       
               62  JUMP_FORWARD         66  'to 66'
             64_0  COME_FROM            36  '36'
               64  END_FINALLY      
             66_0  COME_FROM            62  '62'
             66_1  COME_FROM            28  '28'

 L. 141        66  LOAD_GLOBAL              AdapterManager
               68  LOAD_METHOD              create_adapter

 L. 142        70  LOAD_FAST                'self'
               72  LOAD_ATTR                canonical_adapter_type

 L. 142        74  LOAD_FAST                'self'
               76  LOAD_ATTR                canonical_adapter_id

 L. 142        78  LOAD_FAST                'self'
               80  LOAD_ATTR                config_dir

 L. 142        82  LOAD_FAST                'self'
               84  LOAD_ATTR                config
               86  LOAD_STR                 'metadata'
               88  BINARY_SUBSCR    

 L. 141        90  CALL_METHOD_4         4  ''
               92  STORE_FAST               'canonical_adapter'

 L. 144        94  SETUP_FINALLY       110  'to 110'

 L. 145        96  LOAD_FAST                'canonical_adapter'
               98  LOAD_METHOD              get_actual_checksum
              100  LOAD_FAST                'r_id'
              102  CALL_METHOD_1         1  ''
              104  STORE_FAST               'checksum'
              106  POP_BLOCK        
              108  JUMP_FORWARD        144  'to 144'
            110_0  COME_FROM_FINALLY    94  '94'

 L. 146       110  DUP_TOP          
              112  LOAD_GLOBAL              NoCopyExistsException
              114  COMPARE_OP               exception-match
              116  POP_JUMP_IF_FALSE   142  'to 142'
              118  POP_TOP          
              120  POP_TOP          
              122  POP_TOP          

 L. 147       124  LOAD_FAST                'self'
              126  LOAD_ATTR                metadata_man
              128  LOAD_METHOD              delete_resource
              130  LOAD_FAST                'r_id'
              132  CALL_METHOD_1         1  ''
              134  POP_TOP          

 L. 148       136  POP_EXCEPT       
              138  LOAD_CONST               None
              140  RETURN_VALUE     
            142_0  COME_FROM           116  '116'
              142  END_FINALLY      
            144_0  COME_FROM           108  '108'

 L. 150       144  LOAD_FAST                'checksum'
              146  LOAD_FAST                'canonical_checksum'
              148  COMPARE_OP               ==
              150  POP_JUMP_IF_FALSE   180  'to 180'

 L. 151       152  LOAD_GLOBAL              logger
              154  LOAD_METHOD              debug
              156  LOAD_STR                 'Deleting canonical copy of object '
              158  LOAD_FAST                'r_id'
              160  FORMAT_VALUE          0  ''
              162  BUILD_STRING_2        2 
              164  CALL_METHOD_1         1  ''
              166  POP_TOP          

 L. 152       168  LOAD_FAST                'canonical_adapter'
              170  LOAD_METHOD              _delete_canonical
              172  LOAD_FAST                'r_id'
              174  CALL_METHOD_1         1  ''
              176  POP_TOP          
              178  JUMP_FORWARD        184  'to 184'
            180_0  COME_FROM           150  '150'

 L. 154       180  LOAD_GLOBAL              ChecksumMismatchException
              182  RAISE_VARARGS_1       1  'exception instance'
            184_0  COME_FROM           178  '178'

 L. 156       184  LOAD_GLOBAL              logger
              186  LOAD_METHOD              debug
              188  LOAD_STR                 'Deleting object '
              190  LOAD_FAST                'r_id'
              192  FORMAT_VALUE          0  ''
              194  LOAD_STR                 ' from resources database'
              196  BUILD_STRING_3        3 
              198  CALL_METHOD_1         1  ''
              200  POP_TOP          

 L. 157       202  LOAD_FAST                'self'
              204  LOAD_ATTR                metadata_man
              206  LOAD_METHOD              delete_resource
              208  LOAD_FAST                'r_id'
              210  CALL_METHOD_1         1  ''
              212  POP_TOP          

Parse error at or near `LOAD_CONST' instruction at offset 138