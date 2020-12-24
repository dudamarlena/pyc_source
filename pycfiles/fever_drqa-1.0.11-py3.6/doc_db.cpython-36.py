# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/drqa/retriever/doc_db.py
# Compiled at: 2019-08-29 06:03:42
# Size of source mod 2**32: 1553 bytes
"""Documents, in a sqlite database."""
import sqlite3
from . import utils
from . import DEFAULTS

class DocDB(object):
    __doc__ = 'Sqlite backed document storage.\n\n    Implements get_doc_text(doc_id).\n    '

    def __init__(self, db_path=None):
        self.path = db_path or DEFAULTS['db_path']
        self.connection = sqlite3.connect((self.path), check_same_thread=False)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def path(self):
        """Return the path to the file that backs this database."""
        return self.path

    def close(self):
        """Close the connection to the database."""
        self.connection.close()

    def get_doc_ids(self):
        """Fetch all ids of docs stored in the db."""
        cursor = self.connection.cursor()
        cursor.execute('SELECT id FROM documents')
        results = [r[0] for r in cursor.fetchall()]
        cursor.close()
        return results

    def get_doc_text(self, doc_id):
        """Fetch the raw text of the doc for 'doc_id'."""
        cursor = self.connection.cursor()
        cursor.execute('SELECT text FROM documents WHERE id = ?', (
         utils.normalize(doc_id),))
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            return result
        else:
            return result[0]