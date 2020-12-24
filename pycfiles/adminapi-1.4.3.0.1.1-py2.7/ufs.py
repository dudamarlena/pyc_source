# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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