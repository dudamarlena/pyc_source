# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/tiro/rules_generator.py
# Compiled at: 2016-03-05 17:23:41
import collections, re, random

class Generator(object):

    def __init__(self, text):
        self.symbol_pool = sum([ list(range(x, y)) for x, y in [
         (383, 447), (502, 687), (913, 1071), (1120, 1319)]
                               ], [])
        random.shuffle(self.symbol_pool)
        self.symbol_pool = iter(self.symbol_pool)
        self.text = text

    def token_counter(self, pattern, count):
        """
        Return the <count> most common instances of <pattern> in the text.
        """
        return collections.Counter(re.findall(pattern, self.text)).most_common(count)

    def dict_builder(self, counter, name_prefix='', pattern_suffix=''):
        """
        Build a dictionary of regnet-style abbreviation definitions.
        """
        rules = {'abbreviations': []}
        for most_common, _ in counter:
            rules['abbreviations'].append({'name': name_prefix + most_common.upper(), 
               'pattern': most_common + pattern_suffix, 
               'unicode': chr(next(self.symbol_pool))})

        return rules

    def generate_rules(self):
        patterns = self.dict_builder(self.token_counter('\\w\\w', 15), name_prefix='_')
        patterns.update(self.dict_builder(self.token_counter('\\w\\w+', 20), pattern_suffix='#word'))
        return patterns