# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/egoruni/Desktop/BA/Code/zas-rep-tools/zas_rep_tools/tests/test_integrations_tests.py
# Compiled at: 2018-10-15 23:12:48
import unittest, os, logging, sure, copy
from nose.plugins.attrib import attr
from testfixtures import tempdir, TempDirectory
from distutils.dir_util import copy_tree
import json, csv
from collections import Counter, defaultdict
from zas_rep_tools.src.classes.stats import Stats
from zas_rep_tools.src.classes.reader import Reader
from zas_rep_tools.src.classes.corpus import Corpus
from zas_rep_tools.src.utils.debugger import p, wipd, wipdn, wipdl, wipdo
from zas_rep_tools.src.utils.basetester import BaseTester
import zas_rep_tools.src.utils.db_helper as db_helper, platform
if platform.uname()[0].lower() != 'windows':
    import colored_traceback
    colored_traceback.add_hook()
else:
    import colorama

class TestZASIntergrationTests(BaseTester, unittest.TestCase):
    _multiprocess_shared_ = True

    def setUp(self):
        super(type(self), self).setUp()

    def tearDown(self):
        super(type(self), self).tearDown()

    @attr(status='stable')
    def test_data_insertion_000(self):
        corpus = Corpus(mode=self.mode)
        stats = Stats(mode=self.mode)
        stats.should.be.a(Stats)

    def _get_basic_info_about_reps(self, data):
        extracted = {}
        for item in data:
            temp_item = []
            temp = [ [ unicode(el) for el in _item ] for _item in item['baseline'] ]
            extracted[tuple(item['syntagma'])] = temp

        return extracted

    def convert(self, inp):
        return [ [ unicode(el) for el in _item ] for _item in inp ]

    @attr(status='stable')
    def test_work_flow_with_basic_reps_500(self):
        self.prj_folder()
        self.input_list = [
         {'rowid': '1', 
            'star_constellation': 'Capricorn', 
            'text': 'Klitze klitze kleine kleine Menge...', 
            'working_area': 'IT Consulting', 
            'age': '46', 
            'id': '324114', 
            'gender': 'female'},
         {'rowid': '2', 
            'star_constellation': 'Fish', 
            'text': 'Klitze klitze kleine kleine Menge...', 
            'working_area': 'IT Developing', 
            'age': '23', 
            'id': '8765', 
            'gender': 'male'}]
        name = 'test_corp'
        language = 'de'
        visibility = 'intern'
        platform_name = 'blogger'
        source = 'test'
        license = 'test'
        template_name = 'blogger'
        version = 1
        corp_typ = 'corpus'
        preprocession = True
        tokenizer = True
        pos_tagger = False
        sent_splitter = True
        sentiment_analyzer = True
        lang_classification = False
        del_url = False
        del_punkt = False
        del_num = False
        del_html = False
        del_mention = False
        del_hashtag = False
        case_sensitiv = True
        corp = Corpus(logger_level=logging.DEBUG, mode=self.mode)
        corp.init(self.tempdir_project_folder, name, language, visibility, platform_name, source=source, license=license, template_name=template_name, version=version, preprocession=preprocession, tokenizer=tokenizer, pos_tagger=pos_tagger, sent_splitter=sent_splitter, sentiment_analyzer=sentiment_analyzer, lang_classification=lang_classification, del_url=del_url, del_punkt=del_punkt, del_num=del_num, del_html=del_html, del_mention=del_mention, del_hashtag=del_hashtag, case_sensitiv=case_sensitiv)
        corp.insert(self.input_list)
        list(corp.docs(columns='text'))[0].should.be.equal(('[[[["Klitze", "regular"], ["klitze", "regular"], ["kleine", "regular"], ["kleine", "regular"], ["Menge", "regular"], ["...", "symbol"]], ["neutral", 0.0]]]', ))
        list(corp.docs(columns='text'))[1].should.be.equal(('[[[["Klitze", "regular"], ["klitze", "regular"], ["kleine", "regular"], ["kleine", "regular"], ["Menge", "regular"], ["...", "symbol"]], ["neutral", 0.0]]]', ))
        corp.corpdb.get_attr('token_num').should.be.equal(12)
        corp.corpdb.get_attr('doc_num').should.be.equal(2)
        corp.corpdb.get_attr('sent_num').should.be.equal(2)
        case_sensitiv_stat = False
        stats = Stats(mode=self.mode)
        stats.init(self.tempdir_project_folder, name, language, visibility, version=version, full_repetativ_syntagma=True, case_sensitiv=case_sensitiv_stat, baseline_delimiter='++')
        stats.compute(corp)
        basic_info = self._get_basic_info_about_reps(stats.get_data(redu=True, repl=True, baseline=True))
        basic_info[('klitze', )].should.be.equal(self.convert(([['klitze'], 'klitz', 1, 4, None, None, '2', '4', None, '2'],)))
        basic_info[('kleine', )].should.be.equal(self.convert(([['kleine'], 'klein', 1, 4, None, None, '2', '4', None, '2'],)))
        basic_info[('klitze', 'kleine')].should.be.equal(self.convert(([['klitze', 'kleine'], 'klitz++klein', 2, 2, None, None, '[2, 2]', '[4, 4]', None, '2'],)))
        basic_info[('.', )].should.be.equal(self.convert(([['.'], '.', 1, 2, '2', '2', None, None, '2', None],)))
        len(basic_info).should.be.equal(4)
        right_sum_repl = {'.': {3: [
                   2, {'.^3': 2}]}}
        right_sum_redu = {'kleine': {2: 2}, 'klitze': {2: 2}}
        extracted_repl = {word:{nr_rep:[occur[0], {rle:count for rle, count in occur[1].items()}] for nr_rep, occur in data.items()} for word, data in stats.compute_rep_sum('*', 'repl').items()}
        extracted_redu = {word:{nr_rep:occur for nr_rep, occur in data.items()} for word, data in stats.compute_rep_sum('*', 'redu').items()}
        extracted_repl.should.be.equal(right_sum_repl)
        extracted_redu.should.be.equal(right_sum_redu)
        case_sensitiv_stat = True
        stats = Stats(mode=self.mode)
        stats.init(self.tempdir_project_folder, name, language, visibility, version=version, full_repetativ_syntagma=True, case_sensitiv=case_sensitiv_stat, baseline_delimiter='++')
        stats.compute(corp)
        basic_info = self._get_basic_info_about_reps(stats.get_data(redu=True, repl=True, baseline=True))
        basic_info[('.', )].should.be.equal(self.convert(([['.'], '.', 1, 2, '2', '2', None, None, '2', None],)))
        basic_info[('kleine', )].should.be.equal(self.convert(([['kleine'], 'klein', 1, 4, None, None, '2', '4', None, '2'],)))
        len(basic_info).should.be.equal(2)
        case_sensitiv_stat = False
        stats = Stats(mode=self.mode)
        stats.init(self.tempdir_project_folder, name, language, visibility, version=version, full_repetativ_syntagma=False, case_sensitiv=case_sensitiv_stat, baseline_delimiter='++')
        stats.compute(corp)
        basic_info = self._get_basic_info_about_reps(stats.get_data(redu=True, repl=True, baseline=True))
        basic_info[('klitze', )].should.be.equal(self.convert(([['klitze'], 'klitz', 1, 4, None, None, '2', '4', None, '2'],)))
        basic_info[('kleine', )].should.be.equal(self.convert(([['kleine'], 'klein', 1, 4, None, None, '2', '4', None, '2'],)))
        basic_info[('klitze', 'kleine')].should.be.equal(self.convert(([['klitze', 'kleine'], 'klitz++klein', 2, 2, None, None, '[2, 2]', '[4, 4]', None, None],)))
        basic_info[('.', )].should.be.equal(self.convert(([['.'], '.', 1, 2, '2', '2', None, None, '2', None],)))
        basic_info[('kleine', 'menge', '.')].should.be.equal(self.convert(([['kleine', 'menge', '.'], 'klein++meng++.', 3, 2, '[0, 0, 2]', '[0, 0, 2]', '[2, 0, 0]', '[4, 0, 0]', None, None],)))
        basic_info[('klitze', 'kleine', 'menge', '.')].should.be.equal(self.convert(([['klitze', 'kleine', 'menge', '.'], 'klitz++klein++meng++.', 4, 2, '[0, 0, 0, 2]', '[0, 0, 0, 2]', '[2, 2, 0, 0]', '[4, 4, 0, 0]', None, None],)))
        basic_info[('klitze', 'kleine', 'menge')].should.be.equal(self.convert(([['klitze', 'kleine', 'menge'], 'klitz++klein++meng', 3, 2, None, None, '[2, 2, 0]', '[4, 4, 0]', None, None],)))
        basic_info[('kleine', 'menge')].should.be.equal(self.convert(([['kleine', 'menge'], 'klein++meng', 2, 2, None, None, '[2, 0]', '[4, 0]', None, None],)))
        basic_info[('menge', '.')].should.be.equal(self.convert(([['menge', '.'], 'meng++.', 2, 2, '[0, 2]', '[0, 2]', None, None, None, None],)))
        len(basic_info).should.be.equal(9)
        return

    @attr(status='stable')
    def test_work_flow_with_white_trash_and_ignore_option_501(self):
        self.prj_folder()
        self.input_list = [
         {'rowid': '1', 
            'star_constellation': 'Capricorn', 
            'text': '@buuuussy_guyyyy @buuuussy_guyyyy ...... #hhhaaaavy #hhhaaaavy www.trash.de http://trash.de', 
            'working_area': 'IT Consulting', 
            'age': '46', 
            'id': '324114', 
            'gender': 'female'},
         {'rowid': '2', 
            'star_constellation': 'Fish', 
            'text': '@buuuussy_guyyyy @buuuussy_guyyyy ...... #hhhaaaavy #hhhaaaavy www.trash.de http://trash.de', 
            'working_area': 'IT Developing', 
            'age': '23', 
            'id': '8765', 
            'gender': 'male'}]
        name = 'test_corp'
        language = 'de'
        visibility = 'intern'
        platform_name = 'blogger'
        source = 'test'
        license = 'test'
        template_name = 'blogger'
        version = 1
        corp_typ = 'corpus'
        preprocession = True
        tokenizer = True
        pos_tagger = False
        sent_splitter = True
        sentiment_analyzer = True
        lang_classification = False
        del_url = False
        del_punkt = False
        del_num = False
        del_html = False
        del_mention = False
        del_hashtag = False
        case_sensitiv = True
        corp = Corpus(logger_level=logging.DEBUG, mode=self.mode)
        corp.init(self.tempdir_project_folder, name, language, visibility, platform_name, source=source, license=license, template_name=template_name, version=version, preprocession=preprocession, tokenizer=tokenizer, pos_tagger=pos_tagger, sent_splitter=sent_splitter, sentiment_analyzer=sentiment_analyzer, lang_classification=lang_classification, del_url=del_url, del_punkt=del_punkt, del_num=del_num, del_html=del_html, del_mention=del_mention, del_hashtag=del_hashtag, case_sensitiv=case_sensitiv)
        corp.insert(self.input_list)
        list(corp.docs(columns='text'))[0].should.be.equal(('[[[["@buuuussy_guyyyy", "mention"], ["@buuuussy_guyyyy", "mention"], ["......", "symbol"], ["#hhhaaaavy", "hashtag"], ["#hhhaaaavy", "hashtag"], ["www.trash.de", "URL"], ["http://trash.de", "URL"]], ["neutral", 0.0]]]', ))
        list(corp.docs(columns='text'))[1].should.be.equal(('[[[["@buuuussy_guyyyy", "mention"], ["@buuuussy_guyyyy", "mention"], ["......", "symbol"], ["#hhhaaaavy", "hashtag"], ["#hhhaaaavy", "hashtag"], ["www.trash.de", "URL"], ["http://trash.de", "URL"]], ["neutral", 0.0]]]', ))
        corp.corpdb.get_attr('token_num').should.be.equal(14)
        corp.corpdb.get_attr('doc_num').should.be.equal(2)
        corp.corpdb.get_attr('sent_num').should.be.equal(2)
        case_sensitiv_stat = True
        ignore_hashtag = False
        ignore_url = False
        ignore_mention = False
        ignore_punkt = False
        ignore_num = False
        stats = Stats(mode=self.mode)
        stats.init(self.tempdir_project_folder, name, language, visibility, version=version, baseline_delimiter='++', full_repetativ_syntagma=True, case_sensitiv=case_sensitiv_stat, ignore_hashtag=ignore_hashtag, ignore_url=ignore_url, ignore_mention=ignore_mention, ignore_punkt=ignore_punkt, ignore_num=ignore_num)
        stats.compute(corp)
        basic_info = self._get_basic_info_about_reps(stats.get_data(redu=True, repl=True, baseline=True))
        basic_info[('.', )].should.be.equal(self.convert(([['.'], '.', 1, 2, '2', '2', None, None, '2', None],)))
        basic_info[('.', '#havy')].should.be.equal(self.convert(([['.', '#havy'], '.++#havy', 2, 2, '[2, 4]', '[2, 8]', None, None, '2', None],)))
        basic_info[('@busy_guy', '.', '#havy')].should.be.equal(self.convert(([['@busy_guy', '.', '#havy'], '@busy_guy++.++#havy', 3, 2, '[4, 2, 4]', '[8, 2, 8]', None, None, '2', None],)))
        basic_info[('@busy_guy', '.')].should.be.equal(self.convert(([['@busy_guy', '.'], '@busy_guy++.', 2, 2, '[4, 2]', '[8, 2]', None, None, '2', None],)))
        basic_info[('@busy_guy', )].should.be.equal(self.convert(([['@busy_guy'], '@busy_guy', 1, 4, '4', '8', '2', '4', '4', '2'],)))
        basic_info[('#havy', )].should.be.equal(self.convert(([['#havy'], '#havy', 1, 4, '4', '8', '2', '4', '4', '2'],)))
        len(basic_info).should.be.equal(6)
        case_sensitiv_stat = False
        ignore_hashtag = True
        ignore_url = True
        ignore_mention = True
        ignore_punkt = True
        ignore_num = True
        stats = Stats(mode=self.mode)
        stats.init(self.tempdir_project_folder, name, language, visibility, version=version, baseline_delimiter='++', full_repetativ_syntagma=True, case_sensitiv=case_sensitiv_stat, ignore_hashtag=ignore_hashtag, ignore_url=ignore_url, ignore_mention=ignore_mention, ignore_punkt=ignore_punkt, ignore_num=ignore_num)
        stats.compute(corp)
        basic_info = self._get_basic_info_about_reps(stats.get_data(redu=True, repl=True, baseline=True))
        basic_info[(':hashtag:', ':URL:')].should.be.equal(self.convert(([[':hashtag:', ':URL:'], ':hashtag:++:uRL:', 2, 2, None, None, '[2, 2]', '[4, 4]', None, '2'],)))
        basic_info[(':URL:', )].should.be.equal(self.convert(([[':URL:'], ':uRL:', 1, 4, None, None, '2', '4', None, '2'],)))
        basic_info[(':mention:', )].should.be.equal(self.convert(([[':mention:'], ':mention:', 1, 4, None, None, '2', '4', None, '2'],)))
        basic_info[(':hashtag:', )].should.be.equal(self.convert(([[':hashtag:'], ':hashtag:', 1, 4, None, None, '2', '4', None, '2'],)))
        len(basic_info).should.be.equal(4)
        return

    @attr(status='stable')
    def test_work_flow_with_EMOIMG_EMOASC_502(self):
        self.prj_folder()
        self.input_list = [
         {'rowid': '1', 
            'star_constellation': 'Capricorn', 
            'text': '-))))) -))))))))) 😀😀😀😀😀😀 🌈🌈🌈🌈 \U0001f9d1🏻\U0001f9d1🏻\U0001f9d1🏻\U0001f9d1🏻\U0001f9d1🏻 💁🏿\u200d♀️💁🏿\u200d♀️💁🏿\u200d♀️💁🏿\u200d♀️💁🏿\u200d♀️ 🇧🇭🇧🇭🇧🇭🇧🇭', 
            'working_area': 'IT Consulting', 
            'age': '46', 
            'id': '324114', 
            'gender': 'female'},
         {'rowid': '2', 
            'star_constellation': 'Capricorn', 
            'text': '-))))) -))))))))) 😀😀😀😀😀😀 🌈🌈🌈🌈 \U0001f9d1🏻\U0001f9d1🏻\U0001f9d1🏻\U0001f9d1🏻\U0001f9d1🏻 💁🏿\u200d♀️💁🏿\u200d♀️💁🏿\u200d♀️💁🏿\u200d♀️💁🏿\u200d♀️ 🇧🇭🇧🇭🇧🇭🇧🇭', 
            'working_area': 'IT Support', 
            'age': '24', 
            'id': '3241436543', 
            'gender': 'male'}]
        name = 'test_corp'
        language = 'de'
        visibility = 'intern'
        platform_name = 'blogger'
        source = 'test'
        license = 'test'
        template_name = 'blogger'
        version = 1
        corp_typ = 'corpus'
        preprocession = True
        tokenizer = True
        pos_tagger = False
        sent_splitter = True
        sentiment_analyzer = True
        lang_classification = False
        del_url = False
        del_punkt = False
        del_num = False
        del_html = False
        del_mention = False
        del_hashtag = False
        case_sensitiv = False
        corp = Corpus(logger_level=logging.DEBUG, mode=self.mode, status_bar=True)
        corp.init(self.tempdir_project_folder, name, language, visibility, platform_name, source=source, license=license, template_name=template_name, version=version, preprocession=preprocession, tokenizer=tokenizer, pos_tagger=pos_tagger, sent_splitter=sent_splitter, sentiment_analyzer=sentiment_analyzer, lang_classification=lang_classification, del_url=del_url, del_punkt=del_punkt, del_num=del_num, del_html=del_html, del_mention=del_mention, del_hashtag=del_hashtag, case_sensitiv=case_sensitiv)
        corp.insert(self.input_list)
        list(corp.docs(columns='text'))[0].should.be.equal(('[[[["-)))))", "EMOASC"], ["-)))))))))", "EMOASC"], ["\\ud83d\\ude00\\ud83d\\ude00\\ud83d\\ude00\\ud83d\\ude00\\ud83d\\ude00\\ud83d\\ude00", "EMOIMG"], ["\\ud83c\\udf08\\ud83c\\udf08\\ud83c\\udf08\\ud83c\\udf08", "EMOIMG"], ["\\ud83e\\uddd1", "EMOIMG"], ["\\ud83c\\udffb", "EMOIMG"], ["\\ud83e\\uddd1", "EMOIMG"], ["\\ud83c\\udffb", "EMOIMG"], ["\\ud83e\\uddd1", "EMOIMG"], ["\\ud83c\\udffb", "EMOIMG"], ["\\ud83e\\uddd1", "EMOIMG"], ["\\ud83c\\udffb", "EMOIMG"], ["\\ud83e\\uddd1", "EMOIMG"], ["\\ud83c\\udffb", "EMOIMG"], ["\\ud83d\\udc81", "EMOIMG"], ["\\ud83c\\udfff", "EMOIMG"], ["\\u2640", "EMOIMG"], ["\\ufe0f", "EMOIMG"], ["\\ud83d\\udc81", "EMOIMG"], ["\\ud83c\\udfff", "EMOIMG"], ["\\u2640", "EMOIMG"], ["\\ufe0f", "EMOIMG"], ["\\ud83d\\udc81", "EMOIMG"], ["\\ud83c\\udfff", "EMOIMG"], ["\\u2640", "EMOIMG"], ["\\ufe0f", "EMOIMG"], ["\\ud83d\\udc81", "EMOIMG"], ["\\ud83c\\udfff", "EMOIMG"], ["\\u2640", "EMOIMG"], ["\\ufe0f", "EMOIMG"], ["\\ud83d\\udc81", "EMOIMG"], ["\\ud83c\\udfff", "EMOIMG"], ["\\u2640", "EMOIMG"], ["\\ufe0f", "EMOIMG"], ["\\ud83c\\udde7\\ud83c\\udded\\ud83c\\udde7\\ud83c\\udded\\ud83c\\udde7\\ud83c\\udded\\ud83c\\udde7\\ud83c\\udded", "regular"]], ["neutral", 0.0]]]', ))
        list(corp.docs(columns='text'))[1].should.be.equal(('[[[["-)))))", "EMOASC"], ["-)))))))))", "EMOASC"], ["\\ud83d\\ude00\\ud83d\\ude00\\ud83d\\ude00\\ud83d\\ude00\\ud83d\\ude00\\ud83d\\ude00", "EMOIMG"], ["\\ud83c\\udf08\\ud83c\\udf08\\ud83c\\udf08\\ud83c\\udf08", "EMOIMG"], ["\\ud83e\\uddd1", "EMOIMG"], ["\\ud83c\\udffb", "EMOIMG"], ["\\ud83e\\uddd1", "EMOIMG"], ["\\ud83c\\udffb", "EMOIMG"], ["\\ud83e\\uddd1", "EMOIMG"], ["\\ud83c\\udffb", "EMOIMG"], ["\\ud83e\\uddd1", "EMOIMG"], ["\\ud83c\\udffb", "EMOIMG"], ["\\ud83e\\uddd1", "EMOIMG"], ["\\ud83c\\udffb", "EMOIMG"], ["\\ud83d\\udc81", "EMOIMG"], ["\\ud83c\\udfff", "EMOIMG"], ["\\u2640", "EMOIMG"], ["\\ufe0f", "EMOIMG"], ["\\ud83d\\udc81", "EMOIMG"], ["\\ud83c\\udfff", "EMOIMG"], ["\\u2640", "EMOIMG"], ["\\ufe0f", "EMOIMG"], ["\\ud83d\\udc81", "EMOIMG"], ["\\ud83c\\udfff", "EMOIMG"], ["\\u2640", "EMOIMG"], ["\\ufe0f", "EMOIMG"], ["\\ud83d\\udc81", "EMOIMG"], ["\\ud83c\\udfff", "EMOIMG"], ["\\u2640", "EMOIMG"], ["\\ufe0f", "EMOIMG"], ["\\ud83d\\udc81", "EMOIMG"], ["\\ud83c\\udfff", "EMOIMG"], ["\\u2640", "EMOIMG"], ["\\ufe0f", "EMOIMG"], ["\\ud83c\\udde7\\ud83c\\udded\\ud83c\\udde7\\ud83c\\udded\\ud83c\\udde7\\ud83c\\udded\\ud83c\\udde7\\ud83c\\udded", "regular"]], ["neutral", 0.0]]]', ))
        corp.corpdb.get_attr('token_num').should.be.equal(70)
        corp.corpdb.get_attr('doc_num').should.be.equal(2)
        corp.corpdb.get_attr('sent_num').should.be.equal(2)
        case_sensitiv_stat = False
        ignore_hashtag = False
        ignore_url = False
        ignore_mention = False
        ignore_punkt = False
        ignore_num = False
        stats = Stats(mode=self.mode)
        stats.init(self.tempdir_project_folder, name, language, visibility, version=version, baseline_delimiter='++', full_repetativ_syntagma=True, case_sensitiv=case_sensitiv_stat, ignore_hashtag=ignore_hashtag, ignore_url=ignore_url, ignore_mention=ignore_mention, ignore_punkt=ignore_punkt, ignore_num=ignore_num)
        stats.compute(corp)
        basic_info = self._get_basic_info_about_reps(stats.get_data(redu=True, repl=True, baseline=True))
        basic_info[('-)', '😀')].should.be.equal(self.convert(([['-)', '😀'], '-)++😀', 2, 2, '[4, 2]', '[4, 2]', None, None, '2', None],)))
        basic_info[('😀', )].should.be.equal(self.convert(([['😀'], '😀', 1, 2, '2', '2', None, None, '2', None],)))
        basic_info[('-)', )].should.be.equal(self.convert(([['-)'], '-)', 1, 4, '4', '4', '2', '4', '4', '2'],)))
        basic_info[('🌈', )].should.be.equal(self.convert(([['🌈'], '🌈', 1, 2, '2', '2', None, None, '2', None],)))
        basic_info[('😀', '🌈')].should.be.equal(self.convert(([['😀', '🌈'], '😀++🌈', 2, 2, '[2, 2]', '[2, 2]', None, None, '2', None],)))
        basic_info[('-)', '😀', '🌈')].should.be.equal(self.convert(([['-)', '😀', '🌈'], '-)++😀++🌈', 3, 2, '[4, 2, 2]', '[4, 2, 2]', None, None, '2', None],)))
        len(basic_info).should.be.equal(6)
        basic_info = self._get_basic_info_about_reps(stats.get_data(inp_syntagma=['EMOIMG'], redu=True, repl=True, baseline=True, syntagma_type='pos', if_type_pos_return_lexem_syn=True))
        basic_info[('😀', )].should.be.equal(self.convert([[['😀'], '😀', 1, 2, '2', '2', None, None, '2', None]]))
        basic_info[('🌈', )].should.be.equal(self.convert([[['🌈'], '🌈', 1, 2, '2', '2', None, None, '2', None]]))
        len(basic_info).should.be.equal(2)
        basic_info = self._get_basic_info_about_reps(stats.get_data(inp_syntagma=['EMOASC'], redu=True, repl=True, baseline=True, syntagma_type='pos', if_type_pos_return_lexem_syn=True))
        basic_info[('-)', )].should.be.equal(self.convert([[['-)'], '-)', 1, 4, '4', '4', '2', '4', '4', '2']]))
        len(basic_info).should.be.equal(1)
        right_sum_repl = {')': {9: [
                   2, {'-)^9': 2}], 
                 5: [
                   2, {'-)^5': 2}]}, 
           '😀': {6: [
                   2, {'😀^6': 2}]}, 
           '🌈': {4: [
                   2, {'🌈^4': 2}]}}
        right_sum_redu = {'-)': {2: 2}}
        extracted_repl = {word:{nr_rep:[occur[0], {rle:count for rle, count in occur[1].items()}] for nr_rep, occur in data.items()} for word, data in stats.compute_rep_sum('*', 'repl').items()}
        extracted_redu = {word:{nr_rep:occur for nr_rep, occur in data.items()} for word, data in stats.compute_rep_sum('*', 'redu').items()}
        extracted_repl.should.be.equal(right_sum_repl)
        extracted_redu.should.be.equal(right_sum_redu)
        return