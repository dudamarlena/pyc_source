# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-1.7.35-i686/egg/seedbox/tests/db/test_maintenance.py
# Compiled at: 2015-06-14 13:30:57
import glob, os, six.moves.urllib.parse as urlparse
from seedbox import db
from seedbox.db import maintenance
from seedbox.tests import test

class DbMaintenanceTest(test.ConfiguredBaseTestCase):

    def setUp(self):
        super(DbMaintenanceTest, self).setUp()
        db.dbapi(self.CONF)

    def test_backup_database(self):
        db_name = urlparse.urlparse(self.CONF.database.connection).path.replace('//', '/')
        for cnt in range(0, 15):
            if cnt == 0:
                self.assertEqual(len(glob.glob(db_name + '*')), 1)
            elif 1 <= cnt <= 8:
                self.assertEqual(len(glob.glob(db_name + '*')), 1 + cnt)
            else:
                self.assertEqual(len(glob.glob(db_name + '*')), 9)
            maintenance.backup(self.CONF)

        if os.path.exists(db_name):
            os.remove(db_name)
        maintenance.backup(self.CONF)