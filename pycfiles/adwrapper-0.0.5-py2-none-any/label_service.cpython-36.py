# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/alanjds/src/git/adwords-client/adwords_client/adwordsapi/label_service.py
# Compiled at: 2017-07-12 10:46:26
# Size of source mod 2**32: 703 bytes
from . import common as cm

class LabelServiceOperations:

    def __init__(self, label_service):
        self.label_service = label_service
        self.suds_client = label_service.service.suds_client
        self.operations = []

    def add_operation(self, operation):
        self.operations.append(operation)

    def upload_operations(self):
        raise NotImplementedError()


class LabelService(cm.BaseService):

    def __init__(self, client):
        super().__init__(client, 'LabelService')

    def prepare_mutate(self):
        self.helper = LabelServiceOperations(self)
        self.ResultProcessor = cm.SimpleReturnValue