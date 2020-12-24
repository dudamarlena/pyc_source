# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/egoruni/Desktop/BA/Code/zas-rep-tools/zas_rep_tools/tests/test_zas_rep_tools_rle.py
# Compiled at: 2018-10-15 23:12:48
import unittest, os, logging, sure, copy
from nose.plugins.attrib import attr
from testfixtures import tempdir, TempDirectory
from distutils.dir_util import copy_tree
from zas_rep_tools.src.classes.stats import Stats
from zas_rep_tools.src.classes.corpus import Corpus
from zas_rep_tools.src.utils.debugger import p, wipd, wipdn, wipdl, wipdo
from zas_rep_tools.src.utils.basetester import BaseTester
from zas_rep_tools.src.utils.helpers import Rle
import platform
if platform.uname()[0].lower() != 'windows':
    import colored_traceback
    colored_traceback.add_hook()
else:
    import colorama

class TestZASHelpersRLE(BaseTester, unittest.TestCase):
    _multiprocess_shared_ = True

    def setUp(self):
        super(type(self), self).setUp()
        self.test_byte_str1_decoded = 'biggggggggg fatttttttt pooooonnnnnnnyyyyyyyyyyy..... Or how to beeeeee haaaaapppy!!!!!'
        self.test_byte_str2_decoded = 'So beautiful life 😀😀😀😀😀😀😀😀😜😜😜😜😜😜 😇😇😇😇😇'
        self.test_byte_str3_decoded = 'mit Üüüüüüüberzeugung hat er aaaallllles gestäääämt!!!'
        self.test_byte_str4_decoded = 'нууууу как бы мооооооооооожно лиииииии????'
        self.test_unicode_str1_decoded = 'biggggggggg fatttttttt pooooonnnnnnnyyyyyyyyyyy..... Or how to beeeeee haaaaapppy!!!!!'
        self.test_unicode_str2_decoded = 'So beautiful life 😀😀😀😀😀😀😀😀😜😜😜😜😜😜 😇😇😇😇😇'
        self.test_unicode_str3_decoded = 'mit Üüüüüüüberzeugung hat er aaaallllles gestäääämt!!!'
        self.test_unicode_str4_decoded = 'нууууу как бы мооооооооооожно лиииииии????'
        self.test_byte_str1_repfree = 'big fat pony. Or how to be hapy!'
        self.test_byte_str2_repfree = 'So beautiful life 😀😜 😇'
        self.test_byte_str3_repfree = 'mit Üüberzeugung hat er ales gestämt!'
        self.test_byte_str4_repfree = 'ну как бы можно ли?'
        self.test_byte_str1_encoded_to_tuples = [
         (
          'b', 1), ('i', 1), ('g', 9), (' ', 1), ('f', 1), ('a', 1), ('t', 8), (' ', 1), ('p', 1), ('o', 5), ('n', 7), ('y', 11), ('.', 5), (' ', 1), ('O', 1), ('r', 1), (' ', 1), ('h', 1), ('o', 1), ('w', 1), (' ', 1), ('t', 1), ('o', 1), (' ', 1), ('b', 1), ('e', 6), (' ', 1), ('h', 1), ('a', 5), ('p', 3), ('y', 1), ('!', 5)]
        self.test_byte_str2_encoded_to_tuples = [('S', 1), ('o', 1), (' ', 1), ('b', 1), ('e', 1), ('a', 1), ('u', 1), ('t', 1), ('i', 1), ('f', 1), ('u', 1), ('l', 1), (' ', 1), ('l', 1), ('i', 1), ('f', 1), ('e', 1), (' ', 1), ('😀', 8), ('😜', 6), (' ', 1), ('😇', 5)]
        self.test_byte_str3_encoded_to_tuples = [('m', 1), ('i', 1), ('t', 1), (' ', 1), ('Ü', 1), ('ü', 6), ('b', 1), ('e', 1), ('r', 1), ('z', 1), ('e', 1), ('u', 1), ('g', 1), ('u', 1), ('n', 1), ('g', 1), (' ', 1), ('h', 1), ('a', 1), ('t', 1), (' ', 1), ('e', 1), ('r', 1), (' ', 1), ('a', 4), ('l', 5), ('e', 1), ('s', 1), (' ', 1), ('g', 1), ('e', 1), ('s', 1), ('t', 1), ('ä', 4), ('m', 1), ('t', 1), ('!', 3)]
        self.test_byte_str4_encoded_to_tuples = [('н', 1), ('у', 5), (' ', 1), ('к', 1), ('а', 1), ('к', 1), (' ', 1), ('б', 1), ('ы', 1), (' ', 1), ('м', 1), ('о', 11), ('ж', 1), ('н', 1), ('о', 1), (' ', 1), ('л', 1), ('и', 7), ('?', 4)]
        self.test_byte_str1_encoded_to_str = 'b1i1g9 1f1a1t8 1p1o5n7y11.5 1O1r1 1h1o1w1 1t1o1 1b1e6 1h1a5p3y1!5'
        self.test_byte_str2_encoded_to_str = 'S1o1 1b1e1a1u1t1i1f1u1l1 1l1i1f1e1 1😀8😜6 1😇5'
        self.test_byte_str3_encoded_to_str = 'm1i1t1 1Ü1ü6b1e1r1z1e1u1g1u1n1g1 1h1a1t1 1e1r1 1a4l5e1s1 1g1e1s1t1ä4m1t1!3'
        self.test_byte_str4_encoded_to_str = 'н1у5 1к1а1к1 1б1ы1 1м1о11ж1н1о1 1л1и7?4'
        self.test_byte_sent1_decoded = [
         'big', 'big', 'big', 'big', 'fat', 'pony', 'pony']
        self.test_byte_sent2_decoded = ['😀', '😀', '😀', '😀', '😀', '😍']
        self.test_byte_sent1_decoded_to_str = 'big big big big fat pony pony'
        self.test_byte_sent2_decoded_to_str = '😀 😀 😀 😀 😀 😍'
        self.test_byte_sent1_encoded = [
         (
          'big', 4), ('fat', 1), ('pony', 2)]
        self.test_byte_sent2_encoded = [('😀', 5), ('😍', 1)]
        self.test_byte_sent1_encoded_mapping = [
         0, 4, 5]
        self.test_byte_sent2_encoded_mapping = [0, 5]
        self.test_byte_sent1_repfree = 'big fat pony'
        self.test_byte_sent2_repfree = '😀 😍'

    def tearDown(self):
        super(type(self), self).tearDown()

    @attr(status='stable')
    def test_rle_initialization_000(self):
        rle = Rle()

    @attr(status='stable')
    def test_del_rep_from_byte_str_500(self):
        rle = Rle()
        rle.del_rep(self.test_byte_str1_decoded).encode('utf-8').should.be.equal(self.test_byte_str1_repfree)
        rle.del_rep(self.test_byte_str2_decoded).encode('utf-8').should.be.equal(self.test_byte_str2_repfree)
        rle.del_rep(self.test_byte_str3_decoded).encode('utf-8').should.be.equal(self.test_byte_str3_repfree)
        rle.del_rep(self.test_byte_str4_decoded).encode('utf-8').should.be.equal(self.test_byte_str4_repfree)

    @attr(status='stable')
    def test_del_rep_from_unicode_str_501(self):
        rle = Rle()
        rle.del_rep(self.test_unicode_str1_decoded).encode('utf-8').should.be.equal(self.test_byte_str1_repfree)
        rle.del_rep(self.test_unicode_str2_decoded).encode('utf-8').should.be.equal(self.test_byte_str2_repfree)
        rle.del_rep(self.test_unicode_str3_decoded).encode('utf-8').should.be.equal(self.test_byte_str3_repfree)
        rle.del_rep(self.test_unicode_str4_decoded).encode('utf-8').should.be.equal(self.test_byte_str4_repfree)

    @attr(status='stable')
    def test_del_rep_from_list_with_words_502(self):
        rle = Rle()
        rle.del_rep_from_sent(self.test_byte_sent1_decoded).encode('utf-8').should.be.equal(self.test_byte_sent1_repfree)
        rle.del_rep_from_sent(self.test_byte_sent2_decoded).encode('utf-8').should.be.equal(self.test_byte_sent2_repfree)

    @attr(status='stable')
    def test_encode_rle_of_words_to_tuples_as_byte_str_503_1(self):
        rle = Rle()
        rle.encode_to_tuples(self.test_byte_str1_decoded).should.be.equal(self.test_byte_str1_encoded_to_tuples)
        rle.encode_to_tuples(self.test_byte_str2_decoded).should.be.equal(self.test_byte_str2_encoded_to_tuples)
        rle.encode_to_tuples(self.test_byte_str3_decoded).should.be.equal(self.test_byte_str3_encoded_to_tuples)
        rle.encode_to_tuples(self.test_byte_str4_decoded).should.be.equal(self.test_byte_str4_encoded_to_tuples)

    @attr(status='stable')
    def test_encode_rle_of_words_to_tuples_with_additional_start_index_as_byte_str_503_2(self):
        rle = Rle()
        rle.encode_to_tuples(self.test_byte_str1_decoded, mapping=True).should.be.equal(([('b', 1), ('i', 1), ('g', 9), (' ', 1), ('f', 1), ('a', 1), ('t', 8), (' ', 1), ('p', 1), ('o', 5), ('n', 7), ('y', 11), ('.', 5), (' ', 1), ('O', 1), ('r', 1), (' ', 1), ('h', 1), ('o', 1), ('w', 1), (' ', 1), ('t', 1), ('o', 1), (' ', 1), ('b', 1), ('e', 6), (' ', 1), ('h', 1), ('a', 5), ('p', 3), ('y', 1), ('!', 5)], [0, 1, 2, 11, 12, 13, 14, 22, 23, 24, 29, 36, 47, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 70, 71, 72, 77, 80, 81]))
        rle.encode_to_tuples(self.test_byte_str2_decoded, mapping=True).should.be.equal(([('S', 1), ('o', 1), (' ', 1), ('b', 1), ('e', 1), ('a', 1), ('u', 1), ('t', 1), ('i', 1), ('f', 1), ('u', 1), ('l', 1), (' ', 1), ('l', 1), ('i', 1), ('f', 1), ('e', 1), (' ', 1), ('😀', 8), ('😜', 6), (' ', 1), ('😇', 5)], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 26, 32, 33]))
        rle.encode_to_tuples(self.test_byte_str3_decoded, mapping=True).should.be.equal(([('m', 1), ('i', 1), ('t', 1), (' ', 1), ('Ü', 1), ('ü', 6), ('b', 1), ('e', 1), ('r', 1), ('z', 1), ('e', 1), ('u', 1), ('g', 1), ('u', 1), ('n', 1), ('g', 1), (' ', 1), ('h', 1), ('a', 1), ('t', 1), (' ', 1), ('e', 1), ('r', 1), (' ', 1), ('a', 4), ('l', 5), ('e', 1), ('s', 1), (' ', 1), ('g', 1), ('e', 1), ('s', 1), ('t', 1), ('ä', 4), ('m', 1), ('t', 1), ('!', 3)], [0, 1, 2, 3, 4, 5, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 33, 38, 39, 40, 41, 42, 43, 44, 45, 49, 50, 51]))
        rle.encode_to_tuples(self.test_byte_str4_decoded, mapping=True).should.be.equal(([('н', 1), ('у', 5), (' ', 1), ('к', 1), ('а', 1), ('к', 1), (' ', 1), ('б', 1), ('ы', 1), (' ', 1), ('м', 1), ('о', 11), ('ж', 1), ('н', 1), ('о', 1), (' ', 1), ('л', 1), ('и', 7), ('?', 4)], [0, 1, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 26, 27, 28, 29, 30, 31, 38]))

    @attr(status='stable')
    def test_encode_sent_to_tuples_504_1(self):
        rle = Rle()
        rle.encode_to_tuples(self.test_byte_sent1_decoded).should.be.equal(self.test_byte_sent1_encoded)
        rle.encode_to_tuples(self.test_byte_sent2_decoded).should.be.equal(self.test_byte_sent2_encoded)

    @attr(status='stable')
    def test_encode_sent_to_tuples_504_2(self):
        rle = Rle()
        rle.encode_to_tuples(self.test_byte_sent1_decoded, mapping=True).should.be.equal((self.test_byte_sent1_encoded, self.test_byte_sent1_encoded_mapping))
        rle.encode_to_tuples(self.test_byte_sent2_decoded, mapping=True).should.be.equal((self.test_byte_sent2_encoded, self.test_byte_sent2_encoded_mapping))

    @attr(status='stable')
    def test_decode_list_of_words_in_tuples_to_list_506(self):
        rle = Rle()
        rle.decode_words_to_list(self.test_byte_sent1_encoded).should.be.equal(self.test_byte_sent1_decoded)
        rle.decode_words_to_list(self.test_byte_sent2_encoded).should.be.equal(self.test_byte_sent2_decoded)

    @attr(status='stable')
    def test_decode_letters_to_str_507(self):
        rle = Rle()
        rle.decode_letters_to_str(self.test_byte_str1_encoded_to_tuples).encode('utf-8').should.be.equal(self.test_byte_str1_decoded)
        rle.decode_letters_to_str(self.test_byte_str2_encoded_to_tuples).encode('utf-8').should.be.equal(self.test_byte_str2_decoded)
        rle.decode_letters_to_str(self.test_byte_str3_encoded_to_tuples).encode('utf-8').should.be.equal(self.test_byte_str3_decoded)
        rle.decode_letters_to_str(self.test_byte_str4_encoded_to_tuples).encode('utf-8').should.be.equal(self.test_byte_str4_decoded)

    @attr(status='stable')
    def test_decode_words_to_str_508(self):
        rle = Rle()
        rle.decode_words_to_str(self.test_byte_sent1_encoded).should.be.equal(self.test_byte_sent1_decoded_to_str)
        rle.decode_words_to_str(self.test_byte_sent2_encoded).should.be.equal(self.test_byte_sent2_decoded_to_str)

    @attr(status='stable')
    def test_encode_str_to_str_509(self):
        rle = Rle()
        rle.encode_str_to_str(self.test_byte_str1_decoded).encode('utf-8').should.be.equal(self.test_byte_str1_encoded_to_str)
        rle.encode_str_to_str(self.test_byte_str2_decoded).encode('utf-8').should.be.equal(self.test_byte_str2_encoded_to_str)
        rle.encode_str_to_str(self.test_byte_str3_decoded).encode('utf-8').should.be.equal(self.test_byte_str3_encoded_to_str)
        rle.encode_str_to_str(self.test_byte_str4_decoded).encode('utf-8').should.be.equal(self.test_byte_str4_encoded_to_str)

    @attr(status='stable')
    def test_decode_str_from_str_510(self):
        rle = Rle()
        rle.decode_str_from_str(self.test_byte_str1_encoded_to_str).should.be.equal(self.test_byte_str1_decoded)
        rle.decode_str_from_str(self.test_byte_str2_encoded_to_str).should.be.equal(self.test_byte_str2_decoded)
        rle.decode_str_from_str(self.test_byte_str3_encoded_to_str).should.be.equal(self.test_byte_str3_decoded)
        rle.decode_str_from_str(self.test_byte_str4_encoded_to_str).should.be.equal(self.test_byte_str4_decoded)

    @attr(status='stable')
    def test_get_rep_free_word_from_rle_as_tuples_as_bytestr_511(self):
        rle = Rle()
        rle.get_rep_free_word_from_rle_in_tuples(self.test_byte_str1_encoded_to_tuples).should.be.equal('big fat pony. Or how to be hapy!')
        rle.get_rep_free_word_from_rle_in_tuples(self.test_byte_str2_encoded_to_tuples).should.be.equal('So beautiful life 😀😜 😇')
        rle.get_rep_free_word_from_rle_in_tuples(self.test_byte_str3_encoded_to_tuples).should.be.equal('mit Üüberzeugung hat er ales gestämt!')
        rle.get_rep_free_word_from_rle_in_tuples(self.test_byte_str4_encoded_to_tuples).should.be.equal('ну как бы можно ли?')

    @attr(status='stable')
    def test_encode_rle_of_sent_to_tuples_512(self):
        rle = Rle()
        rle.get_rep_free_sent_from_rle_in_tuples(self.test_byte_sent1_encoded).should.be.equal('big fat pony')
        rle.get_rep_free_sent_from_rle_in_tuples(self.test_byte_sent2_encoded).should.be.equal('😀 😍')

    @attr(status='stable')
    def test_get_repetativ_elems_513(self):
        rle = Rle()
        rle.get_repetativ_elems(self.test_byte_str1_encoded_to_tuples).should.be.equal([('g', 9, 2), ('t', 8, 6), ('o', 5, 9), ('n', 7, 10), ('y', 11, 11), ('.', 5, 12), ('e', 6, 25), ('a', 5, 28), ('p', 3, 29), ('!', 5, 31)])
        rle.get_repetativ_elems(self.test_byte_str2_encoded_to_tuples).should.be.equal([('😀', 8, 18), ('😜', 6, 19), ('😇', 5, 21)])
        rle.get_repetativ_elems(self.test_byte_str3_encoded_to_tuples).should.be.equal([('ü', 6, 5), ('a', 4, 24), ('l', 5, 25), ('ä', 4, 33), ('!', 3, 36)])
        rle.get_repetativ_elems(self.test_byte_str4_encoded_to_tuples).should.be.equal([('у', 5, 1), ('о', 11, 11), ('и', 7, 17), ('?', 4, 18)])

    @attr(status='stable')
    def test_rep_extraction_word_without_rle_514(self):
        rle = Rle()
        rle.rep_extraction_word(self.test_byte_str1_encoded_to_tuples).should.be.equal(([('g', 9, 2), ('t', 8, 6), ('o', 5, 9), ('n', 7, 10), ('y', 11, 11), ('.', 5, 12), ('e', 6, 25), ('a', 5, 28), ('p', 3, 29), ('!', 5, 31)], 'big fat pony. Or how to be hapy!'))
        rle.rep_extraction_word(self.test_byte_str2_encoded_to_tuples).should.be.equal(([('😀', 8, 18), ('😜', 6, 19), ('😇', 5, 21)], 'So beautiful life 😀😜 😇'))
        rle.rep_extraction_word(self.test_byte_str3_encoded_to_tuples).should.be.equal(([('ü', 6, 5), ('a', 4, 24), ('l', 5, 25), ('ä', 4, 33), ('!', 3, 36)], 'mit Üüberzeugung hat er ales gestämt!'))
        rle.rep_extraction_word(self.test_byte_str4_encoded_to_tuples).should.be.equal(([('у', 5, 1), ('о', 11, 11), ('и', 7, 17), ('?', 4, 18)], 'ну как бы можно ли?'))

    @attr(status='stable')
    def test_rep_extraction_word_with_rle_515(self):
        rle = Rle()
        rle.rep_extraction_word(self.test_byte_str1_encoded_to_tuples, get_rle_as_str=True).should.be.equal(([('g', 9, 2), ('t', 8, 6), ('o', 5, 9), ('n', 7, 10), ('y', 11, 11), ('.', 5, 12), ('e', 6, 25), ('a', 5, 28), ('p', 3, 29), ('!', 5, 31)], 'big fat pony. Or how to be hapy!', 'big^9 fat^8 po^5n^7y^11.^5 Or how to be^6 ha^5p^3y!^5'))
        rle.rep_extraction_word(self.test_byte_str2_encoded_to_tuples, get_rle_as_str=True).should.be.equal(([('😀', 8, 18), ('😜', 6, 19), ('😇', 5, 21)], 'So beautiful life 😀😜 😇', 'So beautiful life 😀^8😜^6 😇^5'))
        rle.rep_extraction_word(self.test_byte_str3_encoded_to_tuples, get_rle_as_str=True).should.be.equal(([('ü', 6, 5), ('a', 4, 24), ('l', 5, 25), ('ä', 4, 33), ('!', 3, 36)], 'mit Üüberzeugung hat er ales gestämt!', 'mit Üü^6berzeugung hat er a^4l^5es gestä^4mt!^3'))
        rle.rep_extraction_word(self.test_byte_str4_encoded_to_tuples, get_rle_as_str=True).should.be.equal(([('у', 5, 1), ('о', 11, 11), ('и', 7, 17), ('?', 4, 18)], 'ну как бы можно ли?', 'ну^5 как бы мо^11жно ли^7?^4'))

    @attr(status='stable')
    def test_rep_extraction_sent_515(self):
        rle = Rle()
        (self.test_byte_sent1_encoded, self.test_byte_sent1_encoded_mapping)
        rle.rep_extraction_sent(self.test_byte_sent1_encoded, self.test_byte_sent1_encoded_mapping).should.be.equal(([{'start_index_in_orig': 0, 'length': 4, 'word': 'big', 'index_in_redu_free': 0}, {'start_index_in_orig': 5, 'length': 2, 'word': 'pony', 'index_in_redu_free': 2}], ['big', 'fat', 'pony']))
        rle.rep_extraction_sent(self.test_byte_sent2_encoded, self.test_byte_sent2_encoded_mapping).should.be.equal(([{'start_index_in_orig': 0, 'length': 5, 'word': '😀', 'index_in_redu_free': 0}], ['😀', '😍']))