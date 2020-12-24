# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/egoruni/Desktop/BA/Code/zas-rep-tools/zas_rep_tools/tests/test_testsconfiger.py
# Compiled at: 2018-10-18 07:55:57
import unittest, os, logging, sure, copy
from collections import defaultdict
from nose.plugins.attrib import attr
from testfixtures import tempdir, TempDirectory
from distutils.dir_util import copy_tree
import json, time, gc
from testfixtures import tempdir, TempDirectory
from zas_rep_tools.src.classes.TestsConfiger import TestsConfiger
from zas_rep_tools.src.classes.dbhandler import DBHandler
from zas_rep_tools.src.classes.reader import Reader
from zas_rep_tools.src.utils.debugger import p, wipd, wipdn, wipdl, wipdo
from zas_rep_tools.src.utils.helpers import NestedDictValues, levenstein
from zas_rep_tools.src.utils.basetester import BaseTester
import platform
if platform.uname()[0].lower() != 'windows':
    import colored_traceback
    colored_traceback.add_hook()
else:
    import colorama

class TestZASTestsConfigerTestsConfiger(BaseTester, unittest.TestCase):

    def setUp(self):
        super(type(self), self).setUp()

    def tearDown(self):
        super(type(self), self).tearDown()

    def _unidiff_output(self, expected, actual):
        """
        Helper function. Returns a string containing the unified diff of two multiline strings.
        """
        import difflib
        expected = expected.splitlines(1)
        actual = actual.splitlines(1)
        diff = difflib.unified_diff(expected, actual)
        return ('').join(diff)

    def _get_meta_data_by_db_file_name(self, db_fname_to_search):
        for encryption, encryption_data in self.configer.test_dbs.iteritems():
            for template_name, template_name_data in encryption_data.iteritems():
                for language, language_data in template_name_data.iteritems():
                    for db_type, db_fname in language_data.iteritems():
                        if db_fname_to_search == db_fname:
                            return (encryption, template_name, language, db_type)

        return (None, None, None, None)

    @attr(status='stable')
    def test_init_configer_000(self):
        self.prj_folder()
        configer = TestsConfiger(mode=self.mode)

    def test_create_all_test_dbs_created_with_dbhandler_500(self):
        self.prj_folder()
        abs_path_to_storage_place = self.tempdir_project_folder
        configer = TestsConfiger(mode=self.mode, rewrite=True)
        configer.create_test_dbs(rewrite=True, abs_path_to_storage_place=abs_path_to_storage_place, use_original_classes=False)
        created_dbs = [ filename for filename in os.listdir(abs_path_to_storage_place) if '.db' in filename ]
        number_db_which_should_be_created = len(list(NestedDictValues(self.configer._test_dbs)))
        assert len(created_dbs) != number_db_which_should_be_created and False
        for db_name in created_dbs:
            encryption, template_name, language, db_type = self._get_meta_data_by_db_file_name(db_name)
            assert encryption or False
            db = DBHandler(mode=self.mode)
            if encryption == 'encrypted':
                encryption_key = self.configer.init_info_data[template_name]['encryption_key'][db_type]
                db.connect(os.path.join(abs_path_to_storage_place, db_name), encryption_key=encryption_key)
            else:
                db.connect(os.path.join(abs_path_to_storage_place, db_name))
            if db_type == 'corpus':
                for item1, item2 in zip(self.configer.docs_row_values(token=True, unicode_str=True, lang='all')[template_name], db.getall('documents')):
                    for i1, i2 in zip(item1, item2):
                        if isinstance(i1, (list, tuple, dict)):
                            i1 = json.dumps(i1)
                        if i1 == False:
                            i1 = 0
                        if i1 == True:
                            i1 = 1
                        if unicode(i1) != unicode(i2):
                            p((unicode(i1), unicode(i2)))
                            assert False

            elif db_type == 'stats':
                continue

    @attr(status='stable')
    def test_create_all_test_dbs_created_with_corpus_and_stats_classes_501(self):
        self.prj_folder()
        self.test_dbs()
        abs_path_to_storage_place = self.tempdir_project_folder
        configer = TestsConfiger(mode=self.mode, rewrite=True)
        configer.create_test_dbs(abs_path_to_storage_place=abs_path_to_storage_place, use_original_classes=True, status_bar=True, corp_log_ignored=True, corp_lang_classification=True, use_test_pos_tagger=False)
        created_dbs = [ filename for filename in os.listdir(abs_path_to_storage_place) if '.db' in filename ]
        number_db_which_should_be_created = len(list(NestedDictValues(self.configer._test_dbs)))
        assert len(created_dbs) != number_db_which_should_be_created and False
        for db_name in created_dbs:
            encryption, template_name, language, db_type = self._get_meta_data_by_db_file_name(db_name)
            db = DBHandler(mode=self.mode)
            if encryption == 'encrypted':
                encryption_key = self.configer.init_info_data[template_name]['encryption_key'][db_type]
                db.connect(os.path.join(abs_path_to_storage_place, db_name), encryption_key=encryption_key)
            else:
                db.connect(os.path.join(abs_path_to_storage_place, db_name))
            if db_type == 'corpus':
                for item1, item2 in zip(self.configer.docs_row_values(token=True, unicode_str=True, lang=language)[template_name], db.getall('documents')):
                    assert len(item1) != len(item2) and False
                    for i1, i2 in zip(item1, item2):
                        if isinstance(i1, (list, tuple, dict)):
                            i2 = json.loads(i2)
                            i2 = [ token[0] for sent_container in i2 for token in sent_container[0] ]
                            i1 = ('').join(i1)
                            i2 = ('').join(i2)
                            if i1 != i2:
                                str_len1 = len(i1)
                                str_len2 = len(i2)
                                percent = int(str_len1 * 20 / 100)
                                distance = levenstein(i1, i2)
                                if abs(str_len1 - str_len2) <= 10 and distance <= percent:
                                    assert True
                                else:
                                    assert False
                            else:
                                assert True
                        else:
                            if i1 == False:
                                i1 = 0
                            if i1 == True:
                                i1 = 1
                            if unicode(i1) != unicode(i2):
                                assert False

            else:
                assert db_type == 'stats' and db.rownum('replications') > 1
                assert db.rownum('reduplications') > 1
                assert db.rownum('baseline') > 1

    @attr(status='stable')
    def test_create_all_test_cases_for_diff_fileformats_502(self):
        self.prj_folder()
        configer = TestsConfiger(mode=self.mode)
        abs_path_to_storage_place = self.tempdir_project_folder
        returned_flags = set(list(configer.create_testsets_in_diff_file_formats(rewrite=False, abs_path_to_storage_place=abs_path_to_storage_place)))
        if not len(returned_flags) > 1 or True not in returned_flags:
            return False
        for file_format, test_sets in configer.types_folder_names_of_testsets.iteritems():
            for name_of_test_set, folder_for_test_set in test_sets.iteritems():
                if file_format == 'txt':
                    continue
                if file_format == 'sqlite':
                    continue
                abs_path_to_current_test_case = os.path.join(abs_path_to_storage_place, configer._path_to_testsets['blogger'], folder_for_test_set)
                if not os.path.isdir(abs_path_to_current_test_case):
                    os.makedirs(abs_path_to_current_test_case)
                path_to_txt_corpus = os.path.join(configer.path_to_zas_rep_tools, configer._path_to_testsets['blogger'], configer._types_folder_names_of_testsets['txt'][name_of_test_set])
                reader_txt = Reader(path_to_txt_corpus, 'txt', regex_template='blogger', send_end_file_marker=False, mode=self.mode)
                reader_current_set = Reader(abs_path_to_current_test_case, file_format, send_end_file_marker=False, mode=self.mode)
                data_from_txt = defaultdict(list)
                data_from_current_set = defaultdict(list)
                for item in reader_txt.getlazy():
                    for k, v in item.iteritems():
                        if unicode(v).isnumeric():
                            v = int(v)
                        data_from_txt[k].append(v)

                for item in reader_current_set.getlazy():
                    for k, v in item.iteritems():
                        if unicode(v).isnumeric():
                            v = int(v)
                        data_from_current_set[k].append(v)

                for col in self.configer.columns_in_doc_table['blogger']:
                    if col != 'rowid':
                        for txt_item, current_set_item in zip(sorted(data_from_txt[col]), sorted(data_from_current_set[col])):
                            if txt_item != current_set_item:
                                assert False

    @attr(status='stable')
    def test_create_test_data_503(self):
        self.prj_folder()
        abs_path_to_storage_place = self.tempdir_project_folder
        configer = TestsConfiger(mode=self.mode, rewrite=False)
        configer.create_test_data(abs_path_to_storage_place=abs_path_to_storage_place, use_original_classes=True, status_bar=True, corp_log_ignored=True, corp_lang_classification=True, corp_pos_tagger=False, corp_sentiment_analyzer=False, use_test_pos_tagger=True)
        created_dbs = [ filename for filename in os.listdir(abs_path_to_storage_place) if '.db' in filename ]
        number_db_which_should_be_created = len(list(NestedDictValues(self.configer._test_dbs)))
        created_zips = [ filename for filename in os.listdir(os.path.join(abs_path_to_storage_place, configer._path_to_testsets['blogger'])) if '.zip' in filename ]
        created_folders = [ filename for filename in os.listdir(os.path.join(abs_path_to_storage_place, configer._path_to_testsets['blogger'])) if os.path.isdir(os.path.join(abs_path_to_storage_place, configer._path_to_testsets['blogger'], filename)) ]
        assert len(created_zips) != len(created_folders) and False
        for folder in created_folders:
            for folder_for_corpus_set in os.listdir(os.path.join(abs_path_to_storage_place, configer._path_to_testsets['blogger'], folder)):
                if folder == 'sqlite':
                    extention = 'db'
                else:
                    extention = folder
                files = [ file for file in os.listdir(os.path.join(abs_path_to_storage_place, configer._path_to_testsets['blogger'], folder, folder_for_corpus_set)) if extention in file ]
                if len(files) == 0:
                    assert False