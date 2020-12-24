# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/scheduler/zodb.py
# Compiled at: 2012-10-22 06:18:07
__docformat__ = 'restructuredtext'
from ztfy.scheduler.interfaces import IZODBPackingTask
from ztfy.utils.interfaces import IZEOConnection
from zope.component import queryUtility
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from ztfy.scheduler.task import BaseTask

class ZODBPackingTask(BaseTask):
    """ZODB packing task"""
    implements(IZODBPackingTask)
    zeo_connection = FieldProperty(IZODBPackingTask['zeo_connection'])
    pack_time = FieldProperty(IZODBPackingTask['pack_time'])

    def run(self, report):
        zeo_connection = queryUtility(IZEOConnection, self.zeo_connection)
        if zeo_connection is None:
            report.write('No ZEO connection. Task aborted.')
            return
        else:
            report.write('ZEO connection name = %s\n' % self.zeo_connection)
            report.write('Packing transactions older than %d days\n' % self.pack_time)
            storage, db = zeo_connection.getConnection(get_storage=True)
            try:
                db.pack(days=self.pack_time)
                report.write('\nPack successful.\n')
            finally:
                storage.close()

            return