# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ube/db_upgrader/tests/db_upgrader_test.py
# Compiled at: 2013-09-01 17:36:06
"""
Created on Sep 23, 2010

@author: Nicklas Boerjesson
@note: 
Oracle has a different structure, making it impossible(?) to create databases through SQL-DML.
This is difficult on DB2 as well, but
"""
import unittest
from qal.dal.dal_types import DB_POSTGRESQL, DB_MYSQL, DB_SQLSERVER, DB_DB2, DB_ORACLE
import os
from ube.db_upgrader.tests.db_staging_helper import db_staging_helper
Test_Script_Dir_abs = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
Test_Resource_Dir_abs = Test_Script_Dir_abs + '/resources/'
Test_Upgrade_XML_1 = os.path.normpath(Test_Resource_Dir_abs + 'test_upgrade_1.xml')
Test_Upgrade_XML_2 = os.path.normpath(Test_Resource_Dir_abs + 'test_upgrade_2.xml')

def handle_none(value):
    if value == None:
        return ''
    else:
        return value
        return


class Test(unittest.TestCase):
    debuglevel = 0
    helper = db_staging_helper()

    def test_upgrade_1_DB_MYSQL(self):
        self.helper.upgrade_database(DB_MYSQL, 'dbupgrd', [Test_Upgrade_XML_1, Test_Upgrade_XML_2])
        self.helper.print_and_clear_results('test_upgrade_DB_MYSQL:')

    def test_upgrade_2_DB_POSTGRESQL(self):
        self.helper.upgrade_database(DB_POSTGRESQL, 'dbupgrader', [Test_Upgrade_XML_1, Test_Upgrade_XML_2])
        self.helper.print_and_clear_results('test_upgrade_DB_POSTGRESQL:')

    def test_upgrade_3_DB_SQLSERVER(self):
        self.helper.upgrade_database(DB_SQLSERVER, 'dbupgrader', [Test_Upgrade_XML_1, Test_Upgrade_XML_2])
        self.helper.print_and_clear_results('test_upgrade_DB_SQLSERVER:')

    def test_upgrade_4_DB_DB2(self):
        self.helper.upgrade_database(DB_DB2, 'dbupgrd', [Test_Upgrade_XML_1, Test_Upgrade_XML_2])
        self.helper.print_and_clear_results('test_upgrade_DB_DB2:')

    def test_upgrade_5_DB_ORACLE(self):
        self.helper.upgrade_database(DB_ORACLE, '', [Test_Upgrade_XML_1, Test_Upgrade_XML_2])
        self.helper.print_and_clear_results('test_upgrade_DB_ORACLE:')


if __name__ == '__main__':
    unittest.main()