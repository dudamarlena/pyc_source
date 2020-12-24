# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/alanjds/src/git/adwords-client/adwords_client/adwordsapi/sync_job_service.py
# Compiled at: 2017-07-12 10:46:26
# Size of source mod 2**32: 624 bytes


class SyncJobService:

    def __init__(self, client):
        self.client = client
        self.services = {}

    def get_service(self, service_name):
        if service_name not in self.services:
            self.services[service_name] = globals()[service_name]
        return self.services[service_name](self.client.client)

    def mutate(self, client_id, operations_list, service_name):
        service = self.get_service(service_name)
        service.prepare_mutate()
        for i, operation in enumerate(operations_list, 1):
            service.helper.add_operation(operation)

        service.mutate(int(client_id))