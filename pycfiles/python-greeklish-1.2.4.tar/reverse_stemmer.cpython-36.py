# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/marseltzatzo/01.PROJECTS/01.Python/greeklish/greeklish/reverse_stemmer.py
# Compiled at: 2017-04-03 08:22:30
# Size of source mod 2**32: 2802 bytes
import re

class ReverseStemmer(object):
    SUFFIX_MATOS = 'ματος'
    SUFFIX_MATA = 'ματα'
    SUFFIX_MATWN = 'ματων'
    SUFFIX_AS = 'ασ'
    SUFFIX_EIA = 'εια'
    SUFFIX_EIO = 'ειο'
    SUFFIX_EIOY = 'ειου'
    SUFFIX_EIWN = 'ειων'
    SUFFIX_IOY = 'ιου'
    SUFFIX_IA = 'ια'
    SUFFIX_IWN = 'ιων'
    SUFFIX_OS = 'ος'
    SUFFIX_OI = 'οι'
    SUFFIX_EIS = 'εις'
    SUFFIX_ES = 'ες'
    SUFFIX_HS = 'ης'
    SUFFIX_WN = 'ων'
    SUFFIX_OY = 'ου'
    SUFFIX_O = 'ο'
    SUFFIX_H = 'η'
    SUFFIX_A = 'α'
    SUFFIX_I = 'ι'
    SUFFIX_STRINGS = [
     [
      SUFFIX_MATOS, 'μα', 'ματων', 'ματα'],
     [
      SUFFIX_MATA, 'μα', 'ματων', 'ματος'],
     [
      SUFFIX_MATWN, 'μα', 'ματα', 'ματος'],
     [
      SUFFIX_AS, 'α', 'ων', 'ες'],
     [
      SUFFIX_EIA, 'ειο', 'ειων', 'ειου', 'ειας'],
     [
      SUFFIX_EIO, 'εια', 'ειων', 'ειου'],
     [
      SUFFIX_EIOY, 'εια', 'ειου', 'ειο', 'ειων'],
     [
      SUFFIX_EIWN, 'εια', 'ειου', 'ειο', 'ειας'],
     [
      SUFFIX_IOY, 'ι', 'ια', 'ιων', 'ιο'],
     [
      SUFFIX_IA, 'ιου', 'ι', 'ιων', 'ιας', 'ιο'],
     [
      SUFFIX_IWN, 'ιου', 'ια', 'ι', 'ιο'],
     [
      SUFFIX_OS, 'η', 'ους', 'ου', 'οι', 'ων'],
     [
      SUFFIX_OI, 'ος', 'ου', 'ων'],
     [
      SUFFIX_EIS, 'η', 'ης', 'εων'],
     [
      SUFFIX_ES, 'η', 'ας', 'ων', 'ης', 'α'],
     [
      SUFFIX_HS, 'ων', 'ες', 'η', 'εων'],
     [
      SUFFIX_WN, 'ος', 'ες', 'α', 'η', 'ης', 'ου', 'οι', 'ο', 'α'],
     [
      SUFFIX_OY, 'ων', 'α', 'ο', 'ος'],
     [
      SUFFIX_O, 'α', 'ου', 'εων', 'ων'],
     [
      SUFFIX_H, 'ος', 'ους', 'εων', 'εις', 'ης', 'ων'],
     [
      SUFFIX_A, 'ο', 'ου', 'ων', 'ας', 'ες'],
     [
      SUFFIX_I, 'ιου', 'ια', 'ιων']]

    def __init__(self):
        self.suffixes = {}
        self.greek_words = []
        for suffix in self.SUFFIX_STRINGS:
            self.suffixes[suffix[0]] = suffix[1:]

    def generate_greek_variants(self, token_string):
        self.greek_words = [token_string]
        for key in self.suffixes.keys():
            if token_string.endswith(key):
                self.generate_more_greek_words(token_string, key)
                break

        return self.greek_words

    def generate_more_greek_words(self, token_string, suffix_key):
        regex = re.compile('{0}$'.format(suffix_key))
        for suffix in self.suffixes[suffix_key]:
            self.greek_words.append(regex.sub(suffix, token_string))