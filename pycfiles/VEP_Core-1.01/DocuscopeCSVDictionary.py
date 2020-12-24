# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\LocalUsers\ealexand\VEP_Core\Ity\Taggers\DocuscopeTagger\DocuscopeCSVDictionary.py
# Compiled at: 2014-05-14 13:25:04
__author__ = 'kohlmannj'
import os, codecs, csv
from Ity import dictionaries_root
from Ity import BaseClass

class DocuscopeCSVDictionary(BaseClass):

    def __init__(self, debug=False, label=None, rules_filename='default.csv', case_sensitive=False):
        super(DocuscopeCSVDictionary, self).__init__(debug, label)
        self.case_sensitive = case_sensitive
        self.rules_file = rules_filename
        if self.rules_file is None:
            raise ValueError('Attempting to initialize DocuscopeCSVDictionary without a rules_filename.')
        self.rules_path = os.path.join(dictionaries_root, self.label, self.rules_file)
        if not os.path.exists(self.rules_path):
            raise ValueError('Attempting to instantiate a DocuscopeCSVDictionary with a nonexistent rules_filename.')
        self.rules = {}
        self.tokens_in_rules = set()
        self.shortRules = {}
        self.words = dict()
        return

    def _load_rules(self):
        if len(self.rules.keys()) > 0:
            raise StandardError('Needlessly reloading rules file? Huh?')
        rules_file = codecs.open(self.rules_path, encoding='utf-8')
        reader = csv.reader(rules_file)
        for row_index, row in enumerate(reader):
            row = [ col.strip() for col in row ]
            if row_index == 0 and [ str(col).lower() for col in row ] == ['words', 'rule']:
                continue
            words = row[0].split()
            if not self.case_sensitive:
                words = tuple(str(word).lower() for word in words)
            rule = row[1]
            rule_tuple = (rule, words)
            if len(words) == 0:
                continue
            for w in words:
                self.words[w] = [
                 w]

            rule_root_key = words[0]
            if len(words) == 1:
                self.shortRules[rule_root_key] = rule
            else:
                rule_next_key = words[1]
                if rule_root_key not in self.rules:
                    self.rules[rule_root_key] = {}
                if rule_next_key not in self.rules[rule_root_key]:
                    self.rules[rule_root_key][rule_next_key] = []
                self.rules[rule_root_key][rule_next_key].append(rule_tuple)
            self.tokens_in_rules.update(words)