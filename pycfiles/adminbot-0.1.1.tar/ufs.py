# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cloud_admin/services/ufs.py
# Compiled at: 2018-01-31 14:44:08
from cloud_admin.services.services import EucaComponentService, SHOW_COMPONENTS

class Ufs(EucaComponentService):

    def __init__(self, connection=None, serviceobj=None):
        super(Ufs, self).__init__(connection, serviceobj)
        if not self.child_services:
            self._get_child_services()

    def update(self, new_service=None, get_instances=True, silent=True):
        EucaComponentService.update(self, new_service=new_service, silent=silent)
        self._get_child_services()
        return self

    def show(self, print_table=True):
        return SHOW_COMPONENTS(self.connection, self, print_table)

    def _get_child_services(self):
        self.child_services = []
        for serv in self.connection.get_services(partition=self.partition):
            if serv.type != self.type:
                self.child_services.append(serv)

        return self.child_services