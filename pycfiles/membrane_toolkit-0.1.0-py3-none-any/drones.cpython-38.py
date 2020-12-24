# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/d/UNC Drive/pymemsci/membrane_toolkit/pipeline/drones.py
# Compiled at: 2020-05-10 21:44:55
# Size of source mod 2**32: 5586 bytes
"""
module containing Drones that parse file-based data
"""
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from openpyxl import load_workbook
from monty.serialization import loadfn
from maggma.core.drone import Drone, Document, RecordIdentifier
from maggma.stores import Store
from membrane_toolkit.pipeline.stores import PandasStore
DRONE_TEMPLATE_DIR = Path(__file__).absolute().parent / 'drone_templates'

class ExcelDrone(Drone):
    __doc__ = '\n    Drone that reads Excel files and creates corresponding task documents.\n    '

    def __init__(self, store, path, config):
        """
        Args:
            store: Store.
            path: Path to the directory containing the files to be parsed.
            config: dict of {key: cell reference} specifying how to parse a spreadsheet. Cell
                references should follow openpyxl syntax.
        """
        self.config = config
        super().__init__(store, path)

    def compute_record_identifier(self, record_key: str, doc_list: List[Document]) -> RecordIdentifier:
        """
        Compute meta data for this list of documents, and generate a RecordIdentifier object
        :param record_key: record keys that indicate a record
        :param doc_list: document on disk that this record include
        :return:
            RecordIdentifier that represent this doc_list
        """
        recordIdentifier = RecordIdentifier(last_updated=(datetime.now()),
          documents=doc_list,
          record_key=record_key)
        recordIdentifier.state_hash = recordIdentifier.compute_state_hash()
        return recordIdentifier

    def generate_documents(self, folder_path: Path) -> List[Document]:
        """
        Generate documents by going over the current directory:
        Note: Assumes that there's no folder in the current directory
        :param folder_path:
        :return:
        """
        file_paths = [f for f in folder_path.glob('**/*') if f.is_file()]
        return [Document(path=fp, name=(fp.name)) for fp in file_paths]

    def read(self, path: Path) -> List[RecordIdentifier]:
        """
        Given a folder path to a data folder, read all the files, and return a dictionary
        that maps each RecordKey -> [File Paths]

        ** Note: require user to implement the function computeRecordIdentifierKey

        :param path: Path object that indicate a path to a data folder
        :return:

        """
        documents = self.generate_documents(folder_path=path)
        log = dict()
        for doc in documents:
            key = self.compute_record_identifier_key(doc)
            log[key] = log.get(key, []) + [doc]
        else:
            record_identifiers = [self.compute_record_identifier(record_key, doc_list) for record_key, doc_list in log.items()]
            return record_identifiers

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
        record = dict()
        for document in recordID.documents:
            wb = load_workbook((document.path), read_only=True, data_only=True, keep_vba=False, keep_links=True)
            for sheet in wb:
                if sheet.title in self.config.keys():
                    for k2, v2 in self.config[sheet.title].items():
                        record[k2] = {}
                        if isinstance(v2, dict):
                            for k3, v3 in v2.items():
                                record[k2][k3] = wb[sheet.title][v3].value

                        else:
                            record[k2] = wb[sheet.title][v2].value
                    else:
                        wb.close()

                return record

    def compute_record_identifier_key(self, doc: Document) -> str:
        """
        Compute the recordIdentifier key by interpreting the name
        :param doc:
        :return:
        """
        return doc.name


class ExptDrone(ExcelDrone):
    __doc__ = '\n    Base class for specific Drones for a given type of experimental analysis. ExptDrones\n    automatically create a MemoryStore\n\n    Args:\n        config: Name of a .yaml file that specifies the structure of the parsed spreadsheet data.\n        path: Path to the directory containing the files to be parsed.\n    '

    def __init__(self, path, store, config):
        self.config = loadfn(DRONE_TEMPLATE_DIR / config)
        if not store:
            store = PandasStore(key='record_key')
        super().__init__(store, path, self.config)


class PermselectivityDrone(ExptDrone):
    __doc__ = '\n    Drone for parsing membrane potential data for permselectivity calculations.\n\n    Args:\n        path: Path to the directory containing the files to be parsed.\n        config: Name of a .yaml file that specifies the structure of the parsed spreadsheet data.\n    '

    def __init__(self, path, store=None, config='apparent_permselectivity.yaml'):
        super().__init__(path, store, config)