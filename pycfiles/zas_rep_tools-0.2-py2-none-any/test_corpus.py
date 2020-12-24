# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/egoruni/Desktop/BA/Code/zas-rep-tools/zas_rep_tools/tests/test_corpus.py
# Compiled at: 2018-10-19 06:50:51
import unittest, os, logging, sure, copy
from nose.plugins.attrib import attr
from testfixtures import tempdir, TempDirectory
from distutils.dir_util import copy_tree
import random
from decimal import Decimal, ROUND_HALF_UP, ROUND_UP, ROUND_HALF_DOWN, ROUND_DOWN
import json
from zas_rep_tools.src.classes.corpus import Corpus
from zas_rep_tools.src.classes.reader import Reader
from zas_rep_tools.src.utils.helpers import set_class_mode, print_mode_name, LenGen, path_to_zas_rep_tools, get_number_of_streams_adjust_cpu
from zas_rep_tools.src.utils.debugger import p, wipd, wipdn, wipdl, wipdo
from zas_rep_tools.src.utils.basetester import BaseTester
import platform
if platform.uname()[0].lower() != 'windows':
    import colored_traceback
    colored_traceback.add_hook()
else:
    import colorama

class TestZAScorpusCorpus(BaseTester, unittest.TestCase):
    _multiprocess_shared_ = True

    def setUp(self):
        super(type(self), self).setUp()

    def tearDown(self):
        super(type(self), self).tearDown()

    @attr(status='stable')
    def test_initialization_of_the_corpus_instance_000(self):
        self.test_dbs()
        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_en))
        corp.should.be.a(Corpus)

    @attr(status='stable')
    def test_new_plaintext_corpus_initialization_500(self):
        self.prj_folder()
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['corpus']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'corpus'
        corp = Corpus(mode=self.mode)
        corp.init(self.tempdir_project_folder, name, language, visibility, platform_name, source=source, license=license, template_name=template_name, version=version, corpus_id=corpus_id)
        assert corp.exist()

    @attr(status='stable')
    def test_new_encrypted_corpus_initialization_501(self):
        self.prj_folder()
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['corpus']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'corpus'
        corp = Corpus(mode=self.mode)
        corp.init(self.tempdir_project_folder, name, language, visibility, platform_name, encryption_key=encryption_key, source=source, license=license, template_name=template_name, version=version, corpus_id=corpus_id)
        assert corp.exist()

    @attr(status='stable')
    def test_open_plaintext_blogger_corpus_502(self):
        self.test_dbs()
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['corpus']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'corpus'
        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_en))
        corp.corpdb.get_all_attr()['name'].should.be.equal(name)
        corp.corpdb.get_all_attr()['language'].should.be.equal(language)
        corp.corpdb.get_all_attr()['visibility'].should.be.equal(visibility)
        corp.corpdb.get_all_attr()['platform_name'].should.be.equal(platform_name)
        corp.corpdb.get_all_attr()['typ'].should.be.equal(typ)
        corp.corpdb.get_all_attr()['id'].should.be.equal(corpus_id)
        corp.corpdb.get_all_attr()['license'].should.be.equal(license)
        corp.corpdb.get_all_attr()['version'].should.be.equal(version)
        corp.corpdb.get_all_attr()['template_name'].should.be.equal(template_name)
        corp.corpdb.get_all_attr()['source'].should.be.equal(source)
        assert corp.exist()

    @attr(status='stable')
    def test_open_encrypted_twitter_corpus_503(self):
        self.test_dbs()
        name = self.configer.init_info_data['twitter']['name']
        language = self.configer.init_info_data['twitter']['language']
        visibility = self.configer.init_info_data['twitter']['visibility']
        platform_name = self.configer.init_info_data['twitter']['platform_name']
        license = self.configer.init_info_data['twitter']['license']
        template_name = self.configer.init_info_data['twitter']['template_name']
        version = self.configer.init_info_data['twitter']['version']
        source = self.configer.init_info_data['twitter']['source']
        encryption_key = self.configer.init_info_data['twitter']['encryption_key']['corpus']
        corpus_id = self.configer.init_info_data['twitter']['id']['corpus']
        stats_id = self.configer.init_info_data['twitter']['id']['stats']
        typ = 'corpus'
        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs, self.db_twitter_encrypted_corp_de), encryption_key=encryption_key)
        corp.corpdb.get_all_attr()['name'].should.be.equal(name)
        corp.corpdb.get_all_attr()['language'].should.be.equal(language)
        corp.corpdb.get_all_attr()['visibility'].should.be.equal(visibility)
        corp.corpdb.get_all_attr()['platform_name'].should.be.equal(platform_name)
        corp.corpdb.get_all_attr()['typ'].should.be.equal(typ)
        corp.corpdb.get_all_attr()['id'].should.be.equal(corpus_id)
        corp.corpdb.get_all_attr()['license'].should.be.equal(license)
        corp.corpdb.get_all_attr()['version'].should.be.equal(version)
        corp.corpdb.get_all_attr()['template_name'].should.be.equal(template_name)
        corp.corpdb.get_all_attr()['source'].should.be.equal(source)
        assert corp.exist()

    @attr(status='stable')
    def test_insert_without_preprocession_550(self):
        self.prj_folder()
        self.blogger_lists()
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['corpus']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'corpus'
        corp = Corpus(mode=self.mode, status_bar=True)
        corp.init(self.tempdir_project_folder, name, language, visibility, platform_name, source=source, license=license, template_name=template_name, version=version, corpus_id=corpus_id, preprocession=False)
        corp.insert(self.input_list_blogger_corpus_high_repetativ_subset)
        for row_from_corp, row_from_input in zip(corp.docs(output='dict'), self.input_list_blogger_corpus_high_repetativ_subset):
            {unicode(k):unicode(v) for k, v in row_from_input.iteritems()}.should.be.equal({unicode(k):unicode(v) for k, v in row_from_corp.iteritems()})

        assert corp.total_error_insertion_during_last_insertion_process == 0

    @attr(status='stable')
    def test_insert_with_preprocession_from_json_in_one_thread_on_twitter_example_551(self):
        self.prj_folder()
        self.twitter_corpus()
        name = self.configer.init_info_data['twitter']['name']
        language = self.configer.init_info_data['twitter']['language']
        visibility = self.configer.init_info_data['twitter']['visibility']
        platform_name = self.configer.init_info_data['twitter']['platform_name']
        license = self.configer.init_info_data['twitter']['license']
        template_name = self.configer.init_info_data['twitter']['template_name']
        version = self.configer.init_info_data['twitter']['version']
        source = self.configer.init_info_data['twitter']['source']
        encryption_key = self.configer.init_info_data['twitter']['encryption_key']['corpus']
        corpus_id = self.configer.init_info_data['twitter']['id']['corpus']
        stats_id = self.configer.init_info_data['twitter']['id']['stats']
        typ = 'corpus'
        language = 'en'
        reader = Reader(os.path.join(self.tempdir_twitter_corp, self.json_twitter_set), 'json', formatter_name='twitterstreamapi', logger_traceback=True, ext_tb=True, mode=self.mode)
        corp = Corpus(logger_traceback=True, ext_tb=True, mode=self.mode, use_test_pos_tagger=True)
        corp.init(self.tempdir_project_folder, name, language, visibility, platform_name, source=source, license=license, template_name=template_name, version=version, corpus_id=corpus_id, preprocession=True, sent_splitter='somajo', pos_tagger=True)
        corp.insert(reader.getlazy())
        inserted_rows_into_db = len(list(corp.corpdb.lazyget('documents')))
        corp.inserted_insertion_status_general
        assert inserted_rows_into_db != sum(corp.inserted_insertion_status_general.values()) and False
        assert corp.total_error_insertion_during_last_insertion_process == 0

    @attr(status='stable')
    def test_insert_with_preprocession_from_json_in_many_thread_on_twitter_example_552(self):
        self.prj_folder()
        self.twitter_corpus()
        name = self.configer.init_info_data['twitter']['name']
        language = self.configer.init_info_data['twitter']['language']
        visibility = self.configer.init_info_data['twitter']['visibility']
        platform_name = self.configer.init_info_data['twitter']['platform_name']
        license = self.configer.init_info_data['twitter']['license']
        template_name = self.configer.init_info_data['twitter']['template_name']
        version = self.configer.init_info_data['twitter']['version']
        source = self.configer.init_info_data['twitter']['source']
        encryption_key = self.configer.init_info_data['twitter']['encryption_key']['corpus']
        corpus_id = self.configer.init_info_data['twitter']['id']['corpus']
        stats_id = self.configer.init_info_data['twitter']['id']['stats']
        typ = 'corpus'
        language = 'de'
        reader = Reader(os.path.join(self.tempdir_twitter_corp, self.json_twitter_set), 'json', formatter_name='twitterstreamapi', logger_traceback=True, ext_tb=True, mode=self.mode)
        corp = Corpus(logger_traceback=True, ext_tb=True, mode=self.mode, use_test_pos_tagger=True)
        corp.init(self.tempdir_project_folder, name, language, visibility, platform_name, source=source, license=license, template_name=template_name, version=version, corpus_id=corpus_id, sent_splitter='somajo', pos_tagger='someweta')
        corp.insert(reader.getlazy(stream_number=-1, min_files_pro_stream=7))
        inserted_rows_into_db = len(list(corp.corpdb.lazyget('documents')))
        if inserted_rows_into_db != sum(corp.inserted_insertion_status_general.values()):
            assert False
            assert reader.files_at_all_was_found != inserted_rows_into_db + corp.total_ignored_last_insertion and False
        assert corp.total_error_insertion_during_last_insertion_process == 0

    @attr(status='stable')
    def test_preprocessing_on_example_of_blogger_corp_553_1(self):
        self.prj_folder()
        self.blogger_corpus()
        self.blogger_lists()
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['corpus']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        preprocession = True
        tokenizer = 'somajo'
        sent_splitter = 'somajo'
        pos_tagger = 'someweta'
        sentiment_analyzer = 'textblob'
        lang_classification = True
        del_url = True
        del_punkt = False
        del_num = False
        del_html = False
        del_mention = True
        del_hashtag = False
        case_sensitiv = True
        typ = 'corpus'
        language = 'de'
        reader = Reader(os.path.join(self.tempdir_blogger_corp, self.txt_blogger_small_fake_set), 'txt', regex_template='blogger', mode=self.mode)
        corp = Corpus(logger_traceback=True, status_bar=True, mode=self.mode, use_test_pos_tagger=False)
        corp.init(self.tempdir_project_folder, name, language, visibility, platform_name, source=source, license=license, template_name=template_name, version=version, corpus_id=corpus_id, preprocession=preprocession, tokenizer=tokenizer, sent_splitter=sent_splitter, pos_tagger=pos_tagger, sentiment_analyzer=sentiment_analyzer, lang_classification=lang_classification, del_url=del_url, del_punkt=del_punkt, del_num=del_num, del_mention=del_mention, del_hashtag=del_hashtag, del_html=del_html, case_sensitiv=case_sensitiv)
        corp.insert(self.input_list_blogger_corpus_high_repetativ_subset)
        assert corp.total_inserted_during_last_insert == len(self.input_list_blogger_corpus_high_repetativ_subset)
        assert corp.total_error_insertion_during_last_insertion_process == 0
        assert corp.total_ignored_last_insertion == 0
        for row_from_corp, row_from_input in zip(corp.docs(output='dict'), self.input_list_blogger_corpus_high_repetativ_subset):
            del row_from_corp['text']
            del row_from_input['text']
            {unicode(k):unicode(v) for k, v in row_from_input.iteritems()}.should.be.equal({unicode(k):unicode(v) for k, v in row_from_corp.iteritems()})

        for row_from_corp in corp.docs(output='dict'):
            if row_from_corp['id'] == 324114:
                output_text = '[[[[null, ":mention:"], ["#direct_to_haven", "hashtag"], ["67666", "number"], ["8997", "number"], ["-)))", "EMOASC"], ["-)", "EMOASC"], ["-P", "EMOASC"], ["Neeeeeeeeeeeeeeeeiiiiiiinnnnn", "NN"], ["!!!!!", "symbol"]], ["neutral", 0.0]], [[["Bitte", "PTKANT"], ["nicht", "PTKNEG"], ["\\ud83d\\ude02\\ud83d\\ude02\\ud83d\\ude02", "EMOIMG"], ["Test", "NN"], ["Version", "NN"], ["von", "APPR"], ["einem", "ART"], ["Tweeeeeeeeet", "NN"], ["=)))))))", "EMOASC"], ["noch", "ADV"], ["einen", "ART"], ["Tweeeeeeeeet", "NN"], ["=)))))))", "EMOASC"], ["\\ud83d\\ude05\\ud83d\\ude05", "EMOIMG"]], ["neutral", 0.0]]]'
                row_from_corp['text'].should.be.equal(output_text)
            elif row_from_corp['id'] == 416465:
                output_text = '[[[["Einen", "ART"], ["weiteren", "ADJA"], ["Thread", "NN"], ["eingef\\u00fcgt", "VVPP"], ["!!!", "symbol"], ["ju", "NE"], ["Huuuuuuuu", "NN"], ["=)", "EMOASC"], ["\\ud83d\\udc9b\\ud83d\\udc9b\\ud83d\\udc9b", "EMOIMG"], ["den", "ART"], ["vierten", "ADJA"], ["Threadddddd", "NN"], ["!!!", "symbol"], ["wooooowwwwww", "ADJD"], ["!!!", "symbol"], ["\\u263a", "EMOIMG"], ["\\ufe0f", "EMOIMG"], ["\\ud83d\\ude1c\\ud83d\\ude1c\\ud83d\\ude1c", "EMOIMG"], ["Das", "PDS"], ["ist", "VAFIN"], ["einnnneeeen", "ART"], ["Teeeeest", "NN"], ["Tweeeets", "NE"], [",", "symbol"], ["das", "PRELS"], ["als", "APPR"], ["\\"", "symbol"], ["extended", "ADJD"], ["\\"", "symbol"], ["klassifiziert", "VVPP"], ["werden", "VAINF"], ["sollte", "VMFIN"], ["!!!", "symbol"]], ["positive", 0.13999999999999999]], [[["Weil", "KOUS"], ["es", "PPER"], ["bis", "APPR"], ["280", "number"], ["Zeichen", "NN"], ["beinhalten", "VVINF"], ["sollte", "VMFIN"], [".", "symbol"], ["\\ud83d\\ude1c\\ud83d\\ude1c\\ud83d\\ude1c\\ud83d\\ude1c\\ud83d\\ude1c\\ud83d\\ude1c\\ud83d\\ude1c\\ud83d\\ude1c\\ud83d\\ude1c\\ud83d\\ude1c\\ud83d\\ude1c\\ud83d\\ude1c\\ud83d\\ude1c", "EMOIMG"], ["Das", "PDS"], ["ist", "VAFIN"], ["einnnneeeen", "ART"], ["Teeeeest", "NN"], ["Tweeeets", "NE"], [",", "symbol"], ["das", "PRELS"], ["als", "APPR"], ["\\"", "symbol"], ["extended", "ADJD"], ["\\"", "symbol"], ["klassifiziert", "VVPP"], ["werden", "VAINF"], ["sollte", "VMFIN"], ["!!!", "symbol"]], ["neutral", 0.0]], [[["Weil", "KOUS"], ["es", "PPER"], ["bis", "APPR"], ["280", "number"], ["Zeichen", "NN"], ["\\ud83d\\ude1c\\ud83d\\ude1c\\ud83d\\ude1c\\ud83d\\ude1c", "EMOIMG"], ["Das", "PDS"], ["ist", "VAFIN"], ["einnnneeeen", "ART"], ["Teeeeest", "NN"], ["Quoted", "NE"], ["Tweet", "NN"], [",", "symbol"], ["das", "PRELS"], ["als", "APPR"], ["\\"", "symbol"], ["extended", "ADJD"], ["\\"", "symbol"], ["klassifiziert", "VVPP"], ["werden", "VAINF"], ["sollte", "VMFIN"], ["!!!", "symbol"]], ["neutral", 0.0]], [[["Weil", "KOUS"], ["es", "PPER"], ["bis", "APPR"], ["280", "number"], ["Zeichen", "NN"], ["beinhalten", "VVINF"], ["sollte", "VMFIN"], [".", "symbol"], ["\\ud83d\\ude1c\\ud83d\\ude1c\\ud83d\\ude1c\\ud83d\\ude1c\\ud83d\\ude1c\\ud83d\\ude1c\\ud83d\\ude1c\\ud83d\\ude1c\\ud83d\\ude1c\\ud83d\\ude1c\\ud83d\\ude1c\\ud83d\\ude1c\\ud83d\\ude1c", "EMOIMG"], ["Das", "PDS"], ["ist", "VAFIN"], ["einnnneeeen", "ART"], ["Teeeeest", "NN"], ["Tweeeets", "NE"], [",", "symbol"], ["das", "PRELS"], ["als", "APPR"], ["\\"", "symbol"], ["extended", "ADJD"], ["\\"", "symbol"], ["klassifiziert", "VVPP"], ["werden", "VAINF"], ["sollte", "VMFIN"], ["!!!", "symbol"]], ["neutral", 0.0]], [[["Weil", "KOUS"], ["es", "PPER"], ["bis", "APPR"], ["280", "number"], ["Zeichen", "NN"], ["\\ud83d\\ude1c\\ud83d\\ude1c", "EMOIMG"], ["h", "NN"]], ["neutral", 0.0]]]'
                row_from_corp['text'].should.be.equal(output_text)
            elif row_from_corp['id'] == 322624:
                output_text = '[[[["Eine", "ART"], ["Teeeeeest", "NN"], ["Diskussion", "NN"], ["wird", "VAFIN"], ["er\\u00f6ffnet", "VVPP"], ["!!!", "symbol"], [null, ":mention:"], ["Einen", "ART"], ["Test", "NN"], ["Retweet", "NN"], ["wird", "VAFIN"], ["gepostet", "VVPP"], ["!!!!!", "symbol"]], ["neutral", 0.0]], [[["Juhuuuuuu", "ITJ"], ["=)", "EMOASC"], ["\\ud83d\\ude00\\ud83d\\ude00\\ud83d\\ude00\\ud83d\\ude00", "EMOIMG"], ["noooooooch", "ADV"], ["einen", "ART"], ["Tweeeeeeeeet", "NN"], ["=)))))))", "EMOASC"]], ["neutral", 0.0]]]'
                row_from_corp['text'].should.be.equal(output_text)

    @attr(status='stable')
    def test_preprocessing__with_cleaning_553_2(self):
        self.prj_folder()
        self.blogger_corpus()
        self.blogger_lists()
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['corpus']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        preprocession = True
        tokenizer = 'somajo'
        sent_splitter = True
        pos_tagger = True
        sentiment_analyzer = True
        lang_classification = True
        del_url = True
        del_punkt = True
        del_num = True
        del_html = True
        del_mention = True
        del_hashtag = True
        case_sensitiv = False
        typ = 'corpus'
        language = 'de'
        reader = Reader(os.path.join(self.tempdir_blogger_corp, self.txt_blogger_small_fake_set), 'txt', regex_template='blogger', mode=self.mode)
        corp = Corpus(logger_traceback=True, status_bar=True, mode=self.mode, use_test_pos_tagger=True)
        corp.init(self.tempdir_project_folder, name, language, visibility, platform_name, source=source, license=license, template_name=template_name, version=version, corpus_id=corpus_id, preprocession=preprocession, tokenizer=tokenizer, sent_splitter=sent_splitter, pos_tagger=pos_tagger, sentiment_analyzer=sentiment_analyzer, lang_classification=lang_classification, del_url=del_url, del_punkt=del_punkt, del_num=del_num, del_mention=del_mention, del_hashtag=del_hashtag, del_html=del_html, case_sensitiv=case_sensitiv)
        corp.insert(self.input_list_blogger_corpus_dirty)
        assert corp.total_inserted_during_last_insert == len(self.input_list_blogger_corpus_dirty)
        assert corp.total_error_insertion_during_last_insertion_process == 0
        assert corp.total_ignored_last_insertion == 0
        for row_from_corp, row_from_input in zip(corp.docs(output='dict'), self.input_list_blogger_corpus_dirty):
            del row_from_corp['text']
            del row_from_input['text']
            {unicode(k):unicode(v) for k, v in row_from_input.iteritems()}.should.be.equal({unicode(k):unicode(v) for k, v in row_from_corp.iteritems()})

        for row_from_corp in corp.docs(output='dict'):
            if row_from_corp['id'] == 324114:
                output_text = '[[[[null, ":mention:"], [null, ":hashtag:"], [null, ":number:"], [null, ":number:"], ["-)))", "EMOASC"], ["-)", "EMOASC"], ["-p", "EMOASC"], ["neeeeeeeeeeeeeeeeiiiiiiinnnnn", "!"], [null, ":symbol:"]], ["neutral", 0.0]], [[["bitte", "V"], ["nicht", "!"], [null, ":mention:"], ["\\ud83d\\ude02\\ud83d\\ude02\\ud83d\\ude02", "EMOIMG"], ["test", "N"], ["version", "N"], ["von", "!"], ["einem", "!"], ["tweeeeeeeeet", "V"], ["=)))))))", "EMOASC"], ["noch", "!"], ["einen", "!"], ["tweeeeeeeeet", "V"], ["=)))))))", "EMOASC"], [null, ":number:"], [null, ":number:"], ["3", "ordinal"], [null, ":number:"], ["\\ud83d\\ude05\\ud83d\\ude05", "EMOIMG"]], ["positive", 1.0]]]'
                row_from_corp['text'].should.be.equal(output_text)
            elif row_from_corp['id'] == 322624:
                output_text = '[[[["eine", "!"], ["teeeeeest", "N"], ["diskussion", "!"], ["wird", "!"], ["er\\u00f6ffnet", "!"], [null, ":symbol:"], [null, ":mention:"], [null, ":hashtag:"], [null, ":hashtag:"], ["einen", "^"], ["test", "N"], ["retweet", "V"], ["wird", "!"], ["gepostet", "!"], [null, ":symbol:"], ["=)))))))", "EMOASC"], [null, ":hashtag:"]], ["neutral", 0.0]]]'
                row_from_corp['text'].should.be.equal(output_text)

    @attr(status='stable')
    def test_insert_one_thread_on_example_of_blogger_corp_554(self):
        self.prj_folder()
        self.blogger_corpus()
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['corpus']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        preprocession = True
        tokenizer = True
        pos_tagger = False
        sent_splitter = False
        sentiment_analyzer = False
        lang_classification = False
        del_url = True
        del_punkt = True
        del_num = True
        del_html = True
        del_mention = True
        del_hashtag = True
        case_sensitiv = True
        typ = 'corpus'
        language = 'de'
        reader = Reader(os.path.join(self.tempdir_blogger_corp, self.txt_blogger_small_fake_set), 'txt', regex_template='blogger', mode=self.mode)
        corp = Corpus(logger_traceback=True, status_bar=True, mode=self.mode, use_test_pos_tagger=True)
        corp.init(self.tempdir_project_folder, name, language, visibility, platform_name, source=source, license=license, template_name=template_name, version=version, corpus_id=corpus_id, preprocession=preprocession, tokenizer=tokenizer, sent_splitter=sent_splitter, pos_tagger=pos_tagger, sentiment_analyzer=sentiment_analyzer, lang_classification=lang_classification, del_url=del_url, del_punkt=del_punkt, del_num=del_num, del_mention=del_mention, del_hashtag=del_hashtag, del_html=del_html, case_sensitiv=case_sensitiv)
        corp.insert(reader.getlazy(stream_number=1, min_files_pro_stream=1))
        number_to_insert = len(reader.getlazy(stream_number=1, min_files_pro_stream=1))
        assert corp.total_inserted_during_last_insert == number_to_insert
        assert corp.total_error_insertion_during_last_insertion_process == 0
        assert corp.total_ignored_last_insertion == 0

    @attr(status='stable')
    def test_insert_parallel_many_threads_on_example_of_blogger_corp_555(self):
        self.prj_folder()
        self.blogger_corpus()
        self.blogger_lists()
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['corpus']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        preprocession = True
        tokenizer = True
        pos_tagger = True
        sent_splitter = True
        sentiment_analyzer = True
        lang_classification = True
        del_url = True
        del_punkt = True
        del_num = True
        del_html = True
        del_mention = True
        del_hashtag = True
        case_sensitiv = True
        typ = 'corpus'
        language = 'de'
        reader = Reader(os.path.join(self.tempdir_blogger_corp, self.txt_blogger_small_fake_set), 'txt', regex_template='blogger', mode=self.mode)
        corp = Corpus(logger_traceback=True, status_bar=True, mode=self.mode, use_test_pos_tagger=True)
        corp.init(self.tempdir_project_folder, name, language, visibility, platform_name, source=source, license=license, template_name=template_name, version=version, corpus_id=corpus_id, preprocession=preprocession, tokenizer=tokenizer, sent_splitter=sent_splitter, pos_tagger=pos_tagger, sentiment_analyzer=sentiment_analyzer, lang_classification=lang_classification, del_url=del_url, del_punkt=del_punkt, del_num=del_num, del_mention=del_mention, del_hashtag=del_hashtag, del_html=del_html, case_sensitiv=case_sensitiv)
        corp.insert([self.input_list_blogger_corpus_high_repetativ_subset[:1], self.input_list_blogger_corpus_high_repetativ_subset[1:]])
        assert corp.total_inserted_during_last_insert != len(self.input_list_blogger_corpus_high_repetativ_subset) and False
        assert corp.total_inserted_during_last_insert == len(self.input_list_blogger_corpus_high_repetativ_subset)
        assert corp.total_error_insertion_during_last_insertion_process == 0
        assert corp.total_ignored_last_insertion == 0

    @attr(status='stable')
    def test_insert_parallel_many_threads_on_example_of_twitter_corp_556(self):
        self.prj_folder()
        self.twitter_corpus()
        name = self.configer.init_info_data['twitter']['name']
        language = self.configer.init_info_data['twitter']['language']
        visibility = self.configer.init_info_data['twitter']['visibility']
        platform_name = self.configer.init_info_data['twitter']['platform_name']
        license = self.configer.init_info_data['twitter']['license']
        template_name = self.configer.init_info_data['twitter']['template_name']
        version = self.configer.init_info_data['twitter']['version']
        source = self.configer.init_info_data['twitter']['source']
        encryption_key = self.configer.init_info_data['twitter']['encryption_key']['corpus']
        corpus_id = self.configer.init_info_data['twitter']['id']['corpus']
        stats_id = self.configer.init_info_data['twitter']['id']['stats']
        typ = 'corpus'
        language = 'de'
        preprocession = True
        tokenizer = True
        pos_tagger = False
        sent_splitter = True
        del_url = True
        del_punkt = True
        del_num = True
        case_sensitiv = False
        typ = 'corpus'
        language = 'en'
        sentiment_analyzer = True
        lang_classification = False
        del_mention = True
        del_hashtag = True
        del_html = True
        reader = Reader(os.path.join(self.tempdir_twitter_corp, self.json_twitter_set), 'json', formatter_name='twitterstreamapi', logger_traceback=True, ext_tb=True, mode=self.mode)
        corp = Corpus(logger_traceback=True, status_bar=True, mode=self.mode, use_test_pos_tagger=True)
        corp.init(self.tempdir_project_folder, name, language, visibility, platform_name, source=source, license=license, template_name=template_name, version=version, corpus_id=corpus_id, preprocession=preprocession, tokenizer=tokenizer, sent_splitter=sent_splitter, pos_tagger=pos_tagger, sentiment_analyzer=sentiment_analyzer, lang_classification=lang_classification, del_url=del_url, del_punkt=del_punkt, del_num=del_num, del_mention=del_mention, del_hashtag=del_hashtag, del_html=del_html, case_sensitiv=case_sensitiv)
        corp.insert(reader.getlazy())
        assert corp.total_error_insertion_during_last_insertion_process == 0

    @attr(status='stable')
    def test_get_docs_single_600(self):
        self.prj_folder()
        self.test_dbs()
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['corpus']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'corpus'
        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_en))
        inp_dict = self.configer.docs_row_dict(token=True, unicode_str=True, all_values=True)['blogger']
        num_of_insertions = len(random.choice(inp_dict.values()))
        columns = inp_dict.keys()
        rows = inp_dict.values()
        id_index = self.configer.columns_in_doc_table['blogger'].index('id')
        text_index = self.configer.columns_in_doc_table['blogger'].index('text')
        number_of_rows_in_db = corp.corpdb.rownum('documents')
        docs_row_values = self.configer.docs_row_values(token=True, unicode_str=True, lang='en')
        number_of_values = len(docs_row_values['blogger'])
        number_of_rows_in_input = len(docs_row_values['blogger'])
        assert number_of_rows_in_db != number_of_rows_in_input and False
        rows_from_db = []
        count = 0
        for row_from_db in corp.docs(stream_number=1, adjust_to_cpu=False):
            rows_from_db.append(row_from_db)
            count += 1

        assert count == number_of_rows_in_db
        for row_from_db, row_from_input in zip(rows_from_db, docs_row_values['blogger']):
            i = 0
            while i < number_of_values:
                if i == text_index:
                    pass
                else:
                    assert row_from_db[i] == row_from_input[i]
                i += 1

    @attr(status='stable')
    def test_get_docs_many_streams_601(self):
        self.prj_folder()
        self.test_dbs()
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['corpus']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'corpus'
        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_en))
        inp_dict = self.configer.docs_row_dict(token=True, unicode_str=True, all_values=True, lang='en')['blogger']
        num_of_insertions = len(random.choice(inp_dict.values()))
        columns = inp_dict.keys()
        rows = inp_dict.values()
        id_index = self.configer.columns_in_doc_table['blogger'].index('id')
        text_index = self.configer.columns_in_doc_table['blogger'].index('text')
        number_of_rows = corp.corpdb.rownum('documents')
        docs_row_values = self.configer.docs_row_values(token=True, unicode_str=True, lang='en')
        assert number_of_rows != len(docs_row_values['blogger']) and False
        len(corp.docs(stream_number=4, adjust_to_cpu=True, min_files_pro_stream=number_of_rows + 1)).should.be.equal(get_number_of_streams_adjust_cpu(number_of_rows + 1, number_of_rows, 4))
        len([ row for gen in corp.docs(stream_number=4, adjust_to_cpu=True, min_files_pro_stream=number_of_rows + 1) for row in gen ]).should.be.equal(number_of_rows)
        len(corp.docs(stream_number=4, adjust_to_cpu=True, min_files_pro_stream=number_of_rows)).should.be.equal(get_number_of_streams_adjust_cpu(number_of_rows, number_of_rows, 4))
        len([ row for gen in corp.docs(stream_number=4, adjust_to_cpu=True, min_files_pro_stream=number_of_rows) for row in gen ]).should.be.equal(number_of_rows)
        len(corp.docs(stream_number=4, adjust_to_cpu=True, min_files_pro_stream=number_of_rows - 1)).should.be.equal(get_number_of_streams_adjust_cpu(number_of_rows - 1, number_of_rows, 4))
        len([ row for gen in corp.docs(stream_number=4, adjust_to_cpu=True, min_files_pro_stream=number_of_rows - 1) for row in gen ]).should.be.equal(number_of_rows)
        len(corp.docs(stream_number=4, adjust_to_cpu=True, min_files_pro_stream=4)).should.be.equal(get_number_of_streams_adjust_cpu(4, number_of_rows, 4))
        len([ row for gen in corp.docs(stream_number=4, adjust_to_cpu=True, min_files_pro_stream=4) for row in gen ]).should.be.equal(number_of_rows)
        len(corp.docs(stream_number=4, adjust_to_cpu=True, min_files_pro_stream=3)).should.be.equal(get_number_of_streams_adjust_cpu(3, number_of_rows, 4))
        len([ row for gen in corp.docs(stream_number=4, adjust_to_cpu=True, min_files_pro_stream=3) for row in gen ]).should.be.equal(number_of_rows)
        len(corp.docs(stream_number=4, adjust_to_cpu=True, min_files_pro_stream=2)).should.be.equal(get_number_of_streams_adjust_cpu(2, number_of_rows, 4))
        len([ row for gen in corp.docs(stream_number=4, adjust_to_cpu=True, min_files_pro_stream=2) for row in gen ]).should.be.equal(number_of_rows)
        len(corp.docs(stream_number=4, adjust_to_cpu=True, min_files_pro_stream=1)).should.be.equal(get_number_of_streams_adjust_cpu(1, number_of_rows, 4))
        len([ row for gen in corp.docs(stream_number=4, adjust_to_cpu=True, min_files_pro_stream=1) for row in gen ]).should.be.equal(number_of_rows)
        len(corp.docs(stream_number=4, adjust_to_cpu=True, min_files_pro_stream=0)).should.be.equal(get_number_of_streams_adjust_cpu(0, number_of_rows, 4))
        len([ row for gen in corp.docs(stream_number=4, adjust_to_cpu=True, min_files_pro_stream=0) for row in gen ]).should.be.equal(number_of_rows)
        rows_from_db = []
        for gen in corp.docs(stream_number=4, adjust_to_cpu=True, min_files_pro_stream=2):
            for row_from_db in gen:
                rows_from_db.append(row_from_db)

        assert len(rows_from_db) == len(docs_row_values['blogger'])
        number_of_values = len(docs_row_values['blogger'][0])
        for row_from_db, row_from_input in zip(rows_from_db, docs_row_values['blogger']):
            i = 0
            while i < number_of_values:
                if i == text_index:
                    pass
                else:
                    assert row_from_db[i] == row_from_input[i]
                i += 1

    def _init_variables_for_preprocessing_test(self):
        self.test_byte_str_en_1 = 'I loved it. But it was verrrryyyyy vvveRRRRRRrry very piiiiiiiiity pity pity piiitttyyy for me...... :-(((((  @real_trump #sheetlife #readytogo http://www.absurd.com'
        self.test_byte_str_en_2 = 'a baddddd bad bbbbbbbaaaaaad bbbbaaaaddddd baaaaaaad news, which we can not accept. -(((( 😫😫😫😫 😫😫😫😫😫 😫😫😫 #sheetlife #sheetlife http://www.noooo.com'
        self.test_unicode_str_en_1 = self.test_byte_str_en_1.decode('utf-8')
        self.test_unicode_str_en_1_tokenized_not_cleaned_with_emoji_normalization = [([('I', 'regular'), ('loved', 'regular'), ('it', 'regular'), ('.', 'symbol'), ('But', 'regular'), ('it', 'regular'), ('was', 'regular'), ('verrrryyyyy', 'regular'), ('vvveRRRRRRrry', 'regular'), ('very', 'regular'), ('piiiiiiiiity', 'regular'), ('pity', 'regular'), ('pity', 'regular'), ('piiitttyyy', 'regular'), ('for', 'regular'), ('me', 'regular'), ('......', 'symbol'), (':-(((((', 'EMOASC'), ('@real_trump', 'mention'), ('#sheetlife', 'hashtag'), ('#readytogo', 'hashtag'), ('http://www.absurd.com', 'URL')], (None, None))]
        self.test_unicode_str_en_1_tokenized_not_cleaned_without_emoji_normalization = [([('I', 'regular'), ('loved', 'regular'), ('it', 'regular'), ('.', 'symbol'), ('But', 'regular'), ('it', 'regular'), ('was', 'regular'), ('verrrryyyyy', 'regular'), ('vvveRRRRRRrry', 'regular'), ('very', 'regular'), ('piiiiiiiiity', 'regular'), ('pity', 'regular'), ('pity', 'regular'), ('piiitttyyy', 'regular'), ('for', 'regular'), ('me', 'regular'), ('......', 'symbol'), (':-(((((', 'EMOASC'), ('@real_trump', 'mention'), ('#sheetlife', 'hashtag'), ('#readytogo', 'hashtag'), ('http://www.absurd.com', 'URL')], (None, None))]
        assert self.test_unicode_str_en_1_tokenized_not_cleaned_with_emoji_normalization == self.test_unicode_str_en_1_tokenized_not_cleaned_without_emoji_normalization
        self.test_unicode_str_en_1_tokenized_cleaned = [([('I', 'regular'), ('loved', 'regular'), ('it', 'regular'), (None, ':symbol:'), ('But', 'regular'), ('it', 'regular'), ('was', 'regular'), ('verrrryyyyy', 'regular'), ('vvveRRRRRRrry', 'regular'), ('very', 'regular'), ('piiiiiiiiity', 'regular'), ('pity', 'regular'), ('pity', 'regular'), ('piiitttyyy', 'regular'), ('for', 'regular'), ('me', 'regular'), (None, ':symbol:'), (':-(((((', 'EMOASC'), (None, ':mention:'), (None, ':hashtag:'), (None, ':hashtag:'), (None, ':URL:')], (None, None))]
        self.test_unicode_str_en_2 = self.test_byte_str_en_2.decode('utf-8')
        self.test_unicode_str_en_2_tokenized_not_cleaned_with_emoji_normalization = [([('a', 'regular'), ('baddddd', 'regular'), ('bad', 'regular'), ('bbbbbbbaaaaaad', 'regular'), ('bbbbaaaaddddd', 'regular'), ('baaaaaaad', 'regular'), ('news', 'regular'), (',', 'symbol'), ('which', 'regular'), ('we', 'regular'), ('can', 'regular'), ('not', 'regular'), ('accept', 'regular'), ('.', 'symbol'), ('-((((', 'EMOASC'), ('😫😫😫😫😫😫😫😫😫😫😫😫', 'EMOIMG'), ('#sheetlife', 'hashtag'), ('#sheetlife', 'hashtag'), ('http://www.noooo.com', 'URL')], (None, None))]
        self.test_unicode_str_en_2_tokenized_not_cleaned_without_emoji_normalization = [([('a', 'regular'), ('baddddd', 'regular'), ('bad', 'regular'), ('bbbbbbbaaaaaad', 'regular'), ('bbbbaaaaddddd', 'regular'), ('baaaaaaad', 'regular'), ('news', 'regular'), (',', 'symbol'), ('which', 'regular'), ('we', 'regular'), ('can', 'regular'), ('not', 'regular'), ('accept', 'regular'), ('.', 'symbol'), ('-((((', 'EMOASC'), ('😫', 'EMOIMG'), ('😫', 'EMOIMG'), ('😫', 'EMOIMG'), ('😫', 'EMOIMG'), ('😫', 'EMOIMG'), ('😫', 'EMOIMG'), ('😫', 'EMOIMG'), ('😫', 'EMOIMG'), ('😫', 'EMOIMG'), ('😫', 'EMOIMG'), ('😫', 'EMOIMG'), ('😫', 'EMOIMG'), ('#sheetlife', 'hashtag'), ('#sheetlife', 'hashtag'), ('http://www.noooo.com', 'URL')], (None, None))]
        assert self.test_unicode_str_en_2_tokenized_not_cleaned_with_emoji_normalization != self.test_unicode_str_en_2_tokenized_not_cleaned_without_emoji_normalization
        self.test_unicode_str_en_2_tokenized_cleaned = [([('a', 'regular'), ('baddddd', 'regular'), ('bad', 'regular'), ('bbbbbbbaaaaaad', 'regular'), ('bbbbaaaaddddd', 'regular'), ('baaaaaaad', 'regular'), ('news', 'regular'), (None, ':symbol:'), ('which', 'regular'), ('we', 'regular'), ('can', 'regular'), ('not', 'regular'), ('accept', 'regular'), (None, ':symbol:'), ('-((((', 'EMOASC'), ('😫😫😫😫😫😫😫😫😫😫😫😫', 'EMOIMG'), (None, ':hashtag:'), (None, ':hashtag:'), (None, ':URL:')], (None, None))]
        self.test_unicode_str_en_2_tokenized_not_cleaned_without_emoji_normalization
        self.test_byte_str_de_1 = 'einen wunderschönen Taaaaaagggggg wünsche ich euch 😀😀😀😀😀🌈🌈🌈🌈🌈🌈🌈 Genieeeeeeeeeeesst das Leben. Bleeeeeeeeibt bleeeeibt Huuuuuuuuuuuungrig. '
        self.test_byte_str_de_2 = 'eine klitzeeee kleine Sache.  Die aber trotzdem wichtiiiiiiiig isssssst! 11111 2222 33333 4444 55555'
        self.test_unicode_str_de_1 = self.test_byte_str_de_1.decode('utf-8')
        self.test_unicode_str_de_1_tokenized_not_cleaned_with_emoji_normalization = [([('einen', 'regular'), ('wunderschönen', 'regular'), ('Taaaaaagggggg', 'regular'), ('wünsche', 'regular'), ('ich', 'regular'), ('euch', 'regular'), ('😀😀😀😀😀', 'EMOIMG'), ('🌈🌈🌈🌈🌈🌈🌈', 'EMOIMG'), ('Genieeeeeeeeeeesst', 'regular'), ('das', 'regular'), ('Leben', 'regular'), ('.', 'symbol'), ('Bleeeeeeeeibt', 'regular'), ('bleeeeibt', 'regular'), ('Huuuuuuuuuuuungrig', 'regular'), ('.', 'symbol')], (None, None))]
        self.test_unicode_str_de_1_tokenized_not_cleaned_without_emoji_normalization = [([('einen', 'regular'), ('wunderschönen', 'regular'), ('Taaaaaagggggg', 'regular'), ('wünsche', 'regular'), ('ich', 'regular'), ('euch', 'regular'), ('😀', 'EMOIMG'), ('😀', 'EMOIMG'), ('😀', 'EMOIMG'), ('😀', 'EMOIMG'), ('😀', 'EMOIMG'), ('🌈', 'EMOIMG'), ('🌈', 'EMOIMG'), ('🌈', 'EMOIMG'), ('🌈', 'EMOIMG'), ('🌈', 'EMOIMG'), ('🌈', 'EMOIMG'), ('🌈', 'EMOIMG'), ('Genieeeeeeeeeeesst', 'regular'), ('das', 'regular'), ('Leben', 'regular'), ('.', 'symbol'), ('Bleeeeeeeeibt', 'regular'), ('bleeeeibt', 'regular'), ('Huuuuuuuuuuuungrig', 'regular'), ('.', 'symbol')], (None, None))]
        self.test_unicode_str_de_1_tokenized_cleaned = [([('einen', 'regular'), ('wunderschönen', 'regular'), ('Taaaaaagggggg', 'regular'), ('wünsche', 'regular'), ('ich', 'regular'), ('euch', 'regular'), ('😀😀😀😀😀', 'EMOIMG'), ('🌈🌈🌈🌈🌈🌈🌈', 'EMOIMG'), ('Genieeeeeeeeeeesst', 'regular'), ('das', 'regular'), ('Leben', 'regular'), (None, ':symbol:'), ('Bleeeeeeeeibt', 'regular'), ('bleeeeibt', 'regular'), ('Huuuuuuuuuuuungrig', 'regular'), (None, ':symbol:')], (None, None))]
        self.test_unicode_str_de_2 = self.test_byte_str_de_2.decode('utf-8')
        self.test_unicode_str_de_2_tokenized_not_cleaned_with_emoji_normalization = [([('eine', 'regular'), ('klitzeeee', 'regular'), ('kleine', 'regular'), ('Sache', 'regular'), ('.', 'symbol'), ('Die', 'regular'), ('aber', 'regular'), ('trotzdem', 'regular'), ('wichtiiiiiiiig', 'regular'), ('isssssst', 'regular'), ('!', 'symbol'), ('11111', 'number'), ('2222', 'number'), ('33333', 'number'), ('4444', 'number'), ('55555', 'number')], (None, None))]
        self.test_unicode_str_de_2_tokenized_not_cleaned_without_emoji_normalization = [([('eine', 'regular'), ('klitzeeee', 'regular'), ('kleine', 'regular'), ('Sache', 'regular'), ('.', 'symbol'), ('Die', 'regular'), ('aber', 'regular'), ('trotzdem', 'regular'), ('wichtiiiiiiiig', 'regular'), ('isssssst', 'regular'), ('!', 'symbol'), ('11111', 'number'), ('2222', 'number'), ('33333', 'number'), ('4444', 'number'), ('55555', 'number')], (None, None))]
        self.test_unicode_str_de_2_tokenized_cleaned = [([('eine', 'regular'), ('klitzeeee', 'regular'), ('kleine', 'regular'), ('Sache', 'regular'), (None, ':symbol:'), ('Die', 'regular'), ('aber', 'regular'), ('trotzdem', 'regular'), ('wichtiiiiiiiig', 'regular'), ('isssssst', 'regular'), (None, ':symbol:'), (None, ':number:'), (None, ':number:'), (None, ':number:'), (None, ':number:'), (None, ':number:')], (None, None))]
        return

    def _get_test_corp(self, preprocession=False, tokenizer=False, sent_splitter=False, pos_tagger=False, sentiment_analyzer=False, lang_classification=False, lang='en', status_bar=False, mode='test', init=False, clean=True, emojis_normalization=True, use_test_pos_tagger=True):
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['corpus']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        preprocession = preprocession
        tokenizer = tokenizer
        pos_tagger = pos_tagger
        sent_splitter = sent_splitter
        sentiment_analyzer = sentiment_analyzer
        lang_classification = lang_classification
        status_bar = status_bar
        if clean:
            del_url = True
            del_punkt = True
            del_num = True
            del_html = True
            del_mention = True
            del_hashtag = True
        else:
            del_url = False
            del_punkt = False
            del_num = False
            del_html = False
            del_mention = False
            del_hashtag = False
        case_sensitiv = True
        typ = 'corpus'
        language = lang
        corp = Corpus(logger_traceback=True, status_bar=status_bar, mode=self.mode, use_test_pos_tagger=True)
        if not init:
            return corp
        else:
            corp.init(self.tempdir_project_folder, name, language, visibility, platform_name, source=source, license=license, template_name=template_name, version=version, corpus_id=corpus_id, preprocession=preprocession, tokenizer=tokenizer, sent_splitter=sent_splitter, pos_tagger=pos_tagger, sentiment_analyzer=sentiment_analyzer, lang_classification=lang_classification, del_url=del_url, del_punkt=del_punkt, del_num=del_num, del_mention=del_mention, emojis_normalization=emojis_normalization, del_hashtag=del_hashtag, del_html=del_html, case_sensitiv=case_sensitiv)
            return corp

    def _check_sents_structure(self, sents):
        for sent_container in sents:
            try:
                sent_container[0]
                sent_container[1]
                assert True
            except KeyError:
                assert False
                try:
                    sent_container[1][0]
                    sent_container[1][1]
                    assert True
                except KeyError:
                    assert False

                assert len(sent_container[1]) == 2

            for token_contaner in sent_container[0]:
                try:
                    token_contaner[0]
                    token_contaner[1]
                except KeyError:
                    assert False

    def _check_en_sentences(self, corp):
        sents = corp._preprocessing("Hey, what's up???. Wanna meet?")
        len(sents).should.be.equal(2)
        sents1 = corp._preprocessing(self.test_unicode_str_en_1)
        len(sents1).should.be.equal(2)
        self._check_sents_structure(sents1)
        tokens_after_preprocessing = [ token_contaner[0] for sent_container in sents1 for token_contaner in sent_container[0] ]
        joined_sent_after_preproc = ('').join(tokens_after_preprocessing)
        joined_sent_bevore_preproc = ('').join(self.test_unicode_str_en_1.split(' '))
        joined_sent_after_preproc.should.be.equal(joined_sent_bevore_preproc)
        sents2 = corp._preprocessing(self.test_unicode_str_en_2)
        len(sents2).should.be.equal(1)
        self._check_sents_structure(sents2)
        tokens_after_preprocessing = [ token_contaner[0] for sent_container in sents2 for token_contaner in sent_container[0] ]
        joined_sent_after_preproc = ('').join(tokens_after_preprocessing)
        joined_sent_bevore_preproc = ('').join(self.test_unicode_str_en_2.split(' '))
        joined_sent_after_preproc.should.be.equal(joined_sent_bevore_preproc)

    def _check_de_sentences(self, corp):
        sents = corp._preprocessing('Hey, Was geeeeht??. Wollennnn wa chatenn?')
        len(sents).should.be.equal(2)
        sents1 = corp._preprocessing(self.test_unicode_str_de_1)
        len(sents1).should.be.equal(2)
        self._check_sents_structure(sents1)
        tokens_after_preprocessing = [ token_contaner[0] for sent_container in sents1 for token_contaner in sent_container[0] ]
        joined_sent_after_preproc = ('').join(tokens_after_preprocessing)
        joined_sent_bevore_preproc = ('').join(self.test_unicode_str_de_1.split(' '))
        joined_sent_after_preproc.should.be.equal(joined_sent_bevore_preproc)
        sents2 = corp._preprocessing(self.test_unicode_str_de_2)
        len(sents2).should.be.equal(2)
        self._check_sents_structure(sents2)
        tokens_after_preprocessing = [ token_contaner[0] for sent_container in sents2 for token_contaner in sent_container[0] ]
        joined_sent_after_preproc = ('').join(tokens_after_preprocessing)
        joined_sent_bevore_preproc = ('').join(self.test_unicode_str_de_2.split(' '))
        joined_sent_after_preproc.should.be.equal(joined_sent_bevore_preproc)

    def _check_en_sentence(self, corp):
        sents = corp._preprocessing("Hey, what's up???. Wanna meet?")
        len(sents).should.be.equal(1)
        sents1 = corp._preprocessing(self.test_unicode_str_en_1)
        len(sents1).should.be.equal(1)
        self._check_sents_structure(sents1)
        tokens_after_preprocessing = [ token_contaner[0] for sent_container in sents1 for token_contaner in sent_container[0] ]
        joined_sent_after_preproc = ('').join(tokens_after_preprocessing)
        joined_sent_bevore_preproc = ('').join(self.test_unicode_str_en_1.split(' '))
        joined_sent_after_preproc.should.be.equal(joined_sent_bevore_preproc)
        sents2 = corp._preprocessing(self.test_unicode_str_en_2)
        len(sents2).should.be.equal(1)
        self._check_sents_structure(sents2)
        tokens_after_preprocessing = [ token_contaner[0] for sent_container in sents2 for token_contaner in sent_container[0] ]
        joined_sent_after_preproc = ('').join(tokens_after_preprocessing)
        joined_sent_bevore_preproc = ('').join(self.test_unicode_str_en_2.split(' '))
        joined_sent_after_preproc.should.be.equal(joined_sent_bevore_preproc)

    def _check_de_sentence(self, corp):
        sents = corp._preprocessing('Hey, Was geeeeht??. Wollennnn wa chatenn?')
        len(sents).should.be.equal(1)
        sents1 = corp._preprocessing(self.test_unicode_str_de_1)
        len(sents1).should.be.equal(1)
        self._check_sents_structure(sents1)
        tokens_after_preprocessing = [ token_contaner[0] for sent_container in sents1 for token_contaner in sent_container[0] ]
        joined_sent_after_preproc = ('').join(tokens_after_preprocessing)
        joined_sent_bevore_preproc = ('').join(self.test_unicode_str_de_1.split(' '))
        joined_sent_after_preproc.should.be.equal(joined_sent_bevore_preproc)
        sents2 = corp._preprocessing(self.test_unicode_str_de_2)
        len(sents2).should.be.equal(1)
        self._check_sents_structure(sents2)
        tokens_after_preprocessing = [ token_contaner[0] for sent_container in sents2 for token_contaner in sent_container[0] ]
        joined_sent_after_preproc = ('').join(tokens_after_preprocessing)
        joined_sent_bevore_preproc = ('').join(self.test_unicode_str_de_2.split(' '))
        joined_sent_after_preproc.should.be.equal(joined_sent_bevore_preproc)

    @attr(status='stable')
    def test_preprocessors_if_preproc_are_disabled_700(self):
        self.prj_folder()
        self._init_variables_for_preprocessing_test()
        mode = self.mode
        corp = self._get_test_corp(preprocession=False, tokenizer=False, sent_splitter=False, pos_tagger=False, sentiment_analyzer=False, lang_classification=False, lang='en', mode=mode, init=True)
        answer1 = corp._init_preprocessors()
        answer1['status'].should.be.equal(False)
        answer1['desc'].should.be.equal('PreprocessorsWasDisabled')

    @attr(status='stable')
    def test_preprocessors_with_enabled_tokenizer_not_clean_with_emoji_normalization_702(self):
        self.prj_folder()
        self._init_variables_for_preprocessing_test()
        mode = self.mode
        corp = self._get_test_corp(preprocession=True, tokenizer=True, sent_splitter=False, pos_tagger=False, sentiment_analyzer=False, lang_classification=False, lang='en', mode=mode, init=True, clean=False, emojis_normalization=True, status_bar=False)
        corp._init_insertions_variables()
        answer1 = corp._init_preprocessors()
        answer1['status'].should.be.equal(True)
        answer1['desc'].should.be.equal(1)
        corp._preprocessing(self.test_byte_str_en_1).should.be.equal(self.test_unicode_str_en_1_tokenized_not_cleaned_with_emoji_normalization)
        corp._preprocessing(self.test_byte_str_en_2).should.be.equal(self.test_unicode_str_en_2_tokenized_not_cleaned_with_emoji_normalization)
        corp._preprocessing(self.test_unicode_str_en_1).should.be.equal(self.test_unicode_str_en_1_tokenized_not_cleaned_with_emoji_normalization)
        corp._preprocessing(self.test_unicode_str_en_2).should.be.equal(self.test_unicode_str_en_2_tokenized_not_cleaned_with_emoji_normalization)
        mode = self.mode
        corp = self._get_test_corp(preprocession=True, tokenizer=True, sent_splitter=False, pos_tagger=False, sentiment_analyzer=False, lang_classification=False, lang='de', mode=mode, init=True, clean=False, emojis_normalization=True)
        corp._init_insertions_variables()
        answer1 = corp._init_preprocessors()
        answer1['status'].should.be.equal(True)
        answer1['desc'].should.be.equal(1)
        corp._preprocessing(self.test_byte_str_de_1).should.be.equal(self.test_unicode_str_de_1_tokenized_not_cleaned_with_emoji_normalization)
        corp._preprocessing(self.test_byte_str_de_2).should.be.equal(self.test_unicode_str_de_2_tokenized_not_cleaned_with_emoji_normalization)
        corp._preprocessing(self.test_unicode_str_de_1).should.be.equal(self.test_unicode_str_de_1_tokenized_not_cleaned_with_emoji_normalization)
        corp._preprocessing(self.test_unicode_str_de_2).should.be.equal(self.test_unicode_str_de_2_tokenized_not_cleaned_with_emoji_normalization)
        output = corp._preprocessing(':-)))) -))) 😀😀😀😀😀-))) -)))')
        right_output = [([(':-))))', 'EMOASC'), ('-)))', 'EMOASC'), ('😀😀😀😀😀', 'EMOIMG'), ('-)))', 'EMOASC'), ('-)))', 'EMOASC')], (None, None))]
        output.should.be.equal(right_output)
        output = corp._preprocessing('@RonetteJaye That sounds a++++ (((:')
        right_output = [([('@RonetteJaye', 'mention'), ('That', 'regular'), ('sounds', 'regular'), ('a++++', 'regular'), ('(((:', 'EMOASC')], (None, None))]
        output.should.be.equal(right_output)
        output = corp._preprocessing(' (((==== ===)))))')
        right_output = [([('(((=======)))))', 'EMOASC')], (None, None))]
        output.should.be.equal(right_output)
        output = corp._preprocessing(' (((====  (((===')
        right_output = [([('(((====', 'EMOASC'), ('(((===', 'EMOASC')], (None, None))]
        output.should.be.equal(right_output)
        output = corp._preprocessing(' (((====  :))))))  .))))')
        right_output = [([('(((====', 'EMOASC'), (':))))))', 'EMOASC'), ('.', 'symbol'), ('))))', 'EMOASC')], (None, None))]
        output.should.be.equal(right_output)
        output = corp._preprocessing(' :)))) --))))) ;;;;))))) --;;;)))) :::----)))) ---=====(((())))  :))))))  .))))')
        right_output = [([(':))))', 'EMOASC'), ('--)))))', 'EMOASC'), (';;;;)))))', 'EMOASC'), ('--;;;))))', 'EMOASC'), (':::----))))', 'EMOASC'), ('---=====((((', 'EMOASC'), (')))):))))))', 'EMOASC'), ('.', 'symbol'), ('))))', 'EMOASC')], (None, None))]
        output.should.be.equal(right_output)
        return

    @attr(status='stable')
    def test_preprocessors_with_enabled_tokenizer_without_not_clean_without_emoji_normalization_703(self):
        self.prj_folder()
        self._init_variables_for_preprocessing_test()
        mode = self.mode
        corp = self._get_test_corp(preprocession=True, tokenizer=True, sent_splitter=False, pos_tagger=False, sentiment_analyzer=False, lang_classification=False, lang='en', mode=mode, init=True, clean=False, emojis_normalization=False)
        corp._init_insertions_variables()
        answer1 = corp._init_preprocessors()
        answer1['status'].should.be.equal(True)
        answer1['desc'].should.be.equal(1)
        corp._preprocessing(self.test_byte_str_en_1).should.be.equal(self.test_unicode_str_en_1_tokenized_not_cleaned_without_emoji_normalization)
        corp._preprocessing(self.test_byte_str_en_2).should.be.equal(self.test_unicode_str_en_2_tokenized_not_cleaned_without_emoji_normalization)
        corp._preprocessing(self.test_unicode_str_en_1).should.be.equal(self.test_unicode_str_en_1_tokenized_not_cleaned_without_emoji_normalization)
        corp._preprocessing(self.test_unicode_str_en_2).should.be.equal(self.test_unicode_str_en_2_tokenized_not_cleaned_without_emoji_normalization)
        mode = self.mode
        corp = self._get_test_corp(preprocession=True, tokenizer=True, sent_splitter=False, pos_tagger=False, sentiment_analyzer=False, lang_classification=False, lang='de', mode=mode, init=True, clean=False, emojis_normalization=False)
        corp._init_insertions_variables()
        answer1 = corp._init_preprocessors()
        answer1['status'].should.be.equal(True)
        answer1['desc'].should.be.equal(1)
        corp._preprocessing(self.test_byte_str_de_1).should.be.equal(self.test_unicode_str_de_1_tokenized_not_cleaned_without_emoji_normalization)
        corp._preprocessing(self.test_byte_str_de_2).should.be.equal(self.test_unicode_str_de_2_tokenized_not_cleaned_without_emoji_normalization)
        corp._preprocessing(self.test_unicode_str_de_1).should.be.equal(self.test_unicode_str_de_1_tokenized_not_cleaned_without_emoji_normalization)
        corp._preprocessing(self.test_unicode_str_de_2).should.be.equal(self.test_unicode_str_de_2_tokenized_not_cleaned_without_emoji_normalization)

    @attr(status='stable')
    def test_preprocessors_with_enabled_tokenizer_with_clean_704(self):
        self.prj_folder()
        self._init_variables_for_preprocessing_test()
        mode = self.mode
        corp = self._get_test_corp(preprocession=True, tokenizer=True, sent_splitter=False, pos_tagger=False, sentiment_analyzer=False, lang_classification=False, lang='en', mode=mode, init=True, clean=True)
        corp._init_insertions_variables()
        answer1 = corp._init_preprocessors()
        answer1['status'].should.be.equal(True)
        answer1['desc'].should.be.equal(1)
        corp._preprocessing(self.test_byte_str_en_1).should.be.equal(self.test_unicode_str_en_1_tokenized_cleaned)
        corp._preprocessing(self.test_byte_str_en_2).should.be.equal(self.test_unicode_str_en_2_tokenized_cleaned)
        corp._preprocessing(self.test_unicode_str_en_1).should.be.equal(self.test_unicode_str_en_1_tokenized_cleaned)
        corp._preprocessing(self.test_unicode_str_en_2).should.be.equal(self.test_unicode_str_en_2_tokenized_cleaned)
        mode = self.mode
        corp = self._get_test_corp(preprocession=True, tokenizer=True, sent_splitter=False, pos_tagger=False, sentiment_analyzer=False, lang_classification=False, lang='de', mode=mode, init=True, clean=True)
        corp._init_insertions_variables()
        answer1 = corp._init_preprocessors()
        answer1['status'].should.be.equal(True)
        answer1['desc'].should.be.equal(1)
        corp._preprocessing(self.test_byte_str_de_1).should.be.equal(self.test_unicode_str_de_1_tokenized_cleaned)
        corp._preprocessing(self.test_byte_str_de_2).should.be.equal(self.test_unicode_str_de_2_tokenized_cleaned)
        corp._preprocessing(self.test_unicode_str_de_1).should.be.equal(self.test_unicode_str_de_1_tokenized_cleaned)
        corp._preprocessing(self.test_unicode_str_de_2).should.be.equal(self.test_unicode_str_de_2_tokenized_cleaned)

    @attr(status='stable')
    def test_preprocessors_with_enabled_tokenizer_enabled_sentimentanalysis_705(self):
        self.prj_folder()
        self._init_variables_for_preprocessing_test()
        mode = self.mode
        corp = self._get_test_corp(preprocession=True, tokenizer=True, sent_splitter=False, pos_tagger=False, sentiment_analyzer=True, lang_classification=False, lang='en', mode=mode, init=True, clean=False)
        corp._init_insertions_variables()
        answer1 = corp._init_preprocessors()
        answer1['status'].should.be.equal(True)
        answer1['desc'].should.be.equal(2)
        self._check_en_sentence(corp)
        mode = self.mode
        corp = self._get_test_corp(preprocession=True, tokenizer=True, sent_splitter=False, pos_tagger=False, sentiment_analyzer=True, lang_classification=False, lang='de', mode=mode, init=True, clean=False)
        corp._init_insertions_variables()
        answer1 = corp._init_preprocessors()
        answer1['status'].should.be.equal(True)
        answer1['desc'].should.be.equal(2)
        self._check_de_sentence(corp)

    @attr(status='stable')
    def test_preprocessors_with_enabled_tokenizer_enabled_languageclassification_706(self):
        self.prj_folder()
        self._init_variables_for_preprocessing_test()
        mode = self.mode
        corp = self._get_test_corp(preprocession=True, tokenizer=True, sent_splitter=False, pos_tagger=False, sentiment_analyzer=False, lang_classification=True, lang='en', mode=mode, init=True, clean=False)
        corp._init_insertions_variables()
        answer1 = corp._init_preprocessors()
        answer1['status'].should.be.equal(True)
        answer1['desc'].should.be.equal(2)
        self._check_en_sentence(corp)
        mode = self.mode
        corp = self._get_test_corp(preprocession=True, tokenizer=True, sent_splitter=False, pos_tagger=False, sentiment_analyzer=False, lang_classification=True, lang='de', mode=mode, init=True, clean=False)
        corp._init_insertions_variables()
        answer1 = corp._init_preprocessors()
        answer1['status'].should.be.equal(True)
        answer1['desc'].should.be.equal(2)
        self._check_de_sentence(corp)

    @attr(status='stable')
    def test_preprocessors_with_enabled_tokenizer_enabled_sentimentanalysis_enabled_languageclassification_707(self):
        self.prj_folder()
        self._init_variables_for_preprocessing_test()
        mode = self.mode
        corp = self._get_test_corp(preprocession=True, tokenizer=True, sent_splitter=False, pos_tagger=False, sentiment_analyzer=True, lang_classification=True, lang='en', mode=mode, init=True, clean=False)
        corp._init_insertions_variables()
        answer1 = corp._init_preprocessors()
        answer1['status'].should.be.equal(True)
        answer1['desc'].should.be.equal(3)
        self._check_en_sentence(corp)
        mode = self.mode
        corp = self._get_test_corp(preprocession=True, tokenizer=True, sent_splitter=False, pos_tagger=False, sentiment_analyzer=True, lang_classification=True, lang='de', mode=mode, init=True, clean=False)
        corp._init_insertions_variables()
        answer1 = corp._init_preprocessors()
        answer1['status'].should.be.equal(True)
        answer1['desc'].should.be.equal(3)
        self._check_de_sentence(corp)

    @attr(status='stable')
    def test_preprocessors_with_enabled_tokenizer_enabled_sentsplitter_708(self):
        self.prj_folder()
        self._init_variables_for_preprocessing_test()
        mode = self.mode
        corp = self._get_test_corp(preprocession=True, tokenizer=True, sent_splitter=True, pos_tagger=False, sentiment_analyzer=False, lang_classification=False, lang='en', mode=mode, init=True, clean=False)
        corp._init_insertions_variables()
        answer1 = corp._init_preprocessors()
        answer1['status'].should.be.equal(True)
        answer1['desc'].should.be.equal(2)
        self._check_en_sentences(corp)
        mode = self.mode
        corp = self._get_test_corp(preprocession=True, tokenizer=True, sent_splitter=True, pos_tagger=False, sentiment_analyzer=False, lang_classification=False, lang='de', mode=mode, init=True, clean=False)
        corp._init_insertions_variables()
        answer1 = corp._init_preprocessors()
        answer1['status'].should.be.equal(True)
        answer1['desc'].should.be.equal(2)
        self._check_de_sentences(corp)

    @attr(status='stable')
    def test_preprocessors_with_enabled_tokenizer_enabled_sentsplitter_enabled_language_classification_709(self):
        self.prj_folder()
        self._init_variables_for_preprocessing_test()
        mode = self.mode
        corp = self._get_test_corp(preprocession=True, tokenizer=True, sent_splitter=True, pos_tagger=False, sentiment_analyzer=False, lang_classification=True, lang='en', mode=mode, init=True, clean=False)
        corp._init_insertions_variables()
        answer1 = corp._init_preprocessors()
        answer1['status'].should.be.equal(True)
        answer1['desc'].should.be.equal(3)
        sents = corp._preprocessing("Hey, what's up???. Wanna meet?")
        len(sents).should.be.equal(2)
        self._check_en_sentences(corp)
        mode = self.mode
        corp = self._get_test_corp(preprocession=True, tokenizer=True, sent_splitter=True, pos_tagger=False, sentiment_analyzer=False, lang_classification=True, lang='de', mode=mode, init=True, clean=False)
        corp._init_insertions_variables()
        answer1 = corp._init_preprocessors()
        answer1['status'].should.be.equal(True)
        answer1['desc'].should.be.equal(3)
        self._check_de_sentences(corp)

    @attr(status='stable')
    def test_preprocessors_with_enabled_tokenizer_enabled_sentsplitter_enabled_sentimentanalysis_710(self):
        self.prj_folder()
        self._init_variables_for_preprocessing_test()
        mode = self.mode
        corp = self._get_test_corp(preprocession=True, tokenizer=True, sent_splitter=True, pos_tagger=False, sentiment_analyzer=True, lang_classification=False, lang='en', mode=mode, init=True, clean=False)
        corp._init_insertions_variables()
        answer1 = corp._init_preprocessors()
        answer1['status'].should.be.equal(True)
        answer1['desc'].should.be.equal(3)
        sents = corp._preprocessing("Hey, what's up???. Wanna meet?")
        len(sents).should.be.equal(2)
        self._check_en_sentences(corp)
        mode = self.mode
        corp = self._get_test_corp(preprocession=True, tokenizer=True, sent_splitter=True, pos_tagger=False, sentiment_analyzer=True, lang_classification=False, lang='de', mode=mode, init=True, clean=False)
        corp._init_insertions_variables()
        answer1 = corp._init_preprocessors()
        answer1['status'].should.be.equal(True)
        answer1['desc'].should.be.equal(3)
        self._check_de_sentences(corp)

    @attr(status='stable')
    def test_preprocessors_with_enabled_tokenizer_enabled_sentsplitter_enabled_sentimentanalysis_enabled_language_classification_711(self):
        self.prj_folder()
        self._init_variables_for_preprocessing_test()
        mode = self.mode
        corp = self._get_test_corp(preprocession=True, tokenizer=True, sent_splitter=True, pos_tagger=False, sentiment_analyzer=True, lang_classification=True, lang='en', mode=mode, init=True, clean=False)
        corp._init_insertions_variables()
        answer1 = corp._init_preprocessors()
        answer1['status'].should.be.equal(True)
        answer1['desc'].should.be.equal(4)
        self._check_en_sentences(corp)
        mode = self.mode
        corp = self._get_test_corp(preprocession=True, tokenizer=True, sent_splitter=True, pos_tagger=False, sentiment_analyzer=True, lang_classification=True, lang='de', mode=mode, init=True, clean=False)
        corp._init_insertions_variables()
        answer1 = corp._init_preprocessors()
        answer1['status'].should.be.equal(True)
        answer1['desc'].should.be.equal(4)
        self._check_de_sentences(corp)

    @attr(status='stable')
    def test_preprocessors_with_enabled_tokenizer_enabled_sentsplitter_enabled_postagger_712(self):
        self.prj_folder()
        self._init_variables_for_preprocessing_test()
        mode = self.mode
        corp = self._get_test_corp(preprocession=True, tokenizer=True, sent_splitter=True, pos_tagger=True, sentiment_analyzer=False, lang_classification=False, lang='en', mode=mode, init=True, clean=False, status_bar=True)
        corp._init_insertions_variables()
        corp.status_bars_manager = corp._get_status_bars_manager()
        answer1 = corp._init_preprocessors()
        answer1['status'].should.be.equal(True)
        answer1['desc'].should.be.equal(3)
        self._check_en_sentences(corp)
        del corp
        mode = self.mode
        corp = self._get_test_corp(preprocession=True, tokenizer=True, sent_splitter=True, pos_tagger=True, sentiment_analyzer=False, lang_classification=False, lang='de', mode=mode, init=True, clean=False, status_bar=True)
        corp._init_insertions_variables()
        corp.status_bars_manager = corp._get_status_bars_manager()
        answer1 = corp._init_preprocessors()
        answer1['status'].should.be.equal(True)
        answer1['desc'].should.be.equal(3)
        self._check_de_sentences(corp)

    @attr(status='stable')
    def test_preprocessors_with_enabled_tokenizer_enabled_sentsplitter_enabled_postagger_enabled_sentimentanalysis_713(self):
        self.prj_folder()
        self._init_variables_for_preprocessing_test()
        mode = self.mode
        corp = self._get_test_corp(preprocession=True, tokenizer=True, sent_splitter=True, pos_tagger=True, sentiment_analyzer=True, lang_classification=False, lang='en', mode=mode, init=True, clean=False, status_bar=True)
        corp._init_insertions_variables()
        corp.status_bars_manager = corp._get_status_bars_manager()
        answer1 = corp._init_preprocessors()
        answer1['status'].should.be.equal(True)
        answer1['desc'].should.be.equal(4)
        self._check_en_sentences(corp)
        del corp
        mode = self.mode
        corp = self._get_test_corp(preprocession=True, tokenizer=True, sent_splitter=True, pos_tagger=True, sentiment_analyzer=True, lang_classification=False, lang='de', mode=mode, init=True, clean=False, status_bar=True)
        corp._init_insertions_variables()
        corp.status_bars_manager = corp._get_status_bars_manager()
        answer1 = corp._init_preprocessors()
        answer1['status'].should.be.equal(True)
        answer1['desc'].should.be.equal(4)
        self._check_de_sentences(corp)

    @attr(status='stable')
    def test_preprocessors_with_enabled_tokenizer_enabled_sentsplitter_enabled_postagger_enabled_languagesclassification_714(self):
        self.prj_folder()
        self._init_variables_for_preprocessing_test()
        mode = self.mode
        corp = self._get_test_corp(preprocession=True, tokenizer=True, sent_splitter=True, pos_tagger=True, sentiment_analyzer=False, lang_classification=True, lang='en', mode=mode, init=True, clean=False, status_bar=True)
        corp._init_insertions_variables()
        corp.status_bars_manager = corp._get_status_bars_manager()
        answer1 = corp._init_preprocessors()
        answer1['status'].should.be.equal(True)
        answer1['desc'].should.be.equal(4)
        self._check_en_sentences(corp)
        del corp
        mode = self.mode
        corp = self._get_test_corp(preprocession=True, tokenizer=True, sent_splitter=True, pos_tagger=True, sentiment_analyzer=False, lang_classification=True, lang='de', mode=mode, init=True, clean=False, status_bar=True)
        corp._init_insertions_variables()
        corp.status_bars_manager = corp._get_status_bars_manager()
        answer1 = corp._init_preprocessors()
        answer1['status'].should.be.equal(True)
        answer1['desc'].should.be.equal(4)
        self._check_de_sentences(corp)

    @attr(status='stable')
    def test_preprocessors_with_enabled_tokenizer_enabled_sentsplitter_enabled_postagger_enabled_sentimentanalysis_enabled_languagesclassification_715(self):
        self.prj_folder()
        self._init_variables_for_preprocessing_test()
        mode = self.mode
        corp = self._get_test_corp(preprocession=True, tokenizer=True, sent_splitter=True, pos_tagger=True, sentiment_analyzer=True, lang_classification=True, lang='en', mode=mode, init=True, clean=False, status_bar=True, use_test_pos_tagger=True)
        corp._init_insertions_variables()
        corp.status_bars_manager = corp._get_status_bars_manager()
        answer1 = corp._init_preprocessors()
        answer1['status'].should.be.equal(True)
        answer1['desc'].should.be.equal(5)
        self._check_en_sentences(corp)
        del corp
        mode = self.mode
        corp = self._get_test_corp(preprocession=True, tokenizer=True, sent_splitter=True, pos_tagger=True, sentiment_analyzer=True, lang_classification=True, lang='de', mode=mode, init=True, clean=False, status_bar=True)
        corp._init_insertions_variables()
        corp.status_bars_manager = corp._get_status_bars_manager()
        answer1 = corp._init_preprocessors()
        answer1['status'].should.be.equal(True)
        answer1['desc'].should.be.equal(5)
        self._check_de_sentences(corp)

    @attr(status='stable')
    def test_splitter_sentences_in_the_test_corps_730(self):
        self.test_dbs()
        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_de))
        docs = list(corp.docs(output='list'))
        docs_dict = list(corp.docs(output='dict'))
        len(docs).should.be.equal(5)
        [ tokencontainer[0] for sentcontainer in json.loads(docs[0][2]) for tokencontainer in sentcontainer[0] ].should.be.equal(['klitze', 'kliiiitzeeeeeee', 'kleeeeeinnnnne', 'kleinnne', 'überaschung', '.', 'trotzdem', 'hat', 'sie', 'mich', 'glücklich', 'gemacht', '!', ':-))))', '-)))', '😀😀😀😀😀', '-)))', '-)))'])
        len(json.loads(docs[0][2])).should.be.equal(2)
        [ tokencontainer[0] for sentcontainer in json.loads(docs[1][2]) for tokencontainer in sentcontainer[0] ].should.be.equal(['einen', 'wunderschönen', 'taaaaaagggggg', 'wünsche', 'ich', 'euch', '.', 'geniesssstt', 'geniiiiiessssssssttttt', 'das', 'leben', '.', 'bleeeeeeeeibt', 'bleeeeibt', 'huuuuuuuuuuuungrig', '.', 'baseline', 'baseline', 'baseline', 'in', 'in', 'in', 'in', 'baseline', 'baseline', 'baseline', 'in', 'in', 'in', 'in'])
        len(json.loads(docs[1][2])).should.be.equal(3)
        [ tokencontainer[0] for sentcontainer in json.loads(docs[2][2]) for tokencontainer in sentcontainer[0] ].should.be.equal(['eine', 'klitzeeee', 'kleeeeeine', 'überrrraschung', '@schönesleben', '#machwasdaraus', '#bewegedeinarsch', 'https://www.freiesinternet.de', 'besser', 'kannnnnn', 'kaaaannnnn', 'ess', '.', 'kleineeeesssssss', 'kleinnnneeessss', 'kleeeeiiiiinnneesss', 'mädchennnnn', '.....', 'kleinereeeee', 'kleineeerreeeee', 'auswahhhllll', '.', 'klitz', 'kliiiitz', 'kliiiitzzz', 'kleeeiiinnn', 'kleinnnnn', '.', 'klitzessss', 'kliiitzesss', 'kleinnnees', 'kleinessss'])
        len(json.loads(docs[2][2])).should.be.equal(3)
        [ tokencontainer[0] for sentcontainer in json.loads(docs[3][2]) for tokencontainer in sentcontainer[0] ].should.be.equal(['eine', 'klitzeeee', 'kleine', 'sache', '.', 'die', 'aber', 'trotzdem', 'wichtiiiiiiiig', 'isssssst', '!', 'weil', 'es', 'ja', 'eine', 'kleeeeeiinnnneeeee', 'überrrrraschung', 'ist', '.', '11111', '2222', '33333', '4444', '55555', '6', '.', 'kleineeeesssssss', 'kleinnnneeessss', 'kleeeeiiiiinnneesss', 'mädchennnnn', '.....'])
        len(json.loads(docs[3][2])).should.be.equal(4)
        [ tokencontainer[0] for sentcontainer in json.loads(docs[4][2]) for tokencontainer in sentcontainer[0] ].should.be.equal(['eine', 'klitze', 'klitze', 'klitze', 'klitze', 'kleine', 'überrrraschung', ',', 'die', 'ich', 'mal', 'gerne', 'hatte', '.', '111111', '😫😫😫😫', '11111111', 'du', 'meintest', ',', 'es', 'war', 'so', 'eineeee', 'kleeeeiiiiinnnneeeeeeee', 'übeeeerrrrraaaschunnnnnnggg', '.'])
        len(json.loads(docs[4][2])).should.be.equal(1)
        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_en))
        docs = list(corp.docs(output='list'))
        docs_dict = list(corp.docs(output='dict'))
        len(docs).should.be.equal(7)
        [ tokencontainer[0] for sentcontainer in json.loads(docs[0][2]) for tokencontainer in sentcontainer[0] ].should.be.equal(['i', 'loved', 'it', '.', 'but', 'it', 'was', 'also', 'verrrryyyyy', 'vvverrrrrrrry', 'very', 'piiiiiiiiity', 'pity', 'pity', 'piiitttyyy', 'for', 'me', '......', ':-(((((', '@real_trump', '#sheetlife', '#readytogo', 'http://www.absurd.com'])
        len(json.loads(docs[0][2])).should.be.equal(2)
        [ tokencontainer[0] for sentcontainer in json.loads(docs[1][2]) for tokencontainer in sentcontainer[0] ].should.be.equal(['glaaaaaaad', 'to', 'seeeeeeeee', 'you', '-))))'])
        len(json.loads(docs[1][2])).should.be.equal(1)
        [ tokencontainer[0] for sentcontainer in json.loads(docs[2][2]) for tokencontainer in sentcontainer[0] ].should.be.equal(['a', 'baddddd', 'bad', 'bbbbbbbaaaaaad', 'bbbbaaaaddddd', 'baaaaaaad', 'news', ',', 'which', 'we', 'can', 'not', 'accept', '.', '-((((', '😫😫😫😫😫😫😫😫😫😫😫😫', ':-(((((', '#sheetlife', '#sheetlife', 'http://www.noooo.com'])
        len(json.loads(docs[2][2])).should.be.equal(1)
        [ tokencontainer[0] for sentcontainer in json.loads(docs[3][2]) for tokencontainer in sentcontainer[0] ].should.be.equal(['tiny', 'tiny', 'tiny', 'tiny', 'tiny', 'tiny', 'mooooooodelllllll', ',', 'which', 'we', 'can', 'use', 'for', 'explain', 'a', 'biiig', 'biiiiiiiiiiiiiiig', 'things', '.'])
        len(json.loads(docs[3][2])).should.be.equal(1)
        [ tokencontainer[0] for sentcontainer in json.loads(docs[4][2]) for tokencontainer in sentcontainer[0] ].should.be.equal(['tiny', 'model', ',', 'but', 'a', 'big', 'big', 'big', 'explaaaaanation', '.', 'riiiiiight', '?', 'what', 'do', 'youuuuuu', 'think', 'about', 'it', '????', '111111', '😫😫😫😫', '11111111', '.', 'bbbbbuuuutttt', 'buuuuutttt', 'yyyyyyou', 'yoooooou', 'bbbbbbut', 'bbbbbutttt', 'bbbbbuuuuut', 'yyyoouuuu'])
        len(json.loads(docs[4][2])).should.be.equal(4)
        [ tokencontainer[0] for sentcontainer in json.loads(docs[5][2]) for tokencontainer in sentcontainer[0] ].should.be.equal(['tinnnyy', 'tiny', 'tiny', 'surprise', '.', 'bbbbbut', 'buuuuut', 'yyyyyyou', 'yoooooou', 'bbbbbbut', 'bbbbbut', 'bbbbbut', 'yyyoouuuu', '😀😀😀😀😀', '🌈🌈🌈🌈🌈🌈🌈', '😀😀😀😀😀', '🌈🌈🌈🌈🌈🌈🌈', '😀😀😀😀😀'])
        len(json.loads(docs[5][2])).should.be.equal(2)
        [ tokencontainer[0] for sentcontainer in json.loads(docs[6][2]) for tokencontainer in sentcontainer[0] ].should.be.equal(['it', 'was', 'really', 'bad', 'surprise', 'for', 'me', '😫😫😫😫', ',', 'buuuuuuuuuut', 'i', 'really', 'reallly', 'reeeeeallllyyy', 'liked', 'it', ':p', '=))))))))))', '😀😀😀😀😀', '🌈🌈🌈🌈🌈🌈🌈', '😀'])
        len(json.loads(docs[6][2])).should.be.equal(1)

    @attr(status='stable')
    def test_check_results_of_pos_tagging_with_someweta_in_the_test_corps_731(self):
        self.test_dbs()
        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_de))
        docs = list(corp.docs(output='list'))
        docs_dict = list(corp.docs(output='dict'))
        len(docs).should.be.equal(5)
        [ tokencontainer[1] for sentcontainer in json.loads(docs[0][2]) for tokencontainer in sentcontainer[0] ].should.be.equal(['NN', 'VMFIN', 'NE', 'ADJA', 'NN', 'symbol', 'PAV', 'VAFIN', 'PPER', 'PPER', 'ADJD', 'VVPP', 'symbol', 'EMOASC', 'EMOASC', 'EMOIMG', 'EMOASC', 'EMOASC'])
        len(json.loads(docs[0][2])).should.be.equal(2)
        [ tokencontainer[1] for sentcontainer in json.loads(docs[1][2]) for tokencontainer in sentcontainer[0] ].should.be.equal(['ART', 'ADJA', 'NN', 'VVFIN', 'PPER', 'PRF', 'symbol', 'NE', 'VVFIN', 'ART', 'NN', 'symbol', 'NN', 'VVFIN', 'NN', 'symbol', 'NE', 'NE', 'NE', 'APPR', 'APPR', 'NN', 'APPR', 'NE', 'NE', 'NE', 'APPR', 'APPR', 'NN', 'APPR'])
        len(json.loads(docs[1][2])).should.be.equal(3)
        [ tokencontainer[1] for sentcontainer in json.loads(docs[2][2]) for tokencontainer in sentcontainer[0] ].should.be.equal(['ART', 'ADJA', 'ADJA', 'NN', 'mention', 'hashtag', 'hashtag', 'URL', 'ADJD', 'FM', 'NE', 'VVFIN', 'symbol', 'NN', 'ADJA', 'ADJA', 'NN', 'symbol', 'NE', 'ADJA', 'NN', 'symbol', 'NE', 'VMFIN', 'ADR', 'FM', 'FM', 'symbol', 'FM', 'FM', 'FM', 'FM'])
        len(json.loads(docs[2][2])).should.be.equal(3)
        [ tokencontainer[1] for sentcontainer in json.loads(docs[3][2]) for tokencontainer in sentcontainer[0] ].should.be.equal(['ART', 'VAPPER', 'ADJA', 'NN', 'symbol', 'PDS', 'ADV', 'PAV', 'NN', 'VVPP', 'symbol', 'KOUS', 'PPER', 'PTKMA', 'ART', 'ADJA', 'NN', 'VAFIN', 'symbol', 'number', 'number', 'number', 'number', 'number', 'number', 'symbol', 'NN', 'ADJA', 'ADJA', 'NN', 'symbol'])
        len(json.loads(docs[3][2])).should.be.equal(4)
        [ tokencontainer[1] for sentcontainer in json.loads(docs[4][2]) for tokencontainer in sentcontainer[0] ].should.be.equal(['ART', 'NN', 'ADJD', 'PTKIFG', 'ADJD', 'ADJA', 'NN', 'symbol', 'PRELS', 'PPER', 'PTKMA', 'ADV', 'VAFIN', 'symbol', 'number', 'EMOIMG', 'number', 'PPER', 'VVFIN', 'symbol', 'PPER', 'VAFIN', 'ADV', 'ART', 'ADJA', 'NN', 'symbol'])
        len(json.loads(docs[4][2])).should.be.equal(1)
        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_en))
        docs = list(corp.docs(output='list'))
        docs_dict = list(corp.docs(output='dict'))
        len(docs).should.be.equal(7)
        [ tokencontainer[1] for sentcontainer in json.loads(docs[0][2]) for tokencontainer in sentcontainer[0] ].should.be.equal(['PRP', 'VBD', 'PRP', 'symbol', 'CC', 'PRP', 'VBD', 'RB', 'JJ', 'NNP', 'RB', 'JJ', 'NN', 'NN', 'NN', 'IN', 'PRP', 'symbol', 'EMOASC', 'mention', 'hashtag', 'hashtag', 'URL'])
        len(json.loads(docs[0][2])).should.be.equal(2)
        [ tokencontainer[1] for sentcontainer in json.loads(docs[1][2]) for tokencontainer in sentcontainer[0] ].should.be.equal(['NN', 'TO', 'VB', 'PRP', 'EMOASC'])
        len(json.loads(docs[1][2])).should.be.equal(1)
        [ tokencontainer[1] for sentcontainer in json.loads(docs[2][2]) for tokencontainer in sentcontainer[0] ].should.be.equal(['DT', 'JJ', 'JJ', 'NNS', 'IN', 'JJ', 'NN', 'symbol', 'WDT', 'PRP', 'MD', 'RB', 'VB', 'symbol', 'EMOASC', 'EMOIMG', 'EMOASC', 'hashtag', 'hashtag', 'URL'])
        len(json.loads(docs[2][2])).should.be.equal(1)
        [ tokencontainer[1] for sentcontainer in json.loads(docs[3][2]) for tokencontainer in sentcontainer[0] ].should.be.equal(['JJ', 'JJ', 'JJ', 'JJ', 'JJ', 'JJ', 'NN', 'symbol', 'WDT', 'PRP', 'MD', 'VB', 'IN', 'VB', 'DT', 'NN', 'NN', 'NNS', 'symbol'])
        len(json.loads(docs[3][2])).should.be.equal(1)
        [ tokencontainer[1] for sentcontainer in json.loads(docs[4][2]) for tokencontainer in sentcontainer[0] ].should.be.equal(['JJ', 'NN', 'symbol', 'CC', 'DT', 'JJ', 'JJ', 'JJ', 'NN', 'symbol', 'UH', 'symbol', 'WP', 'VBP', 'PRP', 'VB', 'IN', 'PRP', 'symbol', 'number', 'EMOIMG', 'number', 'symbol', 'NNP', 'NN', 'NN', 'FW', 'FW', 'FW', 'FW', 'FW'])
        len(json.loads(docs[4][2])).should.be.equal(4)
        [ tokencontainer[1] for sentcontainer in json.loads(docs[5][2]) for tokencontainer in sentcontainer[0] ].should.be.equal(['JJ', 'JJ', 'JJ', 'NN', 'symbol', 'NNP', 'VBD', 'JJ', 'NNS', 'CC', 'JJ', 'NN', 'VBD', 'EMOIMG', 'EMOIMG', 'EMOIMG', 'EMOIMG', 'EMOIMG'])
        len(json.loads(docs[5][2])).should.be.equal(2)
        [ tokencontainer[1] for sentcontainer in json.loads(docs[6][2]) for tokencontainer in sentcontainer[0] ].should.be.equal(['PRP', 'VBD', 'RB', 'JJ', 'NN', 'IN', 'PRP', 'EMOIMG', 'symbol', 'MD', 'PRP', 'RB', 'VBD', 'PRP', 'VBD', 'PRP', 'EMOASC', 'EMOASC', 'EMOIMG', 'EMOIMG', 'EMOIMG'])
        len(json.loads(docs[6][2])).should.be.equal(1)

    @attr(status='stable')
    def test_emoji_normalization_800(self):
        self.prj_folder()
        self._init_variables_for_preprocessing_test()
        mode = self.mode
        corp = self._get_test_corp(preprocession=True, tokenizer=True, sent_splitter=False, pos_tagger=False, sentiment_analyzer=False, lang_classification=False, lang='en', mode=mode, init=True, clean=False, emojis_normalization=True)
        corp._init_insertions_variables()
        answer1 = corp._init_preprocessors()
        corp._normalize_emojis(self.test_unicode_str_en_1_tokenized_not_cleaned_without_emoji_normalization[0][0]).should.be.equal(self.test_unicode_str_en_1_tokenized_not_cleaned_with_emoji_normalization[0][0])
        corp._normalize_emojis(self.test_unicode_str_en_2_tokenized_not_cleaned_without_emoji_normalization[0][0]).should.be.equal(self.test_unicode_str_en_2_tokenized_not_cleaned_with_emoji_normalization[0][0])
        corp._normalize_emojis(self.test_unicode_str_de_1_tokenized_not_cleaned_without_emoji_normalization[0][0]).should.be.equal(self.test_unicode_str_de_1_tokenized_not_cleaned_with_emoji_normalization[0][0])
        corp._normalize_emojis(self.test_unicode_str_de_2_tokenized_not_cleaned_without_emoji_normalization[0][0]).should.be.equal(self.test_unicode_str_de_2_tokenized_not_cleaned_with_emoji_normalization[0][0])
        inp = [
         ('😀', 'emoticon'), ('😀', 'emoticon'), ('😀', 'emoticon'), ('😀', 'emoticon'), ('😀', 'emoticon'), ('🌈', 'emoticon'), ('🌈', 'emoticon'), ('🌈', 'emoticon'), ('🌈', 'emoticon'), ('🌈', 'emoticon'), ('🌈', 'emoticon'), ('🌈', 'emoticon')]
        outp = [('😀😀😀😀😀', 'emoticon'), ('🌈🌈🌈🌈🌈🌈🌈', 'emoticon')]
        corp._normalize_emojis(inp).should.be.equal(outp)

    @attr(status='stable')
    def test_count_general_stats_850(self):
        self.prj_folder()
        self._init_variables_for_preprocessing_test()
        self.test_dbs()
        corp = Corpus(mode=self.mode, status_bar=True)
        corp.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_de))
        corp.count_basic_stats()