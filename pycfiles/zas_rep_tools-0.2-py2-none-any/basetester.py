# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/egoruni/Desktop/BA/Code/zas-rep-tools/zas_rep_tools/src/utils/basetester.py
# Compiled at: 2018-10-19 05:26:44
import unittest, os, logging, codecs, sys, gc
from nose.tools import nottest
from nose.plugins.attrib import attr
from testfixtures import tempdir, TempDirectory
from distutils.dir_util import copy_tree
from zas_rep_tools.src.utils.debugger import p, wipd, wipdn, wipdl, wipdo
from zas_rep_tools.src.classes.TestsConfiger import TestsConfiger
from zas_rep_tools.src.utils.zaslogger import ZASLogger, clear_logger
is_test_data_exist = False

@nottest
def create_test_data():
    global is_test_data_exist
    if not is_test_data_exist:
        test_data_creator = TestsConfiger(mode='error')
        test_data_creator.create_test_data(rewrite=False, use_original_classes=True, status_bar=True, corp_log_ignored=True, corp_lang_classification=True)
        del test_data_creator
        clear_logger()
        is_test_data_exist = True
        gc.collect()


class BaseTester(object):
    _multiprocess_can_split_ = True

    def setUp(self):
        create_test_data()
        gc.collect()
        self.mode = 'error'
        clear_logger()
        self.configer = TestsConfiger(mode='silent')
        self.tempdir = TempDirectory()
        self.path_to_zas_rep_tools = self.configer.path_to_zas_rep_tools

    def tearDown(self):
        t = self.tempdir
        del self
        gc.collect()
        t.cleanup()
        del t

    @nottest
    def create_all_test_data(self):
        self.prj_folder()
        self.test_dbs()
        self.blogger_corpus()
        self.twitter_corpus()
        self.blogger_lists()

    @nottest
    def test_dbs(self):
        self.path_to_testdbs = self.configer.path_to_testdbs
        self.db_blogger_plaintext_corp_en = self.configer.test_dbs['plaintext']['blogger']['en']['corpus']
        self.db_blogger_plaintext_corp_de = self.configer.test_dbs['plaintext']['blogger']['de']['corpus']
        self.db_blogger_plaintext_corp_test = self.configer.test_dbs['plaintext']['blogger']['test']['corpus']
        self.db_blogger_plaintext_stats_en = self.configer.test_dbs['plaintext']['blogger']['en']['stats']
        self.db_blogger_plaintext_stats_de = self.configer.test_dbs['plaintext']['blogger']['de']['stats']
        self.db_blogger_plaintext_stats_test = self.configer.test_dbs['plaintext']['blogger']['test']['stats']
        self.db_twitter_encrypted_corp_de = self.configer.test_dbs['encrypted']['twitter']['de']['corpus']
        self.db_twitter_encrypted_stats_de = self.configer.test_dbs['encrypted']['twitter']['de']['stats']
        self.tempdir.makedir('TestDBs')
        self.tempdir_testdbs = self.tempdir.getpath('TestDBs')
        copy_tree(os.path.join(self.path_to_zas_rep_tools, self.path_to_testdbs), self.tempdir_testdbs)

    def blogger_corpus(self):
        self.path_to_test_sets_for_blogger_Corpus = 'data/tests_data/Corpora/BloggerCorpus'
        self.txt_blogger_hightrepetativ_set = 'txt/HighRepetativSubSet'
        self.txt_blogger_small_fake_set = 'txt/SmallFakeSubset'
        self.csv_blogger_hightrepetativ_set = 'csv/HighRepetativSubSet'
        self.csv_blogger_small_fake_set = 'csv/SmallFakeSubset'
        self.xml_blogger_hightrepetativ_set = 'xml/HighRepetativSubSet'
        self.xml_blogger_small_fake_set = 'xml/SmallFakeSubset'
        self.json_blogger_hightrepetativ_set = 'json/HighRepetativSubSet'
        self.json_blogger_small_fake_set = 'json/SmallFakeSubset'
        self.tempdir.makedir('BloggerCorpus')
        self.tempdir_blogger_corp = self.tempdir.getpath('BloggerCorpus')
        copy_tree(os.path.join(self.path_to_zas_rep_tools, self.path_to_test_sets_for_blogger_Corpus), self.tempdir_blogger_corp)

    def twitter_corpus(self):
        self.path_to_test_sets_for_twitter_Corpus = 'data/tests_data/Corpora/TwitterCorpus'
        self.json_twitter_set = 'JSON/zas-rep-tool/'
        self.csv_twitter_set = 'CSV/zas-rep-tool/'
        self.xml_twitter_set = 'XML/zas-rep-tool/'
        self.tempdir.makedir('TwitterCorpus')
        self.tempdir_twitter_corp = self.tempdir.getpath('TwitterCorpus')
        copy_tree(os.path.join(self.path_to_zas_rep_tools, self.path_to_test_sets_for_twitter_Corpus), self.tempdir_twitter_corp)

    def blogger_lists(self):
        self.input_list_fake_blogger_corpus = [{'rowid': '1', 'star_constellation': 'Capricorn', 'text': 'Well, the angel won. I went to work today....after alot of internal struggle with the facts. I calculated sick days left this year,', 'working_area': 'Consulting', 'age': '46', 'id': '324114', 'gender': 'female'}, {'rowid': '2', 'star_constellation': 'Pisces', 'text': "urlLink Drawing Game  It's PICTIONARY. It's very cool.", 'working_area': 'indUnk', 'age': '24', 'id': '416465', 'gender': 'male'}, {'rowid': '3', 'star_constellation': 'Virgo', 'text': 'The mango said, "Hi there!!.... \n"Hi there!!.... \n"Hi there!!.... ', 'working_area': 'Non-Profit', 'age': '17', 'id': '322624', 'gender': 'female'}]
        self.input_list_blogger_corpus_high_repetativ_subset = [{'rowid': '1', 'star_constellation': 'Capricorn', 'text': '@lovelypig #direct_to_haven 67666 8997 -))) -) -P Neeeeeeeeeeeeeeeeiiiiiiinnnnn!!!!! Bitte nicht 😂😂😂 \nTest Version von einem Tweeeeeeeeet=)))))))\nnoch einen Tweeeeeeeeet=))))))) 😅😅', 'working_area': 'Consulting', 'age': '46', 'id': '324114', 'gender': 'female'}, {'rowid': '2', 'star_constellation': 'Pisces', 'text': 'Einen weiteren Thread eingefügt!!! juHuuuuuuuu=) 💛💛💛\nden vierten Threadddddd!!! wooooowwwwww!!! ☺️ 😜😜😜\nDas ist einnnneeeen Teeeeest Tweeeets, das als "extended" klassifiziert werden sollte!!! Weil es bis 280 Zeichen beinhalten sollte. 😜😜😜😜😜😜😜😜😜😜😜😜😜 Das ist einnnneeeen Teeeeest Tweeeets, das als "extended" klassifiziert werden sollte!!! Weil es bis 280 Zeichen 😜😜😜😜\nDas ist einnnneeeen Teeeeest Quoted Tweet, das als "extended" klassifiziert werden sollte!!! Weil es bis 280 Zeichen beinhalten sollte. 😜😜😜😜😜😜😜😜😜😜😜😜😜 Das ist einnnneeeen Teeeeest Tweeeets, das als "extended" klassifiziert werden sollte!!! Weil es bis 280 Zeichen 😜😜 h', 'working_area': 'indUnk', 'age': '24', 'id': '416465', 'gender': 'male'}, {'rowid': '3', 'star_constellation': 'Virgo', 'text': 'Eine Teeeeeest Diskussion wird eröffnet!!! @zas-rep-tools \nEinen Test Retweet wird gepostet!!!!! Juhuuuuuu=) 😀😀😀😀\nnoooooooch einen Tweeeeeeeeet=)))))))', 'working_area': 'Non-Profit', 'age': '17', 'id': '322624', 'gender': 'female'}]
        self.input_list_blogger_corpus_dirty = [{'rowid': '1', 'star_constellation': 'Capricorn', 'text': '@lovelypig #direct_to_haven 67666 8997 -))) -) -P Neeeeeeeeeeeeeeeeiiiiiiinnnnn!!!!! Bitte nicht @lovelypig 😂😂😂 \nTest Version von einem Tweeeeeeeeet=)))))))\nnoch einen Tweeeeeeeeet=))))))) 111111 22222 3. 444 😅😅', 'working_area': 'Consulting', 'age': '46', 'id': '324114', 'gender': 'female'}, {'rowid': '2', 'star_constellation': 'Virgo', 'text': 'Eine Teeeeeest Diskussion wird eröffnet!!! @zas-rep-tools #doit #stay_you \nEinen Test Retweet wird gepostet!!!!! =))))))) #stay_your_self', 'working_area': 'Non-Profit', 'age': '17', 'id': '322624', 'gender': 'female'}]
        self.fieldnames = self.configer.columns_in_doc_table['blogger']

    def prj_folder(self):
        self.tempdir.makedir('ProjectFolder')
        self.tempdir_project_folder = self.tempdir.getpath('ProjectFolder')