# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pyjon/versionning/sqlalchemy.py
# Compiled at: 2010-10-04 09:20:30
from pyjon.versionning.base import Repository

class SARepository(Repository):

    def __init__(self, repo_folder, dbsession, object_classes, default_user='process'):
        self.dbsession = dbsession
        self.object_classes = object_classes
        super(SARepository, self).__init__(repo_folder, default_user=default_user)

    def get_all_objects(self):
        for objcls in self.object_classes:
            for item in self.dbsession.query(objcls):
                yield item

    def send_object_change(self, item):
        self.dbsession.add(item)
        self.dbsession.flush()