# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cloud_admin/services/cloud_controller_service.py
# Compiled at: 2018-01-31 14:44:08
from cloud_admin.services.services import EucaComponentService, SHOW_COMPONENTS

class EucaCloudControllerService(EucaComponentService):

    def show(self, print_table=True):
        return SHOW_COMPONENTS(connection=self.connection, components=self, print_table=print_table)