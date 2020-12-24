# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/dev/signalbox/signalbox/utilities/gibberish.py
# Compiled at: 2014-08-27 19:26:12
"""Make random pronouncable strings"""
import string, itertools, random, functools
initial_consonants = set(string.ascii_lowercase) - set('aeiou') - set('qxc') | set(['bl', 'br', 'cl', 'cr', 'dr', 'fl',
 'fr', 'gl', 'gr', 'pl', 'pr', 'sk',
 'sl', 'sm', 'sn', 'sp', 'st', 'str',
 'sw', 'tr'])
final_consonants = set(string.ascii_lowercase) - set('aeiou') - set('qxcsj') | set(['ct', 'ft', 'mp', 'nd', 'ng', 'nk', 'nt',
 'pt', 'sk', 'sp', 'ss', 'st'])
vowels = 'aeiou'
syllables = map(('').join, itertools.product(initial_consonants, vowels, final_consonants))

def gibberish(wordcount, wordlist=syllables):
    return ('_').join(random.sample(wordlist, wordcount))


random_stata_varname = functools.partial(gibberish, wordcount=3)