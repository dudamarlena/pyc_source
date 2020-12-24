# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: src/repair_regex.py
# Compiled at: 2018-01-10 14:39:00
"""
Module of repairs to do to source code.
"""
COMPARISONS = '(>=|<=|>|<|!=|==)'
ASSIGNMENTS = '(\\+=|-=|/=|\\*=|=)'
START_BRACKETS = '(\\{|\\[|\\()'
END_BRACKETS = '(\\}|\\]|\\))'
WHITESPACE_TABLE = {'Exactly one space required after :': [
                                        (
                                         ':\\s*(\\S+)', ': \\1', {})], 
   'Exactly one space required after comma': [
                                            (
                                             '(.*?),\\s*', '\\1, ', {})], 
   'Exactly one space required after comparison': [
                                                 (
                                                  ('(.*?){0}\\s*(\\S+)').format(COMPARISONS), '\\1\\2 \\3', {})], 
   'Exactly one space required around assignment': [
                                                  (
                                                   ('(.*?[\\w\\d_\\[\\]\\(\\)]+)\\s*{0}\\s*(\\S+)').format(ASSIGNMENTS), '\\1 \\2 \\3', {'count': 1})], 
   'Exactly one space required around comparison': [
                                                  (
                                                   ('(.*\\S+)\\s*{0}\\s*').format(COMPARISONS), '\\1 \\2 ', {})], 
   'No space allowed around keyword argument assignment': [
                                                         (
                                                          ('(.*\\S+)\\s*{0}\\s*(\\S+)').format(ASSIGNMENTS), '\\1\\2\\3', {'count': 1})], 
   'No space allowed before :': [
                               (
                                '(.*?)\\s+:', '\\1:', {})], 
   'No space allowed after bracket': [
                                    (
                                     ('(.*?){0}\\s+').format(START_BRACKETS), '\\1\\2', {})], 
   'No space allowed before bracket': [
                                     (
                                      ('(.*?)\\s+{0}').format(END_BRACKETS), '\\1\\2', {})], 
   'No space allowed before comma': [
                                   (
                                    '(.*?)\\s+,', '\\1,', {})]}