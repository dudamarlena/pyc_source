# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mcfletch/pylive/table/pytable/tests/test_datatypedetermination.py
# Compiled at: 2004-08-27 02:11:56
from pytable.schemabuilder import *
from pytable import dbschema, sqlgeneration, sqlquery, dbspecifier, specifierfromoptions
import unittest, new, traceback
testSpec = specifierfromoptions.specifierFromOptions()
cats = database('kitties', tables=[
 table('cats', (
  field('cat_id', 'integer', 0, 'Unique cat identifier', constraints=(notNull(), primary())), field('cat_name', 'varchar', 255, "The cat's name", constraints=(notNull(),)), field('declawed', 'bool', 0, "Poor lil' kitty")), 'Primary table for storing critical info about cats', defaultRecords=[{'cat_id': 0, 'cat_name': 'Felix', 'declawed': 't'}, {'cat_id': 1, 'cat_name': 'Ginger', 'declawed': 'f'}, {'cat_id': 2, 'cat_name': 'Robusta', 'declawed': 't'}])])
cats.resolve()
items = []

class CatsTest(unittest.TestCase):
    __module__ = __name__
    specifier = testSpec

    def setUp(self):
        (self.driver, self.connection) = self.specifier.connect()
        cursor = self.connection.cursor()
        generator = sqlgeneration.SQLDropStatements(self.driver)
        schema = cats.lookupName('cats')
        query = sqlquery.SQLQuery(sql=generator(schema), debug=1)
        try:
            query(cursor=cursor)
        except Exception, err:
            print 'cats does not exist, reconnecting'
            self.connection.reconnect()
            cursor = self.connection.cursor()

        generator = sqlgeneration.SQLCreateStatements(self.driver)
        query = sqlquery.SQLQuery(sql=generator(schema), debug=1)
        query(cursor)

    def testDBRowDataType(self):
        query = sqlquery.SQLQuery(sql='select * from cats;', debug=1)
        schema = cats.lookupName('cats')
        resultSet = schema.collectionClass(cursor=query(self.connection), schema=schema)
        cats.driver = self.driver
        for item in resultSet:
            for prop in item.getProperties():
                assert prop.dataType, "Property %r didn't find a data-type specifier" % (prop,)

    def tearDown(self):
        try:
            self.connection.rollback()
        except Exception, err:
            pass


if __name__ == '__main__':
    unittest.main()