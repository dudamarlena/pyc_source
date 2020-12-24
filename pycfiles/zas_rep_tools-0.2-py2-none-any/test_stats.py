# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/egoruni/Desktop/BA/Code/zas-rep-tools/zas_rep_tools/tests/test_stats.py
# Compiled at: 2018-10-22 05:55:12
import unittest, os, logging, sure, copy
from nose.plugins.attrib import attr
from testfixtures import tempdir, TempDirectory
from distutils.dir_util import copy_tree
import json, csv
from collections import Counter, defaultdict
from zas_rep_tools.src.classes.stats import Stats
from zas_rep_tools.src.classes.corpus import Corpus
from zas_rep_tools.src.utils.debugger import p, wipd, wipdn, wipdl, wipdo
from zas_rep_tools.src.utils.basetester import BaseTester
import zas_rep_tools.src.utils.db_helper as db_helper, platform
if platform.uname()[0].lower() != 'windows':
    import colored_traceback
    colored_traceback.add_hook()
else:
    import colorama

class TestZASstatsStats(BaseTester, unittest.TestCase):
    _multiprocess_shared_ = True

    def setUp(self):
        super(type(self), self).setUp()
        self.test_dict_row_en_1 = {'star_constellation': 'lion', 'text': '[[[["I", "PRP"], ["loved", "VBD"], ["it", "PRP"], [".", "symbol"]], ["positive", 0.7]], [[["But", "CC"], ["it", "PRP"], ["was", "VBD"], ["also", "RB"], ["verrrryyyyy", "JJ"], ["vvveRRRRRRrry", "NNP"], ["very", "RB"], ["piiiiiiiiity", "JJ"], ["pity", "NN"], ["pity", "NN"], ["piiitttyyy", "NN"], ["for", "IN"], ["me", "PRP"], ["......", "symbol"], [":-(((((", "EMOASC"], ["@real_trump", "mention"], ["#sheetlife", "hashtag"], ["#readytogo", "hashtag"], ["http://www.absurd.com", "URL"]], ["negative", -0.1875]]]', 'age': 37, 'working_area': 'IT', 'rowid': 1, 'gender': 'w', 'id': 1111}
        self.test_dict_row_en_2 = {'star_constellation': 'lion', 'text': '[[[["Tiny", "JJ"], ["model", "NN"], [",", "symbol"], ["but", "CC"], ["a", "DT"], ["big", "JJ"], ["big", "JJ"], ["big", "JJ"], ["explaaaaanation", "NN"], [".", "symbol"]], ["neutral", 0.0]], [[["Riiiiiight", "UH"], ["?", "symbol"]], ["neutral", 0.0]], [[["What", "WP"], ["do", "VBP"], ["youuuuuu", "PRP"], ["think", "VB"], ["about", "IN"], ["it", "PRP"], ["????", "symbol"]], ["neutral", 0.0]]]', 'age': 35, 'working_area': 'Air Industry', 'rowid': 5, 'gender': 'w', 'id': 5555}
        self.test_dict_row_de_1 = {'star_constellation': 'fish', 'text': '[[[["Klitze", "NN"], ["kliiiitze", "VMFIN"], ["kleEEEEine", "NE"], ["kleinnne", "ADJA"], ["\\u00dcberaschung", "NN"], [".", "symbol"]], ["neutral", 0.0]], [[["Trotzdem", "PAV"], ["hat", "VAFIN"], ["sie", "PPER"], ["mich", "PPER"], ["gl\\u00fccklich", "ADJD"], ["gemacht", "VVPP"], ["!", "symbol"], [":-))))", "EMOASC"], ["-)))", "EMOASC"]], ["positive", 0.5]]]', 'age': 23, 'working_area': 'Care', 'rowid': 8, 'gender': 'm', 'id': 8888}
        self.test_dict_row_de_2 = {'star_constellation': 'aquarius', 'text': '[[[["einen", "ART"], ["wundersch\\u00f6nen", "ADJA"], ["Taaaaaagggggg", "NN"], ["w\\u00fcnsche", "VVFIN"], ["ich", "PPER"], ["euch", "PRF"], [".", "symbol"]], ["neutral", 0.0]], [[["Genieeeeeeeeeeesst", "NN"], ["geniiiiiiiiiiiiist", "VVFIN"], ["das", "ART"], ["Leben", "NN"], [".", "symbol"]], ["neutral", 0.0]], [[["Bleeeeeeeeibt", "NN"], ["bleeeeibt", "VVFIN"], ["Huuuuuuuuuuuungrig", "NN"], [".", "symbol"], ["\\ud83d\\ude00\\ud83d\\ude00\\ud83d\\ude00\\ud83d\\ude00\\ud83d\\ude00", "EMOIMG"], ["\\ud83c\\udf08\\ud83c\\udf08\\ud83c\\udf08\\ud83c\\udf08\\ud83c\\udf08\\ud83c\\udf08\\ud83c\\udf08", "EMOIMG"]], ["neutral", 0.0]]]', 'age': 22, 'working_area': 'Finance', 'rowid': 9, 'gender': 'w', 'id': 9999}
        self.docs_ids = {self.test_dict_row_en_1['id']: self.test_dict_row_en_1, 
           self.test_dict_row_en_2['id']: self.test_dict_row_en_2, 
           self.test_dict_row_de_1['id']: self.test_dict_row_de_1, 
           self.test_dict_row_de_2['id']: self.test_dict_row_de_2}
        self.gold_standard_data = {'lower': {'repl': [
                            'rep_lower', ''], 
                     'redu': []}}
        self.path_to_stats_test_data = 'data/tests_data/stats/'

    def tearDown(self):
        super(type(self), self).tearDown()

    @attr(status='stable')
    def test_initialization_of_the_stats_instance_000(self):
        stats = Stats(mode=self.mode)
        stats.should.be.a(Stats)

    @attr(status='stable')
    def test_new_plaintext_stats_initialization_500(self):
        self.prj_folder()
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['stats']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'stats'
        stats = Stats(mode=self.mode)
        stats.init(self.tempdir_project_folder, name, language, visibility, corpus_id=corpus_id, version=version, baseline_delimiter='++')
        assert stats.exist()

    @attr(status='stable')
    def test_new_encrypted_stats_initialization_501(self):
        self.prj_folder()
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['stats']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'stats'
        stats = Stats(mode=self.mode)
        stats.init(self.tempdir_project_folder, name, language, visibility, corpus_id=corpus_id, version=version, encryption_key=encryption_key, baseline_delimiter='++')
        assert stats.exist()

    @attr(status='stable')
    def test_open_plaintext_blogger_stats_502(self):
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
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['stats']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'stats'
        stats = Stats(mode=self.mode)
        stats.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_stats_en))
        stats.statsdb.get_all_attr('main')['name'].should.be.equal(name)
        stats.statsdb.get_all_attr('main')['visibility'].should.be.equal(visibility)
        stats.statsdb.get_all_attr('main')['typ'].should.be.equal(typ)
        stats.statsdb.get_all_attr('main')['id'].should.be.equal(stats_id)
        stats.statsdb.get_all_attr('main')['version'].should.be.equal(version)
        assert stats.exist()

    @attr(status='stable')
    def test_open_encrypted_twitter_stats_503(self):
        self.prj_folder()
        self.test_dbs()
        name = self.configer.init_info_data['twitter']['name']
        language = self.configer.init_info_data['twitter']['language']
        visibility = self.configer.init_info_data['twitter']['visibility']
        platform_name = self.configer.init_info_data['twitter']['platform_name']
        license = self.configer.init_info_data['twitter']['license']
        template_name = self.configer.init_info_data['twitter']['template_name']
        version = self.configer.init_info_data['twitter']['version']
        source = self.configer.init_info_data['twitter']['source']
        encryption_key = self.configer.init_info_data['twitter']['encryption_key']['stats']
        corpus_id = self.configer.init_info_data['twitter']['id']['corpus']
        stats_id = self.configer.init_info_data['twitter']['id']['stats']
        typ = 'stats'
        stats = Stats(mode=self.mode)
        stats.open(os.path.join(self.tempdir_testdbs, self.db_twitter_encrypted_stats_de), encryption_key=encryption_key)
        stats.statsdb.get_all_attr('main')['name'].should.be.equal(name)
        stats.statsdb.get_all_attr('main')['visibility'].should.be.equal(visibility)
        stats.statsdb.get_all_attr('main')['typ'].should.be.equal(typ)
        stats.statsdb.get_all_attr('main')['id'].should.be.equal(stats_id)
        stats.statsdb.get_all_attr('main')['version'].should.be.equal(version)
        assert stats.exist()

    @attr(status='stable')
    def test_attach_corpdb_504(self):
        self.prj_folder()
        self.test_dbs()
        stats = Stats(mode=self.mode)
        stats.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_stats_en))
        stats.attach_corpdb(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_en))
        assert stats.exist()
        assert stats.attached_corpdb_number() == 1
        encryption_key_corp = self.configer.init_info_data['twitter']['encryption_key']['corpus']
        encryption_key_stats = self.configer.init_info_data['twitter']['encryption_key']['stats']
        stats = Stats(mode=self.mode)
        stats.open(os.path.join(self.tempdir_testdbs, self.db_twitter_encrypted_stats_de), encryption_key=encryption_key_stats)
        stats.attach_corpdb(os.path.join(self.tempdir_testdbs, self.db_twitter_encrypted_corp_de), encryption_key=encryption_key_corp)
        assert stats.exist()

    @attr(status='stable')
    def test_extract_repl_lower_case_600(self):
        self.prj_folder()
        self.test_dbs()
        stats = Stats(mode=self.mode)
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['stats']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'stats'
        stats.init(self.tempdir_project_folder, name, language, visibility, corpus_id=corpus_id, version=version, encryption_key=encryption_key, baseline_delimiter='++')
        stats._init_compution_variables()
        stats._init_preprocessors()
        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_en))
        stats.corp = corp
        stats._corp_info = corp.info()
        extracted_repl_in_text_container, repl_free_text_container, rle_for_repl_in_text_container = stats.extract_replications(json.loads(self.test_dict_row_de_1['text']))
        extracted_repl_in_text_container.should.be.equal([['', [('i', 4, 2)], [('e', 5, 2)], [('n', 3, 4)], '', ''], ['', '', '', '', '', '', '', [(')', 4, 2)], [(')', 3, 1)]]])
        repl_free_text_container.should.be.equal([['klitze', 'klitze', 'kleine', 'kleine', 'überaschung', '.'], ['trotzdem', 'hat', 'sie', 'mich', 'glücklich', 'gemacht', '!', ':-)', '-)']])
        rle_for_repl_in_text_container.should.be.equal([['', 'kli^4tze', 'kle^5ine', 'klein^3e', '', ''], ['', '', '', '', '', '', '', ':-)^4', '-)^3']])
        extracted_repl_in_text_container, repl_free_text_container, rle_for_repl_in_text_container = stats.extract_replications(json.loads(self.test_dict_row_de_2['text']))
        extracted_repl_in_text_container.should.be.equal([['', '', [('a', 6, 1), ('g', 6, 2)], '', '', '', ''], [[('e', 11, 4)], [('i', 13, 3)], '', '', ''], [[('e', 8, 2)], [('e', 4, 2)], [('u', 12, 1)], '', [('😀', 5, 0)], [('🌈', 7, 0)]]])
        repl_free_text_container.should.be.equal([['einen', 'wunderschönen', 'tag', 'wünsche', 'ich', 'euch', '.'], ['geniest', 'genist', 'das', 'leben', '.'], ['bleibt', 'bleibt', 'hungrig', '.', '😀', '🌈']])
        rle_for_repl_in_text_container.should.be.equal([['', '', 'ta^6g^6', '', '', '', ''], ['genie^11s^2t', 'geni^13st', '', '', ''], ['ble^8ibt', 'ble^4ibt', 'hu^12ngrig', '', '😀^5', '🌈^7']])
        extracted_repl_in_text_container, repl_free_text_container, rle_for_repl_in_text_container = stats.extract_replications(json.loads(self.test_dict_row_en_1['text']))
        extracted_repl_in_text_container.should.be.equal([['', '', '', ''], ['', '', '', '', [('r', 4, 2), ('y', 5, 3)], [('v', 3, 0), ('r', 8, 2)], '', [('i', 9, 1)], '', '', [('i', 3, 1), ('t', 3, 2), ('y', 3, 3)], '', '', [('.', 6, 0)], [('(', 5, 2)], '', '', '', '']])
        repl_free_text_container.should.be.equal([['i', 'loved', 'it', '.'], ['but', 'it', 'was', 'also', 'very', 'very', 'very', 'pity', 'pity', 'pity', 'pity', 'for', 'me', '.', ':-(', '@real_trump', '#shetlife', '#readytogo', 'http://www.absurd.com']])
        rle_for_repl_in_text_container.should.be.equal([['', '', '', ''], ['', '', '', '', 'ver^4y^5', 'v^3er^8y', '', 'pi^9ty', '', '', 'pi^3t^3y^3', '', '', '.^6', ':-(^5', '', '', '', '']])
        extracted_repl_in_text_container, repl_free_text_container, rle_for_repl_in_text_container = stats.extract_replications(json.loads(self.test_dict_row_en_2['text']))
        extracted_repl_in_text_container.should.be.equal([['', '', '', '', '', '', '', '', [('a', 5, 4)], ''], [[('i', 6, 1)], ''], ['', '', [('u', 6, 2)], '', '', '', [('?', 4, 0)]]])
        repl_free_text_container.should.be.equal([['tiny', 'model', ',', 'but', 'a', 'big', 'big', 'big', 'explanation', '.'], ['right', '?'], ['what', 'do', 'you', 'think', 'about', 'it', '?']])
        rle_for_repl_in_text_container.should.be.equal([['', '', '', '', '', '', '', '', 'expla^5nation', ''], ['ri^6ght', ''], ['', '', 'you^6', '', '', '', '?^4']])

    @attr(status='stable')
    def test_extract_repl_case_sensitiv_601(self):
        self.prj_folder()
        self.test_dbs()
        stats = Stats(mode=self.mode)
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['stats']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'stats'
        stats.init(self.tempdir_project_folder, name, language, visibility, corpus_id=corpus_id, version=version, encryption_key=encryption_key, case_sensitiv=True, baseline_delimiter='++')
        stats._init_compution_variables()
        stats._init_preprocessors()
        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_en))
        stats.corp = corp
        stats._corp_info = corp.info()
        extracted_repl_in_text_container, repl_free_text_container, rle_for_repl_in_text_container = stats.extract_replications(json.loads(self.test_dict_row_de_1['text']))
        extracted_repl_in_text_container.should.be.equal([['', [('i', 4, 2)], [('E', 4, 3)], [('n', 3, 4)], '', ''], ['', '', '', '', '', '', '', [(')', 4, 2)], [(')', 3, 1)]]])
        repl_free_text_container.should.be.equal([['Klitze', 'klitze', 'kleEine', 'kleine', 'Überaschung', '.'], ['Trotzdem', 'hat', 'sie', 'mich', 'glücklich', 'gemacht', '!', ':-)', '-)']])
        rle_for_repl_in_text_container.should.be.equal([['', 'kli^4tze', 'kleE^4ine', 'klein^3e', '', ''], ['', '', '', '', '', '', '', ':-)^4', '-)^3']])
        extracted_repl_in_text_container, repl_free_text_container, rle_for_repl_in_text_container = stats.extract_replications(json.loads(self.test_dict_row_de_2['text']))
        extracted_repl_in_text_container.should.be.equal([['', '', [('a', 6, 1), ('g', 6, 2)], '', '', '', ''], [[('e', 11, 4)], [('i', 13, 3)], '', '', ''], [[('e', 8, 2)], [('e', 4, 2)], [('u', 12, 1)], '', [('😀', 5, 0)], [('🌈', 7, 0)]]])
        repl_free_text_container.should.be.equal([['einen', 'wunderschönen', 'Tag', 'wünsche', 'ich', 'euch', '.'], ['Geniest', 'genist', 'das', 'Leben', '.'], ['Bleibt', 'bleibt', 'Hungrig', '.', '😀', '🌈']])
        rle_for_repl_in_text_container.should.be.equal([['', '', 'Ta^6g^6', '', '', '', ''], ['Genie^11s^2t', 'geni^13st', '', '', ''], ['Ble^8ibt', 'ble^4ibt', 'Hu^12ngrig', '', '😀^5', '🌈^7']])
        extracted_repl_in_text_container, repl_free_text_container, rle_for_repl_in_text_container = stats.extract_replications(json.loads(self.test_dict_row_en_1['text']))
        extracted_repl_in_text_container.should.be.equal([['', '', '', ''], ['', '', '', '', [('r', 4, 2), ('y', 5, 3)], [('v', 3, 0), ('R', 6, 2)], '', [('i', 9, 1)], '', '', [('i', 3, 1), ('t', 3, 2), ('y', 3, 3)], '', '', [('.', 6, 0)], [('(', 5, 2)], '', '', '', '']])
        repl_free_text_container.should.be.equal([['I', 'loved', 'it', '.'], ['But', 'it', 'was', 'also', 'very', 'veRry', 'very', 'pity', 'pity', 'pity', 'pity', 'for', 'me', '.', ':-(', '@real_trump', '#shetlife', '#readytogo', 'http://www.absurd.com']])
        rle_for_repl_in_text_container.should.be.equal([['', '', '', ''], ['', '', '', '', 'ver^4y^5', 'v^3eR^6r^2y', '', 'pi^9ty', '', '', 'pi^3t^3y^3', '', '', '.^6', ':-(^5', '', '', '', '']])
        extracted_repl_in_text_container, repl_free_text_container, rle_for_repl_in_text_container = stats.extract_replications(json.loads(self.test_dict_row_en_2['text']))
        extracted_repl_in_text_container.should.be.equal([['', '', '', '', '', '', '', '', [('a', 5, 4)], ''], [[('i', 6, 1)], ''], ['', '', [('u', 6, 2)], '', '', '', [('?', 4, 0)]]])
        repl_free_text_container.should.be.equal([['Tiny', 'model', ',', 'but', 'a', 'big', 'big', 'big', 'explanation', '.'], ['Right', '?'], ['What', 'do', 'you', 'think', 'about', 'it', '?']])
        rle_for_repl_in_text_container.should.be.equal([['', '', '', '', '', '', '', '', 'expla^5nation', ''], ['Ri^6ght', ''], ['', '', 'you^6', '', '', '', '?^4']])

    @attr(status='stable')
    def test_insert_repl_into_db_lower_case_602(self):
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
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['stats']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'stats'
        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_en))
        import Stemmer
        stemmer = Stemmer.Stemmer('de')
        stats = Stats(mode=self.mode)
        stats.init(self.tempdir_project_folder, name, language, visibility, corpus_id=corpus_id, version=version, encryption_key=encryption_key, baseline_delimiter='++')
        stats._init_compution_variables()
        stats._init_preprocessors()
        stats.corp = corp
        stats._corp_info = corp.info()
        text_list = [
         self.test_dict_row_de_1['id'], self.test_dict_row_de_1['text']]
        rle_for_repl_in_text_container = [['', 'kli^4tze', 'kle^5ine', 'klein^3e', '', ''], ['', '', '', '', '', '', '', ':-)^4', '-)^3']]
        extracted_repl_in_text_container = [['', [('i', 4, 2)], [('e', 5, 2)], [('n', 3, 4)], '', ''], ['', '', '', '', '', '', '', [(')', 4, 2)], [(')', 3, 1)]]]
        repl_free_text_container = [['klitze', 'klitze', 'kleine', 'kleine', 'überaschung', '.'], ['trotzdem', 'hat', 'sie', 'mich', 'glücklich', 'gemacht', '!', ':-)', '-)']]
        redu_free_text_container = [[('klitze', {'klitze': 1, 'kli^4tze': 1}), ('kleine', {'kle^5ine': 1, 'klein^3e': 1}), 'überaschung', '.'], ['trotzdem', 'hat', 'sie', 'mich', 'glücklich', 'gemacht', '!', ':-)', '-)']]
        stemmed_text_container = [ [ stemmer.stemWord(token) if isinstance(token, (str, unicode)) else stemmer.stemWord(token[0]) for token in sent ] for sent in redu_free_text_container ]
        mapping_redu = [
         [
          0, 2, 4, 5], [0, 1, 2, 3, 4, 5, 6, 7, 8]]
        stats.insert_repl_into_db(text_list, json.loads(self.test_dict_row_de_1['text']), extracted_repl_in_text_container, repl_free_text_container, rle_for_repl_in_text_container, redu_free_text_container, mapping_redu, stemmed_text_container)
        stats._write_repl_into_db(thread_name='Thread0')
        stats._write_redu_into_db(thread_name='Thread0')
        right_output = [
         (1, 8888, '[4, 9]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze', 'klitz', 'i', 4, 2, '[0, 0]',
 'NN', '["neutral", 0.0]', None, None, None, None, None, None, None, None, None,
 None, 'kleine', '["NE", {"kle^5ine": 1, "klein^3e": 1}, "klein"]', 'überaschung',
 '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]',
 'hat', '["VAFIN", null, "hat"]'),
         (2, 8888, '[4, 9]', '[0, 2]', '[0, 1]', 'kleine', 'kle^5ine', 'klein', 'e', 5, 2, '[0, 1]',
 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze',
 '["NN", {"klitze": 1, "kli^4tze": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]',
 '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]',
 'sie', '["PPER", null, "sie"]'),
         (3, 8888, '[4, 9]', '[0, 3]', '[0, 1]', 'kleine', 'klein^3e', 'klein', 'n', 3, 4, '[0, 1]',
 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze',
 '["NN", {"klitze": 1, "kli^4tze": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]',
 '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]',
 'sie', '["PPER", null, "sie"]'),
         (4, 8888, '[4, 9]', '[1, 7]', '[1, 7]', ':-)', ':-)^4', ':-)', ')', 4, 2, None, 'EMOASC',
 '["positive", 0.5]', 'sie', '["PPER", null, "sie"]', 'mich', '["PPER", null, "mich"]',
 'glücklich', '["ADJD", null, "glucklich"]', 'gemacht', '["VVPP", null, "gemacht"]',
 '!', '["symbol", null, "!"]', '-)', '["EMOASC", null, "-)"]', None, None, None,
 None, None, None, None, None),
         (5, 8888, '[4, 9]', '[1, 8]', '[1, 8]', '-)', '-)^3', '-)', ')', 3, 1, None, 'EMOASC',
 '["positive", 0.5]', 'mich', '["PPER", null, "mich"]', 'glücklich', '["ADJD", null, "glucklich"]',
 'gemacht', '["VVPP", null, "gemacht"]', '!', '["symbol", null, "!"]', ':-)', '["EMOASC", null, ":-)"]',
 None, None, None, None, None, None, None, None, None, None)]
        list(stats.statsdb.getall('replications')).should.be.equal(right_output)
        stats = Stats(mode=self.mode)
        stats.init(self.tempdir_project_folder, name, language, visibility, corpus_id=corpus_id, version=version, encryption_key=encryption_key, baseline_delimiter='++')
        stats._init_compution_variables()
        stats._init_preprocessors()
        stats.corp = corp
        stats._corp_info = corp.info()
        text_list = [
         self.test_dict_row_de_2['id'], self.test_dict_row_de_2['text']]
        rle_for_repl_in_text_container = [['', '', 'ta^6g^6', '', '', '', ''], ['genie^11s^2t', 'geni^13st', '', '', ''], ['ble^8ibt', 'ble^4ibt', 'hu^12ngrig', '', '😀^5', '🌈^7']]
        extracted_repl_in_text_container = [['', '', [('a', 6, 1), ('g', 6, 2)], '', '', '', ''], [[('e', 11, 4)], [('i', 13, 3)], '', '', ''], [[('e', 8, 2)], [('e', 4, 2)], [('u', 12, 1)], '', [('😀', 5, 0)], [('🌈', 7, 0)]]]
        repl_free_text_container = [['einen', 'wunderschönen', 'tag', 'wünsche', 'ich', 'euch', '.'], ['geniest', 'genist', 'das', 'leben', '.'], ['bleibt', 'bleibt', 'hungrig', '.', '😀', '🌈']]
        redu_free_text_container = [['einen', 'wunderschönen', 'tag', 'wünsche', 'ich', 'euch', '.'], ['geniest', 'genist', 'das', 'leben', '.'], [('bleibt', {'ble^4ibt': 1, 'ble^8ibt': 1}), 'hungrig', '.', '😀', '🌈']]
        mapping_redu = [[0, 1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 4], [0, 2, 3, 4, 5]]
        stemmed_text_container = [ [ stemmer.stemWord(token) if isinstance(token, (str, unicode)) else stemmer.stemWord(token[0]) for token in sent ] for sent in redu_free_text_container ]
        stats.insert_repl_into_db(text_list, json.loads(self.test_dict_row_de_2['text']), extracted_repl_in_text_container, repl_free_text_container, rle_for_repl_in_text_container, redu_free_text_container, mapping_redu, stemmed_text_container)
        stats._write_repl_into_db(thread_name='Thread0')
        stats._write_redu_into_db(thread_name='Thread0')
        right_output = [
         (1, 9999, '[7, 5, 5]', '[0, 2]', '[0, 2]', 'tag', 'ta^6g^6', 'tag', 'a', 6, 1, None,
 'NN', '["neutral", 0.0]', None, None, None, None, None, None, 'einen', '["ART", null, "ein"]',
 'wunderschönen', '["ADJA", null, "wunderschon"]', 'wünsche', '["VVFIN", null, "wunsch"]',
 'ich', '["PPER", null, "ich"]', 'euch', '["PRF", null, "euch"]', '.', '["symbol", null, "."]',
 'geniest', '["NN", null, "geni"]'),
         (2, 9999, '[7, 5, 5]', '[0, 2]', '[0, 2]', 'tag', 'ta^6g^6', 'tag', 'g', 6, 2, None,
 'NN', '["neutral", 0.0]', None, None, None, None, None, None, 'einen', '["ART", null, "ein"]',
 'wunderschönen', '["ADJA", null, "wunderschon"]', 'wünsche', '["VVFIN", null, "wunsch"]',
 'ich', '["PPER", null, "ich"]', 'euch', '["PRF", null, "euch"]', '.', '["symbol", null, "."]',
 'geniest', '["NN", null, "geni"]'),
         (3, 9999, '[7, 5, 5]', '[1, 0]', '[1, 0]', 'geniest', 'genie^11s^2t', 'geni', 'e',
 11, 4, None, 'NN', '["neutral", 0.0]', 'tag', '["NN", null, "tag"]', 'wünsche',
 '["VVFIN", null, "wunsch"]', 'ich', '["PPER", null, "ich"]', 'euch', '["PRF", null, "euch"]',
 '.', '["symbol", null, "."]', 'genist', '["VVFIN", null, "genist"]', 'das', '["ART", null, "das"]',
 'leben', '["NN", null, "leb"]', '.', '["symbol", null, "."]', 'bleibt', '["NN", {"ble^4ibt": 1, "ble^8ibt": 1}, "bleibt"]'),
         (4, 9999, '[7, 5, 5]', '[1, 1]', '[1, 1]', 'genist', 'geni^13st', 'genist', 'i', 13,
 3, None, 'VVFIN', '["neutral", 0.0]', 'wünsche', '["VVFIN", null, "wunsch"]', 'ich',
 '["PPER", null, "ich"]', 'euch', '["PRF", null, "euch"]', '.', '["symbol", null, "."]',
 'geniest', '["NN", null, "geni"]', 'das', '["ART", null, "das"]', 'leben', '["NN", null, "leb"]',
 '.', '["symbol", null, "."]', 'bleibt', '["NN", {"ble^4ibt": 1, "ble^8ibt": 1}, "bleibt"]',
 'hungrig', '["NN", null, "hungrig"]'),
         (5, 9999, '[7, 5, 5]', '[2, 0]', '[2, 0]', 'bleibt', 'ble^8ibt', 'bleibt', 'e', 8,
 2, '[2, 0]', 'NN', '["neutral", 0.0]', 'geniest', '["NN", null, "geni"]', 'genist',
 '["VVFIN", null, "genist"]', 'das', '["ART", null, "das"]', 'leben', '["NN", null, "leb"]',
 '.', '["symbol", null, "."]', 'hungrig', '["NN", null, "hungrig"]', '.', '["symbol", null, "."]',
 '😀', '["EMOIMG", null, "\\ud83d\\ude00"]', '🌈', '["EMOIMG", null, "\\ud83c\\udf08"]',
 None, None),
         (6, 9999, '[7, 5, 5]', '[2, 1]', '[2, 0]', 'bleibt', 'ble^4ibt', 'bleibt', 'e', 4,
 2, '[2, 0]', 'NN', '["neutral", 0.0]', 'geniest', '["NN", null, "geni"]', 'genist',
 '["VVFIN", null, "genist"]', 'das', '["ART", null, "das"]', 'leben', '["NN", null, "leb"]',
 '.', '["symbol", null, "."]', 'hungrig', '["NN", null, "hungrig"]', '.', '["symbol", null, "."]',
 '😀', '["EMOIMG", null, "\\ud83d\\ude00"]', '🌈', '["EMOIMG", null, "\\ud83c\\udf08"]',
 None, None),
         (7, 9999, '[7, 5, 5]', '[2, 2]', '[2, 1]', 'hungrig', 'hu^12ngrig', 'hungrig', 'u',
 12, 1, None, 'NN', '["neutral", 0.0]', 'genist', '["VVFIN", null, "genist"]', 'das',
 '["ART", null, "das"]', 'leben', '["NN", null, "leb"]', '.', '["symbol", null, "."]',
 'bleibt', '["NN", {"ble^4ibt": 1, "ble^8ibt": 1}, "bleibt"]', '.', '["symbol", null, "."]',
 '😀', '["EMOIMG", null, "\\ud83d\\ude00"]', '🌈', '["EMOIMG", null, "\\ud83c\\udf08"]',
 None, None, None, None),
         (8, 9999, '[7, 5, 5]', '[2, 4]', '[2, 3]', '😀', '😀^5', '😀', '😀', 5, 0, None, 'EMOIMG',
 '["neutral", 0.0]', 'leben', '["NN", null, "leb"]', '.', '["symbol", null, "."]',
 'bleibt', '["NN", {"ble^4ibt": 1, "ble^8ibt": 1}, "bleibt"]', 'hungrig', '["NN", null, "hungrig"]',
 '.', '["symbol", null, "."]', '🌈', '["EMOIMG", null, "\\ud83c\\udf08"]', None, None,
 None, None, None, None, None, None),
         (9, 9999, '[7, 5, 5]', '[2, 5]', '[2, 4]', '🌈', '🌈^7', '🌈', '🌈', 7, 0, None, 'EMOIMG',
 '["neutral", 0.0]', '.', '["symbol", null, "."]', 'bleibt', '["NN", {"ble^4ibt": 1, "ble^8ibt": 1}, "bleibt"]',
 'hungrig', '["NN", null, "hungrig"]', '.', '["symbol", null, "."]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]',
 None, None, None, None, None, None, None, None, None, None)]
        list(stats.statsdb.getall('replications')).should.be.equal(right_output)
        stemmer = Stemmer.Stemmer('en')
        stats = Stats(mode=self.mode)
        stats.init(self.tempdir_project_folder, name, language, visibility, corpus_id=corpus_id, version=version, encryption_key=encryption_key, baseline_delimiter='++')
        stats._init_compution_variables()
        stats._init_preprocessors()
        stats.corp = corp
        stats._corp_info = corp.info()
        text_list = [
         self.test_dict_row_en_1['id'], self.test_dict_row_en_1['text']]
        rle_for_repl_in_text_container = [['', '', '', ''], ['', '', '', '', 'ver^4y^5', 'v^3er^8y', '', 'pi^9ty', '', '', 'pi^3t^3y^3', '', '', '.^6', ':-(^5', '', '', '', '']]
        extracted_repl_in_text_container = [['', '', '', ''], ['', '', '', '', [('r', 4, 2), ('y', 5, 3)], [('v', 3, 0), ('r', 8, 2)], '', [('i', 9, 1)], '', '', [('i', 3, 1), ('t', 3, 2), ('y', 3, 3)], '', '', [('.', 6, 0)], [('(', 5, 2)], '', '', '', '']]
        repl_free_text_container = [['i', 'loved', 'it', '.'], ['but', 'it', 'was', 'also', 'very', 'very', 'very', 'pity', 'pity', 'pity', 'pity', 'for', 'me', '.', ':-(', '@real_trump', '#shetlife', '#readytogo', 'http://www.absurd.com']]
        redu_free_text_container = [['i', 'loved', 'it', '.'], ['but', 'it', 'was', 'also', ('very', {'very': 1, 'ver^4y^5': 1, 'v^3er^8y': 1}), ('pity', {'pity': 2, 'pi^3t^3y^3': 1, 'pi^9ty': 1}), 'for', 'me', '.', ':-(', '@real_trump', '#shetlife', '#readytogo', 'http://www.absurd.com']]
        mapping_redu = [[0, 1, 2, 3], [0, 1, 2, 3, 4, 7, 11, 12, 13, 14, 15, 16, 17, 18]]
        stemmed_text_container = [ [ stemmer.stemWord(token) if isinstance(token, (str, unicode)) else stemmer.stemWord(token[0]) for token in sent ] for sent in redu_free_text_container ]
        stats.insert_repl_into_db(text_list, json.loads(self.test_dict_row_en_1['text']), extracted_repl_in_text_container, repl_free_text_container, rle_for_repl_in_text_container, redu_free_text_container, mapping_redu, stemmed_text_container)
        stats._write_repl_into_db(thread_name='Thread0')
        stats._write_redu_into_db(thread_name='Thread0')
        right_output = [
         (1, 1111, '[4, 14]', '[1, 4]', '[1, 4]', 'very', 'ver^4y^5', 'veri', 'r', 4, 2, '[1, 4]',
 'JJ', '["negative", -0.1875]', '.', '["symbol", null, "."]', 'but', '["CC", null, "but"]',
 'it', '["PRP", null, "it"]', 'was', '["VBD", null, "was"]', 'also', '["RB", null, "also"]',
 'pity', '["JJ", {"pity": 2, "pi^3t^3y^3": 1, "pi^9ty": 1}, "piti"]', 'for', '["IN", null, "for"]',
 'me', '["PRP", null, "me"]', '.', '["symbol", null, "."]', ':-(', '["EMOASC", null, ":-("]'),
         (2, 1111, '[4, 14]', '[1, 4]', '[1, 4]', 'very', 'ver^4y^5', 'veri', 'y', 5, 3, '[1, 4]',
 'JJ', '["negative", -0.1875]', '.', '["symbol", null, "."]', 'but', '["CC", null, "but"]',
 'it', '["PRP", null, "it"]', 'was', '["VBD", null, "was"]', 'also', '["RB", null, "also"]',
 'pity', '["JJ", {"pity": 2, "pi^3t^3y^3": 1, "pi^9ty": 1}, "piti"]', 'for', '["IN", null, "for"]',
 'me', '["PRP", null, "me"]', '.', '["symbol", null, "."]', ':-(', '["EMOASC", null, ":-("]'),
         (3, 1111, '[4, 14]', '[1, 5]', '[1, 4]', 'very', 'v^3er^8y', 'veri', 'v', 3, 0, '[1, 4]',
 'JJ', '["negative", -0.1875]', '.', '["symbol", null, "."]', 'but', '["CC", null, "but"]',
 'it', '["PRP", null, "it"]', 'was', '["VBD", null, "was"]', 'also', '["RB", null, "also"]',
 'pity', '["JJ", {"pity": 2, "pi^3t^3y^3": 1, "pi^9ty": 1}, "piti"]', 'for', '["IN", null, "for"]',
 'me', '["PRP", null, "me"]', '.', '["symbol", null, "."]', ':-(', '["EMOASC", null, ":-("]'),
         (4, 1111, '[4, 14]', '[1, 5]', '[1, 4]', 'very', 'v^3er^8y', 'veri', 'r', 8, 2, '[1, 4]',
 'JJ', '["negative", -0.1875]', '.', '["symbol", null, "."]', 'but', '["CC", null, "but"]',
 'it', '["PRP", null, "it"]', 'was', '["VBD", null, "was"]', 'also', '["RB", null, "also"]',
 'pity', '["JJ", {"pity": 2, "pi^3t^3y^3": 1, "pi^9ty": 1}, "piti"]', 'for', '["IN", null, "for"]',
 'me', '["PRP", null, "me"]', '.', '["symbol", null, "."]', ':-(', '["EMOASC", null, ":-("]'),
         (5, 1111, '[4, 14]', '[1, 7]', '[1, 5]', 'pity', 'pi^9ty', 'piti', 'i', 9, 1, '[1, 5]',
 'JJ', '["negative", -0.1875]', 'but', '["CC", null, "but"]', 'it', '["PRP", null, "it"]',
 'was', '["VBD", null, "was"]', 'also', '["RB", null, "also"]', 'very', '["JJ", {"very": 1, "ver^4y^5": 1, "v^3er^8y": 1}, "veri"]',
 'for', '["IN", null, "for"]', 'me', '["PRP", null, "me"]', '.', '["symbol", null, "."]',
 ':-(', '["EMOASC", null, ":-("]', '@real_trump', '["mention", null, "@real_trump"]'),
         (6, 1111, '[4, 14]', '[1, 10]', '[1, 5]', 'pity', 'pi^3t^3y^3', 'piti', 'i', 3, 1,
 '[1, 5]', 'JJ', '["negative", -0.1875]', 'but', '["CC", null, "but"]', 'it', '["PRP", null, "it"]',
 'was', '["VBD", null, "was"]', 'also', '["RB", null, "also"]', 'very', '["JJ", {"very": 1, "ver^4y^5": 1, "v^3er^8y": 1}, "veri"]',
 'for', '["IN", null, "for"]', 'me', '["PRP", null, "me"]', '.', '["symbol", null, "."]',
 ':-(', '["EMOASC", null, ":-("]', '@real_trump', '["mention", null, "@real_trump"]'),
         (7, 1111, '[4, 14]', '[1, 10]', '[1, 5]', 'pity', 'pi^3t^3y^3', 'piti', 't', 3, 2,
 '[1, 5]', 'JJ', '["negative", -0.1875]', 'but', '["CC", null, "but"]', 'it', '["PRP", null, "it"]',
 'was', '["VBD", null, "was"]', 'also', '["RB", null, "also"]', 'very', '["JJ", {"very": 1, "ver^4y^5": 1, "v^3er^8y": 1}, "veri"]',
 'for', '["IN", null, "for"]', 'me', '["PRP", null, "me"]', '.', '["symbol", null, "."]',
 ':-(', '["EMOASC", null, ":-("]', '@real_trump', '["mention", null, "@real_trump"]'),
         (8, 1111, '[4, 14]', '[1, 10]', '[1, 5]', 'pity', 'pi^3t^3y^3', 'piti', 'y', 3, 3,
 '[1, 5]', 'JJ', '["negative", -0.1875]', 'but', '["CC", null, "but"]', 'it', '["PRP", null, "it"]',
 'was', '["VBD", null, "was"]', 'also', '["RB", null, "also"]', 'very', '["JJ", {"very": 1, "ver^4y^5": 1, "v^3er^8y": 1}, "veri"]',
 'for', '["IN", null, "for"]', 'me', '["PRP", null, "me"]', '.', '["symbol", null, "."]',
 ':-(', '["EMOASC", null, ":-("]', '@real_trump', '["mention", null, "@real_trump"]'),
         (9, 1111, '[4, 14]', '[1, 13]', '[1, 8]', '.', '.^6', '.', '.', 6, 0, None, 'symbol',
 '["negative", -0.1875]', 'also', '["RB", null, "also"]', 'very', '["JJ", {"very": 1, "ver^4y^5": 1, "v^3er^8y": 1}, "veri"]',
 'pity', '["JJ", {"pity": 2, "pi^3t^3y^3": 1, "pi^9ty": 1}, "piti"]', 'for', '["IN", null, "for"]',
 'me', '["PRP", null, "me"]', ':-(', '["EMOASC", null, ":-("]', '@real_trump', '["mention", null, "@real_trump"]',
 '#shetlife', '["hashtag", null, "#shetlif"]', '#readytogo', '["hashtag", null, "#readytogo"]',
 'http://www.absurd.com', '["URL", null, "http://www.absurd.com"]'),
         (10, 1111, '[4, 14]', '[1, 14]', '[1, 9]', ':-(', ':-(^5', ':-(', '(', 5, 2, None,
 'EMOASC', '["negative", -0.1875]', 'very', '["JJ", {"very": 1, "ver^4y^5": 1, "v^3er^8y": 1}, "veri"]',
 'pity', '["JJ", {"pity": 2, "pi^3t^3y^3": 1, "pi^9ty": 1}, "piti"]', 'for', '["IN", null, "for"]',
 'me', '["PRP", null, "me"]', '.', '["symbol", null, "."]', '@real_trump', '["mention", null, "@real_trump"]',
 '#shetlife', '["hashtag", null, "#shetlif"]', '#readytogo', '["hashtag", null, "#readytogo"]',
 'http://www.absurd.com', '["URL", null, "http://www.absurd.com"]', None, None)]
        list(stats.statsdb.getall('replications')).should.be.equal(right_output)
        stats = Stats(mode=self.mode)
        stats.init(self.tempdir_project_folder, name, language, visibility, corpus_id=corpus_id, version=version, encryption_key=encryption_key, baseline_delimiter='++')
        stats._init_compution_variables()
        stats._init_preprocessors()
        stats.corp = corp
        stats._corp_info = corp.info()
        text_list = [
         self.test_dict_row_en_2['id'], self.test_dict_row_en_2['text']]
        rle_for_repl_in_text_container = [['', '', '', '', '', '', '', '', 'expla^5nation', ''], ['ri^6ght', ''], ['', '', 'you^6', '', '', '', '?^4']]
        extracted_repl_in_text_container = [['', '', '', '', '', '', '', '', [('a', 5, 4)], ''], [[('i', 6, 1)], ''], ['', '', [('u', 6, 2)], '', '', '', [('?', 4, 0)]]]
        repl_free_text_container = [['tiny', 'model', ',', 'but', 'a', 'big', 'big', 'big', 'explanation', '.'], ['right', '?'], ['what', 'do', 'you', 'think', 'about', 'it', '?']]
        redu_free_text_container = [['tiny', 'model', ',', 'but', 'a', ('big', {'big': 3}), 'explanation', '.'], ['right', '?'], ['what', 'do', 'you', 'think', 'about', 'it', '?']]
        mapping_redu = [[0, 1, 2, 3, 4, 5, 8, 9], [0, 1], [0, 1, 2, 3, 4, 5, 6]]
        stemmed_text_container = [ [ stemmer.stemWord(token) if isinstance(token, (str, unicode)) else stemmer.stemWord(token[0]) for token in sent ] for sent in redu_free_text_container ]
        stats.insert_repl_into_db(text_list, json.loads(self.test_dict_row_en_2['text']), extracted_repl_in_text_container, repl_free_text_container, rle_for_repl_in_text_container, redu_free_text_container, mapping_redu, stemmed_text_container)
        stats._write_repl_into_db(thread_name='Thread0')
        stats._write_redu_into_db(thread_name='Thread0')
        right_output = [
         (1, 5555, '[8, 2, 7]', '[0, 8]', '[0, 6]', 'explanation', 'expla^5nation', 'explan',
 'a', 5, 4, None, 'NN', '["neutral", 0.0]', 'model', '["NN", null, "model"]', ',',
 '["symbol", null, ","]', 'but', '["CC", null, "but"]', 'a', '["DT", null, "a"]',
 'big', '["JJ", {"big": 3}, "big"]', '.', '["symbol", null, "."]', 'right', '["UH", null, "right"]',
 '?', '["symbol", null, "?"]', 'what', '["WP", null, "what"]', 'do', '["VBP", null, "do"]'),
         (2, 5555, '[8, 2, 7]', '[1, 0]', '[1, 0]', 'right', 'ri^6ght', 'right', 'i', 6, 1,
 None, 'UH', '["neutral", 0.0]', 'but', '["CC", null, "but"]', 'a', '["DT", null, "a"]',
 'big', '["JJ", {"big": 3}, "big"]', 'explanation', '["NN", null, "explan"]', '.',
 '["symbol", null, "."]', '?', '["symbol", null, "?"]', 'what', '["WP", null, "what"]',
 'do', '["VBP", null, "do"]', 'you', '["PRP", null, "you"]', 'think', '["VB", null, "think"]'),
         (3, 5555, '[8, 2, 7]', '[2, 2]', '[2, 2]', 'you', 'you^6', 'you', 'u', 6, 2, None,
 'PRP', '["neutral", 0.0]', '.', '["symbol", null, "."]', 'right', '["UH", null, "right"]',
 '?', '["symbol", null, "?"]', 'what', '["WP", null, "what"]', 'do', '["VBP", null, "do"]',
 'think', '["VB", null, "think"]', 'about', '["IN", null, "about"]', 'it', '["PRP", null, "it"]',
 '?', '["symbol", null, "?"]', None, None),
         (4, 5555, '[8, 2, 7]', '[2, 6]', '[2, 6]', '?', '?^4', '?', '?', 4, 0, None, 'symbol',
 '["neutral", 0.0]', 'do', '["VBP", null, "do"]', 'you', '["PRP", null, "you"]',
 'think', '["VB", null, "think"]', 'about', '["IN", null, "about"]', 'it', '["PRP", null, "it"]',
 None, None, None, None, None, None, None, None, None, None)]
        list(stats.statsdb.getall('replications')).should.be.equal(right_output)
        stats = Stats(mode=self.mode)
        stats.init(self.tempdir_project_folder, name, language, visibility, corpus_id=corpus_id, version=version, encryption_key=encryption_key, baseline_delimiter='++')
        stats._init_compution_variables()
        stats._init_preprocessors()
        stats.corp = corp
        stats._corp_info = corp.info()
        text_list = [
         self.test_dict_row_en_1['id'], self.test_dict_row_en_1['text']]
        rle_for_repl_in_text_container = [['', '', '', ''], ['', '', '', '', 'ver^4y^5', 'v^3er^8y', '', 'pi^9ty', '', '', 'pi^3t^3y^3', '', '', '.^6', ':-(^5', '', '', '', '']]
        extracted_repl_in_text_container = [['', '', '', ''], ['', '', '', '', [('r', 4, 2), ('y', 5, 3)], [('v', 3, 0), ('r', 8, 2)], '', [('i', 9, 1)], '', '', [('i', 3, 1), ('t', 3, 2), ('y', 3, 3)], '', '', [('.', 6, 0)], [('(', 5, 2)], '', '', '', '']]
        repl_free_text_container = [['i', 'loved', 'it', '.'], ['but', 'it', 'was', 'also', 'very', 'very', 'very', 'pity', 'pity', 'pity', 'pity', 'for', 'me', '.', ':-(', '@real_trump', '#shetlife', '#readytogo', 'http://www.absurd.com']]
        redu_free_text_container = [['i', 'loved', 'it', '.'], ['but', 'it', 'was', 'also', ('very', {'very': 1, 'ver^4y^5': 1, 'v^3er^8y': 1}), ('pity', {'pity': 2, 'pi^3t^3y^3': 1, 'pi^9ty': 1}), 'for', 'me', '.', ':-(', '@real_trump', '#shetlife', '#readytogo', 'http://www.absurd.com']]
        mapping_redu = [[0, 1, 2, 3], [0, 1, 2, 3, 4, 7, 11, 12, 13, 14, 15, 16, 17, 18]]
        stemmed_text_container = [ [ stemmer.stemWord(token) if isinstance(token, (str, unicode)) else stemmer.stemWord(token[0]) for token in sent ] for sent in redu_free_text_container ]
        stats.insert_repl_into_db(text_list, json.loads(self.test_dict_row_en_1['text']), extracted_repl_in_text_container, repl_free_text_container, rle_for_repl_in_text_container, redu_free_text_container, mapping_redu, stemmed_text_container)
        stats._write_repl_into_db(thread_name='Thread0')
        stats._write_redu_into_db(thread_name='Thread0')
        text_list = [
         self.test_dict_row_en_2['id'], self.test_dict_row_en_2['text']]
        rle_for_repl_in_text_container = [['', '', '', '', '', '', '', '', 'expla^5nation', ''], ['ri^6ght', ''], ['', '', 'you^6', '', '', '', '?^4']]
        extracted_repl_in_text_container = [['', '', '', '', '', '', '', '', [('a', 5, 4)], ''], [[('i', 6, 1)], ''], ['', '', [('u', 6, 2)], '', '', '', [('?', 4, 0)]]]
        repl_free_text_container = [['tiny', 'model', ',', 'but', 'a', 'big', 'big', 'big', 'explanation', '.'], ['right', '?'], ['what', 'do', 'you', 'think', 'about', 'it', '?']]
        redu_free_text_container = [['tiny', 'model', ',', 'but', 'a', ('big', {'big': 3}), 'explanation', '.'], ['right', '?'], ['what', 'do', 'you', 'think', 'about', 'it', '?']]
        mapping_redu = [[0, 1, 2, 3, 4, 5, 8, 9], [0, 1], [0, 1, 2, 3, 4, 5, 6]]
        stemmed_text_container = [ [ stemmer.stemWord(token) if isinstance(token, (str, unicode)) else stemmer.stemWord(token[0]) for token in sent ] for sent in redu_free_text_container ]
        stats.insert_repl_into_db(text_list, json.loads(self.test_dict_row_en_2['text']), extracted_repl_in_text_container, repl_free_text_container, rle_for_repl_in_text_container, redu_free_text_container, mapping_redu, stemmed_text_container)
        stats._write_repl_into_db(thread_name='Thread0')
        stats._write_redu_into_db(thread_name='Thread0')
        right_output = [
         (1, 1111, '[4, 14]', '[1, 4]', '[1, 4]', 'very', 'ver^4y^5', 'veri', 'r', 4, 2, '[1, 4]',
 'JJ', '["negative", -0.1875]', '.', '["symbol", null, "."]', 'but', '["CC", null, "but"]',
 'it', '["PRP", null, "it"]', 'was', '["VBD", null, "was"]', 'also', '["RB", null, "also"]',
 'pity', '["JJ", {"pity": 2, "pi^3t^3y^3": 1, "pi^9ty": 1}, "piti"]', 'for', '["IN", null, "for"]',
 'me', '["PRP", null, "me"]', '.', '["symbol", null, "."]', ':-(', '["EMOASC", null, ":-("]'),
         (2, 1111, '[4, 14]', '[1, 4]', '[1, 4]', 'very', 'ver^4y^5', 'veri', 'y', 5, 3, '[1, 4]',
 'JJ', '["negative", -0.1875]', '.', '["symbol", null, "."]', 'but', '["CC", null, "but"]',
 'it', '["PRP", null, "it"]', 'was', '["VBD", null, "was"]', 'also', '["RB", null, "also"]',
 'pity', '["JJ", {"pity": 2, "pi^3t^3y^3": 1, "pi^9ty": 1}, "piti"]', 'for', '["IN", null, "for"]',
 'me', '["PRP", null, "me"]', '.', '["symbol", null, "."]', ':-(', '["EMOASC", null, ":-("]'),
         (3, 1111, '[4, 14]', '[1, 5]', '[1, 4]', 'very', 'v^3er^8y', 'veri', 'v', 3, 0, '[1, 4]',
 'JJ', '["negative", -0.1875]', '.', '["symbol", null, "."]', 'but', '["CC", null, "but"]',
 'it', '["PRP", null, "it"]', 'was', '["VBD", null, "was"]', 'also', '["RB", null, "also"]',
 'pity', '["JJ", {"pity": 2, "pi^3t^3y^3": 1, "pi^9ty": 1}, "piti"]', 'for', '["IN", null, "for"]',
 'me', '["PRP", null, "me"]', '.', '["symbol", null, "."]', ':-(', '["EMOASC", null, ":-("]'),
         (4, 1111, '[4, 14]', '[1, 5]', '[1, 4]', 'very', 'v^3er^8y', 'veri', 'r', 8, 2, '[1, 4]',
 'JJ', '["negative", -0.1875]', '.', '["symbol", null, "."]', 'but', '["CC", null, "but"]',
 'it', '["PRP", null, "it"]', 'was', '["VBD", null, "was"]', 'also', '["RB", null, "also"]',
 'pity', '["JJ", {"pity": 2, "pi^3t^3y^3": 1, "pi^9ty": 1}, "piti"]', 'for', '["IN", null, "for"]',
 'me', '["PRP", null, "me"]', '.', '["symbol", null, "."]', ':-(', '["EMOASC", null, ":-("]'),
         (5, 1111, '[4, 14]', '[1, 7]', '[1, 5]', 'pity', 'pi^9ty', 'piti', 'i', 9, 1, '[1, 5]',
 'JJ', '["negative", -0.1875]', 'but', '["CC", null, "but"]', 'it', '["PRP", null, "it"]',
 'was', '["VBD", null, "was"]', 'also', '["RB", null, "also"]', 'very', '["JJ", {"very": 1, "ver^4y^5": 1, "v^3er^8y": 1}, "veri"]',
 'for', '["IN", null, "for"]', 'me', '["PRP", null, "me"]', '.', '["symbol", null, "."]',
 ':-(', '["EMOASC", null, ":-("]', '@real_trump', '["mention", null, "@real_trump"]'),
         (6, 1111, '[4, 14]', '[1, 10]', '[1, 5]', 'pity', 'pi^3t^3y^3', 'piti', 'i', 3, 1,
 '[1, 5]', 'JJ', '["negative", -0.1875]', 'but', '["CC", null, "but"]', 'it', '["PRP", null, "it"]',
 'was', '["VBD", null, "was"]', 'also', '["RB", null, "also"]', 'very', '["JJ", {"very": 1, "ver^4y^5": 1, "v^3er^8y": 1}, "veri"]',
 'for', '["IN", null, "for"]', 'me', '["PRP", null, "me"]', '.', '["symbol", null, "."]',
 ':-(', '["EMOASC", null, ":-("]', '@real_trump', '["mention", null, "@real_trump"]'),
         (7, 1111, '[4, 14]', '[1, 10]', '[1, 5]', 'pity', 'pi^3t^3y^3', 'piti', 't', 3, 2,
 '[1, 5]', 'JJ', '["negative", -0.1875]', 'but', '["CC", null, "but"]', 'it', '["PRP", null, "it"]',
 'was', '["VBD", null, "was"]', 'also', '["RB", null, "also"]', 'very', '["JJ", {"very": 1, "ver^4y^5": 1, "v^3er^8y": 1}, "veri"]',
 'for', '["IN", null, "for"]', 'me', '["PRP", null, "me"]', '.', '["symbol", null, "."]',
 ':-(', '["EMOASC", null, ":-("]', '@real_trump', '["mention", null, "@real_trump"]'),
         (8, 1111, '[4, 14]', '[1, 10]', '[1, 5]', 'pity', 'pi^3t^3y^3', 'piti', 'y', 3, 3,
 '[1, 5]', 'JJ', '["negative", -0.1875]', 'but', '["CC", null, "but"]', 'it', '["PRP", null, "it"]',
 'was', '["VBD", null, "was"]', 'also', '["RB", null, "also"]', 'very', '["JJ", {"very": 1, "ver^4y^5": 1, "v^3er^8y": 1}, "veri"]',
 'for', '["IN", null, "for"]', 'me', '["PRP", null, "me"]', '.', '["symbol", null, "."]',
 ':-(', '["EMOASC", null, ":-("]', '@real_trump', '["mention", null, "@real_trump"]'),
         (9, 1111, '[4, 14]', '[1, 13]', '[1, 8]', '.', '.^6', '.', '.', 6, 0, None, 'symbol',
 '["negative", -0.1875]', 'also', '["RB", null, "also"]', 'very', '["JJ", {"very": 1, "ver^4y^5": 1, "v^3er^8y": 1}, "veri"]',
 'pity', '["JJ", {"pity": 2, "pi^3t^3y^3": 1, "pi^9ty": 1}, "piti"]', 'for', '["IN", null, "for"]',
 'me', '["PRP", null, "me"]', ':-(', '["EMOASC", null, ":-("]', '@real_trump', '["mention", null, "@real_trump"]',
 '#shetlife', '["hashtag", null, "#shetlif"]', '#readytogo', '["hashtag", null, "#readytogo"]',
 'http://www.absurd.com', '["URL", null, "http://www.absurd.com"]'),
         (10, 1111, '[4, 14]', '[1, 14]', '[1, 9]', ':-(', ':-(^5', ':-(', '(', 5, 2, None,
 'EMOASC', '["negative", -0.1875]', 'very', '["JJ", {"very": 1, "ver^4y^5": 1, "v^3er^8y": 1}, "veri"]',
 'pity', '["JJ", {"pity": 2, "pi^3t^3y^3": 1, "pi^9ty": 1}, "piti"]', 'for', '["IN", null, "for"]',
 'me', '["PRP", null, "me"]', '.', '["symbol", null, "."]', '@real_trump', '["mention", null, "@real_trump"]',
 '#shetlife', '["hashtag", null, "#shetlif"]', '#readytogo', '["hashtag", null, "#readytogo"]',
 'http://www.absurd.com', '["URL", null, "http://www.absurd.com"]', None, None),
         (11, 5555, '[8, 2, 7]', '[0, 8]', '[0, 6]', 'explanation', 'expla^5nation', 'explan',
 'a', 5, 4, None, 'NN', '["neutral", 0.0]', 'model', '["NN", null, "model"]', ',',
 '["symbol", null, ","]', 'but', '["CC", null, "but"]', 'a', '["DT", null, "a"]',
 'big', '["JJ", {"big": 3}, "big"]', '.', '["symbol", null, "."]', 'right', '["UH", null, "right"]',
 '?', '["symbol", null, "?"]', 'what', '["WP", null, "what"]', 'do', '["VBP", null, "do"]'),
         (12, 5555, '[8, 2, 7]', '[1, 0]', '[1, 0]', 'right', 'ri^6ght', 'right', 'i', 6, 1,
 None, 'UH', '["neutral", 0.0]', 'but', '["CC", null, "but"]', 'a', '["DT", null, "a"]',
 'big', '["JJ", {"big": 3}, "big"]', 'explanation', '["NN", null, "explan"]', '.',
 '["symbol", null, "."]', '?', '["symbol", null, "?"]', 'what', '["WP", null, "what"]',
 'do', '["VBP", null, "do"]', 'you', '["PRP", null, "you"]', 'think', '["VB", null, "think"]'),
         (13, 5555, '[8, 2, 7]', '[2, 2]', '[2, 2]', 'you', 'you^6', 'you', 'u', 6, 2, None,
 'PRP', '["neutral", 0.0]', '.', '["symbol", null, "."]', 'right', '["UH", null, "right"]',
 '?', '["symbol", null, "?"]', 'what', '["WP", null, "what"]', 'do', '["VBP", null, "do"]',
 'think', '["VB", null, "think"]', 'about', '["IN", null, "about"]', 'it', '["PRP", null, "it"]',
 '?', '["symbol", null, "?"]', None, None),
         (14, 5555, '[8, 2, 7]', '[2, 6]', '[2, 6]', '?', '?^4', '?', '?', 4, 0, None, 'symbol',
 '["neutral", 0.0]', 'do', '["VBP", null, "do"]', 'you', '["PRP", null, "you"]',
 'think', '["VB", null, "think"]', 'about', '["IN", null, "about"]', 'it', '["PRP", null, "it"]',
 None, None, None, None, None, None, None, None, None, None)]
        stats.statsdb.getall('replications').should.be.equal(right_output)
        return

    @attr(status='stable')
    def test_extract_redu_lower_case_603(self):
        self.prj_folder()
        self.test_dbs()
        stats = Stats(mode=self.mode)
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['stats']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'stats'
        stats.init(self.tempdir_project_folder, name, language, visibility, corpus_id=corpus_id, version=version, encryption_key=encryption_key, baseline_delimiter='++')
        stats._init_compution_variables()
        stats._init_preprocessors()
        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_en))
        stats.corp = corp
        stats._corp_info = corp.info()
        repl_free_de_row_lowercased_1 = [
         [
          'klitze', 'klitze', 'kleine', 'kleine', 'überaschung', '.'], ['trotzdem', 'hat', 'sie', 'mich', 'glücklich', 'gemacht', '!', ':-)', '-)']]
        rle_for_repl_in_text_container = [['', 'kli^4tze', 'kle^5ine', 'klein^3e', '', ''], ['', '', '', '', '', '', '', ':-)^4', '-)^3']]
        extracted_redu_in_text_container, redu_free_text_container, mapping_redu = stats.extract_reduplications(repl_free_de_row_lowercased_1, rle_for_repl_in_text_container)
        extracted_redu_in_text_container.should.be.equal([[{'start_index_in_orig': 0, 'length': 2, 'word': 'klitze', 'index_in_redu_free': 0}, {'start_index_in_orig': 2, 'length': 2, 'word': 'kleine', 'index_in_redu_free': 1}], []])
        redu_free_text_container.should.be.equal([[('klitze', {'klitze': 1, 'kli^4tze': 1}), ('kleine', {'kle^5ine': 1, 'klein^3e': 1}), 'überaschung', '.'], ['trotzdem', 'hat', 'sie', 'mich', 'glücklich', 'gemacht', '!', ':-)', '-)']])
        mapping_redu.should.be.equal([[0, 2, 4, 5], [0, 1, 2, 3, 4, 5, 6, 7, 8]])
        repl_free_de_row_lowercased_2 = [
         [
          'einen', 'wunderschönen', 'tag', 'wünsche', 'ich', 'euch', '.'], ['geniest', 'genist', 'das', 'leben', '.'], ['bleibt', 'bleibt', 'hungrig', '.', '😀', '🌈']]
        rle_for_repl_in_text_container = [['', '', 'ta^6g^6', '', '', '', ''], ['genie^11s^2t', 'geni^13st', '', '', ''], ['ble^8ibt', 'ble^4ibt', 'hu^12ngrig', '', '😀^5', '🌈^7']]
        extracted_redu_in_text_container, redu_free_text_container, mapping_redu = stats.extract_reduplications(repl_free_de_row_lowercased_2, rle_for_repl_in_text_container)
        extracted_redu_in_text_container.should.be.equal([[], [], [{'start_index_in_orig': 0, 'length': 2, 'word': 'bleibt', 'index_in_redu_free': 0}]])
        redu_free_text_container.should.be.equal([['einen', 'wunderschönen', 'tag', 'wünsche', 'ich', 'euch', '.'], ['geniest', 'genist', 'das', 'leben', '.'], [('bleibt', {'ble^4ibt': 1, 'ble^8ibt': 1}), 'hungrig', '.', '😀', '🌈']])
        mapping_redu.should.be.equal([[0, 1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 4], [0, 2, 3, 4, 5]])
        repl_free_en_row_lowercased_1 = [
         [
          'i', 'loved', 'it', '.'], ['but', 'it', 'was', 'also', 'very', 'very', 'very', 'pity', 'pity', 'pity', 'pity', 'for', 'me', '.', ':-(', '@real_trump', '#shetlife', '#readytogo', 'http://www.absurd.com']]
        rle_for_repl_in_text_container = [['', '', '', ''], ['', '', '', '', 'ver^4y^5', 'v^3er^8y', '', 'pi^9ty', '', '', 'pi^3t^3y^3', '', '', '.^6', ':-(^5', '', '', '', '']]
        extracted_redu_in_text_container, redu_free_text_container, mapping_redu = stats.extract_reduplications(repl_free_en_row_lowercased_1, rle_for_repl_in_text_container)
        extracted_redu_in_text_container.should.be.equal([[], [{'start_index_in_orig': 4, 'length': 3, 'word': 'very', 'index_in_redu_free': 4}, {'start_index_in_orig': 7, 'length': 4, 'word': 'pity', 'index_in_redu_free': 5}]])
        redu_free_text_container.should.be.equal([['i', 'loved', 'it', '.'], ['but', 'it', 'was', 'also', ('very', {'very': 1, 'ver^4y^5': 1, 'v^3er^8y': 1}), ('pity', {'pity': 2, 'pi^3t^3y^3': 1, 'pi^9ty': 1}), 'for', 'me', '.', ':-(', '@real_trump', '#shetlife', '#readytogo', 'http://www.absurd.com']])
        mapping_redu.should.be.equal([[0, 1, 2, 3], [0, 1, 2, 3, 4, 7, 11, 12, 13, 14, 15, 16, 17, 18]])
        repl_free_en_row_lowercased_2 = [
         [
          'tiny', 'model', ',', 'but', 'a', 'big', 'big', 'big', 'explanation', '.'], ['right', '?'], ['what', 'do', 'you', 'think', 'about', 'it', '?']]
        rle_for_repl_in_text_container = [['', '', '', '', '', '', '', '', 'expla^5nation', ''], ['ri^6ght', ''], ['', '', 'you^6', '', '', '', '?^4']]
        extracted_redu_in_text_container, redu_free_text_container, mapping_redu = stats.extract_reduplications(repl_free_en_row_lowercased_2, rle_for_repl_in_text_container)
        extracted_redu_in_text_container.should.be.equal([[{'start_index_in_orig': 5, 'length': 3, 'word': 'big', 'index_in_redu_free': 5}], [], []])
        redu_free_text_container.should.be.equal([['tiny', 'model', ',', 'but', 'a', ('big', {'big': 3}), 'explanation', '.'], ['right', '?'], ['what', 'do', 'you', 'think', 'about', 'it', '?']])
        mapping_redu.should.be.equal([[0, 1, 2, 3, 4, 5, 8, 9], [0, 1], [0, 1, 2, 3, 4, 5, 6]])

    @attr(status='stable')
    def test_extract_redu_case_sensitive_604(self):
        self.prj_folder()
        self.test_dbs()
        stats = Stats(mode=self.mode)
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['stats']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'stats'
        stats.init(self.tempdir_project_folder, name, language, visibility, corpus_id=corpus_id, version=version, encryption_key=encryption_key, case_sensitiv=True, baseline_delimiter='++')
        stats._init_compution_variables()
        stats._init_preprocessors()
        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_en))
        stats.corp = corp
        stats._corp_info = corp.info()
        repl_free_de_row_case_sensitive_1 = [
         [
          'Klitze', 'klitze', 'kleEine', 'kleine', 'Überaschung', '.'], ['Trotzdem', 'hat', 'sie', 'mich', 'glücklich', 'gemacht', '!', ':-)', '-)']]
        rle_for_repl_in_text_container = [['', 'kli^4tze', 'kleE^4ine', 'klein^3e', '', ''], ['', '', '', '', '', '', '', ':-)^4', '-)^3']]
        extracted_redu_in_text_container, redu_free_text_container, mapping_redu = stats.extract_reduplications(repl_free_de_row_case_sensitive_1, rle_for_repl_in_text_container)
        extracted_redu_in_text_container.should.be.equal([[], []])
        redu_free_text_container.should.be.equal([['Klitze', 'klitze', 'kleEine', 'kleine', 'Überaschung', '.'], ['Trotzdem', 'hat', 'sie', 'mich', 'glücklich', 'gemacht', '!', ':-)', '-)']])
        mapping_redu.should.be.equal([[0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5, 6, 7, 8]])
        repl_free_de_row_case_sensitive_2 = [
         [
          'einen', 'wunderschönen', 'Tag', 'wünsche', 'ich', 'euch', '.'], ['Geniest', 'genist', 'das', 'Leben', '.'], ['Bleibt', 'bleibt', 'Hungrig', '.', '😀', '🌈']]
        rle_for_repl_in_text_container = [['', '', 'Ta^6g^6', '', '', '', ''], ['Genie^11s^2t', 'geni^13st', '', '', ''], ['Ble^8ibt', 'ble^4ibt', 'Hu^12ngrig', '', '😀^5', '🌈^7']]
        extracted_redu_in_text_container, redu_free_text_container, mapping_redu = stats.extract_reduplications(repl_free_de_row_case_sensitive_2, rle_for_repl_in_text_container)
        extracted_redu_in_text_container.should.be.equal([[], [], []])
        redu_free_text_container.should.be.equal([['einen', 'wunderschönen', 'Tag', 'wünsche', 'ich', 'euch', '.'], ['Geniest', 'genist', 'das', 'Leben', '.'], ['Bleibt', 'bleibt', 'Hungrig', '.', '😀', '🌈']])
        mapping_redu.should.be.equal([[0, 1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 4], [0, 1, 2, 3, 4, 5]])
        repl_free_en_row_case_sensitive_1 = [
         [
          'I', 'loved', 'it', '.'], ['But', 'it', 'was', 'also', 'very', 'veRry', 'very', 'pity', 'pity', 'pity', 'pity', 'for', 'me', '.', ':-(', '@real_trump', '#shetlife', '#readytogo', 'http://www.absurd.com']]
        rle_for_repl_in_text_container = [['', '', '', ''], ['', '', '', '', 'ver^4y^5', 'v^3eR^6r^2y', '', 'pi^9ty', '', '', 'pi^3t^3y^3', '', '', '.^6', ':-(^5', '', '', '', '']]
        extracted_redu_in_text_container, redu_free_text_container, mapping_redu = stats.extract_reduplications(repl_free_en_row_case_sensitive_1, rle_for_repl_in_text_container)
        extracted_redu_in_text_container.should.be.equal([[], [{'start_index_in_orig': 7, 'length': 4, 'word': 'pity', 'index_in_redu_free': 7}]])
        redu_free_text_container.should.be.equal([['I', 'loved', 'it', '.'], ['But', 'it', 'was', 'also', 'very', 'veRry', 'very', ('pity', {'pity': 2, 'pi^3t^3y^3': 1, 'pi^9ty': 1}), 'for', 'me', '.', ':-(', '@real_trump', '#shetlife', '#readytogo', 'http://www.absurd.com']])
        mapping_redu.should.be.equal([[0, 1, 2, 3], [0, 1, 2, 3, 4, 5, 6, 7, 11, 12, 13, 14, 15, 16, 17, 18]])
        repl_free_en_row_case_sensitive_2 = [
         [
          'Tiny', 'model', ',', 'but', 'a', 'big', 'big', 'big', 'explanation', '.'], ['Right', '?'], ['What', 'do', 'you', 'think', 'about', 'it', '?']]
        rle_for_repl_in_text_container = [['', '', '', '', '', '', '', '', 'expla^5nation', ''], ['Ri^6ght', ''], ['', '', 'you^6', '', '', '', '?^4']]
        extracted_redu_in_text_container, redu_free_text_container, mapping_redu = stats.extract_reduplications(repl_free_en_row_case_sensitive_2, rle_for_repl_in_text_container)
        extracted_redu_in_text_container.should.be.equal([[{'start_index_in_orig': 5, 'length': 3, 'word': 'big', 'index_in_redu_free': 5}], [], []])
        redu_free_text_container.should.be.equal([['Tiny', 'model', ',', 'but', 'a', ('big', {'big': 3}), 'explanation', '.'], ['Right', '?'], ['What', 'do', 'you', 'think', 'about', 'it', '?']])
        mapping_redu.should.be.equal([[0, 1, 2, 3, 4, 5, 8, 9], [0, 1], [0, 1, 2, 3, 4, 5, 6]])

    @attr(status='stable')
    def test_insert_redu_into_db_lower_case_605(self):
        self.prj_folder()
        self.test_dbs()
        stats = Stats(mode=self.mode)
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['stats']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'stats'
        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_en))
        import Stemmer
        stemmer = Stemmer.Stemmer('de')
        stats = Stats(mode=self.mode)
        stats.init(self.tempdir_project_folder, name, language, visibility, corpus_id=corpus_id, version=version, encryption_key=encryption_key, baseline_delimiter='++')
        stats._init_compution_variables()
        stats._init_preprocessors()
        stats.corp = corp
        stats._corp_info = corp.info()
        repl_free_de_row_lowercased_1 = [
         [
          'klitze', 'klitze', 'kleine', 'kleine', 'überaschung', '.'], ['trotzdem', 'hat', 'sie', 'mich', 'glücklich', 'gemacht', '!', ':-)', '-)']]
        text_list = [
         self.test_dict_row_de_1['id'], self.test_dict_row_de_1['text']]
        extracted_redu_in_text_container = [[{'start_index_in_orig': 0, 'length': 2, 'word': 'klitze', 'index_in_redu_free': 0}, {'start_index_in_orig': 2, 'length': 2, 'word': 'kleine', 'index_in_redu_free': 1}], []]
        redu_free_text_container = [[('klitze', {'klitze': 1, 'kli^4tze': 1}), ('kleine', {'kle^5ine': 1, 'klein^3e': 1}), 'überaschung', '.'], ['trotzdem', 'hat', 'sie', 'mich', 'glücklich', 'gemacht', '!', ':-)', '-)']]
        rle_for_repl_in_text_container = [['', 'kli^4tze', 'kle^5ine', 'klein^3e', '', ''], ['', '', '', '', '', '', '', ':-)^4', '-)^3']]
        repl_free_text_container = [['klitze', 'klitze', 'kleine', 'kleine', 'überaschung', '.'], ['trotzdem', 'hat', 'sie', 'mich', 'glücklich', 'gemacht', '!', ':-)', '-)']]
        mapping_redu = [[0, 2, 4, 5], [0, 1, 2, 3, 4, 5, 6, 7, 8]]
        stemmed_text_container = [ [ stemmer.stemWord(token) if isinstance(token, (str, unicode)) else stemmer.stemWord(token[0]) for token in sent ] for sent in redu_free_text_container ]
        stats.insert_redu_into_db(text_list, json.loads(self.test_dict_row_de_1['text']), extracted_redu_in_text_container, redu_free_text_container, rle_for_repl_in_text_container, repl_free_text_container, mapping_redu, stemmed_text_container)
        stats._write_repl_into_db(thread_name='Thread0')
        stats._write_redu_into_db(thread_name='Thread0')
        inserted_columns = list(stats.statsdb.getall('reduplications'))
        right_output = [(1, 8888, '[4, 9]', '[0, 0]', '[0, 0]', 'klitze', 'klitz', '{"klitze": 1, "kli^4tze": 1}',
 2, 'NN', '["neutral", 0.0]', None, None, None, None, None, None, None, None, None,
 None, 'kleine', '["NE", {"kle^5ine": 1, "klein^3e": 1}, "klein"]', 'überaschung',
 '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]',
 'hat', '["VAFIN", null, "hat"]'), (2, 8888, '[4, 9]', '[0, 2]', '[0, 1]', 'kleine', 'klein', '{"kle^5ine": 1, "klein^3e": 1}',
 2, 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze',
 '["NN", {"klitze": 1, "kli^4tze": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]',
 '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]',
 'sie', '["PPER", null, "sie"]')]
        inserted_columns.should.be.equal(right_output)
        stats = Stats(mode=self.mode)
        stats.init(self.tempdir_project_folder, name, language, visibility, corpus_id=corpus_id, version=version, encryption_key=encryption_key, baseline_delimiter='++')
        stats._init_compution_variables()
        stats._init_preprocessors()
        stats.corp = corp
        stats._corp_info = corp.info()
        repl_free_de_row_lowercased_2 = [
         [
          'einen', 'wunderschönen', 'tag', 'wünsche', 'ich', 'euch', '.'], ['geniest', 'genist', 'das', 'leben', '.'], ['bleibt', 'bleibt', 'hungrig', '.', '😀', '🌈']]
        text_list = [
         self.test_dict_row_de_1['id'], self.test_dict_row_de_1['text']]
        extracted_redu_in_text_container = [[], [], [{'start_index_in_orig': 0, 'length': 2, 'word': 'bleibt', 'index_in_redu_free': 0}]]
        redu_free_text_container = [['einen', 'wunderschönen', 'tag', 'wünsche', 'ich', 'euch', '.'], ['geniest', 'genist', 'das', 'leben', '.'], [('bleibt', {'ble^4ibt': 1, 'ble^8ibt': 1}), 'hungrig', '.', '😀', '🌈']]
        rle_for_repl_in_text_container = [['', '', 'ta^6g^6', '', '', '', ''], ['genie^11s^2t', 'geni^13st', '', '', ''], ['ble^8ibt', 'ble^4ibt', 'hu^12ngrig', '', '😀^5', '🌈^7']]
        repl_free_text_container = [['einen', 'wunderschönen', 'tag', 'wünsche', 'ich', 'euch', '.'], ['geniest', 'genist', 'das', 'leben', '.'], ['bleibt', 'bleibt', 'hungrig', '.', '😀', '🌈']]
        mapping_redu = [[0, 1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 4], [0, 2, 3, 4, 5]]
        stemmed_text_container = [ [ stemmer.stemWord(token) if isinstance(token, (str, unicode)) else stemmer.stemWord(token[0]) for token in sent ] for sent in redu_free_text_container ]
        stats.insert_redu_into_db(text_list, json.loads(self.test_dict_row_de_2['text']), extracted_redu_in_text_container, redu_free_text_container, rle_for_repl_in_text_container, repl_free_text_container, mapping_redu, stemmed_text_container)
        stats._write_repl_into_db(thread_name='Thread0')
        stats._write_redu_into_db(thread_name='Thread0')
        inserted_columns = list(stats.statsdb.getall('reduplications'))
        right_output = [(1, 8888, '[7, 5, 5]', '[2, 0]', '[2, 0]', 'bleibt', 'bleibt', '{"ble^4ibt": 1, "ble^8ibt": 1}',
 2, 'NN', '["neutral", 0.0]', 'geniest', '["NN", null, "geni"]', 'genist', '["VVFIN", null, "genist"]',
 'das', '["ART", null, "das"]', 'leben', '["NN", null, "leb"]', '.', '["symbol", null, "."]',
 'hungrig', '["NN", null, "hungrig"]', '.', '["symbol", null, "."]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]',
 '🌈', '["EMOIMG", null, "\\ud83c\\udf08"]', None, None)]
        inserted_columns.should.be.equal(right_output)
        stemmer = Stemmer.Stemmer('en')
        stats = Stats(mode=self.mode)
        stats.init(self.tempdir_project_folder, name, language, visibility, corpus_id=corpus_id, version=version, encryption_key=encryption_key, baseline_delimiter='++')
        stats._init_compution_variables()
        stats._init_preprocessors()
        stats.corp = corp
        stats._corp_info = corp.info()
        repl_free_en_row_lowercased_1 = [
         [
          'i', 'loved', 'it', '.'], ['but', 'it', 'was', 'also', 'very', 'very', 'very', 'pity', 'pity', 'pity', 'pity', 'for', 'me', '.', ':-(', '@real_trump', '#shetlife', '#readytogo', 'http://www.absurd.com']]
        text_list = [
         self.test_dict_row_en_1['id'], self.test_dict_row_en_1['text']]
        extracted_redu_in_text_container = [[], [{'start_index_in_orig': 4, 'length': 3, 'word': 'very', 'index_in_redu_free': 4}, {'start_index_in_orig': 7, 'length': 4, 'word': 'pity', 'index_in_redu_free': 5}]]
        redu_free_text_container = [['i', 'loved', 'it', '.'], ['but', 'it', 'was', 'also', ('very', {'very': 1, 'ver^4y^5': 1, 'v^3er^8y': 1}), ('pity', {'pity': 2, 'pi^3t^3y^3': 1, 'pi^9ty': 1}), 'for', 'me', '.', ':-(', '@real_trump', '#shetlife', '#readytogo', 'http://www.absurd.com']]
        rle_for_repl_in_text_container = [['', '', '', ''], ['', '', '', '', 'ver^4y^5', 'v^3er^8y', '', 'pi^9ty', '', '', 'pi^3t^3y^3', '', '', '.^6', ':-(^5', '', '', '', '']]
        repl_free_text_container = [['i', 'loved', 'it', '.'], ['but', 'it', 'was', 'also', 'very', 'very', 'very', 'pity', 'pity', 'pity', 'pity', 'for', 'me', '.', ':-(', '@real_trump', '#shetlife', '#readytogo', 'http://www.absurd.com']]
        mapping_redu = [[0, 1, 2, 3], [0, 1, 2, 3, 4, 7, 11, 12, 13, 14, 15, 16, 17, 18]]
        stemmed_text_container = [ [ stemmer.stemWord(token) if isinstance(token, (str, unicode)) else stemmer.stemWord(token[0]) for token in sent ] for sent in redu_free_text_container ]
        stats.insert_redu_into_db(text_list, json.loads(self.test_dict_row_en_1['text']), extracted_redu_in_text_container, redu_free_text_container, rle_for_repl_in_text_container, repl_free_text_container, mapping_redu, stemmed_text_container)
        stats._write_repl_into_db(thread_name='Thread0')
        stats._write_redu_into_db(thread_name='Thread0')
        inserted_columns = list(stats.statsdb.getall('reduplications'))
        right_output = [(1, 1111, '[4, 14]', '[1, 4]', '[1, 4]', 'very', 'veri', '{"very": 1, "ver^4y^5": 1, "v^3er^8y": 1}',
 3, 'JJ', '["negative", -0.1875]', '.', '["symbol", null, "."]', 'but', '["CC", null, "but"]',
 'it', '["PRP", null, "it"]', 'was', '["VBD", null, "was"]', 'also', '["RB", null, "also"]',
 'pity', '["JJ", {"pity": 2, "pi^3t^3y^3": 1, "pi^9ty": 1}, "piti"]', 'for', '["IN", null, "for"]',
 'me', '["PRP", null, "me"]', '.', '["symbol", null, "."]', ':-(', '["EMOASC", null, ":-("]'), (2, 1111, '[4, 14]', '[1, 7]', '[1, 5]', 'pity', 'piti', '{"pity": 2, "pi^3t^3y^3": 1, "pi^9ty": 1}',
 4, 'JJ', '["negative", -0.1875]', 'but', '["CC", null, "but"]', 'it', '["PRP", null, "it"]',
 'was', '["VBD", null, "was"]', 'also', '["RB", null, "also"]', 'very', '["JJ", {"very": 1, "ver^4y^5": 1, "v^3er^8y": 1}, "veri"]',
 'for', '["IN", null, "for"]', 'me', '["PRP", null, "me"]', '.', '["symbol", null, "."]',
 ':-(', '["EMOASC", null, ":-("]', '@real_trump', '["mention", null, "@real_trump"]')]
        inserted_columns.should.be.equal(right_output)
        stats = Stats(mode=self.mode)
        stats.init(self.tempdir_project_folder, name, language, visibility, corpus_id=corpus_id, version=version, encryption_key=encryption_key, baseline_delimiter='++')
        stats._init_compution_variables()
        stats._init_preprocessors()
        stats.corp = corp
        stats._corp_info = corp.info()
        repl_free_en_row_lowercased_2 = [
         [
          'tiny', 'model', ',', 'but', 'a', 'big', 'big', 'big', 'explanation', '.'], ['right', '?'], ['what', 'do', 'you', 'think', 'about', 'it', '?']]
        text_list = [
         self.test_dict_row_en_2['id'], self.test_dict_row_en_2['text']]
        extracted_redu_in_text_container = [[{'start_index_in_orig': 5, 'length': 3, 'word': 'big', 'index_in_redu_free': 5}], [], []]
        redu_free_text_container = [['tiny', 'model', ',', 'but', 'a', ('big', {'big': 3}), 'explanation', '.'], ['right', '?'], ['what', 'do', 'you', 'think', 'about', 'it', '?']]
        rle_for_repl_in_text_container = [['', '', '', '', '', '', '', '', 'expla^5nation', ''], ['ri^6ght', ''], ['', '', 'you^6', '', '', '', '?^4']]
        repl_free_text_container = [['tiny', 'model', ',', 'but', 'a', 'big', 'big', 'big', 'explanation', '.'], ['right', '?'], ['what', 'do', 'you', 'think', 'about', 'it', '?']]
        mapping_redu = [[0, 1, 2, 3, 4, 5, 8, 9], [0, 1], [0, 1, 2, 3, 4, 5, 6]]
        stemmed_text_container = [ [ stemmer.stemWord(token) if isinstance(token, (str, unicode)) else stemmer.stemWord(token[0]) for token in sent ] for sent in redu_free_text_container ]
        stats.insert_redu_into_db(text_list, json.loads(self.test_dict_row_en_2['text']), extracted_redu_in_text_container, redu_free_text_container, rle_for_repl_in_text_container, repl_free_text_container, mapping_redu, stemmed_text_container)
        stats._write_repl_into_db(thread_name='Thread0')
        stats._write_redu_into_db(thread_name='Thread0')
        inserted_columns = list(stats.statsdb.getall('reduplications'))
        right_output = [(1, 5555, '[8, 2, 7]', '[0, 5]', '[0, 5]', 'big', 'big', '{"big": 3}', 3, 'JJ', '["neutral", 0.0]',
 'tiny', '["JJ", null, "tini"]', 'model', '["NN", null, "model"]', ',', '["symbol", null, ","]',
 'but', '["CC", null, "but"]', 'a', '["DT", null, "a"]', 'explanation', '["NN", null, "explan"]',
 '.', '["symbol", null, "."]', 'right', '["UH", null, "right"]', '?', '["symbol", null, "?"]',
 'what', '["WP", null, "what"]')]
        inserted_columns.should.be.equal(right_output)
        return

    @attr(status='stable')
    def test_compute_baseline_lowercased_606(self):
        self.prj_folder()
        self.test_dbs()
        stats = Stats(mode=self.mode)
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['stats']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'stats'
        stats.init(self.tempdir_project_folder, name, language, visibility, corpus_id=corpus_id, version=version, encryption_key=encryption_key, baseline_delimiter='++')
        stats._init_compution_variables()
        stats._init_preprocessors()
        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_en))
        stats.corp = corp
        stats._corp_info = corp.info()
        inp = [
         [
          'klitze', 'kleine', 'überaschung', '.']]
        extracted_redu_in_text_container = [[{}]]
        stats.compute_baseline(inp, extracted_redu_in_text_container).should.be.equal([('klitze',), ('kleine',), ('überaschung',), ('.',), ('klitze', 'kleine'), ('kleine', 'überaschung'), ('überaschung', '.'), ('klitze', 'kleine', 'überaschung'), ('kleine', 'überaschung', '.'), ('klitze', 'kleine', 'überaschung', '.')])
        inp = [
         [
          '1', '2', '3', '4', '5', '😂', '\U0001f9d1🏻']]
        extracted_redu_in_text_container = [[{}]]
        stats.compute_baseline(inp, extracted_redu_in_text_container).should.be.equal([('1',), ('2',), ('3',), ('4',), ('5',), ('😂',), ('\U0001f9d1🏻',), ('1', '2'), ('2', '3'), ('3', '4'), ('4', '5'), ('5', '😂'), ('😂', '\U0001f9d1🏻'), ('1', '2', '3'), ('2', '3', '4'), ('3', '4', '5'), ('4', '5', '😂'), ('5', '😂', '\U0001f9d1🏻'), ('1', '2', '3', '4'), ('2', '3', '4', '5'), ('3', '4', '5', '😂'), ('4', '5', '😂', '\U0001f9d1🏻'), ('1', '2', '3', '4', '5'), ('2', '3', '4', '5', '😂'), ('3', '4', '5', '😂', '\U0001f9d1🏻'), ('1', '2', '3', '4', '5', '😂'), ('2', '3', '4', '5', '😂', '\U0001f9d1🏻')])
        inp = [
         [
          (
           'klitze', {'klitze': 1, 'kli^4tze': 1}), ('kleine', {'kle^5ine': 1, 'klein^3e': 1}), 'überaschung', '.'], ['trotzdem', 'hat', 'sie', 'mich', 'glücklich', 'gemacht', '!', ':-)', '-)']]
        extracted_redu_in_text_container = [[{'start_index_in_orig': 0, 'length': 2, 'word': 'klitze', 'index_in_redu_free': 0}, {'start_index_in_orig': 2, 'length': 2, 'word': 'kleine', 'index_in_redu_free': 1}], []]
        set(stats.compute_baseline(inp, extracted_redu_in_text_container)).should.be.equal(set([('klitze',), ('kleine',), ('überaschung',), ('.',), ('trotzdem',), ('hat',), ('sie',), ('mich',), ('glücklich',), ('gemacht',), ('!',), (':-)',), ('-)',), ('klitze', 'kleine'), ('kleine', 'überaschung'), ('überaschung', '.'), ('.', 'trotzdem'), ('trotzdem', 'hat'), ('hat', 'sie'), ('sie', 'mich'), ('mich', 'glücklich'), ('glücklich', 'gemacht'), ('gemacht', '!'), ('!', ':-)'), (':-)', '-)'), ('klitze', 'kleine', 'überaschung'), ('kleine', 'überaschung', '.'), ('überaschung', '.', 'trotzdem'), ('.', 'trotzdem', 'hat'), ('trotzdem', 'hat', 'sie'), ('hat', 'sie', 'mich'), ('sie', 'mich', 'glücklich'), ('mich', 'glücklich', 'gemacht'), ('glücklich', 'gemacht', '!'), ('gemacht', '!', ':-)'), ('!', ':-)', '-)'), ('klitze', 'kleine', 'überaschung', '.'), ('kleine', 'überaschung', '.', 'trotzdem'), ('überaschung', '.', 'trotzdem', 'hat'), ('.', 'trotzdem', 'hat', 'sie'), ('trotzdem', 'hat', 'sie', 'mich'), ('hat', 'sie', 'mich', 'glücklich'), ('sie', 'mich', 'glücklich', 'gemacht'), ('mich', 'glücklich', 'gemacht', '!'), ('glücklich', 'gemacht', '!', ':-)'), ('gemacht', '!', ':-)', '-)'), ('klitze', 'kleine', 'überaschung', '.', 'trotzdem'), ('kleine', 'überaschung', '.', 'trotzdem', 'hat'), ('überaschung', '.', 'trotzdem', 'hat', 'sie'), ('.', 'trotzdem', 'hat', 'sie', 'mich'), ('trotzdem', 'hat', 'sie', 'mich', 'glücklich'), ('hat', 'sie', 'mich', 'glücklich', 'gemacht'), ('sie', 'mich', 'glücklich', 'gemacht', '!'), ('mich', 'glücklich', 'gemacht', '!', ':-)'), ('glücklich', 'gemacht', '!', ':-)', '-)'), ('klitze', 'kleine', 'überaschung', '.', 'trotzdem', 'hat'), ('kleine', 'überaschung', '.', 'trotzdem', 'hat', 'sie'), ('überaschung', '.', 'trotzdem', 'hat', 'sie', 'mich'), ('.', 'trotzdem', 'hat', 'sie', 'mich', 'glücklich'), ('trotzdem', 'hat', 'sie', 'mich', 'glücklich', 'gemacht'), ('hat', 'sie', 'mich', 'glücklich', 'gemacht', '!'), ('sie', 'mich', 'glücklich', 'gemacht', '!', ':-)'), ('mich', 'glücklich', 'gemacht', '!', ':-)', '-)')]))
        inp = [
         [
          'i', 'loved', 'it', '.'], ['but', 'it', 'was', 'also', 'very', 'pity', 'for', 'me', '.', ':-(', '@real_trump', '#sheetlife', '#readytogo', 'http://www.absurd.com']]
        extracted_redu_in_text_container = [[], [{'start_index_in_orig': 4, 'length': 3, 'word': 'very', 'index_in_redu_free': 4}, {'start_index_in_orig': 7, 'length': 4, 'word': 'pity', 'index_in_redu_free': 5}]]
        set(stats.compute_baseline(inp, extracted_redu_in_text_container)).should.be.equal(set([('i',), ('loved',), ('it',), ('.',), ('but',), ('it',), ('was',), ('also',), ('very',), ('pity',), ('for',), ('me',), ('.',), (':-(',), ('@real_trump',), ('#sheetlife',), ('#readytogo',), ('http://www.absurd.com',), ('i', 'loved'), ('loved', 'it'), ('it', '.'), ('.', 'but'), ('but', 'it'), ('it', 'was'), ('was', 'also'), ('also', 'very'), ('very', 'pity'), ('pity', 'for'), ('for', 'me'), ('me', '.'), ('.', ':-('), (':-(', '@real_trump'), ('@real_trump', '#sheetlife'), ('#sheetlife', '#readytogo'), ('#readytogo', 'http://www.absurd.com'), ('i', 'loved', 'it'), ('loved', 'it', '.'), ('it', '.', 'but'), ('.', 'but', 'it'), ('but', 'it', 'was'), ('it', 'was', 'also'), ('was', 'also', 'very'), ('also', 'very', 'pity'), ('very', 'pity', 'for'), ('pity', 'for', 'me'), ('for', 'me', '.'), ('me', '.', ':-('), ('.', ':-(', '@real_trump'), (':-(', '@real_trump', '#sheetlife'), ('@real_trump', '#sheetlife', '#readytogo'), ('#sheetlife', '#readytogo', 'http://www.absurd.com'), ('i', 'loved', 'it', '.'), ('loved', 'it', '.', 'but'), ('it', '.', 'but', 'it'), ('.', 'but', 'it', 'was'), ('but', 'it', 'was', 'also'), ('it', 'was', 'also', 'very'), ('was', 'also', 'very', 'pity'), ('also', 'very', 'pity', 'for'), ('very', 'pity', 'for', 'me'), ('pity', 'for', 'me', '.'), ('for', 'me', '.', ':-('), ('me', '.', ':-(', '@real_trump'), ('.', ':-(', '@real_trump', '#sheetlife'), (':-(', '@real_trump', '#sheetlife', '#readytogo'), ('@real_trump', '#sheetlife', '#readytogo', 'http://www.absurd.com'), ('i', 'loved', 'it', '.', 'but'), ('loved', 'it', '.', 'but', 'it'), ('it', '.', 'but', 'it', 'was'), ('.', 'but', 'it', 'was', 'also'), ('but', 'it', 'was', 'also', 'very'), ('it', 'was', 'also', 'very', 'pity'), ('was', 'also', 'very', 'pity', 'for'), ('also', 'very', 'pity', 'for', 'me'), ('very', 'pity', 'for', 'me', '.'), ('pity', 'for', 'me', '.', ':-('), ('for', 'me', '.', ':-(', '@real_trump'), ('me', '.', ':-(', '@real_trump', '#sheetlife'), ('.', ':-(', '@real_trump', '#sheetlife', '#readytogo'), (':-(', '@real_trump', '#sheetlife', '#readytogo', 'http://www.absurd.com'), ('i', 'loved', 'it', '.', 'but', 'it'), ('loved', 'it', '.', 'but', 'it', 'was'), ('it', '.', 'but', 'it', 'was', 'also'), ('.', 'but', 'it', 'was', 'also', 'very'), ('but', 'it', 'was', 'also', 'very', 'pity'), ('it', 'was', 'also', 'very', 'pity', 'for'), ('was', 'also', 'very', 'pity', 'for', 'me'), ('also', 'very', 'pity', 'for', 'me', '.'), ('very', 'pity', 'for', 'me', '.', ':-('), ('pity', 'for', 'me', '.', ':-(', '@real_trump'), ('for', 'me', '.', ':-(', '@real_trump', '#sheetlife'), ('me', '.', ':-(', '@real_trump', '#sheetlife', '#readytogo'), ('.', ':-(', '@real_trump', '#sheetlife', '#readytogo', 'http://www.absurd.com'), ('very',), ('very',), ('pity',), ('pity',), ('pity',)]))

    @attr(status='stable')
    def test_temporize_baseline_lowercased_607_1(self):
        self.prj_folder()
        self.test_dbs()
        stats = Stats(mode=self.mode)
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['stats']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'stats'
        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_en))
        stats = Stats(mode=self.mode)
        stats.init(self.tempdir_project_folder, name, language, visibility, corpus_id=corpus_id, version=version, encryption_key=encryption_key, baseline_delimiter='++')
        stats._init_compution_variables()
        stats._init_preprocessors()
        stats.corp = corp
        stats._corp_info = corp.info()
        stats._init_compution_variables()
        computed_baseline = [
         (
          'klitze',), ('kleine',), ('überaschung',), ('.',), ('klitze', 'kleine'), ('kleine', 'überaschung'), ('überaschung', '.'), ('klitze', 'kleine', 'überaschung'), ('kleine', 'überaschung', '.'), ('klitze', 'kleine', 'überaschung', '.')]
        extracted_redu_in_text_container = ((), ())
        stats.temporize_baseline(computed_baseline, extracted_redu_in_text_container)
        stats.temporized_baseline.should.be.equal({('.',): 1, ('kleine',): 1, 
           ('kleine', 'überaschung'): 1, 
           ('kleine', 'überaschung', '.'): 1, 
           ('klitze',): 1, 
           ('klitze', 'kleine'): 1, 
           ('klitze', 'kleine', 'überaschung'): 1, 
           ('klitze', 'kleine', 'überaschung', '.'): 1, 
           ('überaschung',): 1, 
           ('überaschung', '.'): 1})
        stats.temporize_baseline(computed_baseline, extracted_redu_in_text_container)
        stats.temporized_baseline.should.be.equal({('.',): 2, ('kleine',): 2, 
           ('kleine', 'überaschung'): 2, 
           ('kleine', 'überaschung', '.'): 2, 
           ('klitze',): 2, 
           ('klitze', 'kleine'): 2, 
           ('klitze', 'kleine', 'überaschung'): 2, 
           ('klitze', 'kleine', 'überaschung', '.'): 2, 
           ('überaschung',): 2, 
           ('überaschung', '.'): 2})
        stats._init_compution_variables()
        computed_baseline = [('1',), ('2',), ('3',), ('4',), ('5',), ('😂',), ('\U0001f9d1🏻',), ('1', '2'), ('2', '3'), ('3', '4'), ('4', '5'), ('5', '😂'), ('😂', '\U0001f9d1🏻'), ('1', '2', '3'), ('2', '3', '4'), ('3', '4', '5'), ('4', '5', '😂'), ('5', '😂', '\U0001f9d1🏻'), ('1', '2', '3', '4'), ('2', '3', '4', '5'), ('3', '4', '5', '😂'), ('4', '5', '😂', '\U0001f9d1🏻'), ('1', '2', '3', '4', '5'), ('2', '3', '4', '5', '😂'), ('3', '4', '5', '😂', '\U0001f9d1🏻'), ('1', '2', '3', '4', '5', '😂'), ('2', '3', '4', '5', '😂', '\U0001f9d1🏻'), ('1', '2', '3', '4', '5', '😂', '\U0001f9d1🏻')]
        stats.temporize_baseline(computed_baseline, extracted_redu_in_text_container)
        stats.temporized_baseline.should.be.equal({('1',): 1, ('1', '2'): 1, 
           ('1', '2', '3'): 1, 
           ('1', '2', '3', '4'): 1, 
           ('1', '2', '3', '4', '5'): 1, 
           ('1', '2', '3', '4', '5', '😂'): 1, 
           ('1', '2', '3', '4', '5', '😂', '\U0001f9d1🏻'): 1, 
           ('2',): 1, 
           ('2', '3'): 1, 
           ('2', '3', '4'): 1, 
           ('2', '3', '4', '5'): 1, 
           ('2', '3', '4', '5', '😂'): 1, 
           ('2', '3', '4', '5', '😂', '\U0001f9d1🏻'): 1, 
           ('3',): 1, 
           ('3', '4'): 1, 
           ('3', '4', '5'): 1, 
           ('3', '4', '5', '😂'): 1, 
           ('3', '4', '5', '😂', '\U0001f9d1🏻'): 1, 
           ('4',): 1, 
           ('4', '5'): 1, 
           ('4', '5', '😂'): 1, 
           ('4', '5', '😂', '\U0001f9d1🏻'): 1, 
           ('5',): 1, 
           ('5', '😂'): 1, 
           ('5', '😂', '\U0001f9d1🏻'): 1, 
           ('😂',): 1, 
           ('😂', '\U0001f9d1🏻'): 1, 
           ('\U0001f9d1🏻',): 1})

    @attr(status='stable')
    def test_baseline_lazyinsertion_into_db_lowercased_607_2(self):
        self.prj_folder()
        self.test_dbs()
        stats = Stats(mode=self.mode)
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['stats']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'stats'
        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_en))
        stats = Stats(mode=self.mode)
        stats.init(self.tempdir_project_folder, name, language, visibility, corpus_id=corpus_id, version=version, encryption_key=encryption_key, baseline_delimiter='++')
        stats._init_compution_variables()
        stats._init_preprocessors()
        stats.corp = corp
        stats._corp_info = corp.info()
        stats._init_stemmer(stats._corp_info['language'])
        stats._init_compution_variables()
        computed_baseline = [
         ('klitze', ), ('kleine', ), ('überaschung', ), ('.', ), ('klitze', 'kleine'), ('kleine', 'überaschung'), ('überaschung', '.'), ('klitze', 'kleine', 'überaschung'), ('kleine', 'überaschung', '.'), ('klitze', 'kleine', 'überaschung', '.')]
        extracted_redu_in_text_container = [
         [
          {'word': 'klitze', 'length': 2}]]
        stats.baseline_lazyinsertion_into_db(computed_baseline, extracted_redu_in_text_container)
        stats.statsdb.getall('baseline').should.be.equal([])
        stats.baseline_insert_left_over_data()
        inserted_baseline = stats.statsdb.getall('baseline')
        baseline_should_be_in_the_db = [
         ('überaschung', 'überaschung', 1, 1, None, None, None, None, None, None),
         ('klitze++kleine++überaschung++.', 'klitz++klein++überaschung++.', 4, 1, None, None,
 None, None, None, None),
         ('kleine++überaschung++.', 'klein++überaschung++.', 3, 1, None, None, None, None, None,
 None),
         ('kleine++überaschung', 'klein++überaschung', 2, 1, None, None, None, None, None, None),
         ('überaschung++.', 'überaschung++.', 2, 1, None, None, None, None, None, None),
         ('klitze++kleine++überaschung', 'klitz++klein++überaschung', 3, 1, None, None, None,
 None, None, None),
         ('klitze++kleine', 'klitz++klein', 2, 1, None, None, None, None, None, None),
         ('.', '.', 1, 1, None, None, None, None, None, None),
         ('klitze', 'klitz', 1, 2, None, None, None, None, None, None),
         ('kleine', 'klein', 1, 1, None, None, None, None, None, None)]
        set(inserted_baseline).should.be.equal(set(baseline_should_be_in_the_db))
        stats.baseline_lazyinsertion_into_db(computed_baseline, extracted_redu_in_text_container, baseline_insertion_border=1)
        stats.baseline_lazyinsertion_into_db(computed_baseline, extracted_redu_in_text_container, baseline_insertion_border=1)
        stats.baseline_insert_left_over_data()
        inserted_baseline = stats.statsdb.getall('baseline')
        baseline_should_be_in_the_db = [
         ('kleine++überaschung', 'klein++überaschung', 2, 3, None, None, None, None, None, None),
         ('überaschung', 'überaschung', 1, 3, None, None, None, None, None, None),
         ('klitze++kleine++überaschung++.', 'klitz++klein++überaschung++.', 4, 3, None, None,
 None, None, None, None),
         ('klitze++kleine', 'klitz++klein', 2, 3, None, None, None, None, None, None),
         ('kleine++überaschung++.', 'klein++überaschung++.', 3, 3, None, None, None, None, None,
 None),
         ('klitze', 'klitz', 1, 6, None, None, None, None, None, None),
         ('überaschung++.', 'überaschung++.', 2, 3, None, None, None, None, None, None),
         ('klitze++kleine++überaschung', 'klitz++klein++überaschung', 3, 3, None, None, None,
 None, None, None),
         ('.', '.', 1, 3, None, None, None, None, None, None),
         ('kleine', 'klein', 1, 3, None, None, None, None, None, None)]
        set(inserted_baseline).should.be.equal(set(baseline_should_be_in_the_db))
        return

    @attr(status='stable')
    def test_intern_compute_function_lower_case_608(self):
        self.prj_folder()
        self.test_dbs()
        stats = Stats(mode=self.mode, status_bar=False)
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['stats']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'stats'
        stats.init(self.tempdir_project_folder, name, language, visibility, corpus_id=corpus_id, version=version, encryption_key=encryption_key, baseline_delimiter='++')
        stats._init_compution_variables()
        stats._init_preprocessors()
        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_en))
        stats.corp = corp
        stats._corp_info = corp.info()
        stats._init_stemmer(stats._corp_info['language'])
        import time
        text_list = [
         self.test_dict_row_de_1['id'], self.test_dict_row_de_1['text']]
        stats._compute([copy.deepcopy(text_list)])
        redu = stats.statsdb.getall('reduplications')
        repl = stats.statsdb.getall('replications')
        baseline = stats.statsdb.getall('baseline')
        redu.should.be.equal([
         (
          1, 8888, '[4, 9]', '[0, 0]', '[0, 0]', 'klitze', 'klitz', '{"klitze": 1, "kli^4tze": 1}', 2, 'NN', '["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, 'kleine', '["NE", {"kle^5ine": 1, "klein^3e": 1}, "klein"]', 'überaschung', '["NN", null, "\\u00fcberaschung"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzdem"]', 'hat', '["VAFIN", null, "hat"]'), (2, 8888, '[4, 9]', '[0, 2]', '[0, 1]', 'kleine', 'klein', '{"kle^5ine": 1, "klein^3e": 1}', 2, 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze": 1}, "klitz"]', 'überaschung', '["NN", null, "\\u00fcberaschung"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzdem"]', 'hat', '["VAFIN", null, "hat"]', 'sie', '["PPER", null, "sie"]')])
        repl.should.be.equal([
         (
          1, 8888, '[4, 9]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze', 'klitz', 'i', 4, 2, '[0, 0]', 'NN', '["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, 'kleine', '["NE", {"kle^5ine": 1, "klein^3e": 1}, "klein"]', 'überaschung', '["NN", null, "\\u00fcberaschung"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzdem"]', 'hat', '["VAFIN", null, "hat"]'), (2, 8888, '[4, 9]', '[0, 2]', '[0, 1]', 'kleine', 'kle^5ine', 'klein', 'e', 5, 2, '[0, 1]', 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze": 1}, "klitz"]', 'überaschung', '["NN", null, "\\u00fcberaschung"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzdem"]', 'hat', '["VAFIN", null, "hat"]', 'sie', '["PPER", null, "sie"]'), (3, 8888, '[4, 9]', '[0, 3]', '[0, 1]', 'kleine', 'klein^3e', 'klein', 'n', 3, 4, '[0, 1]', 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze": 1}, "klitz"]', 'überaschung', '["NN", null, "\\u00fcberaschung"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzdem"]', 'hat', '["VAFIN", null, "hat"]', 'sie', '["PPER", null, "sie"]'), (4, 8888, '[4, 9]', '[1, 7]', '[1, 7]', ':-)', ':-)^4', ':-)', ')', 4, 2, None, 'EMOASC', '["positive", 0.5]', 'sie', '["PPER", null, "sie"]', 'mich', '["PPER", null, "mich"]', 'glücklich', '["ADJD", null, "gl\\u00fccklich"]', 'gemacht', '["VVPP", null, "gemacht"]', '!', '["symbol", null, "!"]', '-)', '["EMOASC", null, "-)"]', None, None, None, None, None, None, None, None), (5, 8888, '[4, 9]', '[1, 8]', '[1, 8]', '-)', '-)^3', '-)', ')', 3, 1, None, 'EMOASC', '["positive", 0.5]', 'mich', '["PPER", null, "mich"]', 'glücklich', '["ADJD", null, "gl\\u00fccklich"]', 'gemacht', '["VVPP", null, "gemacht"]', '!', '["symbol", null, "!"]', ':-)', '["EMOASC", null, ":-)"]', None, None, None, None, None, None, None, None, None, None)])
        baseline.should.be.equal([('.++trotzdem', '.++trotzdem', 2, 1, None, None, None, None, None, None), ('!', '!', 1, 1, None, None, None, None, None, None), ('hat++sie++mich', 'hat++sie++mich', 3, 1, None, None, None, None, None, None), ('sie++mich++glücklich++gemacht++!', 'sie++mich++glücklich++gemacht++!', 5, 1, None, None, None, None, None, None), ('gemacht++!', 'gemacht++!', 2, 1, None, None, None, None, None, None), ('glücklich++gemacht', 'glücklich++gemacht', 2, 1, None, None, None, None, None, None), ('sie++mich++glücklich', 'sie++mich++glücklich', 3, 1, None, None, None, None, None, None), (':-)', ':-)', 1, 1, None, None, None, None, None, None), ('mich++glücklich++gemacht++!++:-)++-)', 'mich++glücklich++gemacht++!++:-)++-)', 6, 1, None, None, None, None, None, None), ('glücklich', 'glücklich', 1, 1, None, None, None, None, None, None), ('glücklich++gemacht++!++:-)++-)', 'glücklich++gemacht++!++:-)++-)', 5, 1, None, None, None, None, None, None), ('.++trotzdem++hat++sie++mich++glücklich', '.++trotzdem++hat++sie++mich++glücklich', 6, 1, None, None, None, None, None, None), ('gemacht++!++:-)++-)', 'gemacht++!++:-)++-)', 4, 1, None, None, None, None, None, None), ('klitze++kleine++überaschung++.++trotzdem++hat', 'klitz++klein++überaschung++.++trotzdem++hat', 6, 1, None, None, None, None, None, None), ('mich++glücklich++gemacht', 'mich++glücklich++gemacht', 3, 1, None, None, None, None, None, None), ('gemacht', 'gemacht', 1, 1, None, None, None, None, None, None), ('!++:-)', '!++:-)', 2, 1, None, None, None, None, None, None), ('.++trotzdem++hat++sie++mich', '.++trotzdem++hat++sie++mich', 5, 1, None, None, None, None, None, None), ('trotzdem++hat++sie++mich++glücklich++gemacht', 'trotzdem++hat++sie++mich++glücklich++gemacht', 6, 1, None, None, None, None, None, None), ('überaschung++.++trotzdem', 'überaschung++.++trotzdem', 3, 1, None, None, None, None, None, None), ('klitze++kleine++überaschung++.++trotzdem', 'klitz++klein++überaschung++.++trotzdem', 5, 1, None, None, None, None, None, None), (':-)++-)', ':-)++-)', 2, 1, None, None, None, None, None, None), ('glücklich++gemacht++!', 'glücklich++gemacht++!', 3, 1, None, None, None, None, None, None), ('überaschung++.', 'überaschung++.', 2, 1, None, None, None, None, None, None), ('hat++sie++mich++glücklich++gemacht', 'hat++sie++mich++glücklich++gemacht', 5, 1, None, None, None, None, None, None), ('trotzdem++hat++sie++mich++glücklich', 'trotzdem++hat++sie++mich++glücklich', 5, 1, None, None, None, None, None, None), ('klitze++kleine', 'klitz++klein', 2, 1, None, None, None, None, None, None), ('sie++mich++glücklich++gemacht++!++:-)', 'sie++mich++glücklich++gemacht++!++:-)', 6, 1, None, None, None, None, None, None), ('überaschung', 'überaschung', 1, 1, None, None, None, None, None, None), ('trotzdem++hat++sie', 'trotzdem++hat++sie', 3, 1, None, None, None, None, None, None), ('kleine', 'klein', 1, 2, None, None, None, None, None, None), ('-)', '-)', 1, 1, None, None, None, None, None, None), ('trotzdem++hat++sie++mich', 'trotzdem++hat++sie++mich', 4, 1, None, None, None, None, None, None), ('trotzdem++hat', 'trotzdem++hat', 2, 1, None, None, None, None, None, None), ('.', '.', 1, 1, None, None, None, None, None, None), ('trotzdem', 'trotzdem', 1, 1, None, None, None, None, None, None), ('hat', 'hat', 1, 1, None, None, None, None, None, None), ('mich', 'mich', 1, 1, None, None, None, None, None, None), ('.++trotzdem++hat', '.++trotzdem++hat', 3, 1, None, None, None, None, None, None), ('klitze', 'klitz', 1, 2, None, None, None, None, None, None), ('hat++sie', 'hat++sie', 2, 1, None, None, None, None, None, None), ('hat++sie++mich++glücklich++gemacht++!', 'hat++sie++mich++glücklich++gemacht++!', 6, 1, None, None, None, None, None, None), ('gemacht++!++:-)', 'gemacht++!++:-)', 3, 1, None, None, None, None, None, None), ('hat++sie++mich++glücklich', 'hat++sie++mich++glücklich', 4, 1, None, None, None, None, None, None), ('kleine++überaschung++.++trotzdem', 'klein++überaschung++.++trotzdem', 4, 1, None, None, None, None, None, None), ('kleine++überaschung++.++trotzdem++hat', 'klein++überaschung++.++trotzdem++hat', 5, 1, None, None, None, None, None, None), ('.++trotzdem++hat++sie', '.++trotzdem++hat++sie', 4, 1, None, None, None, None, None, None), ('kleine++überaschung++.++trotzdem++hat++sie', 'klein++überaschung++.++trotzdem++hat++sie', 6, 1, None, None, None, None, None, None), ('überaschung++.++trotzdem++hat++sie++mich', 'überaschung++.++trotzdem++hat++sie++mich', 6, 1, None, None, None, None, None, None), ('mich++glücklich++gemacht++!++:-)', 'mich++glücklich++gemacht++!++:-)', 5, 1, None, None, None, None, None, None), ('mich++glücklich', 'mich++glücklich', 2, 1, None, None, None, None, None, None), ('überaschung++.++trotzdem++hat++sie', 'überaschung++.++trotzdem++hat++sie', 5, 1, None, None, None, None, None, None), ('sie++mich', 'sie++mich', 2, 1, None, None, None, None, None, None), ('sie', 'sie', 1, 1, None, None, None, None, None, None), ('glücklich++gemacht++!++:-)', 'glücklich++gemacht++!++:-)', 4, 1, None, None, None, None, None, None), ('klitze++kleine++überaschung', 'klitz++klein++überaschung', 3, 1, None, None, None, None, None, None), ('überaschung++.++trotzdem++hat', 'überaschung++.++trotzdem++hat', 4, 1, None, None, None, None, None, None), ('klitze++kleine++überaschung++.', 'klitz++klein++überaschung++.', 4, 1, None, None, None, None, None, None), ('!++:-)++-)', '!++:-)++-)', 3, 1, None, None, None, None, None, None), ('mich++glücklich++gemacht++!', 'mich++glücklich++gemacht++!', 4, 1, None, None, None, None, None, None), ('kleine++überaschung++.', 'klein++überaschung++.', 3, 1, None, None, None, None, None, None), ('sie++mich++glücklich++gemacht', 'sie++mich++glücklich++gemacht', 4, 1, None, None, None, None, None, None), ('kleine++überaschung', 'klein++überaschung', 2, 1, None, None, None, None, None, None)])
        text_list = [
         self.test_dict_row_de_1['id'], self.test_dict_row_de_1['text']]
        stats._compute([copy.deepcopy(text_list)])
        redu = stats.statsdb.getall('reduplications')
        repl = stats.statsdb.getall('replications')
        baseline = stats.statsdb.getall('baseline')
        redu.should.be.equal([
         (
          1, 8888, '[4, 9]', '[0, 0]', '[0, 0]', 'klitze', 'klitz', '{"klitze": 1, "kli^4tze": 1}', 2, 'NN', '["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, 'kleine', '["NE", {"kle^5ine": 1, "klein^3e": 1}, "klein"]', 'überaschung', '["NN", null, "\\u00fcberaschung"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzdem"]', 'hat', '["VAFIN", null, "hat"]'), (2, 8888, '[4, 9]', '[0, 2]', '[0, 1]', 'kleine', 'klein', '{"kle^5ine": 1, "klein^3e": 1}', 2, 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze": 1}, "klitz"]', 'überaschung', '["NN", null, "\\u00fcberaschung"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzdem"]', 'hat', '["VAFIN", null, "hat"]', 'sie', '["PPER", null, "sie"]'), (3, 8888, '[4, 9]', '[0, 0]', '[0, 0]', 'klitze', 'klitz', '{"klitze": 1, "kli^4tze": 1}', 2, 'NN', '["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, 'kleine', '["NE", {"kle^5ine": 1, "klein^3e": 1}, "klein"]', 'überaschung', '["NN", null, "\\u00fcberaschung"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzdem"]', 'hat', '["VAFIN", null, "hat"]'), (4, 8888, '[4, 9]', '[0, 2]', '[0, 1]', 'kleine', 'klein', '{"kle^5ine": 1, "klein^3e": 1}', 2, 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze": 1}, "klitz"]', 'überaschung', '["NN", null, "\\u00fcberaschung"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzdem"]', 'hat', '["VAFIN", null, "hat"]', 'sie', '["PPER", null, "sie"]')])
        repl.should.be.equal([
         (
          1, 8888, '[4, 9]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze', 'klitz', 'i', 4, 2, '[0, 0]', 'NN', '["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, 'kleine', '["NE", {"kle^5ine": 1, "klein^3e": 1}, "klein"]', 'überaschung', '["NN", null, "\\u00fcberaschung"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzdem"]', 'hat', '["VAFIN", null, "hat"]'), (2, 8888, '[4, 9]', '[0, 2]', '[0, 1]', 'kleine', 'kle^5ine', 'klein', 'e', 5, 2, '[0, 1]', 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze": 1}, "klitz"]', 'überaschung', '["NN", null, "\\u00fcberaschung"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzdem"]', 'hat', '["VAFIN", null, "hat"]', 'sie', '["PPER", null, "sie"]'), (3, 8888, '[4, 9]', '[0, 3]', '[0, 1]', 'kleine', 'klein^3e', 'klein', 'n', 3, 4, '[0, 1]', 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze": 1}, "klitz"]', 'überaschung', '["NN", null, "\\u00fcberaschung"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzdem"]', 'hat', '["VAFIN", null, "hat"]', 'sie', '["PPER", null, "sie"]'), (4, 8888, '[4, 9]', '[1, 7]', '[1, 7]', ':-)', ':-)^4', ':-)', ')', 4, 2, None, 'EMOASC', '["positive", 0.5]', 'sie', '["PPER", null, "sie"]', 'mich', '["PPER", null, "mich"]', 'glücklich', '["ADJD", null, "gl\\u00fccklich"]', 'gemacht', '["VVPP", null, "gemacht"]', '!', '["symbol", null, "!"]', '-)', '["EMOASC", null, "-)"]', None, None, None, None, None, None, None, None), (5, 8888, '[4, 9]', '[1, 8]', '[1, 8]', '-)', '-)^3', '-)', ')', 3, 1, None, 'EMOASC', '["positive", 0.5]', 'mich', '["PPER", null, "mich"]', 'glücklich', '["ADJD", null, "gl\\u00fccklich"]', 'gemacht', '["VVPP", null, "gemacht"]', '!', '["symbol", null, "!"]', ':-)', '["EMOASC", null, ":-)"]', None, None, None, None, None, None, None, None, None, None), (6, 8888, '[4, 9]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze', 'klitz', 'i', 4, 2, '[0, 0]', 'NN', '["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, 'kleine', '["NE", {"kle^5ine": 1, "klein^3e": 1}, "klein"]', 'überaschung', '["NN", null, "\\u00fcberaschung"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzdem"]', 'hat', '["VAFIN", null, "hat"]'), (7, 8888, '[4, 9]', '[0, 2]', '[0, 1]', 'kleine', 'kle^5ine', 'klein', 'e', 5, 2, '[0, 1]', 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze": 1}, "klitz"]', 'überaschung', '["NN", null, "\\u00fcberaschung"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzdem"]', 'hat', '["VAFIN", null, "hat"]', 'sie', '["PPER", null, "sie"]'), (8, 8888, '[4, 9]', '[0, 3]', '[0, 1]', 'kleine', 'klein^3e', 'klein', 'n', 3, 4, '[0, 1]', 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze": 1}, "klitz"]', 'überaschung', '["NN", null, "\\u00fcberaschung"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzdem"]', 'hat', '["VAFIN", null, "hat"]', 'sie', '["PPER", null, "sie"]'), (9, 8888, '[4, 9]', '[1, 7]', '[1, 7]', ':-)', ':-)^4', ':-)', ')', 4, 2, None, 'EMOASC', '["positive", 0.5]', 'sie', '["PPER", null, "sie"]', 'mich', '["PPER", null, "mich"]', 'glücklich', '["ADJD", null, "gl\\u00fccklich"]', 'gemacht', '["VVPP", null, "gemacht"]', '!', '["symbol", null, "!"]', '-)', '["EMOASC", null, "-)"]', None, None, None, None, None, None, None, None), (10, 8888, '[4, 9]', '[1, 8]', '[1, 8]', '-)', '-)^3', '-)', ')', 3, 1, None, 'EMOASC', '["positive", 0.5]', 'mich', '["PPER", null, "mich"]', 'glücklich', '["ADJD", null, "gl\\u00fccklich"]', 'gemacht', '["VVPP", null, "gemacht"]', '!', '["symbol", null, "!"]', ':-)', '["EMOASC", null, ":-)"]', None, None, None, None, None, None, None, None, None, None)])
        baseline.should.be.equal([('.++trotzdem', '.++trotzdem', 2, 2, None, None, None, None, None, None), ('!', '!', 1, 2, None, None, None, None, None, None), ('hat++sie++mich', 'hat++sie++mich', 3, 2, None, None, None, None, None, None), ('sie++mich++glücklich++gemacht++!', 'sie++mich++glücklich++gemacht++!', 5, 2, None, None, None, None, None, None), ('gemacht++!', 'gemacht++!', 2, 2, None, None, None, None, None, None), ('glücklich++gemacht', 'glücklich++gemacht', 2, 2, None, None, None, None, None, None), ('sie++mich++glücklich', 'sie++mich++glücklich', 3, 2, None, None, None, None, None, None), (':-)', ':-)', 1, 2, None, None, None, None, None, None), ('mich++glücklich++gemacht++!++:-)++-)', 'mich++glücklich++gemacht++!++:-)++-)', 6, 2, None, None, None, None, None, None), ('glücklich', 'glücklich', 1, 2, None, None, None, None, None, None), ('glücklich++gemacht++!++:-)++-)', 'glücklich++gemacht++!++:-)++-)', 5, 2, None, None, None, None, None, None), ('.++trotzdem++hat++sie++mich++glücklich', '.++trotzdem++hat++sie++mich++glücklich', 6, 2, None, None, None, None, None, None), ('gemacht++!++:-)++-)', 'gemacht++!++:-)++-)', 4, 2, None, None, None, None, None, None), ('klitze++kleine++überaschung++.++trotzdem++hat', 'klitz++klein++überaschung++.++trotzdem++hat', 6, 2, None, None, None, None, None, None), ('mich++glücklich++gemacht', 'mich++glücklich++gemacht', 3, 2, None, None, None, None, None, None), ('gemacht', 'gemacht', 1, 2, None, None, None, None, None, None), ('!++:-)', '!++:-)', 2, 2, None, None, None, None, None, None), ('.++trotzdem++hat++sie++mich', '.++trotzdem++hat++sie++mich', 5, 2, None, None, None, None, None, None), ('trotzdem++hat++sie++mich++glücklich++gemacht', 'trotzdem++hat++sie++mich++glücklich++gemacht', 6, 2, None, None, None, None, None, None), ('überaschung++.++trotzdem', 'überaschung++.++trotzdem', 3, 2, None, None, None, None, None, None), ('klitze++kleine++überaschung++.++trotzdem', 'klitz++klein++überaschung++.++trotzdem', 5, 2, None, None, None, None, None, None), (':-)++-)', ':-)++-)', 2, 2, None, None, None, None, None, None), ('glücklich++gemacht++!', 'glücklich++gemacht++!', 3, 2, None, None, None, None, None, None), ('überaschung++.', 'überaschung++.', 2, 2, None, None, None, None, None, None), ('hat++sie++mich++glücklich++gemacht', 'hat++sie++mich++glücklich++gemacht', 5, 2, None, None, None, None, None, None), ('trotzdem++hat++sie++mich++glücklich', 'trotzdem++hat++sie++mich++glücklich', 5, 2, None, None, None, None, None, None), ('klitze++kleine', 'klitz++klein', 2, 2, None, None, None, None, None, None), ('sie++mich++glücklich++gemacht++!++:-)', 'sie++mich++glücklich++gemacht++!++:-)', 6, 2, None, None, None, None, None, None), ('überaschung', 'überaschung', 1, 2, None, None, None, None, None, None), ('trotzdem++hat++sie', 'trotzdem++hat++sie', 3, 2, None, None, None, None, None, None), ('kleine', 'klein', 1, 4, None, None, None, None, None, None), ('-)', '-)', 1, 2, None, None, None, None, None, None), ('trotzdem++hat++sie++mich', 'trotzdem++hat++sie++mich', 4, 2, None, None, None, None, None, None), ('trotzdem++hat', 'trotzdem++hat', 2, 2, None, None, None, None, None, None), ('.', '.', 1, 2, None, None, None, None, None, None), ('trotzdem', 'trotzdem', 1, 2, None, None, None, None, None, None), ('hat', 'hat', 1, 2, None, None, None, None, None, None), ('mich', 'mich', 1, 2, None, None, None, None, None, None), ('.++trotzdem++hat', '.++trotzdem++hat', 3, 2, None, None, None, None, None, None), ('klitze', 'klitz', 1, 4, None, None, None, None, None, None), ('hat++sie', 'hat++sie', 2, 2, None, None, None, None, None, None), ('hat++sie++mich++glücklich++gemacht++!', 'hat++sie++mich++glücklich++gemacht++!', 6, 2, None, None, None, None, None, None), ('gemacht++!++:-)', 'gemacht++!++:-)', 3, 2, None, None, None, None, None, None), ('hat++sie++mich++glücklich', 'hat++sie++mich++glücklich', 4, 2, None, None, None, None, None, None), ('kleine++überaschung++.++trotzdem', 'klein++überaschung++.++trotzdem', 4, 2, None, None, None, None, None, None), ('kleine++überaschung++.++trotzdem++hat', 'klein++überaschung++.++trotzdem++hat', 5, 2, None, None, None, None, None, None), ('.++trotzdem++hat++sie', '.++trotzdem++hat++sie', 4, 2, None, None, None, None, None, None), ('kleine++überaschung++.++trotzdem++hat++sie', 'klein++überaschung++.++trotzdem++hat++sie', 6, 2, None, None, None, None, None, None), ('überaschung++.++trotzdem++hat++sie++mich', 'überaschung++.++trotzdem++hat++sie++mich', 6, 2, None, None, None, None, None, None), ('mich++glücklich++gemacht++!++:-)', 'mich++glücklich++gemacht++!++:-)', 5, 2, None, None, None, None, None, None), ('mich++glücklich', 'mich++glücklich', 2, 2, None, None, None, None, None, None), ('überaschung++.++trotzdem++hat++sie', 'überaschung++.++trotzdem++hat++sie', 5, 2, None, None, None, None, None, None), ('sie++mich', 'sie++mich', 2, 2, None, None, None, None, None, None), ('sie', 'sie', 1, 2, None, None, None, None, None, None), ('glücklich++gemacht++!++:-)', 'glücklich++gemacht++!++:-)', 4, 2, None, None, None, None, None, None), ('klitze++kleine++überaschung', 'klitz++klein++überaschung', 3, 2, None, None, None, None, None, None), ('überaschung++.++trotzdem++hat', 'überaschung++.++trotzdem++hat', 4, 2, None, None, None, None, None, None), ('klitze++kleine++überaschung++.', 'klitz++klein++überaschung++.', 4, 2, None, None, None, None, None, None), ('!++:-)++-)', '!++:-)++-)', 3, 2, None, None, None, None, None, None), ('mich++glücklich++gemacht++!', 'mich++glücklich++gemacht++!', 4, 2, None, None, None, None, None, None), ('kleine++überaschung++.', 'klein++überaschung++.', 3, 2, None, None, None, None, None, None), ('sie++mich++glücklich++gemacht', 'sie++mich++glücklich++gemacht', 4, 2, None, None, None, None, None, None), ('kleine++überaschung', 'klein++überaschung', 2, 2, None, None, None, None, None, None)])
        return

    @attr(status='stable')
    def test_get_streams_from_corp_609(self):
        self.prj_folder()
        self.test_dbs()
        stats = Stats(mode=self.mode, status_bar=False)
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['stats']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'stats'
        stats.init(self.tempdir_project_folder, name, language, visibility, corpus_id=corpus_id, version=version, encryption_key=encryption_key, baseline_delimiter='++')
        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_en))
        rownum = corp.corpdb.rownum('documents')
        stats._init_compution_variables()
        stats._text_field_name = corp.info()['text_field_name']
        stats._id_field_name = corp.info()['id_field_name']
        stream_num = 4
        streams = stats.get_streams_from_corpus(corp, stream_num)
        all_rows_from_corpus = []
        for stream in streams:
            rows = list(stream[1])
            all_rows_from_corpus += rows
            len(stream[1]).should.be.equal(len(rows))

        rows_as_text = [ unicode(row) for row in all_rows_from_corpus ]
        len(rows_as_text).should.be.equal(rownum)
        len(rows_as_text).should.be.equal(len(set(rows_as_text)))
        stream_num = 1
        streams = stats.get_streams_from_corpus(corp, stream_num)
        all_rows_from_corpus = []
        for stream in streams:
            rows = list(stream[1])
            all_rows_from_corpus += rows
            len(stream[1]).should.be.equal(len(rows))

        rows_as_text = [ unicode(row) for row in all_rows_from_corpus ]
        len(rows_as_text).should.be.equal(rownum)
        len(rows_as_text).should.be.equal(len(set(rows_as_text)))

    @attr(status='stable')
    def test_preprocess_610(self):
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
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['stats']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'stats'
        stats = Stats(mode=self.mode, use_cash=True)
        stats.init(self.tempdir_project_folder, name, language, visibility, corpus_id=corpus_id, version=version, baseline_delimiter='++', encryption_key=encryption_key, ignore_hashtag=True, force_cleaning=True, ignore_url=True, ignore_mention=True, ignore_punkt=True, ignore_num=True)
        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_en))
        stats.corp = corp
        stats._corp_info = stats.corp.info()
        stats._init_compution_variables()
        stats._compute_cleaning_flags()
        text_elem = [[[['I', 'PRP'], ['loved', 'VBD'], ['it', 'PRP'], ['.', 'symbol']], ['positive', 0.7]], [[['But', 'CC'], ['it', 'PRP'], ['was', 'VBD'], ['also', 'RB'], ['verrrryyyyy', 'JJ'], ['vvveRRRRRRrry', 'NNP'], ['very', 'RB'], ['piiiiiiiiity', 'JJ'], ['pity', 'NN'], ['pity', 'NN'], ['piiitttyyy', 'NN'], ['for', 'IN'], ['me', 'PRP'], ['......', 'symbol'], [':-(((((', 'EMOASC'], ['@real_trump', 'mention'], ['#sheetlife', 'hashtag'], ['#readytogo', 'hashtag'], ['http://www.absurd.com', 'URL']], ['negative', -0.1875]]]
        results = stats._preprocess(text_elem)
        right_results = [
         (
          [
           ('i', 'PRP'), ('loved', 'VBD'), ('it', 'PRP'), (None, ':symbol:')], ['positive', 0.7]), ([('but', 'CC'), ('it', 'PRP'), ('was', 'VBD'), ('also', 'RB'), ('verrrryyyyy', 'JJ'), ('vvverrrrrrrry', 'NNP'), ('very', 'RB'), ('piiiiiiiiity', 'JJ'), ('pity', 'NN'), ('pity', 'NN'), ('piiitttyyy', 'NN'), ('for', 'IN'), ('me', 'PRP'), (None, ':symbol:'), (':-(((((', 'EMOASC'), (None, ':mention:'), (None, ':hashtag:'), (None, ':hashtag:'), (None, ':URL:')], ['negative', -0.1875])]
        results.should.be.equal(right_results)
        return

    @attr(status='stable')
    def test_main_compute_function_lower_case_for_1_stream__610_1(self):
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
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['stats']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'stats'
        stats = Stats(mode=self.mode, use_cash=True)
        stats.init(self.tempdir_project_folder, name, language, visibility, corpus_id=corpus_id, version=version, encryption_key=encryption_key, baseline_delimiter='++')
        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_en))
        stats.compute(corp, stream_number=1, adjust_to_cpu=False, freeze_db=False)
        baseline = stats.statsdb.getall('baseline')
        repls = stats.statsdb.getall('replications')
        redus = stats.statsdb.getall('reduplications')
        self.configer.right_rep_num['en']['repls'].should.be.equal(len(repls))
        self.configer.right_rep_num['en']['redus'].should.be.equal(len(redus))
        self._check_correctnes(stats.col_index_orig, self.configer._counted_reps['en'], repls=repls, redus=redus, baseline=baseline)
        bas_synts = [ bs[0] for bs in baseline ]
        for r in redus:
            if r[5] not in bas_synts:
                p(r[5], 'ERROR', c='r')
                assert False

        for r in repls:
            if r[5] not in bas_synts:
                p(r[5], 'ERROR', c='r')
                assert False

        stats = Stats(mode=self.mode, use_cash=True)
        stats.init(self.tempdir_project_folder, name, language, visibility, corpus_id=corpus_id, version=version, encryption_key=encryption_key, baseline_delimiter='++')
        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_en))
        stats.compute(corp, stream_number=1, adjust_to_cpu=False, freeze_db=True)
        baseline = stats.statsdb.getall('baseline')
        repls = stats.statsdb.getall('replications')
        redus = stats.statsdb.getall('reduplications')
        self.configer.right_rep_num['en']['repls'].should.be.equal(len(repls))
        self.configer.right_rep_num['en']['redus'].should.be.equal(len(redus))
        self._check_correctnes(stats.col_index_orig, self.configer._counted_reps['en'], repls=repls, redus=redus, baseline=baseline)
        bas_synts = [ bs[0] for bs in baseline ]
        for r in redus:
            if r[5] not in bas_synts:
                p(r[5], 'ERROR', c='r')
                assert False

        for r in repls:
            if r[5] not in bas_synts:
                p(r[5], 'ERROR', c='r')
                assert False

    @attr(status='stable')
    def test_main_compute_function_lower_case_for_4_streams_610_2(self):
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
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['stats']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'stats'
        stats = Stats(mode=self.mode, use_cash=True)
        stats.init(self.tempdir_project_folder, name, language, visibility, corpus_id=corpus_id, version=version, encryption_key=encryption_key, baseline_delimiter='++')
        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_en))
        stats.compute(corp, stream_number=4, adjust_to_cpu=False, freeze_db=False)
        baseline = stats.statsdb.getall('baseline')
        repls = stats.statsdb.getall('replications')
        redus = stats.statsdb.getall('reduplications')
        self.configer.right_rep_num['en']['repls'].should.be.equal(len(repls))
        self.configer.right_rep_num['en']['redus'].should.be.equal(len(redus))
        self._check_correctnes(stats.col_index_orig, self.configer._counted_reps['en'], repls=repls, redus=redus, baseline=baseline)
        bas_synts = [ bs[0] for bs in baseline ]
        for r in redus:
            if r[5] not in bas_synts:
                p(r[5], 'ERROR', c='r')
                assert False

        for r in repls:
            if r[5] not in bas_synts:
                p(r[5], 'ERROR', c='r')
                assert False

        stats = Stats(mode=self.mode, use_cash=True)
        stats.init(self.tempdir_project_folder, name, language, visibility, corpus_id=corpus_id, version=version, encryption_key=encryption_key, baseline_delimiter='++')
        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_en))
        stats.compute(corp, stream_number=4, adjust_to_cpu=False, freeze_db=True)
        baseline = stats.statsdb.getall('baseline')
        repls = stats.statsdb.getall('replications')
        redus = stats.statsdb.getall('reduplications')
        self.configer.right_rep_num['en']['repls'].should.be.equal(len(repls))
        self.configer.right_rep_num['en']['redus'].should.be.equal(len(redus))
        self._check_correctnes(stats.col_index_orig, self.configer._counted_reps['en'], repls=repls, redus=redus, baseline=baseline)
        bas_synts = [ bs[0] for bs in baseline ]
        for r in redus:
            if r[5] not in bas_synts:
                p(r[5], 'ERROR', c='r')
                assert False

        for r in repls:
            if r[5] not in bas_synts:
                p(r[5], 'ERROR', c='r')
                assert False

    @attr(status='stable')
    def test_main_compute_function_lower_case_for_1_stream_with_preprocessing_and_frozen_610_3(self):
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
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['stats']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'stats'
        precomputed_data = copy.deepcopy(self.configer._counted_reps['en'])
        del precomputed_data['1']
        del precomputed_data['#shetlife']
        del precomputed_data['.']
        del precomputed_data['?']
        precomputed_data[':hashtag:'] = {'baseline': 4, 'redu': (2, 4)}
        right_rep_num = {'repls': sum([ data['repl'][1] for word, data in precomputed_data.items() if 'repl' in data ]), 
           'redus': sum([ data['redu'][0] for word, data in precomputed_data.items() if 'redu' in data ])}
        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_en))
        stats = Stats(mode=self.mode, use_cash=True, status_bar=True)
        stats.init(self.tempdir_project_folder, name, language, visibility, corpus_id=corpus_id, version=version, baseline_delimiter='++', encryption_key=encryption_key, ignore_hashtag=True, force_cleaning=True, ignore_url=True, ignore_mention=True, ignore_punkt=True, ignore_num=True)
        stats.compute(corp, stream_number=1, adjust_to_cpu=False, freeze_db=False, baseline_insertion_border=10)
        baseline = stats.statsdb.getall('baseline')
        repls = stats.statsdb.getall('replications')
        redus = stats.statsdb.getall('reduplications')
        self._check_correctnes(stats.col_index_orig, precomputed_data, repls=repls, redus=redus, baseline=baseline)
        right_rep_num['repls'].should.be.equal(len(repls))
        right_rep_num['redus'].should.be.equal(len(redus))
        bas_synts = [ bs[0] for bs in baseline ]
        for r in redus:
            if r[5] not in bas_synts:
                p(r[5], 'ERROR', c='r')
                assert False

        for r in repls:
            if r[5] not in bas_synts:
                p(r[5], 'ERROR', c='r')
                assert False

    @attr(status='stable')
    def test_main_compute_function_lower_case_for_1_stream_with_and_without_optimization_610_4(self):
        self.prj_folder()
        self.test_dbs()
        right_repls = [
         (
          1, 1111, '[4, 14]', '[1, 4]', '[1, 4]', 'very', 'ver^4y^5', 'veri', 'r', 4, 2, '[1, 4]', 'JJ', '["negative", -0.1875]', '.', '["symbol", null, "."]', 'but', '["CC", null, "but"]', 'it', '["PRP", null, "it"]', 'was', '["VBD", null, "was"]', 'also', '["RB", null, "also"]', 'pity', '["JJ", {"pity": 2, "pi^3t^3y^3": 1, "pi^9ty": 1}, "piti"]', 'for', '["IN", null, "for"]', 'me', '["PRP", null, "me"]', '.', '["symbol", null, "."]', ':-(', '["EMOASC", null, ":-("]'), (2, 1111, '[4, 14]', '[1, 4]', '[1, 4]', 'very', 'ver^4y^5', 'veri', 'y', 5, 3, '[1, 4]', 'JJ', '["negative", -0.1875]', '.', '["symbol", null, "."]', 'but', '["CC", null, "but"]', 'it', '["PRP", null, "it"]', 'was', '["VBD", null, "was"]', 'also', '["RB", null, "also"]', 'pity', '["JJ", {"pity": 2, "pi^3t^3y^3": 1, "pi^9ty": 1}, "piti"]', 'for', '["IN", null, "for"]', 'me', '["PRP", null, "me"]', '.', '["symbol", null, "."]', ':-(', '["EMOASC", null, ":-("]'), (3, 1111, '[4, 14]', '[1, 5]', '[1, 4]', 'very', 'v^3er^8y', 'veri', 'v', 3, 0, '[1, 4]', 'JJ', '["negative", -0.1875]', '.', '["symbol", null, "."]', 'but', '["CC", null, "but"]', 'it', '["PRP", null, "it"]', 'was', '["VBD", null, "was"]', 'also', '["RB", null, "also"]', 'pity', '["JJ", {"pity": 2, "pi^3t^3y^3": 1, "pi^9ty": 1}, "piti"]', 'for', '["IN", null, "for"]', 'me', '["PRP", null, "me"]', '.', '["symbol", null, "."]', ':-(', '["EMOASC", null, ":-("]'), (4, 1111, '[4, 14]', '[1, 5]', '[1, 4]', 'very', 'v^3er^8y', 'veri', 'r', 8, 2, '[1, 4]', 'JJ', '["negative", -0.1875]', '.', '["symbol", null, "."]', 'but', '["CC", null, "but"]', 'it', '["PRP", null, "it"]', 'was', '["VBD", null, "was"]', 'also', '["RB", null, "also"]', 'pity', '["JJ", {"pity": 2, "pi^3t^3y^3": 1, "pi^9ty": 1}, "piti"]', 'for', '["IN", null, "for"]', 'me', '["PRP", null, "me"]', '.', '["symbol", null, "."]', ':-(', '["EMOASC", null, ":-("]'), (5, 1111, '[4, 14]', '[1, 7]', '[1, 5]', 'pity', 'pi^9ty', 'piti', 'i', 9, 1, '[1, 5]', 'JJ', '["negative", -0.1875]', 'but', '["CC", null, "but"]', 'it', '["PRP", null, "it"]', 'was', '["VBD", null, "was"]', 'also', '["RB", null, "also"]', 'very', '["JJ", {"very": 1, "ver^4y^5": 1, "v^3er^8y": 1}, "veri"]', 'for', '["IN", null, "for"]', 'me', '["PRP", null, "me"]', '.', '["symbol", null, "."]', ':-(', '["EMOASC", null, ":-("]', '@real_trump', '["mention", null, "@real_trump"]'), (6, 1111, '[4, 14]', '[1, 10]', '[1, 5]', 'pity', 'pi^3t^3y^3', 'piti', 'i', 3, 1, '[1, 5]', 'JJ', '["negative", -0.1875]', 'but', '["CC", null, "but"]', 'it', '["PRP", null, "it"]', 'was', '["VBD", null, "was"]', 'also', '["RB", null, "also"]', 'very', '["JJ", {"very": 1, "ver^4y^5": 1, "v^3er^8y": 1}, "veri"]', 'for', '["IN", null, "for"]', 'me', '["PRP", null, "me"]', '.', '["symbol", null, "."]', ':-(', '["EMOASC", null, ":-("]', '@real_trump', '["mention", null, "@real_trump"]'), (7, 1111, '[4, 14]', '[1, 10]', '[1, 5]', 'pity', 'pi^3t^3y^3', 'piti', 't', 3, 2, '[1, 5]', 'JJ', '["negative", -0.1875]', 'but', '["CC", null, "but"]', 'it', '["PRP", null, "it"]', 'was', '["VBD", null, "was"]', 'also', '["RB", null, "also"]', 'very', '["JJ", {"very": 1, "ver^4y^5": 1, "v^3er^8y": 1}, "veri"]', 'for', '["IN", null, "for"]', 'me', '["PRP", null, "me"]', '.', '["symbol", null, "."]', ':-(', '["EMOASC", null, ":-("]', '@real_trump', '["mention", null, "@real_trump"]'), (8, 1111, '[4, 14]', '[1, 10]', '[1, 5]', 'pity', 'pi^3t^3y^3', 'piti', 'y', 3, 3, '[1, 5]', 'JJ', '["negative", -0.1875]', 'but', '["CC", null, "but"]', 'it', '["PRP", null, "it"]', 'was', '["VBD", null, "was"]', 'also', '["RB", null, "also"]', 'very', '["JJ", {"very": 1, "ver^4y^5": 1, "v^3er^8y": 1}, "veri"]', 'for', '["IN", null, "for"]', 'me', '["PRP", null, "me"]', '.', '["symbol", null, "."]', ':-(', '["EMOASC", null, ":-("]', '@real_trump', '["mention", null, "@real_trump"]'), (9, 1111, '[4, 14]', '[1, 13]', '[1, 8]', '.', '.^6', '.', '.', 6, 0, None, 'symbol', '["negative", -0.1875]', 'also', '["RB", null, "also"]', 'very', '["JJ", {"very": 1, "ver^4y^5": 1, "v^3er^8y": 1}, "veri"]', 'pity', '["JJ", {"pity": 2, "pi^3t^3y^3": 1, "pi^9ty": 1}, "piti"]', 'for', '["IN", null, "for"]', 'me', '["PRP", null, "me"]', ':-(', '["EMOASC", null, ":-("]', '@real_trump', '["mention", null, "@real_trump"]', '#shetlife', '["hashtag", null, "#shetlif"]', '#readytogo', '["hashtag", null, "#readytogo"]', 'http://www.absurd.com', '["URL", null, "http://www.absurd.com"]'), (10, 1111, '[4, 14]', '[1, 14]', '[1, 9]', ':-(', ':-(^5', ':-(', '(', 5, 2, None, 'EMOASC', '["negative", -0.1875]', 'very', '["JJ", {"very": 1, "ver^4y^5": 1, "v^3er^8y": 1}, "veri"]', 'pity', '["JJ", {"pity": 2, "pi^3t^3y^3": 1, "pi^9ty": 1}, "piti"]', 'for', '["IN", null, "for"]', 'me', '["PRP", null, "me"]', '.', '["symbol", null, "."]', '@real_trump', '["mention", null, "@real_trump"]', '#shetlife', '["hashtag", null, "#shetlif"]', '#readytogo', '["hashtag", null, "#readytogo"]', 'http://www.absurd.com', '["URL", null, "http://www.absurd.com"]', None, None), (11, 2222, '[5]', '[0, 0]', '[0, 0]', 'glad', 'gla^7d', 'glad', 'a', 7, 2, None, 'NN', '["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, 'to', '["TO", null, "to"]', 'se', '["VB", null, "se"]', 'you', '["PRP", null, "you"]', '-)', '["EMOASC", null, "-)"]', None, None), (12, 2222, '[5]', '[0, 2]', '[0, 2]', 'se', 'se^9', 'se', 'e', 9, 1, None, 'VB', '["neutral", 0.0]', None, None, None, None, None, None, 'glad', '["NN", null, "glad"]', 'to', '["TO", null, "to"]', 'you', '["PRP", null, "you"]', '-)', '["EMOASC", null, "-)"]', None, None, None, None, None, None), (13, 2222, '[5]', '[0, 4]', '[0, 4]', '-)', '-)^4', '-)', ')', 4, 1, None, 'EMOASC', '["neutral", 0.0]', None, None, 'glad', '["NN", null, "glad"]', 'to', '["TO", null, "to"]', 'se', '["VB", null, "se"]', 'you', '["PRP", null, "you"]', None, None, None, None, None, None, None, None, None, None), (14, 3333, '[15]', '[0, 1]', '[0, 1]', 'bad', 'bad^5', 'bad', 'd', 5, 2, '[0, 1]', 'JJ', '["negative", -0.7249999999999999]', None, None, None, None, None, None, None, None, 'a', '["DT", null, "a"]', 'news', '["NN", null, "news"]', ',', '["symbol", null, ","]', 'which', '["WDT", null, "which"]', 'we', '["PRP", null, "we"]', 'can', '["MD", null, "can"]'), (15, 3333, '[15]', '[0, 3]', '[0, 1]', 'bad', 'b^7a^6d', 'bad', 'b', 7, 0, '[0, 1]', 'JJ', '["negative", -0.7249999999999999]', None, None, None, None, None, None, None, None, 'a', '["DT", null, "a"]', 'news', '["NN", null, "news"]', ',', '["symbol", null, ","]', 'which', '["WDT", null, "which"]', 'we', '["PRP", null, "we"]', 'can', '["MD", null, "can"]'), (16, 3333, '[15]', '[0, 3]', '[0, 1]', 'bad', 'b^7a^6d', 'bad', 'a', 6, 1, '[0, 1]', 'JJ', '["negative", -0.7249999999999999]', None, None, None, None, None, None, None, None, 'a', '["DT", null, "a"]', 'news', '["NN", null, "news"]', ',', '["symbol", null, ","]', 'which', '["WDT", null, "which"]', 'we', '["PRP", null, "we"]', 'can', '["MD", null, "can"]'), (17, 3333, '[15]', '[0, 4]', '[0, 1]', 'bad', 'b^4a^4d^5', 'bad', 'b', 4, 0, '[0, 1]', 'JJ', '["negative", -0.7249999999999999]', None, None, None, None, None, None, None, None, 'a', '["DT", null, "a"]', 'news', '["NN", null, "news"]', ',', '["symbol", null, ","]', 'which', '["WDT", null, "which"]', 'we', '["PRP", null, "we"]', 'can', '["MD", null, "can"]'), (18, 3333, '[15]', '[0, 4]', '[0, 1]', 'bad', 'b^4a^4d^5', 'bad', 'a', 4, 1, '[0, 1]', 'JJ', '["negative", -0.7249999999999999]', None, None, None, None, None, None, None, None, 'a', '["DT", null, "a"]', 'news', '["NN", null, "news"]', ',', '["symbol", null, ","]', 'which', '["WDT", null, "which"]', 'we', '["PRP", null, "we"]', 'can', '["MD", null, "can"]'), (19, 3333, '[15]', '[0, 4]', '[0, 1]', 'bad', 'b^4a^4d^5', 'bad', 'd', 5, 2, '[0, 1]', 'JJ', '["negative", -0.7249999999999999]', None, None, None, None, None, None, None, None, 'a', '["DT", null, "a"]', 'news', '["NN", null, "news"]', ',', '["symbol", null, ","]', 'which', '["WDT", null, "which"]', 'we', '["PRP", null, "we"]', 'can', '["MD", null, "can"]'), (20, 3333, '[15]', '[0, 5]', '[0, 1]', 'bad', 'ba^7d', 'bad', 'a', 7, 1, '[0, 1]', 'JJ', '["negative", -0.7249999999999999]', None, None, None, None, None, None, None, None, 'a', '["DT", null, "a"]', 'news', '["NN", null, "news"]', ',', '["symbol", null, ","]', 'which', '["WDT", null, "which"]', 'we', '["PRP", null, "we"]', 'can', '["MD", null, "can"]'), (21, 3333, '[15]', '[0, 14]', '[0, 10]', '-(', '-(^4', '-(', '(', 4, 1, None, 'EMOASC', '["negative", -0.7249999999999999]', 'we', '["PRP", null, "we"]', 'can', '["MD", null, "can"]', 'not', '["RB", null, "not"]', 'acept', '["VB", null, "acept"]', '.', '["symbol", null, "."]', '😫', '["EMOIMG", null, "\\ud83d\\ude2b"]', ':-(', '["EMOASC", null, ":-("]', '#shetlife', '["hashtag", {"#shetlife": 2}, "#shetlif"]', 'http://www.noooo.com', '["URL", null, "http://www.noooo.com"]', None, None), (22, 3333, '[15]', '[0, 15]', '[0, 11]', '😫', '😫^12', '😫', '😫', 12, 0, None, 'EMOIMG', '["negative", -0.7249999999999999]', 'can', '["MD", null, "can"]', 'not', '["RB", null, "not"]', 'acept', '["VB", null, "acept"]', '.', '["symbol", null, "."]', '-(', '["EMOASC", null, "-("]', ':-(', '["EMOASC", null, ":-("]', '#shetlife', '["hashtag", {"#shetlife": 2}, "#shetlif"]', 'http://www.noooo.com', '["URL", null, "http://www.noooo.com"]', None, None, None, None), (23, 3333, '[15]', '[0, 16]', '[0, 12]', ':-(', ':-(^5', ':-(', '(', 5, 2, None, 'EMOASC', '["negative", -0.7249999999999999]', 'not', '["RB", null, "not"]', 'acept', '["VB", null, "acept"]', '.', '["symbol", null, "."]', '-(', '["EMOASC", null, "-("]', '😫', '["EMOIMG", null, "\\ud83d\\ude2b"]', '#shetlife', '["hashtag", {"#shetlife": 2}, "#shetlif"]', 'http://www.noooo.com', '["URL", null, "http://www.noooo.com"]', None, None, None, None, None, None), (24, 4444, '[13]', '[0, 6]', '[0, 1]', 'model', 'mo^7del^7', 'model', 'o', 7, 1, None, 'NN', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'tiny', '["JJ", {"tiny": 6}, "tini"]', ',', '["symbol", null, ","]', 'which', '["WDT", null, "which"]', 'we', '["PRP", null, "we"]', 'can', '["MD", null, "can"]', 'use', '["VB", null, "use"]'), (25, 4444, '[13]', '[0, 6]', '[0, 1]', 'model', 'mo^7del^7', 'model', 'l', 7, 4, None, 'NN', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'tiny', '["JJ", {"tiny": 6}, "tini"]', ',', '["symbol", null, ","]', 'which', '["WDT", null, "which"]', 'we', '["PRP", null, "we"]', 'can', '["MD", null, "can"]', 'use', '["VB", null, "use"]'), (26, 4444, '[13]', '[0, 15]', '[0, 10]', 'big', 'bi^3g', 'big', 'i', 3, 1, '[0, 10]', 'NN', '["neutral", 0.0]', 'can', '["MD", null, "can"]', 'use', '["VB", null, "use"]', 'for', '["IN", null, "for"]', 'explain', '["VB", null, "explain"]', 'a', '["DT", null, "a"]', 'things', '["NNS", null, "thing"]', '.', '["symbol", null, "."]', None, None, None, None, None, None), (27, 4444, '[13]', '[0, 16]', '[0, 10]', 'big', 'bi^15g', 'big', 'i', 15, 1, '[0, 10]', 'NN', '["neutral", 0.0]', 'can', '["MD", null, "can"]', 'use', '["VB", null, "use"]', 'for', '["IN", null, "for"]', 'explain', '["VB", null, "explain"]', 'a', '["DT", null, "a"]', 'things', '["NNS", null, "thing"]', '.', '["symbol", null, "."]', None, None, None, None, None, None), (28, 5555, '[8, 2, 11, 4]', '[0, 8]', '[0, 6]', 'explanation', 'expla^5nation', 'explan', 'a', 5, 4, None, 'NN', '["neutral", 0.0]', 'model', '["NN", null, "model"]', ',', '["symbol", null, ","]', 'but', '["CC", null, "but"]', 'a', '["DT", null, "a"]', 'big', '["JJ", {"big": 3}, "big"]', '.', '["symbol", null, "."]', 'right', '["UH", null, "right"]', '?', '["symbol", null, "?"]', 'what', '["WP", null, "what"]', 'do', '["VBP", null, "do"]'), (29, 5555, '[8, 2, 11, 4]', '[1, 0]', '[1, 0]', 'right', 'ri^6ght', 'right', 'i', 6, 1, None, 'UH', '["neutral", 0.0]', 'but', '["CC", null, "but"]', 'a', '["DT", null, "a"]', 'big', '["JJ", {"big": 3}, "big"]', 'explanation', '["NN", null, "explan"]', '.', '["symbol", null, "."]', '?', '["symbol", null, "?"]', 'what', '["WP", null, "what"]', 'do', '["VBP", null, "do"]', 'you', '["PRP", null, "you"]', 'think', '["VB", null, "think"]'), (30, 5555, '[8, 2, 11, 4]', '[2, 2]', '[2, 2]', 'you', 'you^6', 'you', 'u', 6, 2, None, 'PRP', '["neutral", 0.0]', '.', '["symbol", null, "."]', 'right', '["UH", null, "right"]', '?', '["symbol", null, "?"]', 'what', '["WP", null, "what"]', 'do', '["VBP", null, "do"]', 'think', '["VB", null, "think"]', 'about', '["IN", null, "about"]', 'it', '["PRP", null, "it"]', '?', '["symbol", null, "?"]', 1, '["number", null, "1"]'), (31, 5555, '[8, 2, 11, 4]', '[2, 6]', '[2, 6]', '?', '?^4', '?', '?', 4, 0, None, 'symbol', '["neutral", 0.0]', 'do', '["VBP", null, "do"]', 'you', '["PRP", null, "you"]', 'think', '["VB", null, "think"]', 'about', '["IN", null, "about"]', 'it', '["PRP", null, "it"]', 1, '["number", null, "1"]', '😫', '["EMOIMG", null, "\\ud83d\\ude2b"]', 1, '["number", null, "1"]', '.', '["symbol", null, "."]', 'but', '["NNP", {"bu^5t^4": 1, "b^5u^4t^4": 1}, "but"]'), (32, 5555, '[8, 2, 11, 4]', '[2, 7]', '[2, 7]', '1', '1^6', '1', '1', 6, 0, None, 'number', '["neutral", 0.0]', 'you', '["PRP", null, "you"]', 'think', '["VB", null, "think"]', 'about', '["IN", null, "about"]', 'it', '["PRP", null, "it"]', '?', '["symbol", null, "?"]', '😫', '["EMOIMG", null, "\\ud83d\\ude2b"]', 1, '["number", null, "1"]', '.', '["symbol", null, "."]', 'but', '["NNP", {"bu^5t^4": 1, "b^5u^4t^4": 1}, "but"]', 'you', '["NN", {"yo^6u": 1, "y^6ou": 1}, "you"]'), (33, 5555, '[8, 2, 11, 4]', '[2, 8]', '[2, 8]', '😫', '😫^4', '😫', '😫', 4, 0, None, 'EMOIMG', '["neutral", 0.0]', 'think', '["VB", null, "think"]', 'about', '["IN", null, "about"]', 'it', '["PRP", null, "it"]', '?', '["symbol", null, "?"]', 1, '["number", null, "1"]', 1, '["number", null, "1"]', '.', '["symbol", null, "."]', 'but', '["NNP", {"bu^5t^4": 1, "b^5u^4t^4": 1}, "but"]', 'you', '["NN", {"yo^6u": 1, "y^6ou": 1}, "you"]', 'but', '["FW", {"b^6ut": 1, "b^5ut^4": 1, "b^5u^5t": 1}, "but"]'), (34, 5555, '[8, 2, 11, 4]', '[2, 9]', '[2, 9]', '1', '1^8', '1', '1', 8, 0, None, 'number', '["neutral", 0.0]', 'about', '["IN", null, "about"]', 'it', '["PRP", null, "it"]', '?', '["symbol", null, "?"]', 1, '["number", null, "1"]', '😫', '["EMOIMG", null, "\\ud83d\\ude2b"]', '.', '["symbol", null, "."]', 'but', '["NNP", {"bu^5t^4": 1, "b^5u^4t^4": 1}, "but"]', 'you', '["NN", {"yo^6u": 1, "y^6ou": 1}, "you"]', 'but', '["FW", {"b^6ut": 1, "b^5ut^4": 1, "b^5u^5t": 1}, "but"]', 'you', '["FW", null, "you"]'), (35, 5555, '[8, 2, 11, 4]', '[3, 0]', '[3, 0]', 'but', 'b^5u^4t^4', 'but', 'b', 5, 0, '[3, 0]', 'NNP', '["neutral", 0.0]', '?', '["symbol", null, "?"]', 1, '["number", null, "1"]', '😫', '["EMOIMG", null, "\\ud83d\\ude2b"]', 1, '["number", null, "1"]', '.', '["symbol", null, "."]', 'you', '["NN", {"yo^6u": 1, "y^6ou": 1}, "you"]', 'but', '["FW", {"b^6ut": 1, "b^5ut^4": 1, "b^5u^5t": 1}, "but"]', 'you', '["FW", null, "you"]', None, None, None, None), (36, 5555, '[8, 2, 11, 4]', '[3, 0]', '[3, 0]', 'but', 'b^5u^4t^4', 'but', 'u', 4, 1, '[3, 0]', 'NNP', '["neutral", 0.0]', '?', '["symbol", null, "?"]', 1, '["number", null, "1"]', '😫', '["EMOIMG", null, "\\ud83d\\ude2b"]', 1, '["number", null, "1"]', '.', '["symbol", null, "."]', 'you', '["NN", {"yo^6u": 1, "y^6ou": 1}, "you"]', 'but', '["FW", {"b^6ut": 1, "b^5ut^4": 1, "b^5u^5t": 1}, "but"]', 'you', '["FW", null, "you"]', None, None, None, None), (37, 5555, '[8, 2, 11, 4]', '[3, 0]', '[3, 0]', 'but', 'b^5u^4t^4', 'but', 't', 4, 2, '[3, 0]', 'NNP', '["neutral", 0.0]', '?', '["symbol", null, "?"]', 1, '["number", null, "1"]', '😫', '["EMOIMG", null, "\\ud83d\\ude2b"]', 1, '["number", null, "1"]', '.', '["symbol", null, "."]', 'you', '["NN", {"yo^6u": 1, "y^6ou": 1}, "you"]', 'but', '["FW", {"b^6ut": 1, "b^5ut^4": 1, "b^5u^5t": 1}, "but"]', 'you', '["FW", null, "you"]', None, None, None, None), (38, 5555, '[8, 2, 11, 4]', '[3, 1]', '[3, 0]', 'but', 'bu^5t^4', 'but', 'u', 5, 1, '[3, 0]', 'NNP', '["neutral", 0.0]', '?', '["symbol", null, "?"]', 1, '["number", null, "1"]', '😫', '["EMOIMG", null, "\\ud83d\\ude2b"]', 1, '["number", null, "1"]', '.', '["symbol", null, "."]', 'you', '["NN", {"yo^6u": 1, "y^6ou": 1}, "you"]', 'but', '["FW", {"b^6ut": 1, "b^5ut^4": 1, "b^5u^5t": 1}, "but"]', 'you', '["FW", null, "you"]', None, None, None, None), (39, 5555, '[8, 2, 11, 4]', '[3, 1]', '[3, 0]', 'but', 'bu^5t^4', 'but', 't', 4, 2, '[3, 0]', 'NNP', '["neutral", 0.0]', '?', '["symbol", null, "?"]', 1, '["number", null, "1"]', '😫', '["EMOIMG", null, "\\ud83d\\ude2b"]', 1, '["number", null, "1"]', '.', '["symbol", null, "."]', 'you', '["NN", {"yo^6u": 1, "y^6ou": 1}, "you"]', 'but', '["FW", {"b^6ut": 1, "b^5ut^4": 1, "b^5u^5t": 1}, "but"]', 'you', '["FW", null, "you"]', None, None, None, None), (40, 5555, '[8, 2, 11, 4]', '[3, 2]', '[3, 1]', 'you', 'y^6ou', 'you', 'y', 6, 0, '[3, 1]', 'NN', '["neutral", 0.0]', 1, '["number", null, "1"]', '😫', '["EMOIMG", null, "\\ud83d\\ude2b"]', 1, '["number", null, "1"]', '.', '["symbol", null, "."]', 'but', '["NNP", {"bu^5t^4": 1, "b^5u^4t^4": 1}, "but"]', 'but', '["FW", {"b^6ut": 1, "b^5ut^4": 1, "b^5u^5t": 1}, "but"]', 'you', '["FW", null, "you"]', None, None, None, None, None, None), (41, 5555, '[8, 2, 11, 4]', '[3, 3]', '[3, 1]', 'you', 'yo^6u', 'you', 'o', 6, 1, '[3, 1]', 'NN', '["neutral", 0.0]', 1, '["number", null, "1"]', '😫', '["EMOIMG", null, "\\ud83d\\ude2b"]', 1, '["number", null, "1"]', '.', '["symbol", null, "."]', 'but', '["NNP", {"bu^5t^4": 1, "b^5u^4t^4": 1}, "but"]', 'but', '["FW", {"b^6ut": 1, "b^5ut^4": 1, "b^5u^5t": 1}, "but"]', 'you', '["FW", null, "you"]', None, None, None, None, None, None), (42, 5555, '[8, 2, 11, 4]', '[3, 4]', '[3, 2]', 'but', 'b^6ut', 'but', 'b', 6, 0, '[3, 2]', 'FW', '["neutral", 0.0]', '😫', '["EMOIMG", null, "\\ud83d\\ude2b"]', 1, '["number", null, "1"]', '.', '["symbol", null, "."]', 'but', '["NNP", {"bu^5t^4": 1, "b^5u^4t^4": 1}, "but"]', 'you', '["NN", {"yo^6u": 1, "y^6ou": 1}, "you"]', 'you', '["FW", null, "you"]', None, None, None, None, None, None, None, None), (43, 5555, '[8, 2, 11, 4]', '[3, 5]', '[3, 2]', 'but', 'b^5ut^4', 'but', 'b', 5, 0, '[3, 2]', 'FW', '["neutral", 0.0]', '😫', '["EMOIMG", null, "\\ud83d\\ude2b"]', 1, '["number", null, "1"]', '.', '["symbol", null, "."]', 'but', '["NNP", {"bu^5t^4": 1, "b^5u^4t^4": 1}, "but"]', 'you', '["NN", {"yo^6u": 1, "y^6ou": 1}, "you"]', 'you', '["FW", null, "you"]', None, None, None, None, None, None, None, None), (44, 5555, '[8, 2, 11, 4]', '[3, 5]', '[3, 2]', 'but', 'b^5ut^4', 'but', 't', 4, 2, '[3, 2]', 'FW', '["neutral", 0.0]', '😫', '["EMOIMG", null, "\\ud83d\\ude2b"]', 1, '["number", null, "1"]', '.', '["symbol", null, "."]', 'but', '["NNP", {"bu^5t^4": 1, "b^5u^4t^4": 1}, "but"]', 'you', '["NN", {"yo^6u": 1, "y^6ou": 1}, "you"]', 'you', '["FW", null, "you"]', None, None, None, None, None, None, None, None), (45, 5555, '[8, 2, 11, 4]', '[3, 6]', '[3, 2]', 'but', 'b^5u^5t', 'but', 'b', 5, 0, '[3, 2]', 'FW', '["neutral", 0.0]', '😫', '["EMOIMG", null, "\\ud83d\\ude2b"]', 1, '["number", null, "1"]', '.', '["symbol", null, "."]', 'but', '["NNP", {"bu^5t^4": 1, "b^5u^4t^4": 1}, "but"]', 'you', '["NN", {"yo^6u": 1, "y^6ou": 1}, "you"]', 'you', '["FW", null, "you"]', None, None, None, None, None, None, None, None), (46, 5555, '[8, 2, 11, 4]', '[3, 6]', '[3, 2]', 'but', 'b^5u^5t', 'but', 'u', 5, 1, '[3, 2]', 'FW', '["neutral", 0.0]', '😫', '["EMOIMG", null, "\\ud83d\\ude2b"]', 1, '["number", null, "1"]', '.', '["symbol", null, "."]', 'but', '["NNP", {"bu^5t^4": 1, "b^5u^4t^4": 1}, "but"]', 'you', '["NN", {"yo^6u": 1, "y^6ou": 1}, "you"]', 'you', '["FW", null, "you"]', None, None, None, None, None, None, None, None), (47, 5555, '[8, 2, 11, 4]', '[3, 7]', '[3, 3]', 'you', 'y^3o^2u^4', 'you', 'y', 3, 0, None, 'FW', '["neutral", 0.0]', 1, '["number", null, "1"]', '.', '["symbol", null, "."]', 'but', '["NNP", {"bu^5t^4": 1, "b^5u^4t^4": 1}, "but"]', 'you', '["NN", {"yo^6u": 1, "y^6ou": 1}, "you"]', 'but', '["FW", {"b^6ut": 1, "b^5ut^4": 1, "b^5u^5t": 1}, "but"]', None, None, None, None, None, None, None, None, None, None), (48, 5555, '[8, 2, 11, 4]', '[3, 7]', '[3, 3]', 'you', 'y^3o^2u^4', 'you', 'u', 4, 2, None, 'FW', '["neutral", 0.0]', 1, '["number", null, "1"]', '.', '["symbol", null, "."]', 'but', '["NNP", {"bu^5t^4": 1, "b^5u^4t^4": 1}, "but"]', 'you', '["NN", {"yo^6u": 1, "y^6ou": 1}, "you"]', 'but', '["FW", {"b^6ut": 1, "b^5ut^4": 1, "b^5u^5t": 1}, "but"]', None, None, None, None, None, None, None, None, None, None), (49, 6666, '[3, 9]', '[0, 0]', '[0, 0]', 'tiny', 'tin^3y^2', 'tini', 'n', 3, 2, '[0, 0]', 'JJ', '["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, 'surprise', '["NN", null, "surpris"]', '.', '["symbol", null, "."]', 'but', '["NNP", {"bu^5t": 1, "b^5ut": 1}, "but"]', 'you', '["JJ", {"yo^6u": 1, "y^6ou": 1}, "you"]', 'but', '["CC", {"b^6ut": 1, "b^5ut": 2}, "but"]'), (50, 6666, '[3, 9]', '[1, 0]', '[1, 0]', 'but', 'b^5ut', 'but', 'b', 5, 0, '[1, 0]', 'NNP', '["neutral", 0.0]', None, None, None, None, 'tiny', '["JJ", {"tin^3y^2": 1, "tiny": 2}, "tini"]', 'surprise', '["NN", null, "surpris"]', '.', '["symbol", null, "."]', 'you', '["JJ", {"yo^6u": 1, "y^6ou": 1}, "you"]', 'but', '["CC", {"b^6ut": 1, "b^5ut": 2}, "but"]', 'you', '["VBD", null, "you"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]', '🌈', '["EMOIMG", null, "\\ud83c\\udf08"]'), (51, 6666, '[3, 9]', '[1, 1]', '[1, 0]', 'but', 'bu^5t', 'but', 'u', 5, 1, '[1, 0]', 'NNP', '["neutral", 0.0]', None, None, None, None, 'tiny', '["JJ", {"tin^3y^2": 1, "tiny": 2}, "tini"]', 'surprise', '["NN", null, "surpris"]', '.', '["symbol", null, "."]', 'you', '["JJ", {"yo^6u": 1, "y^6ou": 1}, "you"]', 'but', '["CC", {"b^6ut": 1, "b^5ut": 2}, "but"]', 'you', '["VBD", null, "you"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]', '🌈', '["EMOIMG", null, "\\ud83c\\udf08"]'), (52, 6666, '[3, 9]', '[1, 2]', '[1, 1]', 'you', 'y^6ou', 'you', 'y', 6, 0, '[1, 1]', 'JJ', '["neutral", 0.0]', None, None, 'tiny', '["JJ", {"tin^3y^2": 1, "tiny": 2}, "tini"]', 'surprise', '["NN", null, "surpris"]', '.', '["symbol", null, "."]', 'but', '["NNP", {"bu^5t": 1, "b^5ut": 1}, "but"]', 'but', '["CC", {"b^6ut": 1, "b^5ut": 2}, "but"]', 'you', '["VBD", null, "you"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]', '🌈', '["EMOIMG", null, "\\ud83c\\udf08"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]'), (53, 6666, '[3, 9]', '[1, 3]', '[1, 1]', 'you', 'yo^6u', 'you', 'o', 6, 1, '[1, 1]', 'JJ', '["neutral", 0.0]', None, None, 'tiny', '["JJ", {"tin^3y^2": 1, "tiny": 2}, "tini"]', 'surprise', '["NN", null, "surpris"]', '.', '["symbol", null, "."]', 'but', '["NNP", {"bu^5t": 1, "b^5ut": 1}, "but"]', 'but', '["CC", {"b^6ut": 1, "b^5ut": 2}, "but"]', 'you', '["VBD", null, "you"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]', '🌈', '["EMOIMG", null, "\\ud83c\\udf08"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]'), (54, 6666, '[3, 9]', '[1, 4]', '[1, 2]', 'but', 'b^6ut', 'but', 'b', 6, 0, '[1, 2]', 'CC', '["neutral", 0.0]', 'tiny', '["JJ", {"tin^3y^2": 1, "tiny": 2}, "tini"]', 'surprise', '["NN", null, "surpris"]', '.', '["symbol", null, "."]', 'but', '["NNP", {"bu^5t": 1, "b^5ut": 1}, "but"]', 'you', '["JJ", {"yo^6u": 1, "y^6ou": 1}, "you"]', 'you', '["VBD", null, "you"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]', '🌈', '["EMOIMG", null, "\\ud83c\\udf08"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]', '🌈', '["EMOIMG", null, "\\ud83c\\udf08"]'), (55, 6666, '[3, 9]', '[1, 5]', '[1, 2]', 'but', 'b^5ut', 'but', 'b', 5, 0, '[1, 2]', 'CC', '["neutral", 0.0]', 'tiny', '["JJ", {"tin^3y^2": 1, "tiny": 2}, "tini"]', 'surprise', '["NN", null, "surpris"]', '.', '["symbol", null, "."]', 'but', '["NNP", {"bu^5t": 1, "b^5ut": 1}, "but"]', 'you', '["JJ", {"yo^6u": 1, "y^6ou": 1}, "you"]', 'you', '["VBD", null, "you"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]', '🌈', '["EMOIMG", null, "\\ud83c\\udf08"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]', '🌈', '["EMOIMG", null, "\\ud83c\\udf08"]'), (56, 6666, '[3, 9]', '[1, 6]', '[1, 2]', 'but', 'b^5ut', 'but', 'b', 5, 0, '[1, 2]', 'CC', '["neutral", 0.0]', 'tiny', '["JJ", {"tin^3y^2": 1, "tiny": 2}, "tini"]', 'surprise', '["NN", null, "surpris"]', '.', '["symbol", null, "."]', 'but', '["NNP", {"bu^5t": 1, "b^5ut": 1}, "but"]', 'you', '["JJ", {"yo^6u": 1, "y^6ou": 1}, "you"]', 'you', '["VBD", null, "you"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]', '🌈', '["EMOIMG", null, "\\ud83c\\udf08"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]', '🌈', '["EMOIMG", null, "\\ud83c\\udf08"]'), (57, 6666, '[3, 9]', '[1, 7]', '[1, 3]', 'you', 'y^3o^2u^4', 'you', 'y', 3, 0, None, 'VBD', '["neutral", 0.0]', 'surprise', '["NN", null, "surpris"]', '.', '["symbol", null, "."]', 'but', '["NNP", {"bu^5t": 1, "b^5ut": 1}, "but"]', 'you', '["JJ", {"yo^6u": 1, "y^6ou": 1}, "you"]', 'but', '["CC", {"b^6ut": 1, "b^5ut": 2}, "but"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]', '🌈', '["EMOIMG", null, "\\ud83c\\udf08"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]', '🌈', '["EMOIMG", null, "\\ud83c\\udf08"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]'), (58, 6666, '[3, 9]', '[1, 7]', '[1, 3]', 'you', 'y^3o^2u^4', 'you', 'u', 4, 2, None, 'VBD', '["neutral", 0.0]', 'surprise', '["NN", null, "surpris"]', '.', '["symbol", null, "."]', 'but', '["NNP", {"bu^5t": 1, "b^5ut": 1}, "but"]', 'you', '["JJ", {"yo^6u": 1, "y^6ou": 1}, "you"]', 'but', '["CC", {"b^6ut": 1, "b^5ut": 2}, "but"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]', '🌈', '["EMOIMG", null, "\\ud83c\\udf08"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]', '🌈', '["EMOIMG", null, "\\ud83c\\udf08"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]'), (59, 6666, '[3, 9]', '[1, 8]', '[1, 4]', '😀', '😀^5', '😀', '😀', 5, 0, None, 'EMOIMG', '["neutral", 0.0]', '.', '["symbol", null, "."]', 'but', '["NNP", {"bu^5t": 1, "b^5ut": 1}, "but"]', 'you', '["JJ", {"yo^6u": 1, "y^6ou": 1}, "you"]', 'but', '["CC", {"b^6ut": 1, "b^5ut": 2}, "but"]', 'you', '["VBD", null, "you"]', '🌈', '["EMOIMG", null, "\\ud83c\\udf08"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]', '🌈', '["EMOIMG", null, "\\ud83c\\udf08"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]', None, None), (60, 6666, '[3, 9]', '[1, 9]', '[1, 5]', '🌈', '🌈^7', '🌈', '🌈', 7, 0, None, 'EMOIMG', '["neutral", 0.0]', 'but', '["NNP", {"bu^5t": 1, "b^5ut": 1}, "but"]', 'you', '["JJ", {"yo^6u": 1, "y^6ou": 1}, "you"]', 'but', '["CC", {"b^6ut": 1, "b^5ut": 2}, "but"]', 'you', '["VBD", null, "you"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]', '🌈', '["EMOIMG", null, "\\ud83c\\udf08"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]', None, None, None, None), (61, 6666, '[3, 9]', '[1, 10]', '[1, 6]', '😀', '😀^5', '😀', '😀', 5, 0, None, 'EMOIMG', '["neutral", 0.0]', 'you', '["JJ", {"yo^6u": 1, "y^6ou": 1}, "you"]', 'but', '["CC", {"b^6ut": 1, "b^5ut": 2}, "but"]', 'you', '["VBD", null, "you"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]', '🌈', '["EMOIMG", null, "\\ud83c\\udf08"]', '🌈', '["EMOIMG", null, "\\ud83c\\udf08"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]', None, None, None, None, None, None), (62, 6666, '[3, 9]', '[1, 11]', '[1, 7]', '🌈', '🌈^7', '🌈', '🌈', 7, 0, None, 'EMOIMG', '["neutral", 0.0]', 'but', '["CC", {"b^6ut": 1, "b^5ut": 2}, "but"]', 'you', '["VBD", null, "you"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]', '🌈', '["EMOIMG", null, "\\ud83c\\udf08"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]', None, None, None, None, None, None, None, None), (63, 6666, '[3, 9]', '[1, 12]', '[1, 8]', '😀', '😀^5', '😀', '😀', 5, 0, None, 'EMOIMG', '["neutral", 0.0]', 'you', '["VBD", null, "you"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]', '🌈', '["EMOIMG", null, "\\ud83c\\udf08"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]', '🌈', '["EMOIMG", null, "\\ud83c\\udf08"]', None, None, None, None, None, None, None, None, None, None), (64, 7777, '[19]', '[0, 7]', '[0, 7]', '😫', '😫^4', '😫', '😫', 4, 0, None, 'EMOIMG', '["positive", 0.27]', 'realy', '["RB", null, "reali"]', 'bad', '["JJ", null, "bad"]', 'surprise', '["NN", null, "surpris"]', 'for', '["IN", null, "for"]', 'me', '["PRP", null, "me"]', ',', '["symbol", null, ","]', 'but', '["MD", null, "but"]', 'i', '["PRP", null, "i"]', 'realy', '["RB", {"realy": 1, "real^3y": 1, "re^5al^4y^3": 1}, "reali"]', 'liked', '["VBD", null, "like"]'), (65, 7777, '[19]', '[0, 9]', '[0, 9]', 'but', 'bu^10t', 'but', 'u', 10, 1, None, 'MD', '["positive", 0.27]', 'surprise', '["NN", null, "surpris"]', 'for', '["IN", null, "for"]', 'me', '["PRP", null, "me"]', '😫', '["EMOIMG", null, "\\ud83d\\ude2b"]', ',', '["symbol", null, ","]', 'i', '["PRP", null, "i"]', 'realy', '["RB", {"realy": 1, "real^3y": 1, "re^5al^4y^3": 1}, "reali"]', 'liked', '["VBD", null, "like"]', 'it', '["PRP", null, "it"]', ':p', '["EMOASC", null, ":p"]'), (66, 7777, '[19]', '[0, 12]', '[0, 11]', 'realy', 'real^3y', 'reali', 'l', 3, 3, '[0, 11]', 'RB', '["positive", 0.27]', 'me', '["PRP", null, "me"]', '😫', '["EMOIMG", null, "\\ud83d\\ude2b"]', ',', '["symbol", null, ","]', 'but', '["MD", null, "but"]', 'i', '["PRP", null, "i"]', 'liked', '["VBD", null, "like"]', 'it', '["PRP", null, "it"]', ':p', '["EMOASC", null, ":p"]', '=)', '["EMOASC", null, "=)"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]'), (67, 7777, '[19]', '[0, 13]', '[0, 11]', 'realy', 're^5al^4y^3', 'reali', 'e', 5, 1, '[0, 11]', 'RB', '["positive", 0.27]', 'me', '["PRP", null, "me"]', '😫', '["EMOIMG", null, "\\ud83d\\ude2b"]', ',', '["symbol", null, ","]', 'but', '["MD", null, "but"]', 'i', '["PRP", null, "i"]', 'liked', '["VBD", null, "like"]', 'it', '["PRP", null, "it"]', ':p', '["EMOASC", null, ":p"]', '=)', '["EMOASC", null, "=)"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]'), (68, 7777, '[19]', '[0, 13]', '[0, 11]', 'realy', 're^5al^4y^3', 'reali', 'l', 4, 3, '[0, 11]', 'RB', '["positive", 0.27]', 'me', '["PRP", null, "me"]', '😫', '["EMOIMG", null, "\\ud83d\\ude2b"]', ',', '["symbol", null, ","]', 'but', '["MD", null, "but"]', 'i', '["PRP", null, "i"]', 'liked', '["VBD", null, "like"]', 'it', '["PRP", null, "it"]', ':p', '["EMOASC", null, ":p"]', '=)', '["EMOASC", null, "=)"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]'), (69, 7777, '[19]', '[0, 13]', '[0, 11]', 'realy', 're^5al^4y^3', 'reali', 'y', 3, 4, '[0, 11]', 'RB', '["positive", 0.27]', 'me', '["PRP", null, "me"]', '😫', '["EMOIMG", null, "\\ud83d\\ude2b"]', ',', '["symbol", null, ","]', 'but', '["MD", null, "but"]', 'i', '["PRP", null, "i"]', 'liked', '["VBD", null, "like"]', 'it', '["PRP", null, "it"]', ':p', '["EMOASC", null, ":p"]', '=)', '["EMOASC", null, "=)"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]'), (70, 7777, '[19]', '[0, 17]', '[0, 15]', '=)', '=)^10', '=)', ')', 10, 1, None, 'EMOASC', '["positive", 0.27]', 'i', '["PRP", null, "i"]', 'realy', '["RB", {"realy": 1, "real^3y": 1, "re^5al^4y^3": 1}, "reali"]', 'liked', '["VBD", null, "like"]', 'it', '["PRP", null, "it"]', ':p', '["EMOASC", null, ":p"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]', '🌈', '["EMOIMG", null, "\\ud83c\\udf08"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]', None, None, None, None), (71, 7777, '[19]', '[0, 18]', '[0, 16]', '😀', '😀^5', '😀', '😀', 5, 0, None, 'EMOIMG', '["positive", 0.27]', 'realy', '["RB", {"realy": 1, "real^3y": 1, "re^5al^4y^3": 1}, "reali"]', 'liked', '["VBD", null, "like"]', 'it', '["PRP", null, "it"]', ':p', '["EMOASC", null, ":p"]', '=)', '["EMOASC", null, "=)"]', '🌈', '["EMOIMG", null, "\\ud83c\\udf08"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]', None, None, None, None, None, None), (72, 7777, '[19]', '[0, 19]', '[0, 17]', '🌈', '🌈^7', '🌈', '🌈', 7, 0, None, 'EMOIMG', '["positive", 0.27]', 'liked', '["VBD", null, "like"]', 'it', '["PRP", null, "it"]', ':p', '["EMOASC", null, ":p"]', '=)', '["EMOASC", null, "=)"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]', None, None, None, None, None, None, None, None)]
        right_redus = [
         (
          1, 1111, '[4, 14]', '[1, 4]', '[1, 4]', 'very', 'veri', '{"very": 1, "ver^4y^5": 1, "v^3er^8y": 1}', 3, 'JJ', '["negative", -0.1875]', '.', '["symbol", null, "."]', 'but', '["CC", null, "but"]', 'it', '["PRP", null, "it"]', 'was', '["VBD", null, "was"]', 'also', '["RB", null, "also"]', 'pity', '["JJ", {"pity": 2, "pi^3t^3y^3": 1, "pi^9ty": 1}, "piti"]', 'for', '["IN", null, "for"]', 'me', '["PRP", null, "me"]', '.', '["symbol", null, "."]', ':-(', '["EMOASC", null, ":-("]'), (2, 1111, '[4, 14]', '[1, 7]', '[1, 5]', 'pity', 'piti', '{"pity": 2, "pi^3t^3y^3": 1, "pi^9ty": 1}', 4, 'JJ', '["negative", -0.1875]', 'but', '["CC", null, "but"]', 'it', '["PRP", null, "it"]', 'was', '["VBD", null, "was"]', 'also', '["RB", null, "also"]', 'very', '["JJ", {"very": 1, "ver^4y^5": 1, "v^3er^8y": 1}, "veri"]', 'for', '["IN", null, "for"]', 'me', '["PRP", null, "me"]', '.', '["symbol", null, "."]', ':-(', '["EMOASC", null, ":-("]', '@real_trump', '["mention", null, "@real_trump"]'), (3, 3333, '[15]', '[0, 1]', '[0, 1]', 'bad', 'bad', '{"bad": 1, "ba^7d": 1, "bad^5": 1, "b^4a^4d^5": 1, "b^7a^6d": 1}', 5, 'JJ', '["negative", -0.7249999999999999]', None, None, None, None, None, None, None, None, 'a', '["DT", null, "a"]', 'news', '["NN", null, "news"]', ',', '["symbol", null, ","]', 'which', '["WDT", null, "which"]', 'we', '["PRP", null, "we"]', 'can', '["MD", null, "can"]'), (4, 3333, '[15]', '[0, 17]', '[0, 13]', '#shetlife', '#shetlif', '{"#shetlife": 2}', 2, 'hashtag', '["negative", -0.7249999999999999]', 'acept', '["VB", null, "acept"]', '.', '["symbol", null, "."]', '-(', '["EMOASC", null, "-("]', '😫', '["EMOIMG", null, "\\ud83d\\ude2b"]', ':-(', '["EMOASC", null, ":-("]', 'http://www.noooo.com', '["URL", null, "http://www.noooo.com"]', None, None, None, None, None, None, None, None), (5, 4444, '[13]', '[0, 0]', '[0, 0]', 'tiny', 'tini', '{"tiny": 6}', 6, 'JJ', '["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, 'model', '["NN", null, "model"]', ',', '["symbol", null, ","]', 'which', '["WDT", null, "which"]', 'we', '["PRP", null, "we"]', 'can', '["MD", null, "can"]'), (6, 4444, '[13]', '[0, 15]', '[0, 10]', 'big', 'big', '{"bi^3g": 1, "bi^15g": 1}', 2, 'NN', '["neutral", 0.0]', 'can', '["MD", null, "can"]', 'use', '["VB", null, "use"]', 'for', '["IN", null, "for"]', 'explain', '["VB", null, "explain"]', 'a', '["DT", null, "a"]', 'things', '["NNS", null, "thing"]', '.', '["symbol", null, "."]', None, None, None, None, None, None), (7, 5555, '[8, 2, 11, 4]', '[0, 5]', '[0, 5]', 'big', 'big', '{"big": 3}', 3, 'JJ', '["neutral", 0.0]', 'tiny', '["JJ", null, "tini"]', 'model', '["NN", null, "model"]', ',', '["symbol", null, ","]', 'but', '["CC", null, "but"]', 'a', '["DT", null, "a"]', 'explanation', '["NN", null, "explan"]', '.', '["symbol", null, "."]', 'right', '["UH", null, "right"]', '?', '["symbol", null, "?"]', 'what', '["WP", null, "what"]'), (8, 5555, '[8, 2, 11, 4]', '[3, 0]', '[3, 0]', 'but', 'but', '{"bu^5t^4": 1, "b^5u^4t^4": 1}', 2, 'NNP', '["neutral", 0.0]', '?', '["symbol", null, "?"]', 1, '["number", null, "1"]', '😫', '["EMOIMG", null, "\\ud83d\\ude2b"]', 1, '["number", null, "1"]', '.', '["symbol", null, "."]', 'you', '["NN", {"yo^6u": 1, "y^6ou": 1}, "you"]', 'but', '["FW", {"b^6ut": 1, "b^5ut^4": 1, "b^5u^5t": 1}, "but"]', 'you', '["FW", null, "you"]', None, None, None, None), (9, 5555, '[8, 2, 11, 4]', '[3, 2]', '[3, 1]', 'you', 'you', '{"yo^6u": 1, "y^6ou": 1}', 2, 'NN', '["neutral", 0.0]', 1, '["number", null, "1"]', '😫', '["EMOIMG", null, "\\ud83d\\ude2b"]', 1, '["number", null, "1"]', '.', '["symbol", null, "."]', 'but', '["NNP", {"bu^5t^4": 1, "b^5u^4t^4": 1}, "but"]', 'but', '["FW", {"b^6ut": 1, "b^5ut^4": 1, "b^5u^5t": 1}, "but"]', 'you', '["FW", null, "you"]', None, None, None, None, None, None), (10, 5555, '[8, 2, 11, 4]', '[3, 4]', '[3, 2]', 'but', 'but', '{"b^6ut": 1, "b^5ut^4": 1, "b^5u^5t": 1}', 3, 'FW', '["neutral", 0.0]', '😫', '["EMOIMG", null, "\\ud83d\\ude2b"]', 1, '["number", null, "1"]', '.', '["symbol", null, "."]', 'but', '["NNP", {"bu^5t^4": 1, "b^5u^4t^4": 1}, "but"]', 'you', '["NN", {"yo^6u": 1, "y^6ou": 1}, "you"]', 'you', '["FW", null, "you"]', None, None, None, None, None, None, None, None), (11, 6666, '[3, 9]', '[0, 0]', '[0, 0]', 'tiny', 'tini', '{"tin^3y^2": 1, "tiny": 2}', 3, 'JJ', '["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, 'surprise', '["NN", null, "surpris"]', '.', '["symbol", null, "."]', 'but', '["NNP", {"bu^5t": 1, "b^5ut": 1}, "but"]', 'you', '["JJ", {"yo^6u": 1, "y^6ou": 1}, "you"]', 'but', '["CC", {"b^6ut": 1, "b^5ut": 2}, "but"]'), (12, 6666, '[3, 9]', '[1, 0]', '[1, 0]', 'but', 'but', '{"bu^5t": 1, "b^5ut": 1}', 2, 'NNP', '["neutral", 0.0]', None, None, None, None, 'tiny', '["JJ", {"tin^3y^2": 1, "tiny": 2}, "tini"]', 'surprise', '["NN", null, "surpris"]', '.', '["symbol", null, "."]', 'you', '["JJ", {"yo^6u": 1, "y^6ou": 1}, "you"]', 'but', '["CC", {"b^6ut": 1, "b^5ut": 2}, "but"]', 'you', '["VBD", null, "you"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]', '🌈', '["EMOIMG", null, "\\ud83c\\udf08"]'), (13, 6666, '[3, 9]', '[1, 2]', '[1, 1]', 'you', 'you', '{"yo^6u": 1, "y^6ou": 1}', 2, 'JJ', '["neutral", 0.0]', None, None, 'tiny', '["JJ", {"tin^3y^2": 1, "tiny": 2}, "tini"]', 'surprise', '["NN", null, "surpris"]', '.', '["symbol", null, "."]', 'but', '["NNP", {"bu^5t": 1, "b^5ut": 1}, "but"]', 'but', '["CC", {"b^6ut": 1, "b^5ut": 2}, "but"]', 'you', '["VBD", null, "you"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]', '🌈', '["EMOIMG", null, "\\ud83c\\udf08"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]'), (14, 6666, '[3, 9]', '[1, 4]', '[1, 2]', 'but', 'but', '{"b^6ut": 1, "b^5ut": 2}', 3, 'CC', '["neutral", 0.0]', 'tiny', '["JJ", {"tin^3y^2": 1, "tiny": 2}, "tini"]', 'surprise', '["NN", null, "surpris"]', '.', '["symbol", null, "."]', 'but', '["NNP", {"bu^5t": 1, "b^5ut": 1}, "but"]', 'you', '["JJ", {"yo^6u": 1, "y^6ou": 1}, "you"]', 'you', '["VBD", null, "you"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]', '🌈', '["EMOIMG", null, "\\ud83c\\udf08"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]', '🌈', '["EMOIMG", null, "\\ud83c\\udf08"]'), (15, 7777, '[19]', '[0, 11]', '[0, 11]', 'realy', 'reali', '{"realy": 1, "real^3y": 1, "re^5al^4y^3": 1}', 3, 'RB', '["positive", 0.27]', 'me', '["PRP", null, "me"]', '😫', '["EMOIMG", null, "\\ud83d\\ude2b"]', ',', '["symbol", null, ","]', 'but', '["MD", null, "but"]', 'i', '["PRP", null, "i"]', 'liked', '["VBD", null, "like"]', 'it', '["PRP", null, "it"]', ':p', '["EMOASC", null, ":p"]', '=)', '["EMOASC", null, "=)"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]')]
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['stats']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'stats'
        precomputed_data = self.configer._counted_reps['en']
        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_en))
        import sys
        stats = Stats(mode=self.mode, use_cash=True, status_bar=True)
        stats.init(self.tempdir_project_folder, name, language, visibility, corpus_id=corpus_id, version=version, baseline_delimiter='++', encryption_key=encryption_key, full_repetativ_syntagma=False, ignore_hashtag=False, force_cleaning=False, ignore_url=False, ignore_mention=False, ignore_punkt=False, ignore_num=False)
        stats.compute(corp, stream_number=1, adjust_to_cpu=False, freeze_db=False, baseline_insertion_border=10)
        baseline = stats.statsdb.getall('baseline')
        repls = stats.statsdb.getall('replications')
        redus = stats.statsdb.getall('reduplications')
        repls.should.be.equal(right_repls)
        redus.should.be.equal(right_redus)
        self.configer.right_rep_num['en']['repls'].should.be.equal(len(repls))
        self.configer.right_rep_num['en']['redus'].should.be.equal(len(redus))
        self._check_correctnes(stats.col_index_orig, precomputed_data, repls=repls, redus=redus, baseline=baseline)
        bas_synts = [ bs[0] for bs in baseline ]
        for r in redus:
            if r[5] not in bas_synts:
                p(r[5], 'ERROR', c='r')
                assert False

        for r in repls:
            if r[5] not in bas_synts:
                p(r[5], 'ERROR', c='r')
                assert False

        stats = Stats(mode=self.mode, use_cash=True, status_bar=True)
        stats.init(self.tempdir_project_folder, name, language, visibility, corpus_id=corpus_id, version=version, baseline_delimiter='++', encryption_key=encryption_key, ignore_hashtag=False, force_cleaning=False, ignore_url=False, ignore_mention=False, ignore_punkt=False, ignore_num=False)
        stats.compute(corp, stream_number=1, adjust_to_cpu=False, freeze_db=False, baseline_insertion_border=100000000)
        baseline = stats.statsdb.getall('baseline')
        repls = stats.statsdb.getall('replications')
        redus = stats.statsdb.getall('reduplications')
        repls.should.be.equal(right_repls)
        redus.should.be.equal(right_redus)
        self.configer.right_rep_num['en']['repls'].should.be.equal(len(repls))
        self.configer.right_rep_num['en']['redus'].should.be.equal(len(redus))
        self._check_correctnes(stats.col_index_orig, precomputed_data, repls=repls, redus=redus, baseline=baseline)
        bas_synts = [ bs[0] for bs in baseline ]
        for r in redus:
            if r[5] not in bas_synts:
                p(r[5], 'ERROR', c='r')
                assert False

        for r in repls:
            if r[5] not in bas_synts:
                p(r[5], 'ERROR', c='r')
                assert False

        stats = Stats(mode=self.mode, use_cash=True, status_bar=True)
        stats.init(self.tempdir_project_folder, name, language, visibility, corpus_id=corpus_id, version=version, baseline_delimiter='++', encryption_key=encryption_key, ignore_hashtag=False, force_cleaning=False, ignore_url=False, ignore_mention=False, ignore_punkt=False, ignore_num=False)
        stats.compute(corp, stream_number=1, adjust_to_cpu=False, freeze_db=True, baseline_insertion_border=10)
        baseline = stats.statsdb.getall('baseline')
        repls = stats.statsdb.getall('replications')
        redus = stats.statsdb.getall('reduplications')
        repls.should.be.equal(right_repls)
        redus.should.be.equal(right_redus)
        self.configer.right_rep_num['en']['repls'].should.be.equal(len(repls))
        self.configer.right_rep_num['en']['redus'].should.be.equal(len(redus))
        self._check_correctnes(stats.col_index_orig, precomputed_data, repls=repls, redus=redus, baseline=baseline)
        bas_synts = [ bs[0] for bs in baseline ]
        for r in redus:
            if r[5] not in bas_synts:
                p(r[5], 'ERROR', c='r')
                assert False

        for r in repls:
            if r[5] not in bas_synts:
                p(r[5], 'ERROR', c='r')
                assert False

        stats = Stats(mode=self.mode, use_cash=True, status_bar=True)
        stats.init(self.tempdir_project_folder, name, language, visibility, corpus_id=corpus_id, version=version, baseline_delimiter='++', encryption_key=encryption_key, full_repetativ_syntagma=True, ignore_hashtag=False, force_cleaning=False, ignore_url=False, ignore_mention=False, ignore_punkt=False, ignore_num=False)
        stats.compute(corp, stream_number=1, adjust_to_cpu=False, freeze_db=False, baseline_insertion_border=10)
        baseline = stats.statsdb.getall('baseline')
        repls = stats.statsdb.getall('replications')
        redus = stats.statsdb.getall('reduplications')
        repls.should.be.equal(right_repls)
        redus.should.be.equal(right_redus)
        self.configer.right_rep_num['en']['repls'].should.be.equal(len(repls))
        self.configer.right_rep_num['en']['redus'].should.be.equal(len(redus))
        self._check_correctnes(stats.col_index_orig, precomputed_data, repls=repls, redus=redus, baseline=baseline)
        bas_synts = [ bs[0] for bs in baseline ]
        for r in redus:
            if r[5] not in bas_synts:
                p(r[5], 'ERROR', c='r')
                assert False

        for r in repls:
            if r[5] not in bas_synts:
                p(r[5], 'ERROR', c='r')
                assert False

        stats = Stats(mode=self.mode, use_cash=True, status_bar=True)
        stats.init(self.tempdir_project_folder, name, language, visibility, corpus_id=corpus_id, version=version, baseline_delimiter='++', encryption_key=encryption_key, full_repetativ_syntagma=True, ignore_hashtag=False, force_cleaning=False, ignore_url=False, ignore_mention=False, ignore_punkt=False, ignore_num=False)
        stats.compute(corp, stream_number=1, adjust_to_cpu=False, freeze_db=True, baseline_insertion_border=10)
        baseline = stats.statsdb.getall('baseline')
        repls = stats.statsdb.getall('replications')
        redus = stats.statsdb.getall('reduplications')
        repls.should.be.equal(right_repls)
        redus.should.be.equal(right_redus)
        self.configer.right_rep_num['en']['repls'].should.be.equal(len(repls))
        self.configer.right_rep_num['en']['redus'].should.be.equal(len(redus))
        self._check_correctnes(stats.col_index_orig, precomputed_data, repls=repls, redus=redus, baseline=baseline)
        bas_synts = [ bs[0] for bs in baseline ]
        for r in redus:
            if r[5] not in bas_synts:
                p(r[5], 'ERROR', c='r')
                assert False

        for r in repls:
            if r[5] not in bas_synts:
                p(r[5], 'ERROR', c='r')
                assert False

        return

    def _check_correctnes(self, indexes, precomputed_data, repls=False, redus=False, baseline=False):
        import copy
        dict_repls = defaultdict(lambda : defaultdict(lambda : defaultdict(lambda : 0)))
        dict_redus = defaultdict(lambda : defaultdict(lambda : defaultdict(lambda : 0)))
        dict_baseline = defaultdict()
        if repls:
            ix_repl = indexes['repl']
            for r in repls:
                doc_id = r[ix_repl['doc_id']]
                index_in_corpus = r[ix_repl['index_in_corpus']]
                word = r[ix_repl['normalized_word']]
                dict_repls[word][doc_id][index_in_corpus] += 1

        if redus:
            ix_redu = indexes['redu']
            for r in redus:
                doc_id = r[ix_redu['doc_id']]
                index_in_corpus = r[ix_redu['index_in_corpus']]
                word = r[ix_redu['normalized_word']]
                redu_length = r[ix_redu['redu_length']]
                dict_redus[word][doc_id][index_in_corpus] += redu_length

        if baseline:
            ix_b = indexes['baseline']
            for b in baseline:
                syntagma = b[ix_b['syntagma']]
                scope = b[ix_b['scope']]
                occur_syntagma_all = b[ix_b['occur_syntagma_all']]
                if int(scope) == 1:
                    dict_baseline[syntagma] = occur_syntagma_all

        computed_counts = defaultdict(lambda : defaultdict(lambda : [0, 0]))
        if repls:
            for word, word_data in dict_repls.items():
                for doc_id, doc_data in word_data.items():
                    for index_in_corpus, counter in doc_data.items():
                        computed_counts[word]['repl'][0] += 1
                        computed_counts[word]['repl'][1] += counter

        if redus:
            for word, word_data in dict_redus.items():
                for doc_id, doc_data in word_data.items():
                    for index_in_corpus, counter in doc_data.items():
                        computed_counts[word]['redu'][0] += 1
                        computed_counts[word]['redu'][1] += counter

        if baseline:
            for syntagma, counter in dict_baseline.items():
                computed_counts[syntagma]['baseline'] = counter

        precounted_reps = precomputed_data
        computed_counts = {word:{phanomen:tuple(counter) if isinstance(counter, (list, tuple)) else counter for phanomen, counter in data.items()} for word, data in computed_counts.items()}
        precounted_reps = {word:{phanomen:tuple(counter) if isinstance(counter, (list, tuple)) else counter for phanomen, counter in data.items()} for word, data in precounted_reps.items()}
        copy_precounted_reps = copy.deepcopy(precounted_reps)
        copy_computed_counts = copy.deepcopy(computed_counts)
        if repls and baseline or redus and baseline:
            computed_counts = {word:data for word, data in computed_counts.items() if 'repl' in data and 'baseline' in data or 'redu' in data and 'baseline' in data if 'repl' in data and 'baseline' in data or 'redu' in data and 'baseline' in data}
        for word, data in precounted_reps.items():
            for phanomen, counts in data.items():
                if phanomen == 'baseline':
                    if baseline:
                        if counts != computed_counts[word][phanomen]:
                            precomputed = counts
                            extracted = computed_counts[word][phanomen]
                        else:
                            del copy_computed_counts[word][phanomen]
                            del copy_precounted_reps[word][phanomen]
                else:
                    if not (phanomen == 'repl' and repls):
                        continue
                    elif not (phanomen == 'redu' and redus):
                        continue
                    if tuple(counts) != tuple(computed_counts[word][phanomen]):
                        precomputed = tuple(counts)
                        extracted = tuple(computed_counts[word][phanomen])
                    else:
                        del copy_computed_counts[word][phanomen]
                        del copy_precounted_reps[word][phanomen]

        for word, data in precounted_reps.items():
            if computed_counts[word] == data:
                del copy_computed_counts[word]
                del copy_precounted_reps[word]
            else:
                msg = ("Not Equal Data for word: '{}' >>>> '{}' != '{}' <<<<").format(word, data, computed_counts[word])

        copy_computed_counts = {word:data for word, data in copy_computed_counts.items() if len(data) > 1 if len(data) > 1}
        if copy_computed_counts:
            assert False
            copy_computed_counts = {word:data for word, data in copy_precounted_reps.items() if len(data) > 1 if len(data) > 1}
            assert copy_precounted_reps and False
        assert True

    def pretty_print_uniq(self, item, syn_order=False, baseline_small=True):
        if syn_order:
            print '\n\n\n'
            for k, v in item.iteritems():
                print '\n'
                if v and k not in ('syntagma', 'baseline', 'stem_syn'):
                    main_open_tag = '(' if isinstance(v, tuple) else '['
                    print ('\t\tright_{} = {}').format(k, main_open_tag)
                    if len(v) == 3 and v[1] in [True, False]:
                        main_open_tag1 = '(' if isinstance(v[0], tuple) else '['
                        print ('\t\t\t\t\t\t {}').format(main_open_tag1)
                        for data_for_syntagmas_part in v[0]:
                            word = data_for_syntagmas_part[0]
                            reps = data_for_syntagmas_part[1]
                            main_open_tag_2 = '(' if isinstance(data_for_syntagmas_part, tuple) else '['
                            open_tag = '(' if isinstance(reps, tuple) else '['
                            print ('\t\t\t\t\t\t\t{}{}, {}').format(main_open_tag_2, repr(word), open_tag)
                            for row in reps:
                                print ('\t\t\t\t\t\t\t\t\t\t\t {},').format(row)

                            main_close_tag_2 = ')' if isinstance(data_for_syntagmas_part, tuple) else ']'
                            close_tag = ')' if isinstance(reps, tuple) else ']'
                            print ('\t\t\t\t\t\t\t\t\t\t {}\n\t\t\t\t\t\t\t\t  {},').format(close_tag, main_close_tag_2)

                        main_close_tag1 = ')' if isinstance(v[0], tuple) else ']'
                        print ('\t\t\t\t\t\t {},').format(main_close_tag1)
                        print ('\t\t\t\t\t\t {},').format(v[1])
                        print ('\t\t\t\t\t\t {},').format(v[2])
                    else:
                        for data in v:
                            word = data[0]
                            reps = data[1]
                            main_open_tag_2 = '(' if isinstance(data, tuple) else '['
                            open_tag = '(' if isinstance(reps, tuple) else '['
                            print ('\t\t\t\t\t{}{}, {}').format(main_open_tag_2, repr(word), open_tag)
                            for row in reps:
                                print ('\t\t\t\t\t\t\t\t {},').format(row)

                            close_tag = ')' if isinstance(reps, tuple) else ']'
                            main_close_tag_2 = ')' if isinstance(data, tuple) else ']'
                            print ('\t\t\t\t\t\t\t {}\n\t\t\t\t\t  {},').format(close_tag, main_close_tag_2)

                    main_close_tag = ')' if isinstance(v, tuple) else ']'
                    print ('\t\t\t\t {}').format(main_close_tag)
                else:
                    print ('\t\tright_{} = {}').format(k, v)

        else:
            print '\n\n\n'
            for k, v in item.iteritems():
                print '\n'
                l = len(v)
                if len(v) >= 2 and k not in ('syntagma', 'stem_syn'):
                    if k == 'baseline' and baseline_small:
                        print ('\t\tright_{} = {}').format(k, v)
                        continue
                    if len(v) == 3 and v[1] in [True, False]:
                        open_tag = '(' if isinstance(v, tuple) else '['
                        print ('\t\tright_{} = {}').format(k, open_tag)
                        open_tag = '(' if isinstance(v[0], tuple) else '['
                        print ('\t\t\t\t\t\t {}').format(open_tag)
                        for row in v[0]:
                            print ('\t\t\t\t\t\t\t {},').format(row)

                        close_tag = ')' if isinstance(v[0], tuple) else ']'
                        print ('\t\t\t\t\t\t {},').format(close_tag)
                        print ('\t\t\t\t\t\t {},').format(v[1])
                        print ('\t\t\t\t\t\t {},').format(v[2])
                        close_tag = ')' if isinstance(v, tuple) else ']'
                        print ('\t\t\t {}').format(close_tag)
                    else:
                        open_tag = '(' if isinstance(v, tuple) else '['
                        print ('\t\tright_{} = {}').format(k, open_tag)
                        for row in v:
                            print ('\t\t\t\t\t {},').format(row)

                        close_tag = ')' if isinstance(v, tuple) else ']'
                        print ('\t\t\t\t {}').format(close_tag)
                else:
                    print ('\t\tright_{} = {}').format(k, v)

    def _summerize_reps(self, indexes, repls, redus, baseline):
        import copy
        dict_repls = defaultdict(lambda : defaultdict(lambda : defaultdict(lambda : 0)))
        dict_redus = defaultdict(lambda : defaultdict(lambda : defaultdict(lambda : 0)))
        dict_baseline = defaultdict()
        if repls:
            ix_repl = indexes['repl']
            for r in repls:
                doc_id = r[ix_repl['doc_id']]
                index_in_corpus = r[ix_repl['index_in_corpus']]
                word = r[ix_repl['normalized_word']]
                dict_repls[word][doc_id][index_in_corpus] += 1

        if redus:
            ix_redu = indexes['redu']
            for r in redus:
                doc_id = r[ix_redu['doc_id']]
                index_in_corpus = r[ix_redu['index_in_corpus']]
                word = r[ix_redu['normalized_word']]
                redu_length = r[ix_redu['redu_length']]
                dict_redus[word][doc_id][index_in_corpus] += redu_length

        if baseline:
            ix_b = indexes['baseline']
            for b in baseline:
                syntagma = b[ix_b['syntagma']][0]
                scope = b[ix_b['scope']]
                occur_syntagma_all = b[ix_b['occur_syntagma_all']]
                if int(scope) == 1:
                    dict_baseline[syntagma] = occur_syntagma_all

        computed_counts = defaultdict(lambda : defaultdict(lambda : [0, 0]))
        if repls:
            for word, word_data in dict_repls.items():
                for doc_id, doc_data in word_data.items():
                    for index_in_corpus, counter in doc_data.items():
                        computed_counts[word]['repl'][0] += 1
                        computed_counts[word]['repl'][1] += counter

        if redus:
            for word, word_data in dict_redus.items():
                for doc_id, doc_data in word_data.items():
                    for index_in_corpus, counter in doc_data.items():
                        computed_counts[word]['redu'][0] += 1
                        computed_counts[word]['redu'][1] += counter

        if baseline:
            for syntagma, counter in dict_baseline.items():
                computed_counts[syntagma]['baseline'] = counter

        out_repls = computed_counts[word]['repl'] if repls else None
        out_redus = computed_counts[word]['redu'] if redus else None
        out_baseline = computed_counts[syntagma]['baseline'] if baseline else None
        output = {}
        if out_repls and out_repls[0] > 0:
            output['repl'] = tuple(out_repls)
        if out_redus and out_redus[0] > 0:
            output['redu'] = tuple(out_redus)
        if out_baseline and out_baseline > 0:
            output['baseline'] = out_baseline
        return output

    def _summerize_reps2(self, indexes, repls, redus, baseline):
        import copy
        dict_repls = defaultdict(lambda : defaultdict(lambda : defaultdict(lambda : 0)))
        dict_redus = defaultdict(lambda : defaultdict(lambda : defaultdict(lambda : 0)))
        dict_baseline = defaultdict()
        if repls:
            ix_repl = indexes['repl']
            for r in repls:
                doc_id = r[ix_repl['doc_id']]
                index_in_corpus = r[ix_repl['index_in_corpus']]
                word = r[ix_repl['normalized_word']]
                dict_repls[word][doc_id][index_in_corpus] += 1

        if redus:
            ix_redu = indexes['redu']
            for r in redus:
                doc_id = r[ix_redu['doc_id']]
                index_in_corpus = r[ix_redu['index_in_corpus']]
                word = r[ix_redu['normalized_word']]
                redu_length = r[ix_redu['redu_length']]
                dict_redus[word][doc_id][index_in_corpus] += redu_length

        if baseline:
            ix_b = indexes['baseline']
            for b in baseline:
                syntagma = tuple(b[ix_b['syntagma']])
                scope = b[ix_b['scope']]
                occur_syntagma_all = b[ix_b['occur_syntagma_all']]
                dict_baseline[syntagma] = occur_syntagma_all

        computed_counts = defaultdict(lambda : defaultdict(lambda : [0, 0]))
        if repls:
            for word, word_data in dict_repls.items():
                for doc_id, doc_data in word_data.items():
                    for index_in_corpus, counter in doc_data.items():
                        computed_counts['repl'][word][0] += 1
                        computed_counts['repl'][word][1] += counter

        if redus:
            for word, word_data in dict_redus.items():
                for doc_id, doc_data in word_data.items():
                    for index_in_corpus, counter in doc_data.items():
                        computed_counts['redu'][word][0] += 1
                        computed_counts['redu'][word][1] += counter

        if baseline:
            for syntagma, counter in dict_baseline.items():
                computed_counts['baseline'][tuple(syntagma)] = counter

        return {phanomen:{word:counts for word, counts in data.items()} for phanomen, data in computed_counts.items()}

    @attr(status='stable')
    def test_get_data_for_one_syntagma_compared_with_gold_stabdard_611_0(self):
        self.prj_folder()
        self.test_dbs()
        stats = Stats(mode=self.mode, use_cash=True)
        stats.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_stats_en))
        gold_standard_data = self.configer._counted_reps['en']
        stats.recompute_syntagma_repetativity_scope(True)
        syntagma = [
         'bad']
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='lexem')
        right_data = gold_standard_data[syntagma[0]]
        answer = self._summerize_reps(stats.col_index_orig, item['repl'], item['redu'], item['baseline'])
        repl_num = right_data['repl'][1]
        redu_num = right_data['redu'][0]
        right_data.should.be.equal(answer)
        len(item['repl']).should.be.equal(repl_num)
        len(item['redu']).should.be.equal(redu_num)
        syntagma = [
         '-(']
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='lexem')
        right_data = gold_standard_data[syntagma[0]]
        answer = self._summerize_reps(stats.col_index_orig, item['repl'], item['redu'], item['baseline'])
        right_data.should.be.equal(answer)
        syntagma = [
         '-)']
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='lexem')
        right_data = gold_standard_data[syntagma[0]]
        answer = self._summerize_reps(stats.col_index_orig, item['repl'], item['redu'], item['baseline'])
        right_data.should.be.equal(answer)
        syntagma = [
         '=)']
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='lexem')
        right_data = gold_standard_data[syntagma[0]]
        answer = self._summerize_reps(stats.col_index_orig, item['repl'], item['redu'], item['baseline'])
        right_data.should.be.equal(answer)
        syntagma = [
         '.']
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='lexem')
        right_data = gold_standard_data[syntagma[0]]
        answer = self._summerize_reps(stats.col_index_orig, item['repl'], item['redu'], item['baseline'])
        right_data.should.be.equal(answer)
        syntagma = [
         '😀']
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='lexem')
        right_data = gold_standard_data[syntagma[0]]
        answer = self._summerize_reps(stats.col_index_orig, item['repl'], item['redu'], item['baseline'])
        right_data.should.be.equal(answer)
        syntagma = [
         '😫']
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='lexem')
        right_data = gold_standard_data[syntagma[0]]
        answer = self._summerize_reps(stats.col_index_orig, item['repl'], item['redu'], item['baseline'])
        right_data.should.be.equal(answer)
        syntagma = [
         'but']
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='lexem')
        right_data = gold_standard_data[syntagma[0]]
        answer = self._summerize_reps(stats.col_index_orig, item['repl'], item['redu'], item['baseline'])
        right_data.should.be.equal(answer)
        syntagma = [
         'se']
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='lexem')
        right_data = gold_standard_data[syntagma[0]]
        answer = self._summerize_reps(stats.col_index_orig, item['repl'], item['redu'], item['baseline'])
        right_data.should.be.equal(answer)
        syntagma = [
         'big']
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='lexem')
        right_data = gold_standard_data[syntagma[0]]
        answer = self._summerize_reps(stats.col_index_orig, item['repl'], item['redu'], item['baseline'])
        right_data.should.be.equal(answer)
        syntagma = [
         'se']
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='lexem')
        right_data = gold_standard_data[syntagma[0]]
        answer = self._summerize_reps(stats.col_index_orig, item['repl'], item['redu'], item['baseline'])
        right_data.should.be.equal(answer)
        syntagma = [
         'right']
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='lexem')
        right_data = gold_standard_data[syntagma[0]]
        answer = self._summerize_reps(stats.col_index_orig, item['repl'], item['redu'], item['baseline'])
        right_data.should.be.equal(answer)
        syntagma = [
         'EMOASC']
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='pos')
        right_data = {'repl': {'=)': [
                         1, 1], 
                    ':-(': [
                          2, 2], 
                    '-)': [
                         1, 1], 
                    '-(': [
                         1, 1]}, 
           'baseline': {(':-(', '@real_trump', '#shetlife'): 1, 
                        ('-(', '😫', ':-(', '#shetlife', 'http://www.noooo.com'): 1, 
                        ('=)', ): 1, 
                        (':-(', ): 2, (':-(', '@real_trump', '#shetlife', '#readytogo'): 1, 
                        (':-(', '#shetlife', 'http://www.noooo.com'): 1, 
                        ('=)', '😀', '🌈'): 1, 
                        ('=)', '😀', '🌈', '😀'): 1, 
                        ('=)', '😀'): 1, 
                        (':-(', '@real_trump'): 1, ('-(', '😫'): 1, 
                        ('-)', ): 1, 
                        ('-(', ): 1, 
                        ('-(', '😫', ':-('): 1, 
                        (':-(', '@real_trump', '#shetlife', '#readytogo', 'http://www.absurd.com'): 1, 
                        ('-(', '😫', ':-(', '#shetlife'): 1, 
                        (':-(', '#shetlife'): 1}}
        repl_num = sum([ counts[1] for word, counts in right_data['repl'].items() ])
        answer = self._summerize_reps2(stats.col_index_orig, item['repl'], item['redu'], item['baseline'])
        right_data.should.be.equal(answer)
        len(item['repl']).should.be.equal(repl_num)
        syntagma = [
         'number']
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='pos')
        right_data = {'repl': {'1': [2, 2]}, 'baseline': {('1', '.', 'but', 'you', 'but'): 1, ('1', '😫', '1', '.'): 1, ('1', '😫', '1', '.', 'but', 'you'): 1, ('1', '😫'): 1, ('1', '.', 'but'): 1, ('1', '😫', '1', '.', 'but'): 1, ('1', '.', 'but', 'you', 'but', 'you'): 1, ('1', ): 2, ('1', '.', 'but', 'you'): 1, ('1', '😫', '1'): 1, ('1', '.'): 1}}
        repl_num = sum([ counts[1] for word, counts in right_data['repl'].items() ])
        answer = self._summerize_reps2(stats.col_index_orig, item['repl'], item['redu'], item['baseline'])
        right_data.should.be.equal(answer)
        len(item['repl']).should.be.equal(repl_num)
        syntagma = [
         'very', 'pity']
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='lexem')
        right_data = {'repl': {'very': [
                           2, 4], 
                    'pity': [
                           2, 4]}, 
           'redu': {'very': [
                           1, 3], 
                    'pity': [
                           1, 4]}, 
           'baseline': {('very', 'pity'): 1}}
        repl_num = sum([ counts[1] for word, counts in right_data['repl'].items() ])
        redu_num = sum([ counts[0] for word, counts in right_data['redu'].items() ])
        answer = self._summerize_reps2(stats.col_index_orig, item['repl'], item['redu'], item['baseline'])
        right_data['repl'].should.be.equal(answer['repl'])
        right_data['redu'].should.be.equal(answer['redu'])
        right_data['baseline'].should.be.equal(answer['baseline'])
        len(item['repl']).should.be.equal(repl_num)
        len(item['redu']).should.be.equal(redu_num)
        syntagma = [
         'bad', 'news']
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='lexem')
        right_data = {'baseline': {('bad', 'news'): 1}}
        answer = self._summerize_reps2(stats.col_index_orig, item['repl'], item['redu'], item['baseline'])
        right_data.should.be.equal(answer)
        syntagma = [
         'but', 'you']
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='lexem')
        right_data = {'repl': {'you': [
                          6, 8], 
                    'but': [
                          10, 15]}, 
           'baseline': {('but', 'you'): 4}, 
           'redu': {'you': [
                          2, 4], 
                    'but': [
                          2, 4]}}
        repl_num = sum([ counts[1] for word, counts in right_data['repl'].items() ])
        redu_num = sum([ counts[0] for word, counts in right_data['redu'].items() ])
        answer = self._summerize_reps2(stats.col_index_orig, item['repl'], item['redu'], item['baseline'])
        right_data.should.be.equal(answer)
        len(item['repl']).should.be.equal(repl_num)
        len(item['redu']).should.be.equal(redu_num)
        syntagma = [
         '😀', '🌈']
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='lexem')
        right_data = {'repl': {'😀': [3, 3], '🌈': [
                        3, 3]}, 
           'baseline': {('😀', '🌈'): 3}}
        repl_num = sum([ counts[1] for word, counts in right_data['repl'].items() ])
        answer = self._summerize_reps2(stats.col_index_orig, item['repl'], item['redu'], item['baseline'])
        right_data.should.be.equal(answer)
        len(item['repl']).should.be.equal(repl_num)
        syntagma = [
         '🌈', '😀']
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='lexem')
        right_data = {'repl': {'😀': [
                        2, 2], 
                    '🌈': [
                        2, 2]}, 
           'baseline': {('🌈', '😀'): 3}}
        repl_num = sum([ counts[1] for word, counts in right_data['repl'].items() ])
        answer = self._summerize_reps2(stats.col_index_orig, item['repl'], item['redu'], item['baseline'])
        right_data.should.be.equal(answer)
        len(item['repl']).should.be.equal(repl_num)
        stats.recompute_syntagma_repetativity_scope(False)
        syntagma = [
         'bad', 'news']
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='lexem')
        right_data = {'repl': {'bad': [
                          4, 7]}, 
           'baseline': {('bad', 'news'): 1}, 
           'redu': {'bad': [
                          1, 5]}}
        answer = self._summerize_reps2(stats.col_index_orig, item['repl'], item['redu'], item['baseline'])
        right_data.should.be.equal(answer)
        syntagma = [
         'tiny', 'model']
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='lexem')
        right_data = {'repl': {'model': [1, 2]}, 'baseline': {('tiny', 'model'): 2}, 'redu': {'tiny': [1, 6]}}
        answer = self._summerize_reps2(stats.col_index_orig, item['repl'], item['redu'], item['baseline'])
        right_data.should.be.equal(answer)
        syntagma = [
         'but', 'you']
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='lexem')
        right_data = {'repl': {'you': [
                          6, 8], 
                    'but': [
                          10, 15]}, 
           'baseline': {('but', 'you'): 4}, 
           'redu': {'you': [
                          2, 4], 
                    'but': [
                          4, 10]}}
        repl_num = sum([ counts[1] for word, counts in right_data['repl'].items() ])
        redu_num = sum([ counts[0] for word, counts in right_data['redu'].items() ])
        answer = self._summerize_reps2(stats.col_index_orig, item['repl'], item['redu'], item['baseline'])
        right_data.should.be.equal(answer)
        len(item['repl']).should.be.equal(repl_num)
        len(item['redu']).should.be.equal(redu_num)
        syntagma = [
         '😀', '🌈']
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='lexem')
        right_data = {'repl': {'😀': [3, 3], '🌈': [
                        3, 3]}, 
           'baseline': {('😀', '🌈'): 3}}
        repl_num = sum([ counts[1] for word, counts in right_data['repl'].items() ])
        answer = self._summerize_reps2(stats.col_index_orig, item['repl'], item['redu'], item['baseline'])
        right_data.should.be.equal(answer)
        len(item['repl']).should.be.equal(repl_num)
        syntagma = [
         '🌈', '😀']
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='lexem')
        right_data = {'repl': {'😀': [
                        2, 2], 
                    '🌈': [
                        3, 3]}, 
           'baseline': {('🌈', '😀'): 3}}
        repl_num = sum([ counts[1] for word, counts in right_data['repl'].items() ])
        answer = self._summerize_reps2(stats.col_index_orig, item['repl'], item['redu'], item['baseline'])
        right_data.should.be.equal(answer)
        len(item['repl']).should.be.equal(repl_num)

    def convert_all_lists_to_tuples(self, giv_object):
        new_obj = []
        for item in giv_object:
            try:
                new_item = []
                for underitem in item:
                    new_item.append(tuple(underitem))

                new_obj.append(tuple(new_item))
            except:
                try:
                    new_obj.append(tuple(item))
                except:
                    new_obj.append(item)

        return tuple(new_obj)

    @attr(status='stable')
    def test_get_data_for_one_syntagma_611_1(self):
        self.prj_folder()
        self.test_dbs()
        stats = Stats(mode=self.mode, use_cash=True)
        stats.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_stats_de))
        stats.recompute_syntagma_repetativity_scope(True)
        syntagma = [
         'klitze']
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='lexem')
        extracted_repl = item['repl']
        extracted_redu = item['redu']
        extracted_baseline = item['baseline']
        extracted_syntagma = item['syntagma']
        right_repl = [
         (54, 11111, '[5, 6, 15, 3]', '[0, 1]', '[0, 1]', 'klitze', 'klitze^4', 'klitz', 'e',
 4, 5, None, 'VAPPER', '["neutral", 0.0]', None, None, None, None, None, None, None,
 None, 'eine', '["ART", null, "ein"]', 'kleine', '["ADJA", null, "klein"]', 'sache',
 '["NN", null, "sach"]', '.', '["symbol", null, "."]', 'die', '["PDS", null, "die"]',
 'aber', '["ADV", null, "aber"]'),
         (1, 8888, '[4, 11]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze^7', 'klitz', 'i', 4, 2,
 '[0, 0]', 'NN', '["neutral", 0.0]', None, None, None, None, None, None, None, None,
 None, None, 'kleine', '["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', 'überaschung',
 '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]',
 'hat', '["VAFIN", null, "hat"]'),
         (2, 8888, '[4, 11]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze^7', 'klitz', 'e', 7, 5,
 '[0, 0]', 'NN', '["neutral", 0.0]', None, None, None, None, None, None, None, None,
 None, None, 'kleine', '["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', 'überaschung',
 '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]',
 'hat', '["VAFIN", null, "hat"]'),
         (20, 10000, '[12, 3, 8]', '[0, 1]', '[0, 1]', 'klitze', 'klitze^4', 'klitz', 'e', 4,
 5, None, 'ADJA', '["neutral", 0.0]', None, None, None, None, None, None, None, None,
 'eine', '["ART", null, "ein"]', 'kleine', '["ADJA", null, "klein"]', 'überaschung',
 '["NN", null, "uberasch"]', '@schönesleben', '["mention", null, "@schonesleb"]',
 '#machwasdaraus', '["hashtag", null, "#machwasdaraus"]', '#bewegedeinarsch', '["hashtag", null, "#bewegedeinarsch"]')]
        right_syntagma = [
         'klitze']
        right_baseline = [
         [
          [
           'klitze'], 'klitz', 1, 8, '3', '4', '2', '6', '3', '2']]
        right_redu = [
         (18, 12222, '[24]', '[0, 1]', '[0, 1]', 'klitze', 'klitz', '{"klitze": 4}', 4, 'NN',
 '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'eine', '["ART", null, "ein"]',
 'kleine', '["ADJA", null, "klein"]', 'überaschung', '["NN", null, "uberasch"]',
 ',', '["symbol", null, ","]', 'die', '["PRELS", null, "die"]', 'ich', '["PPER", null, "ich"]'),
         (1, 8888, '[4, 11]', '[0, 0]', '[0, 0]', 'klitze', 'klitz', '{"klitze": 1, "kli^4tze^7": 1}',
 2, 'NN', '["neutral", 0.0]', None, None, None, None, None, None, None, None, None,
 None, 'kleine', '["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', 'überaschung',
 '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]',
 'hat', '["VAFIN", null, "hat"]')]
        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list(tuple(unicode(elem) for elem in item) for item in extracted_baseline)).should.be.equal(set(list(tuple(unicode(elem) for elem in item) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)
        syntagma = [
         'kleine']
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='lexem')
        extracted_repl = item['repl']
        extracted_redu = item['redu']
        extracted_baseline = item['baseline']
        extracted_syntagma = item['syntagma']
        right_repl = [
         (82, 12222, '[24]', '[0, 24]', '[0, 21]', 'kleine', 'kle^4i^5n^4e^8', 'klein', 'e',
 4, 2, None, 'ADJA', '["neutral", 0.0]', ',', '["symbol", null, ","]', 'es', '["PPER", null, "es"]',
 'war', '["VAFIN", null, "war"]', 'so', '["ADV", null, "so"]', 'eine', '["ART", null, "ein"]',
 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', None, None,
 None, None, None, None),
         (83, 12222, '[24]', '[0, 24]', '[0, 21]', 'kleine', 'kle^4i^5n^4e^8', 'klein', 'i',
 5, 3, None, 'ADJA', '["neutral", 0.0]', ',', '["symbol", null, ","]', 'es', '["PPER", null, "es"]',
 'war', '["VAFIN", null, "war"]', 'so', '["ADV", null, "so"]', 'eine', '["ART", null, "ein"]',
 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', None, None,
 None, None, None, None),
         (84, 12222, '[24]', '[0, 24]', '[0, 21]', 'kleine', 'kle^4i^5n^4e^8', 'klein', 'n',
 4, 4, None, 'ADJA', '["neutral", 0.0]', ',', '["symbol", null, ","]', 'es', '["PPER", null, "es"]',
 'war', '["VAFIN", null, "war"]', 'so', '["ADV", null, "so"]', 'eine', '["ART", null, "ein"]',
 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', None, None,
 None, None, None, None),
         (85, 12222, '[24]', '[0, 24]', '[0, 21]', 'kleine', 'kle^4i^5n^4e^8', 'klein', 'e',
 8, 5, None, 'ADJA', '["neutral", 0.0]', ',', '["symbol", null, ","]', 'es', '["PPER", null, "es"]',
 'war', '["VAFIN", null, "war"]', 'so', '["ADV", null, "so"]', 'eine', '["ART", null, "ein"]',
 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', None, None,
 None, None, None, None),
         (3, 8888, '[4, 11]', '[0, 2]', '[0, 1]', 'kleine', 'kle^5in^5e', 'klein', 'e', 5, 2,
 '[0, 1]', 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None,
 'klitze', '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]',
 '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]',
 'sie', '["PPER", null, "sie"]'),
         (4, 8888, '[4, 11]', '[0, 2]', '[0, 1]', 'kleine', 'kle^5in^5e', 'klein', 'n', 5, 4,
 '[0, 1]', 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None,
 'klitze', '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]',
 '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]',
 'sie', '["PPER", null, "sie"]'),
         (5, 8888, '[4, 11]', '[0, 3]', '[0, 1]', 'kleine', 'klein^3e', 'klein', 'n', 3, 4,
 '[0, 1]', 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None,
 'klitze', '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]',
 '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]',
 'sie', '["PPER", null, "sie"]'),
         (21, 10000, '[12, 3, 8]', '[0, 2]', '[0, 2]', 'kleine', 'kle^5ine', 'klein', 'e', 5,
 2, None, 'ADJA', '["neutral", 0.0]', None, None, None, None, None, None, 'eine',
 '["ART", null, "ein"]', 'klitze', '["ADJA", null, "klitz"]', 'überaschung', '["NN", null, "uberasch"]',
 '@schönesleben', '["mention", null, "@schonesleb"]', '#machwasdaraus', '["hashtag", null, "#machwasdaraus"]',
 '#bewegedeinarsch', '["hashtag", null, "#bewegedeinarsch"]', 'https://www.freiesinternet.de',
 '["URL", null, "https://www.freiesinternet.d"]'),
         (57, 11111, '[5, 6, 15, 3]', '[2, 4]', '[2, 4]', 'kleine', 'kle^5i^2n^4e^5', 'klein',
 'e', 5, 2, None, 'ADJA', '["neutral", 0.0]', '!', '["symbol", null, "!"]', 'weil',
 '["KOUS", null, "weil"]', 'es', '["PPER", null, "es"]', 'ja', '["PTKMA", null, "ja"]',
 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', 'ist',
 '["VAFIN", null, "ist"]', '.', '["symbol", null, "."]', 1, '["number", null, "1"]',
 2, '["number", null, "2"]'),
         (58, 11111, '[5, 6, 15, 3]', '[2, 4]', '[2, 4]', 'kleine', 'kle^5i^2n^4e^5', 'klein',
 'n', 4, 4, None, 'ADJA', '["neutral", 0.0]', '!', '["symbol", null, "!"]', 'weil',
 '["KOUS", null, "weil"]', 'es', '["PPER", null, "es"]', 'ja', '["PTKMA", null, "ja"]',
 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', 'ist',
 '["VAFIN", null, "ist"]', '.', '["symbol", null, "."]', 1, '["number", null, "1"]',
 2, '["number", null, "2"]'),
         (59, 11111, '[5, 6, 15, 3]', '[2, 4]', '[2, 4]', 'kleine', 'kle^5i^2n^4e^5', 'klein',
 'e', 5, 5, None, 'ADJA', '["neutral", 0.0]', '!', '["symbol", null, "!"]', 'weil',
 '["KOUS", null, "weil"]', 'es', '["PPER", null, "es"]', 'ja', '["PTKMA", null, "ja"]',
 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', 'ist',
 '["VAFIN", null, "ist"]', '.', '["symbol", null, "."]', 1, '["number", null, "1"]',
 2, '["number", null, "2"]')]
        right_syntagma = [
         'kleine']
        right_baseline = [
         [
          [
           'kleine'], 'klein', 1, 7, '5', '11', '1', '2', '5', '1']]
        right_redu = [
         (2, 8888, '[4, 11]', '[0, 2]', '[0, 1]', 'kleine', 'klein', '{"kle^5in^5e": 1, "klein^3e": 1}',
 2, 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze',
 '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]',
 '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]',
 'sie', '["PPER", null, "sie"]')]
        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list(tuple(unicode(elem) for elem in item) for item in extracted_baseline)).should.be.equal(set(list(tuple(unicode(elem) for elem in item) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)
        syntagma = [
         'klein']
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='lexem', stemmed_search=True)
        extracted_repl = item['repl']
        extracted_redu = item['redu']
        extracted_baseline = item['baseline']
        extracted_syntagma = item['syntagma']
        right_repl = [
         (3, 8888, '[4, 11]', '[0, 2]', '[0, 1]', 'kleine', 'kle^5in^5e', 'klein', 'e', 5, 2,
 '[0, 1]', 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None,
 'klitze', '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]',
 '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]',
 'sie', '["PPER", null, "sie"]'),
         (4, 8888, '[4, 11]', '[0, 2]', '[0, 1]', 'kleine', 'kle^5in^5e', 'klein', 'n', 5, 4,
 '[0, 1]', 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None,
 'klitze', '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]',
 '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]',
 'sie', '["PPER", null, "sie"]'),
         (5, 8888, '[4, 11]', '[0, 3]', '[0, 1]', 'kleine', 'klein^3e', 'klein', 'n', 3, 4,
 '[0, 1]', 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None,
 'klitze', '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]',
 '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]',
 'sie', '["PPER", null, "sie"]'),
         (21, 10000, '[12, 3, 8]', '[0, 2]', '[0, 2]', 'kleine', 'kle^5ine', 'klein', 'e', 5,
 2, None, 'ADJA', '["neutral", 0.0]', None, None, None, None, None, None, 'eine',
 '["ART", null, "ein"]', 'klitze', '["ADJA", null, "klitz"]', 'überaschung', '["NN", null, "uberasch"]',
 '@schönesleben', '["mention", null, "@schonesleb"]', '#machwasdaraus', '["hashtag", null, "#machwasdaraus"]',
 '#bewegedeinarsch', '["hashtag", null, "#bewegedeinarsch"]', 'https://www.freiesinternet.de',
 '["URL", null, "https://www.freiesinternet.d"]'),
         (26, 10000, '[12, 3, 8]', '[1, 0]', '[1, 0]', 'kleines', 'kleine^4s^7', 'klein', 'e',
 4, 5, '[1, 0]', 'NN', '["neutral", 0.0]', 'https://www.freiesinternet.de', '["URL", null, "https://www.freiesinternet.d"]',
 'beser', '["ADJD", null, "bes"]', 'kan', '["FM", {"ka^4n^5": 1, "kan^6": 1}, "kan"]',
 'es', '["VVFIN", null, "es"]', '.', '["symbol", null, "."]', 'mädchen', '["NN", null, "madch"]',
 '.', '["symbol", null, "."]', 'kleinere', '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]',
 'auswahl', '["NN", null, "auswahl"]', '.', '["symbol", null, "."]'),
         (27, 10000, '[12, 3, 8]', '[1, 0]', '[1, 0]', 'kleines', 'kleine^4s^7', 'klein', 's',
 7, 6, '[1, 0]', 'NN', '["neutral", 0.0]', 'https://www.freiesinternet.de', '["URL", null, "https://www.freiesinternet.d"]',
 'beser', '["ADJD", null, "bes"]', 'kan', '["FM", {"ka^4n^5": 1, "kan^6": 1}, "kan"]',
 'es', '["VVFIN", null, "es"]', '.', '["symbol", null, "."]', 'mädchen', '["NN", null, "madch"]',
 '.', '["symbol", null, "."]', 'kleinere', '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]',
 'auswahl', '["NN", null, "auswahl"]', '.', '["symbol", null, "."]'),
         (28, 10000, '[12, 3, 8]', '[1, 1]', '[1, 0]', 'kleines', 'klein^4e^3s^4', 'klein',
 'n', 4, 4, '[1, 0]', 'NN', '["neutral", 0.0]', 'https://www.freiesinternet.de',
 '["URL", null, "https://www.freiesinternet.d"]', 'beser', '["ADJD", null, "bes"]',
 'kan', '["FM", {"ka^4n^5": 1, "kan^6": 1}, "kan"]', 'es', '["VVFIN", null, "es"]',
 '.', '["symbol", null, "."]', 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]',
 'kleinere', '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', 'auswahl',
 '["NN", null, "auswahl"]', '.', '["symbol", null, "."]'),
         (29, 10000, '[12, 3, 8]', '[1, 1]', '[1, 0]', 'kleines', 'klein^4e^3s^4', 'klein',
 'e', 3, 5, '[1, 0]', 'NN', '["neutral", 0.0]', 'https://www.freiesinternet.de',
 '["URL", null, "https://www.freiesinternet.d"]', 'beser', '["ADJD", null, "bes"]',
 'kan', '["FM", {"ka^4n^5": 1, "kan^6": 1}, "kan"]', 'es', '["VVFIN", null, "es"]',
 '.', '["symbol", null, "."]', 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]',
 'kleinere', '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', 'auswahl',
 '["NN", null, "auswahl"]', '.', '["symbol", null, "."]'),
         (30, 10000, '[12, 3, 8]', '[1, 1]', '[1, 0]', 'kleines', 'klein^4e^3s^4', 'klein',
 's', 4, 6, '[1, 0]', 'NN', '["neutral", 0.0]', 'https://www.freiesinternet.de',
 '["URL", null, "https://www.freiesinternet.d"]', 'beser', '["ADJD", null, "bes"]',
 'kan', '["FM", {"ka^4n^5": 1, "kan^6": 1}, "kan"]', 'es', '["VVFIN", null, "es"]',
 '.', '["symbol", null, "."]', 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]',
 'kleinere', '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', 'auswahl',
 '["NN", null, "auswahl"]', '.', '["symbol", null, "."]'),
         (31, 10000, '[12, 3, 8]', '[1, 2]', '[1, 0]', 'kleines', 'kle^4i^5n^3e^2s^3', 'klein',
 'e', 4, 2, '[1, 0]', 'NN', '["neutral", 0.0]', 'https://www.freiesinternet.de',
 '["URL", null, "https://www.freiesinternet.d"]', 'beser', '["ADJD", null, "bes"]',
 'kan', '["FM", {"ka^4n^5": 1, "kan^6": 1}, "kan"]', 'es', '["VVFIN", null, "es"]',
 '.', '["symbol", null, "."]', 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]',
 'kleinere', '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', 'auswahl',
 '["NN", null, "auswahl"]', '.', '["symbol", null, "."]'),
         (32, 10000, '[12, 3, 8]', '[1, 2]', '[1, 0]', 'kleines', 'kle^4i^5n^3e^2s^3', 'klein',
 'i', 5, 3, '[1, 0]', 'NN', '["neutral", 0.0]', 'https://www.freiesinternet.de',
 '["URL", null, "https://www.freiesinternet.d"]', 'beser', '["ADJD", null, "bes"]',
 'kan', '["FM", {"ka^4n^5": 1, "kan^6": 1}, "kan"]', 'es', '["VVFIN", null, "es"]',
 '.', '["symbol", null, "."]', 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]',
 'kleinere', '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', 'auswahl',
 '["NN", null, "auswahl"]', '.', '["symbol", null, "."]'),
         (33, 10000, '[12, 3, 8]', '[1, 2]', '[1, 0]', 'kleines', 'kle^4i^5n^3e^2s^3', 'klein',
 'n', 3, 4, '[1, 0]', 'NN', '["neutral", 0.0]', 'https://www.freiesinternet.de',
 '["URL", null, "https://www.freiesinternet.d"]', 'beser', '["ADJD", null, "bes"]',
 'kan', '["FM", {"ka^4n^5": 1, "kan^6": 1}, "kan"]', 'es', '["VVFIN", null, "es"]',
 '.', '["symbol", null, "."]', 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]',
 'kleinere', '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', 'auswahl',
 '["NN", null, "auswahl"]', '.', '["symbol", null, "."]'),
         (34, 10000, '[12, 3, 8]', '[1, 2]', '[1, 0]', 'kleines', 'kle^4i^5n^3e^2s^3', 'klein',
 's', 3, 6, '[1, 0]', 'NN', '["neutral", 0.0]', 'https://www.freiesinternet.de',
 '["URL", null, "https://www.freiesinternet.d"]', 'beser', '["ADJD", null, "bes"]',
 'kan', '["FM", {"ka^4n^5": 1, "kan^6": 1}, "kan"]', 'es', '["VVFIN", null, "es"]',
 '.', '["symbol", null, "."]', 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]',
 'kleinere', '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', 'auswahl',
 '["NN", null, "auswahl"]', '.', '["symbol", null, "."]'),
         (37, 10000, '[12, 3, 8]', '[2, 0]', '[2, 0]', 'kleinere', 'kleinere^5', 'klein', 'e',
 5, 7, '[2, 0]', 'NE', '["neutral", 0.0]', 'es', '["VVFIN", null, "es"]', '.', '["symbol", null, "."]',
 'kleines', '["NN", {"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}, "klein"]',
 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', 'auswahl', '["NN", null, "auswahl"]',
 '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]',
 'klein', '["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', '.', '["symbol", null, "."]'),
         (38, 10000, '[12, 3, 8]', '[2, 1]', '[2, 0]', 'kleinere', 'kleine^3r^2e^5', 'klein',
 'e', 3, 5, '[2, 0]', 'NE', '["neutral", 0.0]', 'es', '["VVFIN", null, "es"]', '.',
 '["symbol", null, "."]', 'kleines', '["NN", {"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}, "klein"]',
 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', 'auswahl', '["NN", null, "auswahl"]',
 '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]',
 'klein', '["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', '.', '["symbol", null, "."]'),
         (39, 10000, '[12, 3, 8]', '[2, 1]', '[2, 0]', 'kleinere', 'kleine^3r^2e^5', 'klein',
 'e', 5, 7, '[2, 0]', 'NE', '["neutral", 0.0]', 'es', '["VVFIN", null, "es"]', '.',
 '["symbol", null, "."]', 'kleines', '["NN", {"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}, "klein"]',
 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', 'auswahl', '["NN", null, "auswahl"]',
 '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]',
 'klein', '["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', '.', '["symbol", null, "."]'),
         (45, 10000, '[12, 3, 8]', '[2, 7]', '[2, 4]', 'klein', 'kle^3i^3n^3', 'klein', 'e',
 3, 2, '[2, 4]', 'FM', '["neutral", 0.0]', '.', '["symbol", null, "."]', 'kleinere',
 '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', 'auswahl', '["NN", null, "auswahl"]',
 '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]',
 '.', '["symbol", null, "."]', 'klitzes', '["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]',
 'kleines', '["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None,
 None),
         (46, 10000, '[12, 3, 8]', '[2, 7]', '[2, 4]', 'klein', 'kle^3i^3n^3', 'klein', 'i',
 3, 3, '[2, 4]', 'FM', '["neutral", 0.0]', '.', '["symbol", null, "."]', 'kleinere',
 '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', 'auswahl', '["NN", null, "auswahl"]',
 '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]',
 '.', '["symbol", null, "."]', 'klitzes', '["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]',
 'kleines', '["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None,
 None),
         (47, 10000, '[12, 3, 8]', '[2, 7]', '[2, 4]', 'klein', 'kle^3i^3n^3', 'klein', 'n',
 3, 4, '[2, 4]', 'FM', '["neutral", 0.0]', '.', '["symbol", null, "."]', 'kleinere',
 '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', 'auswahl', '["NN", null, "auswahl"]',
 '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]',
 '.', '["symbol", null, "."]', 'klitzes', '["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]',
 'kleines', '["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None,
 None),
         (48, 10000, '[12, 3, 8]', '[2, 8]', '[2, 4]', 'klein', 'klein^5', 'klein', 'n', 5,
 4, '[2, 4]', 'FM', '["neutral", 0.0]', '.', '["symbol", null, "."]', 'kleinere',
 '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', 'auswahl', '["NN", null, "auswahl"]',
 '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]',
 '.', '["symbol", null, "."]', 'klitzes', '["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]',
 'kleines', '["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None,
 None),
         (52, 10000, '[12, 3, 8]', '[2, 12]', '[2, 7]', 'kleines', 'klein^3e^2s', 'klein', 'n',
 3, 4, '[2, 7]', 'FM', '["neutral", 0.0]', '.', '["symbol", null, "."]', 'klitz',
 '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', 'klein', '["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]',
 '.', '["symbol", null, "."]', 'klitzes', '["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]',
 None, None, None, None, None, None, None, None, None, None),
         (53, 10000, '[12, 3, 8]', '[2, 13]', '[2, 7]', 'kleines', 'kleines^4', 'klein', 's',
 4, 6, '[2, 7]', 'FM', '["neutral", 0.0]', '.', '["symbol", null, "."]', 'klitz',
 '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', 'klein', '["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]',
 '.', '["symbol", null, "."]', 'klitzes', '["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]',
 None, None, None, None, None, None, None, None, None, None),
         (57, 11111, '[5, 6, 15, 3]', '[2, 4]', '[2, 4]', 'kleine', 'kle^5i^2n^4e^5', 'klein',
 'e', 5, 2, None, 'ADJA', '["neutral", 0.0]', '!', '["symbol", null, "!"]', 'weil',
 '["KOUS", null, "weil"]', 'es', '["PPER", null, "es"]', 'ja', '["PTKMA", null, "ja"]',
 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', 'ist',
 '["VAFIN", null, "ist"]', '.', '["symbol", null, "."]', 1, '["number", null, "1"]',
 2, '["number", null, "2"]'),
         (58, 11111, '[5, 6, 15, 3]', '[2, 4]', '[2, 4]', 'kleine', 'kle^5i^2n^4e^5', 'klein',
 'n', 4, 4, None, 'ADJA', '["neutral", 0.0]', '!', '["symbol", null, "!"]', 'weil',
 '["KOUS", null, "weil"]', 'es', '["PPER", null, "es"]', 'ja', '["PTKMA", null, "ja"]',
 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', 'ist',
 '["VAFIN", null, "ist"]', '.', '["symbol", null, "."]', 1, '["number", null, "1"]',
 2, '["number", null, "2"]'),
         (59, 11111, '[5, 6, 15, 3]', '[2, 4]', '[2, 4]', 'kleine', 'kle^5i^2n^4e^5', 'klein',
 'e', 5, 5, None, 'ADJA', '["neutral", 0.0]', '!', '["symbol", null, "!"]', 'weil',
 '["KOUS", null, "weil"]', 'es', '["PPER", null, "es"]', 'ja', '["PTKMA", null, "ja"]',
 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', 'ist',
 '["VAFIN", null, "ist"]', '.', '["symbol", null, "."]', 1, '["number", null, "1"]',
 2, '["number", null, "2"]'),
         (66, 11111, '[5, 6, 15, 3]', '[3, 0]', '[3, 0]', 'kleines', 'kleine^4s^7', 'klein',
 'e', 4, 5, '[3, 0]', 'NN', '["neutral", 0.0]', 3, '["number", null, "3"]', 4, '["number", null, "4"]',
 5, '["number", null, "5"]', 6, '["number", null, "6"]', '.', '["symbol", null, "."]',
 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', None, None, None,
 None, None, None),
         (67, 11111, '[5, 6, 15, 3]', '[3, 0]', '[3, 0]', 'kleines', 'kleine^4s^7', 'klein',
 's', 7, 6, '[3, 0]', 'NN', '["neutral", 0.0]', 3, '["number", null, "3"]', 4, '["number", null, "4"]',
 5, '["number", null, "5"]', 6, '["number", null, "6"]', '.', '["symbol", null, "."]',
 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', None, None, None,
 None, None, None),
         (68, 11111, '[5, 6, 15, 3]', '[3, 1]', '[3, 0]', 'kleines', 'klein^4e^3s^4', 'klein',
 'n', 4, 4, '[3, 0]', 'NN', '["neutral", 0.0]', 3, '["number", null, "3"]', 4, '["number", null, "4"]',
 5, '["number", null, "5"]', 6, '["number", null, "6"]', '.', '["symbol", null, "."]',
 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', None, None, None,
 None, None, None),
         (69, 11111, '[5, 6, 15, 3]', '[3, 1]', '[3, 0]', 'kleines', 'klein^4e^3s^4', 'klein',
 'e', 3, 5, '[3, 0]', 'NN', '["neutral", 0.0]', 3, '["number", null, "3"]', 4, '["number", null, "4"]',
 5, '["number", null, "5"]', 6, '["number", null, "6"]', '.', '["symbol", null, "."]',
 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', None, None, None,
 None, None, None),
         (70, 11111, '[5, 6, 15, 3]', '[3, 1]', '[3, 0]', 'kleines', 'klein^4e^3s^4', 'klein',
 's', 4, 6, '[3, 0]', 'NN', '["neutral", 0.0]', 3, '["number", null, "3"]', 4, '["number", null, "4"]',
 5, '["number", null, "5"]', 6, '["number", null, "6"]', '.', '["symbol", null, "."]',
 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', None, None, None,
 None, None, None),
         (71, 11111, '[5, 6, 15, 3]', '[3, 2]', '[3, 0]', 'kleines', 'kle^4i^5n^3e^2s^3', 'klein',
 'e', 4, 2, '[3, 0]', 'NN', '["neutral", 0.0]', 3, '["number", null, "3"]', 4, '["number", null, "4"]',
 5, '["number", null, "5"]', 6, '["number", null, "6"]', '.', '["symbol", null, "."]',
 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', None, None, None,
 None, None, None),
         (72, 11111, '[5, 6, 15, 3]', '[3, 2]', '[3, 0]', 'kleines', 'kle^4i^5n^3e^2s^3', 'klein',
 'i', 5, 3, '[3, 0]', 'NN', '["neutral", 0.0]', 3, '["number", null, "3"]', 4, '["number", null, "4"]',
 5, '["number", null, "5"]', 6, '["number", null, "6"]', '.', '["symbol", null, "."]',
 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', None, None, None,
 None, None, None),
         (73, 11111, '[5, 6, 15, 3]', '[3, 2]', '[3, 0]', 'kleines', 'kle^4i^5n^3e^2s^3', 'klein',
 'n', 3, 4, '[3, 0]', 'NN', '["neutral", 0.0]', 3, '["number", null, "3"]', 4, '["number", null, "4"]',
 5, '["number", null, "5"]', 6, '["number", null, "6"]', '.', '["symbol", null, "."]',
 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', None, None, None,
 None, None, None),
         (74, 11111, '[5, 6, 15, 3]', '[3, 2]', '[3, 0]', 'kleines', 'kle^4i^5n^3e^2s^3', 'klein',
 's', 3, 6, '[3, 0]', 'NN', '["neutral", 0.0]', 3, '["number", null, "3"]', 4, '["number", null, "4"]',
 5, '["number", null, "5"]', 6, '["number", null, "6"]', '.', '["symbol", null, "."]',
 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', None, None, None,
 None, None, None),
         (82, 12222, '[24]', '[0, 24]', '[0, 21]', 'kleine', 'kle^4i^5n^4e^8', 'klein', 'e',
 4, 2, None, 'ADJA', '["neutral", 0.0]', ',', '["symbol", null, ","]', 'es', '["PPER", null, "es"]',
 'war', '["VAFIN", null, "war"]', 'so', '["ADV", null, "so"]', 'eine', '["ART", null, "ein"]',
 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', None, None,
 None, None, None, None),
         (83, 12222, '[24]', '[0, 24]', '[0, 21]', 'kleine', 'kle^4i^5n^4e^8', 'klein', 'i',
 5, 3, None, 'ADJA', '["neutral", 0.0]', ',', '["symbol", null, ","]', 'es', '["PPER", null, "es"]',
 'war', '["VAFIN", null, "war"]', 'so', '["ADV", null, "so"]', 'eine', '["ART", null, "ein"]',
 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', None, None,
 None, None, None, None),
         (84, 12222, '[24]', '[0, 24]', '[0, 21]', 'kleine', 'kle^4i^5n^4e^8', 'klein', 'n',
 4, 4, None, 'ADJA', '["neutral", 0.0]', ',', '["symbol", null, ","]', 'es', '["PPER", null, "es"]',
 'war', '["VAFIN", null, "war"]', 'so', '["ADV", null, "so"]', 'eine', '["ART", null, "ein"]',
 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', None, None,
 None, None, None, None),
         (85, 12222, '[24]', '[0, 24]', '[0, 21]', 'kleine', 'kle^4i^5n^4e^8', 'klein', 'e',
 8, 5, None, 'ADJA', '["neutral", 0.0]', ',', '["symbol", null, ","]', 'es', '["PPER", null, "es"]',
 'war', '["VAFIN", null, "war"]', 'so', '["ADV", null, "so"]', 'eine', '["ART", null, "ein"]',
 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', None, None,
 None, None, None, None)]
        right_syntagma = [
         'klein']
        right_baseline = [
         [
          [
           'kleines'], 'klein', 1, 8, '8', '20', '3', '8', '8', '3'], [['kleinere'], 'klein', 1, 2, '2', '3', '1', '2', '2', '1'], [['kleine'], 'klein', 1, 7, '5', '11', '1', '2', '5', '1'], [['klein'], 'klein', 1, 2, '2', '4', '1', '2', '2', '1']]
        right_redu = [
         (2, 8888, '[4, 11]', '[0, 2]', '[0, 1]', 'kleine', 'klein', '{"kle^5in^5e": 1, "klein^3e": 1}',
 2, 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze',
 '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]',
 '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]',
 'sie', '["PPER", null, "sie"]'),
         (11, 10000, '[12, 3, 8]', '[1, 0]', '[1, 0]', 'kleines', 'klein', '{"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}',
 3, 'NN', '["neutral", 0.0]', 'https://www.freiesinternet.de', '["URL", null, "https://www.freiesinternet.d"]',
 'beser', '["ADJD", null, "bes"]', 'kan', '["FM", {"ka^4n^5": 1, "kan^6": 1}, "kan"]',
 'es', '["VVFIN", null, "es"]', '.', '["symbol", null, "."]', 'mädchen', '["NN", null, "madch"]',
 '.', '["symbol", null, "."]', 'kleinere', '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]',
 'auswahl', '["NN", null, "auswahl"]', '.', '["symbol", null, "."]'),
         (12, 10000, '[12, 3, 8]', '[2, 0]', '[2, 0]', 'kleinere', 'klein', '{"kleinere^5": 1, "kleine^3r^2e^5": 1}',
 2, 'NE', '["neutral", 0.0]', 'es', '["VVFIN", null, "es"]', '.', '["symbol", null, "."]',
 'kleines', '["NN", {"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}, "klein"]',
 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', 'auswahl', '["NN", null, "auswahl"]',
 '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]',
 'klein', '["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', '.', '["symbol", null, "."]'),
         (14, 10000, '[12, 3, 8]', '[2, 7]', '[2, 4]', 'klein', 'klein', '{"kle^3i^3n^3": 1, "klein^5": 1}',
 2, 'FM', '["neutral", 0.0]', '.', '["symbol", null, "."]', 'kleinere', '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]',
 'auswahl', '["NN", null, "auswahl"]', '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]',
 '.', '["symbol", null, "."]', 'klitzes', '["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]',
 'kleines', '["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None,
 None),
         (16, 10000, '[12, 3, 8]', '[2, 12]', '[2, 7]', 'kleines', 'klein', '{"klein^3e^2s": 1, "kleines^4": 1}',
 2, 'FM', '["neutral", 0.0]', '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]',
 'klein', '["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', '.', '["symbol", null, "."]',
 'klitzes', '["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', None, None, None,
 None, None, None, None, None, None, None),
         (17, 11111, '[5, 6, 15, 3]', '[3, 0]', '[3, 0]', 'kleines', 'klein', '{"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}',
 3, 'NN', '["neutral", 0.0]', 3, '["number", null, "3"]', 4, '["number", null, "4"]',
 5, '["number", null, "5"]', 6, '["number", null, "6"]', '.', '["symbol", null, "."]',
 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', None, None, None,
 None, None, None)]
        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list(tuple(unicode(elem) for elem in item) for item in extracted_baseline)).should.be.equal(set(list(tuple(unicode(elem) for elem in item) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)
        syntagma = [
         'klitze', 'kleine']
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='lexem')
        extracted_repl = item['repl']
        extracted_redu = item['redu']
        extracted_baseline = item['baseline']
        extracted_syntagma = item['syntagma']
        right_repl = [
         (1, 8888, '[4, 11]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze^7', 'klitz', 'i', 4, 2,
 '[0, 0]', 'NN', '["neutral", 0.0]', None, None, None, None, None, None, None, None,
 None, None, 'kleine', '["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', 'überaschung',
 '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]',
 'hat', '["VAFIN", null, "hat"]'),
         (2, 8888, '[4, 11]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze^7', 'klitz', 'e', 7, 5,
 '[0, 0]', 'NN', '["neutral", 0.0]', None, None, None, None, None, None, None, None,
 None, None, 'kleine', '["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', 'überaschung',
 '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]',
 'hat', '["VAFIN", null, "hat"]'),
         (20, 10000, '[12, 3, 8]', '[0, 1]', '[0, 1]', 'klitze', 'klitze^4', 'klitz', 'e', 4,
 5, None, 'ADJA', '["neutral", 0.0]', None, None, None, None, None, None, None, None,
 'eine', '["ART", null, "ein"]', 'kleine', '["ADJA", null, "klein"]', 'überaschung',
 '["NN", null, "uberasch"]', '@schönesleben', '["mention", null, "@schonesleb"]',
 '#machwasdaraus', '["hashtag", null, "#machwasdaraus"]', '#bewegedeinarsch', '["hashtag", null, "#bewegedeinarsch"]'),
         (3, 8888, '[4, 11]', '[0, 2]', '[0, 1]', 'kleine', 'kle^5in^5e', 'klein', 'e', 5, 2,
 '[0, 1]', 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None,
 'klitze', '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]',
 '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]',
 'sie', '["PPER", null, "sie"]'),
         (4, 8888, '[4, 11]', '[0, 2]', '[0, 1]', 'kleine', 'kle^5in^5e', 'klein', 'n', 5, 4,
 '[0, 1]', 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None,
 'klitze', '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]',
 '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]',
 'sie', '["PPER", null, "sie"]'),
         (5, 8888, '[4, 11]', '[0, 3]', '[0, 1]', 'kleine', 'klein^3e', 'klein', 'n', 3, 4,
 '[0, 1]', 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None,
 'klitze', '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]',
 '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]',
 'sie', '["PPER", null, "sie"]'),
         (21, 10000, '[12, 3, 8]', '[0, 2]', '[0, 2]', 'kleine', 'kle^5ine', 'klein', 'e', 5,
 2, None, 'ADJA', '["neutral", 0.0]', None, None, None, None, None, None, 'eine',
 '["ART", null, "ein"]', 'klitze', '["ADJA", null, "klitz"]', 'überaschung', '["NN", null, "uberasch"]',
 '@schönesleben', '["mention", null, "@schonesleb"]', '#machwasdaraus', '["hashtag", null, "#machwasdaraus"]',
 '#bewegedeinarsch', '["hashtag", null, "#bewegedeinarsch"]', 'https://www.freiesinternet.de',
 '["URL", null, "https://www.freiesinternet.d"]')]
        right_syntagma = [
         'klitze', 'kleine']
        right_baseline = [
         [
          [
           'klitze', 'kleine'], 'klitz++klein', 2, 4, '[2, 3]', '[3, 4]', '[1, 1]', '[2, 2]', '2', '1']]
        right_redu = [
         (1, 8888, '[4, 11]', '[0, 0]', '[0, 0]', 'klitze', 'klitz', '{"klitze": 1, "kli^4tze^7": 1}',
 2, 'NN', '["neutral", 0.0]', None, None, None, None, None, None, None, None, None,
 None, 'kleine', '["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', 'überaschung',
 '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]',
 'hat', '["VAFIN", null, "hat"]'),
         (2, 8888, '[4, 11]', '[0, 2]', '[0, 1]', 'kleine', 'klein', '{"kle^5in^5e": 1, "klein^3e": 1}',
 2, 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze',
 '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]',
 '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]',
 'sie', '["PPER", null, "sie"]')]
        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list(tuple(unicode(elem) for elem in item) for item in extracted_baseline)).should.be.equal(set(list(tuple(unicode(elem) for elem in item) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)
        syntagma = [
         'klitz', 'klein']
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='lexem', stemmed_search=True)
        extracted_repl = item['repl']
        extracted_redu = item['redu']
        extracted_baseline = item['baseline']
        extracted_syntagma = item['syntagma']
        right_repl = [
         (1, 8888, '[4, 11]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze^7', 'klitz', 'i', 4, 2,
 '[0, 0]', 'NN', '["neutral", 0.0]', None, None, None, None, None, None, None, None,
 None, None, 'kleine', '["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', 'überaschung',
 '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]',
 'hat', '["VAFIN", null, "hat"]'),
         (2, 8888, '[4, 11]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze^7', 'klitz', 'e', 7, 5,
 '[0, 0]', 'NN', '["neutral", 0.0]', None, None, None, None, None, None, None, None,
 None, None, 'kleine', '["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', 'überaschung',
 '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]',
 'hat', '["VAFIN", null, "hat"]'),
         (20, 10000, '[12, 3, 8]', '[0, 1]', '[0, 1]', 'klitze', 'klitze^4', 'klitz', 'e', 4,
 5, None, 'ADJA', '["neutral", 0.0]', None, None, None, None, None, None, None, None,
 'eine', '["ART", null, "ein"]', 'kleine', '["ADJA", null, "klein"]', 'überaschung',
 '["NN", null, "uberasch"]', '@schönesleben', '["mention", null, "@schonesleb"]',
 '#machwasdaraus', '["hashtag", null, "#machwasdaraus"]', '#bewegedeinarsch', '["hashtag", null, "#bewegedeinarsch"]'),
         (42, 10000, '[12, 3, 8]', '[2, 5]', '[2, 3]', 'klitz', 'kli^4tz', 'klitz', 'i', 4,
 2, '[2, 3]', 'NE', '["neutral", 0.0]', 'mädchen', '["NN", null, "madch"]', '.',
 '["symbol", null, "."]', 'kleinere', '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]',
 'auswahl', '["NN", null, "auswahl"]', '.', '["symbol", null, "."]', 'klein', '["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]',
 '.', '["symbol", null, "."]', 'klitzes', '["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]',
 'kleines', '["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None),
         (43, 10000, '[12, 3, 8]', '[2, 6]', '[2, 3]', 'klitz', 'kli^4tz^3', 'klitz', 'i', 4,
 2, '[2, 3]', 'NE', '["neutral", 0.0]', 'mädchen', '["NN", null, "madch"]', '.',
 '["symbol", null, "."]', 'kleinere', '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]',
 'auswahl', '["NN", null, "auswahl"]', '.', '["symbol", null, "."]', 'klein', '["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]',
 '.', '["symbol", null, "."]', 'klitzes', '["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]',
 'kleines', '["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None),
         (44, 10000, '[12, 3, 8]', '[2, 6]', '[2, 3]', 'klitz', 'kli^4tz^3', 'klitz', 'z', 3,
 4, '[2, 3]', 'NE', '["neutral", 0.0]', 'mädchen', '["NN", null, "madch"]', '.',
 '["symbol", null, "."]', 'kleinere', '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]',
 'auswahl', '["NN", null, "auswahl"]', '.', '["symbol", null, "."]', 'klein', '["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]',
 '.', '["symbol", null, "."]', 'klitzes', '["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]',
 'kleines', '["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None),
         (49, 10000, '[12, 3, 8]', '[2, 10]', '[2, 6]', 'klitzes', 'klitzes^4', 'klitz', 's',
 4, 6, '[2, 6]', 'FM', '["neutral", 0.0]', 'auswahl', '["NN", null, "auswahl"]',
 '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]',
 'klein', '["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', '.', '["symbol", null, "."]',
 'kleines', '["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None,
 None, None, None, None, None),
         (50, 10000, '[12, 3, 8]', '[2, 11]', '[2, 6]', 'klitzes', 'kli^3tzes^3', 'klitz', 'i',
 3, 2, '[2, 6]', 'FM', '["neutral", 0.0]', 'auswahl', '["NN", null, "auswahl"]',
 '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]',
 'klein', '["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', '.', '["symbol", null, "."]',
 'kleines', '["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None,
 None, None, None, None, None),
         (51, 10000, '[12, 3, 8]', '[2, 11]', '[2, 6]', 'klitzes', 'kli^3tzes^3', 'klitz', 's',
 3, 6, '[2, 6]', 'FM', '["neutral", 0.0]', 'auswahl', '["NN", null, "auswahl"]',
 '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]',
 'klein', '["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', '.', '["symbol", null, "."]',
 'kleines', '["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None,
 None, None, None, None, None),
         (3, 8888, '[4, 11]', '[0, 2]', '[0, 1]', 'kleine', 'kle^5in^5e', 'klein', 'e', 5, 2,
 '[0, 1]', 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None,
 'klitze', '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]',
 '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]',
 'sie', '["PPER", null, "sie"]'),
         (4, 8888, '[4, 11]', '[0, 2]', '[0, 1]', 'kleine', 'kle^5in^5e', 'klein', 'n', 5, 4,
 '[0, 1]', 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None,
 'klitze', '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]',
 '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]',
 'sie', '["PPER", null, "sie"]'),
         (5, 8888, '[4, 11]', '[0, 3]', '[0, 1]', 'kleine', 'klein^3e', 'klein', 'n', 3, 4,
 '[0, 1]', 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None,
 'klitze', '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]',
 '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]',
 'sie', '["PPER", null, "sie"]'),
         (21, 10000, '[12, 3, 8]', '[0, 2]', '[0, 2]', 'kleine', 'kle^5ine', 'klein', 'e', 5,
 2, None, 'ADJA', '["neutral", 0.0]', None, None, None, None, None, None, 'eine',
 '["ART", null, "ein"]', 'klitze', '["ADJA", null, "klitz"]', 'überaschung', '["NN", null, "uberasch"]',
 '@schönesleben', '["mention", null, "@schonesleb"]', '#machwasdaraus', '["hashtag", null, "#machwasdaraus"]',
 '#bewegedeinarsch', '["hashtag", null, "#bewegedeinarsch"]', 'https://www.freiesinternet.de',
 '["URL", null, "https://www.freiesinternet.d"]'),
         (45, 10000, '[12, 3, 8]', '[2, 7]', '[2, 4]', 'klein', 'kle^3i^3n^3', 'klein', 'e',
 3, 2, '[2, 4]', 'FM', '["neutral", 0.0]', '.', '["symbol", null, "."]', 'kleinere',
 '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', 'auswahl', '["NN", null, "auswahl"]',
 '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]',
 '.', '["symbol", null, "."]', 'klitzes', '["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]',
 'kleines', '["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None,
 None),
         (46, 10000, '[12, 3, 8]', '[2, 7]', '[2, 4]', 'klein', 'kle^3i^3n^3', 'klein', 'i',
 3, 3, '[2, 4]', 'FM', '["neutral", 0.0]', '.', '["symbol", null, "."]', 'kleinere',
 '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', 'auswahl', '["NN", null, "auswahl"]',
 '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]',
 '.', '["symbol", null, "."]', 'klitzes', '["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]',
 'kleines', '["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None,
 None),
         (47, 10000, '[12, 3, 8]', '[2, 7]', '[2, 4]', 'klein', 'kle^3i^3n^3', 'klein', 'n',
 3, 4, '[2, 4]', 'FM', '["neutral", 0.0]', '.', '["symbol", null, "."]', 'kleinere',
 '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', 'auswahl', '["NN", null, "auswahl"]',
 '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]',
 '.', '["symbol", null, "."]', 'klitzes', '["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]',
 'kleines', '["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None,
 None),
         (48, 10000, '[12, 3, 8]', '[2, 8]', '[2, 4]', 'klein', 'klein^5', 'klein', 'n', 5,
 4, '[2, 4]', 'FM', '["neutral", 0.0]', '.', '["symbol", null, "."]', 'kleinere',
 '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', 'auswahl', '["NN", null, "auswahl"]',
 '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]',
 '.', '["symbol", null, "."]', 'klitzes', '["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]',
 'kleines', '["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None,
 None),
         (52, 10000, '[12, 3, 8]', '[2, 12]', '[2, 7]', 'kleines', 'klein^3e^2s', 'klein', 'n',
 3, 4, '[2, 7]', 'FM', '["neutral", 0.0]', '.', '["symbol", null, "."]', 'klitz',
 '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', 'klein', '["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]',
 '.', '["symbol", null, "."]', 'klitzes', '["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]',
 None, None, None, None, None, None, None, None, None, None),
         (53, 10000, '[12, 3, 8]', '[2, 13]', '[2, 7]', 'kleines', 'kleines^4', 'klein', 's',
 4, 6, '[2, 7]', 'FM', '["neutral", 0.0]', '.', '["symbol", null, "."]', 'klitz',
 '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', 'klein', '["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]',
 '.', '["symbol", null, "."]', 'klitzes', '["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]',
 None, None, None, None, None, None, None, None, None, None)]
        right_syntagma = [
         'klitz', 'klein']
        right_baseline = [
         [
          [
           'klitzes', 'kleines'], 'klitz++klein', 2, 1, '[2, 2]', '[3, 2]', '[1, 1]', '[2, 2]', '1', '1'], [['klitz', 'klein'], 'klitz++klein', 2, 1, '[2, 2]', '[3, 4]', '[1, 1]', '[3, 2]', '1', '1'], [['klitze', 'kleine'], 'klitz++klein', 2, 4, '[2, 3]', '[3, 4]', '[1, 1]', '[2, 2]', '2', '1']]
        right_redu = [
         (1, 8888, '[4, 11]', '[0, 0]', '[0, 0]', 'klitze', 'klitz', '{"klitze": 1, "kli^4tze^7": 1}',
 2, 'NN', '["neutral", 0.0]', None, None, None, None, None, None, None, None, None,
 None, 'kleine', '["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', 'überaschung',
 '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]',
 'hat', '["VAFIN", null, "hat"]'),
         (13, 10000, '[12, 3, 8]', '[2, 4]', '[2, 3]', 'klitz', 'klitz', '{"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}',
 3, 'NE', '["neutral", 0.0]', 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]',
 'kleinere', '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', 'auswahl',
 '["NN", null, "auswahl"]', '.', '["symbol", null, "."]', 'klein', '["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]',
 '.', '["symbol", null, "."]', 'klitzes', '["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]',
 'kleines', '["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None),
         (15, 10000, '[12, 3, 8]', '[2, 10]', '[2, 6]', 'klitzes', 'klitz', '{"klitzes^4": 1, "kli^3tzes^3": 1}',
 2, 'FM', '["neutral", 0.0]', 'auswahl', '["NN", null, "auswahl"]', '.', '["symbol", null, "."]',
 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', 'klein',
 '["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', '.', '["symbol", null, "."]',
 'kleines', '["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None,
 None, None, None, None, None),
         (2, 8888, '[4, 11]', '[0, 2]', '[0, 1]', 'kleine', 'klein', '{"kle^5in^5e": 1, "klein^3e": 1}',
 2, 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze',
 '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]',
 '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]',
 'sie', '["PPER", null, "sie"]'),
         (14, 10000, '[12, 3, 8]', '[2, 7]', '[2, 4]', 'klein', 'klein', '{"kle^3i^3n^3": 1, "klein^5": 1}',
 2, 'FM', '["neutral", 0.0]', '.', '["symbol", null, "."]', 'kleinere', '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]',
 'auswahl', '["NN", null, "auswahl"]', '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]',
 '.', '["symbol", null, "."]', 'klitzes', '["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]',
 'kleines', '["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None,
 None),
         (16, 10000, '[12, 3, 8]', '[2, 12]', '[2, 7]', 'kleines', 'klein', '{"klein^3e^2s": 1, "kleines^4": 1}',
 2, 'FM', '["neutral", 0.0]', '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]',
 'klein', '["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', '.', '["symbol", null, "."]',
 'klitzes', '["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', None, None, None,
 None, None, None, None, None, None, None)]
        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list(tuple(unicode(elem) for elem in item) for item in extracted_baseline)).should.be.equal(set(list(tuple(unicode(elem) for elem in item) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)
        syntagma = [
         '.', 'kleinere', 'auswahl']
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='lexem', stemmed_search=False, get_also_non_full_repetativ_result=True)
        right_repl = [
         (36, 10000, '[12, 3, 8]', '[1, 4]', '[1, 2]', '.', '.^5', '.', '.', 5, 0, None, 'symbol',
 '["neutral", 0.0]', 'kan', '["FM", {"ka^4n^5": 1, "kan^6": 1}, "kan"]', 'es', '["VVFIN", null, "es"]',
 '.', '["symbol", null, "."]', 'kleines', '["NN", {"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}, "klein"]',
 'mädchen', '["NN", null, "madch"]', 'kleinere', '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]',
 'auswahl', '["NN", null, "auswahl"]', '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]',
 'klein', '["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]'),
         (37, 10000, '[12, 3, 8]', '[2, 0]', '[2, 0]', 'kleinere', 'kleinere^5', 'klein', 'e',
 5, 7, '[2, 0]', 'NE', '["neutral", 0.0]', 'es', '["VVFIN", null, "es"]', '.', '["symbol", null, "."]',
 'kleines', '["NN", {"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}, "klein"]',
 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', 'auswahl', '["NN", null, "auswahl"]',
 '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]',
 'klein', '["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', '.', '["symbol", null, "."]'),
         (38, 10000, '[12, 3, 8]', '[2, 1]', '[2, 0]', 'kleinere', 'kleine^3r^2e^5', 'klein',
 'e', 3, 5, '[2, 0]', 'NE', '["neutral", 0.0]', 'es', '["VVFIN", null, "es"]', '.',
 '["symbol", null, "."]', 'kleines', '["NN", {"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}, "klein"]',
 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', 'auswahl', '["NN", null, "auswahl"]',
 '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]',
 'klein', '["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', '.', '["symbol", null, "."]'),
         (39, 10000, '[12, 3, 8]', '[2, 1]', '[2, 0]', 'kleinere', 'kleine^3r^2e^5', 'klein',
 'e', 5, 7, '[2, 0]', 'NE', '["neutral", 0.0]', 'es', '["VVFIN", null, "es"]', '.',
 '["symbol", null, "."]', 'kleines', '["NN", {"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}, "klein"]',
 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', 'auswahl', '["NN", null, "auswahl"]',
 '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]',
 'klein', '["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', '.', '["symbol", null, "."]'),
         (40, 10000, '[12, 3, 8]', '[2, 2]', '[2, 1]', 'auswahl', 'auswah^3l^4', 'auswahl',
 'h', 3, 5, None, 'NN', '["neutral", 0.0]', '.', '["symbol", null, "."]', 'kleines',
 '["NN", {"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}, "klein"]',
 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', 'kleinere', '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]',
 '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]',
 'klein', '["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', '.', '["symbol", null, "."]',
 'klitzes', '["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]'),
         (41, 10000, '[12, 3, 8]', '[2, 2]', '[2, 1]', 'auswahl', 'auswah^3l^4', 'auswahl',
 'l', 4, 6, None, 'NN', '["neutral", 0.0]', '.', '["symbol", null, "."]', 'kleines',
 '["NN", {"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}, "klein"]',
 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', 'kleinere', '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]',
 '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]',
 'klein', '["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', '.', '["symbol", null, "."]',
 'klitzes', '["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]')]
        right_syntagma = [
         '.', 'kleinere', 'auswahl']
        right_baseline = [
         [
          [
           '.', 'kleinere', 'auswahl'], '.++klein++auswahl', 3, 1, '[1, 2, 1]', '[1, 3, 2]', None, None, '1', None]]
        right_redu = [
         (12, 10000, '[12, 3, 8]', '[2, 0]', '[2, 0]', 'kleinere', 'klein', '{"kleinere^5": 1, "kleine^3r^2e^5": 1}',
 2, 'NE', '["neutral", 0.0]', 'es', '["VVFIN", null, "es"]', '.', '["symbol", null, "."]',
 'kleines', '["NN", {"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}, "klein"]',
 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', 'auswahl', '["NN", null, "auswahl"]',
 '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]',
 'klein', '["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', '.', '["symbol", null, "."]')]
        extracted_repl = item['repl']
        extracted_redu = item['redu']
        extracted_baseline = item['baseline']
        extracted_syntagma = item['syntagma']
        syntagma = [
         'klitze']
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='lexem', return_full_tuple=True)
        extracted_repl = item['repl']
        extracted_redu = item['redu']
        extracted_baseline = item['baseline']
        extracted_syntagma = item['syntagma']
        right_repl = (
         [
          (54, 11111, '[5, 6, 15, 3]', '[0, 1]', '[0, 1]', 'klitze', 'klitze^4', 'klitz', 'e',
 4, 5, None, 'VAPPER', '["neutral", 0.0]', None, None, None, None, None, None, None,
 None, 'eine', '["ART", null, "ein"]', 'kleine', '["ADJA", null, "klein"]', 'sache',
 '["NN", null, "sach"]', '.', '["symbol", null, "."]', 'die', '["PDS", null, "die"]',
 'aber', '["ADV", null, "aber"]'),
          (1, 8888, '[4, 11]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze^7', 'klitz', 'i', 4, 2,
 '[0, 0]', 'NN', '["neutral", 0.0]', None, None, None, None, None, None, None, None,
 None, None, 'kleine', '["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', 'überaschung',
 '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]',
 'hat', '["VAFIN", null, "hat"]'),
          (2, 8888, '[4, 11]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze^7', 'klitz', 'e', 7, 5,
 '[0, 0]', 'NN', '["neutral", 0.0]', None, None, None, None, None, None, None, None,
 None, None, 'kleine', '["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', 'überaschung',
 '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]',
 'hat', '["VAFIN", null, "hat"]'),
          (20, 10000, '[12, 3, 8]', '[0, 1]', '[0, 1]', 'klitze', 'klitze^4', 'klitz', 'e', 4,
 5, None, 'ADJA', '["neutral", 0.0]', None, None, None, None, None, None, None, None,
 'eine', '["ART", null, "ein"]', 'kleine', '["ADJA", null, "klein"]', 'überaschung',
 '["NN", null, "uberasch"]', '@schönesleben', '["mention", null, "@schonesleb"]',
 '#machwasdaraus', '["hashtag", null, "#machwasdaraus"]', '#bewegedeinarsch', '["hashtag", null, "#bewegedeinarsch"]')],
         True,
         None)
        right_syntagma = [
         'klitze']
        right_baseline = [
         [
          [
           'klitze'], 'klitz', 1, 8, '3', '4', '2', '6', '3', '2']]
        right_redu = (
         [
          (18, 12222, '[24]', '[0, 1]', '[0, 1]', 'klitze', 'klitz', '{"klitze": 4}', 4, 'NN',
 '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'eine', '["ART", null, "ein"]',
 'kleine', '["ADJA", null, "klein"]', 'überaschung', '["NN", null, "uberasch"]',
 ',', '["symbol", null, ","]', 'die', '["PRELS", null, "die"]', 'ich', '["PPER", null, "ich"]'),
          (1, 8888, '[4, 11]', '[0, 0]', '[0, 0]', 'klitze', 'klitz', '{"klitze": 1, "kli^4tze^7": 1}',
 2, 'NN', '["neutral", 0.0]', None, None, None, None, None, None, None, None, None,
 None, 'kleine', '["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', 'überaschung',
 '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]',
 'hat', '["VAFIN", null, "hat"]')],
         True,
         None)
        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list(tuple(unicode(elem) for elem in item) for item in extracted_baseline)).should.be.equal(set(list(tuple(unicode(elem) for elem in item) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)
        syntagma = [
         'klitze', 'kleine']
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='lexem', return_full_tuple=True)
        extracted_repl = item['repl']
        extracted_redu = item['redu']
        extracted_baseline = item['baseline']
        extracted_syntagma = item['syntagma']
        right_repl = (
         [
          (1, 8888, '[4, 11]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze^7', 'klitz', 'i', 4, 2,
 '[0, 0]', 'NN', '["neutral", 0.0]', None, None, None, None, None, None, None, None,
 None, None, 'kleine', '["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', 'überaschung',
 '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]',
 'hat', '["VAFIN", null, "hat"]'),
          (2, 8888, '[4, 11]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze^7', 'klitz', 'e', 7, 5,
 '[0, 0]', 'NN', '["neutral", 0.0]', None, None, None, None, None, None, None, None,
 None, None, 'kleine', '["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', 'überaschung',
 '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]',
 'hat', '["VAFIN", null, "hat"]'),
          (20, 10000, '[12, 3, 8]', '[0, 1]', '[0, 1]', 'klitze', 'klitze^4', 'klitz', 'e', 4,
 5, None, 'ADJA', '["neutral", 0.0]', None, None, None, None, None, None, None, None,
 'eine', '["ART", null, "ein"]', 'kleine', '["ADJA", null, "klein"]', 'überaschung',
 '["NN", null, "uberasch"]', '@schönesleben', '["mention", null, "@schonesleb"]',
 '#machwasdaraus', '["hashtag", null, "#machwasdaraus"]', '#bewegedeinarsch', '["hashtag", null, "#bewegedeinarsch"]'),
          (3, 8888, '[4, 11]', '[0, 2]', '[0, 1]', 'kleine', 'kle^5in^5e', 'klein', 'e', 5, 2,
 '[0, 1]', 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None,
 'klitze', '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]',
 '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]',
 'sie', '["PPER", null, "sie"]'),
          (4, 8888, '[4, 11]', '[0, 2]', '[0, 1]', 'kleine', 'kle^5in^5e', 'klein', 'n', 5, 4,
 '[0, 1]', 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None,
 'klitze', '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]',
 '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]',
 'sie', '["PPER", null, "sie"]'),
          (5, 8888, '[4, 11]', '[0, 3]', '[0, 1]', 'kleine', 'klein^3e', 'klein', 'n', 3, 4,
 '[0, 1]', 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None,
 'klitze', '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]',
 '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]',
 'sie', '["PPER", null, "sie"]'),
          (21, 10000, '[12, 3, 8]', '[0, 2]', '[0, 2]', 'kleine', 'kle^5ine', 'klein', 'e', 5,
 2, None, 'ADJA', '["neutral", 0.0]', None, None, None, None, None, None, 'eine',
 '["ART", null, "ein"]', 'klitze', '["ADJA", null, "klitz"]', 'überaschung', '["NN", null, "uberasch"]',
 '@schönesleben', '["mention", null, "@schonesleb"]', '#machwasdaraus', '["hashtag", null, "#machwasdaraus"]',
 '#bewegedeinarsch', '["hashtag", null, "#bewegedeinarsch"]', 'https://www.freiesinternet.de',
 '["URL", null, "https://www.freiesinternet.d"]')],
         True,
         2)
        right_syntagma = [
         'klitze', 'kleine']
        right_baseline = [
         [
          [
           'klitze', 'kleine'], 'klitz++klein', 2, 4, '[2, 3]', '[3, 4]', '[1, 1]', '[2, 2]', '2', '1']]
        right_redu = (
         [
          (1, 8888, '[4, 11]', '[0, 0]', '[0, 0]', 'klitze', 'klitz', '{"klitze": 1, "kli^4tze^7": 1}',
 2, 'NN', '["neutral", 0.0]', None, None, None, None, None, None, None, None, None,
 None, 'kleine', '["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', 'überaschung',
 '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]',
 'hat', '["VAFIN", null, "hat"]'),
          (2, 8888, '[4, 11]', '[0, 2]', '[0, 1]', 'kleine', 'klein', '{"kle^5in^5e": 1, "klein^3e": 1}',
 2, 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze',
 '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]',
 '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]',
 'sie', '["PPER", null, "sie"]')],
         True,
         1)
        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list(tuple(unicode(elem) for elem in item) for item in extracted_baseline)).should.be.equal(set(list(tuple(unicode(elem) for elem in item) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)
        stats.recompute_syntagma_repetativity_scope(False)
        syntagma = [
         'klitze', 'kleine']
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='lexem')
        extracted_repl = item['repl']
        extracted_redu = item['redu']
        extracted_baseline = item['baseline']
        extracted_syntagma = item['syntagma']
        right_repl = [
         (54, 11111, '[5, 6, 15, 3]', '[0, 1]', '[0, 1]', 'klitze', 'klitze^4', 'klitz', 'e',
 4, 5, None, 'VAPPER', '["neutral", 0.0]', None, None, None, None, None, None, None,
 None, 'eine', '["ART", null, "ein"]', 'kleine', '["ADJA", null, "klein"]', 'sache',
 '["NN", null, "sach"]', '.', '["symbol", null, "."]', 'die', '["PDS", null, "die"]',
 'aber', '["ADV", null, "aber"]'),
         (1, 8888, '[4, 11]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze^7', 'klitz', 'i', 4, 2,
 '[0, 0]', 'NN', '["neutral", 0.0]', None, None, None, None, None, None, None, None,
 None, None, 'kleine', '["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', 'überaschung',
 '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]',
 'hat', '["VAFIN", null, "hat"]'),
         (2, 8888, '[4, 11]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze^7', 'klitz', 'e', 7, 5,
 '[0, 0]', 'NN', '["neutral", 0.0]', None, None, None, None, None, None, None, None,
 None, None, 'kleine', '["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', 'überaschung',
 '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]',
 'hat', '["VAFIN", null, "hat"]'),
         (20, 10000, '[12, 3, 8]', '[0, 1]', '[0, 1]', 'klitze', 'klitze^4', 'klitz', 'e', 4,
 5, None, 'ADJA', '["neutral", 0.0]', None, None, None, None, None, None, None, None,
 'eine', '["ART", null, "ein"]', 'kleine', '["ADJA", null, "klein"]', 'überaschung',
 '["NN", null, "uberasch"]', '@schönesleben', '["mention", null, "@schonesleb"]',
 '#machwasdaraus', '["hashtag", null, "#machwasdaraus"]', '#bewegedeinarsch', '["hashtag", null, "#bewegedeinarsch"]'),
         (3, 8888, '[4, 11]', '[0, 2]', '[0, 1]', 'kleine', 'kle^5in^5e', 'klein', 'e', 5, 2,
 '[0, 1]', 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None,
 'klitze', '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]',
 '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]',
 'sie', '["PPER", null, "sie"]'),
         (4, 8888, '[4, 11]', '[0, 2]', '[0, 1]', 'kleine', 'kle^5in^5e', 'klein', 'n', 5, 4,
 '[0, 1]', 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None,
 'klitze', '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]',
 '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]',
 'sie', '["PPER", null, "sie"]'),
         (5, 8888, '[4, 11]', '[0, 3]', '[0, 1]', 'kleine', 'klein^3e', 'klein', 'n', 3, 4,
 '[0, 1]', 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None,
 'klitze', '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]',
 '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]',
 'sie', '["PPER", null, "sie"]'),
         (21, 10000, '[12, 3, 8]', '[0, 2]', '[0, 2]', 'kleine', 'kle^5ine', 'klein', 'e', 5,
 2, None, 'ADJA', '["neutral", 0.0]', None, None, None, None, None, None, 'eine',
 '["ART", null, "ein"]', 'klitze', '["ADJA", null, "klitz"]', 'überaschung', '["NN", null, "uberasch"]',
 '@schönesleben', '["mention", null, "@schonesleb"]', '#machwasdaraus', '["hashtag", null, "#machwasdaraus"]',
 '#bewegedeinarsch', '["hashtag", null, "#bewegedeinarsch"]', 'https://www.freiesinternet.de',
 '["URL", null, "https://www.freiesinternet.d"]')]
        right_syntagma = [
         'klitze', 'kleine']
        right_baseline = [
         [
          [
           'klitze', 'kleine'], 'klitz++klein', 2, 4, '[3, 3]', '[4, 4]', '[2, 1]', '[6, 2]', None, None]]
        right_redu = [
         (18, 12222, '[24]', '[0, 1]', '[0, 1]', 'klitze', 'klitz', '{"klitze": 4}', 4, 'NN',
 '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'eine', '["ART", null, "ein"]',
 'kleine', '["ADJA", null, "klein"]', 'überaschung', '["NN", null, "uberasch"]',
 ',', '["symbol", null, ","]', 'die', '["PRELS", null, "die"]', 'ich', '["PPER", null, "ich"]'),
         (1, 8888, '[4, 11]', '[0, 0]', '[0, 0]', 'klitze', 'klitz', '{"klitze": 1, "kli^4tze^7": 1}',
 2, 'NN', '["neutral", 0.0]', None, None, None, None, None, None, None, None, None,
 None, 'kleine', '["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', 'überaschung',
 '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]',
 'hat', '["VAFIN", null, "hat"]'),
         (2, 8888, '[4, 11]', '[0, 2]', '[0, 1]', 'kleine', 'klein', '{"kle^5in^5e": 1, "klein^3e": 1}',
 2, 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze',
 '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]',
 '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]',
 'sie', '["PPER", null, "sie"]')]
        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list(tuple(unicode(elem) for elem in item) for item in extracted_baseline)).should.be.equal(set(list(tuple(unicode(elem) for elem in item) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)
        return

    @attr(status='stable')
    def test_get_data_611_2(self):
        self.prj_folder()
        self.test_dbs()
        stats = Stats(mode=self.mode, use_cash=True, status_bar=True)
        stats.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_stats_en))
        syntagma = [
         'EMOIMG', 'EMOIMG']
        data1 = list(stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='pos', order_output_by_syntagma_order=False, if_type_pos_return_lexem_syn=False))
        repl1 = sorted(data1[0]['repl'])
        redu1 = sorted(data1[0]['redu'])
        data2 = list(stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='pos', order_output_by_syntagma_order=False, if_type_pos_return_lexem_syn=True))
        ext_id = []
        repl2 = []
        for item in data2:
            for r in item['repl']:
                if r[0] not in ext_id:
                    ext_id.append(r[0])
                    repl2.append(r)

        ext_id = []
        redu2 = []
        for item in data2:
            for r in item['redu']:
                if r[0] not in ext_id:
                    ext_id.append(r[0])
                    redu2.append(r)

        assert len(repl1) <= len(repl2)
        assert len(redu1) <= len(redu2)
        stats.close()
        stats.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_stats_de))
        stats.recompute_syntagma_repetativity_scope(True)
        syntagma = [
         'big']
        data = list(stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='lexem'))
        data.should.be.equal([])
        syntagma = [
         'kleine']
        data = stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='lexem')
        len1 = len(data)
        data = list(data)
        len2 = len(data)
        len1.should.be.equal(len2)
        extracted_repl = data[0]['repl']
        extracted_redu = data[0]['redu']
        extracted_baseline = data[0]['baseline']
        extracted_syntagma = data[0]['syntagma']
        right_repl = [
         (
          82, 12222, '[24]', '[0, 24]', '[0, 21]', 'kleine', 'kle^4i^5n^4e^8', 'klein', 'e', 4, 2, None, 'ADJA', '["neutral", 0.0]', ',', '["symbol", null, ","]', 'es', '["PPER", null, "es"]', 'war', '["VAFIN", null, "war"]', 'so', '["ADV", null, "so"]', 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', None, None, None, None, None, None),
         (
          83, 12222, '[24]', '[0, 24]', '[0, 21]', 'kleine', 'kle^4i^5n^4e^8', 'klein', 'i', 5, 3, None, 'ADJA', '["neutral", 0.0]', ',', '["symbol", null, ","]', 'es', '["PPER", null, "es"]', 'war', '["VAFIN", null, "war"]', 'so', '["ADV", null, "so"]', 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', None, None, None, None, None, None),
         (
          84, 12222, '[24]', '[0, 24]', '[0, 21]', 'kleine', 'kle^4i^5n^4e^8', 'klein', 'n', 4, 4, None, 'ADJA', '["neutral", 0.0]', ',', '["symbol", null, ","]', 'es', '["PPER", null, "es"]', 'war', '["VAFIN", null, "war"]', 'so', '["ADV", null, "so"]', 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', None, None, None, None, None, None),
         (
          85, 12222, '[24]', '[0, 24]', '[0, 21]', 'kleine', 'kle^4i^5n^4e^8', 'klein', 'e', 8, 5, None, 'ADJA', '["neutral", 0.0]', ',', '["symbol", null, ","]', 'es', '["PPER", null, "es"]', 'war', '["VAFIN", null, "war"]', 'so', '["ADV", null, "so"]', 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', None, None, None, None, None, None),
         (
          3, 8888, '[4, 11]', '[0, 2]', '[0, 1]', 'kleine', 'kle^5in^5e', 'klein', 'e', 5, 2, '[0, 1]', 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]', 'sie', '["PPER", null, "sie"]'),
         (
          4, 8888, '[4, 11]', '[0, 2]', '[0, 1]', 'kleine', 'kle^5in^5e', 'klein', 'n', 5, 4, '[0, 1]', 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]', 'sie', '["PPER", null, "sie"]'),
         (
          5, 8888, '[4, 11]', '[0, 3]', '[0, 1]', 'kleine', 'klein^3e', 'klein', 'n', 3, 4, '[0, 1]', 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]', 'sie', '["PPER", null, "sie"]'),
         (
          21, 10000, '[12, 3, 8]', '[0, 2]', '[0, 2]', 'kleine', 'kle^5ine', 'klein', 'e', 5, 2, None, 'ADJA', '["neutral", 0.0]', None, None, None, None, None, None, 'eine', '["ART", null, "ein"]', 'klitze', '["ADJA", null, "klitz"]', 'überaschung', '["NN", null, "uberasch"]', '@schönesleben', '["mention", null, "@schonesleb"]', '#machwasdaraus', '["hashtag", null, "#machwasdaraus"]', '#bewegedeinarsch', '["hashtag", null, "#bewegedeinarsch"]', 'https://www.freiesinternet.de', '["URL", null, "https://www.freiesinternet.d"]'),
         (
          57, 11111, '[5, 6, 15, 3]', '[2, 4]', '[2, 4]', 'kleine', 'kle^5i^2n^4e^5', 'klein', 'e', 5, 2, None, 'ADJA', '["neutral", 0.0]', '!', '["symbol", null, "!"]', 'weil', '["KOUS", null, "weil"]', 'es', '["PPER", null, "es"]', 'ja', '["PTKMA", null, "ja"]', 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', 'ist', '["VAFIN", null, "ist"]', '.', '["symbol", null, "."]', 1, '["number", null, "1"]', 2, '["number", null, "2"]'),
         (
          58, 11111, '[5, 6, 15, 3]', '[2, 4]', '[2, 4]', 'kleine', 'kle^5i^2n^4e^5', 'klein', 'n', 4, 4, None, 'ADJA', '["neutral", 0.0]', '!', '["symbol", null, "!"]', 'weil', '["KOUS", null, "weil"]', 'es', '["PPER", null, "es"]', 'ja', '["PTKMA", null, "ja"]', 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', 'ist', '["VAFIN", null, "ist"]', '.', '["symbol", null, "."]', 1, '["number", null, "1"]', 2, '["number", null, "2"]'),
         (
          59, 11111, '[5, 6, 15, 3]', '[2, 4]', '[2, 4]', 'kleine', 'kle^5i^2n^4e^5', 'klein', 'e', 5, 5, None, 'ADJA', '["neutral", 0.0]', '!', '["symbol", null, "!"]', 'weil', '["KOUS", null, "weil"]', 'es', '["PPER", null, "es"]', 'ja', '["PTKMA", null, "ja"]', 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', 'ist', '["VAFIN", null, "ist"]', '.', '["symbol", null, "."]', 1, '["number", null, "1"]', 2, '["number", null, "2"]')]
        right_syntagma = [
         'kleine']
        right_baseline = [
         [
          [
           'kleine'], 'klein', 1, 7, '5', '11', '1', '2', '5', '1']]
        right_redu = [
         (
          2, 8888, '[4, 11]', '[0, 2]', '[0, 1]', 'kleine', 'klein', '{"kle^5in^5e": 1, "klein^3e": 1}', 2, 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]', 'sie', '["PPER", null, "sie"]')]
        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list(tuple(unicode(elem) for elem in item) for item in extracted_baseline)).should.be.equal(set(list(tuple(unicode(elem) for elem in item) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)
        columns_repl = [
         'doc_id', 'redufree_len', 'index_in_redufree', 'index_in_corpus']
        columns_redu = ['doc_id', 'redufree_len', 'index_in_redufree', 'index_in_corpus', 'redu_length']
        columns_baseline = ['syntagma', 'occur_syntagma_all', 'scope']
        syntagma = [
         'kleine']
        data = list(stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='lexem', get_columns_repl=columns_repl, get_columns_redu=columns_redu, get_columns_baseline=columns_baseline))
        extracted_repl = data[0]['repl']
        extracted_redu = data[0]['redu']
        extracted_baseline = data[0]['baseline']
        extracted_syntagma = data[0]['syntagma']
        right_repl = [
         [
          12222, '[24]', '[0, 21]', '[0, 24]'],
         [
          12222, '[24]', '[0, 21]', '[0, 24]'],
         [
          12222, '[24]', '[0, 21]', '[0, 24]'],
         [
          12222, '[24]', '[0, 21]', '[0, 24]'],
         [
          8888, '[4, 11]', '[0, 1]', '[0, 2]'],
         [
          8888, '[4, 11]', '[0, 1]', '[0, 2]'],
         [
          8888, '[4, 11]', '[0, 1]', '[0, 3]'],
         [
          10000, '[12, 3, 8]', '[0, 2]', '[0, 2]'],
         [
          11111, '[5, 6, 15, 3]', '[2, 4]', '[2, 4]'],
         [
          11111, '[5, 6, 15, 3]', '[2, 4]', '[2, 4]'],
         [
          11111, '[5, 6, 15, 3]', '[2, 4]', '[2, 4]']]
        right_syntagma = [
         'kleine']
        right_baseline = [
         [
          [
           'kleine'], 7, 1]]
        right_redu = [
         [
          8888, '[4, 11]', '[0, 1]', '[0, 2]', 2]]
        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list(tuple(unicode(elem) for elem in item) for item in extracted_baseline)).should.be.equal(set(list(tuple(unicode(elem) for elem in item) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)
        syntagma = [
         'kleine']
        data = list(stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='lexem', order_output_by_syntagma_order=True))
        extracted_repl = data[0]['repl']
        extracted_redu = data[0]['redu']
        extracted_baseline = data[0]['baseline']
        extracted_syntagma = data[0]['syntagma']
        right_repl = [
         (
          'kleine',
          (
           (
            82, 12222, '[24]', '[0, 24]', '[0, 21]', 'kleine', 'kle^4i^5n^4e^8', 'klein', 'e', 4, 2, None, 'ADJA', '["neutral", 0.0]', ',', '["symbol", null, ","]', 'es', '["PPER", null, "es"]', 'war', '["VAFIN", null, "war"]', 'so', '["ADV", null, "so"]', 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', None, None, None, None, None, None),
           (
            83, 12222, '[24]', '[0, 24]', '[0, 21]', 'kleine', 'kle^4i^5n^4e^8', 'klein', 'i', 5, 3, None, 'ADJA', '["neutral", 0.0]', ',', '["symbol", null, ","]', 'es', '["PPER", null, "es"]', 'war', '["VAFIN", null, "war"]', 'so', '["ADV", null, "so"]', 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', None, None, None, None, None, None),
           (
            84, 12222, '[24]', '[0, 24]', '[0, 21]', 'kleine', 'kle^4i^5n^4e^8', 'klein', 'n', 4, 4, None, 'ADJA', '["neutral", 0.0]', ',', '["symbol", null, ","]', 'es', '["PPER", null, "es"]', 'war', '["VAFIN", null, "war"]', 'so', '["ADV", null, "so"]', 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', None, None, None, None, None, None),
           (
            85, 12222, '[24]', '[0, 24]', '[0, 21]', 'kleine', 'kle^4i^5n^4e^8', 'klein', 'e', 8, 5, None, 'ADJA', '["neutral", 0.0]', ',', '["symbol", null, ","]', 'es', '["PPER", null, "es"]', 'war', '["VAFIN", null, "war"]', 'so', '["ADV", null, "so"]', 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', None, None, None, None, None, None),
           (
            3, 8888, '[4, 11]', '[0, 2]', '[0, 1]', 'kleine', 'kle^5in^5e', 'klein', 'e', 5, 2, '[0, 1]', 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]', 'sie', '["PPER", null, "sie"]'),
           (
            4, 8888, '[4, 11]', '[0, 2]', '[0, 1]', 'kleine', 'kle^5in^5e', 'klein', 'n', 5, 4, '[0, 1]', 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]', 'sie', '["PPER", null, "sie"]'),
           (
            5, 8888, '[4, 11]', '[0, 3]', '[0, 1]', 'kleine', 'klein^3e', 'klein', 'n', 3, 4, '[0, 1]', 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]', 'sie', '["PPER", null, "sie"]'),
           (
            21, 10000, '[12, 3, 8]', '[0, 2]', '[0, 2]', 'kleine', 'kle^5ine', 'klein', 'e', 5, 2, None, 'ADJA', '["neutral", 0.0]', None, None, None, None, None, None, 'eine', '["ART", null, "ein"]', 'klitze', '["ADJA", null, "klitz"]', 'überaschung', '["NN", null, "uberasch"]', '@schönesleben', '["mention", null, "@schonesleb"]', '#machwasdaraus', '["hashtag", null, "#machwasdaraus"]', '#bewegedeinarsch', '["hashtag", null, "#bewegedeinarsch"]', 'https://www.freiesinternet.de', '["URL", null, "https://www.freiesinternet.d"]'),
           (
            57, 11111, '[5, 6, 15, 3]', '[2, 4]', '[2, 4]', 'kleine', 'kle^5i^2n^4e^5', 'klein', 'e', 5, 2, None, 'ADJA', '["neutral", 0.0]', '!', '["symbol", null, "!"]', 'weil', '["KOUS", null, "weil"]', 'es', '["PPER", null, "es"]', 'ja', '["PTKMA", null, "ja"]', 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', 'ist', '["VAFIN", null, "ist"]', '.', '["symbol", null, "."]', 1, '["number", null, "1"]', 2, '["number", null, "2"]'),
           (
            58, 11111, '[5, 6, 15, 3]', '[2, 4]', '[2, 4]', 'kleine', 'kle^5i^2n^4e^5', 'klein', 'n', 4, 4, None, 'ADJA', '["neutral", 0.0]', '!', '["symbol", null, "!"]', 'weil', '["KOUS", null, "weil"]', 'es', '["PPER", null, "es"]', 'ja', '["PTKMA", null, "ja"]', 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', 'ist', '["VAFIN", null, "ist"]', '.', '["symbol", null, "."]', 1, '["number", null, "1"]', 2, '["number", null, "2"]'),
           (
            59, 11111, '[5, 6, 15, 3]', '[2, 4]', '[2, 4]', 'kleine', 'kle^5i^2n^4e^5', 'klein', 'e', 5, 5, None, 'ADJA', '["neutral", 0.0]', '!', '["symbol", null, "!"]', 'weil', '["KOUS", null, "weil"]', 'es', '["PPER", null, "es"]', 'ja', '["PTKMA", null, "ja"]', 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', 'ist', '["VAFIN", null, "ist"]', '.', '["symbol", null, "."]', 1, '["number", null, "1"]', 2, '["number", null, "2"]')))]
        right_syntagma = [
         'kleine']
        right_baseline = [
         [
          [
           'kleine'], 'klein', 1, 7, '5', '11', '1', '2', '5', '1']]
        right_redu = [
         (
          'kleine',
          (
           (
            2, 8888, '[4, 11]', '[0, 2]', '[0, 1]', 'kleine', 'klein', '{"kle^5in^5e": 1, "klein^3e": 1}', 2, 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]', 'sie', '["PPER", null, "sie"]'),))]
        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list(tuple(unicode(elem) for elem in item) for item in extracted_baseline)).should.be.equal(set(list(tuple(unicode(elem) for elem in item) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)
        syntagma = [
         'kleine']
        data = list(stats.get_data(syntagma, repl=True, redu=False, baseline=False, sentiment=False, syntagma_type='lexem'))
        right_repl = [
         (
          82, 12222, '[24]', '[0, 24]', '[0, 21]', 'kleine', 'kle^4i^5n^4e^8', 'klein', 'e', 4, 2, None, 'ADJA', '["neutral", 0.0]', ',', '["symbol", null, ","]', 'es', '["PPER", null, "es"]', 'war', '["VAFIN", null, "war"]', 'so', '["ADV", null, "so"]', 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', None, None, None, None, None, None),
         (
          83, 12222, '[24]', '[0, 24]', '[0, 21]', 'kleine', 'kle^4i^5n^4e^8', 'klein', 'i', 5, 3, None, 'ADJA', '["neutral", 0.0]', ',', '["symbol", null, ","]', 'es', '["PPER", null, "es"]', 'war', '["VAFIN", null, "war"]', 'so', '["ADV", null, "so"]', 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', None, None, None, None, None, None),
         (
          84, 12222, '[24]', '[0, 24]', '[0, 21]', 'kleine', 'kle^4i^5n^4e^8', 'klein', 'n', 4, 4, None, 'ADJA', '["neutral", 0.0]', ',', '["symbol", null, ","]', 'es', '["PPER", null, "es"]', 'war', '["VAFIN", null, "war"]', 'so', '["ADV", null, "so"]', 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', None, None, None, None, None, None),
         (
          85, 12222, '[24]', '[0, 24]', '[0, 21]', 'kleine', 'kle^4i^5n^4e^8', 'klein', 'e', 8, 5, None, 'ADJA', '["neutral", 0.0]', ',', '["symbol", null, ","]', 'es', '["PPER", null, "es"]', 'war', '["VAFIN", null, "war"]', 'so', '["ADV", null, "so"]', 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', None, None, None, None, None, None),
         (
          3, 8888, '[4, 11]', '[0, 2]', '[0, 1]', 'kleine', 'kle^5in^5e', 'klein', 'e', 5, 2, '[0, 1]', 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]', 'sie', '["PPER", null, "sie"]'),
         (
          4, 8888, '[4, 11]', '[0, 2]', '[0, 1]', 'kleine', 'kle^5in^5e', 'klein', 'n', 5, 4, '[0, 1]', 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]', 'sie', '["PPER", null, "sie"]'),
         (
          5, 8888, '[4, 11]', '[0, 3]', '[0, 1]', 'kleine', 'klein^3e', 'klein', 'n', 3, 4, '[0, 1]', 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]', 'sie', '["PPER", null, "sie"]'),
         (
          21, 10000, '[12, 3, 8]', '[0, 2]', '[0, 2]', 'kleine', 'kle^5ine', 'klein', 'e', 5, 2, None, 'ADJA', '["neutral", 0.0]', None, None, None, None, None, None, 'eine', '["ART", null, "ein"]', 'klitze', '["ADJA", null, "klitz"]', 'überaschung', '["NN", null, "uberasch"]', '@schönesleben', '["mention", null, "@schonesleb"]', '#machwasdaraus', '["hashtag", null, "#machwasdaraus"]', '#bewegedeinarsch', '["hashtag", null, "#bewegedeinarsch"]', 'https://www.freiesinternet.de', '["URL", null, "https://www.freiesinternet.d"]'),
         (
          57, 11111, '[5, 6, 15, 3]', '[2, 4]', '[2, 4]', 'kleine', 'kle^5i^2n^4e^5', 'klein', 'e', 5, 2, None, 'ADJA', '["neutral", 0.0]', '!', '["symbol", null, "!"]', 'weil', '["KOUS", null, "weil"]', 'es', '["PPER", null, "es"]', 'ja', '["PTKMA", null, "ja"]', 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', 'ist', '["VAFIN", null, "ist"]', '.', '["symbol", null, "."]', 1, '["number", null, "1"]', 2, '["number", null, "2"]'),
         (
          58, 11111, '[5, 6, 15, 3]', '[2, 4]', '[2, 4]', 'kleine', 'kle^5i^2n^4e^5', 'klein', 'n', 4, 4, None, 'ADJA', '["neutral", 0.0]', '!', '["symbol", null, "!"]', 'weil', '["KOUS", null, "weil"]', 'es', '["PPER", null, "es"]', 'ja', '["PTKMA", null, "ja"]', 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', 'ist', '["VAFIN", null, "ist"]', '.', '["symbol", null, "."]', 1, '["number", null, "1"]', 2, '["number", null, "2"]'),
         (
          59, 11111, '[5, 6, 15, 3]', '[2, 4]', '[2, 4]', 'kleine', 'kle^5i^2n^4e^5', 'klein', 'e', 5, 5, None, 'ADJA', '["neutral", 0.0]', '!', '["symbol", null, "!"]', 'weil', '["KOUS", null, "weil"]', 'es', '["PPER", null, "es"]', 'ja', '["PTKMA", null, "ja"]', 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', 'ist', '["VAFIN", null, "ist"]', '.', '["symbol", null, "."]', 1, '["number", null, "1"]', 2, '["number", null, "2"]')]
        right_syntagma = [
         'kleine']
        right_baseline = []
        right_redu = []
        extracted_repl = data[0]['repl']
        extracted_redu = data[0]['redu']
        extracted_baseline = data[0]['baseline']
        extracted_syntagma = data[0]['syntagma']
        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list(tuple(unicode(elem) for elem in item) for item in extracted_baseline)).should.be.equal(set(list(tuple(unicode(elem) for elem in item) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)
        syntagma = [
         'kleine']
        data = list(stats.get_data(syntagma, repl=False, redu=True, baseline=False, sentiment=False, syntagma_type='lexem'))
        extracted_repl = data[0]['repl']
        extracted_redu = data[0]['redu']
        extracted_baseline = data[0]['baseline']
        extracted_syntagma = data[0]['syntagma']
        right_repl = []
        right_syntagma = [
         'kleine']
        right_baseline = []
        right_redu = [
         (
          2, 8888, '[4, 11]', '[0, 2]', '[0, 1]', 'kleine', 'klein', '{"kle^5in^5e": 1, "klein^3e": 1}', 2, 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]', 'sie', '["PPER", null, "sie"]')]
        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list(tuple(unicode(elem) for elem in item) for item in extracted_baseline)).should.be.equal(set(list(tuple(unicode(elem) for elem in item) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)
        syntagma = [
         'kleine']
        data = list(stats.get_data(syntagma, repl=False, redu=False, baseline=True, sentiment=False, syntagma_type='lexem'))
        extracted_repl = data[0]['repl']
        extracted_redu = data[0]['redu']
        extracted_baseline = data[0]['baseline']
        extracted_syntagma = data[0]['syntagma']
        right_repl = []
        right_syntagma = [
         'kleine']
        right_baseline = [
         [
          [
           'kleine'], 'klein', 1, 7, '5', '11', '1', '2', '5', '1']]
        right_redu = []
        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list(tuple(unicode(elem) for elem in item) for item in extracted_baseline)).should.be.equal(set(list(tuple(unicode(elem) for elem in item) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)
        syntagma = [
         'kleine', 'Überaschung']
        data = stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='lexem', order_output_by_syntagma_order=True, return_full_tuple=False)
        len1 = len(data)
        data = list(data)
        len2 = len(data)
        len1.should.be.equal(len2)
        extracted_repl = data[0]['repl']
        extracted_redu = data[0]['redu']
        extracted_baseline = data[0]['baseline']
        extracted_syntagma = data[0]['syntagma']
        right_repl = [
         (
          'kleine',
          (
           (
            82, 12222, '[24]', '[0, 24]', '[0, 21]', 'kleine', 'kle^4i^5n^4e^8', 'klein', 'e', 4, 2, None, 'ADJA', '["neutral", 0.0]', ',', '["symbol", null, ","]', 'es', '["PPER", null, "es"]', 'war', '["VAFIN", null, "war"]', 'so', '["ADV", null, "so"]', 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', None, None, None, None, None, None),
           (
            83, 12222, '[24]', '[0, 24]', '[0, 21]', 'kleine', 'kle^4i^5n^4e^8', 'klein', 'i', 5, 3, None, 'ADJA', '["neutral", 0.0]', ',', '["symbol", null, ","]', 'es', '["PPER", null, "es"]', 'war', '["VAFIN", null, "war"]', 'so', '["ADV", null, "so"]', 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', None, None, None, None, None, None),
           (
            84, 12222, '[24]', '[0, 24]', '[0, 21]', 'kleine', 'kle^4i^5n^4e^8', 'klein', 'n', 4, 4, None, 'ADJA', '["neutral", 0.0]', ',', '["symbol", null, ","]', 'es', '["PPER", null, "es"]', 'war', '["VAFIN", null, "war"]', 'so', '["ADV", null, "so"]', 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', None, None, None, None, None, None),
           (
            85, 12222, '[24]', '[0, 24]', '[0, 21]', 'kleine', 'kle^4i^5n^4e^8', 'klein', 'e', 8, 5, None, 'ADJA', '["neutral", 0.0]', ',', '["symbol", null, ","]', 'es', '["PPER", null, "es"]', 'war', '["VAFIN", null, "war"]', 'so', '["ADV", null, "so"]', 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', None, None, None, None, None, None),
           (
            21, 10000, '[12, 3, 8]', '[0, 2]', '[0, 2]', 'kleine', 'kle^5ine', 'klein', 'e', 5, 2, None, 'ADJA', '["neutral", 0.0]', None, None, None, None, None, None, 'eine', '["ART", null, "ein"]', 'klitze', '["ADJA", null, "klitz"]', 'überaschung', '["NN", null, "uberasch"]', '@schönesleben', '["mention", null, "@schonesleb"]', '#machwasdaraus', '["hashtag", null, "#machwasdaraus"]', '#bewegedeinarsch', '["hashtag", null, "#bewegedeinarsch"]', 'https://www.freiesinternet.de', '["URL", null, "https://www.freiesinternet.d"]'),
           (
            57, 11111, '[5, 6, 15, 3]', '[2, 4]', '[2, 4]', 'kleine', 'kle^5i^2n^4e^5', 'klein', 'e', 5, 2, None, 'ADJA', '["neutral", 0.0]', '!', '["symbol", null, "!"]', 'weil', '["KOUS", null, "weil"]', 'es', '["PPER", null, "es"]', 'ja', '["PTKMA", null, "ja"]', 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', 'ist', '["VAFIN", null, "ist"]', '.', '["symbol", null, "."]', 1, '["number", null, "1"]', 2, '["number", null, "2"]'),
           (
            58, 11111, '[5, 6, 15, 3]', '[2, 4]', '[2, 4]', 'kleine', 'kle^5i^2n^4e^5', 'klein', 'n', 4, 4, None, 'ADJA', '["neutral", 0.0]', '!', '["symbol", null, "!"]', 'weil', '["KOUS", null, "weil"]', 'es', '["PPER", null, "es"]', 'ja', '["PTKMA", null, "ja"]', 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', 'ist', '["VAFIN", null, "ist"]', '.', '["symbol", null, "."]', 1, '["number", null, "1"]', 2, '["number", null, "2"]'),
           (
            59, 11111, '[5, 6, 15, 3]', '[2, 4]', '[2, 4]', 'kleine', 'kle^5i^2n^4e^5', 'klein', 'e', 5, 5, None, 'ADJA', '["neutral", 0.0]', '!', '["symbol", null, "!"]', 'weil', '["KOUS", null, "weil"]', 'es', '["PPER", null, "es"]', 'ja', '["PTKMA", null, "ja"]', 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', 'ist', '["VAFIN", null, "ist"]', '.', '["symbol", null, "."]', 1, '["number", null, "1"]', 2, '["number", null, "2"]'))),
         (
          'überaschung',
          (
           (
            86, 12222, '[24]', '[0, 25]', '[0, 22]', 'überaschung', 'übe^4r^5a^3schun^6g^3', 'uberasch', 'e', 4, 2, None, 'NN', '["neutral", 0.0]', 'es', '["PPER", null, "es"]', 'war', '["VAFIN", null, "war"]', 'so', '["ADV", null, "so"]', 'eine', '["ART", null, "ein"]', 'kleine', '["ADJA", null, "klein"]', '.', '["symbol", null, "."]', None, None, None, None, None, None, None, None),
           (
            87, 12222, '[24]', '[0, 25]', '[0, 22]', 'überaschung', 'übe^4r^5a^3schun^6g^3', 'uberasch', 'r', 5, 3, None, 'NN', '["neutral", 0.0]', 'es', '["PPER", null, "es"]', 'war', '["VAFIN", null, "war"]', 'so', '["ADV", null, "so"]', 'eine', '["ART", null, "ein"]', 'kleine', '["ADJA", null, "klein"]', '.', '["symbol", null, "."]', None, None, None, None, None, None, None, None),
           (
            88, 12222, '[24]', '[0, 25]', '[0, 22]', 'überaschung', 'übe^4r^5a^3schun^6g^3', 'uberasch', 'a', 3, 4, None, 'NN', '["neutral", 0.0]', 'es', '["PPER", null, "es"]', 'war', '["VAFIN", null, "war"]', 'so', '["ADV", null, "so"]', 'eine', '["ART", null, "ein"]', 'kleine', '["ADJA", null, "klein"]', '.', '["symbol", null, "."]', None, None, None, None, None, None, None, None),
           (
            89, 12222, '[24]', '[0, 25]', '[0, 22]', 'überaschung', 'übe^4r^5a^3schun^6g^3', 'uberasch', 'n', 6, 9, None, 'NN', '["neutral", 0.0]', 'es', '["PPER", null, "es"]', 'war', '["VAFIN", null, "war"]', 'so', '["ADV", null, "so"]', 'eine', '["ART", null, "ein"]', 'kleine', '["ADJA", null, "klein"]', '.', '["symbol", null, "."]', None, None, None, None, None, None, None, None),
           (
            90, 12222, '[24]', '[0, 25]', '[0, 22]', 'überaschung', 'übe^4r^5a^3schun^6g^3', 'uberasch', 'g', 3, 10, None, 'NN', '["neutral", 0.0]', 'es', '["PPER", null, "es"]', 'war', '["VAFIN", null, "war"]', 'so', '["ADV", null, "so"]', 'eine', '["ART", null, "ein"]', 'kleine', '["ADJA", null, "klein"]', '.', '["symbol", null, "."]', None, None, None, None, None, None, None, None),
           (
            22, 10000, '[12, 3, 8]', '[0, 3]', '[0, 3]', 'überaschung', 'über^4aschung', 'uberasch', 'r', 4, 3, None, 'NN', '["neutral", 0.0]', None, None, None, None, 'eine', '["ART", null, "ein"]', 'klitze', '["ADJA", null, "klitz"]', 'kleine', '["ADJA", null, "klein"]', '@schönesleben', '["mention", null, "@schonesleb"]', '#machwasdaraus', '["hashtag", null, "#machwasdaraus"]', '#bewegedeinarsch', '["hashtag", null, "#bewegedeinarsch"]', 'https://www.freiesinternet.de', '["URL", null, "https://www.freiesinternet.d"]', 'beser', '["ADJD", null, "bes"]'),
           (
            60, 11111, '[5, 6, 15, 3]', '[2, 5]', '[2, 5]', 'überaschung', 'über^5aschung', 'uberasch', 'r', 5, 3, None, 'NN', '["neutral", 0.0]', 'weil', '["KOUS", null, "weil"]', 'es', '["PPER", null, "es"]', 'ja', '["PTKMA", null, "ja"]', 'eine', '["ART", null, "ein"]', 'kleine', '["ADJA", null, "klein"]', 'ist', '["VAFIN", null, "ist"]', '.', '["symbol", null, "."]', 1, '["number", null, "1"]', 2, '["number", null, "2"]', 3, '["number", null, "3"]')))]
        right_syntagma = [
         'kleine', 'überaschung']
        right_baseline = [
         [
          [
           'kleine', 'überaschung'], 'klein++uberasch', 2, 5, '[3, 3]', '[8, 7]', None, None, '3', None]]
        right_redu = ()
        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list(tuple(unicode(elem) for elem in item) for item in extracted_baseline)).should.be.equal(set(list(tuple(unicode(elem) for elem in item) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)
        syntagma = [
         'kleine', 'Überaschung']
        data = list(stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='lexem', order_output_by_syntagma_order=True, return_full_tuple=True))
        extracted_repl = data[0]['repl']
        extracted_redu = data[0]['redu']
        extracted_baseline = data[0]['baseline']
        extracted_syntagma = data[0]['syntagma']
        right_repl = (
         [
          (
           'kleine',
           (
            (
             82, 12222, '[24]', '[0, 24]', '[0, 21]', 'kleine', 'kle^4i^5n^4e^8', 'klein', 'e', 4, 2, None, 'ADJA', '["neutral", 0.0]', ',', '["symbol", null, ","]', 'es', '["PPER", null, "es"]', 'war', '["VAFIN", null, "war"]', 'so', '["ADV", null, "so"]', 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', None, None, None, None, None, None),
            (
             83, 12222, '[24]', '[0, 24]', '[0, 21]', 'kleine', 'kle^4i^5n^4e^8', 'klein', 'i', 5, 3, None, 'ADJA', '["neutral", 0.0]', ',', '["symbol", null, ","]', 'es', '["PPER", null, "es"]', 'war', '["VAFIN", null, "war"]', 'so', '["ADV", null, "so"]', 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', None, None, None, None, None, None),
            (
             84, 12222, '[24]', '[0, 24]', '[0, 21]', 'kleine', 'kle^4i^5n^4e^8', 'klein', 'n', 4, 4, None, 'ADJA', '["neutral", 0.0]', ',', '["symbol", null, ","]', 'es', '["PPER", null, "es"]', 'war', '["VAFIN", null, "war"]', 'so', '["ADV", null, "so"]', 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', None, None, None, None, None, None),
            (
             85, 12222, '[24]', '[0, 24]', '[0, 21]', 'kleine', 'kle^4i^5n^4e^8', 'klein', 'e', 8, 5, None, 'ADJA', '["neutral", 0.0]', ',', '["symbol", null, ","]', 'es', '["PPER", null, "es"]', 'war', '["VAFIN", null, "war"]', 'so', '["ADV", null, "so"]', 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', None, None, None, None, None, None),
            (
             21, 10000, '[12, 3, 8]', '[0, 2]', '[0, 2]', 'kleine', 'kle^5ine', 'klein', 'e', 5, 2, None, 'ADJA', '["neutral", 0.0]', None, None, None, None, None, None, 'eine', '["ART", null, "ein"]', 'klitze', '["ADJA", null, "klitz"]', 'überaschung', '["NN", null, "uberasch"]', '@schönesleben', '["mention", null, "@schonesleb"]', '#machwasdaraus', '["hashtag", null, "#machwasdaraus"]', '#bewegedeinarsch', '["hashtag", null, "#bewegedeinarsch"]', 'https://www.freiesinternet.de', '["URL", null, "https://www.freiesinternet.d"]'),
            (
             57, 11111, '[5, 6, 15, 3]', '[2, 4]', '[2, 4]', 'kleine', 'kle^5i^2n^4e^5', 'klein', 'e', 5, 2, None, 'ADJA', '["neutral", 0.0]', '!', '["symbol", null, "!"]', 'weil', '["KOUS", null, "weil"]', 'es', '["PPER", null, "es"]', 'ja', '["PTKMA", null, "ja"]', 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', 'ist', '["VAFIN", null, "ist"]', '.', '["symbol", null, "."]', 1, '["number", null, "1"]', 2, '["number", null, "2"]'),
            (
             58, 11111, '[5, 6, 15, 3]', '[2, 4]', '[2, 4]', 'kleine', 'kle^5i^2n^4e^5', 'klein', 'n', 4, 4, None, 'ADJA', '["neutral", 0.0]', '!', '["symbol", null, "!"]', 'weil', '["KOUS", null, "weil"]', 'es', '["PPER", null, "es"]', 'ja', '["PTKMA", null, "ja"]', 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', 'ist', '["VAFIN", null, "ist"]', '.', '["symbol", null, "."]', 1, '["number", null, "1"]', 2, '["number", null, "2"]'),
            (
             59, 11111, '[5, 6, 15, 3]', '[2, 4]', '[2, 4]', 'kleine', 'kle^5i^2n^4e^5', 'klein', 'e', 5, 5, None, 'ADJA', '["neutral", 0.0]', '!', '["symbol", null, "!"]', 'weil', '["KOUS", null, "weil"]', 'es', '["PPER", null, "es"]', 'ja', '["PTKMA", null, "ja"]', 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', 'ist', '["VAFIN", null, "ist"]', '.', '["symbol", null, "."]', 1, '["number", null, "1"]', 2, '["number", null, "2"]'))),
          (
           'überaschung',
           (
            (
             86, 12222, '[24]', '[0, 25]', '[0, 22]', 'überaschung', 'übe^4r^5a^3schun^6g^3', 'uberasch', 'e', 4, 2, None, 'NN', '["neutral", 0.0]', 'es', '["PPER", null, "es"]', 'war', '["VAFIN", null, "war"]', 'so', '["ADV", null, "so"]', 'eine', '["ART", null, "ein"]', 'kleine', '["ADJA", null, "klein"]', '.', '["symbol", null, "."]', None, None, None, None, None, None, None, None),
            (
             87, 12222, '[24]', '[0, 25]', '[0, 22]', 'überaschung', 'übe^4r^5a^3schun^6g^3', 'uberasch', 'r', 5, 3, None, 'NN', '["neutral", 0.0]', 'es', '["PPER", null, "es"]', 'war', '["VAFIN", null, "war"]', 'so', '["ADV", null, "so"]', 'eine', '["ART", null, "ein"]', 'kleine', '["ADJA", null, "klein"]', '.', '["symbol", null, "."]', None, None, None, None, None, None, None, None),
            (
             88, 12222, '[24]', '[0, 25]', '[0, 22]', 'überaschung', 'übe^4r^5a^3schun^6g^3', 'uberasch', 'a', 3, 4, None, 'NN', '["neutral", 0.0]', 'es', '["PPER", null, "es"]', 'war', '["VAFIN", null, "war"]', 'so', '["ADV", null, "so"]', 'eine', '["ART", null, "ein"]', 'kleine', '["ADJA", null, "klein"]', '.', '["symbol", null, "."]', None, None, None, None, None, None, None, None),
            (
             89, 12222, '[24]', '[0, 25]', '[0, 22]', 'überaschung', 'übe^4r^5a^3schun^6g^3', 'uberasch', 'n', 6, 9, None, 'NN', '["neutral", 0.0]', 'es', '["PPER", null, "es"]', 'war', '["VAFIN", null, "war"]', 'so', '["ADV", null, "so"]', 'eine', '["ART", null, "ein"]', 'kleine', '["ADJA", null, "klein"]', '.', '["symbol", null, "."]', None, None, None, None, None, None, None, None),
            (
             90, 12222, '[24]', '[0, 25]', '[0, 22]', 'überaschung', 'übe^4r^5a^3schun^6g^3', 'uberasch', 'g', 3, 10, None, 'NN', '["neutral", 0.0]', 'es', '["PPER", null, "es"]', 'war', '["VAFIN", null, "war"]', 'so', '["ADV", null, "so"]', 'eine', '["ART", null, "ein"]', 'kleine', '["ADJA", null, "klein"]', '.', '["symbol", null, "."]', None, None, None, None, None, None, None, None),
            (
             22, 10000, '[12, 3, 8]', '[0, 3]', '[0, 3]', 'überaschung', 'über^4aschung', 'uberasch', 'r', 4, 3, None, 'NN', '["neutral", 0.0]', None, None, None, None, 'eine', '["ART", null, "ein"]', 'klitze', '["ADJA", null, "klitz"]', 'kleine', '["ADJA", null, "klein"]', '@schönesleben', '["mention", null, "@schonesleb"]', '#machwasdaraus', '["hashtag", null, "#machwasdaraus"]', '#bewegedeinarsch', '["hashtag", null, "#bewegedeinarsch"]', 'https://www.freiesinternet.de', '["URL", null, "https://www.freiesinternet.d"]', 'beser', '["ADJD", null, "bes"]'),
            (
             60, 11111, '[5, 6, 15, 3]', '[2, 5]', '[2, 5]', 'überaschung', 'über^5aschung', 'uberasch', 'r', 5, 3, None, 'NN', '["neutral", 0.0]', 'weil', '["KOUS", null, "weil"]', 'es', '["PPER", null, "es"]', 'ja', '["PTKMA", null, "ja"]', 'eine', '["ART", null, "ein"]', 'kleine', '["ADJA", null, "klein"]', 'ist', '["VAFIN", null, "ist"]', '.', '["symbol", null, "."]', 1, '["number", null, "1"]', 2, '["number", null, "2"]', 3, '["number", null, "3"]')))],
         True,
         3)
        right_syntagma = [
         'kleine', 'überaschung']
        right_baseline = [
         [
          [
           'kleine', 'überaschung'], 'klein++uberasch', 2, 5, '[3, 3]', '[8, 7]', None, None, '3', None]]
        right_redu = None
        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        extracted_redu.should.be.equal(right_redu)
        set(list(tuple(unicode(elem) for elem in item) for item in extracted_baseline)).should.be.equal(set(list(tuple(unicode(elem) for elem in item) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)
        syntagma = [
         'klitze', 'kleine', 'überaschung']
        data = list(stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='lexem', order_output_by_syntagma_order=True))
        extracted_repl = data[0]['repl']
        extracted_redu = data[0]['redu']
        extracted_baseline = data[0]['baseline']
        extracted_syntagma = data[0]['syntagma']
        right_repl = [
         (
          'klitze',
          (
           (
            20, 10000, '[12, 3, 8]', '[0, 1]', '[0, 1]', 'klitze', 'klitze^4', 'klitz', 'e', 4, 5, None, 'ADJA', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'eine', '["ART", null, "ein"]', 'kleine', '["ADJA", null, "klein"]', 'überaschung', '["NN", null, "uberasch"]', '@schönesleben', '["mention", null, "@schonesleb"]', '#machwasdaraus', '["hashtag", null, "#machwasdaraus"]', '#bewegedeinarsch', '["hashtag", null, "#bewegedeinarsch"]'),)),
         (
          'kleine',
          (
           (
            21, 10000, '[12, 3, 8]', '[0, 2]', '[0, 2]', 'kleine', 'kle^5ine', 'klein', 'e', 5, 2, None, 'ADJA', '["neutral", 0.0]', None, None, None, None, None, None, 'eine', '["ART", null, "ein"]', 'klitze', '["ADJA", null, "klitz"]', 'überaschung', '["NN", null, "uberasch"]', '@schönesleben', '["mention", null, "@schonesleb"]', '#machwasdaraus', '["hashtag", null, "#machwasdaraus"]', '#bewegedeinarsch', '["hashtag", null, "#bewegedeinarsch"]', 'https://www.freiesinternet.de', '["URL", null, "https://www.freiesinternet.d"]'),)),
         (
          'überaschung',
          (
           (
            22, 10000, '[12, 3, 8]', '[0, 3]', '[0, 3]', 'überaschung', 'über^4aschung', 'uberasch', 'r', 4, 3, None, 'NN', '["neutral", 0.0]', None, None, None, None, 'eine', '["ART", null, "ein"]', 'klitze', '["ADJA", null, "klitz"]', 'kleine', '["ADJA", null, "klein"]', '@schönesleben', '["mention", null, "@schonesleb"]', '#machwasdaraus', '["hashtag", null, "#machwasdaraus"]', '#bewegedeinarsch', '["hashtag", null, "#bewegedeinarsch"]', 'https://www.freiesinternet.de', '["URL", null, "https://www.freiesinternet.d"]', 'beser', '["ADJD", null, "bes"]'),))]
        right_syntagma = [
         'klitze', 'kleine', 'überaschung']
        right_baseline = [
         [
          [
           'klitze', 'kleine', 'überaschung'], 'klitz++klein++uberasch', 3, 3, '[1, 1, 1]', '[1, 1, 1]', None, None, '1', None]]
        right_redu = ()
        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list(tuple(unicode(elem) for elem in item) for item in extracted_baseline)).should.be.equal(set(list(tuple(unicode(elem) for elem in item) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)
        syntagma = [
         'NN', 'NE']
        data = list(stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='pos'))
        extracted_repl = data[0]['repl']
        extracted_redu = data[0]['redu']
        extracted_baseline = data[0]['baseline']
        extracted_syntagma = data[0]['syntagma']
        right_repl = [
         (
          1, 8888, '[4, 11]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze^7', 'klitz', 'i', 4, 2, '[0, 0]', 'NN', '["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, 'kleine', '["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]'),
         (
          2, 8888, '[4, 11]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze^7', 'klitz', 'e', 7, 5, '[0, 0]', 'NN', '["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, 'kleine', '["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]'),
         (
          3, 8888, '[4, 11]', '[0, 2]', '[0, 1]', 'kleine', 'kle^5in^5e', 'klein', 'e', 5, 2, '[0, 1]', 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]', 'sie', '["PPER", null, "sie"]'),
         (
          4, 8888, '[4, 11]', '[0, 2]', '[0, 1]', 'kleine', 'kle^5in^5e', 'klein', 'n', 5, 4, '[0, 1]', 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]', 'sie', '["PPER", null, "sie"]'),
         (
          5, 8888, '[4, 11]', '[0, 3]', '[0, 1]', 'kleine', 'klein^3e', 'klein', 'n', 3, 4, '[0, 1]', 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]', 'sie', '["PPER", null, "sie"]')]
        right_syntagma = [
         'NN', 'NE']
        right_baseline = [
         [
          [
           'klitze', 'kleine', 'überaschung'], 'klitz++klein++uberasch', 3, 3, '[1, 1, 1]', '[1, 1, 1]', None, None, '1', None], [['klitze', 'kleine'], 'klitz++klein', 2, 4, '[2, 3]', '[3, 4]', '[1, 1]', '[2, 2]', '2', '1'], [['klitze'], 'klitz', 1, 8, '3', '4', '2', '6', '3', '2'], [['klitze', 'kleine', 'überaschung', '.'], 'klitz++klein++uberasch++.', 4, 1, None, None, None, None, None, None], [['kleine'], 'klein', 1, 7, '5', '11', '1', '2', '5', '1'], [['klitze', 'kleine', 'überaschung', '.', 'trotzdem', 'hat'], 'klitz++klein++uberasch++.++trotzd++hat', 6, 1, None, None, None, None, None, None], [['kleine', 'überaschung', '.', 'trotzdem'], 'klein++uberasch++.++trotzd', 4, 1, None, None, None, None, None, None], [['kleine', 'überaschung', '.'], 'klein++uberasch++.', 3, 2, None, None, None, None, None, None], [['kleine', 'überaschung', '.', 'trotzdem', 'hat'], 'klein++uberasch++.++trotzd++hat', 5, 1, None, None, None, None, None, None], [['klitze', 'kleine', 'überaschung', '.', 'trotzdem'], 'klitz++klein++uberasch++.++trotzd', 5, 1, None, None, None, None, None, None], [['kleine', 'überaschung', '.', 'trotzdem', 'hat', 'sie'], 'klein++uberasch++.++trotzd++hat++sie', 6, 1, None, None, None, None, None, None], [['kleine', 'überaschung'], 'klein++uberasch', 2, 5, '[3, 3]', '[8, 7]', None, None, '3', None]]
        right_redu = [
         (
          1, 8888, '[4, 11]', '[0, 0]', '[0, 0]', 'klitze', 'klitz', '{"klitze": 1, "kli^4tze^7": 1}', 2, 'NN', '["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, 'kleine', '["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]'),
         (
          2, 8888, '[4, 11]', '[0, 2]', '[0, 1]', 'kleine', 'klein', '{"kle^5in^5e": 1, "klein^3e": 1}', 2, 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]', 'sie', '["PPER", null, "sie"]')]
        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list(tuple(unicode(elem) for elem in item) for item in extracted_baseline)).should.be.equal(set(list(tuple(unicode(elem) for elem in item) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)
        syntagma = [
         'number']
        data = stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='pos')
        len1 = len(data)
        data = list(data)
        len2 = len(data)
        len1.should.be.equal(len2)
        extracted_repl = data[0]['repl']
        extracted_redu = data[0]['redu']
        extracted_baseline = data[0]['baseline']
        extracted_syntagma = data[0]['syntagma']
        right_repl = [
         (
          78, 12222, '[24]', '[0, 14]', '[0, 11]', '1', '1^6', '1', '1', 6, 0, None, 'number', '["neutral", 0.0]', 'ich', '["PPER", null, "ich"]', 'mal', '["PTKMA", null, "mal"]', 'gerne', '["ADV", null, "gern"]', 'hate', '["VAFIN", null, "hat"]', '.', '["symbol", null, "."]', '😫', '["EMOIMG", null, "\\ud83d\\ude2b"]', 1, '["number", null, "1"]', 'du', '["PPER", null, "du"]', 'meintest', '["VVFIN", null, "meint"]', ',', '["symbol", null, ","]'),
         (
          80, 12222, '[24]', '[0, 16]', '[0, 13]', '1', '1^8', '1', '1', 8, 0, None, 'number', '["neutral", 0.0]', 'gerne', '["ADV", null, "gern"]', 'hate', '["VAFIN", null, "hat"]', '.', '["symbol", null, "."]', 1, '["number", null, "1"]', '😫', '["EMOIMG", null, "\\ud83d\\ude2b"]', 'du', '["PPER", null, "du"]', 'meintest', '["VVFIN", null, "meint"]', ',', '["symbol", null, ","]', 'es', '["PPER", null, "es"]', 'war', '["VAFIN", null, "war"]'),
         (
          61, 11111, '[5, 6, 15, 3]', '[2, 8]', '[2, 8]', '1', '1^5', '1', '1', 5, 0, None, 'number', '["neutral", 0.0]', 'eine', '["ART", null, "ein"]', 'kleine', '["ADJA", null, "klein"]', 'überaschung', '["NN", null, "uberasch"]', 'ist', '["VAFIN", null, "ist"]', '.', '["symbol", null, "."]', 2, '["number", null, "2"]', 3, '["number", null, "3"]', 4, '["number", null, "4"]', 5, '["number", null, "5"]', 6, '["number", null, "6"]'),
         (
          62, 11111, '[5, 6, 15, 3]', '[2, 9]', '[2, 9]', '2', '2^4', '2', '2', 4, 0, None, 'number', '["neutral", 0.0]', 'kleine', '["ADJA", null, "klein"]', 'überaschung', '["NN", null, "uberasch"]', 'ist', '["VAFIN", null, "ist"]', '.', '["symbol", null, "."]', 1, '["number", null, "1"]', 3, '["number", null, "3"]', 4, '["number", null, "4"]', 5, '["number", null, "5"]', 6, '["number", null, "6"]', '.', '["symbol", null, "."]'),
         (
          63, 11111, '[5, 6, 15, 3]', '[2, 10]', '[2, 10]', '3', '3^5', '3', '3', 5, 0, None, 'number', '["neutral", 0.0]', 'überaschung', '["NN", null, "uberasch"]', 'ist', '["VAFIN", null, "ist"]', '.', '["symbol", null, "."]', 1, '["number", null, "1"]', 2, '["number", null, "2"]', 4, '["number", null, "4"]', 5, '["number", null, "5"]', 6, '["number", null, "6"]', '.', '["symbol", null, "."]', 'kleines', '["NN", {"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}, "klein"]'),
         (
          64, 11111, '[5, 6, 15, 3]', '[2, 11]', '[2, 11]', '4', '4^4', '4', '4', 4, 0, None, 'number', '["neutral", 0.0]', 'ist', '["VAFIN", null, "ist"]', '.', '["symbol", null, "."]', 1, '["number", null, "1"]', 2, '["number", null, "2"]', 3, '["number", null, "3"]', 5, '["number", null, "5"]', 6, '["number", null, "6"]', '.', '["symbol", null, "."]', 'kleines', '["NN", {"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}, "klein"]', 'mädchen', '["NN", null, "madch"]'),
         (
          65, 11111, '[5, 6, 15, 3]', '[2, 12]', '[2, 12]', '5', '5^5', '5', '5', 5, 0, None, 'number', '["neutral", 0.0]', '.', '["symbol", null, "."]', 1, '["number", null, "1"]', 2, '["number", null, "2"]', 3, '["number", null, "3"]', 4, '["number", null, "4"]', 6, '["number", null, "6"]', '.', '["symbol", null, "."]', 'kleines', '["NN", {"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}, "klein"]', 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]')]
        right_syntagma = [
         'number']
        right_baseline = [
         [
          [
           '1', '😫', '1', 'du', 'meintest'], '1++😫++1++du++meint', 5, 1, None, None, None, None, None, None], [['3', '4', '5', '6', '.', 'kleines'], '3++4++5++6++.++klein', 6, 1, None, None, None, None, None, None], [['3', '4', '5', '6'], '3++4++5++6', 4, 1, None, None, None, None, None, None], [['1', '2'], '1++2', 2, 1, '[1, 1]', '[1, 1]', None, None, '1', None], [['5', '6'], '5++6', 2, 1, None, None, None, None, None, None], [['1', '😫', '1', 'du', 'meintest', ','], '1++😫++1++du++meint++,', 6, 1, None, None, None, None, None, None], [['2'], '2', 1, 1, '1', '1', None, None, '1', None], [['1', '2', '3', '4'], '1++2++3++4', 4, 1, '[1, 1, 1, 1]', '[1, 1, 1, 1]', None, None, '1', None], [['2', '3', '4', '5', '6'], '2++3++4++5++6', 5, 1, None, None, None, None, None, None], [['1', '😫'], '1++😫', 2, 1, '[1, 1]', '[1, 1]', None, None, '1', None], [['5', '6', '.', 'kleines'], '5++6++.++klein', 4, 1, None, None, None, None, None, None], [['3', '4'], '3++4', 2, 1, '[1, 1]', '[1, 1]', None, None, '1', None], [['1', 'du', 'meintest', ','], '1++du++meint++,', 4, 1, None, None, None, None, None, None], [['1', '2', '3', '4', '5', '6'], '1++2++3++4++5++6', 6, 1, None, None, None, None, None, None], [['4', '5', '6', '.', 'kleines', 'mädchen'], '4++5++6++.++klein++madch', 6, 1, None, None, None, None, None, None], [['1', '😫', '1', 'du'], '1++😫++1++du', 4, 1, None, None, None, None, None, None], [['2', '3', '4'], '2++3++4', 3, 1, '[1, 1, 1]', '[1, 1, 1]', None, None, '1', None], [['3', '4', '5'], '3++4++5', 3, 1, '[1, 1, 1]', '[1, 1, 1]', None, None, '1', None], [['4', '5', '6', '.'], '4++5++6++.', 4, 1, None, None, None, None, None, None], [['4'], '4', 1, 1, '1', '1', None, None, '1', None], [['1', '2', '3'], '1++2++3', 3, 1, '[1, 1, 1]', '[1, 1, 1]', None, None, '1', None], [['1', 'du'], '1++du', 2, 1, None, None, None, None, None, None], [['1'], '1', 1, 3, '3', '3', None, None, '3', None], [['2', '3'], '2++3', 2, 1, '[1, 1]', '[1, 1]', None, None, '1', None], [['3'], '3', 1, 1, '1', '1', None, None, '1', None], [['4', '5', '6'], '4++5++6', 3, 1, None, None, None, None, None, None], [['1', '😫', '1'], '1++😫++1', 3, 1, '[2, 1, "IGNOR"]', '[2, 1, "IGNOR"]', None, None, '1', None], [['5'], '5', 1, 1, '1', '1', None, None, '1', None], [['4', '5', '6', '.', 'kleines'], '4++5++6++.++klein', 5, 1, None, None, None, None, None, None], [['5', '6', '.'], '5++6++.', 3, 1, None, None, None, None, None, None], [['2', '3', '4', '5', '6', '.'], '2++3++4++5++6++.', 6, 1, None, None, None, None, None, None], [['1', 'du', 'meintest', ',', 'es'], '1++du++meint++,++es', 5, 1, None, None, None, None, None, None], [['5', '6', '.', 'kleines', 'mädchen', '.'], '5++6++.++klein++madch++.', 6, 1, None, None, None, None, None, None], [['3', '4', '5', '6', '.'], '3++4++5++6++.', 5, 1, None, None, None, None, None, None], [['1', 'du', 'meintest', ',', 'es', 'war'], '1++du++meint++,++es++war', 6, 1, None, None, None, None, None, None], [['2', '3', '4', '5'], '2++3++4++5', 4, 1, '[1, 1, 1, 1]', '[1, 1, 1, 1]', None, None, '1', None], [['1', 'du', 'meintest'], '1++du++meint', 3, 1, None, None, None, None, None, None], [['1', '2', '3', '4', '5'], '1++2++3++4++5', 5, 1, '[1, 1, 1, 1, 1]', '[1, 1, 1, 1, 1]', None, None, '1', None], [['5', '6', '.', 'kleines', 'mädchen'], '5++6++.++klein++madch', 5, 1, None, None, None, None, None, None], [['4', '5'], '4++5', 2, 1, '[1, 1]', '[1, 1]', None, None, '1', None]]
        right_redu = ()
        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list(tuple(unicode(elem) for elem in item) for item in extracted_baseline)).should.be.equal(set(list(tuple(unicode(elem) for elem in item) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)
        syntagma = [
         'number', 'number']
        data = list(stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='pos'))
        extracted_repl = data[0]['repl']
        extracted_redu = data[0]['redu']
        extracted_baseline = data[0]['baseline']
        extracted_syntagma = data[0]['syntagma']
        right_repl = [
         (
          61, 11111, '[5, 6, 15, 3]', '[2, 8]', '[2, 8]', '1', '1^5', '1', '1', 5, 0, None, 'number', '["neutral", 0.0]', 'eine', '["ART", null, "ein"]', 'kleine', '["ADJA", null, "klein"]', 'überaschung', '["NN", null, "uberasch"]', 'ist', '["VAFIN", null, "ist"]', '.', '["symbol", null, "."]', 2, '["number", null, "2"]', 3, '["number", null, "3"]', 4, '["number", null, "4"]', 5, '["number", null, "5"]', 6, '["number", null, "6"]'),
         (
          62, 11111, '[5, 6, 15, 3]', '[2, 9]', '[2, 9]', '2', '2^4', '2', '2', 4, 0, None, 'number', '["neutral", 0.0]', 'kleine', '["ADJA", null, "klein"]', 'überaschung', '["NN", null, "uberasch"]', 'ist', '["VAFIN", null, "ist"]', '.', '["symbol", null, "."]', 1, '["number", null, "1"]', 3, '["number", null, "3"]', 4, '["number", null, "4"]', 5, '["number", null, "5"]', 6, '["number", null, "6"]', '.', '["symbol", null, "."]'),
         (
          63, 11111, '[5, 6, 15, 3]', '[2, 10]', '[2, 10]', '3', '3^5', '3', '3', 5, 0, None, 'number', '["neutral", 0.0]', 'überaschung', '["NN", null, "uberasch"]', 'ist', '["VAFIN", null, "ist"]', '.', '["symbol", null, "."]', 1, '["number", null, "1"]', 2, '["number", null, "2"]', 4, '["number", null, "4"]', 5, '["number", null, "5"]', 6, '["number", null, "6"]', '.', '["symbol", null, "."]', 'kleines', '["NN", {"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}, "klein"]'),
         (
          64, 11111, '[5, 6, 15, 3]', '[2, 11]', '[2, 11]', '4', '4^4', '4', '4', 4, 0, None, 'number', '["neutral", 0.0]', 'ist', '["VAFIN", null, "ist"]', '.', '["symbol", null, "."]', 1, '["number", null, "1"]', 2, '["number", null, "2"]', 3, '["number", null, "3"]', 5, '["number", null, "5"]', 6, '["number", null, "6"]', '.', '["symbol", null, "."]', 'kleines', '["NN", {"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}, "klein"]', 'mädchen', '["NN", null, "madch"]')]
        right_syntagma = [
         'number', 'number']
        right_baseline = [
         [
          [
           '3', '4', '5', '6', '.', 'kleines'], '3++4++5++6++.++klein', 6, 1, None, None, None, None, None, None], [['3', '4', '5', '6'], '3++4++5++6', 4, 1, None, None, None, None, None, None], [['1', '2'], '1++2', 2, 1, '[1, 1]', '[1, 1]', None, None, '1', None], [['2'], '2', 1, 1, '1', '1', None, None, '1', None], [['1', '2', '3', '4'], '1++2++3++4', 4, 1, '[1, 1, 1, 1]', '[1, 1, 1, 1]', None, None, '1', None], [['2', '3', '4', '5', '6'], '2++3++4++5++6', 5, 1, None, None, None, None, None, None], [['3', '4'], '3++4', 2, 1, '[1, 1]', '[1, 1]', None, None, '1', None], [['1', '2', '3', '4', '5', '6'], '1++2++3++4++5++6', 6, 1, None, None, None, None, None, None], [['4', '5', '6', '.', 'kleines', 'mädchen'], '4++5++6++.++klein++madch', 6, 1, None, None, None, None, None, None], [['2', '3', '4'], '2++3++4', 3, 1, '[1, 1, 1]', '[1, 1, 1]', None, None, '1', None], [['3', '4', '5'], '3++4++5', 3, 1, '[1, 1, 1]', '[1, 1, 1]', None, None, '1', None], [['4', '5', '6', '.'], '4++5++6++.', 4, 1, None, None, None, None, None, None], [['4'], '4', 1, 1, '1', '1', None, None, '1', None], [['1', '2', '3'], '1++2++3', 3, 1, '[1, 1, 1]', '[1, 1, 1]', None, None, '1', None], [['1'], '1', 1, 3, '3', '3', None, None, '3', None], [['2', '3'], '2++3', 2, 1, '[1, 1]', '[1, 1]', None, None, '1', None], [['3'], '3', 1, 1, '1', '1', None, None, '1', None], [['4', '5', '6', '.', 'kleines'], '4++5++6++.++klein', 5, 1, None, None, None, None, None, None], [['2', '3', '4', '5', '6', '.'], '2++3++4++5++6++.', 6, 1, None, None, None, None, None, None], [['4', '5', '6'], '4++5++6', 3, 1, None, None, None, None, None, None], [['3', '4', '5', '6', '.'], '3++4++5++6++.', 5, 1, None, None, None, None, None, None], [['2', '3', '4', '5'], '2++3++4++5', 4, 1, '[1, 1, 1, 1]', '[1, 1, 1, 1]', None, None, '1', None], [['1', '2', '3', '4', '5'], '1++2++3++4++5', 5, 1, '[1, 1, 1, 1, 1]', '[1, 1, 1, 1, 1]', None, None, '1', None], [['4', '5'], '4++5', 2, 1, '[1, 1]', '[1, 1]', None, None, '1', None]]
        right_redu = ()
        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list(tuple(unicode(elem) for elem in item) for item in extracted_baseline)).should.be.equal(set(list(tuple(unicode(elem) for elem in item) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)
        syntagma = [
         'number', 'number', 'number']
        data = list(stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='pos'))
        extracted_repl = data[0]['repl']
        extracted_redu = data[0]['redu']
        extracted_baseline = data[0]['baseline']
        extracted_syntagma = data[0]['syntagma']
        right_repl = [
         (
          61, 11111, '[5, 6, 15, 3]', '[2, 8]', '[2, 8]', '1', '1^5', '1', '1', 5, 0, None, 'number', '["neutral", 0.0]', 'eine', '["ART", null, "ein"]', 'kleine', '["ADJA", null, "klein"]', 'überaschung', '["NN", null, "uberasch"]', 'ist', '["VAFIN", null, "ist"]', '.', '["symbol", null, "."]', 2, '["number", null, "2"]', 3, '["number", null, "3"]', 4, '["number", null, "4"]', 5, '["number", null, "5"]', 6, '["number", null, "6"]'),
         (
          62, 11111, '[5, 6, 15, 3]', '[2, 9]', '[2, 9]', '2', '2^4', '2', '2', 4, 0, None, 'number', '["neutral", 0.0]', 'kleine', '["ADJA", null, "klein"]', 'überaschung', '["NN", null, "uberasch"]', 'ist', '["VAFIN", null, "ist"]', '.', '["symbol", null, "."]', 1, '["number", null, "1"]', 3, '["number", null, "3"]', 4, '["number", null, "4"]', 5, '["number", null, "5"]', 6, '["number", null, "6"]', '.', '["symbol", null, "."]'),
         (
          63, 11111, '[5, 6, 15, 3]', '[2, 10]', '[2, 10]', '3', '3^5', '3', '3', 5, 0, None, 'number', '["neutral", 0.0]', 'überaschung', '["NN", null, "uberasch"]', 'ist', '["VAFIN", null, "ist"]', '.', '["symbol", null, "."]', 1, '["number", null, "1"]', 2, '["number", null, "2"]', 4, '["number", null, "4"]', 5, '["number", null, "5"]', 6, '["number", null, "6"]', '.', '["symbol", null, "."]', 'kleines', '["NN", {"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}, "klein"]')]
        right_syntagma = [
         'number', 'number', 'number']
        right_baseline = [
         [
          [
           '1', '2', '3', '4'], '1++2++3++4', 4, 1, '[1, 1, 1, 1]', '[1, 1, 1, 1]', None, None, '1', None], [['2', '3', '4'], '2++3++4', 3, 1, '[1, 1, 1]', '[1, 1, 1]', None, None, '1', None], [['2', '3', '4', '5', '6'], '2++3++4++5++6', 5, 1, None, None, None, None, None, None], [['2', '3', '4', '5', '6', '.'], '2++3++4++5++6++.', 6, 1, None, None, None, None, None, None], [['3', '4', '5', '6', '.', 'kleines'], '3++4++5++6++.++klein', 6, 1, None, None, None, None, None, None], [['1', '2'], '1++2', 2, 1, '[1, 1]', '[1, 1]', None, None, '1', None], [['3', '4', '5', '6'], '3++4++5++6', 4, 1, None, None, None, None, None, None], [['3', '4'], '3++4', 2, 1, '[1, 1]', '[1, 1]', None, None, '1', None], [['1', '2', '3'], '1++2++3', 3, 1, '[1, 1, 1]', '[1, 1, 1]', None, None, '1', None], [['1'], '1', 1, 3, '3', '3', None, None, '3', None], [['2', '3'], '2++3', 2, 1, '[1, 1]', '[1, 1]', None, None, '1', None], [['1', '2', '3', '4', '5', '6'], '1++2++3++4++5++6', 6, 1, None, None, None, None, None, None], [['2', '3', '4', '5'], '2++3++4++5', 4, 1, '[1, 1, 1, 1]', '[1, 1, 1, 1]', None, None, '1', None], [['3'], '3', 1, 1, '1', '1', None, None, '1', None], [['2'], '2', 1, 1, '1', '1', None, None, '1', None], [['1', '2', '3', '4', '5'], '1++2++3++4++5', 5, 1, '[1, 1, 1, 1, 1]', '[1, 1, 1, 1, 1]', None, None, '1', None], [['3', '4', '5'], '3++4++5', 3, 1, '[1, 1, 1]', '[1, 1, 1]', None, None, '1', None], [['3', '4', '5', '6', '.'], '3++4++5++6++.', 5, 1, None, None, None, None, None, None]]
        right_redu = ()
        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list(tuple(unicode(elem) for elem in item) for item in extracted_baseline)).should.be.equal(set(list(tuple(unicode(elem) for elem in item) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)
        syntagma = [
         'number', 'number', 'number']
        data = list(stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='pos', order_output_by_syntagma_order=True))
        extracted_repl = data[0]['repl']
        extracted_redu = data[0]['redu']
        extracted_baseline = data[0]['baseline']
        extracted_syntagma = data[0]['syntagma']
        right_repl = [
         (
          'number', ((61, 11111, '[5, 6, 15, 3]', '[2, 8]', '[2, 8]', '1', '1^5', '1', '1', 5, 0, None, 'number', '["neutral", 0.0]', 'eine', '["ART", null, "ein"]', 'kleine', '["ADJA", null, "klein"]', 'überaschung', '["NN", null, "uberasch"]', 'ist', '["VAFIN", null, "ist"]', '.', '["symbol", null, "."]', 2, '["number", null, "2"]', 3, '["number", null, "3"]', 4, '["number", null, "4"]', 5, '["number", null, "5"]', 6, '["number", null, "6"]'),)),
         (
          'number', ((62, 11111, '[5, 6, 15, 3]', '[2, 9]', '[2, 9]', '2', '2^4', '2', '2', 4, 0, None, 'number', '["neutral", 0.0]', 'kleine', '["ADJA", null, "klein"]', 'überaschung', '["NN", null, "uberasch"]', 'ist', '["VAFIN", null, "ist"]', '.', '["symbol", null, "."]', 1, '["number", null, "1"]', 3, '["number", null, "3"]', 4, '["number", null, "4"]', 5, '["number", null, "5"]', 6, '["number", null, "6"]', '.', '["symbol", null, "."]'),)),
         (
          'number', ((63, 11111, '[5, 6, 15, 3]', '[2, 10]', '[2, 10]', '3', '3^5', '3', '3', 5, 0, None, 'number', '["neutral", 0.0]', 'überaschung', '["NN", null, "uberasch"]', 'ist', '["VAFIN", null, "ist"]', '.', '["symbol", null, "."]', 1, '["number", null, "1"]', 2, '["number", null, "2"]', 4, '["number", null, "4"]', 5, '["number", null, "5"]', 6, '["number", null, "6"]', '.', '["symbol", null, "."]', 'kleines', '["NN", {"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}, "klein"]'),))]
        right_syntagma = [
         'number', 'number', 'number']
        right_baseline = [
         [
          [
           '1', '2', '3', '4'], '1++2++3++4', 4, 1, '[1, 1, 1, 1]', '[1, 1, 1, 1]', None, None, '1', None], [['2', '3', '4'], '2++3++4', 3, 1, '[1, 1, 1]', '[1, 1, 1]', None, None, '1', None], [['2', '3', '4', '5', '6'], '2++3++4++5++6', 5, 1, None, None, None, None, None, None], [['2', '3', '4', '5', '6', '.'], '2++3++4++5++6++.', 6, 1, None, None, None, None, None, None], [['3', '4', '5', '6', '.', 'kleines'], '3++4++5++6++.++klein', 6, 1, None, None, None, None, None, None], [['1', '2'], '1++2', 2, 1, '[1, 1]', '[1, 1]', None, None, '1', None], [['3', '4', '5', '6'], '3++4++5++6', 4, 1, None, None, None, None, None, None], [['3', '4'], '3++4', 2, 1, '[1, 1]', '[1, 1]', None, None, '1', None], [['1', '2', '3'], '1++2++3', 3, 1, '[1, 1, 1]', '[1, 1, 1]', None, None, '1', None], [['1'], '1', 1, 3, '3', '3', None, None, '3', None], [['2', '3'], '2++3', 2, 1, '[1, 1]', '[1, 1]', None, None, '1', None], [['1', '2', '3', '4', '5', '6'], '1++2++3++4++5++6', 6, 1, None, None, None, None, None, None], [['2', '3', '4', '5'], '2++3++4++5', 4, 1, '[1, 1, 1, 1]', '[1, 1, 1, 1]', None, None, '1', None], [['3'], '3', 1, 1, '1', '1', None, None, '1', None], [['2'], '2', 1, 1, '1', '1', None, None, '1', None], [['1', '2', '3', '4', '5'], '1++2++3++4++5', 5, 1, '[1, 1, 1, 1, 1]', '[1, 1, 1, 1, 1]', None, None, '1', None], [['3', '4', '5'], '3++4++5', 3, 1, '[1, 1, 1]', '[1, 1, 1]', None, None, '1', None], [['3', '4', '5', '6', '.'], '3++4++5++6++.', 5, 1, None, None, None, None, None, None]]
        right_redu = ()
        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list(tuple(unicode(elem) for elem in item) for item in extracted_baseline)).should.be.equal(set(list(tuple(unicode(elem) for elem in item) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)
        syntagma = [
         'EMOIMG']
        data1 = list(stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='pos', order_output_by_syntagma_order=False, if_type_pos_return_lexem_syn=False))
        repl1 = sorted(data1[0]['repl'])
        redu1 = sorted(data1[0]['redu'])
        data2 = list(stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='pos', order_output_by_syntagma_order=False, if_type_pos_return_lexem_syn=True))
        repl2 = sorted([ r for item in data2 for r in item['repl'] ])
        redu2 = sorted([ r for item in data2 for r in item['redu'] ])
        repl1.should.be.equal(repl2)
        redu1.should.be.equal(redu2)
        syntagma = [
         'EMOIMG', 'EMOASC']
        data1 = list(stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='pos', order_output_by_syntagma_order=False, if_type_pos_return_lexem_syn=False))
        repl1 = sorted(data1[0]['repl'])
        redu1 = sorted(data1[0]['redu'])
        data2 = list(stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='pos', order_output_by_syntagma_order=False, if_type_pos_return_lexem_syn=True))
        repl2 = sorted([ r for item in data2 for r in item['repl'] ])
        redu2 = sorted([ r for item in data2 for r in item['redu'] ])
        repl1.should.be.equal(repl2)
        redu1.should.be.equal(redu2)
        syntagma = [
         'EMOASC']
        data1 = list(stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='pos', order_output_by_syntagma_order=False, if_type_pos_return_lexem_syn=False))
        repl1 = sorted(data1[0]['repl'])
        redu1 = sorted(data1[0]['redu'])
        data2 = list(stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='pos', order_output_by_syntagma_order=False, if_type_pos_return_lexem_syn=True))
        ext_id = []
        repl2 = []
        for item in data2:
            for r in item['repl']:
                if r[0] not in ext_id:
                    ext_id.append(r[0])
                    repl2.append(r)

        repl2 = sorted(repl2)
        ext_id = []
        redu2 = []
        for item in data2:
            for r in item['redu']:
                if r[0] not in ext_id:
                    ext_id.append(r[0])
                    redu2.append(r)

        redu2 = sorted(redu2)
        if len(repl1) == len(repl2):
            assert repl1 == repl2
        else:
            assert len(repl1) <= len(repl2)
        if len(redu1) == len(redu2):
            assert redu1 == redu2
        else:
            assert len(redu1) <= len(redu2)
        syntagma = [
         'klitze', 'kleines']
        items = stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='lexem', stemmed_search=True)
        len1 = len(items)
        items = list(items)
        len2 = len(items)
        len1.should.be.equal(len2)
        for item in items:
            if item['syntagma'] == ['klitzes', 'kleines']:
                right_stem_syn = [
                 'klitz', 'klein']
                right_repl = [
                 (
                  49, 10000, '[12, 3, 8]', '[2, 10]', '[2, 6]', 'klitzes', 'klitzes^4', 'klitz', 's', 4, 6, '[2, 6]', 'FM', '["neutral", 0.0]', 'auswahl', '["NN", null, "auswahl"]', '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', 'klein', '["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', '.', '["symbol", null, "."]', 'kleines', '["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None, None, None, None, None, None),
                 (
                  50, 10000, '[12, 3, 8]', '[2, 11]', '[2, 6]', 'klitzes', 'kli^3tzes^3', 'klitz', 'i', 3, 2, '[2, 6]', 'FM', '["neutral", 0.0]', 'auswahl', '["NN", null, "auswahl"]', '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', 'klein', '["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', '.', '["symbol", null, "."]', 'kleines', '["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None, None, None, None, None, None),
                 (
                  51, 10000, '[12, 3, 8]', '[2, 11]', '[2, 6]', 'klitzes', 'kli^3tzes^3', 'klitz', 's', 3, 6, '[2, 6]', 'FM', '["neutral", 0.0]', 'auswahl', '["NN", null, "auswahl"]', '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', 'klein', '["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', '.', '["symbol", null, "."]', 'kleines', '["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None, None, None, None, None, None),
                 (
                  52, 10000, '[12, 3, 8]', '[2, 12]', '[2, 7]', 'kleines', 'klein^3e^2s', 'klein', 'n', 3, 4, '[2, 7]', 'FM', '["neutral", 0.0]', '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', 'klein', '["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', '.', '["symbol", null, "."]', 'klitzes', '["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', None, None, None, None, None, None, None, None, None, None),
                 (
                  53, 10000, '[12, 3, 8]', '[2, 13]', '[2, 7]', 'kleines', 'kleines^4', 'klein', 's', 4, 6, '[2, 7]', 'FM', '["neutral", 0.0]', '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', 'klein', '["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', '.', '["symbol", null, "."]', 'klitzes', '["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', None, None, None, None, None, None, None, None, None, None)]
                right_syntagma = [
                 'klitzes', 'kleines']
                right_baseline = (
                 [
                  [
                   'klitzes', 'kleines'], 'klitz++klein', 2, 1, '[2, 2]', '[3, 2]', '[1, 1]', '[2, 2]', '1', '1'],)
                right_redu = [
                 (
                  15, 10000, '[12, 3, 8]', '[2, 10]', '[2, 6]', 'klitzes', 'klitz', '{"klitzes^4": 1, "kli^3tzes^3": 1}', 2, 'FM', '["neutral", 0.0]', 'auswahl', '["NN", null, "auswahl"]', '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', 'klein', '["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', '.', '["symbol", null, "."]', 'kleines', '["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None, None, None, None, None, None),
                 (
                  16, 10000, '[12, 3, 8]', '[2, 12]', '[2, 7]', 'kleines', 'klein', '{"klein^3e^2s": 1, "kleines^4": 1}', 2, 'FM', '["neutral", 0.0]', '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', 'klein', '["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', '.', '["symbol", null, "."]', 'klitzes', '["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', None, None, None, None, None, None, None, None, None, None)]
            elif item['syntagma'] == ['klitz', 'klein']:
                right_stem_syn = [
                 'klitz', 'klein']
                right_repl = [
                 (
                  42, 10000, '[12, 3, 8]', '[2, 5]', '[2, 3]', 'klitz', 'kli^4tz', 'klitz', 'i', 4, 2, '[2, 3]', 'NE', '["neutral", 0.0]', 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', 'kleinere', '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', 'auswahl', '["NN", null, "auswahl"]', '.', '["symbol", null, "."]', 'klein', '["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', '.', '["symbol", null, "."]', 'klitzes', '["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', 'kleines', '["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None),
                 (
                  43, 10000, '[12, 3, 8]', '[2, 6]', '[2, 3]', 'klitz', 'kli^4tz^3', 'klitz', 'i', 4, 2, '[2, 3]', 'NE', '["neutral", 0.0]', 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', 'kleinere', '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', 'auswahl', '["NN", null, "auswahl"]', '.', '["symbol", null, "."]', 'klein', '["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', '.', '["symbol", null, "."]', 'klitzes', '["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', 'kleines', '["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None),
                 (
                  44, 10000, '[12, 3, 8]', '[2, 6]', '[2, 3]', 'klitz', 'kli^4tz^3', 'klitz', 'z', 3, 4, '[2, 3]', 'NE', '["neutral", 0.0]', 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', 'kleinere', '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', 'auswahl', '["NN", null, "auswahl"]', '.', '["symbol", null, "."]', 'klein', '["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', '.', '["symbol", null, "."]', 'klitzes', '["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', 'kleines', '["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None),
                 (
                  45, 10000, '[12, 3, 8]', '[2, 7]', '[2, 4]', 'klein', 'kle^3i^3n^3', 'klein', 'e', 3, 2, '[2, 4]', 'FM', '["neutral", 0.0]', '.', '["symbol", null, "."]', 'kleinere', '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', 'auswahl', '["NN", null, "auswahl"]', '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', '.', '["symbol", null, "."]', 'klitzes', '["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', 'kleines', '["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None, None),
                 (
                  46, 10000, '[12, 3, 8]', '[2, 7]', '[2, 4]', 'klein', 'kle^3i^3n^3', 'klein', 'i', 3, 3, '[2, 4]', 'FM', '["neutral", 0.0]', '.', '["symbol", null, "."]', 'kleinere', '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', 'auswahl', '["NN", null, "auswahl"]', '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', '.', '["symbol", null, "."]', 'klitzes', '["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', 'kleines', '["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None, None),
                 (
                  47, 10000, '[12, 3, 8]', '[2, 7]', '[2, 4]', 'klein', 'kle^3i^3n^3', 'klein', 'n', 3, 4, '[2, 4]', 'FM', '["neutral", 0.0]', '.', '["symbol", null, "."]', 'kleinere', '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', 'auswahl', '["NN", null, "auswahl"]', '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', '.', '["symbol", null, "."]', 'klitzes', '["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', 'kleines', '["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None, None),
                 (
                  48, 10000, '[12, 3, 8]', '[2, 8]', '[2, 4]', 'klein', 'klein^5', 'klein', 'n', 5, 4, '[2, 4]', 'FM', '["neutral", 0.0]', '.', '["symbol", null, "."]', 'kleinere', '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', 'auswahl', '["NN", null, "auswahl"]', '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', '.', '["symbol", null, "."]', 'klitzes', '["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', 'kleines', '["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None, None)]
                right_syntagma = [
                 'klitz', 'klein']
                right_baseline = (
                 [
                  [
                   'klitz', 'klein'], 'klitz++klein', 2, 1, '[2, 2]', '[3, 4]', '[1, 1]', '[3, 2]', '1', '1'],)
                right_redu = [
                 (
                  13, 10000, '[12, 3, 8]', '[2, 4]', '[2, 3]', 'klitz', 'klitz', '{"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}', 3, 'NE', '["neutral", 0.0]', 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', 'kleinere', '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', 'auswahl', '["NN", null, "auswahl"]', '.', '["symbol", null, "."]', 'klein', '["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', '.', '["symbol", null, "."]', 'klitzes', '["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', 'kleines', '["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None),
                 (
                  14, 10000, '[12, 3, 8]', '[2, 7]', '[2, 4]', 'klein', 'klein', '{"kle^3i^3n^3": 1, "klein^5": 1}', 2, 'FM', '["neutral", 0.0]', '.', '["symbol", null, "."]', 'kleinere', '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', 'auswahl', '["NN", null, "auswahl"]', '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', '.', '["symbol", null, "."]', 'klitzes', '["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', 'kleines', '["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None, None)]
            elif item['syntagma'] == ['klitze', 'kleine']:
                right_stem_syn = [
                 'klitz', 'klein']
                right_repl = [
                 (
                  1, 8888, '[4, 11]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze^7', 'klitz', 'i', 4, 2, '[0, 0]', 'NN', '["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, 'kleine', '["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]'),
                 (
                  2, 8888, '[4, 11]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze^7', 'klitz', 'e', 7, 5, '[0, 0]', 'NN', '["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, 'kleine', '["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]'),
                 (
                  20, 10000, '[12, 3, 8]', '[0, 1]', '[0, 1]', 'klitze', 'klitze^4', 'klitz', 'e', 4, 5, None, 'ADJA', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'eine', '["ART", null, "ein"]', 'kleine', '["ADJA", null, "klein"]', 'überaschung', '["NN", null, "uberasch"]', '@schönesleben', '["mention", null, "@schonesleb"]', '#machwasdaraus', '["hashtag", null, "#machwasdaraus"]', '#bewegedeinarsch', '["hashtag", null, "#bewegedeinarsch"]'),
                 (
                  3, 8888, '[4, 11]', '[0, 2]', '[0, 1]', 'kleine', 'kle^5in^5e', 'klein', 'e', 5, 2, '[0, 1]', 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]', 'sie', '["PPER", null, "sie"]'),
                 (
                  4, 8888, '[4, 11]', '[0, 2]', '[0, 1]', 'kleine', 'kle^5in^5e', 'klein', 'n', 5, 4, '[0, 1]', 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]', 'sie', '["PPER", null, "sie"]'),
                 (
                  5, 8888, '[4, 11]', '[0, 3]', '[0, 1]', 'kleine', 'klein^3e', 'klein', 'n', 3, 4, '[0, 1]', 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]', 'sie', '["PPER", null, "sie"]'),
                 (
                  21, 10000, '[12, 3, 8]', '[0, 2]', '[0, 2]', 'kleine', 'kle^5ine', 'klein', 'e', 5, 2, None, 'ADJA', '["neutral", 0.0]', None, None, None, None, None, None, 'eine', '["ART", null, "ein"]', 'klitze', '["ADJA", null, "klitz"]', 'überaschung', '["NN", null, "uberasch"]', '@schönesleben', '["mention", null, "@schonesleb"]', '#machwasdaraus', '["hashtag", null, "#machwasdaraus"]', '#bewegedeinarsch', '["hashtag", null, "#bewegedeinarsch"]', 'https://www.freiesinternet.de', '["URL", null, "https://www.freiesinternet.d"]')]
                right_syntagma = [
                 'klitze', 'kleine']
                right_baseline = (
                 [
                  [
                   'klitze', 'kleine'], 'klitz++klein', 2, 4, '[2, 3]', '[3, 4]', '[1, 1]', '[2, 2]', '2', '1'],)
                right_redu = [
                 (
                  1, 8888, '[4, 11]', '[0, 0]', '[0, 0]', 'klitze', 'klitz', '{"klitze": 1, "kli^4tze^7": 1}', 2, 'NN', '["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, 'kleine', '["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]'),
                 (
                  2, 8888, '[4, 11]', '[0, 2]', '[0, 1]', 'kleine', 'klein', '{"kle^5in^5e": 1, "klein^3e": 1}', 2, 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]', 'sie', '["PPER", null, "sie"]')]
            else:
                assert False
            extracted_repl = item['repl']
            extracted_redu = item['redu']
            extracted_baseline = item['baseline']
            extracted_syntagma = item['syntagma']
            assert item['stem_syn'] == ['klitz', 'klein']
            set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
            set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
            set(list(tuple(unicode(elem) for elem in item) for item in extracted_baseline)).should.be.equal(set(list(tuple(unicode(elem) for elem in item) for item in right_baseline)))
            extracted_syntagma.should.be.equal(right_syntagma)

        stats.recompute_syntagma_repetativity_scope(False)
        syntagma = [
         'EMOIMG']
        data = list(stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='pos'))
        extracted_repl = data[0]['repl']
        extracted_redu = data[0]['redu']
        extracted_baseline = data[0]['baseline']
        extracted_syntagma = data[0]['syntagma']
        right_repl = [
         (
          8, 8888, '[4, 11]', '[1, 9]', '[1, 9]', '😀', '😀^5', '😀', '😀', 5, 0, None, 'EMOIMG', '["positive", 0.5]', 'glücklich', '["ADJD", null, "glucklich"]', 'gemacht', '["VVPP", null, "gemacht"]', '!', '["symbol", null, "!"]', ':-)', '["EMOASC", null, ":-)"]', '-)', '["EMOASC", null, "-)"]', '-)', '["EMOASC", {"-)^3": 2}, "-)"]', None, None, None, None, None, None, None, None),
         (
          79, 12222, '[24]', '[0, 15]', '[0, 12]', '😫', '😫^4', '😫', '😫', 4, 0, None, 'EMOIMG', '["neutral", 0.0]', 'mal', '["PTKMA", null, "mal"]', 'gerne', '["ADV", null, "gern"]', 'hate', '["VAFIN", null, "hat"]', '.', '["symbol", null, "."]', 1, '["number", null, "1"]', 1, '["number", null, "1"]', 'du', '["PPER", null, "du"]', 'meintest', '["VVFIN", null, "meint"]', ',', '["symbol", null, ","]', 'es', '["PPER", null, "es"]')]
        right_syntagma = [
         'EMOIMG']
        right_baseline = [
         [
          [
           '😫', '1', 'du'], '😫++1++du', 3, 1, '[1, 1, 0]', '[1, 1, 0]', None, None, None, None], [['😀'], '😀', 1, 1, '1', '1', None, None, '1', None], [['😫', '1', 'du', 'meintest', ',', 'es'], '😫++1++du++meint++,++es', 6, 1, '[1, 1, 0, 0, 0, 0]', '[1, 1, 0, 0, 0, 0]', None, None, None, None], [['😫', '1', 'du', 'meintest'], '😫++1++du++meint', 4, 1, '[1, 1, 0, 0]', '[1, 1, 0, 0]', None, None, None, None], [['😫'], '😫', 1, 1, '1', '1', None, None, '1', None], [['😫', '1'], '😫++1', 2, 1, '[1, 1]', '[1, 1]', None, None, None, None], [['😫', '1', 'du', 'meintest', ','], '😫++1++du++meint++,', 5, 1, '[1, 1, 0, 0, 0]', '[1, 1, 0, 0, 0]', None, None, None, None], [['😀', '-)'], '😀++-)', 2, 1, '[1, 2]', '[1, 2]', '[0, 1]', '[0, 2]', None, None]]
        right_redu = []
        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list(tuple(unicode(elem) for elem in item) for item in extracted_baseline)).should.be.equal(set(list(tuple(unicode(elem) for elem in item) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)
        syntagma = [
         'EMOASC', 'EMOIMG']
        data = list(stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='pos'))
        extracted_repl = data[0]['repl']
        extracted_redu = data[0]['redu']
        extracted_baseline = data[0]['baseline']
        extracted_syntagma = data[0]['syntagma']
        right_repl = [
         (
          7, 8888, '[4, 11]', '[1, 8]', '[1, 8]', '-)', '-)^3', '-)', ')', 3, 1, None, 'EMOASC', '["positive", 0.5]', 'mich', '["PPER", null, "mich"]', 'glücklich', '["ADJD", null, "glucklich"]', 'gemacht', '["VVPP", null, "gemacht"]', '!', '["symbol", null, "!"]', ':-)', '["EMOASC", null, ":-)"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]', '-)', '["EMOASC", {"-)^3": 2}, "-)"]', None, None, None, None, None, None),
         (
          8, 8888, '[4, 11]', '[1, 9]', '[1, 9]', '😀', '😀^5', '😀', '😀', 5, 0, None, 'EMOIMG', '["positive", 0.5]', 'glücklich', '["ADJD", null, "glucklich"]', 'gemacht', '["VVPP", null, "gemacht"]', '!', '["symbol", null, "!"]', ':-)', '["EMOASC", null, ":-)"]', '-)', '["EMOASC", null, "-)"]', '-)', '["EMOASC", {"-)^3": 2}, "-)"]', None, None, None, None, None, None, None, None)]
        right_syntagma = [
         'EMOASC', 'EMOIMG']
        right_baseline = [
         [
          [
           '-)', '😀'], '-)++😀', 2, 1, '[1, 1]', '[1, 1]', None, None, None, None], [['😀'], '😀', 1, 1, '1', '1', None, None, '1', None], [['😀', '-)'], '😀++-)', 2, 1, '[1, 2]', '[1, 2]', '[0, 1]', '[0, 2]', None, None], [['-)', '😀', '-)'], '-)++😀++-)', 3, 1, '[3, 1, "IGNOR"]', '[3, 1, "IGNOR"]', '[1, 0, "IGNOR"]', '[2, 0, "IGNOR"]', None, None], [['-)'], '-)', 1, 3, '3', '3', '1', '2', '3', '1']]
        right_redu = []
        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list(tuple(unicode(elem) for elem in item) for item in extracted_baseline)).should.be.equal(set(list(tuple(unicode(elem) for elem in item) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)
        syntagma = [
         'EMOASC']
        data = list(stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment='positive', syntagma_type='pos'))
        extracted_repl = data[0]['repl']
        extracted_redu = data[0]['redu']
        extracted_baseline = data[0]['baseline']
        extracted_syntagma = data[0]['syntagma']
        right_repl = [
         (
          9, 8888, '[4, 11]', '[1, 10]', '[1, 10]', '-)', '-)^3', '-)', ')', 3, 1, '[1, 10]', 'EMOASC', '["positive", 0.5]', 'gemacht', '["VVPP", null, "gemacht"]', '!', '["symbol", null, "!"]', ':-)', '["EMOASC", null, ":-)"]', '-)', '["EMOASC", null, "-)"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]', None, None, None, None, None, None, None, None, None, None),
         (
          10, 8888, '[4, 11]', '[1, 11]', '[1, 10]', '-)', '-)^3', '-)', ')', 3, 1, '[1, 10]', 'EMOASC', '["positive", 0.5]', 'gemacht', '["VVPP", null, "gemacht"]', '!', '["symbol", null, "!"]', ':-)', '["EMOASC", null, ":-)"]', '-)', '["EMOASC", null, "-)"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]', None, None, None, None, None, None, None, None, None, None),
         (
          6, 8888, '[4, 11]', '[1, 7]', '[1, 7]', ':-)', ':-)^4', ':-)', ')', 4, 2, None, 'EMOASC', '["positive", 0.5]', 'sie', '["PPER", null, "sie"]', 'mich', '["PPER", null, "mich"]', 'glücklich', '["ADJD", null, "glucklich"]', 'gemacht', '["VVPP", null, "gemacht"]', '!', '["symbol", null, "!"]', '-)', '["EMOASC", null, "-)"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]', '-)', '["EMOASC", {"-)^3": 2}, "-)"]', None, None, None, None),
         (
          7, 8888, '[4, 11]', '[1, 8]', '[1, 8]', '-)', '-)^3', '-)', ')', 3, 1, None, 'EMOASC', '["positive", 0.5]', 'mich', '["PPER", null, "mich"]', 'glücklich', '["ADJD", null, "glucklich"]', 'gemacht', '["VVPP", null, "gemacht"]', '!', '["symbol", null, "!"]', ':-)', '["EMOASC", null, ":-)"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]', '-)', '["EMOASC", {"-)^3": 2}, "-)"]', None, None, None, None, None, None)]
        right_syntagma = [
         'EMOASC']
        right_baseline = [
         [
          [
           '-)', '😀'], '-)++😀', 2, 1, '[1, 1]', '[1, 1]', None, None, None, None], [[':-)', '-)', '😀'], ':-)++-)++😀', 3, 1, '[1, 1, 1]', '[1, 1, 1]', None, None, None, None], [[':-)', '-)'], ':-)++-)', 2, 1, '[1, 1]', '[1, 1]', None, None, None, None], [['-)'], '-)', 1, 3, '3', '3', '1', '2', '3', '1'], [[':-)'], ':-)', 1, 1, '1', '1', None, None, '1', None], [[':-)', '-)', '😀', '-)'], ':-)++-)++😀++-)', 4, 1, '[1, 3, 1, "IGNOR"]', '[1, 3, 1, "IGNOR"]', '[0, 1, 0, "IGNOR"]', '[0, 2, 0, "IGNOR"]', None, None], [['-)', '😀', '-)'], '-)++😀++-)', 3, 1, '[3, 1, "IGNOR"]', '[3, 1, "IGNOR"]', '[1, 0, "IGNOR"]', '[2, 0, "IGNOR"]', None, None]]
        right_redu = [
         (
          3, 8888, '[4, 11]', '[1, 10]', '[1, 10]', '-)', '-)', '{"-)^3": 2}', 2, 'EMOASC', '["positive", 0.5]', 'gemacht', '["VVPP", null, "gemacht"]', '!', '["symbol", null, "!"]', ':-)', '["EMOASC", null, ":-)"]', '-)', '["EMOASC", null, "-)"]', '😀', '["EMOIMG", null, "\\ud83d\\ude00"]', None, None, None, None, None, None, None, None, None, None)]
        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list(tuple(unicode(elem) for elem in item) for item in extracted_baseline)).should.be.equal(set(list(tuple(unicode(elem) for elem in item) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)
        syntagma = [
         'klein']
        items = list(stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type='lexem', stemmed_search=True))
        for item in items:
            if item['syntagma'] == ['kleines']:
                right_stem_syn = [
                 'klein']
                right_repl = [
                 (
                  52, 10000, '[12, 3, 8]', '[2, 12]', '[2, 7]', 'kleines', 'klein^3e^2s', 'klein', 'n', 3, 4, '[2, 7]', 'FM', '["neutral", 0.0]', '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', 'klein', '["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', '.', '["symbol", null, "."]', 'klitzes', '["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', None, None, None, None, None, None, None, None, None, None),
                 (
                  53, 10000, '[12, 3, 8]', '[2, 13]', '[2, 7]', 'kleines', 'kleines^4', 'klein', 's', 4, 6, '[2, 7]', 'FM', '["neutral", 0.0]', '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', 'klein', '["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', '.', '["symbol", null, "."]', 'klitzes', '["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', None, None, None, None, None, None, None, None, None, None),
                 (
                  66, 11111, '[5, 6, 15, 3]', '[3, 0]', '[3, 0]', 'kleines', 'kleine^4s^7', 'klein', 'e', 4, 5, '[3, 0]', 'NN', '["neutral", 0.0]', 3, '["number", null, "3"]', 4, '["number", null, "4"]', 5, '["number", null, "5"]', 6, '["number", null, "6"]', '.', '["symbol", null, "."]', 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', None, None, None, None, None, None),
                 (
                  67, 11111, '[5, 6, 15, 3]', '[3, 0]', '[3, 0]', 'kleines', 'kleine^4s^7', 'klein', 's', 7, 6, '[3, 0]', 'NN', '["neutral", 0.0]', 3, '["number", null, "3"]', 4, '["number", null, "4"]', 5, '["number", null, "5"]', 6, '["number", null, "6"]', '.', '["symbol", null, "."]', 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', None, None, None, None, None, None),
                 (
                  68, 11111, '[5, 6, 15, 3]', '[3, 1]', '[3, 0]', 'kleines', 'klein^4e^3s^4', 'klein', 'n', 4, 4, '[3, 0]', 'NN', '["neutral", 0.0]', 3, '["number", null, "3"]', 4, '["number", null, "4"]', 5, '["number", null, "5"]', 6, '["number", null, "6"]', '.', '["symbol", null, "."]', 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', None, None, None, None, None, None),
                 (
                  69, 11111, '[5, 6, 15, 3]', '[3, 1]', '[3, 0]', 'kleines', 'klein^4e^3s^4', 'klein', 'e', 3, 5, '[3, 0]', 'NN', '["neutral", 0.0]', 3, '["number", null, "3"]', 4, '["number", null, "4"]', 5, '["number", null, "5"]', 6, '["number", null, "6"]', '.', '["symbol", null, "."]', 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', None, None, None, None, None, None),
                 (
                  70, 11111, '[5, 6, 15, 3]', '[3, 1]', '[3, 0]', 'kleines', 'klein^4e^3s^4', 'klein', 's', 4, 6, '[3, 0]', 'NN', '["neutral", 0.0]', 3, '["number", null, "3"]', 4, '["number", null, "4"]', 5, '["number", null, "5"]', 6, '["number", null, "6"]', '.', '["symbol", null, "."]', 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', None, None, None, None, None, None),
                 (
                  71, 11111, '[5, 6, 15, 3]', '[3, 2]', '[3, 0]', 'kleines', 'kle^4i^5n^3e^2s^3', 'klein', 'e', 4, 2, '[3, 0]', 'NN', '["neutral", 0.0]', 3, '["number", null, "3"]', 4, '["number", null, "4"]', 5, '["number", null, "5"]', 6, '["number", null, "6"]', '.', '["symbol", null, "."]', 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', None, None, None, None, None, None),
                 (
                  72, 11111, '[5, 6, 15, 3]', '[3, 2]', '[3, 0]', 'kleines', 'kle^4i^5n^3e^2s^3', 'klein', 'i', 5, 3, '[3, 0]', 'NN', '["neutral", 0.0]', 3, '["number", null, "3"]', 4, '["number", null, "4"]', 5, '["number", null, "5"]', 6, '["number", null, "6"]', '.', '["symbol", null, "."]', 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', None, None, None, None, None, None),
                 (
                  73, 11111, '[5, 6, 15, 3]', '[3, 2]', '[3, 0]', 'kleines', 'kle^4i^5n^3e^2s^3', 'klein', 'n', 3, 4, '[3, 0]', 'NN', '["neutral", 0.0]', 3, '["number", null, "3"]', 4, '["number", null, "4"]', 5, '["number", null, "5"]', 6, '["number", null, "6"]', '.', '["symbol", null, "."]', 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', None, None, None, None, None, None),
                 (
                  74, 11111, '[5, 6, 15, 3]', '[3, 2]', '[3, 0]', 'kleines', 'kle^4i^5n^3e^2s^3', 'klein', 's', 3, 6, '[3, 0]', 'NN', '["neutral", 0.0]', 3, '["number", null, "3"]', 4, '["number", null, "4"]', 5, '["number", null, "5"]', 6, '["number", null, "6"]', '.', '["symbol", null, "."]', 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', None, None, None, None, None, None),
                 (
                  26, 10000, '[12, 3, 8]', '[1, 0]', '[1, 0]', 'kleines', 'kleine^4s^7', 'klein', 'e', 4, 5, '[1, 0]', 'NN', '["neutral", 0.0]', 'https://www.freiesinternet.de', '["URL", null, "https://www.freiesinternet.d"]', 'beser', '["ADJD", null, "bes"]', 'kan', '["FM", {"ka^4n^5": 1, "kan^6": 1}, "kan"]', 'es', '["VVFIN", null, "es"]', '.', '["symbol", null, "."]', 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', 'kleinere', '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', 'auswahl', '["NN", null, "auswahl"]', '.', '["symbol", null, "."]'),
                 (
                  27, 10000, '[12, 3, 8]', '[1, 0]', '[1, 0]', 'kleines', 'kleine^4s^7', 'klein', 's', 7, 6, '[1, 0]', 'NN', '["neutral", 0.0]', 'https://www.freiesinternet.de', '["URL", null, "https://www.freiesinternet.d"]', 'beser', '["ADJD", null, "bes"]', 'kan', '["FM", {"ka^4n^5": 1, "kan^6": 1}, "kan"]', 'es', '["VVFIN", null, "es"]', '.', '["symbol", null, "."]', 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', 'kleinere', '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', 'auswahl', '["NN", null, "auswahl"]', '.', '["symbol", null, "."]'),
                 (
                  28, 10000, '[12, 3, 8]', '[1, 1]', '[1, 0]', 'kleines', 'klein^4e^3s^4', 'klein', 'n', 4, 4, '[1, 0]', 'NN', '["neutral", 0.0]', 'https://www.freiesinternet.de', '["URL", null, "https://www.freiesinternet.d"]', 'beser', '["ADJD", null, "bes"]', 'kan', '["FM", {"ka^4n^5": 1, "kan^6": 1}, "kan"]', 'es', '["VVFIN", null, "es"]', '.', '["symbol", null, "."]', 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', 'kleinere', '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', 'auswahl', '["NN", null, "auswahl"]', '.', '["symbol", null, "."]'),
                 (
                  29, 10000, '[12, 3, 8]', '[1, 1]', '[1, 0]', 'kleines', 'klein^4e^3s^4', 'klein', 'e', 3, 5, '[1, 0]', 'NN', '["neutral", 0.0]', 'https://www.freiesinternet.de', '["URL", null, "https://www.freiesinternet.d"]', 'beser', '["ADJD", null, "bes"]', 'kan', '["FM", {"ka^4n^5": 1, "kan^6": 1}, "kan"]', 'es', '["VVFIN", null, "es"]', '.', '["symbol", null, "."]', 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', 'kleinere', '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', 'auswahl', '["NN", null, "auswahl"]', '.', '["symbol", null, "."]'),
                 (
                  30, 10000, '[12, 3, 8]', '[1, 1]', '[1, 0]', 'kleines', 'klein^4e^3s^4', 'klein', 's', 4, 6, '[1, 0]', 'NN', '["neutral", 0.0]', 'https://www.freiesinternet.de', '["URL", null, "https://www.freiesinternet.d"]', 'beser', '["ADJD", null, "bes"]', 'kan', '["FM", {"ka^4n^5": 1, "kan^6": 1}, "kan"]', 'es', '["VVFIN", null, "es"]', '.', '["symbol", null, "."]', 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', 'kleinere', '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', 'auswahl', '["NN", null, "auswahl"]', '.', '["symbol", null, "."]'),
                 (
                  31, 10000, '[12, 3, 8]', '[1, 2]', '[1, 0]', 'kleines', 'kle^4i^5n^3e^2s^3', 'klein', 'e', 4, 2, '[1, 0]', 'NN', '["neutral", 0.0]', 'https://www.freiesinternet.de', '["URL", null, "https://www.freiesinternet.d"]', 'beser', '["ADJD", null, "bes"]', 'kan', '["FM", {"ka^4n^5": 1, "kan^6": 1}, "kan"]', 'es', '["VVFIN", null, "es"]', '.', '["symbol", null, "."]', 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', 'kleinere', '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', 'auswahl', '["NN", null, "auswahl"]', '.', '["symbol", null, "."]'),
                 (
                  32, 10000, '[12, 3, 8]', '[1, 2]', '[1, 0]', 'kleines', 'kle^4i^5n^3e^2s^3', 'klein', 'i', 5, 3, '[1, 0]', 'NN', '["neutral", 0.0]', 'https://www.freiesinternet.de', '["URL", null, "https://www.freiesinternet.d"]', 'beser', '["ADJD", null, "bes"]', 'kan', '["FM", {"ka^4n^5": 1, "kan^6": 1}, "kan"]', 'es', '["VVFIN", null, "es"]', '.', '["symbol", null, "."]', 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', 'kleinere', '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', 'auswahl', '["NN", null, "auswahl"]', '.', '["symbol", null, "."]'),
                 (
                  33, 10000, '[12, 3, 8]', '[1, 2]', '[1, 0]', 'kleines', 'kle^4i^5n^3e^2s^3', 'klein', 'n', 3, 4, '[1, 0]', 'NN', '["neutral", 0.0]', 'https://www.freiesinternet.de', '["URL", null, "https://www.freiesinternet.d"]', 'beser', '["ADJD", null, "bes"]', 'kan', '["FM", {"ka^4n^5": 1, "kan^6": 1}, "kan"]', 'es', '["VVFIN", null, "es"]', '.', '["symbol", null, "."]', 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', 'kleinere', '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', 'auswahl', '["NN", null, "auswahl"]', '.', '["symbol", null, "."]'),
                 (
                  34, 10000, '[12, 3, 8]', '[1, 2]', '[1, 0]', 'kleines', 'kle^4i^5n^3e^2s^3', 'klein', 's', 3, 6, '[1, 0]', 'NN', '["neutral", 0.0]', 'https://www.freiesinternet.de', '["URL", null, "https://www.freiesinternet.d"]', 'beser', '["ADJD", null, "bes"]', 'kan', '["FM", {"ka^4n^5": 1, "kan^6": 1}, "kan"]', 'es', '["VVFIN", null, "es"]', '.', '["symbol", null, "."]', 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', 'kleinere', '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', 'auswahl', '["NN", null, "auswahl"]', '.', '["symbol", null, "."]')]
                right_syntagma = [
                 'kleines']
                right_baseline = (
                 [
                  [
                   'kleines'], 'klein', 1, 8, '8', '20', '3', '8', '8', '3'],)
                right_redu = [
                 (
                  16, 10000, '[12, 3, 8]', '[2, 12]', '[2, 7]', 'kleines', 'klein', '{"klein^3e^2s": 1, "kleines^4": 1}', 2, 'FM', '["neutral", 0.0]', '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', 'klein', '["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', '.', '["symbol", null, "."]', 'klitzes', '["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', None, None, None, None, None, None, None, None, None, None),
                 (
                  17, 11111, '[5, 6, 15, 3]', '[3, 0]', '[3, 0]', 'kleines', 'klein', '{"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}', 3, 'NN', '["neutral", 0.0]', 3, '["number", null, "3"]', 4, '["number", null, "4"]', 5, '["number", null, "5"]', 6, '["number", null, "6"]', '.', '["symbol", null, "."]', 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', None, None, None, None, None, None),
                 (
                  11, 10000, '[12, 3, 8]', '[1, 0]', '[1, 0]', 'kleines', 'klein', '{"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}', 3, 'NN', '["neutral", 0.0]', 'https://www.freiesinternet.de', '["URL", null, "https://www.freiesinternet.d"]', 'beser', '["ADJD", null, "bes"]', 'kan', '["FM", {"ka^4n^5": 1, "kan^6": 1}, "kan"]', 'es', '["VVFIN", null, "es"]', '.', '["symbol", null, "."]', 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', 'kleinere', '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', 'auswahl', '["NN", null, "auswahl"]', '.', '["symbol", null, "."]')]
            elif item['syntagma'] == ['kleinere']:
                right_stem_syn = [
                 'klein']
                right_repl = [
                 (
                  37, 10000, '[12, 3, 8]', '[2, 0]', '[2, 0]', 'kleinere', 'kleinere^5', 'klein', 'e', 5, 7, '[2, 0]', 'NE', '["neutral", 0.0]', 'es', '["VVFIN", null, "es"]', '.', '["symbol", null, "."]', 'kleines', '["NN", {"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}, "klein"]', 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', 'auswahl', '["NN", null, "auswahl"]', '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', 'klein', '["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', '.', '["symbol", null, "."]'),
                 (
                  38, 10000, '[12, 3, 8]', '[2, 1]', '[2, 0]', 'kleinere', 'kleine^3r^2e^5', 'klein', 'e', 3, 5, '[2, 0]', 'NE', '["neutral", 0.0]', 'es', '["VVFIN", null, "es"]', '.', '["symbol", null, "."]', 'kleines', '["NN", {"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}, "klein"]', 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', 'auswahl', '["NN", null, "auswahl"]', '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', 'klein', '["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', '.', '["symbol", null, "."]'),
                 (
                  39, 10000, '[12, 3, 8]', '[2, 1]', '[2, 0]', 'kleinere', 'kleine^3r^2e^5', 'klein', 'e', 5, 7, '[2, 0]', 'NE', '["neutral", 0.0]', 'es', '["VVFIN", null, "es"]', '.', '["symbol", null, "."]', 'kleines', '["NN", {"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}, "klein"]', 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', 'auswahl', '["NN", null, "auswahl"]', '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', 'klein', '["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', '.', '["symbol", null, "."]')]
                right_syntagma = [
                 'kleinere']
                right_baseline = (
                 [
                  [
                   'kleinere'], 'klein', 1, 2, '2', '3', '1', '2', '2', '1'],)
                right_redu = [
                 (
                  12, 10000, '[12, 3, 8]', '[2, 0]', '[2, 0]', 'kleinere', 'klein', '{"kleinere^5": 1, "kleine^3r^2e^5": 1}', 2, 'NE', '["neutral", 0.0]', 'es', '["VVFIN", null, "es"]', '.', '["symbol", null, "."]', 'kleines', '["NN", {"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}, "klein"]', 'mädchen', '["NN", null, "madch"]', '.', '["symbol", null, "."]', 'auswahl', '["NN", null, "auswahl"]', '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', 'klein', '["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', '.', '["symbol", null, "."]')]
            elif item['syntagma'] == ['kleine']:
                right_stem_syn = [
                 'klein']
                right_repl = [
                 (
                  82, 12222, '[24]', '[0, 24]', '[0, 21]', 'kleine', 'kle^4i^5n^4e^8', 'klein', 'e', 4, 2, None, 'ADJA', '["neutral", 0.0]', ',', '["symbol", null, ","]', 'es', '["PPER", null, "es"]', 'war', '["VAFIN", null, "war"]', 'so', '["ADV", null, "so"]', 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', None, None, None, None, None, None),
                 (
                  83, 12222, '[24]', '[0, 24]', '[0, 21]', 'kleine', 'kle^4i^5n^4e^8', 'klein', 'i', 5, 3, None, 'ADJA', '["neutral", 0.0]', ',', '["symbol", null, ","]', 'es', '["PPER", null, "es"]', 'war', '["VAFIN", null, "war"]', 'so', '["ADV", null, "so"]', 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', None, None, None, None, None, None),
                 (
                  84, 12222, '[24]', '[0, 24]', '[0, 21]', 'kleine', 'kle^4i^5n^4e^8', 'klein', 'n', 4, 4, None, 'ADJA', '["neutral", 0.0]', ',', '["symbol", null, ","]', 'es', '["PPER", null, "es"]', 'war', '["VAFIN", null, "war"]', 'so', '["ADV", null, "so"]', 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', None, None, None, None, None, None),
                 (
                  85, 12222, '[24]', '[0, 24]', '[0, 21]', 'kleine', 'kle^4i^5n^4e^8', 'klein', 'e', 8, 5, None, 'ADJA', '["neutral", 0.0]', ',', '["symbol", null, ","]', 'es', '["PPER", null, "es"]', 'war', '["VAFIN", null, "war"]', 'so', '["ADV", null, "so"]', 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', None, None, None, None, None, None),
                 (
                  3, 8888, '[4, 11]', '[0, 2]', '[0, 1]', 'kleine', 'kle^5in^5e', 'klein', 'e', 5, 2, '[0, 1]', 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]', 'sie', '["PPER", null, "sie"]'),
                 (
                  4, 8888, '[4, 11]', '[0, 2]', '[0, 1]', 'kleine', 'kle^5in^5e', 'klein', 'n', 5, 4, '[0, 1]', 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]', 'sie', '["PPER", null, "sie"]'),
                 (
                  5, 8888, '[4, 11]', '[0, 3]', '[0, 1]', 'kleine', 'klein^3e', 'klein', 'n', 3, 4, '[0, 1]', 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]', 'sie', '["PPER", null, "sie"]'),
                 (
                  21, 10000, '[12, 3, 8]', '[0, 2]', '[0, 2]', 'kleine', 'kle^5ine', 'klein', 'e', 5, 2, None, 'ADJA', '["neutral", 0.0]', None, None, None, None, None, None, 'eine', '["ART", null, "ein"]', 'klitze', '["ADJA", null, "klitz"]', 'überaschung', '["NN", null, "uberasch"]', '@schönesleben', '["mention", null, "@schonesleb"]', '#machwasdaraus', '["hashtag", null, "#machwasdaraus"]', '#bewegedeinarsch', '["hashtag", null, "#bewegedeinarsch"]', 'https://www.freiesinternet.de', '["URL", null, "https://www.freiesinternet.d"]'),
                 (
                  57, 11111, '[5, 6, 15, 3]', '[2, 4]', '[2, 4]', 'kleine', 'kle^5i^2n^4e^5', 'klein', 'e', 5, 2, None, 'ADJA', '["neutral", 0.0]', '!', '["symbol", null, "!"]', 'weil', '["KOUS", null, "weil"]', 'es', '["PPER", null, "es"]', 'ja', '["PTKMA", null, "ja"]', 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', 'ist', '["VAFIN", null, "ist"]', '.', '["symbol", null, "."]', 1, '["number", null, "1"]', 2, '["number", null, "2"]'),
                 (
                  58, 11111, '[5, 6, 15, 3]', '[2, 4]', '[2, 4]', 'kleine', 'kle^5i^2n^4e^5', 'klein', 'n', 4, 4, None, 'ADJA', '["neutral", 0.0]', '!', '["symbol", null, "!"]', 'weil', '["KOUS", null, "weil"]', 'es', '["PPER", null, "es"]', 'ja', '["PTKMA", null, "ja"]', 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', 'ist', '["VAFIN", null, "ist"]', '.', '["symbol", null, "."]', 1, '["number", null, "1"]', 2, '["number", null, "2"]'),
                 (
                  59, 11111, '[5, 6, 15, 3]', '[2, 4]', '[2, 4]', 'kleine', 'kle^5i^2n^4e^5', 'klein', 'e', 5, 5, None, 'ADJA', '["neutral", 0.0]', '!', '["symbol", null, "!"]', 'weil', '["KOUS", null, "weil"]', 'es', '["PPER", null, "es"]', 'ja', '["PTKMA", null, "ja"]', 'eine', '["ART", null, "ein"]', 'überaschung', '["NN", null, "uberasch"]', 'ist', '["VAFIN", null, "ist"]', '.', '["symbol", null, "."]', 1, '["number", null, "1"]', 2, '["number", null, "2"]')]
                right_syntagma = [
                 'kleine']
                right_baseline = (
                 [
                  [
                   'kleine'], 'klein', 1, 7, '5', '11', '1', '2', '5', '1'],)
                right_redu = [
                 (
                  2, 8888, '[4, 11]', '[0, 2]', '[0, 1]', 'kleine', 'klein', '{"kle^5in^5e": 1, "klein^3e": 1}', 2, 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', 'überaschung', '["NN", null, "uberasch"]', '.', '["symbol", null, "."]', 'trotzdem', '["PAV", null, "trotzd"]', 'hat', '["VAFIN", null, "hat"]', 'sie', '["PPER", null, "sie"]')]
            elif item['syntagma'] == ['klein']:
                right_stem_syn = [
                 'klein']
                right_repl = [
                 (
                  45, 10000, '[12, 3, 8]', '[2, 7]', '[2, 4]', 'klein', 'kle^3i^3n^3', 'klein', 'e', 3, 2, '[2, 4]', 'FM', '["neutral", 0.0]', '.', '["symbol", null, "."]', 'kleinere', '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', 'auswahl', '["NN", null, "auswahl"]', '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', '.', '["symbol", null, "."]', 'klitzes', '["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', 'kleines', '["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None, None),
                 (
                  46, 10000, '[12, 3, 8]', '[2, 7]', '[2, 4]', 'klein', 'kle^3i^3n^3', 'klein', 'i', 3, 3, '[2, 4]', 'FM', '["neutral", 0.0]', '.', '["symbol", null, "."]', 'kleinere', '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', 'auswahl', '["NN", null, "auswahl"]', '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', '.', '["symbol", null, "."]', 'klitzes', '["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', 'kleines', '["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None, None),
                 (
                  47, 10000, '[12, 3, 8]', '[2, 7]', '[2, 4]', 'klein', 'kle^3i^3n^3', 'klein', 'n', 3, 4, '[2, 4]', 'FM', '["neutral", 0.0]', '.', '["symbol", null, "."]', 'kleinere', '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', 'auswahl', '["NN", null, "auswahl"]', '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', '.', '["symbol", null, "."]', 'klitzes', '["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', 'kleines', '["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None, None),
                 (
                  48, 10000, '[12, 3, 8]', '[2, 8]', '[2, 4]', 'klein', 'klein^5', 'klein', 'n', 5, 4, '[2, 4]', 'FM', '["neutral", 0.0]', '.', '["symbol", null, "."]', 'kleinere', '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', 'auswahl', '["NN", null, "auswahl"]', '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', '.', '["symbol", null, "."]', 'klitzes', '["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', 'kleines', '["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None, None)]
                right_syntagma = [
                 'klein']
                right_baseline = (
                 [
                  [
                   'klein'], 'klein', 1, 2, '2', '4', '1', '2', '2', '1'],)
                right_redu = [
                 (
                  14, 10000, '[12, 3, 8]', '[2, 7]', '[2, 4]', 'klein', 'klein', '{"kle^3i^3n^3": 1, "klein^5": 1}', 2, 'FM', '["neutral", 0.0]', '.', '["symbol", null, "."]', 'kleinere', '["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', 'auswahl', '["NN", null, "auswahl"]', '.', '["symbol", null, "."]', 'klitz', '["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', '.', '["symbol", null, "."]', 'klitzes', '["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', 'kleines', '["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None, None)]
            else:
                assert False
            extracted_repl = item['repl']
            extracted_redu = item['redu']
            extracted_baseline = item['baseline']
            extracted_syntagma = item['syntagma']
            item['stem_syn'] = [
             'klein']
            set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
            set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
            set(list(tuple(unicode(elem) for elem in item) for item in extracted_baseline)).should.be.equal(set(list(tuple(unicode(elem) for elem in item) for item in right_baseline)))
            extracted_syntagma.should.be.equal(right_syntagma)

        return

    @attr(status='stable')
    def test_test_get_header_for_exhausted_output_table_type_612_1(self):
        self.prj_folder()
        self.test_dbs()
        stats = Stats(mode='silent', use_cash=True)
        stats.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_stats_de))
        cols = stats._get_header_exhausted(repl=False, redu=False, baseline=False, additional_doc_cols=False, context_len_left=True, context_len_right=True)
        assert not cols
        cols = stats._get_header_exhausted(repl=True, redu=False, baseline=False, additional_doc_cols=False, context_len_left=True, context_len_right=True)
        assert not cols
        cols = stats._get_header_exhausted(repl=True, redu=False, baseline=False, additional_doc_cols=False, context_len_left=True, context_len_right=True)
        assert not cols
        cols = stats._get_header_exhausted(repl=True, redu=False, baseline=True, additional_doc_cols=False, context_len_left=1, context_len_right=1)
        cols['repl'].should.be.equal(('id', 'index_in_corpus', 'index_in_redufree',
                                      'repl_letter', 'repl_length', 'index_of_repl',
                                      'in_redu'))
        assert not cols['redu']
        cols['word'].should.be.equal(('normalized_word', 'rle_word', 'stemmed', 'pos',
                                      'polarity'))
        cols['document'].should.be.equal((('doc_id', 'redufree_len'), None))
        cols['context'].should.be.equal(('contextL1', 'context_infoL1', 'contextR1',
                                         'context_infoR1'))
        cols['baseline'].should.be.equal(('syntagma', 'stemmed', 'scope', 'occur_syntagma_all',
                                          'occur_repl_uniq', 'occur_repl_exhausted',
                                          'occur_full_syn_repl'))
        cols = stats._get_header_exhausted(repl=True, redu=False, baseline=False, additional_doc_cols=False, context_len_left=False, context_len_right=False)
        assert not cols
        cols = stats._get_header_exhausted(repl=True, redu=False, baseline=False, additional_doc_cols=['gender', 'sex'], context_len_left=False, context_len_right=False)
        assert not cols
        cols = stats._get_header_exhausted(repl=False, redu=True, baseline=False, additional_doc_cols=False, context_len_left=True, context_len_right=True)
        assert not cols
        cols = stats._get_header_exhausted(repl=False, redu=True, baseline=True, additional_doc_cols=False, context_len_left=True, context_len_right=True)
        assert not cols['repl']
        cols['redu'].should.be.equal(('id', 'index_in_corpus', 'index_in_redufree',
                                      'orig_words', 'redu_length'))
        cols['word'].should.be.equal(('normalized_word', 'stemmed', 'pos', 'polarity'))
        cols['document'].should.be.equal((('doc_id', 'redufree_len'), None))
        cols['context'].should.be.equal(('contextL5', 'context_infoL5', 'contextL4',
                                         'context_infoL4', 'contextL3', 'context_infoL3',
                                         'contextL2', 'context_infoL2', 'contextL1',
                                         'context_infoL1', 'contextR1', 'context_infoR1',
                                         'contextR2', 'context_infoR2', 'contextR3',
                                         'context_infoR3', 'contextR4', 'context_infoR4',
                                         'contextR5', 'context_infoR5'))
        cols['baseline'].should.be.equal(('syntagma', 'stemmed', 'scope', 'occur_syntagma_all',
                                          'occur_redu_uniq', 'occur_redu_exhausted',
                                          'occur_full_syn_redu'))
        cols = stats._get_header_exhausted(repl=True, redu=True, baseline=False, additional_doc_cols=False, context_len_left=True, context_len_right=True)
        assert not cols
        cols = stats._get_header_exhausted(repl=True, redu=True, baseline=True, additional_doc_cols=False, context_len_left=True, context_len_right=True)
        cols['repl'].should.be.equal(('id', 'index_in_corpus', 'index_in_redufree',
                                      'repl_letter', 'repl_length', 'index_of_repl',
                                      'in_redu'))
        cols['redu'].should.be.equal(('id', 'index_in_corpus', 'index_in_redufree',
                                      'orig_words', 'redu_length'))
        cols['word'].should.be.equal(('normalized_word', 'rle_word', 'stemmed', 'pos',
                                      'polarity'))
        cols['document'].should.be.equal((('doc_id', 'redufree_len'), None))
        cols['context'].should.be.equal(('contextL5', 'context_infoL5', 'contextL4',
                                         'context_infoL4', 'contextL3', 'context_infoL3',
                                         'contextL2', 'context_infoL2', 'contextL1',
                                         'context_infoL1', 'contextR1', 'context_infoR1',
                                         'contextR2', 'context_infoR2', 'contextR3',
                                         'context_infoR3', 'contextR4', 'context_infoR4',
                                         'contextR5', 'context_infoR5'))
        cols['baseline'].should.be.equal(('syntagma', 'stemmed', 'scope', 'occur_syntagma_all',
                                          'occur_repl_uniq', 'occur_repl_exhausted',
                                          'occur_redu_uniq', 'occur_redu_exhausted',
                                          'occur_full_syn_repl', 'occur_full_syn_redu'))
        return

    @attr(status='stable')
    def test_test_get_header_for_sum_output_table_type_612_2(self):
        self.prj_folder()
        self.test_dbs()
        stats = Stats(mode=self.mode, use_cash=True)
        stats.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_stats_de))
        cols = stats._get_header_sum(repl=False, redu=False, word_examples_sum_table=True)
        cols.should.be.equal(False)
        cols = stats._get_header_sum(repl=True, redu=False, word_examples_sum_table=True)
        cols.should.be.equal(('letter', 'NrOfRepl', 'Occur', 'Examples'))
        cols = stats._get_header_sum(repl=True, redu=False, word_examples_sum_table=False)
        cols.should.be.equal(('letter', 'NrOfRepl', 'Occur'))
        cols = stats._get_header_sum(repl=False, redu=True, word_examples_sum_table=True)
        cols.should.be.equal(('word', 'ReduLength', 'Occur'))
        cols = stats._get_header_sum(repl=False, redu=True, word_examples_sum_table=False)
        cols.should.be.equal(('word', 'ReduLength', 'Occur'))

    @attr(status='stable')
    def test_export_613_1(self):
        self.prj_folder()
        self.test_dbs()
        stats = Stats(mode=self.mode, use_cash=True, status_bar=True)
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['stats']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'stats'
        stats.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_stats_de))
        rewrite = True
        stats.export(self.tempdir_project_folder, repl=True, redu=True, export_file_type='csv', output_table_type='exhausted', rewrite=False, max_scope=2)
        stats.export(self.tempdir_project_folder, repl=True, redu=True, export_file_type='xml', output_table_type='exhausted', rewrite=rewrite)
        stats.export(self.tempdir_project_folder, repl=True, redu=True, export_file_type='json', output_table_type='exhausted', rewrite=rewrite)
        stats.export(self.tempdir_project_folder, repl=True, redu=True, export_file_type='csv', output_table_type='exhausted', rewrite=rewrite, additional_doc_cols=[
         'gender', 'working_area', 'age'], fname='WITH_ADDIT_COLS_FROM_CORP', path_to_corpdb=os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_de))
        stats.export(self.tempdir_project_folder, repl=True, redu=True, export_file_type='csv', output_table_type='exhausted', rewrite=rewrite, context_len_left=False, context_len_right=False, fname='NULL_KONTEXT')
        stats.export(self.tempdir_project_folder, repl=True, redu=True, export_file_type='csv', output_table_type='exhausted', rewrite=rewrite, context_len_left=1, context_len_right=2, fname='1_2_KONTEXT_')
        stats.export(self.tempdir_project_folder, repl=True, redu=True, export_file_type='csv', output_table_type='exhausted', rewrite=rewrite, max_scope=1, fname='MAX_SCOPE_VON_ONE')
        stats.export(self.tempdir_project_folder, syntagma=['klitze'], repl=True, redu=True, export_file_type='csv', output_table_type='exhausted', rewrite=rewrite, stemmed_search=True, fname='STEMMED_FOR_KLITZE')
        stats.export(self.tempdir_project_folder, syntagma=['klitze', 'kleine'], repl=True, redu=True, export_file_type='csv', output_table_type='exhausted', rewrite=rewrite, stemmed_search=True, fname='STEMMED_FOR_KLITZE_KLEINE')
        stats.export(self.tempdir_project_folder, syntagma=['klitze', 'kleine'], repl=True, redu=True, export_file_type='csv', output_table_type='exhausted', rewrite=rewrite, stemmed_search=False, fname='UN_STEMMED_FOR_KLITZE_KLEINE')
        stats.export(self.tempdir_project_folder, syntagma=[['klitze', 'kleine'], ['klitzes', 'kleines'], ['klitz', 'klein']], repl=True, redu=True, export_file_type='csv', output_table_type='exhausted', rewrite=rewrite, stemmed_search=False, fname='UN_STEMMED_FOR_ALL_KLITZ_KLEIN')
        stats.export(self.tempdir_project_folder, syntagma=['EMOIMG', 'EMOASC'], repl=True, redu=True, export_file_type='csv', output_table_type='exhausted', rewrite=rewrite, stemmed_search=False, fname='EMOIMG_EMOASC', syntagma_type='pos')
        stats.export(self.tempdir_project_folder, syntagma=['EMOIMG'], repl=True, redu=True, export_file_type='csv', output_table_type='exhausted', rewrite=rewrite, stemmed_search=False, fname='EMOIMG', syntagma_type='pos')
        stats.export(self.tempdir_project_folder, syntagma=['EMOASC'], repl=True, redu=True, export_file_type='csv', output_table_type='exhausted', rewrite=rewrite, stemmed_search=False, fname='EMOASC', syntagma_type='pos')
        stats.export(self.tempdir_project_folder, repl=True, redu=False, export_file_type='csv', output_table_type='sum', fname='SUM_REPL', rewrite=rewrite)
        stats.export(self.tempdir_project_folder, repl=False, redu=True, export_file_type='csv', output_table_type='sum', fname='SUM_REDU', rewrite=rewrite)
        stats.export(self.tempdir_project_folder, syntagma=['EMOIMG'], repl=True, redu=False, export_file_type='csv', rewrite=rewrite, output_table_type='sum', fname='SUM_REPL_EMOIMG', syntagma_type='pos')
        stats.export(self.tempdir_project_folder, syntagma=['EMOASC'], repl=False, redu=True, export_file_type='csv', rewrite=rewrite, output_table_type='sum', fname='SUM_REDU_EMOASC', syntagma_type='pos')
        files = os.listdir(self.tempdir_project_folder)
        len(files).should.be.equal(18)

    @attr(status='stable')
    def test_test_export_generator_structure_613_2(self):
        self.prj_folder()
        self.test_dbs()
        stats = Stats(mode=self.mode, use_cash=True, status_bar=True)
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['stats']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'stats'
        stats.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_stats_de))
        stats.attach_corpdb(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_de))
        repl = True
        redu = True
        baseline = True
        output_table_type = 'exhausted'
        max_scope = False
        additional_doc_cols = ()
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True
        header = stats._get_header(repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type, max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right, word_examples_sum_table=word_examples_sum_table)
        col_num = sum([ sum([ len(doc_cols) for doc_cols in cols if doc_cols ]) if tables_part_name == 'document' else len(cols) for tables_part_name, cols in header.iteritems() if cols ])
        assert col_num == 49
        syntagma = [
         'klitze', 'kleine']
        stemmed_search = False
        data = stats._export_generator(header, inp_syntagma=syntagma, stemmed_search=stemmed_search)
        for row in data:
            if not row:
                continue
            len(row).should.be.equal(col_num)

        repl = True
        redu = True
        baseline = True
        output_table_type = 'exhausted'
        max_scope = False
        additional_doc_cols = ()
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True
        header = stats._get_header(repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type, max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right, word_examples_sum_table=word_examples_sum_table)
        col_num = sum([ sum([ len(doc_cols) for doc_cols in cols if doc_cols ]) if tables_part_name == 'document' else len(cols) for tables_part_name, cols in header.iteritems() if cols ])
        assert col_num == 49
        syntagma = [
         'klitze', 'kleine']
        stemmed_search = True
        data = stats._export_generator(header, inp_syntagma=syntagma, stemmed_search=stemmed_search)
        for row in data:
            if not row:
                continue
            len(row).should.be.equal(col_num)

        repl = True
        redu = True
        baseline = True
        output_table_type = 'exhausted'
        max_scope = False
        additional_doc_cols = ()
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True
        header = stats._get_header(repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type, max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right, word_examples_sum_table=word_examples_sum_table)
        col_num = sum([ sum([ len(doc_cols) for doc_cols in cols if doc_cols ]) if tables_part_name == 'document' else len(cols) for tables_part_name, cols in header.iteritems() if cols ])
        assert col_num == 49
        syntagma = '*'
        stemmed_search = True
        data = stats._export_generator(header, inp_syntagma=syntagma, stemmed_search=stemmed_search)
        for row in data:
            if not row:
                continue
            len(row).should.be.equal(col_num)

        repl = False
        redu = True
        baseline = True
        output_table_type = 'exhausted'
        max_scope = False
        additional_doc_cols = ()
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True
        header = stats._get_header(repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type, max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right, word_examples_sum_table=word_examples_sum_table)
        col_num = sum([ sum([ len(doc_cols) for doc_cols in cols if doc_cols ]) if tables_part_name == 'document' else len(cols) for tables_part_name, cols in header.iteritems() if cols ])
        assert col_num == 38
        syntagma = '*'
        stemmed_search = True
        data = stats._export_generator(header, inp_syntagma=syntagma, stemmed_search=stemmed_search)
        for row in data:
            if not row:
                continue
            len(row).should.be.equal(col_num)

        repl = True
        redu = True
        baseline = True
        output_table_type = 'exhausted'
        max_scope = False
        additional_doc_cols = ()
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True
        header = stats._get_header(repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type, max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right, word_examples_sum_table=word_examples_sum_table)
        col_num = sum([ sum([ len(doc_cols) for doc_cols in cols if doc_cols ]) if tables_part_name == 'document' else len(cols) for tables_part_name, cols in header.iteritems() if cols ])
        assert col_num == 49
        syntagma = '*'
        stemmed_search = True
        data = stats._export_generator(header, inp_syntagma=syntagma, stemmed_search=stemmed_search, sentiment='positive')
        for row in data:
            if not row:
                continue
            len(row).should.be.equal(col_num)

        repl = True
        redu = True
        baseline = True
        output_table_type = 'exhausted'
        max_scope = False
        additional_doc_cols = ()
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True
        header = stats._get_header(repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type, max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right, word_examples_sum_table=word_examples_sum_table)
        col_num = sum([ sum([ len(doc_cols) for doc_cols in cols if doc_cols ]) if tables_part_name == 'document' else len(cols) for tables_part_name, cols in header.iteritems() if cols ])
        assert col_num == 49
        rows_equal = []
        rows_not_equal = []
        counter2 = 0
        syntagma = [['klitzes', 'kleines'], ['klitz', 'klein'], ['klitze', 'kleine']]
        stemmed_search = False
        data = stats._export_generator(header, inp_syntagma=syntagma, stemmed_search=stemmed_search)
        for row in data:
            if row:
                rows_equal.append(row)
                counter2 += 1
                len(row).should.be.equal(col_num)

        counter1 = 0
        syntagma = ['klitze', 'kleine']
        stemmed_search = True
        data = stats._export_generator(header, inp_syntagma=syntagma, stemmed_search=stemmed_search)
        rows = []
        for row in data:
            if row:
                if not row:
                    continue
                counter1 += 1
                len(row).should.be.equal(col_num)
                if row not in rows_equal:
                    rows_not_equal.append(row)

        counter1.should.be.equal(counter2)
        assert not rows_not_equal
        repl = True
        redu = True
        baseline = True
        output_table_type = 'exhausted'
        max_scope = False
        additional_doc_cols = ()
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True
        header = stats._get_header(repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type, max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right, word_examples_sum_table=word_examples_sum_table)
        col_num = sum([ sum([ len(doc_cols) for doc_cols in cols if doc_cols ]) if tables_part_name == 'document' else len(cols) for tables_part_name, cols in header.iteritems() if cols ])
        if not col_num == 49:
            raise AssertionError
            syntagma = [
             [
              'klitze', 'kleine']]
            stemmed_search = True
            data = stats._export_generator(header, inp_syntagma=syntagma, stemmed_search=stemmed_search, sentiment='neutral')
            assert data or False
        i = 0
        for row in data:
            if not row:
                continue
            i += 1
            len(row).should.be.equal(col_num)

        repl = True
        redu = False
        baseline = True
        output_table_type = 'exhausted'
        max_scope = False
        additional_doc_cols = ()
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True
        header = stats._get_header(repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type, max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right, word_examples_sum_table=word_examples_sum_table)
        col_num = sum([ sum([ len(doc_cols) for doc_cols in cols if doc_cols ]) if tables_part_name == 'document' else len(cols) for tables_part_name, cols in header.iteritems() if cols ])
        assert col_num == 41
        syntagma = [
         'klitze', 'kleine']
        stemmed_search = False
        data = stats._export_generator(header, inp_syntagma=syntagma, stemmed_search=stemmed_search)
        for row in data:
            if not row:
                continue
            len(row).should.be.equal(col_num)

        repl = False
        redu = True
        baseline = True
        output_table_type = 'exhausted'
        max_scope = False
        additional_doc_cols = ()
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True
        header = stats._get_header(repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type, max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right, word_examples_sum_table=word_examples_sum_table)
        col_num = sum([ sum([ len(doc_cols) for doc_cols in cols if doc_cols ]) if tables_part_name == 'document' else len(cols) for tables_part_name, cols in header.iteritems() if cols ])
        assert col_num == 38
        syntagma = [
         'klitze', 'kleine']
        stemmed_search = False
        data = stats._export_generator(header, inp_syntagma=syntagma, stemmed_search=stemmed_search)
        for row in data:
            if not row:
                continue
            len(row).should.be.equal(col_num)

        repl = False
        redu = True
        baseline = True
        output_table_type = 'exhausted'
        max_scope = False
        additional_doc_cols = ('gender', 'age', 'working_area')
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True
        header = stats._get_header(repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type, max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right, word_examples_sum_table=word_examples_sum_table)
        col_num = sum([ sum([ len(doc_cols) for doc_cols in cols if doc_cols ]) if tables_part_name == 'document' else len(cols) for tables_part_name, cols in header.iteritems() if cols ])
        assert col_num == 41
        stats.cols_exists_in_corpb(additional_doc_cols)
        syntagma = [
         'klitze', 'kleine']
        stemmed_search = False
        data = stats._export_generator(header, inp_syntagma=syntagma, stemmed_search=stemmed_search)
        for row in data:
            if not row:
                continue
            len(row).should.be.equal(col_num)

        repl = False
        redu = True
        baseline = True
        output_table_type = 'sum'
        max_scope = False
        word_examples_sum_table = True
        additional_doc_cols = False
        context_len_right = True
        context_len_left = True
        reptype_sum_table = 'redu'
        header = stats._get_header(repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type, max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right, word_examples_sum_table=word_examples_sum_table)
        col_num = len(header)
        syntagma = '*'
        stemmed_search = False
        data = stats._export_generator(header, inp_syntagma=syntagma, stemmed_search=stemmed_search, output_table_type=output_table_type, reptype_sum_table=reptype_sum_table)
        for row in data:
            if not row:
                continue
            len(row).should.be.equal(col_num)

        repl = False
        redu = True
        baseline = True
        output_table_type = 'sum'
        max_scope = False
        word_examples_sum_table = True
        additional_doc_cols = False
        context_len_right = True
        context_len_left = True
        reptype_sum_table = 'redu'
        header = stats._get_header(repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type, max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right, word_examples_sum_table=word_examples_sum_table)
        col_num = len(header)
        sentiment = 'positive'
        syntagma = '*'
        stemmed_search = False
        data = stats._export_generator(header, inp_syntagma=syntagma, stemmed_search=stemmed_search, output_table_type=output_table_type, reptype_sum_table=reptype_sum_table, sentiment=sentiment)
        for row in data:
            if not row:
                continue
            len(row).should.be.equal(col_num)

        repl = True
        redu = False
        baseline = True
        output_table_type = 'sum'
        max_scope = False
        word_examples_sum_table = True
        additional_doc_cols = False
        context_len_right = True
        context_len_left = True
        reptype_sum_table = 'repl'
        header = stats._get_header(repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type, max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right, word_examples_sum_table=word_examples_sum_table)
        col_num = len(header)
        syntagma = '*'
        stemmed_search = False
        data = stats._export_generator(header, inp_syntagma=syntagma, stemmed_search=stemmed_search, output_table_type=output_table_type, reptype_sum_table=reptype_sum_table)
        for row in data:
            if not row:
                continue
            len(row).should.be.equal(col_num)

        repl = True
        redu = False
        baseline = True
        output_table_type = 'sum'
        max_scope = False
        word_examples_sum_table = True
        additional_doc_cols = False
        context_len_right = True
        context_len_left = True
        reptype_sum_table = 'repl'
        header = stats._get_header(repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type, max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right, word_examples_sum_table=word_examples_sum_table)
        col_num = len(header)
        sentiment = 'positive'
        syntagma = '*'
        stemmed_search = False
        data = stats._export_generator(header, inp_syntagma=syntagma, stemmed_search=stemmed_search, output_table_type=output_table_type, reptype_sum_table=reptype_sum_table, sentiment=sentiment)
        for row in data:
            if not row:
                continue
            len(row).should.be.equal(col_num)

    def _summerize_reps3(self, header, data, redu=False, repl=True):
        import copy
        dict_repls = defaultdict(lambda : defaultdict(lambda : defaultdict(lambda : 0)))
        dict_redus = defaultdict(lambda : defaultdict(lambda : defaultdict(lambda : 0)))
        dict_baseline = defaultdict(dict)
        if repl:
            ix_repl_index = header.index('[repl].index_in_corpus')
            ix_repl_id = header.index('[repl].id')
            ix_occur_repl_uniq = header.index('[baseline].occur_repl_uniq')
            ix_occur_repl_exhausted = header.index('[baseline].occur_repl_exhausted')
            ix_occur_full_syn_repl = header.index('[baseline].occur_full_syn_repl')
        if redu:
            dict_redus = defaultdict(lambda : defaultdict(lambda : defaultdict(lambda : 0)))
            ix_redu_index = header.index('[redu].index_in_corpus')
            ix_redu_lenght = header.index('[redu].redu_length')
            ix_occur_redu_uniq = header.index('[baseline].occur_redu_uniq')
            ix_occur_redu_exhausted = header.index('[baseline].occur_redu_exhausted')
            ix_occur_full_syn_redu = header.index('[baseline].occur_full_syn_redu')
            ix_redu_id = header.index('[redu].id')
        ix_doc_id = header.index('[document].doc_id')
        ix_syn = header.index('[baseline].syntagma')
        ix_occur = header.index('[baseline].occur_syntagma_all')
        ix_scope = header.index('[baseline].scope')
        ix_word = header.index('[word].normalized_word')
        if repl:
            for row in data:
                repl_id = row[ix_repl_id]
                if repl_id:
                    doc_id = row[ix_doc_id]
                    index_in_corpus = row[ix_repl_index]
                    word = row[ix_word]
                    dict_repls[word][doc_id][index_in_corpus] += 1

        if redu:
            for row in data:
                redu_id = row[ix_redu_id]
                if redu_id:
                    doc_id = row[ix_doc_id]
                    index_in_corpus = row[ix_redu_index]
                    word = row[ix_word]
                    redu_lenght = row[ix_redu_lenght]
                    dict_redus[word][doc_id][index_in_corpus] = redu_lenght

        for row in data:
            syntagma = row[ix_syn]
            scope = row[ix_scope]
            occur_all = row[ix_occur]
            dict_baseline[syntagma]['occur_all'] = occur_all
            dict_baseline[syntagma]['scope'] = scope
            if repl:
                occur_repl_uniq = row[ix_occur_repl_uniq]
                occur_repl_exhausted = row[ix_occur_repl_exhausted]
                occur_full_syn_repl = row[ix_occur_full_syn_repl]
                dict_baseline[syntagma]['occur_repl_uniq'] = occur_repl_uniq
                dict_baseline[syntagma]['occur_repl_exhausted'] = occur_repl_exhausted
                dict_baseline[syntagma]['occur_full_syn_repl'] = occur_full_syn_repl
            if redu:
                occur_redu_uniq = row[ix_occur_redu_uniq]
                occur_redu_exhausted = row[ix_occur_redu_exhausted]
                occur_full_syn_redu = row[ix_occur_full_syn_redu]
                dict_baseline[syntagma]['occur_redu_uniq'] = occur_redu_uniq
                dict_baseline[syntagma]['occur_redu_exhausted'] = occur_redu_exhausted
                dict_baseline[syntagma]['occur_full_syn_redu'] = occur_full_syn_redu

        computed_counts = defaultdict(lambda : defaultdict(lambda : [0, 0]))
        if repl:
            for word, word_data in dict_repls.items():
                for doc_id, doc_data in word_data.items():
                    for index_in_corpus, counter in doc_data.items():
                        computed_counts[word]['repl'][0] += 1
                        computed_counts[word]['repl'][1] += counter

        if redu:
            for word, word_data in dict_redus.items():
                for doc_id, doc_data in word_data.items():
                    for index_in_corpus, counter in doc_data.items():
                        computed_counts[word]['redu'][0] += 1
                        computed_counts[word]['redu'][1] += counter

        temp_dict = {}
        for syntagma, counter_data in dict_baseline.items():
            for counter_name, num in counter_data.items():
                temp_dict[counter_name] = num

        computed_counts[syntagma]['baseline'] = temp_dict
        return computed_counts

    @attr(status='stable')
    def test_test_export_generator_content_correctnes_613_3(self):
        self.prj_folder()
        self.test_dbs()
        stats = Stats(mode=self.mode, use_cash=True, status_bar=True)
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['stats']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'stats'
        gold_standard_data = self.configer._counted_reps['en']
        stats.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_stats_en))
        stats.attach_corpdb(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_en))
        repl = True
        redu = False
        baseline = True
        output_table_type = 'exhausted'
        max_scope = False
        additional_doc_cols = ()
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True
        header = stats._get_header(repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type, max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right, word_examples_sum_table=word_examples_sum_table)
        ordered_header = stats.order_header(header, False, 'csv')
        col_num = sum([ sum([ len(doc_cols) for doc_cols in cols if doc_cols ]) if tables_part_name == 'document' else len(cols) for tables_part_name, cols in header.iteritems() if cols ])
        syntagma = [
         'bad']
        right_data = gold_standard_data[syntagma[0]]
        repl_num = right_data['repl'][1]
        stemmed_search = False
        data = stats._export_generator(header, inp_syntagma=syntagma, stemmed_search=stemmed_search)
        data = list(data)
        answer = self._summerize_reps3(ordered_header, data, redu=redu, repl=repl)
        if repl:
            assert len(data) >= right_data['repl'][1]
            tuple(right_data['repl']).should.be.equal(tuple(answer[syntagma[0]]['repl']))
            baseline_entry_repl = (int(answer[syntagma[0]]['baseline']['occur_repl_uniq']), int(answer[syntagma[0]]['baseline']['occur_repl_exhausted']))
            tuple(right_data['repl']).should.be.equal(tuple(baseline_entry_repl))
            len(syntagma).should.be.equal(answer[syntagma[0]]['baseline']['scope'])
            repl = True
            redu = False
            baseline = True
            output_table_type = 'exhausted'
            max_scope = False
            additional_doc_cols = ()
            context_len_left = True
            context_len_right = True
            word_examples_sum_table = True
            header = stats._get_header(repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type, max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right, word_examples_sum_table=word_examples_sum_table)
            ordered_header = stats.order_header(header, False, 'csv')
            col_num = sum([ sum([ len(doc_cols) for doc_cols in cols if doc_cols ]) if tables_part_name == 'document' else len(cols) for tables_part_name, cols in header.iteritems() if cols ])
            syntagma = [
             'big']
            right_data = gold_standard_data[syntagma[0]]
            repl_num = right_data['repl'][1]
            stemmed_search = False
            data = stats._export_generator(header, inp_syntagma=syntagma, stemmed_search=stemmed_search)
            data = list(data)
            answer = self._summerize_reps3(ordered_header, data, redu=redu, repl=repl)
            assert repl and len(data) >= right_data['repl'][1]
        len(data).should.be.equal(right_data['repl'][1])
        tuple(right_data['repl']).should.be.equal(tuple(answer[syntagma[0]]['repl']))
        baseline_entry_repl = (int(answer[syntagma[0]]['baseline']['occur_repl_uniq']), int(answer[syntagma[0]]['baseline']['occur_repl_exhausted']))
        tuple(right_data['repl']).should.be.equal(tuple(baseline_entry_repl))
        len(syntagma).should.be.equal(answer[syntagma[0]]['baseline']['scope'])
        repl = True
        redu = True
        baseline = True
        output_table_type = 'exhausted'
        max_scope = False
        additional_doc_cols = ()
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True
        header = stats._get_header(repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type, max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right, word_examples_sum_table=word_examples_sum_table)
        ordered_header = stats.order_header(header, False, 'csv')
        col_num = sum([ sum([ len(doc_cols) for doc_cols in cols if doc_cols ]) if tables_part_name == 'document' else len(cols) for tables_part_name, cols in header.iteritems() if cols ])
        syntagma = [
         'big']
        right_data = gold_standard_data[syntagma[0]]
        repl_num = right_data['repl'][1]
        stemmed_search = False
        data = stats._export_generator(header, inp_syntagma=syntagma, stemmed_search=stemmed_search)
        data = list(data)
        answer = self._summerize_reps3(ordered_header, data, redu=redu, repl=repl)
        if repl:
            assert len(data) >= right_data['repl'][1]
            tuple(right_data['repl']).should.be.equal(tuple(answer[syntagma[0]]['repl']))
            baseline_entry_repl = (int(answer[syntagma[0]]['baseline']['occur_repl_uniq']), int(answer[syntagma[0]]['baseline']['occur_repl_exhausted']))
            tuple(right_data['repl']).should.be.equal(tuple(baseline_entry_repl))
            len(syntagma).should.be.equal(answer[syntagma[0]]['baseline']['scope'])
            tuple(right_data['redu']).should.be.equal(tuple(answer[syntagma[0]]['redu']))
            baseline_entry_redu = (int(answer[syntagma[0]]['baseline']['occur_redu_uniq']), int(answer[syntagma[0]]['baseline']['occur_redu_exhausted']))
            tuple(right_data['redu']).should.be.equal(tuple(baseline_entry_redu))
            len(syntagma).should.be.equal(answer[syntagma[0]]['baseline']['scope'])
            repl = True
            redu = True
            baseline = True
            output_table_type = 'exhausted'
            max_scope = False
            additional_doc_cols = ()
            context_len_left = True
            context_len_right = True
            word_examples_sum_table = True
            header = stats._get_header(repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type, max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right, word_examples_sum_table=word_examples_sum_table)
            ordered_header = stats.order_header(header, False, 'csv')
            col_num = sum([ sum([ len(doc_cols) for doc_cols in cols if doc_cols ]) if tables_part_name == 'document' else len(cols) for tables_part_name, cols in header.iteritems() if cols ])
            syntagma = [
             '🌈']
            right_data = gold_standard_data[syntagma[0]]
            repl_num = right_data['repl'][1]
            stemmed_search = False
            data = stats._export_generator(header, inp_syntagma=syntagma, stemmed_search=stemmed_search)
            data = list(data)
            answer = self._summerize_reps3(ordered_header, data, redu=redu, repl=repl)
            assert repl and len(data) >= right_data['repl'][1]
        if 'repl' in right_data:
            tuple(right_data['repl']).should.be.equal(tuple(answer[syntagma[0]]['repl']))
            baseline_entry_repl = (int(answer[syntagma[0]]['baseline']['occur_repl_uniq']), int(answer[syntagma[0]]['baseline']['occur_repl_exhausted']))
            tuple(right_data['repl']).should.be.equal(tuple(baseline_entry_repl))
            len(syntagma).should.be.equal(answer[syntagma[0]]['baseline']['scope'])
        if 'redu' in right_data:
            tuple(right_data['redu']).should.be.equal(tuple(answer[syntagma[0]]['redu']))
            baseline_entry_redu = (int(answer[syntagma[0]]['baseline']['occur_redu_uniq']), int(answer[syntagma[0]]['baseline']['occur_redu_exhausted']))
            tuple(right_data['redu']).should.be.equal(tuple(baseline_entry_redu))
            len(syntagma).should.be.equal(answer[syntagma[0]]['baseline']['scope'])
        repl = True
        redu = True
        baseline = True
        output_table_type = 'exhausted'
        max_scope = False
        additional_doc_cols = ()
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True
        header = stats._get_header(repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type, max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right, word_examples_sum_table=word_examples_sum_table)
        ordered_header = stats.order_header(header, False, 'csv')
        col_num = sum([ sum([ len(doc_cols) for doc_cols in cols if doc_cols ]) if tables_part_name == 'document' else len(cols) for tables_part_name, cols in header.iteritems() if cols ])
        syntagma = [
         '😀']
        right_data = gold_standard_data[syntagma[0]]
        repl_num = right_data['repl'][1]
        stemmed_search = False
        data = stats._export_generator(header, inp_syntagma=syntagma, stemmed_search=stemmed_search)
        data = list(data)
        answer = self._summerize_reps3(ordered_header, data, redu=redu, repl=repl)
        if repl:
            assert len(data) >= right_data['repl'][1]
            if 'repl' in right_data:
                tuple(right_data['repl']).should.be.equal(tuple(answer[syntagma[0]]['repl']))
                baseline_entry_repl = (int(answer[syntagma[0]]['baseline']['occur_repl_uniq']), int(answer[syntagma[0]]['baseline']['occur_repl_exhausted']))
                tuple(right_data['repl']).should.be.equal(tuple(baseline_entry_repl))
                len(syntagma).should.be.equal(answer[syntagma[0]]['baseline']['scope'])
            if 'redu' in right_data:
                tuple(right_data['redu']).should.be.equal(tuple(answer[syntagma[0]]['redu']))
                baseline_entry_redu = (int(answer[syntagma[0]]['baseline']['occur_redu_uniq']), int(answer[syntagma[0]]['baseline']['occur_redu_exhausted']))
                tuple(right_data['redu']).should.be.equal(tuple(baseline_entry_redu))
                len(syntagma).should.be.equal(answer[syntagma[0]]['baseline']['scope'])
            repl = True
            redu = True
            baseline = True
            output_table_type = 'exhausted'
            max_scope = False
            additional_doc_cols = ()
            context_len_left = True
            context_len_right = True
            word_examples_sum_table = True
            header = stats._get_header(repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type, max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right, word_examples_sum_table=word_examples_sum_table)
            ordered_header = stats.order_header(header, False, 'csv')
            col_num = sum([ sum([ len(doc_cols) for doc_cols in cols if doc_cols ]) if tables_part_name == 'document' else len(cols) for tables_part_name, cols in header.iteritems() if cols ])
            syntagma = [
             ':-(']
            right_data = gold_standard_data[syntagma[0]]
            repl_num = right_data['repl'][1]
            stemmed_search = False
            data = stats._export_generator(header, inp_syntagma=syntagma, stemmed_search=stemmed_search)
            data = list(data)
            answer = self._summerize_reps3(ordered_header, data, redu=redu, repl=repl)
            assert repl and len(data) >= right_data['repl'][1]
        if 'repl' in right_data:
            tuple(right_data['repl']).should.be.equal(tuple(answer[syntagma[0]]['repl']))
            baseline_entry_repl = (int(answer[syntagma[0]]['baseline']['occur_repl_uniq']), int(answer[syntagma[0]]['baseline']['occur_repl_exhausted']))
            tuple(right_data['repl']).should.be.equal(tuple(baseline_entry_repl))
            len(syntagma).should.be.equal(answer[syntagma[0]]['baseline']['scope'])
        if 'redu' in right_data:
            tuple(right_data['redu']).should.be.equal(tuple(answer[syntagma[0]]['redu']))
            baseline_entry_redu = (int(answer[syntagma[0]]['baseline']['occur_redu_uniq']), int(answer[syntagma[0]]['baseline']['occur_redu_exhausted']))
            tuple(right_data['redu']).should.be.equal(tuple(baseline_entry_redu))
            len(syntagma).should.be.equal(answer[syntagma[0]]['baseline']['scope'])
        repl = True
        redu = True
        baseline = True
        output_table_type = 'exhausted'
        max_scope = False
        additional_doc_cols = ()
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True
        header = stats._get_header(repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type, max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right, word_examples_sum_table=word_examples_sum_table)
        ordered_header = stats.order_header(header, False, 'csv')
        col_num = sum([ sum([ len(doc_cols) for doc_cols in cols if doc_cols ]) if tables_part_name == 'document' else len(cols) for tables_part_name, cols in header.iteritems() if cols ])
        syntagma = [
         '1']
        right_data = gold_standard_data[syntagma[0]]
        repl_num = right_data['repl'][1]
        stemmed_search = False
        data = stats._export_generator(header, inp_syntagma=syntagma, stemmed_search=stemmed_search)
        data = list(data)
        answer = self._summerize_reps3(ordered_header, data, redu=redu, repl=repl)
        if repl:
            assert len(data) >= right_data['repl'][1]
            if 'repl' in right_data:
                tuple(right_data['repl']).should.be.equal(tuple(answer[syntagma[0]]['repl']))
                baseline_entry_repl = (int(answer[syntagma[0]]['baseline']['occur_repl_uniq']), int(answer[syntagma[0]]['baseline']['occur_repl_exhausted']))
                tuple(right_data['repl']).should.be.equal(tuple(baseline_entry_repl))
                len(syntagma).should.be.equal(answer[syntagma[0]]['baseline']['scope'])
            if 'redu' in right_data:
                tuple(right_data['redu']).should.be.equal(tuple(answer[syntagma[0]]['redu']))
                baseline_entry_redu = (int(answer[syntagma[0]]['baseline']['occur_redu_uniq']), int(answer[syntagma[0]]['baseline']['occur_redu_exhausted']))
                tuple(right_data['redu']).should.be.equal(tuple(baseline_entry_redu))
                len(syntagma).should.be.equal(answer[syntagma[0]]['baseline']['scope'])
            repl = True
            redu = True
            baseline = True
            output_table_type = 'exhausted'
            max_scope = False
            additional_doc_cols = ()
            context_len_left = True
            context_len_right = True
            word_examples_sum_table = True
            header = stats._get_header(repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type, max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right, word_examples_sum_table=word_examples_sum_table)
            ordered_header = stats.order_header(header, False, 'csv')
            col_num = sum([ sum([ len(doc_cols) for doc_cols in cols if doc_cols ]) if tables_part_name == 'document' else len(cols) for tables_part_name, cols in header.iteritems() if cols ])
            syntagma = [
             'tiny']
            right_data = gold_standard_data[syntagma[0]]
            repl_num = right_data['repl'][1]
            stemmed_search = False
            data = stats._export_generator(header, inp_syntagma=syntagma, stemmed_search=stemmed_search)
            data = list(data)
            answer = self._summerize_reps3(ordered_header, data, redu=redu, repl=repl)
            assert repl and len(data) >= right_data['repl'][1]
        if 'repl' in right_data:
            tuple(right_data['repl']).should.be.equal(tuple(answer[syntagma[0]]['repl']))
            baseline_entry_repl = (int(answer[syntagma[0]]['baseline']['occur_repl_uniq']), int(answer[syntagma[0]]['baseline']['occur_repl_exhausted']))
            tuple(right_data['repl']).should.be.equal(tuple(baseline_entry_repl))
            len(syntagma).should.be.equal(answer[syntagma[0]]['baseline']['scope'])
        if 'redu' in right_data:
            tuple(right_data['redu']).should.be.equal(tuple(answer[syntagma[0]]['redu']))
            baseline_entry_redu = (int(answer[syntagma[0]]['baseline']['occur_redu_uniq']), int(answer[syntagma[0]]['baseline']['occur_redu_exhausted']))
            tuple(right_data['redu']).should.be.equal(tuple(baseline_entry_redu))
            len(syntagma).should.be.equal(answer[syntagma[0]]['baseline']['scope'])
        repl = False
        redu = True
        baseline = True
        output_table_type = 'exhausted'
        max_scope = False
        additional_doc_cols = ()
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True
        header = stats._get_header(repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type, max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right, word_examples_sum_table=word_examples_sum_table)
        ordered_header = stats.order_header(header, False, 'csv')
        col_num = sum([ sum([ len(doc_cols) for doc_cols in cols if doc_cols ]) if tables_part_name == 'document' else len(cols) for tables_part_name, cols in header.iteritems() if cols ])
        syntagma = [
         'tiny']
        right_data = gold_standard_data[syntagma[0]]
        repl_num = right_data['repl'][1]
        stemmed_search = False
        data = stats._export_generator(header, inp_syntagma=syntagma, stemmed_search=stemmed_search)
        data = list(data)
        answer = self._summerize_reps3(ordered_header, data, redu=redu, repl=repl)
        if repl:
            assert len(data) >= right_data['repl'][1]
            if 'repl' in right_data and repl:
                tuple(right_data['repl']).should.be.equal(tuple(answer[syntagma[0]]['repl']))
                baseline_entry_repl = (int(answer[syntagma[0]]['baseline']['occur_repl_uniq']), int(answer[syntagma[0]]['baseline']['occur_repl_exhausted']))
                tuple(right_data['repl']).should.be.equal(tuple(baseline_entry_repl))
                len(syntagma).should.be.equal(answer[syntagma[0]]['baseline']['scope'])
            if 'redu' in right_data and redu:
                tuple(right_data['redu']).should.be.equal(tuple(answer[syntagma[0]]['redu']))
                baseline_entry_redu = (int(answer[syntagma[0]]['baseline']['occur_redu_uniq']), int(answer[syntagma[0]]['baseline']['occur_redu_exhausted']))
                tuple(right_data['redu']).should.be.equal(tuple(baseline_entry_redu))
                len(syntagma).should.be.equal(answer[syntagma[0]]['baseline']['scope'])
            repl = False
            redu = True
            baseline = True
            output_table_type = 'exhausted'
            max_scope = False
            additional_doc_cols = ()
            context_len_left = True
            context_len_right = True
            word_examples_sum_table = True
            header = stats._get_header(repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type, max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right, word_examples_sum_table=word_examples_sum_table)
            ordered_header = stats.order_header(header, False, 'csv')
            col_num = sum([ sum([ len(doc_cols) for doc_cols in cols if doc_cols ]) if tables_part_name == 'document' else len(cols) for tables_part_name, cols in header.iteritems() if cols ])
            syntagma = [
             'bad']
            right_data = gold_standard_data[syntagma[0]]
            repl_num = right_data['repl'][1]
            stemmed_search = False
            data = stats._export_generator(header, inp_syntagma=syntagma, stemmed_search=stemmed_search)
            data = list(data)
            answer = self._summerize_reps3(ordered_header, data, redu=redu, repl=repl)
            assert repl and len(data) >= right_data['repl'][1]
        if 'repl' in right_data and repl:
            tuple(right_data['repl']).should.be.equal(tuple(answer[syntagma[0]]['repl']))
            baseline_entry_repl = (int(answer[syntagma[0]]['baseline']['occur_repl_uniq']), int(answer[syntagma[0]]['baseline']['occur_repl_exhausted']))
            tuple(right_data['repl']).should.be.equal(tuple(baseline_entry_repl))
            len(syntagma).should.be.equal(answer[syntagma[0]]['baseline']['scope'])
        if 'redu' in right_data and redu:
            tuple(right_data['redu']).should.be.equal(tuple(answer[syntagma[0]]['redu']))
            baseline_entry_redu = (int(answer[syntagma[0]]['baseline']['occur_redu_uniq']), int(answer[syntagma[0]]['baseline']['occur_redu_exhausted']))
            tuple(right_data['redu']).should.be.equal(tuple(baseline_entry_redu))
            len(syntagma).should.be.equal(answer[syntagma[0]]['baseline']['scope'])
        repl = True
        redu = True
        baseline = True
        output_table_type = 'exhausted'
        max_scope = False
        additional_doc_cols = ()
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True
        header = stats._get_header(repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type, max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right, word_examples_sum_table=word_examples_sum_table)
        ordered_header = stats.order_header(header, False, 'csv')
        col_num = sum([ sum([ len(doc_cols) for doc_cols in cols if doc_cols ]) if tables_part_name == 'document' else len(cols) for tables_part_name, cols in header.iteritems() if cols ])
        syntagma = [
         'but']
        right_data = gold_standard_data[syntagma[0]]
        repl_num = right_data['repl'][1]
        stemmed_search = False
        data = stats._export_generator(header, inp_syntagma=syntagma, stemmed_search=stemmed_search)
        data = list(data)
        answer = self._summerize_reps3(ordered_header, data, redu=redu, repl=repl)
        if repl:
            assert len(data) >= right_data['repl'][1]
            if 'repl' in right_data and repl:
                tuple(right_data['repl']).should.be.equal(tuple(answer[syntagma[0]]['repl']))
                baseline_entry_repl = (int(answer[syntagma[0]]['baseline']['occur_repl_uniq']), int(answer[syntagma[0]]['baseline']['occur_repl_exhausted']))
                tuple(right_data['repl']).should.be.equal(tuple(baseline_entry_repl))
                len(syntagma).should.be.equal(answer[syntagma[0]]['baseline']['scope'])
            if 'redu' in right_data and redu:
                tuple(right_data['redu']).should.be.equal(tuple(answer[syntagma[0]]['redu']))
                baseline_entry_redu = (int(answer[syntagma[0]]['baseline']['occur_redu_uniq']), int(answer[syntagma[0]]['baseline']['occur_redu_exhausted']))
                tuple(right_data['redu']).should.be.equal(tuple(baseline_entry_redu))
                len(syntagma).should.be.equal(answer[syntagma[0]]['baseline']['scope'])
            repl = True
            redu = True
            baseline = True
            output_table_type = 'exhausted'
            max_scope = False
            additional_doc_cols = ()
            context_len_left = True
            context_len_right = True
            word_examples_sum_table = True
            header = stats._get_header(repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type, max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right, word_examples_sum_table=word_examples_sum_table)
            ordered_header = stats.order_header(header, False, 'csv')
            col_num = sum([ sum([ len(doc_cols) for doc_cols in cols if doc_cols ]) if tables_part_name == 'document' else len(cols) for tables_part_name, cols in header.iteritems() if cols ])
            syntagma = [
             'EMOIMG']
            stemmed_search = False
            data = stats._export_generator(header, inp_syntagma=syntagma, stemmed_search=stemmed_search, syntagma_type='pos')
            data = list(data)
            answer = self._summerize_reps3(ordered_header, data, redu=redu, repl=repl)
            repl_num = sum([ _data['repl'][1] for word, _data in answer.items() if word != 'baseline' ])
            assert repl and len(data) >= repl_num
        answer = {word:{phanomen:counts for phanomen, counts in _data.items()} for word, _data in answer.items()}
        for word, _data in answer.items():
            if word != 'baseline':
                if tuple(_data['repl']) != gold_standard_data[word]['repl']:
                    assert False

        repl = True
        redu = True
        baseline = True
        output_table_type = 'exhausted'
        max_scope = False
        additional_doc_cols = ()
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True
        header = stats._get_header(repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type, max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right, word_examples_sum_table=word_examples_sum_table)
        ordered_header = stats.order_header(header, False, 'csv')
        col_num = sum([ sum([ len(doc_cols) for doc_cols in cols if doc_cols ]) if tables_part_name == 'document' else len(cols) for tables_part_name, cols in header.iteritems() if cols ])
        syntagma = [
         'number']
        stemmed_search = False
        data = stats._export_generator(header, inp_syntagma=syntagma, stemmed_search=stemmed_search, syntagma_type='pos')
        data = list(data)
        answer = self._summerize_reps3(ordered_header, data, redu=redu, repl=repl)
        repl_num = sum([ _data['repl'][1] for word, _data in answer.items() if word != 'baseline' ])
        if repl:
            assert len(data) >= repl_num
            answer = {word:{phanomen:counts for phanomen, counts in _data.items()} for word, _data in answer.items()}
            for word, _data in answer.items():
                if word != 'baseline':
                    if tuple(_data['repl']) != gold_standard_data[word]['repl']:
                        assert False

            repl = True
            redu = True
            baseline = True
            output_table_type = 'exhausted'
            max_scope = False
            additional_doc_cols = ()
            context_len_left = True
            context_len_right = True
            word_examples_sum_table = True
            header = stats._get_header(repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type, max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right, word_examples_sum_table=word_examples_sum_table)
            ordered_header = stats.order_header(header, False, 'csv')
            col_num = sum([ sum([ len(doc_cols) for doc_cols in cols if doc_cols ]) if tables_part_name == 'document' else len(cols) for tables_part_name, cols in header.iteritems() if cols ])
            syntagma = [
             'EMOASC']
            stemmed_search = False
            data = stats._export_generator(header, inp_syntagma=syntagma, stemmed_search=stemmed_search, syntagma_type='pos')
            data = list(data)
            answer = self._summerize_reps3(ordered_header, data, redu=redu, repl=repl)
            repl_num = sum([ _data['repl'][1] for word, _data in answer.items() if word != 'baseline' ])
            assert repl and len(data) >= repl_num
        answer = {word:{phanomen:counts for phanomen, counts in _data.items()} for word, _data in answer.items()}
        for word, _data in answer.items():
            if word != 'baseline':
                if tuple(_data['repl']) != gold_standard_data[word]['repl']:
                    assert False

        repl = True
        redu = True
        baseline = True
        output_table_type = 'exhausted'
        max_scope = False
        additional_doc_cols = ()
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True
        header = stats._get_header(repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type, max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right, word_examples_sum_table=word_examples_sum_table)
        ordered_header = stats.order_header(header, False, 'csv')
        col_num = sum([ sum([ len(doc_cols) for doc_cols in cols if doc_cols ]) if tables_part_name == 'document' else len(cols) for tables_part_name, cols in header.iteritems() if cols ])
        syntagma = [
         'very', 'pity']
        right_data = {'very': {'repl': [
                           2, 4], 
                    'redu': [
                           1, 3]}, 
           'pity': {'repl': [
                           2, 4], 
                    'redu': [
                           1, 4]}, 
           'very || pity': {'baseline': {'occur_repl_uniq': '[2, 2]', 
                                         'occur_all': 1, 
                                         'occur_repl_exhausted': '[4, 4]', 
                                         'occur_full_syn_redu': '1', 
                                         'occur_redu_exhausted': '[3, 4]', 
                                         'scope': 2, 
                                         'occur_full_syn_repl': '1', 
                                         'occur_redu_uniq': '[1, 1]'}}}
        stemmed_search = False
        data = stats._export_generator(header, inp_syntagma=syntagma, stemmed_search=stemmed_search)
        data = list(data)
        answer = self._summerize_reps3(ordered_header, data, redu=redu, repl=repl)
        answer = {word:{phanomen:counts for phanomen, counts in data.items()} for word, data in answer.items()}
        joined_syn = (' || ').join(syntagma)
        if repl:
            if 'repl' in right_data[syntagma[0]]:
                tuple(right_data[syntagma[0]]['repl']).should.be.equal(tuple(answer[syntagma[0]]['repl']))
                baseline_entry_repl_word_1 = (
                 json.loads(answer[joined_syn]['baseline']['occur_repl_uniq'])[0],
                 json.loads(answer[joined_syn]['baseline']['occur_repl_exhausted'])[0])
                tuple(right_data[syntagma[0]]['repl']).should.be.equal(tuple(baseline_entry_repl_word_1))
            if 'repl' in right_data[syntagma[1]]:
                baseline_entry_repl_word_2 = (
                 json.loads(answer[joined_syn]['baseline']['occur_repl_uniq'])[1],
                 json.loads(answer[joined_syn]['baseline']['occur_repl_exhausted'])[1])
                tuple(right_data[syntagma[1]]['repl']).should.be.equal(tuple(baseline_entry_repl_word_2))
                len(syntagma).should.be.equal(answer[joined_syn]['baseline']['scope'])
            int(answer[joined_syn]['baseline']['occur_full_syn_repl']).should.be.equal(int(right_data[joined_syn]['baseline']['occur_full_syn_repl']))
        if redu:
            if 'redu' in right_data[syntagma[0]]:
                tuple(right_data[syntagma[0]]['redu']).should.be.equal(tuple(answer[syntagma[0]]['redu']))
                baseline_entry_redu_word_1 = (
                 json.loads(answer[joined_syn]['baseline']['occur_redu_uniq'])[0],
                 json.loads(answer[joined_syn]['baseline']['occur_redu_exhausted'])[0])
                tuple(right_data[syntagma[0]]['redu']).should.be.equal(tuple(baseline_entry_redu_word_1))
            if 'redu' in right_data[syntagma[1]]:
                baseline_entry_redu_word_2 = (
                 json.loads(answer[joined_syn]['baseline']['occur_redu_uniq'])[1],
                 json.loads(answer[joined_syn]['baseline']['occur_redu_exhausted'])[1])
                tuple(right_data[syntagma[1]]['redu']).should.be.equal(tuple(baseline_entry_redu_word_2))
                len(syntagma).should.be.equal(answer[joined_syn]['baseline']['scope'])
            int(answer[joined_syn]['baseline']['occur_full_syn_redu']).should.be.equal(int(right_data[joined_syn]['baseline']['occur_full_syn_redu']))
        repl = True
        redu = True
        baseline = True
        output_table_type = 'exhausted'
        max_scope = False
        additional_doc_cols = ()
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True
        header = stats._get_header(repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type, max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right, word_examples_sum_table=word_examples_sum_table)
        ordered_header = stats.order_header(header, False, 'csv')
        col_num = sum([ sum([ len(doc_cols) for doc_cols in cols if doc_cols ]) if tables_part_name == 'document' else len(cols) for tables_part_name, cols in header.iteritems() if cols ])
        syntagma = ['but', 'you']
        right_data = {'but || you': {'baseline': {'occur_repl_uniq': '[10, 6]', 
                                       'occur_all': 4, 
                                       'occur_repl_exhausted': '[15, 8]', 
                                       'occur_full_syn_redu': '2', 
                                       'occur_redu_exhausted': '[4, 4]', 
                                       'scope': 2, 
                                       'occur_full_syn_repl': '4', 'occur_redu_uniq': '[2, 2]'}}, 
           'you': {'repl': [
                          6, 8], 
                   'redu': [
                          2, 4]}, 
           'but': {'repl': [
                          10, 15], 
                   'redu': [
                          4, 10]}}
        stemmed_search = False
        data = stats._export_generator(header, inp_syntagma=syntagma, stemmed_search=stemmed_search)
        data = list(data)
        answer = self._summerize_reps3(ordered_header, data, redu=redu, repl=repl)
        answer = {word:{phanomen:counts for phanomen, counts in data.items()} for word, data in answer.items()}
        joined_syn = (' || ').join(syntagma)
        if repl:
            if 'repl' in right_data[syntagma[0]]:
                tuple(right_data[syntagma[0]]['repl']).should.be.equal(tuple(answer[syntagma[0]]['repl']))
                baseline_entry_repl_word_1 = (
                 json.loads(answer[joined_syn]['baseline']['occur_repl_uniq'])[0],
                 json.loads(answer[joined_syn]['baseline']['occur_repl_exhausted'])[0])
                tuple(right_data[syntagma[0]]['repl']).should.be.equal(tuple(baseline_entry_repl_word_1))
            if 'repl' in right_data[syntagma[1]]:
                baseline_entry_repl_word_2 = (
                 json.loads(answer[joined_syn]['baseline']['occur_repl_uniq'])[1],
                 json.loads(answer[joined_syn]['baseline']['occur_repl_exhausted'])[1])
                tuple(right_data[syntagma[1]]['repl']).should.be.equal(tuple(baseline_entry_repl_word_2))
                len(syntagma).should.be.equal(answer[joined_syn]['baseline']['scope'])
            int(answer[joined_syn]['baseline']['occur_full_syn_repl']).should.be.equal(int(right_data[joined_syn]['baseline']['occur_full_syn_repl']))
        if redu:
            if 'redu' in right_data[syntagma[0]]:
                tuple(right_data[syntagma[0]]['redu']).should.be.equal(tuple(answer[syntagma[0]]['redu']))
                baseline_entry_redu_word_1 = (
                 json.loads(answer[joined_syn]['baseline']['occur_redu_uniq'])[0],
                 json.loads(answer[joined_syn]['baseline']['occur_redu_exhausted'])[0])
            if 'redu' in right_data[syntagma[1]]:
                baseline_entry_redu_word_2 = (
                 json.loads(answer[joined_syn]['baseline']['occur_redu_uniq'])[1],
                 json.loads(answer[joined_syn]['baseline']['occur_redu_exhausted'])[1])
                tuple(right_data[syntagma[1]]['redu']).should.be.equal(tuple(baseline_entry_redu_word_2))
                len(syntagma).should.be.equal(answer[joined_syn]['baseline']['scope'])
            int(answer[joined_syn]['baseline']['occur_full_syn_redu']).should.be.equal(int(right_data[joined_syn]['baseline']['occur_full_syn_redu']))

    @attr(status='stable')
    def test_get_where_statement_type_614(self):
        self.prj_folder()
        self.test_dbs()
        stats = Stats(mode=self.mode, use_cash=True)
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['stats']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'stats'
        stats.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_stats_de))
        inp_syntagma_splitted = [
         '😀']
        inp_syntagma_unsplitted = '😀'
        scope = 1
        with_context = True
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted, scope, with_context=with_context))
        assert where == [["normalized_word='😀' "]]
        inp_syntagma_splitted = [
         '😀']
        inp_syntagma_unsplitted = '😀'
        scope = 1
        with_context = True
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted, scope, with_context=with_context))
        assert where == [["normalized_word='😀' "]]
        inp_syntagma_splitted = [
         '😀']
        inp_syntagma_unsplitted = '😀'
        scope = 1
        with_context = True
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted, scope, with_context=with_context))
        assert where == [["normalized_word='😀' "]]
        inp_syntagma_splitted = [
         '😀']
        inp_syntagma_unsplitted = '😀'
        scope = 1
        with_context = True
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted, scope, with_context=with_context))
        assert where == [["normalized_word='😀' "]]
        inp_syntagma_splitted = [
         '😀']
        inp_syntagma_unsplitted = False
        scope = 1
        with_context = True
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted, scope, with_context=with_context))
        assert where == [["normalized_word='😀' "]]
        inp_syntagma_splitted = [
         '😀']
        inp_syntagma_unsplitted = False
        scope = 1
        with_context = True
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted, scope, with_context=with_context))
        assert where == [["normalized_word='😀' "]]
        inp_syntagma_splitted = [
         '.']
        inp_syntagma_unsplitted = '.'
        scope = 1
        with_context = True
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted, scope, with_context=with_context))
        assert where == [["normalized_word='.' "]]
        inp_syntagma_splitted = [
         'klitze', 'kleine']
        inp_syntagma_unsplitted = 'klitze++kleine'
        scope = 2
        with_context = True
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted, scope, with_context=with_context))
        assert where == [["normalized_word='klitze' ", "contextR1='kleine'"], ["contextL1='klitze'", "normalized_word='kleine' "]]
        inp_syntagma_splitted = [
         'klitze', 'kleine', 'überaschung']
        inp_syntagma_unsplitted = 'klitze++kleine++überaschung'
        scope = 3
        with_context = True
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted, scope, with_context=with_context))
        assert where == [["normalized_word='klitze' ", "contextR1='kleine'", "contextR2='überaschung'"], ["contextL1='klitze'", "normalized_word='kleine' ", "contextR1='überaschung'"], ["contextL2='klitze'", "contextL1='kleine'", "normalized_word='überaschung' "]]
        inp_syntagma_splitted = [
         '1', 2, 3]
        inp_syntagma_unsplitted = '1++2++3'
        scope = 3
        with_context = True
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted, scope, with_context=with_context))
        assert where == [["normalized_word='1' ", "contextR1='2'", "contextR2='3'"], ["contextL1='1'", "normalized_word='2' ", "contextR1='3'"], ["contextL2='1'", "contextL1='2'", "normalized_word='3' "]]
        inp_syntagma_splitted = [
         '1', 2, 3]
        inp_syntagma_unsplitted = '1++2++3'
        scope = 3
        with_context = True
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted, scope, with_context=with_context))
        assert where == [["normalized_word='1' ", "contextR1='2'", "contextR2='3'"], ["contextL1='1'", "normalized_word='2' ", "contextR1='3'"], ["contextL2='1'", "contextL1='2'", "normalized_word='3' "]]
        inp_syntagma_splitted = [
         '1', 2, 3]
        inp_syntagma_unsplitted = False
        scope = 3
        with_context = True
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted, scope, with_context=with_context))
        assert where == [["normalized_word='1' ", "contextR1='2'", "contextR2='3'"], ["contextL1='1'", "normalized_word='2' ", "contextR1='3'"], ["contextL2='1'", "contextL1='2'", "normalized_word='3' "]]
        inp_syntagma_splitted = [
         '1', 2, 3]
        inp_syntagma_unsplitted = False
        scope = 3
        with_context = True
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted, scope, with_context=with_context))
        assert where == [["normalized_word='1' ", "contextR1='2'", "contextR2='3'"], ["contextL1='1'", "normalized_word='2' ", "contextR1='3'"], ["contextL2='1'", "contextL1='2'", "normalized_word='3' "]]
        inp_syntagma_splitted = [
         1, 2, 3]
        inp_syntagma_unsplitted = False
        scope = 3
        with_context = True
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted, scope, with_context=with_context))
        assert where == [["normalized_word='1' ", "contextR1='2'", "contextR2='3'"], ["contextL1='1'", "normalized_word='2' ", "contextR1='3'"], ["contextL2='1'", "contextL1='2'", "normalized_word='3' "]]
        inp_syntagma_splitted = [
         1, 2, 3]
        inp_syntagma_unsplitted = '1++2++3'
        scope = 3
        with_context = True
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted, scope, with_context=with_context))
        assert where == [["normalized_word='1' ", "contextR1='2'", "contextR2='3'"], ["contextL1='1'", "normalized_word='2' ", "contextR1='3'"], ["contextL2='1'", "contextL1='2'", "normalized_word='3' "]]
        inp_syntagma_splitted = [
         1, 2, 3]
        inp_syntagma_unsplitted = '1++2++3'
        scope = 3
        with_context = True
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted, scope, with_context=with_context))
        assert where == [["normalized_word='1' ", "contextR1='2'", "contextR2='3'"], ["contextL1='1'", "normalized_word='2' ", "contextR1='3'"], ["contextL2='1'", "contextL1='2'", "normalized_word='3' "]]
        inp_syntagma_splitted = [
         '😀']
        inp_syntagma_unsplitted = '😀'
        scope = 1
        with_context = False
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted, scope, with_context=with_context))
        assert where == ["syntagma= '😀'"]
        inp_syntagma_splitted = [
         '😀']
        inp_syntagma_unsplitted = '😀'
        scope = 1
        with_context = False
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted, scope, with_context=with_context))
        assert where == ["syntagma= '😀'"]
        inp_syntagma_splitted = [
         '😀']
        inp_syntagma_unsplitted = '😀'
        scope = 1
        with_context = False
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted, scope, with_context=with_context))
        assert where == ["syntagma= '😀'"]
        inp_syntagma_splitted = [
         '😀']
        inp_syntagma_unsplitted = '😀'
        scope = 1
        with_context = False
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted, scope, with_context=with_context))
        assert where == ["syntagma= '😀'"]
        inp_syntagma_splitted = [
         '😀']
        inp_syntagma_unsplitted = False
        scope = 1
        with_context = False
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted, scope, with_context=with_context))
        assert where == ["syntagma= '😀'"]
        inp_syntagma_splitted = [
         '😀']
        inp_syntagma_unsplitted = False
        scope = 1
        with_context = False
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted, scope, with_context=with_context))
        assert where == ["syntagma= '😀'"]
        inp_syntagma_splitted = [
         'klitze', 'kleine']
        inp_syntagma_unsplitted = 'klitze++kleine'
        scope = 2
        with_context = False
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted, scope, with_context=with_context))
        assert where == ["syntagma= 'klitze++kleine'"]
        inp_syntagma_splitted = [
         'klitze', 'kleine', 'überaschung']
        inp_syntagma_unsplitted = 'klitze++kleine++überaschung'
        scope = 3
        with_context = False
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted, scope, with_context=with_context))
        assert where == ["syntagma= 'klitze++kleine++überaschung'"]
        inp_syntagma_splitted = [
         '1', 2, 3]
        inp_syntagma_unsplitted = '1++2++3'
        scope = 3
        with_context = False
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted, scope, with_context=with_context))
        assert where == ["syntagma= '1++2++3'"]
        inp_syntagma_splitted = [
         '1', 2, 3]
        inp_syntagma_unsplitted = '1++2++3'
        scope = 3
        with_context = False
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted, scope, with_context=with_context))
        assert where == ["syntagma= '1++2++3'"]
        inp_syntagma_splitted = [
         '1', 2, 3]
        inp_syntagma_unsplitted = False
        scope = 3
        with_context = False
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted, scope, with_context=with_context))
        assert where == ["syntagma= '1++2++3'"]
        inp_syntagma_splitted = [
         '1', 2, 3]
        inp_syntagma_unsplitted = False
        scope = 3
        with_context = False
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted, scope, with_context=with_context))
        assert where == ["syntagma= '1++2++3'"]
        inp_syntagma_splitted = [
         1, 2, 3]
        inp_syntagma_unsplitted = False
        scope = 3
        with_context = False
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted, scope, with_context=with_context))
        assert where == ["syntagma= '1++2++3'"]
        inp_syntagma_splitted = [
         1, 2, 3]
        inp_syntagma_unsplitted = '1++2++3'
        scope = 3
        with_context = False
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted, scope, with_context=with_context))
        assert where == ["syntagma= '1++2++3'"]
        inp_syntagma_splitted = [
         1, 2, 3]
        inp_syntagma_unsplitted = '1++2++3'
        scope = 3
        with_context = False
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted, scope, with_context=with_context))
        assert where == ["syntagma= '1++2++3'"]
        inp_syntagma_splitted = [
         'JJ']
        inp_syntagma_unsplitted = False
        scope = 1
        with_context = True
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted, scope, with_context=with_context, syntagma_type='pos'))
        assert where == [["pos='JJ' "]]
        inp_syntagma_splitted = [
         'JJ', 'JJ']
        inp_syntagma_unsplitted = False
        scope = 2
        with_context = True
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted, scope, with_context=with_context, syntagma_type='pos'))
        assert where == [["pos='JJ' ", 'json_extract("context_infoR1", "$[0]")  = "JJ"'], ['json_extract("context_infoL1", "$[0]")  = "JJ"', "pos='JJ' "]]
        inp_syntagma_splitted = [
         'JJ', 'JJ', 'JJ']
        inp_syntagma_unsplitted = False
        scope = 3
        with_context = True
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted, scope, with_context=with_context, syntagma_type='pos'))
        assert where == [["pos='JJ' ", 'json_extract("context_infoR1", "$[0]")  = "JJ"', 'json_extract("context_infoR2", "$[0]")  = "JJ"'], ['json_extract("context_infoL1", "$[0]")  = "JJ"', "pos='JJ' ", 'json_extract("context_infoR1", "$[0]")  = "JJ"'], ['json_extract("context_infoL2", "$[0]")  = "JJ"', 'json_extract("context_infoL1", "$[0]")  = "JJ"', "pos='JJ' "]]
        inp_syntagma_splitted = [
         'JJ']
        inp_syntagma_unsplitted = False
        scope = 1
        with_context = True
        sentiment = 'positive'
        syntagma_type = 'pos'
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted, scope, with_context=with_context, syntagma_type=syntagma_type, sentiment=sentiment))
        assert where == [["pos='JJ' ", "polarity LIKE '%positive%'"]]
        inp_syntagma_splitted = [
         'JJ', 'JJ']
        inp_syntagma_unsplitted = False
        scope = 2
        with_context = True
        sentiment = 'positive'
        syntagma_type = 'pos'
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted, scope, with_context=with_context, syntagma_type=syntagma_type, sentiment=sentiment))
        assert where == [["pos='JJ' ", 'json_extract("context_infoR1", "$[0]")  = "JJ"', "polarity LIKE '%positive%'"], ['json_extract("context_infoL1", "$[0]")  = "JJ"', "pos='JJ' ", "polarity LIKE '%positive%'"]]
        inp_syntagma_splitted = [
         'like']
        inp_syntagma_unsplitted = False
        scope = 1
        with_context = True
        sentiment = 'positive'
        syntagma_type = 'lexem'
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted, scope, with_context=with_context, syntagma_type=syntagma_type, sentiment=sentiment))
        assert where == [["normalized_word='like' ", "polarity LIKE '%positive%'"]]
        inp_syntagma_splitted = [
         'like', 'you']
        inp_syntagma_unsplitted = False
        scope = 2
        with_context = True
        sentiment = 'positive'
        syntagma_type = 'lexem'
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted, scope, with_context=with_context, syntagma_type=syntagma_type, sentiment=sentiment))
        assert where == [["normalized_word='like' ", "contextR1='you'", "polarity LIKE '%positive%'"], ["contextL1='like'", "normalized_word='you' ", "polarity LIKE '%positive%'"]]
        stats = Stats(mode='free', use_cash=True, logger_usage=False)
        stats.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_stats_de))
        inp_syntagma_splitted = ['JJ']
        inp_syntagma_unsplitted = False
        scope = 1
        with_context = False
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted, scope, with_context=with_context, syntagma_type='pos'))
        assert not where

    @attr(status='stable')
    def test_clean_baseline_table_615(self):
        self.prj_folder()
        self.test_dbs()
        stats = Stats(mode=self.mode, use_cash=True, status_bar=True)
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['stats']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'stats'
        stats.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_stats_de))
        baseline_rownum_bevore = stats.statsdb.rownum('baseline')
        assert stats.clean_baseline_table()
        stats.statsdb.commit()
        assert stats.clean_baseline_table()
        stats.statsdb.commit()
        baseline_rownum_after = stats.statsdb.rownum('baseline')
        assert baseline_rownum_bevore > baseline_rownum_after

    @attr(status='stable')
    def test_drop_indexes_616(self):
        self.prj_folder()
        self.test_dbs()
        stats = Stats(mode=self.mode, use_cash=True)
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['stats']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'stats'
        stats.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_stats_en))
        assert stats._get_created_indexes()
        stats._drop_created_indexes()
        assert not stats._get_created_indexes()

    @attr(status='stable')
    def test_create_indexes_617(self):
        self.prj_folder()
        self.test_dbs()
        stats = Stats(mode=self.mode, use_cash=True)
        stats.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_stats_en))
        stats._drop_created_indexes()
        number_indexes_bevore = stats._get_number_created_indexes()
        number_should_be_created = stats.create_additional_indexes(optimized_for_long_syntagmas=True)
        number_indexes_after = stats._get_number_created_indexes()
        assert number_indexes_after - number_indexes_bevore == number_should_be_created
        stats._drop_created_indexes()
        number_indexes_bevore = stats._get_number_created_indexes()
        number_should_be_created = stats.create_additional_indexes(optimized_for_long_syntagmas=False)
        number_indexes_after = stats._get_number_created_indexes()
        assert number_indexes_after - number_indexes_bevore == number_should_be_created
        stats._drop_created_indexes()
        number_indexes_bevore = stats._get_number_created_indexes()
        number_should_be_created = stats.create_additional_indexes(scope=3, optimized_for_long_syntagmas=False)
        number_indexes_after = stats._get_number_created_indexes()
        assert number_indexes_after - number_indexes_bevore == number_should_be_created
        stats._drop_created_indexes()
        number_indexes_bevore = stats._get_number_created_indexes()
        number_should_be_created = stats.create_additional_indexes(scope=2, optimized_for_long_syntagmas=False)
        stats._drop_created_indexes()
        number_should_be_created = stats.create_additional_indexes(scope=3, optimized_for_long_syntagmas=False)
        stats._drop_created_indexes()
        number_indexes_bevore = stats._get_number_created_indexes()
        number_should_be_created1 = stats.create_additional_indexes()
        number_indexes_after1 = stats._get_number_created_indexes()
        number_should_be_created2 = stats.create_additional_indexes()
        number_indexes_after2 = stats._get_number_created_indexes()
        assert number_indexes_after2 - number_indexes_bevore == number_should_be_created1

    @attr(status='stable')
    def test_clean_baseline_table_618(self):
        self.prj_folder()
        self.test_dbs()
        stats = Stats(mode=self.mode, use_cash=True)
        stats.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_stats_en))
        assert stats.optimize_db()

    @attr(status='stable')
    def test_compute_baseline_sum_619(self):
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
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['stats']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'stats'
        stats = Stats(mode=self.mode, use_cash=True, status_bar=True)
        stats.init(self.tempdir_project_folder, name, language, visibility, corpus_id=corpus_id, version=version, encryption_key=encryption_key, full_repetativ_syntagma=True, baseline_delimiter='++')
        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_en))
        stats.compute(corp, stream_number=1, adjust_to_cpu=False, freeze_db=False, optimized_for_long_syntagmas=True)
        stats.optimize_db()
        stats._compute_baseline_sum()
        stats.statsdb.commit()
        baseline = stats.statsdb.getall('baseline')
        right_baseline = [
         (':-(++#shetlife++http://www.noooo.com', ':-(++#shetlif++http://www.noooo.com', 3,
 1, None, None, None, None, None, None),
         ('tiny++model++,++which++we', 'tini++model++,++which++we', 5, 1, None, None, None,
 None, None, None),
         ('.++:-(++@real_trump++#shetlife', '.++:-(++@real_trump++#shetlif', 4, 1, None, None,
 None, None, None, None),
         ('pity++for++me++.++:-(', 'piti++for++me++.++:-(', 5, 1, None, None, None, None, None,
 None),
         ('🌈++😀++🌈++😀', '🌈++😀++🌈++😀', 4, 1, '[2, 2, "IGNOR", "IGNOR"]', '[2, 2, "IGNOR", "IGNOR"]',
 None, None, '1', None),
         ('tiny++model++,++which', 'tini++model++,++which', 4, 1, None, None, None, None, None,
 None),
         ('a++bad++news++,', 'a++bad++news++,', 4, 1, None, None, None, None, None, None),
         ('.++but', '.++but', 2, 3, None, None, None, None, None, None),
         ('.++:-(++@real_trump', '.++:-(++@real_trump', 3, 1, None, None, None, None, None,
 None),
         ('about++it++?++1++😫++1', 'about++it++?++1++😫++1', 6, 1, None, None, None, None, None,
 None),
         ('explain++a++big', 'explain++a++big', 3, 1, None, None, None, None, None, None),
         ('me++😫++,', 'me++😫++,', 3, 1, None, None, None, None, None, None),
         ('liked++it++:p++=)++😀', 'like++it++:p++=)++😀', 5, 1, None, None, None, None, None,
 None),
         ('realy', 'reali', 1, 4, '2', '4', '1', '3', '2', '1'),
         ('to++se++you++-)', 'to++se++you++-)', 4, 1, None, None, None, None, None, None),
         ('about++it++?++1', 'about++it++?++1', 4, 1, None, None, None, None, None, None),
         ('tiny', 'tini', 1, 10, '1', '1', '2', '9', '1', '2'),
         ('but++it++was++also++very', 'but++it++was++also++veri', 5, 1, None, None, None, None,
 None, None),
         ('surprise++.++but++you', 'surpris++.++but++you', 4, 1, None, None, None, None, None,
 None),
         ('🌈++😀++🌈', '🌈++😀++🌈', 3, 1, '[2, 1, "IGNOR"]', '[2, 1, "IGNOR"]', None, None, '1',
 None),
         ('explanation++.++right++?++what++do', 'explan++.++right++?++what++do', 6, 1, None,
 None, None, None, None, None),
         ('=)++😀++🌈++😀', '=)++😀++🌈++😀', 4, 1, None, None, None, None, None, None),
         ('what++do++you++think++about', 'what++do++you++think++about', 5, 1, None, None, None,
 None, None, None),
         ('😫++,', '😫++,', 2, 1, None, None, None, None, None, None),
         ('surprise++.++but', 'surpris++.++but', 3, 1, None, None, None, None, None, None),
         ('can++not++acept++.++-(++😫', 'can++not++acept++.++-(++😫', 6, 1, None, None, None,
 None, None, None),
         ('🌈', '🌈', 1, 3, '3', '3', None, None, '3', None),
         ('but++it++was++also++very++pity', 'but++it++was++also++veri++piti', 6, 1, None, None,
 None, None, None, None),
         ('i++realy++liked', 'i++reali++like', 3, 1, None, None, None, None, None, None),
         ('but++you++but', 'but++you++but', 3, 2, '[10, 4, "IGNOR"]', '[15, 4, "IGNOR"]', '[4, 2, "IGNOR"]',
 '[10, 4, "IGNOR"]', '2', '2'),
         (':-(++#shetlife', ':-(++#shetlif', 2, 1, None, None, None, None, None, None),
         ('a++big++things', 'a++big++thing', 3, 1, None, None, None, None, None, None),
         ('?++what++do++you', '?++what++do++you', 4, 1, None, None, None, None, None, None),
         ('se', 'se', 1, 1, '1', '1', None, None, '1', None),
         ('.++but++you++but++you', '.++but++you++but++you', 5, 2, None, None, None, None, None,
 None),
         ('very++pity++for++me', 'veri++piti++for++me', 4, 1, None, None, None, None, None,
 None),
         ('tiny++surprise++.', 'tini++surpris++.', 3, 1, None, None, None, None, None, None),
         (':-(++@real_trump', ':-(++@real_trump', 2, 1, None, None, None, None, None, None),
         ('-(++😫++:-(++#shetlife', '-(++😫++:-(++#shetlif', 4, 1, None, None, None, None, None,
 None),
         ('.++but++you++but', '.++but++you++but', 4, 2, None, None, None, None, None, None),
         (',++but++a++big++explanation', ',++but++a++big++explan', 5, 1, None, None, None, None,
 None, None),
         ('=)++😀', '=)++😀', 2, 1, '[1, 1]', '[1, 1]', None, None, '1', None),
         ('for++me++.++:-(++@real_trump', 'for++me++.++:-(++@real_trump', 5, 1, None, None,
 None, None, None, None),
         ('tiny++model++,', 'tini++model++,', 3, 2, None, None, None, None, None, None),
         ('you++think++about++it++?++1', 'you++think++about++it++?++1', 6, 1, None, None, None,
 None, None, None),
         ('use++for++explain++a++big++things', 'use++for++explain++a++big++thing', 6, 1, None,
 None, None, None, None, None),
         ('use++for++explain++a++big', 'use++for++explain++a++big', 5, 1, None, None, None,
 None, None, None),
         ('model++,++which++we++can', 'model++,++which++we++can', 5, 1, None, None, None, None,
 None, None),
         ('it++:p++=)++😀++🌈++😀', 'it++:p++=)++😀++🌈++😀', 6, 1, None, None, None, None, None,
 None),
         ('?++what++do++you++think', '?++what++do++you++think', 5, 1, None, None, None, None,
 None, None),
         ('bad++news++,', 'bad++news++,', 3, 1, None, None, None, None, None, None),
         ('but++you++but++you', 'but++you++but++you', 4, 2, '[10, 6, "IGNOR", "IGNOR"]', '[15, 8, "IGNOR", "IGNOR"]',
 None, None, '2', None),
         ('bad', 'bad', 1, 6, '4', '7', '1', '5', '4', '1'),
         ('pity++for++me', 'piti++for++me', 3, 1, None, None, None, None, None, None),
         ('.++-(++😫++:-(', '.++-(++😫++:-(', 4, 1, None, None, None, None, None, None),
         ('tiny++surprise++.++but++you', 'tini++surpris++.++but++you', 5, 1, None, None, None,
 None, None, None),
         ('but++i++realy++liked', 'but++i++reali++like', 4, 1, None, None, None, None, None,
 None),
         (',++but++i++realy++liked', ',++but++i++reali++like', 5, 1, None, None, None, None,
 None, None),
         ('.++right++?', '.++right++?', 3, 1, None, None, None, None, None, None),
         ('1++😫++1++.++but++you', '1++😫++1++.++but++you', 6, 1, None, None, None, None, None,
 None),
         ('a++bad++news++,++which++we', 'a++bad++news++,++which++we', 6, 1, None, None, None,
 None, None, None),
         ('😫++:-(', '😫++:-(', 2, 1, '[1, 1]', '[1, 1]', None, None, '1', None),
         ('?++1++😫++1', '?++1++😫++1', 4, 1, '[1, 2, 1, "IGNOR"]', '[1, 2, 1, "IGNOR"]', None,
 None, '1', None),
         ('.++but++it++was++also++very', '.++but++it++was++also++veri', 6, 1, None, None, None,
 None, None, None),
         (',++but++a++big', ',++but++a++big', 4, 1, None, None, None, None, None, None),
         ('😫++:-(++#shetlife', '😫++:-(++#shetlif', 3, 1, None, None, None, None, None, None),
         ('also++very++pity++for++me', 'also++veri++piti++for++me', 5, 1, None, None, None,
 None, None, None),
         ('but++a++big++explanation++.++right', 'but++a++big++explan++.++right', 6, 1, None,
 None, None, None, None, None),
         ('it++was++also++very', 'it++was++also++veri', 4, 1, None, None, None, None, None,
 None),
         ('but++a++big++explanation++.', 'but++a++big++explan++.', 5, 1, None, None, None, None,
 None, None),
         (',++but++i++realy', ',++but++i++reali', 4, 1, None, None, None, None, None, None),
         ('it++?++1++😫', 'it++?++1++😫', 4, 1, None, None, None, None, None, None),
         ('a++big', 'a++big', 2, 2, None, None, None, None, None, None),
         ('acept++.++-(', 'acept++.++-(', 3, 1, None, None, None, None, None, None),
         ('but', 'but', 1, 13, '11', '16', '4', '10', '11', '4'),
         ('tiny++surprise', 'tini++surpris', 2, 1, None, None, None, None, None, None),
         ('realy++liked', 'reali++like', 2, 1, None, None, None, None, None, None),
         ('what++do++you++think++about++it', 'what++do++you++think++about++it', 6, 1, None,
 None, None, None, None, None),
         (':p++=)++😀++🌈++😀', ':p++=)++😀++🌈++😀', 5, 1, None, None, None, None, None, None),
         ('you++-)', 'you++-)', 2, 1, None, None, None, None, None, None),
         ('😀++🌈++😀++🌈', '😀++🌈++😀++🌈', 4, 1, '[2, 2, "IGNOR", "IGNOR"]', '[2, 2, "IGNOR", "IGNOR"]',
 None, None, '1', None),
         ('.++:-(++@real_trump++#shetlife++#readytogo', '.++:-(++@real_trump++#shetlif++#readytogo',
 5, 1, None, None, None, None, None, None),
         ('what++do++you', 'what++do++you', 3, 1, None, None, None, None, None, None),
         ('surprise++for++me++😫', 'surpris++for++me++😫', 4, 1, None, None, None, None, None,
 None),
         ('?++what++do++you++think++about', '?++what++do++you++think++about', 6, 1, None, None,
 None, None, None, None),
         ('a++bad++news', 'a++bad++news', 3, 1, None, None, None, None, None, None),
         ('very++pity++for', 'veri++piti++for', 3, 1, None, None, None, None, None, None),
         (',++but++i', ',++but++i', 3, 1, None, None, None, None, None, None),
         ('glad++to', 'glad++to', 2, 1, None, None, None, None, None, None),
         ('big++things++.', 'big++thing++.', 3, 1, None, None, None, None, None, None),
         ('for++me++😫++,', 'for++me++😫++,', 4, 1, None, None, None, None, None, None),
         (':-(++@real_trump++#shetlife++#readytogo', ':-(++@real_trump++#shetlif++#readytogo',
 4, 1, None, None, None, None, None, None),
         ('.++:-(++@real_trump++#shetlife++#readytogo++http://www.absurd.com', '.++:-(++@real_trump++#shetlif++#readytogo++http://www.absurd.com',
 6, 1, None, None, None, None, None, None),
         ('.', '.', 1, 7, '1', '1', None, None, '1', None),
         ('but++i++realy++liked++it', 'but++i++reali++like++it', 5, 1, None, None, None, None,
 None, None),
         ('pity', 'piti', 1, 4, '2', '4', '1', '4', '2', '1'),
         ('explanation++.++right++?', 'explan++.++right++?', 4, 1, None, None, None, None, None,
 None),
         ('do++you++think++about++it', 'do++you++think++about++it', 5, 1, None, None, None,
 None, None, None),
         ('think++about++it++?++1', 'think++about++it++?++1', 5, 1, None, None, None, None,
 None, None),
         ('also++very++pity++for++me++.', 'also++veri++piti++for++me++.', 6, 1, None, None,
 None, None, None, None),
         ('😀++🌈++😀++🌈++😀', '😀++🌈++😀++🌈++😀', 5, 1, '[3, 2, "IGNOR", "IGNOR", "IGNOR"]', '[3, 2, "IGNOR", "IGNOR", "IGNOR"]',
 None, None, '1', None),
         ('se++you', 'se++you', 2, 1, None, None, None, None, None, None),
         ('realy++liked++it', 'reali++like++it', 3, 1, None, None, None, None, None, None),
         ('me++😫++,++but', 'me++😫++,++but', 4, 1, None, None, None, None, None, None),
         ('for++me++.++:-(++@real_trump++#shetlife', 'for++me++.++:-(++@real_trump++#shetlif',
 6, 1, None, None, None, None, None, None),
         ('😀++🌈++😀', '😀++🌈++😀', 3, 3, '[2, 1, "IGNOR"]', '[3, 1, "IGNOR"]', None, None, '1',
 None),
         ('big++explanation++.++right++?', 'big++explan++.++right++?', 5, 1, None, None, None,
 None, None, None),
         ('bad++news', 'bad++news', 2, 1, None, None, None, None, None, None),
         ('glad++to++se++you', 'glad++to++se++you', 4, 1, None, None, None, None, None, None),
         ('model++,++but++a++big', 'model++,++but++a++big', 5, 1, None, None, None, None, None,
 None),
         ('😫++1++.', '😫++1++.', 3, 1, None, None, None, None, None, None),
         ('it++:p++=)++😀++🌈', 'it++:p++=)++😀++🌈', 5, 1, None, None, None, None, None, None),
         ('explain++a++big++things', 'explain++a++big++thing', 4, 1, None, None, None, None,
 None, None),
         ('also++very', 'also++veri', 2, 1, None, None, None, None, None, None),
         ('to++se', 'to++se', 2, 1, None, None, None, None, None, None),
         ('you++but++you++😀++🌈', 'you++but++you++😀++🌈', 5, 1, '[3, 3, "IGNOR", 1, 1]', '[4, 3, "IGNOR", 1, 1]',
 None, None, '1', None),
         ('to++se++you', 'to++se++you', 3, 1, None, None, None, None, None, None),
         ('realy++bad++surprise++for++me++😫', 'reali++bad++surpris++for++me++😫', 6, 1, None,
 None, None, None, None, None),
         ('realy++liked++it++:p', 'reali++like++it++:p', 4, 1, None, None, None, None, None,
 None),
         ('you++but++you++😀', 'you++but++you++😀', 4, 1, '[3, 3, "IGNOR", 1]', '[4, 3, "IGNOR", 1]',
 None, None, '1', None),
         ('not++acept++.++-(++😫++:-(', 'not++acept++.++-(++😫++:-(', 6, 1, None, None, None,
 None, None, None),
         ('very', 'veri', 1, 3, '2', '4', '1', '3', '2', '1'),
         ('1++.++but++you', '1++.++but++you', 4, 1, None, None, None, None, None, None),
         ('surprise++for++me++😫++,', 'surpris++for++me++😫++,', 5, 1, None, None, None, None,
 None, None),
         ('.++right++?++what++do', '.++right++?++what++do', 5, 1, None, None, None, None, None,
 None),
         ('was++also++very++pity', 'was++also++veri++piti', 4, 1, None, None, None, None, None,
 None),
         ('1++😫++1', '1++😫++1', 3, 1, '[2, 1, "IGNOR"]', '[2, 1, "IGNOR"]', None, None, '1',
 None),
         ('big++explanation++.++right', 'big++explan++.++right', 4, 1, None, None, None, None,
 None, None),
         ('for++explain++a++big', 'for++explain++a++big', 4, 1, None, None, None, None, None,
 None),
         ('for++me++😫++,++but++i', 'for++me++😫++,++but++i', 6, 1, None, None, None, None, None,
 None),
         (':-(++@real_trump++#shetlife', ':-(++@real_trump++#shetlif', 3, 1, None, None, None,
 None, None, None),
         ('?++1++😫++1++.++but', '?++1++😫++1++.++but', 6, 1, None, None, None, None, None, None),
         ('1++😫++1++.++but', '1++😫++1++.++but', 5, 1, None, None, None, None, None, None),
         ('think++about++it++?', 'think++about++it++?', 4, 1, None, None, None, None, None,
 None),
         ('big', 'big', 1, 5, '2', '2', '2', '5', '2', '2'),
         ('realy++liked++it++:p++=)', 'reali++like++it++:p++=)', 5, 1, None, None, None, None,
 None, None),
         ('we++can++not++acept++.++-(', 'we++can++not++acept++.++-(', 6, 1, None, None, None,
 None, None, None),
         ('a++big++explanation++.', 'a++big++explan++.', 4, 1, None, None, None, None, None,
 None),
         ('for++explain++a++big++things', 'for++explain++a++big++thing', 5, 1, None, None, None,
 None, None, None),
         ('model', 'model', 1, 2, '1', '2', None, None, '1', None),
         ('bad++news++,++which', 'bad++news++,++which', 4, 1, None, None, None, None, None,
 None),
         ('you++😀++🌈++😀', 'you++😀++🌈++😀', 4, 1, '[1, 2, 1, "IGNOR"]', '[2, 2, 1, "IGNOR"]',
 None, None, '1', None),
         ('i++realy++liked++it++:p', 'i++reali++like++it++:p', 5, 1, None, None, None, None,
 None, None),
         ('but++i++realy++liked++it++:p', 'but++i++reali++like++it++:p', 6, 1, None, None, None,
 None, None, None),
         ('glad++to++se++you++-)', 'glad++to++se++you++-)', 5, 1, None, None, None, None, None,
 None),
         ('1++😫++1++.', '1++😫++1++.', 4, 1, None, None, None, None, None, None),
         ('you++think', 'you++think', 2, 1, None, None, None, None, None, None),
         ('not++acept++.++-(++😫', 'not++acept++.++-(++😫', 5, 1, None, None, None, None, None,
 None),
         (',++but++a++big++explanation++.', ',++but++a++big++explan++.', 6, 1, None, None, None,
 None, None, None),
         ('think++about++it++?++1++😫', 'think++about++it++?++1++😫', 6, 1, None, None, None,
 None, None, None),
         ('but++you', 'but++you', 2, 4, '[10, 6]', '[15, 8]', '[2, 2]', '[4, 4]', '4', '2'),
         ('-)', '-)', 1, 1, '1', '1', None, None, '1', None),
         ('-(++😫', '-(++😫', 2, 1, '[1, 1]', '[1, 1]', None, None, '1', None),
         ('big++explanation++.++right++?++what', 'big++explan++.++right++?++what', 6, 1, None,
 None, None, None, None, None),
         ('me++.++:-(', 'me++.++:-(', 3, 1, None, None, None, None, None, None),
         ('tiny++surprise++.++but', 'tini++surpris++.++but', 4, 1, None, None, None, None, None,
 None),
         ('-(++😫++:-(++#shetlife++http://www.noooo.com', '-(++😫++:-(++#shetlif++http://www.noooo.com',
 5, 1, None, None, None, None, None, None),
         ('😫++1++.++but++you', '😫++1++.++but++you', 5, 1, None, None, None, None, None, None),
         ('it++?', 'it++?', 2, 1, None, None, None, None, None, None),
         ('😫++,++but', '😫++,++but', 3, 1, None, None, None, None, None, None),
         ('model++,', 'model++,', 2, 2, None, None, None, None, None, None),
         ('me++.++:-(++@real_trump++#shetlife++#readytogo', 'me++.++:-(++@real_trump++#shetlif++#readytogo',
 6, 1, None, None, None, None, None, None),
         ('right++?++what++do', 'right++?++what++do', 4, 1, None, None, None, None, None, None),
         ('🌈++😀', '🌈++😀', 2, 3, '[2, 2]', '[2, 2]', None, None, '2', None),
         ('=)', '=)', 1, 1, '1', '1', None, None, '1', None),
         ('it++was++also++very++pity', 'it++was++also++veri++piti', 5, 1, None, None, None,
 None, None, None),
         ('i++realy++liked++it', 'i++reali++like++it', 4, 1, None, None, None, None, None, None),
         ('se++you++-)', 'se++you++-)', 3, 1, None, None, None, None, None, None),
         ('tiny++model', 'tini++model', 2, 2, None, None, None, None, None, None),
         ('it++:p++=)++😀', 'it++:p++=)++😀', 4, 1, None, None, None, None, None, None),
         ('a++bad++news++,++which', 'a++bad++news++,++which', 5, 1, None, None, None, None,
 None, None),
         ('it++?++1++😫++1++.', 'it++?++1++😫++1++.', 6, 1, None, None, None, None, None, None),
         ('1++.++but++you++but', '1++.++but++you++but', 5, 1, None, None, None, None, None,
 None),
         ('right', 'right', 1, 1, '1', '1', None, None, '1', None),
         ('it++:p++=)', 'it++:p++=)', 3, 1, None, None, None, None, None, None),
         ('model++,++which++we', 'model++,++which++we', 4, 1, None, None, None, None, None,
 None),
         ('but++you++but++you++😀++🌈', 'but++you++but++you++😀++🌈', 6, 1, '[5, 3, "IGNOR", "IGNOR", 1, 1]',
 '[5, 4, "IGNOR", "IGNOR", 1, 1]', None, None, '1', None),
         ('#shetlife', '#shetlif', 1, 3, None, None, '1', '2', None, '1'),
         ('?', '?', 1, 2, '1', '1', None, None, '1', None),
         ('me++.++:-(++@real_trump', 'me++.++:-(++@real_trump', 4, 1, None, None, None, None,
 None, None),
         ('acept++.++-(++😫++:-(', 'acept++.++-(++😫++:-(', 5, 1, None, None, None, None, None,
 None),
         ('but++you++😀++🌈', 'but++you++😀++🌈', 4, 1, '[3, 1, 1, 1]', '[3, 2, 1, 1]', None, None,
 '1', None),
         ('very++pity++for++me++.', 'veri++piti++for++me++.', 5, 1, None, None, None, None,
 None, None),
         ('😫++:-(++#shetlife++http://www.noooo.com', '😫++:-(++#shetlif++http://www.noooo.com',
 4, 1, None, None, None, None, None, None),
         ('explanation++.', 'explan++.', 2, 1, None, None, None, None, None, None),
         ('.++but++you++but++you++😀', '.++but++you++but++you++😀', 6, 1, None, None, None, None,
 None, None),
         ('.++-(++😫++:-(++#shetlife++http://www.noooo.com', '.++-(++😫++:-(++#shetlif++http://www.noooo.com',
 6, 1, None, None, None, None, None, None),
         ('.++-(', '.++-(', 2, 1, None, None, None, None, None, None),
         ('i++realy++liked++it++:p++=)', 'i++reali++like++it++:p++=)', 6, 1, None, None, None,
 None, None, None),
         ('😀++🌈', '😀++🌈', 2, 3, '[3, 3]', '[3, 3]', None, None, '3', None),
         ('explanation', 'explan', 1, 1, '1', '1', None, None, '1', None),
         ('you++but++you++😀++🌈++😀', 'you++but++you++😀++🌈++😀', 6, 1, '[3, 3, "IGNOR", 2, 1, "IGNOR"]',
 '[4, 3, "IGNOR", 2, 1, "IGNOR"]', None, None, '1', None),
         ('do++you++think', 'do++you++think', 3, 1, None, None, None, None, None, None),
         ('acept++.++-(++😫++:-(++#shetlife', 'acept++.++-(++😫++:-(++#shetlif', 6, 1, None, None,
 None, None, None, None),
         ('but++i', 'but++i', 2, 1, None, None, None, None, None, None),
         ('😫++,++but++i++realy++liked', '😫++,++but++i++reali++like', 6, 1, None, None, None,
 None, None, None),
         ('me++😫++,++but++i++realy', 'me++😫++,++but++i++reali', 6, 1, None, None, None, None,
 None, None),
         ('but++you++but++you++😀', 'but++you++but++you++😀', 5, 1, '[5, 3, "IGNOR", "IGNOR", 1]',
 '[5, 4, "IGNOR", "IGNOR", 1]', None, None, '1', None),
         ('acept++.++-(++😫', 'acept++.++-(++😫', 4, 1, None, None, None, None, None, None),
         (',++but', ',++but', 2, 2, None, None, None, None, None, None),
         ('was++also++very++pity++for', 'was++also++veri++piti++for', 5, 1, None, None, None,
 None, None, None),
         ('surprise++.++but++you++but', 'surpris++.++but++you++but', 5, 1, None, None, None,
 None, None, None),
         ('surprise++.++but++you++but++you', 'surpris++.++but++you++but++you', 6, 1, None, None,
 None, None, None, None),
         ('a++big++explanation++.++right', 'a++big++explan++.++right', 5, 1, None, None, None,
 None, None, None),
         (':p++=)', ':p++=)', 2, 1, None, None, None, None, None, None),
         ('😫++,++but++i', '😫++,++but++i', 4, 1, None, None, None, None, None, None),
         ('tiny++model++,++which++we++can', 'tini++model++,++which++we++can', 6, 1, None, None,
 None, None, None, None),
         ('😫++1', '😫++1', 2, 1, '[1, 1]', '[1, 1]', None, None, '1', None),
         ('?++1++😫', '?++1++😫', 3, 1, '[1, 1, 1]', '[1, 1, 1]', None, None, '1', None),
         ('was++also++very', 'was++also++veri', 3, 1, None, None, None, None, None, None),
         (':p++=)++😀++🌈', ':p++=)++😀++🌈', 4, 1, None, None, None, None, None, None),
         ('surprise++for++me++😫++,++but', 'surpris++for++me++😫++,++but', 6, 1, None, None, None,
 None, None, None),
         ('about++it++?++1++😫', 'about++it++?++1++😫', 5, 1, None, None, None, None, None, None),
         ('me++.++:-(++@real_trump++#shetlife', 'me++.++:-(++@real_trump++#shetlif', 5, 1, None,
 None, None, None, None, None),
         ('you++think++about++it', 'you++think++about++it', 4, 1, None, None, None, None, None,
 None),
         ('but++you++😀++🌈++😀', 'but++you++😀++🌈++😀', 5, 1, '[3, 1, 2, 1, "IGNOR"]', '[3, 2, 2, 1, "IGNOR"]',
 None, None, '1', None),
         ('but++you++😀++🌈++😀++🌈', 'but++you++😀++🌈++😀++🌈', 6, 1, '[3, 1, 2, 2, "IGNOR", "IGNOR"]',
 '[3, 2, 2, 2, "IGNOR", "IGNOR"]', None, None, '1', None),
         ('also++very++pity++for', 'also++veri++piti++for', 4, 1, None, None, None, None, None,
 None),
         ('you++😀', 'you++😀', 2, 1, '[1, 1]', '[2, 1]', None, None, '1', None),
         ('glad++to++se', 'glad++to++se', 3, 1, None, None, None, None, None, None),
         ('you++😀++🌈++😀++🌈', 'you++😀++🌈++😀++🌈', 5, 1, '[1, 2, 2, "IGNOR", "IGNOR"]', '[2, 2, 2, "IGNOR", "IGNOR"]',
 None, None, '1', None),
         ('#shetlife++http://www.noooo.com', '#shetlif++http://www.noooo.com', 2, 1, None, None,
 None, None, None, None),
         ('1++.++but++you++but++you', '1++.++but++you++but++you', 6, 1, None, None, None, None,
 None, None),
         ('was++also++very++pity++for++me', 'was++also++veri++piti++for++me', 6, 1, None, None,
 None, None, None, None),
         ('.++-(++😫++:-(++#shetlife', '.++-(++😫++:-(++#shetlif', 5, 1, None, None, None, None,
 None, None),
         ('1++.', '1++.', 2, 1, None, None, None, None, None, None),
         ('i++realy', 'i++reali', 2, 1, None, None, None, None, None, None),
         ('can++use++for++explain++a++big', 'can++use++for++explain++a++big', 6, 1, None, None,
 None, None, None, None),
         ('very++pity', 'veri++piti', 2, 1, '[2, 2]', '[4, 4]', '[1, 1]', '[3, 4]', '1', '1'),
         ('liked++it++:p++=)++😀++🌈', 'like++it++:p++=)++😀++🌈', 6, 1, None, None, None, None,
 None, None),
         ('do++you++think++about', 'do++you++think++about', 4, 1, None, None, None, None, None,
 None),
         ('bad++surprise++for++me++😫++,', 'bad++surpris++for++me++😫++,', 6, 1, None, None, None,
 None, None, None),
         (':-(++@real_trump++#shetlife++#readytogo++http://www.absurd.com', ':-(++@real_trump++#shetlif++#readytogo++http://www.absurd.com',
 5, 1, None, None, None, None, None, None),
         ('me++.', 'me++.', 2, 1, None, None, None, None, None, None),
         ('me++😫++,++but++i', 'me++😫++,++but++i', 5, 1, None, None, None, None, None, None),
         ('you++think++about++it++?', 'you++think++about++it++?', 5, 1, None, None, None, None,
 None, None),
         ('right++?++what++do++you', 'right++?++what++do++you', 5, 1, None, None, None, None,
 None, None),
         ('1', '1', 1, 2, '2', '2', None, None, '2', None),
         ('pity++for++me++.', 'piti++for++me++.', 4, 1, None, None, None, None, None, None),
         ('explain++a++big++things++.', 'explain++a++big++thing++.', 5, 1, None, None, None,
 None, None, None),
         ('what++do++you++think', 'what++do++you++think', 4, 1, None, None, None, None, None,
 None),
         ('for++me++.++:-(', 'for++me++.++:-(', 4, 1, None, None, None, None, None, None),
         ('😀', '😀', 1, 5, '4', '4', None, None, '4', None),
         ('you++but', 'you++but', 2, 2, '[4, 6]', '[4, 8]', '[2, 2]', '[4, 6]', '2', '2'),
         ('bad++news++,++which++we', 'bad++news++,++which++we', 5, 1, None, None, None, None,
 None, None),
         ('very++pity++for++me++.++:-(', 'veri++piti++for++me++.++:-(', 6, 1, None, None, None,
 None, None, None),
         ('.++right++?++what', '.++right++?++what', 4, 1, None, None, None, None, None, None),
         ('.++but++you', '.++but++you', 3, 2, None, None, None, None, None, None),
         ('but++a++big', 'but++a++big', 3, 1, None, None, None, None, None, None),
         ('it++was++also++very++pity++for', 'it++was++also++veri++piti++for', 6, 1, None, None,
 None, None, None, None),
         ('bad++news++,++which++we++can', 'bad++news++,++which++we++can', 6, 1, None, None,
 None, None, None, None),
         ('😫++,++but++i++realy', '😫++,++but++i++reali', 5, 1, None, None, None, None, None,
 None),
         ('=)++😀++🌈', '=)++😀++🌈', 3, 1, '[1, 1, 1]', '[1, 1, 1]', None, None, '1', None),
         ('for++me++.', 'for++me++.', 3, 1, None, None, None, None, None, None),
         ('realy++liked++it++:p++=)++😀', 'reali++like++it++:p++=)++😀', 6, 1, None, None, None,
 None, None, None),
         ('explanation++.++right++?++what', 'explan++.++right++?++what', 5, 1, None, None, None,
 None, None, None),
         ('model++,++but++a++big++explanation', 'model++,++but++a++big++explan', 6, 1, None,
 None, None, None, None, None),
         ('a++big++explanation', 'a++big++explan', 3, 1, None, None, None, None, None, None),
         ('you++but++you', 'you++but++you', 3, 2, '[6, 6, "IGNOR"]', '[8, 8, "IGNOR"]', None,
 None, '2', None),
         ('-(++😫++:-(', '-(++😫++:-(', 3, 1, '[1, 1, 1]', '[1, 1, 1]', None, None, '1', None),
         ('explanation++.++right', 'explan++.++right', 3, 1, None, None, None, None, None, None),
         ('you', 'you', 1, 8, '7', '9', '2', '4', '7', '2'),
         ('big++things', 'big++thing', 2, 1, None, None, None, None, None, None),
         ('it++?++1', 'it++?++1', 3, 1, None, None, None, None, None, None),
         ('for++me++😫', 'for++me++😫', 3, 1, None, None, None, None, None, None),
         ('-(', '-(', 1, 1, '1', '1', None, None, '1', None),
         ('tiny++surprise++.++but++you++but', 'tini++surpris++.++but++you++but', 6, 1, None,
 None, None, None, None, None),
         ('right++?++what++do++you++think', 'right++?++what++do++you++think', 6, 1, None, None,
 None, None, None, None),
         ('big++explanation++.', 'big++explan++.', 3, 1, None, None, None, None, None, None),
         ('for++explain++a++big++things++.', 'for++explain++a++big++thing++.', 6, 1, None, None,
 None, None, None, None),
         ('.++right', '.++right', 2, 1, None, None, None, None, None, None),
         ('😫', '😫', 1, 3, '3', '3', None, None, '3', None),
         ('not++acept++.++-(', 'not++acept++.++-(', 4, 1, None, None, None, None, None, None),
         ('for++me++😫++,++but', 'for++me++😫++,++but', 5, 1, None, None, None, None, None, None),
         ('you++think++about', 'you++think++about', 3, 1, None, None, None, None, None, None),
         ('a++bad', 'a++bad', 2, 1, None, None, None, None, None, None),
         ('?++1', '?++1', 2, 1, '[1, 1]', '[1, 1]', None, None, '1', None),
         ('do++you++think++about++it++?', 'do++you++think++about++it++?', 6, 1, None, None,
 None, None, None, None),
         ('can++not++acept++.++-(', 'can++not++acept++.++-(', 5, 1, None, None, None, None,
 None, None),
         ('a++big++things++.', 'a++big++thing++.', 4, 1, None, None, None, None, None, None),
         ('but++you++😀', 'but++you++😀', 3, 1, '[3, 1, 1]', '[3, 2, 1]', None, None, '1', None),
         ('😫++1++.++but', '😫++1++.++but', 4, 1, None, None, None, None, None, None),
         ('right++?', 'right++?', 2, 1, None, None, None, None, None, None),
         ('😫++1++.++but++you++but', '😫++1++.++but++you++but', 6, 1, None, None, None, None,
 None, None),
         ('pity++for++me++.++:-(++@real_trump', 'piti++for++me++.++:-(++@real_trump', 6, 1,
 None, None, None, None, None, None),
         ('it++?++1++😫++1', 'it++?++1++😫++1', 5, 1, None, None, None, None, None, None),
         ('tiny++model++,++but++a++big', 'tini++model++,++but++a++big', 6, 1, None, None, None,
 None, None, None),
         ('right++?++what', 'right++?++what', 3, 1, None, None, None, None, None, None),
         ('bad++surprise++for++me++😫', 'bad++surpris++for++me++😫', 5, 1, None, None, None, None,
 None, None),
         ('model++,++which', 'model++,++which', 3, 1, None, None, None, None, None, None),
         ('1++.++but', '1++.++but', 3, 1, None, None, None, None, None, None),
         ('pity++for', 'piti++for', 2, 1, None, None, None, None, None, None),
         (':p++=)++😀', ':p++=)++😀', 3, 1, None, None, None, None, None, None),
         ('me++😫', 'me++😫', 2, 1, None, None, None, None, None, None),
         ('also++very++pity', 'also++veri++piti', 3, 1, None, None, None, None, None, None),
         ('model++,++which++we++can++use', 'model++,++which++we++can++use', 6, 1, None, None,
 None, None, None, None),
         ('you++😀++🌈++😀++🌈++😀', 'you++😀++🌈++😀++🌈++😀', 6, 1, '[1, 3, 2, "IGNOR", "IGNOR", "IGNOR"]',
 '[2, 3, 2, "IGNOR", "IGNOR", "IGNOR"]', None, None, '1', None),
         ('about++it++?', 'about++it++?', 3, 1, None, None, None, None, None, None),
         ('but++i++realy', 'but++i++reali', 3, 1, None, None, None, None, None, None),
         ('liked++it++:p++=)', 'like++it++:p++=)', 4, 1, None, None, None, None, None, None),
         ('do++you', 'do++you', 2, 1, None, None, None, None, None, None),
         ('1++😫', '1++😫', 2, 1, '[1, 1]', '[1, 1]', None, None, '1', None),
         (':-(', ':-(', 1, 2, '2', '2', None, None, '2', None),
         ('?++1++😫++1++.', '?++1++😫++1++.', 5, 1, None, None, None, None, None, None),
         ('.++right++?++what++do++you', '.++right++?++what++do++you', 6, 1, None, None, None,
 None, None, None),
         ('big++explanation', 'big++explan', 2, 1, None, None, None, None, None, None),
         ('.++-(++😫', '.++-(++😫', 3, 1, None, None, None, None, None, None),
         ('but++a++big++explanation', 'but++a++big++explan', 4, 1, None, None, None, None, None,
 None),
         ('.++:-(', '.++:-(', 2, 1, '[1, 1]', '[1, 1]', None, None, '1', None),
         ('glad', 'glad', 1, 1, '1', '1', None, None, '1', None),
         ('a++big++explanation++.++right++?', 'a++big++explan++.++right++?', 6, 1, None, None,
 None, None, None, None),
         ('you++😀++🌈', 'you++😀++🌈', 3, 1, '[1, 1, 1]', '[2, 1, 1]', None, None, '1', None),
         (',++but++i++realy++liked++it', ',++but++i++reali++like++it', 6, 1, None, None, None,
 None, None, None)]
        set([ tuple(unicode(item) for item in b) for b in baseline ]).should.be.equal(set([ tuple(unicode(item) for item in b) for b in right_baseline ]))
        assert stats._compute_baseline_sum() > 0
        return

    @attr(status='stable')
    def test_recompute_syntagma_repetativity_scope_621(self):
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
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['stats']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'stats'
        stats = Stats(mode=self.mode, use_cash=True, status_bar=True)
        stats.init(self.tempdir_project_folder, name, language, visibility, corpus_id=corpus_id, version=version, encryption_key=encryption_key, full_repetativ_syntagma=True, baseline_delimiter='++')
        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_de))
        stats.compute(corp, stream_number=1, adjust_to_cpu=False, freeze_db=False)
        stats.optimize_db()
        assert stats._full_repetativ_syntagma == True
        assert stats.recompute_syntagma_repetativity_scope(False)
        assert stats._full_repetativ_syntagma == False
        assert stats.recompute_syntagma_repetativity_scope(True)
        assert stats._full_repetativ_syntagma == True
        stats = Stats(mode=self.mode, use_cash=True, status_bar=True)
        stats.init(self.tempdir_project_folder, name, language, visibility, corpus_id=corpus_id, version=version, encryption_key=encryption_key, full_repetativ_syntagma=False, baseline_delimiter='++')
        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_de))
        stats.compute(corp, stream_number=1, adjust_to_cpu=False, freeze_db=False)
        stats.optimize_db()
        assert stats._full_repetativ_syntagma == False
        assert stats.recompute_syntagma_repetativity_scope(True)
        assert stats._full_repetativ_syntagma == True
        assert stats.recompute_syntagma_repetativity_scope(False)
        assert stats._full_repetativ_syntagma == False

    @attr(status='stable')
    def test_reconstruct_syntagma_630(self):
        self.prj_folder()
        self.test_dbs()
        stats = Stats(mode=self.mode, use_cash=True)
        stats.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_stats_de))
        indexes = {'repl': {'pos': 10, 'index_of_repl': 9, 'id': 0, 'polarity': 11, 'in_redu': 12, 'context_infoL2': 20, 'context_infoL3': 18, 'context_infoL1': 22, 'context_infoL4': 16, 'context_infoL5': 14, 'contextR2': 25, 'contextR3': 27, 'contextR1': 23, 'contextR4': 29, 'contextR5': 31, 'rle_word': 6, 'index_in_redufree': 4, 'contextL1': 21, 'contextL4': 15, 'contextL5': 13, 'redufree_len': 2, 'repl_length': 8, 'contextL2': 19, 'contextL3': 17, 'context_infoR1': 24, 'context_infoR2': 26, 'context_infoR3': 28, 'context_infoR4': 30, 'context_infoR5': 32, 'index_in_corpus': 3, 'normalized_word': 5, 'doc_id': 1, 'repl_letter': 7}, 'baseline': {'occur_repl_uniq': 3, 'syntagma': 0, 'hight_scope_uniq_occur_redu': 8, 'occur_redu_exhausted': 6, 'occur_redu_uniq': 5, 'hight_scope_uniq_occur_repl': 7, 'occur_syntagma_all': 1, 'scope': 2, 'occur_repl_exhausted': 4}, 'redu': {'orig_words': 6, 'pos': 8, 'id': 0, 'polarity': 9, 'redu_length': 7, 'context_infoL2': 17, 'context_infoL3': 15, 'context_infoL1': 19, 'context_infoL4': 13, 'context_infoL5': 11, 'contextR2': 22, 'contextR3': 24, 'contextR1': 20, 'contextR4': 26, 'contextR5': 28, 'index_in_redufree': 4, 'contextL4': 12, 'contextL5': 10, 'redufree_len': 2, 'contextL1': 18, 'contextL2': 16, 'contextL3': 14, 'context_infoR1': 21, 'context_infoR2': 23, 'context_infoR3': 25, 'context_infoR4': 27, 'context_infoR5': 29, 'index_in_corpus': 3, 'normalized_word': 5, 'doc_id': 1}}
        rep_type = 'repl'
        reps = [
         (
          1, 8888, '[4, 9]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze', 'i', 4, 2, 'NN', '["neutral", 0.0]', '[0, 0]', None, None, None, None, None, None, None, None, None, None, 'kleine', '["NE", {"kle^5ine": 1, "klein^3e": 1}]', 'überaschung', '["NN"]', '.', '["symbol"]', 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]'),
         (
          15, 10000, '[8]', '[0, 1]', '[0, 1]', 'klitze', 'klitze^4', 'e', 4, 5, 'VAPPER', '["neutral", 0.0]', None, None, None, None, None, None, None, None, None, 'eine', '["ART"]', 'kleine', '["ADJA"]', 'überaschung', '["NN"]', '@schönesleben', '["mention"]', '#machwasdaraus', '["hashtag"]', '#bewegedeinarsch', '["hashtag"]'),
         (
          17, 11111, '[5, 12]', '[0, 1]', '[0, 1]', 'klitze', 'klitze^4', 'e', 4, 5, 'VAPPER', '["neutral", 0.0]', None, None, None, None, None, None, None, None, None, 'eine', '["ART"]', 'kleine', '["ADJA"]', 'sache', '["NN"]', '.', '["symbol"]', 'die', '["PDS"]', 'aber', '["ADV"]'),
         (
          2, 8888, '[4, 9]', '[0, 2]', '[0, 1]', 'kleine', 'kle^5ine', 'e', 5, 2, 'NE', '["neutral", 0.0]', '[0, 2]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze": 1}]', 'überaschung', '["NN"]', '.', '["symbol"]', 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]', 'sie', '["PPER"]'),
         (
          3, 8888, '[4, 9]', '[0, 3]', '[0, 1]', 'kleine', 'klein^3e', 'n', 3, 4, 'NE', '["neutral", 0.0]', '[0, 2]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze": 1}]', 'überaschung', '["NN"]', '.', '["symbol"]', 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]', 'sie', '["PPER"]')]
        inp_syntagma_splitted = [
         'klitze', 'kleine']
        scope = 2
        minimum_columns = False
        order_output_by_syntagma_order = False
        right_output = {8888: {0: {0: [
                        'klitze', (1,)], 
                      1: [
                        'kleine', (2, 3)]}}, 
           10000: {0: {1: [
                         'klitze', (15,)]}}, 
           11111: {0: {1: ['klitze', (17,)]}}}
        right_length = {8888: [4, 9], 10000: [8], 11111: [5, 12]}
        output_raw, length = stats._reconstruct_syntagma(rep_type, reps, order_output_by_syntagma_order, indexes)
        preparated_output = {d:{s:{t:ids for t, ids in s_data.iteritems()} for s, s_data in doc_data.iteritems()} for d, doc_data in output_raw.iteritems()}
        preparated_output.should.be.equal(right_output)
        length.should.be.equal(right_length)
        rep_type = 'redu'
        reps = [
         (
          1, 8888, '[4, 9]', '[0, 0]', '[0, 0]', 'klitze', '{"klitze": 1, "kli^4tze": 1}', 2, 'NN', '["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, 'kleine', '["NE", {"kle^5ine": 1, "klein^3e": 1}]', 'überaschung', '["NN"]', '.', '["symbol"]', 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]'),
         (
          4, 12222, '[11]', '[0, 1]', '[0, 1]', 'klitze', '{"klitze": 4}', 4, 'NN', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'eine', '["ART"]', 'kleine', '["ADJA"]', 'überaschung', '["NN"]', ',', '["symbol"]', 'die', '["PRELS"]', 'ich', '["PPER"]'),
         (
          2, 8888, '[4, 9]', '[0, 2]', '[0, 1]', 'kleine', '{"kle^5ine": 1, "klein^3e": 1}', 2, 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze": 1}]', 'überaschung', '["NN"]', '.', '["symbol"]', 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]', 'sie', '["PPER"]')]
        inp_syntagma_splitted = [
         'klitze', 'kleine']
        scope = 2
        minimum_columns = False
        order_output_by_syntagma_order = False
        right_output = {8888: {0: {0: [
                        'klitze', (1,)], 
                      1: [
                        'kleine', (2,)]}}, 
           12222: {0: {1: [
                         'klitze', (4,)]}}}
        right_length = {8888: [4, 9], 12222: [11]}
        output_raw, length = stats._reconstruct_syntagma(rep_type, reps, order_output_by_syntagma_order, indexes)
        preparated_output = {d:{s:{t:ids for t, ids in s_data.iteritems()} for s, s_data in doc_data.iteritems()} for d, doc_data in output_raw.iteritems()}
        preparated_output.should.be.equal(right_output)
        length.should.be.equal(right_length)
        rep_type = 'repl'
        reps = [
         (
          'klitze',
          [
           (
            1, 8888, '[4, 9]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze', 'i', 4, 2, 'NN', '["neutral", 0.0]', '[0, 0]', None, None, None, None, None, None, None, None, None, None, 'kleine', '["NE", {"kle^5ine": 1, "klein^3e": 1}]', 'überaschung', '["NN"]', '.', '["symbol"]', 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]'),
           (
            15, 10000, '[8]', '[0, 1]', '[0, 1]', 'klitze', 'klitze^4', 'e', 4, 5, 'VAPPER', '["neutral", 0.0]', None, None, None, None, None, None, None, None, None, 'eine', '["ART"]', 'kleine', '["ADJA"]', 'überaschung', '["NN"]', '@schönesleben', '["mention"]', '#machwasdaraus', '["hashtag"]', '#bewegedeinarsch', '["hashtag"]'),
           (
            17, 11111, '[5, 12]', '[0, 1]', '[0, 1]', 'klitze', 'klitze^4', 'e', 4, 5, 'VAPPER', '["neutral", 0.0]', None, None, None, None, None, None, None, None, None, 'eine', '["ART"]', 'kleine', '["ADJA"]', 'sache', '["NN"]', '.', '["symbol"]', 'die', '["PDS"]', 'aber', '["ADV"]')]),
         (
          'kleine',
          [
           (
            2, 8888, '[4, 9]', '[0, 2]', '[0, 1]', 'kleine', 'kle^5ine', 'e', 5, 2, 'NE', '["neutral", 0.0]', '[0, 2]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze": 1}]', 'überaschung', '["NN"]', '.', '["symbol"]', 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]', 'sie', '["PPER"]'),
           (
            3, 8888, '[4, 9]', '[0, 3]', '[0, 1]', 'kleine', 'klein^3e', 'n', 3, 4, 'NE', '["neutral", 0.0]', '[0, 2]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze": 1}]', 'überaschung', '["NN"]', '.', '["symbol"]', 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]', 'sie', '["PPER"]')])]
        inp_syntagma_splitted = [
         'klitze', 'kleine']
        scope = 2
        minimum_columns = False
        order_output_by_syntagma_order = True
        right_output = {8888: {0: {0: [
                        'klitze', (1,)], 
                      1: [
                        'kleine', (2, 3)]}}, 
           10000: {0: {1: [
                         'klitze', (15,)]}}, 
           11111: {0: {1: [
                         'klitze', (17,)]}}}
        right_length = {8888: [4, 9], 10000: [8], 11111: [5, 12]}
        output_raw, length = stats._reconstruct_syntagma(rep_type, reps, order_output_by_syntagma_order, indexes)
        preparated_output = {d:{s:{t:ids for t, ids in s_data.iteritems()} for s, s_data in doc_data.iteritems()} for d, doc_data in output_raw.iteritems()}
        preparated_output.should.be.equal(right_output)
        length.should.be.equal(right_length)
        rep_type = 'repl'
        reps = (
         (
          'number',
          (
           (
            20, 11111, '[5, 12]', '[1, 6]', '[1, 6]', '1', '1^5', '1', 5, 0, 'number', '["neutral", 0.0]', None, 'aber', '["ADV"]', 'trotzdem', '["PAV"]', 'wichtig', '["ADJA"]', 'ist', '["NN"]', '!', '["symbol"]', 2, '["number"]', 3, '["number"]', 4, '["number"]', 5, '["number"]', 6, '["number"]'),
           (
            21, 11111, '[5, 12]', '[1, 7]', '[1, 7]', '2', '2^4', '2', 4, 0, 'number', '["neutral", 0.0]', None, 'trotzdem', '["PAV"]', 'wichtig', '["ADJA"]', 'ist', '["NN"]', '!', '["symbol"]', 1, '["number"]', 3, '["number"]', 4, '["number"]', 5, '["number"]', 6, '["number"]', None, None),
           (
            22, 11111, '[5, 12]', '[1, 8]', '[1, 8]', '3', '3^5', '3', 5, 0, 'number', '["neutral", 0.0]', None, 'wichtig', '["ADJA"]', 'ist', '["NN"]', '!', '["symbol"]', 1, '["number"]', 2, '["number"]', 4, '["number"]', 5, '["number"]', 6, '["number"]', None, None, None, None),
           (
            23, 11111, '[5, 12]', '[1, 9]', '[1, 9]', '4', '4^4', '4', 4, 0, 'number', '["neutral", 0.0]', None, 'ist', '["NN"]', '!', '["symbol"]', 1, '["number"]', 2, '["number"]', 3, '["number"]', 5, '["number"]', 6, '["number"]', None, None, None, None, None, None))),
         (
          'number',
          (
           (
            21, 11111, '[5, 12]', '[1, 7]', '[1, 7]', '2', '2^4', '2', 4, 0, 'number', '["neutral", 0.0]', None, 'trotzdem', '["PAV"]', 'wichtig', '["ADJA"]', 'ist', '["NN"]', '!', '["symbol"]', 1, '["number"]', 3, '["number"]', 4, '["number"]', 5, '["number"]', 6, '["number"]', None, None),
           (
            22, 11111, '[5, 12]', '[1, 8]', '[1, 8]', '3', '3^5', '3', 5, 0, 'number', '["neutral", 0.0]', None, 'wichtig', '["ADJA"]', 'ist', '["NN"]', '!', '["symbol"]', 1, '["number"]', 2, '["number"]', 4, '["number"]', 5, '["number"]', 6, '["number"]', None, None, None, None),
           (
            23, 11111, '[5, 12]', '[1, 9]', '[1, 9]', '4', '4^4', '4', 4, 0, 'number', '["neutral", 0.0]', None, 'ist', '["NN"]', '!', '["symbol"]', 1, '["number"]', 2, '["number"]', 3, '["number"]', 5, '["number"]', 6, '["number"]', None, None, None, None, None, None),
           (
            24, 11111, '[5, 12]', '[1, 10]', '[1, 10]', '5', '5^5', '5', 5, 0, 'number', '["neutral", 0.0]', None, '!', '["symbol"]', 1, '["number"]', 2, '["number"]', 3, '["number"]', 4, '["number"]', 6, '["number"]', None, None, None, None, None, None, None, None))),
         (
          'number',
          (
           (
            22, 11111, '[5, 12]', '[1, 8]', '[1, 8]', '3', '3^5', '3', 5, 0, 'number', '["neutral", 0.0]', None, 'wichtig', '["ADJA"]', 'ist', '["NN"]', '!', '["symbol"]', 1, '["number"]', 2, '["number"]', 4, '["number"]', 5, '["number"]', 6, '["number"]', None, None, None, None),
           (
            23, 11111, '[5, 12]', '[1, 9]', '[1, 9]', '4', '4^4', '4', 4, 0, 'number', '["neutral", 0.0]', None, 'ist', '["NN"]', '!', '["symbol"]', 1, '["number"]', 2, '["number"]', 3, '["number"]', 5, '["number"]', 6, '["number"]', None, None, None, None, None, None),
           (
            24, 11111, '[5, 12]', '[1, 10]', '[1, 10]', '5', '5^5', '5', 5, 0, 'number', '["neutral", 0.0]', None, '!', '["symbol"]', 1, '["number"]', 2, '["number"]', 3, '["number"]', 4, '["number"]', 6, '["number"]', None, None, None, None, None, None, None, None))))
        scope = 3
        minimum_columns = False
        order_output_by_syntagma_order = True
        right_output = {11111: {1: {8: [
                         'number', (22, 22, 22)], 
                       9: [
                         'number', (23, 23, 23)], 
                       10: [
                          'number', (24, 24)], 
                       6: [
                         'number', (20,)], 
                       7: [
                         'number', (21, 21)]}}}
        right_length = {11111: [5, 12]}
        output_raw, length = stats._reconstruct_syntagma(rep_type, reps, order_output_by_syntagma_order, indexes, syntagma_type='pos')
        preparated_output = {d:{s:{t:ids for t, ids in s_data.iteritems()} for s, s_data in doc_data.iteritems()} for d, doc_data in output_raw.iteritems()}
        preparated_output.should.be.equal(right_output)
        length.should.be.equal(right_length)
        return

    @attr(status='stable')
    def test_exctract_full_syntagmas_631(self):
        stats = Stats(mode=self.mode)
        inp_syntagma_splitted = ('klitze', )
        redu_free_elem_length = {10000: [5, 1, 1], 11111: [2, 5, 6]}
        scope = 1
        reconstructed_syntagmas = {11111: {0: {1: [
                         'klitze', (18, )]}, 
                   1: {1: [
                         'klitze', (20, )], 
                       2: [
                         'kleine', (22, )]}, 
                   2: {0: [
                         'klitze', (29, )], 
                       2: [
                         'klitze', (26, )], 
                       4: [
                         'klitze', (27, )]}}}
        right_full_syntagmas = (
         ((0, 1), ), ((1, 1), ), ((2, 0), ), ((2, 2), ), ((2, 4), ))
        right_allow_ids = (18, 27, 20, 26, 29)
        full_syntagmas, allow_ids = stats._exctract_full_syntagmas(reconstructed_syntagmas, scope, redu_free_elem_length, inp_syntagma_splitted)
        full_syntagmas.should.be.equal(right_full_syntagmas)
        set(allow_ids).should.be.equal(set(right_allow_ids))
        assert False not in set([ True if len(syn) >= scope else False for syn in full_syntagmas ])
        inp_syntagma_splitted = ('klitze', 'kleine')
        redu_free_elem_length = {10000: [5, 1, 1], 11111: [2, 5, 4]}
        scope = 2
        reconstructed_syntagmas = {11111: {0: {1: [
                         'klitze', (18, )], 
                       2: [
                         'kleine', (19, )]}}}
        right_full_syntagmas = (
         (
          (0, 1), (0, 2)),)
        right_allow_ids = (18, 19)
        full_syntagmas, allow_ids = stats._exctract_full_syntagmas(reconstructed_syntagmas, scope, redu_free_elem_length, inp_syntagma_splitted)
        full_syntagmas.should.be.equal(right_full_syntagmas)
        set(allow_ids).should.be.equal(set(right_allow_ids))
        assert False not in set([ True if len(syn) == scope else False for syn in full_syntagmas ])
        inp_syntagma_splitted = ('klitze', 'kleine')
        redu_free_elem_length = {10000: [5, 1, 1], 11111: [2, 5, 4]}
        scope = 2
        reconstructed_syntagmas = {11111: {0: {1: [
                         'klitze', (18, )], 
                       2: [
                         'kleine', (19, )]}, 
                   1: {1: [
                         'klitze', (20, )], 
                       2: [
                         'kleine', (22, )]}}}
        right_full_syntagmas = (
         (
          (0, 1), (0, 2)), ((1, 1), (1, 2)))
        right_allow_ids = (18, 19, 20, 22)
        full_syntagmas, allow_ids = stats._exctract_full_syntagmas(reconstructed_syntagmas, scope, redu_free_elem_length, inp_syntagma_splitted)
        full_syntagmas.should.be.equal(right_full_syntagmas)
        set(allow_ids).should.be.equal(set(right_allow_ids))
        assert False not in set([ True if len(syn) == scope else False for syn in full_syntagmas ])
        inp_syntagma_splitted = ('klitze', 'kleine')
        redu_free_elem_length = {11111: [2, 5, 4]}
        scope = 2
        reconstructed_syntagmas = {11111: {0: {1: [
                         'klitze', (18, )], 
                       2: [
                         'kleine', (19, )]}, 
                   1: {1: [
                         'klitze', (20, )], 
                       4: [
                         'klitze', (22, )]}, 
                   2: {0: [
                         'kleine', (24, 554)], 
                       2: [
                         'kleine', (29, 56)]}}}
        right_full_syntagmas = (
         (
          (0, 1), (0, 2)), ((1, 4), (2, 0)))
        right_allow_ids = (18, 19, 22, 24, 554)
        full_syntagmas, allow_ids = stats._exctract_full_syntagmas(reconstructed_syntagmas, scope, redu_free_elem_length, inp_syntagma_splitted)
        full_syntagmas.should.be.equal(right_full_syntagmas)
        set(allow_ids).should.be.equal(set(right_allow_ids))
        assert False not in set([ True if len(syn) == scope else False for syn in full_syntagmas ])
        inp_syntagma_splitted = [
         'klitze', 'kleine']
        redu_free_elem_length = {8888: [4, 9], 10000: [8], 11111: [5, 12]}
        scope = 2
        reconstructed_syntagmas = {8888: {0: {0: [
                        'klitze', (1, )], 
                      1: [
                        'kleine', (2, 3)]}}, 
           10000: {0: {1: [
                         'klitze', (15, )]}}, 
           11111: {0: {1: [
                         'klitze', (17, )]}}}
        right_full_syntagmas = (
         (
          (0, 0), (0, 1)),)
        right_allow_ids = (1, 2, 3)
        full_syntagmas, allow_ids = stats._exctract_full_syntagmas(reconstructed_syntagmas, scope, redu_free_elem_length, inp_syntagma_splitted)
        full_syntagmas.should.be.equal(right_full_syntagmas)
        set(allow_ids).should.be.equal(set(right_allow_ids))
        assert False not in set([ True if len(syn) == scope else False for syn in full_syntagmas ])
        inp_syntagma_splitted = [
         'klitze', 'kleine']
        redu_free_elem_length = {8888: [4, 9], 12222: [11]}
        scope = 2
        reconstructed_syntagmas = {8888: {0: {0: [
                        'klitze', (1, )], 
                      1: [
                        'kleine', (2, )]}}, 
           12222: {0: {1: [
                         'klitze', (4, )]}}}
        right_full_syntagmas = (
         (
          (0, 0), (0, 1)),)
        right_allow_ids = (1, 2)
        full_syntagmas, allow_ids = stats._exctract_full_syntagmas(reconstructed_syntagmas, scope, redu_free_elem_length, inp_syntagma_splitted)
        full_syntagmas.should.be.equal(right_full_syntagmas)
        set(allow_ids).should.be.equal(set(right_allow_ids))
        assert False not in set([ True if len(syn) == scope else False for syn in full_syntagmas ])
        inp_syntagma_splitted = [
         'klitze', 'kleine']
        redu_free_elem_length = {8888: [4, 9], 12222: [11]}
        scope = 2
        reconstructed_syntagmas = {8888: {0: {0: [
                        'klitze', (1, )], 
                      1: [
                        'kleine', (2, )], 
                      2: [
                        'klitze', (2, )], 
                      3: [
                        'kleine', (3, )]}}, 
           12222: {0: {1: [
                         'klitze', (4, )]}}}
        right_full_syntagmas = (
         (
          (0, 0), (0, 1)), ((0, 2), (0, 3)))
        right_allow_ids = (1, 2, 3)
        full_syntagmas, allow_ids = stats._exctract_full_syntagmas(reconstructed_syntagmas, scope, redu_free_elem_length, inp_syntagma_splitted)
        full_syntagmas.should.be.equal(right_full_syntagmas)
        set(allow_ids).should.be.equal(set(right_allow_ids))
        assert False not in set([ True if len(syn) == scope else False for syn in full_syntagmas ])
        inp_syntagma_splitted = ('klitze', 'kleine', 'iii')
        redu_free_elem_length = {8888: [2, 3], 10000: [3, 4], 11111: [2, 5, 4]}
        scope = 3
        reconstructed_syntagmas = {8888: {0: {0: [
                        'klitze', (1, )], 
                      1: [
                        'kleine', (2, 3)]}, 
                  1: {0: [
                        'iii', (10, )]}}, 
           10000: {0: {1: [
                         'kleine', (15, )]}}, 
           11111: {0: {1: [
                         'kleine', (17, )]}}}
        right_full_syntagmas = (
         (
          (0, 0), (0, 1), (1, 0)),)
        right_allow_ids = (1, 2, 3, 10)
        full_syntagmas, allow_ids = stats._exctract_full_syntagmas(reconstructed_syntagmas, scope, redu_free_elem_length, inp_syntagma_splitted)
        full_syntagmas.should.be.equal(right_full_syntagmas)
        set(allow_ids).should.be.equal(set(right_allow_ids))
        assert False not in set([ True if len(syn) == scope else False for syn in full_syntagmas ])
        inp_syntagma_splitted = ('klitze', 'kleine', 'iii')
        redu_free_elem_length = {8888: [4, 5], 10000: [5, 1, 1], 11111: [2, 5, 4]}
        scope = 3
        reconstructed_syntagmas = {8888: {0: {0: [
                        'klitze', (1, )], 
                      1: [
                        'kleine', (2, 3)], 
                      2: [
                        'iii', (4, 5)]}, 
                  1: {1: [
                        'klitze', (10, )], 
                      2: [
                        'kleine', (11, )], 
                      3: [
                        'i', (12, )]}}}
        right_full_syntagmas = (
         (
          (0, 0), (0, 1), (0, 2)), ((1, 1), (1, 2), (1, 3)))
        right_allow_ids = (1, 2, 3, 4, 5, 10, 11, 12)
        full_syntagmas, allow_ids = stats._exctract_full_syntagmas(reconstructed_syntagmas, scope, redu_free_elem_length, inp_syntagma_splitted)
        full_syntagmas.should.be.equal(right_full_syntagmas)
        set(allow_ids).should.be.equal(set(right_allow_ids))
        assert False not in set([ True if len(syn) == scope else False for syn in full_syntagmas ])
        inp_syntagma_splitted = ('klitze', 'kleine', 'iii')
        redu_free_elem_length = {10000: [5, 1, 1], 11111: [2, 5, 4]}
        scope = 3
        reconstructed_syntagmas = {10000: {0: {4: [
                         'klitze', (15, )]}, 
                   1: {0: [
                         'kleine', (16, )]}, 
                   2: {0: [
                         'iii', (17, )]}}}
        right_full_syntagmas = (
         (
          (0, 4), (1, 0), (2, 0)),)
        right_allow_ids = (15, 16, 17)
        full_syntagmas, allow_ids = stats._exctract_full_syntagmas(reconstructed_syntagmas, scope, redu_free_elem_length, inp_syntagma_splitted)
        full_syntagmas.should.be.equal(right_full_syntagmas)
        set(allow_ids).should.be.equal(set(right_allow_ids))
        assert False not in set([ True if len(syn) == scope else False for syn in full_syntagmas ])
        inp_syntagma_splitted = ('klitze', 'kleine', 'iii', ',', 'oder', 'wie')
        redu_free_elem_length = {10000: [5, 2, 2, 1], 11111: [2, 5, 4]}
        scope = 6
        reconstructed_syntagmas = {10000: {0: {4: [
                         'klitze', (15, )]}, 
                   1: {0: [
                         'kleine', (16, )], 
                       1: [
                         'iii', (19, )]}, 
                   2: {0: [
                         ',', (17, )], 
                       1: [
                         'oder', (34, )]}, 
                   3: {0: [
                         'wie', (17, )]}}}
        right_full_syntagmas = (
         (
          (0, 4), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0)),)
        right_allow_ids = (15, 16, 19, 17, 34, 17)
        full_syntagmas, allow_ids = stats._exctract_full_syntagmas(reconstructed_syntagmas, scope, redu_free_elem_length, inp_syntagma_splitted)
        full_syntagmas.should.be.equal(right_full_syntagmas)
        set(allow_ids).should.be.equal(set(right_allow_ids))
        assert False not in set([ True if len(syn) == scope else False for syn in full_syntagmas ])
        inp_syntagma_splitted = ('klitze', 'kleine', 'iii', ',', 'oder', 'wie')
        redu_free_elem_length = {10000: [10, 3, 4, 5], 11111: [7, 4, 2, 1]}
        scope = 6
        reconstructed_syntagmas = {10000: {0: {0: [
                         'klitze', (15, )], 
                       1: [
                         'kleine', (16, )], 
                       2: [
                         'iii', (17, )], 
                       3: [
                         ',', (18, )], 
                       4: [
                         'oder', (19, )], 
                       5: [
                         'wie', (20, )]}, 
                   1: {0: [
                         'klitze', (164, )], 
                       1: [
                         'kleine', (193, )]}, 
                   2: {0: [
                         'klitze', (172, )], 
                       1: [
                         'kleine', (343, )]}}, 
           11111: {0: {4: [
                         'klitze', (23, )], 
                       5: [
                         'kleine', (25, )], 
                       6: [
                         'iii', (64, )]}, 
                   1: {0: [
                         ',', (152, )], 
                       1: [
                         'oder', (114, )], 
                       2: [
                         'wie', (1, )]}, 
                   2: {0: [
                         'klitze', (147, )], 
                       1: [
                         'kleine', (344, )]}, 
                   3: {0: [
                         'iii', (178, )]}}}
        right_full_syntagmas = (
         (
          (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5)), ((0, 4), (0, 5), (0, 6), (1, 0), (1, 1), (1, 2)))
        right_allow_ids = (15, 16, 17, 18, 19, 20, 23, 25, 64, 152, 114, 1)
        full_syntagmas, allow_ids = stats._exctract_full_syntagmas(reconstructed_syntagmas, scope, redu_free_elem_length, inp_syntagma_splitted)
        full_syntagmas.should.be.equal(right_full_syntagmas)
        set(allow_ids).should.be.equal(set(right_allow_ids))
        assert False not in set([ True if len(syn) == scope else False for syn in full_syntagmas ])
        inp_syntagma_splitted = ('klitze', 'kleine', 'iii', ',', 'oder', 'wie')
        redu_free_elem_length = {10000: [10, 10, 10, 10], 11111: [7, 4, 2, 1]}
        scope = 6
        reconstructed_syntagmas = {10000: {0: {2: [
                         'klitze', (15, )], 
                       3: [
                         'kleine', (16, )], 
                       4: [
                         'iii', (17, )], 
                       6: [
                         ',', (18, )], 
                       7: [
                         'oder', (19, )], 
                       8: [
                         'wie', (20, )]}, 
                   2: {4: [
                         'klitze', (152, )], 
                       5: [
                         'kleine', (163, )], 
                       6: [
                         'iii', (174, )], 
                       7: [
                         ',', (185, )], 
                       8: [
                         'oder', (196, )], 
                       9: [
                         'wie', (207, )]}, 
                   3: {1: [
                         'klitze', (150, )], 
                       2: [
                         'kleine', (160, )], 
                       3: [
                         'iii', (170, )], 
                       4: [
                         ',', (180, )], 
                       5: [
                         'oder', (190, )], 
                       6: [
                         'wie', (200, )]}}}
        right_full_syntagmas = (
         (
          (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9)), ((3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6)))
        right_allow_ids = (160, 163, 196, 200, 170, 174, 207, 180, 150, 152, 185, 190)
        full_syntagmas, allow_ids = stats._exctract_full_syntagmas(reconstructed_syntagmas, scope, redu_free_elem_length, inp_syntagma_splitted)
        full_syntagmas.should.be.equal(right_full_syntagmas)
        set(allow_ids).should.be.equal(set(right_allow_ids))
        assert False not in set([ True if len(syn) == scope else False for syn in full_syntagmas ])
        syntagma_type = 'pos'
        inp_syntagma_splitted = ['number', 'number', 'number']
        redu_free_elem_length = {11111: [5, 6, 14]}
        scope = 3
        reconstructed_syntagmas = {11111: {2: {8: [
                         'number', (33, )], 
                       9: [
                         'number', (34, 34)], 
                       10: [
                          'number', (35, 35, 35)], 
                       11: [
                          'number', (36, 36, 36)], 
                       12: [
                          'number', (37, 37)]}}}
        right_full_syntagmas = (
         (
          (2, 8), (2, 9), (2, 10)),)
        right_allow_ids = (33, 34, 35)
        full_syntagmas, allow_ids = stats._exctract_full_syntagmas(reconstructed_syntagmas, scope, redu_free_elem_length, inp_syntagma_splitted, syntagma_type=syntagma_type)
        full_syntagmas.should.be.equal(right_full_syntagmas)
        set(allow_ids).should.be.equal(set(right_allow_ids))
        assert False not in set([ True if len(syn) >= scope else False for syn in full_syntagmas ])
        syntagma_type = 'pos'
        inp_syntagma_splitted = ('NN', 'NP', 'NN')
        redu_free_elem_length = {11111: [5, 12]}
        scope = 3
        reconstructed_syntagmas = {11111: {1: {6: [
                         'NN', (22, 22, 22)], 
                       7: [
                         'NP', (23, 23, 23)], 
                       8: [
                         'NN', (24, 24)], 
                       9: [
                         'NN', (221, 221, 221)], 
                       10: [
                          'NP', (232, 233, 236)], 
                       11: [
                          'NN', (240, 248)]}}}
        right_full_syntagmas = (
         (
          (1, 6), (1, 7), (1, 8)), ((1, 9), (1, 10), (1, 11)))
        right_allow_ids = (232, 233, 236, 240, 24, 22, 23, 248, 221)
        full_syntagmas, allow_ids = stats._exctract_full_syntagmas(reconstructed_syntagmas, scope, redu_free_elem_length, inp_syntagma_splitted, syntagma_type=syntagma_type)
        full_syntagmas.should.be.equal(right_full_syntagmas)
        set(allow_ids).should.be.equal(set(right_allow_ids))
        assert False not in set([ True if len(syn) >= scope else False for syn in full_syntagmas ])
        syntagma_type = 'pos'
        inp_syntagma_splitted = ('NN', 'NP', 'NN', 'NP')
        redu_free_elem_length = {11111: [5, 12]}
        scope = 4
        reconstructed_syntagmas = {11111: {1: {6: [
                         'NN', (22, 22, 22)], 
                       7: [
                         'NP', (23, 23, 23)], 
                       8: [
                         'NN', (24, 24)], 
                       9: [
                         'NP', (221, 221, 221)], 
                       10: [
                          'NN', (232, 233, 236)], 
                       11: [
                          'NP', (240, 248)]}}}
        right_full_syntagmas = (
         (
          (1, 6), (1, 7), (1, 8), (1, 9)),)
        right_allow_ids = (24, 221, 22, 23)
        full_syntagmas, allow_ids = stats._exctract_full_syntagmas(reconstructed_syntagmas, scope, redu_free_elem_length, inp_syntagma_splitted, syntagma_type=syntagma_type)
        full_syntagmas.should.be.equal(right_full_syntagmas)
        set(allow_ids).should.be.equal(set(right_allow_ids))
        assert False not in set([ True if len(syn) >= scope else False for syn in full_syntagmas ])
        syntagma_type = 'lexem'
        inp_syntagma_splitted = ('klitze', 'kleine', 'klitze')
        redu_free_elem_length = {11111: [5, 15]}
        scope = 3
        reconstructed_syntagmas = {11111: {1: {6: [
                         'klitze', (22, 22, 22)], 
                       7: [
                         'kleine', (23, 23, 23)], 
                       8: [
                         'klitze', (24, 24)], 
                       9: [
                         'klitze', (22, 22, 22)], 
                       10: [
                          'kleine', (23, 23, 23)], 
                       11: [
                          'klitze', (24, 24)]}}}
        right_full_syntagmas = (
         (
          (1, 6), (1, 7), (1, 8)), ((1, 9), (1, 10), (1, 11)))
        right_allow_ids = (24, 22, 23)
        full_syntagmas, allow_ids = stats._exctract_full_syntagmas(reconstructed_syntagmas, scope, redu_free_elem_length, inp_syntagma_splitted, syntagma_type=syntagma_type)
        full_syntagmas.should.be.equal(right_full_syntagmas)
        set(allow_ids).should.be.equal(set(right_allow_ids))
        assert False not in set([ True if len(syn) >= scope else False for syn in full_syntagmas ])
        syntagma_type = 'lexem'
        inp_syntagma_splitted = ('klitze', 'kleine', 'klitze', 'kleine')
        redu_free_elem_length = {11111: [5, 15]}
        scope = 4
        reconstructed_syntagmas = {11111: {1: {6: [
                         'klitze', (22, 22, 22)], 
                       7: [
                         'kleine', (23, 23, 23)], 
                       8: [
                         'klitze', (22, 22, 22)], 
                       9: [
                         'kleine', (23, 23, 23)], 
                       10: [
                          'klitze', (22, 22, 22)], 
                       11: [
                          'kleine', (23, 23, 23)]}}}
        right_full_syntagmas = (
         (
          (1, 6), (1, 7), (1, 8), (1, 9)),)
        right_allow_ids = (22, 23)
        full_syntagmas, allow_ids = stats._exctract_full_syntagmas(reconstructed_syntagmas, scope, redu_free_elem_length, inp_syntagma_splitted, syntagma_type=syntagma_type)
        full_syntagmas.should.be.equal(right_full_syntagmas)
        set(allow_ids).should.be.equal(set(right_allow_ids))
        assert False not in set([ True if len(syn) >= scope else False for syn in full_syntagmas ])
        syntagma_type = 'lexem'
        inp_syntagma_splitted = ('klitze', 'kleine')
        redu_free_elem_length = {11111: [5, 15]}
        scope = 2
        reconstructed_syntagmas = {11111: {1: {6: [
                         'klitze', (22, 22, 22)], 
                       7: [
                         'kleine', (23, 23, 23)], 
                       8: [
                         'klitze', (22, 22, 22)], 
                       9: [
                         'kleine', (23, 23, 23)], 
                       10: [
                          'klitze', (22, 22, 22)], 
                       11: [
                          'kleine', (23, 23, 23)]}}}
        right_full_syntagmas = (
         (
          (1, 6), (1, 7)), ((1, 8), (1, 9)), ((1, 10), (1, 11)))
        right_allow_ids = (22, 23)
        full_syntagmas, allow_ids = stats._exctract_full_syntagmas(reconstructed_syntagmas, scope, redu_free_elem_length, inp_syntagma_splitted, syntagma_type=syntagma_type)
        full_syntagmas.should.be.equal(right_full_syntagmas)
        set(allow_ids).should.be.equal(set(right_allow_ids))
        assert False not in set([ True if len(syn) >= scope else False for syn in full_syntagmas ])

    @attr(status='stable')
    def test_filter_full_rep_syn_632(self):
        stats = Stats(mode=self.mode)
        rep_type = 'repl'
        _rep = (
         (
          'klitze',
          (
           (1, 8888, '[4, 9]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze', 'i', 4, 2, 'NN', '["neutral", 0.0]',
 '[0, 0]', None, None, None, None, None, None, None, None, None, None, 'kleine',
 '["NE", {"kle^5ine": 1, "klein^3e": 1}]', 'überaschung', '["NN"]', '.', '["symbol"]',
 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]'),
           (15, 10000, '[8]', '[0, 1]', '[0, 1]', 'klitze', 'klitze^4', 'e', 4, 5, 'VAPPER', '["neutral", 0.0]',
 None, None, None, None, None, None, None, None, None, 'eine', '["ART"]', 'kleine',
 '["ADJA"]', 'überaschung', '["NN"]', '@schönesleben', '["mention"]', '#machwasdaraus',
 '["hashtag"]', '#bewegedeinarsch', '["hashtag"]'),
           (17, 11111, '[5, 12]', '[0, 1]', '[0, 1]', 'klitze', 'klitze^4', 'e', 4, 5, 'VAPPER',
 '["neutral", 0.0]', None, None, None, None, None, None, None, None, None, 'eine',
 '["ART"]', 'kleine', '["ADJA"]', 'sache', '["NN"]', '.', '["symbol"]', 'die', '["PDS"]',
 'aber', '["ADV"]'))),
         (
          'kleine',
          (
           (2, 8888, '[4, 9]', '[0, 2]', '[0, 1]', 'kleine', 'kle^5ine', 'e', 5, 2, 'NE', '["neutral", 0.0]',
 '[0, 2]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze": 1}]',
 'überaschung', '["NN"]', '.', '["symbol"]', 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]',
 'sie', '["PPER"]'),
           (3, 8888, '[4, 9]', '[0, 3]', '[0, 1]', 'kleine', 'klein^3e', 'n', 3, 4, 'NE', '["neutral", 0.0]',
 '[0, 2]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze": 1}]',
 'überaschung', '["NN"]', '.', '["symbol"]', 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]',
 'sie', '["PPER"]'))))
        allowed_ids = set((1, 2, 3))
        order_output_by_syntagma_order = True
        right_filtered_reps = (
         (
          'klitze',
          ((1, 8888, '[4, 9]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze', 'i', 4, 2, 'NN', '["neutral", 0.0]', '[0, 0]', None, None, None, None, None, None, None, None, None, None, 'kleine', '["NE", {"kle^5ine": 1, "klein^3e": 1}]', 'überaschung', '["NN"]', '.', '["symbol"]', 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]'), )),
         (
          'kleine',
          (
           (2, 8888, '[4, 9]', '[0, 2]', '[0, 1]', 'kleine', 'kle^5ine', 'e', 5, 2, 'NE', '["neutral", 0.0]',
 '[0, 2]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze": 1}]',
 'überaschung', '["NN"]', '.', '["symbol"]', 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]',
 'sie', '["PPER"]'),
           (3, 8888, '[4, 9]', '[0, 3]', '[0, 1]', 'kleine', 'klein^3e', 'n', 3, 4, 'NE', '["neutral", 0.0]',
 '[0, 2]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze": 1}]',
 'überaschung', '["NN"]', '.', '["symbol"]', 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]',
 'sie', '["PPER"]'))))
        filtered_reps = stats._filter_full_rep_syn(rep_type, _rep, allowed_ids, order_output_by_syntagma_order, 0)
        tuple(filtered_reps).should.be.equal(tuple(right_filtered_reps))
        rep_type = 'redu'
        _rep = (
         (
          'klitze',
          (
           (1, 8888, '[4, 9]', '[0, 0]', '[0, 0]', 'klitze', '{"klitze": 1, "kli^4tze": 1}', 2,
 'NN', '["neutral", 0.0]', None, None, None, None, None, None, None, None, None,
 None, 'kleine', '["NE", {"kle^5ine": 1, "klein^3e": 1}]', 'überaschung', '["NN"]',
 '.', '["symbol"]', 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]'),
           (4, 12222, '[11]', '[0, 1]', '[0, 1]', 'klitze', '{"klitze": 4}', 4, 'NN', '["neutral", 0.0]',
 None, None, None, None, None, None, None, None, 'eine', '["ART"]', 'kleine', '["ADJA"]',
 'überaschung', '["NN"]', ',', '["symbol"]', 'die', '["PRELS"]', 'ich', '["PPER"]'))),
         (
          'kleine',
          ((2, 8888, '[4, 9]', '[0, 2]', '[0, 1]', 'kleine', '{"kle^5ine": 1, "klein^3e": 1}', 2, 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze": 1}]', 'überaschung', '["NN"]', '.', '["symbol"]', 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]', 'sie', '["PPER"]'), )))
        allowed_ids = set((1, 2))
        order_output_by_syntagma_order = True
        right_filtered_reps = (
         (
          'klitze',
          ((1, 8888, '[4, 9]', '[0, 0]', '[0, 0]', 'klitze', '{"klitze": 1, "kli^4tze": 1}', 2, 'NN', '["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, 'kleine', '["NE", {"kle^5ine": 1, "klein^3e": 1}]', 'überaschung', '["NN"]', '.', '["symbol"]', 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]'), )),
         (
          'kleine',
          ((2, 8888, '[4, 9]', '[0, 2]', '[0, 1]', 'kleine', '{"kle^5ine": 1, "klein^3e": 1}', 2, 'NE', '["neutral", 0.0]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze": 1}]', 'überaschung', '["NN"]', '.', '["symbol"]', 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]', 'sie', '["PPER"]'), )))
        filtered_reps = stats._filter_full_rep_syn(rep_type, _rep, allowed_ids, order_output_by_syntagma_order, 0)
        tuple(filtered_reps).should.be.equal(tuple(right_filtered_reps))
        rep_type = 'redu'
        _rep = (
         (1, 8888, '[4, 9]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze', 'i', 4, 2, 'NN', '["neutral", 0.0]',
 '[0, 0]', None, None, None, None, None, None, None, None, None, None, 'kleine',
 '["NE", {"kle^5ine": 1, "klein^3e": 1}]', 'überaschung', '["NN"]', '.', '["symbol"]',
 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]'),
         (15, 10000, '[8]', '[0, 1]', '[0, 1]', 'klitze', 'klitze^4', 'e', 4, 5, 'VAPPER', '["neutral", 0.0]',
 None, None, None, None, None, None, None, None, None, 'eine', '["ART"]', 'kleine',
 '["ADJA"]', 'überaschung', '["NN"]', '@schönesleben', '["mention"]', '#machwasdaraus',
 '["hashtag"]', '#bewegedeinarsch', '["hashtag"]'),
         (17, 11111, '[5, 12]', '[0, 1]', '[0, 1]', 'klitze', 'klitze^4', 'e', 4, 5, 'VAPPER',
 '["neutral", 0.0]', None, None, None, None, None, None, None, None, None, 'eine',
 '["ART"]', 'kleine', '["ADJA"]', 'sache', '["NN"]', '.', '["symbol"]', 'die', '["PDS"]',
 'aber', '["ADV"]'),
         (2, 8888, '[4, 9]', '[0, 2]', '[0, 1]', 'kleine', 'kle^5ine', 'e', 5, 2, 'NE', '["neutral", 0.0]',
 '[0, 2]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze": 1}]',
 'überaschung', '["NN"]', '.', '["symbol"]', 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]',
 'sie', '["PPER"]'),
         (3, 8888, '[4, 9]', '[0, 3]', '[0, 1]', 'kleine', 'klein^3e', 'n', 3, 4, 'NE', '["neutral", 0.0]',
 '[0, 2]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze": 1}]',
 'überaschung', '["NN"]', '.', '["symbol"]', 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]',
 'sie', '["PPER"]'))
        allowed_ids = set((1, 2))
        order_output_by_syntagma_order = False
        right_filtered_reps = (
         (1, 8888, '[4, 9]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze', 'i', 4, 2, 'NN', '["neutral", 0.0]',
 '[0, 0]', None, None, None, None, None, None, None, None, None, None, 'kleine',
 '["NE", {"kle^5ine": 1, "klein^3e": 1}]', 'überaschung', '["NN"]', '.', '["symbol"]',
 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]'),
         (2, 8888, '[4, 9]', '[0, 2]', '[0, 1]', 'kleine', 'kle^5ine', 'e', 5, 2, 'NE', '["neutral", 0.0]',
 '[0, 2]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze": 1}]',
 'überaschung', '["NN"]', '.', '["symbol"]', 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]',
 'sie', '["PPER"]'))
        filtered_reps = stats._filter_full_rep_syn(rep_type, _rep, allowed_ids, order_output_by_syntagma_order, 0)
        tuple(filtered_reps).should.be.equal(tuple(right_filtered_reps))
        return

    @attr(status='stable')
    def test_delete_dublicats_in_reps_633(self):
        stats = Stats(mode=self.mode)
        order_output_by_syntagma_order = True
        _rep = (
         (
          'klitze',
          (
           (1, 8888, '[4, 9]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze', 'i', 4, 2, 'NN', '["neutral", 0.0]',
 '[0, 0]', None, None, None, None, None, None, None, None, None, None, 'kleine',
 '["NE", {"kle^5ine": 1, "klein^3e": 1}]', 'überaschung', '["NN"]', '.', '["symbol"]',
 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]'),
           (1, 8888, '[4, 9]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze', 'i', 4, 2, 'NN', '["neutral", 0.0]',
 '[0, 0]', None, None, None, None, None, None, None, None, None, None, 'kleine',
 '["NE", {"kle^5ine": 1, "klein^3e": 1}]', 'überaschung', '["NN"]', '.', '["symbol"]',
 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]'),
           (1, 8888, '[4, 9]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze', 'i', 4, 2, 'NN', '["neutral", 0.0]',
 '[0, 0]', None, None, None, None, None, None, None, None, None, None, 'kleine',
 '["NE", {"kle^5ine": 1, "klein^3e": 1}]', 'überaschung', '["NN"]', '.', '["symbol"]',
 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]'))),
         (
          'kleine',
          (
           (2, 8888, '[4, 9]', '[0, 2]', '[0, 1]', 'kleine', 'kle^5ine', 'e', 5, 2, 'NE', '["neutral", 0.0]',
 '[0, 2]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze": 1}]',
 'überaschung', '["NN"]', '.', '["symbol"]', 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]',
 'sie', '["PPER"]'),
           (3, 8888, '[4, 9]', '[0, 3]', '[0, 1]', 'kleine', 'klein^3e', 'n', 3, 4, 'NE', '["neutral", 0.0]',
 '[0, 2]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze": 1}]',
 'überaschung', '["NN"]', '.', '["symbol"]', 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]',
 'sie', '["PPER"]'),
           (3, 8888, '[4, 9]', '[0, 3]', '[0, 1]', 'kleine', 'klein^3e', 'n', 3, 4, 'NE', '["neutral", 0.0]',
 '[0, 2]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze": 1}]',
 'überaschung', '["NN"]', '.', '["symbol"]', 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]',
 'sie', '["PPER"]'))))
        right_dublicates_free = (
         (
          'klitze',
          ((1, 8888, '[4, 9]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze', 'i', 4, 2, 'NN', '["neutral", 0.0]', '[0, 0]', None, None, None, None, None, None, None, None, None, None, 'kleine', '["NE", {"kle^5ine": 1, "klein^3e": 1}]', 'überaschung', '["NN"]', '.', '["symbol"]', 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]'), )),
         (
          'kleine',
          (
           (2, 8888, '[4, 9]', '[0, 2]', '[0, 1]', 'kleine', 'kle^5ine', 'e', 5, 2, 'NE', '["neutral", 0.0]',
 '[0, 2]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze": 1}]',
 'überaschung', '["NN"]', '.', '["symbol"]', 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]',
 'sie', '["PPER"]'),
           (3, 8888, '[4, 9]', '[0, 3]', '[0, 1]', 'kleine', 'klein^3e', 'n', 3, 4, 'NE', '["neutral", 0.0]',
 '[0, 2]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze": 1}]',
 'überaschung', '["NN"]', '.', '["symbol"]', 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]',
 'sie', '["PPER"]'))))
        dublicats_free = stats._delete_dublicats_in_reps(_rep, order_output_by_syntagma_order, 0)
        tuple(right_dublicates_free).should.be.equal(tuple(dublicats_free))
        stats._full_repetativ_syntagma = True
        order_output_by_syntagma_order = True
        _rep = (
         (
          'klitze',
          (
           (1, 8888, '[4, 9]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze', 'i', 4, 2, 'NN', '["neutral", 0.0]',
 '[0, 0]', None, None, None, None, None, None, None, None, None, None, 'kleine',
 '["NE", {"kle^5ine": 1, "klein^3e": 1}]', 'überaschung', '["NN"]', '.', '["symbol"]',
 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]'),
           (1, 8888, '[4, 9]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze', 'i', 4, 2, 'NN', '["neutral", 0.0]',
 '[0, 0]', None, None, None, None, None, None, None, None, None, None, 'kleine',
 '["NE", {"kle^5ine": 1, "klein^3e": 1}]', 'überaschung', '["NN"]', '.', '["symbol"]',
 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]'),
           (1, 8888, '[4, 9]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze', 'i', 4, 2, 'NN', '["neutral", 0.0]',
 '[0, 0]', None, None, None, None, None, None, None, None, None, None, 'kleine',
 '["NE", {"kle^5ine": 1, "klein^3e": 1}]', 'überaschung', '["NN"]', '.', '["symbol"]',
 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]'))),
         (
          'kleine',
          (
           (1, 8888, '[4, 9]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze', 'i', 4, 2, 'NN', '["neutral", 0.0]',
 '[0, 0]', None, None, None, None, None, None, None, None, None, None, 'kleine',
 '["NE", {"kle^5ine": 1, "klein^3e": 1}]', 'überaschung', '["NN"]', '.', '["symbol"]',
 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]'),
           (1, 8888, '[4, 9]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze', 'i', 4, 2, 'NN', '["neutral", 0.0]',
 '[0, 0]', None, None, None, None, None, None, None, None, None, None, 'kleine',
 '["NE", {"kle^5ine": 1, "klein^3e": 1}]', 'überaschung', '["NN"]', '.', '["symbol"]',
 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]'),
           (1, 8888, '[4, 9]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze', 'i', 4, 2, 'NN', '["neutral", 0.0]',
 '[0, 0]', None, None, None, None, None, None, None, None, None, None, 'kleine',
 '["NE", {"kle^5ine": 1, "klein^3e": 1}]', 'überaschung', '["NN"]', '.', '["symbol"]',
 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]'))))
        right_dublicates_free = ()
        dublicats_free = stats._delete_dublicats_in_reps(_rep, order_output_by_syntagma_order, 0)
        tuple(right_dublicates_free).should.be.equal(tuple(dublicats_free))
        stats._full_repetativ_syntagma = False
        order_output_by_syntagma_order = True
        _rep = (
         (
          'klitze',
          (
           (1, 8888, '[4, 9]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze', 'i', 4, 2, 'NN', '["neutral", 0.0]',
 '[0, 0]', None, None, None, None, None, None, None, None, None, None, 'kleine',
 '["NE", {"kle^5ine": 1, "klein^3e": 1}]', 'überaschung', '["NN"]', '.', '["symbol"]',
 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]'),
           (1, 8888, '[4, 9]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze', 'i', 4, 2, 'NN', '["neutral", 0.0]',
 '[0, 0]', None, None, None, None, None, None, None, None, None, None, 'kleine',
 '["NE", {"kle^5ine": 1, "klein^3e": 1}]', 'überaschung', '["NN"]', '.', '["symbol"]',
 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]'),
           (1, 8888, '[4, 9]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze', 'i', 4, 2, 'NN', '["neutral", 0.0]',
 '[0, 0]', None, None, None, None, None, None, None, None, None, None, 'kleine',
 '["NE", {"kle^5ine": 1, "klein^3e": 1}]', 'überaschung', '["NN"]', '.', '["symbol"]',
 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]'))),
         (
          'kleine',
          (
           (1, 8888, '[4, 9]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze', 'i', 4, 2, 'NN', '["neutral", 0.0]',
 '[0, 0]', None, None, None, None, None, None, None, None, None, None, 'kleine',
 '["NE", {"kle^5ine": 1, "klein^3e": 1}]', 'überaschung', '["NN"]', '.', '["symbol"]',
 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]'),
           (1, 8888, '[4, 9]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze', 'i', 4, 2, 'NN', '["neutral", 0.0]',
 '[0, 0]', None, None, None, None, None, None, None, None, None, None, 'kleine',
 '["NE", {"kle^5ine": 1, "klein^3e": 1}]', 'überaschung', '["NN"]', '.', '["symbol"]',
 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]'),
           (1, 8888, '[4, 9]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze', 'i', 4, 2, 'NN', '["neutral", 0.0]',
 '[0, 0]', None, None, None, None, None, None, None, None, None, None, 'kleine',
 '["NE", {"kle^5ine": 1, "klein^3e": 1}]', 'überaschung', '["NN"]', '.', '["symbol"]',
 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]'))))
        right_dublicates_free = (
         (
          'klitze', ()),
         (
          'kleine',
          ((1, 8888, '[4, 9]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze', 'i', 4, 2, 'NN', '["neutral", 0.0]', '[0, 0]', None, None, None, None, None, None, None, None, None, None, 'kleine', '["NE", {"kle^5ine": 1, "klein^3e": 1}]', 'überaschung', '["NN"]', '.', '["symbol"]', 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]'), )))
        dublicats_free = stats._delete_dublicats_in_reps(_rep, order_output_by_syntagma_order, 0)
        tuple(right_dublicates_free).should.be.equal(tuple(dublicats_free))
        stats._full_repetativ_syntagma = True
        order_output_by_syntagma_order = True
        _rep = (
         (
          'number',
          (
           (20, 11111, '[5, 12]', '[1, 6]', '[1, 6]', '1', '1^5', '1', 5, 0, 'number', '["neutral", 0.0]',
 None, 'aber', '["ADV"]', 'trotzdem', '["PAV"]', 'wichtig', '["ADJA"]', 'ist', '["NN"]',
 '!', '["symbol"]', 2, '["number"]', 3, '["number"]', 4, '["number"]', 5, '["number"]',
 6, '["number"]'),
           (21, 11111, '[5, 12]', '[1, 7]', '[1, 7]', '2', '2^4', '2', 4, 0, 'number', '["neutral", 0.0]',
 None, 'trotzdem', '["PAV"]', 'wichtig', '["ADJA"]', 'ist', '["NN"]', '!', '["symbol"]',
 1, '["number"]', 3, '["number"]', 4, '["number"]', 5, '["number"]', 6, '["number"]',
 None, None),
           (22, 11111, '[5, 12]', '[1, 8]', '[1, 8]', '3', '3^5', '3', 5, 0, 'number', '["neutral", 0.0]',
 None, 'wichtig', '["ADJA"]', 'ist', '["NN"]', '!', '["symbol"]', 1, '["number"]',
 2, '["number"]', 4, '["number"]', 5, '["number"]', 6, '["number"]', None, None,
 None, None),
           (23, 11111, '[5, 12]', '[1, 9]', '[1, 9]', '4', '4^4', '4', 4, 0, 'number', '["neutral", 0.0]',
 None, 'ist', '["NN"]', '!', '["symbol"]', 1, '["number"]', 2, '["number"]', 3, '["number"]',
 5, '["number"]', 6, '["number"]', None, None, None, None, None, None))),
         (
          'number',
          (
           (21, 11111, '[5, 12]', '[1, 7]', '[1, 7]', '2', '2^4', '2', 4, 0, 'number', '["neutral", 0.0]',
 None, 'trotzdem', '["PAV"]', 'wichtig', '["ADJA"]', 'ist', '["NN"]', '!', '["symbol"]',
 1, '["number"]', 3, '["number"]', 4, '["number"]', 5, '["number"]', 6, '["number"]',
 None, None),
           (22, 11111, '[5, 12]', '[1, 8]', '[1, 8]', '3', '3^5', '3', 5, 0, 'number', '["neutral", 0.0]',
 None, 'wichtig', '["ADJA"]', 'ist', '["NN"]', '!', '["symbol"]', 1, '["number"]',
 2, '["number"]', 4, '["number"]', 5, '["number"]', 6, '["number"]', None, None,
 None, None),
           (23, 11111, '[5, 12]', '[1, 9]', '[1, 9]', '4', '4^4', '4', 4, 0, 'number', '["neutral", 0.0]',
 None, 'ist', '["NN"]', '!', '["symbol"]', 1, '["number"]', 2, '["number"]', 3, '["number"]',
 5, '["number"]', 6, '["number"]', None, None, None, None, None, None),
           (24, 11111, '[5, 12]', '[1, 10]', '[1, 10]', '5', '5^5', '5', 5, 0, 'number', '["neutral", 0.0]',
 None, '!', '["symbol"]', 1, '["number"]', 2, '["number"]', 3, '["number"]', 4, '["number"]',
 6, '["number"]', None, None, None, None, None, None, None, None))),
         (
          'number',
          (
           (22, 11111, '[5, 12]', '[1, 8]', '[1, 8]', '3', '3^5', '3', 5, 0, 'number', '["neutral", 0.0]',
 None, 'wichtig', '["ADJA"]', 'ist', '["NN"]', '!', '["symbol"]', 1, '["number"]',
 2, '["number"]', 4, '["number"]', 5, '["number"]', 6, '["number"]', None, None,
 None, None),
           (23, 11111, '[5, 12]', '[1, 9]', '[1, 9]', '4', '4^4', '4', 4, 0, 'number', '["neutral", 0.0]',
 None, 'ist', '["NN"]', '!', '["symbol"]', 1, '["number"]', 2, '["number"]', 3, '["number"]',
 5, '["number"]', 6, '["number"]', None, None, None, None, None, None),
           (24, 11111, '[5, 12]', '[1, 10]', '[1, 10]', '5', '5^5', '5', 5, 0, 'number', '["neutral", 0.0]',
 None, '!', '["symbol"]', 1, '["number"]', 2, '["number"]', 3, '["number"]', 4, '["number"]',
 6, '["number"]', None, None, None, None, None, None, None, None))))
        right_dublicates_free = (
         (
          'number',
          ((20, 11111, '[5, 12]', '[1, 6]', '[1, 6]', '1', '1^5', '1', 5, 0, 'number', '["neutral", 0.0]', None, 'aber', '["ADV"]', 'trotzdem', '["PAV"]', 'wichtig', '["ADJA"]', 'ist', '["NN"]', '!', '["symbol"]', 2, '["number"]', 3, '["number"]', 4, '["number"]', 5, '["number"]', 6, '["number"]'), )),
         (
          'number',
          ((21, 11111, '[5, 12]', '[1, 7]', '[1, 7]', '2', '2^4', '2', 4, 0, 'number', '["neutral", 0.0]', None, 'trotzdem', '["PAV"]', 'wichtig', '["ADJA"]', 'ist', '["NN"]', '!', '["symbol"]', 1, '["number"]', 3, '["number"]', 4, '["number"]', 5, '["number"]', 6, '["number"]', None, None), )),
         (
          'number',
          (
           (22, 11111, '[5, 12]', '[1, 8]', '[1, 8]', '3', '3^5', '3', 5, 0, 'number', '["neutral", 0.0]',
 None, 'wichtig', '["ADJA"]', 'ist', '["NN"]', '!', '["symbol"]', 1, '["number"]',
 2, '["number"]', 4, '["number"]', 5, '["number"]', 6, '["number"]', None, None,
 None, None),
           (23, 11111, '[5, 12]', '[1, 9]', '[1, 9]', '4', '4^4', '4', 4, 0, 'number', '["neutral", 0.0]',
 None, 'ist', '["NN"]', '!', '["symbol"]', 1, '["number"]', 2, '["number"]', 3, '["number"]',
 5, '["number"]', 6, '["number"]', None, None, None, None, None, None),
           (24, 11111, '[5, 12]', '[1, 10]', '[1, 10]', '5', '5^5', '5', 5, 0, 'number', '["neutral", 0.0]',
 None, '!', '["symbol"]', 1, '["number"]', 2, '["number"]', 3, '["number"]', 4, '["number"]',
 6, '["number"]', None, None, None, None, None, None, None, None))))
        dublicats_free = stats._delete_dublicats_in_reps(_rep, order_output_by_syntagma_order, 0)
        tuple(right_dublicates_free).should.be.equal(tuple(dublicats_free))
        order_output_by_syntagma_order = False
        _rep = (
         (1, 8888, '[4, 9]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze', 'i', 4, 2, 'NN', '["neutral", 0.0]',
 '[0, 0]', None, None, None, None, None, None, None, None, None, None, 'kleine',
 '["NE", {"kle^5ine": 1, "klein^3e": 1}]', 'überaschung', '["NN"]', '.', '["symbol"]',
 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]'),
         (2, 8888, '[4, 9]', '[0, 2]', '[0, 1]', 'kleine', 'kle^5ine', 'e', 5, 2, 'NE', '["neutral", 0.0]',
 '[0, 2]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze": 1}]',
 'überaschung', '["NN"]', '.', '["symbol"]', 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]',
 'sie', '["PPER"]'),
         (2, 8888, '[4, 9]', '[0, 2]', '[0, 1]', 'kleine', 'kle^5ine', 'e', 5, 2, 'NE', '["neutral", 0.0]',
 '[0, 2]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze": 1}]',
 'überaschung', '["NN"]', '.', '["symbol"]', 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]',
 'sie', '["PPER"]'),
         (2, 8888, '[4, 9]', '[0, 2]', '[0, 1]', 'kleine', 'kle^5ine', 'e', 5, 2, 'NE', '["neutral", 0.0]',
 '[0, 2]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze": 1}]',
 'überaschung', '["NN"]', '.', '["symbol"]', 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]',
 'sie', '["PPER"]'),
         (2, 8888, '[4, 9]', '[0, 2]', '[0, 1]', 'kleine', 'kle^5ine', 'e', 5, 2, 'NE', '["neutral", 0.0]',
 '[0, 2]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze": 1}]',
 'überaschung', '["NN"]', '.', '["symbol"]', 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]',
 'sie', '["PPER"]'),
         (1, 8888, '[4, 9]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze', 'i', 4, 2, 'NN', '["neutral", 0.0]',
 '[0, 0]', None, None, None, None, None, None, None, None, None, None, 'kleine',
 '["NE", {"kle^5ine": 1, "klein^3e": 1}]', 'überaschung', '["NN"]', '.', '["symbol"]',
 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]'))
        right_dublicates_free = (
         (1, 8888, '[4, 9]', '[0, 1]', '[0, 0]', 'klitze', 'kli^4tze', 'i', 4, 2, 'NN', '["neutral", 0.0]',
 '[0, 0]', None, None, None, None, None, None, None, None, None, None, 'kleine',
 '["NE", {"kle^5ine": 1, "klein^3e": 1}]', 'überaschung', '["NN"]', '.', '["symbol"]',
 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]'),
         (2, 8888, '[4, 9]', '[0, 2]', '[0, 1]', 'kleine', 'kle^5ine', 'e', 5, 2, 'NE', '["neutral", 0.0]',
 '[0, 2]', None, None, None, None, None, None, None, None, 'klitze', '["NN", {"klitze": 1, "kli^4tze": 1}]',
 'überaschung', '["NN"]', '.', '["symbol"]', 'trotzdem', '["PAV"]', 'hat', '["VAFIN"]',
 'sie', '["PPER"]'))
        dublicats_free = stats._delete_dublicats_in_reps(_rep, order_output_by_syntagma_order, 0)
        tuple(dublicats_free).should.be.equal(tuple(right_dublicates_free))
        return

    def get_dict_rows_from_csv(self, fname):
        with open(fname + '.csv') as (csvfile):
            readCSV = csv.reader(csvfile, delimiter=';')
            columns = readCSV.next()
            for row in readCSV:
                if row[0]:
                    yield {k:v for k, v in zip(columns, row) if k if k}

    def get_list_rows_from_csv(self, fname):
        with open(fname + '.csv') as (csvfile):
            readCSV = csv.reader(csvfile, delimiter=';')
            columns = readCSV.next()
            for row in readCSV:
                if row[0]:
                    yield row

    @attr(status='stable')
    def test_compute_rep_sum_700(self):
        self.prj_folder()
        self.test_dbs()
        stats = Stats(mode=self.mode, use_cash=True)
        stats.open(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_stats_de))
        summery = stats.compute_rep_sum('*', 'repl')
        summery = {letter:{rep_num:[rep_num_data[0], dict(rep_num_data[1])] for rep_num, rep_num_data in letter_data.iteritems()} for letter, letter_data in summery.iteritems()}
        right_summery = {'a': {3: [1, {'übe^4r^5a^3schun^6g^3': 1}], 4: [1, {'ka^4n^5': 1}], 6: [1, {'ta^6g^6': 1}]}, 'z': {3: [1, {'kli^4tz^3': 1}]}, 'e': {8: [2, {'kle^4i^5n^4e^8': 1, 'ble^8ibt': 1}], 3: [4, {'kle^3i^3n^3': 1, 'klein^4e^3s^4': 2, 'kleine^3r^2e^5': 1}], 4: [10, {'übe^4r^5a^3schun^6g^3': 1, 'ble^4ibt': 1, 'kle^4i^5n^4e^8': 1, 'kle^4i^5n^3e^2s^3': 2, 'eine^4': 1, 'kleine^4s^7': 2, 'klitze^4': 2}], 5: [6, {'kle^5ine': 1, 'kleinere^5': 1, 'kle^5in^5e': 1, 'kle^5i^2n^4e^5': 2, 'kleine^3r^2e^5': 1}], 7: [1, {'kli^4tze^7': 1}]}, 'g': {3: [1, {'übe^4r^5a^3schun^6g^3': 1}], 6: [1, {'ta^6g^6': 1}]}, '4': {4: [1, {'4^4': 1}]}, ')': {3: [3, {'-)^3': 3}], 4: [1, {':-)^4': 1}]}, 'h': {3: [1, {'auswah^3l^4': 1}]}, 'l': {4: [1, {'auswah^3l^4': 1}]}, 'n': {3: [5, {'kle^4i^5n^3e^2s^3': 2, 'kle^3i^3n^3': 1, 'klein^3e^2s': 1, 'klein^3e': 1}], 4: [4, {'kle^4i^5n^4e^8': 1, 'klein^4e^3s^4': 2, 'kle^5i^2n^4e^5': 1}], 5: [5, {'klein^5': 1, 'ka^4n^5': 1, 'kle^5in^5e': 1, 'mädchen^5': 2}], 6: [2, {'übe^4r^5a^3schun^6g^3': 1, 'kan^6': 1}]}, '1': {8: [1, {'1^8': 1}], 5: [1, {'1^5': 1}], 6: [1, {'1^6': 1}]}, 'i': {8: [1, {'wichti^8g': 1}], 3: [2, {'kle^3i^3n^3': 1, 'kli^3tzes^3': 1}], 4: [3, {'kli^4tz': 1, 'kli^4tze^7': 1, 'kli^4tz^3': 1}], 5: [4, {'kle^4i^5n^3e^2s^3': 2, 'kle^4i^5n^4e^8': 1, 'geni^5es^8t^5': 1}]}, '3': {5: [1, {'3^5': 1}]}, 'r': {4: [2, {'über^4aschung': 2}], 5: [2, {'übe^4r^5a^3schun^6g^3': 1, 'über^5aschung': 1}]}, '5': {5: [1, {'5^5': 1}]}, '😀': {5: [1, {'😀^5': 1}]}, '2': {4: [1, {'2^4': 1}]}, 's': {8: [1, {'geni^5es^8t^5': 1}], 3: [3, {'kle^4i^5n^3e^2s^3': 2, 'kli^3tzes^3': 1}], 4: [5, {'kleines^4': 1, 'klitzes^4': 1, 'genies^4t^2': 1, 'klein^4e^3s^4': 2}], 6: [1, {'is^6t': 1}], 7: [2, {'kleine^4s^7': 2}]}, '.': {5: [2, {'.^5': 2}]}, 'u': {12: [1, {'hu^12ngrig': 1}]}, '😫': {4: [1, {'😫^4': 1}]}, 't': {5: [1, {'geni^5es^8t^5': 1}]}}
        summery.should.be.equal(right_summery)
        summery = stats.compute_rep_sum('*', 'repl', ignore_num=True, ignore_symbol=True)
        summery = {letter:{rep_num:[rep_num_data[0], dict(rep_num_data[1])] for rep_num, rep_num_data in letter_data.iteritems()} for letter, letter_data in summery.iteritems()}
        right_summery = {'a': {3: [1, {'übe^4r^5a^3schun^6g^3': 1}], 4: [1, {'ka^4n^5': 1}], 6: [1, {'ta^6g^6': 1}]}, 'e': {8: [2, {'kle^4i^5n^4e^8': 1, 'ble^8ibt': 1}], 3: [4, {'kle^3i^3n^3': 1, 'klein^4e^3s^4': 2, 'kleine^3r^2e^5': 1}], 4: [10, {'übe^4r^5a^3schun^6g^3': 1, 'ble^4ibt': 1, 'kle^4i^5n^4e^8': 1, 'kle^4i^5n^3e^2s^3': 2, 'eine^4': 1, 'kleine^4s^7': 2, 'klitze^4': 2}], 5: [6, {'kle^5ine': 1, 'kleinere^5': 1, 'kle^5in^5e': 1, 'kle^5i^2n^4e^5': 2, 'kleine^3r^2e^5': 1}], 7: [1, {'kli^4tze^7': 1}]}, 'g': {3: [1, {'übe^4r^5a^3schun^6g^3': 1}], 6: [1, {'ta^6g^6': 1}]}, 'i': {8: [1, {'wichti^8g': 1}], 3: [2, {'kle^3i^3n^3': 1, 'kli^3tzes^3': 1}], 4: [3, {'kli^4tz': 1, 'kli^4tze^7': 1, 'kli^4tz^3': 1}], 5: [4, {'kle^4i^5n^3e^2s^3': 2, 'kle^4i^5n^4e^8': 1, 'geni^5es^8t^5': 1}]}, 'h': {3: [1, {'auswah^3l^4': 1}]}, 'l': {4: [1, {'auswah^3l^4': 1}]}, 'n': {3: [5, {'kle^4i^5n^3e^2s^3': 2, 'kle^3i^3n^3': 1, 'klein^3e^2s': 1, 'klein^3e': 1}], 4: [4, {'kle^4i^5n^4e^8': 1, 'klein^4e^3s^4': 2, 'kle^5i^2n^4e^5': 1}], 5: [5, {'klein^5': 1, 'ka^4n^5': 1, 'kle^5in^5e': 1, 'mädchen^5': 2}], 6: [2, {'übe^4r^5a^3schun^6g^3': 1, 'kan^6': 1}]}, ')': {3: [3, {'-)^3': 3}], 4: [1, {':-)^4': 1}]}, 's': {8: [1, {'geni^5es^8t^5': 1}], 3: [3, {'kle^4i^5n^3e^2s^3': 2, 'kli^3tzes^3': 1}], 4: [5, {'kleines^4': 1, 'klitzes^4': 1, 'genies^4t^2': 1, 'klein^4e^3s^4': 2}], 6: [1, {'is^6t': 1}], 7: [2, {'kleine^4s^7': 2}]}, 'r': {4: [2, {'über^4aschung': 2}], 5: [2, {'übe^4r^5a^3schun^6g^3': 1, 'über^5aschung': 1}]}, 'u': {12: [1, {'hu^12ngrig': 1}]}, '😀': {5: [1, {'😀^5': 1}]}, 'z': {3: [1, {'kli^4tz^3': 1}]}, '😫': {4: [1, {'😫^4': 1}]}, 't': {5: [1, {'geni^5es^8t^5': 1}]}}
        summery.should.be.equal(right_summery)
        summery = stats.compute_rep_sum('*', 'repl', ignore_num=True, ignore_symbol=True, word_examples_sum_table=False)
        summery = {letter:{rep_num:[rep_num_data[0]] for rep_num, rep_num_data in letter_data.iteritems()} for letter, letter_data in summery.iteritems()}
        right_summery = {'a': {3: [1], 4: [1], 6: [1]}, 'e': {8: [2], 3: [4], 4: [10], 5: [6], 7: [1]}, 'g': {3: [1], 6: [1]}, 'i': {8: [1], 3: [2], 4: [3], 5: [4]}, 'h': {3: [1]}, 'l': {4: [1]}, 'n': {3: [5], 4: [4], 5: [5], 6: [2]}, ')': {3: [3], 4: [1]}, 's': {8: [1], 3: [3], 4: [5], 6: [1], 7: [2]}, 'r': {4: [2], 5: [2]}, 'u': {12: [1]}, '😀': {5: [1]}, 'z': {3: [1]}, '😫': {4: [1]}, 't': {5: [1]}}
        summery.should.be.equal(right_summery)
        summery = stats.compute_rep_sum('*', 'repl', ignore_num=True, ignore_symbol=True, sentiment='positive')
        summery = summery = {letter:{rep_num:[rep_num_data[0], dict(rep_num_data[1])] for rep_num, rep_num_data in letter_data.iteritems()} for letter, letter_data in summery.iteritems()}
        right_summery = {')': {3: [3, {'-)^3': 3}], 4: [1, {':-)^4': 1}]}, '😀': {5: [1, {'😀^5': 1}]}}
        summery.should.be.equal(right_summery)
        summery = stats.compute_rep_sum(['klitze'], 'repl', ignore_num=True, ignore_symbol=True, word_examples_sum_table=True)
        summery = summery = {letter:{rep_num:[rep_num_data[0], dict(rep_num_data[1])] for rep_num, rep_num_data in letter_data.iteritems()} for letter, letter_data in summery.iteritems()}
        right_summery = {'i': {4: [1, {'kli^4tze^7': 1}]}, 'e': {4: [2, {'klitze^4': 2}], 7: [1, {'kli^4tze^7': 1}]}}
        summery.should.be.equal(right_summery)
        summery = stats.compute_rep_sum(['klitze', 'kleine'], 'repl', ignore_num=True, ignore_symbol=True)
        summery = {letter:{rep_num:[rep_num_data[0], dict(rep_num_data[1])] for rep_num, rep_num_data in letter_data.iteritems()} for letter, letter_data in summery.iteritems()}
        right_summery = {'i': {4: [1, {'kli^4tze^7': 1}]}, 'e': {4: [1, {'klitze^4': 1}], 5: [2, {'kle^5ine': 1, 'kle^5in^5e': 1}], 7: [1, {'kli^4tze^7': 1}]}, 'n': {3: [1, {'klein^3e': 1}], 5: [1, {'kle^5in^5e': 1}]}}
        summery.should.be.equal(right_summery)
        summery = stats.compute_rep_sum(['klitze', 'kleine'], 'repl', ignore_num=True, ignore_symbol=True, stemmed_search=True)
        summery = {letter:{rep_num:[rep_num_data[0], dict(rep_num_data[1])] for rep_num, rep_num_data in letter_data.iteritems()} for letter, letter_data in summery.iteritems()}
        right_summery = {'i': {3: [2, {'kle^3i^3n^3': 1, 'kli^3tzes^3': 1}], 4: [3, {'kli^4tz': 1, 'kli^4tze^7': 1, 'kli^4tz^3': 1}]}, 's': {3: [1, {'kli^3tzes^3': 1}], 4: [2, {'klitzes^4': 1, 'kleines^4': 1}]}, 'z': {3: [1, {'kli^4tz^3': 1}]}, 'e': {3: [1, {'kle^3i^3n^3': 1}], 4: [1, {'klitze^4': 1}], 5: [2, {'kle^5ine': 1, 'kle^5in^5e': 1}], 7: [1, {'kli^4tze^7': 1}]}, 'n': {3: [3, {'klein^3e^2s': 1, 'kle^3i^3n^3': 1, 'klein^3e': 1}], 5: [2, {'kle^5in^5e': 1, 'klein^5': 1}]}}
        summery.should.be.equal(right_summery)
        summery = stats.compute_rep_sum(['klitze'], 'repl', ignore_num=True, ignore_symbol=True)
        summery = {letter:{rep_num:[rep_num_data[0], dict(rep_num_data[1])] for rep_num, rep_num_data in letter_data.iteritems()} for letter, letter_data in summery.iteritems()}
        right_summery = {'i': {4: [1, {'kli^4tze^7': 1}]}, 'e': {4: [2, {'klitze^4': 2}], 7: [1, {'kli^4tze^7': 1}]}}
        summery.should.be.equal(right_summery)
        summery = stats.compute_rep_sum(['klitze', 'kleine'], 'repl', ignore_num=True, ignore_symbol=True, stemmed_search=True)
        summery = {letter:{rep_num:[rep_num_data[0], dict(rep_num_data[1])] for rep_num, rep_num_data in letter_data.iteritems()} for letter, letter_data in summery.iteritems()}
        right_summery = {'i': {3: [2, {'kle^3i^3n^3': 1, 'kli^3tzes^3': 1}], 4: [3, {'kli^4tz': 1, 'kli^4tze^7': 1, 'kli^4tz^3': 1}]}, 's': {3: [1, {'kli^3tzes^3': 1}], 4: [2, {'klitzes^4': 1, 'kleines^4': 1}]}, 'z': {3: [1, {'kli^4tz^3': 1}]}, 'e': {3: [1, {'kle^3i^3n^3': 1}], 4: [1, {'klitze^4': 1}], 5: [2, {'kle^5ine': 1, 'kle^5in^5e': 1}], 7: [1, {'kli^4tze^7': 1}]}, 'n': {3: [3, {'klein^3e^2s': 1, 'kle^3i^3n^3': 1, 'klein^3e': 1}], 5: [2, {'kle^5in^5e': 1, 'klein^5': 1}]}}
        summery.should.be.equal(right_summery)
        summery = stats.compute_rep_sum('*', 'redu')
        summery = {word:{redu_length:occur for redu_length, occur in word_data.iteritems()} for word, word_data in summery.iteritems()}
        right_summery = {'-)': {2: 1}, 'baseline': {3: 2}, 'bleibt': {2: 1}, 'geniest': {2: 1}, 'in': {4: 2}, 'kan': {2: 1}, 'klein': {2: 1}, 'kleine': {2: 1}, 'kleinere': {2: 1}, 'kleines': {2: 1, 3: 2}, 'klitz': {3: 1}, 'klitze': {2: 1, 4: 1}, 'klitzes': {2: 1}}
        summery.should.be.equal(right_summery)