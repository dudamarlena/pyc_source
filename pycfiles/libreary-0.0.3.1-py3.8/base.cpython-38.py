# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/libreary/metadata/base.py
# Compiled at: 2020-03-19 14:48:15
# Size of source mod 2**32: 1604 bytes
from typing import List

class BaseMetadataManager(object):
    __doc__ = 'docstring for BaseMetadataManager\n\n    This object contains the following methods:\n\n    - verify_db_structure\n\n    '

    def __init__(self, config: dict):
        pass

    def verify_db_structure(self) -> bool:
        pass

    def add_level(self, name: str, frequency: int, adapters: List[dict], copies=1) -> None:
        pass

    def ingest_to_db(self, canonical_adapter_locator: str, levels: List[str], filename: str, checksum: str, obj_uuid: str, description: str) -> None:
        pass

    def list_resources(self) -> List[List[str]]:
        pass

    def get_resource_info(self, r_id: str) -> List[str]:
        pass

    def delete_resource(self, r_id: str) -> None:
        pass

    def minimal_test_ingest(self, locator: str, real_checksum: str, r_id: str):
        pass

    def get_levels(self):
        pass

    def update_resource_levels(self, r_id: str, new_levels: List[str]):
        pass

    def summarize_copies(self, r_id: str) -> List[List[str]]:
        pass

    def get_canonical_copy_metadata(self, r_id: str) -> List[List[str]]:
        pass

    def get_copy_info(self, r_id: str, adapter_id: str, canonical: bool=False):
        pass

    def delete_copy_metadata(self, copy_id: str):
        pass

    def add_copy(self, r_id: str, adapter_id: str, new_location: str, sha1Hashed: str, adapter_type: str, canonical: bool=False):
        pass

    def search(self, search_term: str) -> List[List[str]]:
        pass