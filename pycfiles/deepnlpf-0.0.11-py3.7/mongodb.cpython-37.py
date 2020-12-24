# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/deepnlpf/models/mongodb.py
# Compiled at: 2020-03-16 10:43:28
# Size of source mod 2**32: 2364 bytes


class DataBase(object):
    __doc__ = '\n        Description:\n    '

    def __init__(self):
        from deepnlpf.helpers.mongodb import ConnectMongoDB
        self.db = ConnectMongoDB()

    def save(self, document):
        """
            @param document
        """
        db_response = self.db.insert_document('dataset', document)
        db_response = {'dataset': {'_id': db_response}}
        return db_response

    def select(self, key):
        """
            @param key
        """
        db_response = self.db.select_document('dataset', key)
        if db_response:
            return db_response
        return db_response

    def select_all(self):
        db_response = self.db.select_document_all('dataset')
        if db_response:
            return db_response
        return db_response

    def update(self, key, document):
        db_response = self.db.update('dataset', key, document)
        if db_response:
            return 'Dataset Successfully Updated!'
        return 'Dataset Update Error!'

    def delete(self, key):
        _key = {'_id': ObjectId(key)}
        db_response = self.db.delete('dataset', _key)
        if db_response.deleted_count == 1:
            return {'dataset': {'delete': True}}
        return {'dataset': {'delete': False}}

    def save_analysis(self, tool, document):
        """
            @param document
        """
        if self.db.insert_document('analysis', document):
            return tool + ': Analysis successfully added!'
        return tool + ': Error adding analysis!'

    def select_analysis(self, _id_dataset):
        """
            @param _id_dataset
        """
        db_response = self.db.select_document_all_key('analysis', _id_dataset)
        if db_response:
            return db_response
        return db_response

    def save_statistics(self, document):
        """
            @param document
        """
        db_response = self.db.insert_document('statistics', document)
        db_response = {'statistics': {'_id': db_response}}
        return db_response

    def select_statistics(self, key):
        """
            @param key
        """
        return self.db.select_document('statistics', key)