# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/tests/plugins/test_persistence.py
# Compiled at: 2020-01-25 09:04:28
# Size of source mod 2**32: 1956 bytes
import unittest, logging, os, asyncio, sqlite3
from hbmqtt.plugins.manager import BaseContext
from hbmqtt.plugins.persistence import SQLitePlugin
formatter = '[%(asctime)s] %(name)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s'
logging.basicConfig(level=(logging.DEBUG), format=formatter)

class TestSQLitePlugin(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()

    def test_create_tables(self):
        dbfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test.db')
        context = BaseContext()
        context.logger = logging.getLogger(__name__)
        context.config = {'persistence': {'file': dbfile}}
        SQLitePlugin(context)
        conn = sqlite3.connect(dbfile)
        cursor = conn.cursor()
        rows = cursor.execute("SELECT name FROM sqlite_master where type = 'table'")
        tables = []
        for row in rows:
            tables.append(row[0])
        else:
            self.assertIn('session', tables)