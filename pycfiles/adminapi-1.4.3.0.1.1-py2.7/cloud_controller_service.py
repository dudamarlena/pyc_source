# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cloud_admin/services/cloud_controller_service.py
# Compiled at: 2018-01-31 14:44:08
from cloud_admin.services.services import EucaComponentService, SHOW_COMPONENTS

class EucaCloudControllerService(EucaComponentService):

    def show(self, print_table=True):
        return SHOW_COMPONENTS(connection=self.connection, components=self, print_table=print_table)