# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mcfletch/pylive/table/pytable/tests/test_dbschema.py
# Compiled at: 2004-08-27 02:11:56
from pytable.schemabuilder import *
from pytable import dbschema, sqlgeneration, sqlquery, dbspecifier
import unittest
cats = table('cats', (
 field('cat_id', 'serial', 0, 'Unique cat identifier', constraints=(notNull(), primary())), field('cat_name', 'varchar', 255, "The cat's name", constraints=(notNull(),)), field('declawed', 'boolean', 0, "Poor lil' kitty")), 'Primary table for storing critical info about cats')

class CatsTest(unittest.TestCase):
    __module__ = __name__

    def testKeys(self):
        assert cats.getUniqueKeys() == [('cat_id', )]

    def testKeys2(self):
        t = table('blah', (), constraints=(unique(fields=('whatever', )),))
        assert t.getUniqueKeys() == [('whatever', )]

    def testKeys3(self):
        t = table('blah', (), indices=(index(unique=1, fields=('whatever', )),))
        assert t.getUniqueKeys() == [('whatever', )]

    def testPrimaryFirst(self):
        t = table('blah', (), indices=(index(unique=1, fields=('whatever', )),), constraints=(primary(fields=('whatever2', )),))
        assert t.getUniqueKeys() == [('whatever2', ), ('whatever', )]


if __name__ == '__main__':
    unittest.main()