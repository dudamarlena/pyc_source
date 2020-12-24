# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/egoruni/Desktop/BA/Code/zas-rep-tools/zas_rep_tools/tests/test_exporter.py
# Compiled at: 2018-10-19 06:50:53
import unittest, os, logging, sure, copy
from nose.plugins.attrib import attr
from testfixtures import tempdir, TempDirectory
from distutils.dir_util import copy_tree
import sys
from zas_rep_tools.src.classes.exporter import Exporter
from zas_rep_tools.src.classes.reader import Reader
from zas_rep_tools.src.utils.debugger import p, wipd, wipdn, wipdl, wipdo
from zas_rep_tools.src.utils.basetester import BaseTester

class TestZAScorpusExporterExporter(BaseTester, unittest.TestCase):
    _multiprocess_shared_ = True

    def setUp(self):
        super(type(self), self).setUp()

    def tearDown(self):
        super(type(self), self).tearDown()

    @attr(status='stable')
    def test_exporter_initialisation_with_list_000(self):
        self.blogger_lists()
        exporter = Exporter(self.input_list_fake_blogger_corpus, mode=self.mode)
        exporter.should.be.a(Exporter)

    @attr(status='stable')
    def test_exporter_initialisation_with_reader_obj_001(self):
        self.blogger_corpus()
        reader = Reader(os.path.join(self.tempdir_blogger_corp, self.txt_blogger_hightrepetativ_set), 'txt', regex_template='blogger', mode=self.mode)
        exporter = Exporter(reader.getlazy(), mode=self.mode)
        exporter.should.be.a(Exporter)

    @attr(status='stable')
    def test_export_to_csv_from_list_000(self):
        self.blogger_corpus()
        self.prj_folder()
        self.blogger_lists()
        exporter = Exporter(self.input_list_fake_blogger_corpus, mode=self.mode)
        exporter.tocsv(self.tempdir_project_folder, 'blogger_corpus', self.fieldnames, rows_limit_in_file=1)
        i = 0
        for item in os.listdir(self.tempdir_project_folder):
            if '.csv' in item:
                i += 1

        assert len(self.input_list_fake_blogger_corpus) != i and False

    @attr(status='stable')
    def test_export_to_csv_from_reader_001(self):
        self.blogger_corpus()
        self.prj_folder()
        self.blogger_lists()
        reader = Reader(os.path.join(self.tempdir_blogger_corp, self.txt_blogger_hightrepetativ_set), 'txt', send_end_file_marker=False, regex_template='blogger', mode=self.mode)
        exporter = Exporter(reader.getlazy(), mode=self.mode)
        exporter.tocsv(self.tempdir_project_folder, 'blogger_corpus', self.fieldnames, rows_limit_in_file=1)
        i = 0
        for item in os.listdir(self.tempdir_project_folder):
            if '.csv' in item:
                i += 1

        assert len(list(reader.getlazy())) != i and False

    @attr(status='stable')
    def test_export_to_xml_from_list_002(self):
        self.blogger_corpus()
        self.prj_folder()
        self.blogger_lists()
        exporter = Exporter(self.input_list_fake_blogger_corpus, mode=self.mode)
        exporter.toxml(self.tempdir_project_folder, 'blogger_corpus', rows_limit_in_file=1)
        i = 0
        for item in os.listdir(self.tempdir_project_folder):
            if '.xml' in item:
                i += 1

        assert len(self.input_list_fake_blogger_corpus) != i and False

    @attr(status='stable')
    def test_export_to_xml_from_reader_003(self):
        self.blogger_corpus()
        self.prj_folder()
        self.blogger_lists()
        reader = Reader(os.path.join(self.tempdir_blogger_corp, self.txt_blogger_hightrepetativ_set), 'txt', send_end_file_marker=False, regex_template='blogger', mode=self.mode)
        exporter = Exporter(reader.getlazy(), mode=self.mode)
        exporter.toxml(self.tempdir_project_folder, 'blogger_corpus', rows_limit_in_file=1)
        i = 0
        for item in os.listdir(self.tempdir_project_folder):
            if '.xml' in item:
                i += 1

        assert len(list(reader.getlazy())) != i and False

    @attr(status='stable')
    def test_export_to_json_from_list_004(self):
        self.blogger_corpus()
        self.prj_folder()
        self.blogger_lists()
        exporter = Exporter(self.input_list_fake_blogger_corpus, mode=self.mode, rewrite=True, silent_ignore=True)
        exporter.tojson(self.tempdir_project_folder, 'blogger_corpus', rows_limit_in_file=1)
        i = 0
        for item in os.listdir(self.tempdir_project_folder):
            if '.json' in item:
                i += 1

        assert len(self.input_list_fake_blogger_corpus) != i and False

    @attr(status='stable')
    def test_export_to_json_from_reader_005(self):
        self.blogger_corpus()
        self.prj_folder()
        self.blogger_lists()
        reader = Reader(os.path.join(self.tempdir_blogger_corp, self.txt_blogger_hightrepetativ_set), 'txt', send_end_file_marker=False, regex_template='blogger', mode=self.mode)
        exporter = Exporter(reader.getlazy(), mode=self.mode)
        exporter.tojson(self.tempdir_project_folder, 'blogger_corpus', rows_limit_in_file=1)
        i = 0
        for item in os.listdir(self.tempdir_project_folder):
            if '.json' in item:
                i += 1

        assert len(list(reader.getlazy())) != i and False

    @attr(status='stable')
    def test_export_to_sqlite_from_list_006(self):
        self.blogger_corpus()
        self.prj_folder()
        self.blogger_lists()
        exporter = Exporter(self.input_list_fake_blogger_corpus, mode=self.mode)
        dbname = 'blogger_corpus'
        exporter.tosqlite(self.tempdir_project_folder, dbname, self.fieldnames)
        for item in os.listdir(self.tempdir_project_folder):
            if '.db' in item:
                if dbname not in item:
                    assert False

    @attr(status='stable')
    def test_export_to_sqlite_from_reader_007(self):
        self.blogger_corpus()
        self.prj_folder()
        self.blogger_lists()
        reader = Reader(os.path.join(self.tempdir_blogger_corp, self.txt_blogger_hightrepetativ_set), 'txt', send_end_file_marker=False, regex_template='blogger', mode=self.mode)
        exporter = Exporter(reader.getlazy(), mode=self.mode)
        dbname = 'blogger_corpus'
        exporter.tosqlite(self.tempdir_project_folder, dbname, self.fieldnames)
        for item in os.listdir(self.tempdir_project_folder):
            if '.db' in item:
                if dbname not in item:
                    assert False