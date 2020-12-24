# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bauble/utils/test.py
# Compiled at: 2016-10-03 09:39:22
import sys, unittest
from pyparsing import *
from sqlalchemy import *
from nose import SkipTest
import bauble, bauble.db as db
from bauble.error import check, CheckConditionError
import bauble.utils as utils
from bauble.test import BaubleTestCase

class UtilsGTKTests(unittest.TestCase):

    def test_create_message_details_dialog(self):
        """
        Interactive test for bauble.utils.create_message_details_dialog()
        """
        raise SkipTest('Not Implemented')
        details = 'these are the lines that i want to test\nasdasdadasddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd\ndasd\nasd\naddasdadadad'
        msg = 'msg'
        d = utils.create_message_details_dialog(msg, details)
        d.run()

    def test_create_message_dialog(self):
        """
        Interactive test for bauble.utils.create_message_details_dialog()
        """
        raise SkipTest('Not Implemented')
        msg = 'msg'
        d = utils.create_message_dialog(msg)
        d.run()

    def test_search_tree_model(self):
        """
        Test bauble.utils.search_tree_model
        """
        import gtk
        model = gtk.TreeStore(str)
        to_find = []
        row = model.append(None, ['1'])
        model.append(row, ['1.1'])
        to_find.append(model.append(row, ['something']))
        model.append(row, ['1.3'])
        row = model.append(None, ['2'])
        to_find.append(model.append(row, ['something']))
        model.append(row, ['2.1'])
        to_find.append(model.append(None, ['something']))
        root = model.get_iter_root()
        results = utils.search_tree_model(model[root], 'something')
        self.assert_(sorted([ model.get_path(r) for r in results ]), sorted(to_find))
        return


class UtilsTests(unittest.TestCase):

    def test_xml_safe(self):
        """
        Test bauble.utils.xml_safe
        """

        class test(object):

            def __str__(self):
                return repr(self)

            def __unicode__(self):
                return repr(self)

        import re
        assert re.match('&lt;.*?&gt;', utils.xml_safe(str(test())))
        assert re.match('&lt;.*?&gt;', utils.xml_safe(unicode(test())))
        assert utils.xml_safe('test string') == 'test string'
        assert utils.xml_safe('test string') == 'test string'
        assert utils.xml_safe('test< string') == 'test&lt; string'
        assert utils.xml_safe('test< string') == 'test&lt; string'

    def test_range_builder(self):
        """Test bauble.utils.range_builder
        """
        assert utils.range_builder('1-3') == [1, 2, 3]
        assert utils.range_builder('1-3,5-7') == [1, 2, 3, 5, 6, 7]
        assert utils.range_builder('1-3,5') == [1, 2, 3, 5]
        assert utils.range_builder('1-3,5,7-9') == [1, 2, 3, 5, 7, 8, 9]
        assert utils.range_builder('1,2,3,4') == [1, 2, 3, 4]
        assert utils.range_builder('11') == [11]
        assert utils.range_builder('-1') == []
        assert utils.range_builder('a-b') == []
        self.assertRaises(CheckConditionError, utils.range_builder, '2-1')

    def test_get_urls(self):
        text = 'There a link in here: http://bauble.belizebotanic.org'
        urls = utils.get_urls(text)
        self.assert_(urls == [(None, 'http://bauble.belizebotanic.org')], urls)
        text = 'There a link in here: http://bauble.belizebotanic.org and some text afterwards.'
        urls = utils.get_urls(text)
        self.assert_(urls == [(None, 'http://bauble.belizebotanic.org')], urls)
        text = 'There is a link here: http://bauble.belizebotanic.org and here: https://belizebotanic.org and some text afterwards.'
        urls = utils.get_urls(text)
        self.assert_(urls == [(None, 'http://bauble.belizebotanic.org'),
         (None, 'https://belizebotanic.org')], urls)
        text = 'There a labeled link in here: [BBG]http://bauble.belizebotanic.org and some text afterwards.'
        urls = utils.get_urls(text)
        self.assert_(urls == [('BBG', 'http://bauble.belizebotanic.org')], urls)
        return


class UtilsDBTests(BaubleTestCase):

    def test_find_dependent_tables(self):
        """
        Test bauble.utils.find_dependent_tables
        """
        metadata = MetaData()
        metadata.bind = db.engine
        table1 = Table('table1', metadata, Column('id', Integer, primary_key=True))
        table2 = Table('table2', metadata, Column('id', Integer, primary_key=True), Column('table1', Integer, ForeignKey('table1.id')))
        table3 = Table('table3', metadata, Column('id', Integer, primary_key=True), Column('table2', Integer, ForeignKey('table2.id')), Column('table4', Integer, ForeignKey('table4.id')))
        table4 = Table('table4', metadata, Column('id', Integer, primary_key=True), Column('table2', Integer, ForeignKey('table2.id')))
        depends = list(utils.find_dependent_tables(table1, metadata))
        print 'table1: %s' % [ table.name for table in depends ]
        self.assert_(list(depends) == [table2, table4, table3])
        depends = list(utils.find_dependent_tables(table2, metadata))
        print 'table2: %s' % [ table.name for table in depends ]
        self.assert_(depends == [table4, table3])
        depends = list(utils.find_dependent_tables(table3, metadata))
        print 'table3: %s' % [ table.name for table in depends ]
        self.assert_(depends == [])
        depends = list(utils.find_dependent_tables(table4, metadata))
        print 'table4: %s' % [ table.name for table in depends ]
        self.assert_(depends == [table3])


class ResetSequenceTests(BaubleTestCase):

    def setUp(self):
        super(ResetSequenceTests, self).setUp()
        self.metadata = MetaData()
        self.metadata.bind = db.engine

    def tearDown(self):
        super(ResetSequenceTests, self).tearDown()
        self.metadata.drop_all()

    @staticmethod
    def get_currval(col):
        if db.engine.name == 'postgresql':
            name = '%s_%s_seq' % (col.table.name, col.name)
            stmt = "select currval('%s');" % name
            return db.engine.execute(stmt).fetchone()[0]
        if db.engine.name == 'sqlite':
            stmt = 'select max(%s) from %s' % (col.name, col.table.name)
            return db.engine.execute(stmt).fetchone()[0] + 1

    def test_no_col_sequence(self):
        """
        Test utils.reset_sequence on a column without a Sequence()

        This only tests that reset_sequence() doesn't fail if there is
        no sequence.
        """
        table = Table('test_reset_sequence', self.metadata, Column('id', Integer, primary_key=True))
        self.metadata.create_all()
        self.insert = table.insert()
        db.engine.execute(self.insert, values=[{'id': 1}])
        utils.reset_sequence(table.c.id)

    def test_empty_col_sequence(self):
        """
        Test utils.reset_sequence on a column without a Sequence()

        This only tests that reset_sequence() doesn't fail if there is
        no sequence.
        """
        table = Table('test_reset_sequence', self.metadata, Column('id', Integer, primary_key=True))
        self.metadata.create_all()
        utils.reset_sequence(table.c.id)

    def test_with_col_sequence(self):
        """
        Test utils.reset_sequence on a column that has an Sequence()
        """
        table = Table('test_reset_sequence', self.metadata, Column('id', Integer, Sequence('test_reset_sequence_id_seq'), primary_key=True, unique=True))
        self.metadata.create_all()
        rangemax = 10
        for i in range(1, rangemax + 1):
            table.insert().values(id=i).execute()

        utils.reset_sequence(table.c.id)
        currval = self.get_currval(table.c.id)
        self.assert_(currval > rangemax, currval)