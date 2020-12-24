# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fever/reader/document_database.py
# Compiled at: 2019-01-25 08:19:53
# Size of source mod 2**32: 1567 bytes
import logging, sqlite3, unicodedata
from allennlp.common.file_utils import cached_path

class FEVERDocumentDatabase(object):

    def __init__(self, path: str):
        self._connection = self.connect(cached_path(path))

    @staticmethod
    def connect(path: str):
        try:
            return sqlite3.connect(path, check_same_thread=False)
        except sqlite3.Error as e:
            logging.exception(e)
            logging.critical('Unable to load sqlite database')
            raise e

    def get_doc_lines(self, page_title: str) -> str:
        cursor = self._connection.cursor()
        cursor.execute('SELECT lines FROM documents WHERE id = :page_title', {'page_title': unicodedata.normalize('NFD', page_title)})
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            raise Exception('Document not found')
        return result[0].split('\n')

    def get_doc_ids(self):
        cursor = self._connection.cursor()
        cursor.execute('SELECT id FROM documents')
        results = [result[0] for result in cursor.fetchall()]
        cursor.close()
        return results

    def get_non_empty_doc_ids(self):
        cursor = self._connection.cursor()
        cursor.execute('SELECT id FROM documents WHERE length(trim(text)) > 0')
        results = [r[0] for r in cursor.fetchall()]
        cursor.close()
        return results