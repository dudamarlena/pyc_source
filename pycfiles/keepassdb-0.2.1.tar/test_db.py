# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hans/workspace/keepassdb/keepassdb/tests/test_db.py
# Compiled at: 2013-01-01 18:40:31
"""
Unit tests for the main Database class.
"""
from __future__ import print_function, unicode_literals
import os.path
from io import BytesIO
from keepassdb import Database, model, exc
from keepassdb.tests import TestBase, RESOURCES_DIR

class DatabaseTest(TestBase):

    def test_init_missing_fil(self):
        """ Test initialization w/ invalid file. """
        with self.assertRaises(IOError):
            db = Database(b'./missing-path.kdb')

    def test_init_new(self):
        """ Test initializing new database. """
        db = Database()
        db.create_default_group()
        exp_g = model.Group(title=b'Internet', icon=1, level=0, id=1, db=db, parent=db.root)
        self.assertEquals(1, len(db.groups))
        self.assertEquals(exp_g.__dict__, db.groups[0].__dict__)
        self.assertEquals([], db.groups[0].entries)

    def test_load_file(self):
        """
        Test loading from file path.
        """
        db = Database()
        kdb = os.path.join(RESOURCES_DIR, b'example.kdb')
        with self.assertRaisesRegexp(ValueError, b'Password and/or keyfile is required.'):
            db.load(kdb)
        db.load(kdb, password=b'test')
        self.assertEquals(kdb, db.filepath)

    def test_load_stream(self):
        """
        Test loading from stream.
        """
        db = Database()
        kdb = os.path.join(RESOURCES_DIR, b'example.kdb')
        with open(kdb, b'rb') as (fp):
            stream = BytesIO(fp.read())
            stream.seek(0)
            with self.assertRaisesRegexp(ValueError, b'Password and/or keyfile is required.'):
                db.load(stream)
            stream.seek(0)
            db.load(stream, password=b'test')

    def test_load(self):
        """ Test loading database """
        db = Database()
        kdb = os.path.join(RESOURCES_DIR, b'example.kdb')
        db.load(kdb, password=b'test')
        top_groups = [ g.title for g in db.root.children ]
        self.assertEquals([b'Internet', b'eMail', b'Backup'], top_groups)
        self.assertEquals([b'A1', b'B1', b'C1'], [ g.title for g in db.root.children[0].children ])
        self.assertEquals(set([b'AEntry1', b'AEntry2', b'AEntry3']), set([ e.title for e in db.root.children[0].children[0].entries ]))
        self.assertEquals([b'A2'], [ g.title for g in db.root.children[0].children[0].children ])

    def test_save(self):
        """ Test creating and saving a database. """
        db = Database()
        i_group = db.create_default_group()
        e_group = db.create_group(title=b'eMail')
        e1 = i_group.create_entry(title=b'FirstEntry', username=b'root', password=b'test', url=b'http://example.com')
        e2 = i_group.create_entry(title=b'SecondEntry', username=b'root', password=b'test', url=b'http://example.com')
        e3 = e_group.create_entry(title=b'ThirdEntry', username=b'root', password=b'test', url=b'http://example.com')
        ser = db.to_dict(hierarchy=True, hide_passwords=True)
        with self.assertRaisesRegexp(ValueError, b'Unable to save without target file.'):
            db.save(password=b'test')
        stream = BytesIO()
        db.save(dbfile=stream, password=b'test')
        stream.seek(0)
        with self.assertRaises(exc.AuthenticationError):
            db.load(dbfile=stream, password=b'wrong')
        stream.seek(0)
        db.load(dbfile=stream, password=b'test')
        self.maxDiff = None
        self.assertEquals(ser, db.to_dict(hierarchy=True, hide_passwords=True))
        return