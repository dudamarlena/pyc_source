# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/head_controller/tests.py
# Compiled at: 2019-10-27 02:12:58
# Size of source mod 2**32: 631 bytes
import unittest
import head_controller.Camera as Camera
import head_controller.db as db
import head_controller.Features as Features
import pandas as pd, pymysql

class TestStringMethods(unittest.TestCase):

    def test_read_write(self):
        df = pd.DataFrame({'name': ['User 1', 'User 2', 'User 3']})
        db.send_df_to_table(df, 'test', operation='replace')
        con = db.get_connection()
        resp = con.cursor().execute('SELECT * FROM test').fetchall()
        con.close()
        self.assertEqual(len(resp), len([(0, 'User 1'), (1, 'User 2'), (2, 'User 3')]))


if __name__ == '__main__':
    unittest.main()