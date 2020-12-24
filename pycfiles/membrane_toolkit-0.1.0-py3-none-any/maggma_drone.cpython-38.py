# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/d/UNC Drive/pymemsci/membrane_toolkit/pipeline/maggma_drone.py
# Compiled at: 2020-04-26 20:17:56
# Size of source mod 2**32: 7748 bytes
"""
Temporary file for abstract Drone class that will eventually be part of maggma.

See https://github.com/wuxiaohua1011/mp_update_project/blob/9250b115740c9ae6e95629d8835f8268f09bee19/drone.py
"""
from pydantic import BaseModel, Field
from pathlib import PosixPath, Path
from datetime import datetime
from typing import Dict, List, Optional, Iterable
import hashlib
from abc import abstractmethod
import os.path
from maggma.core import Builder

class Document(BaseModel):
    __doc__ = '\n    Represent a file\n    '
    path = Field(..., title='Path of this file')
    path: PosixPath
    name = Field(..., title='File name')
    name: str


class RecordIdentifier(BaseModel):
    __doc__ = '\n    The meta data for a record\n    '
    last_updated = Field(...,
      title='The time in which this record is last updated')
    last_updated: datetime
    documents = Field([], title='List of documents this RecordIdentifier indicate')
    documents: List[Document]
    record_key = Field(...,
      title='Hash that uniquely define this record, can be inferred from each document inside')
    record_key: str
    state_hash = Field(None,
      title='Hash of the state of the documents in this Record')
    state_hash: Optional[str]

    @property
    def parent_directory(self) -> Path:
        """
        root most directory that documnents in this record share
        :return:
        """
        paths = [doc.path.as_posix() for doc in self.documents]
        return Path(os.path.commonprefix(paths))

    def compute_state_hash(self) -> str:
        """
        compute the hash of the state of the documents in this record
        :param doc_list: list of documents
        :return:
            hash of the list of documents passed in
        """
        digest = hashlib.md5()
        for doc in self.documents:
            digest.update(doc.name.encode())
            with open(doc.path.as_posix(), 'rb') as (file):
                buf = file.read()
                digest.update(buf)
        else:
            return str(digest.hexdigest())


class Drone(Builder):
    __doc__ = "\n    An abstract drone that handles operations with database, using Builder to support multi-threadding\n    User have to implement all abstract methods to specify the data that they want to use to interact with this class\n\n    Note: All embarrassingly parallel function should be in process_items\n    Note: The steps of a Drone can be divided into roughly 5 steps\n    - Step 1(readRecord):\n        - Crawl through Path of the folder where data live (User has to implement the crawling function)\n            - it will return Record of  (Already in method 2)\n                (cite.bibtex, data.txt)\n                (cite2.bibtex, text-2.txt)\n                (citations-3.bibtex, ) ...\n     - Step 2: Takes a list of Record (from the result above), and return a list of Record that needs to be\n                updated by querying the database\n        - If you've seen it before and the raw data has changed --> return True\n        - If you never seen it before --> return True\n        - Otherwise --> return False\n     - Step 3: Process the Record (convert the Record into MongoDB data) (abstract function) (Parallel function\n                implemented in process_item)\n     - Step 4: Inject back the meta data to see if the Record if needed to be updated\n     - Step 5: Inject into the data base\n\n     For sample usage, please see simpleBibDrone.py\n    "

    def __init__(self, store, path):
        self.store = store
        self.path = path
        super().__init__(sources=[], targets=store)

    @abstractmethod
    def compute_record_identifier_key(self, doc: Document) -> str:
        """
        Compute the RecordIdentifier key that this document correspond to
        :param doc: document which the record identifier key will be inferred from
        :return:
            RecordIdentifiierKey
        """
        raise NotImplementedError

    @abstractmethod
    def read(self, path: Path) -> List[RecordIdentifier]:
        """
        Given a folder path to a data folder, read all the files, and return a dictionary
        that maps each RecordKey -> [File Paths]

        ** Note: require user to implement the function computeRecordIdentifierKey

        :param path: Path object that indicate a path to a data folder
        :return:

        """
        raise NotImplementedError

    @abstractmethod
    def compute_data(self, recordID: RecordIdentifier) -> Dict:
        """
        User can specify what raw data they want to save from the Documents that this recordID refers to

        :param recordID: recordID that needs to be re-saved
        :return:
            Dictionary of NAME_OF_DATA -> DATA
            ex:
                for a recordID refering to 1,
                {
                    "citation": cite.bibtex ,
                    "text": data.txt
                }

        """
        raise NotImplementedError

    def should_update_records(self, record_identifiers: List[RecordIdentifier]) -> List[RecordIdentifier]:
        """
        Batch query database by computing all the keys and send them at once
        :param record_identifiers: all the record_identifiers that need to fetch from database
        :return:
            boolean mask of whether the record_identifier at that index require update
        """
        cursor = self.store.query(criteria={'record_key': {'$in': [r.record_key for r in record_identifiers]}},
          properties=[
         'record_key', 'state_hash', 'last_updated'])
        not_exists = object()
        db_record_log = {doc['state_hash']:doc['record_key'] for doc in cursor}
        to_update_list = [recordID.state_hash != db_record_log.get(recordID.record_key, not_exists) for recordID in record_identifiers]
        return [recordID for recordID, to_update in zip(record_identifiers, to_update_list) if to_update]

    def assimilate(self, path: Path) -> List[RecordIdentifier]:
        """
        Function mainly for debugging purpose. It will
        1. read file in the path specified
        2. convert them into recordIdentifier
        3. return the converted recordIdentifiers

        :param path: path in which files are read
        :return:
            list of record Identifiers
        """
        record_identifiers = self.read(path=path)
        return record_identifiers

    def get_items(self) -> Iterable:
        self.logger.debug('Starting get_items in {} Builder'.format(self.__class__.__name__))
        record_identifiers = self.read(path=(self.path))
        records_to_update = self.should_update_records(record_identifiers)
        return records_to_update

    def update_targets(self, items: List):
        """
        Receive a list of items to update, update the items

        Assume that each item are in the correct format

        :param items: List of items to update
        :return:
            None
        """
        if len(items) > 0:
            self.logger.debug('Updating {} items'.format(len(items)))
            self.store.update(items)
        else:
            self.logger.debug('There are no items to update')

    def process_item(self, item: RecordIdentifier) -> Dict:
        """
        compute the item to update

        :param item: item to update
        :return:
            result from expanding the item
        """
        return {**(self.compute_data(recordID=item)), **(item.dict())}