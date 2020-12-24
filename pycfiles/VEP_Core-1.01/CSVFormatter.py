# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\LocalUsers\ealexand\VEP_Core\vep_core\Ity\Formatters\CSVFormatter.py
# Compiled at: 2013-12-05 13:11:49
__author__ = 'kohlmannj'
import csv
from collections import OrderedDict
from Ity.Tokenizers import Tokenizer
from Ity.Formatters import Formatter
import cStringIO as StringIO

class CSVFormatter(Formatter):

    def __init__(self, debug=False, untagged_rule='!UNTAGGED', no_rules_rule='!NORULE', excluded_rule='!EXCLUDED'):
        super(CSVFormatter, self).__init__(debug)
        self.output = None
        self.writer = None
        self.untagged_rule = untagged_rule
        self.no_rules_rule = no_rules_rule
        self.excluded_rule = excluded_rule
        self.special_rules = [
         self.untagged_rule,
         self.no_rules_rule,
         self.excluded_rule]
        return

    def format(self, tags=None, tokens=None, s=None, corpus_name=None, text_name=None, write_headings=False):
        raise StandardError('format() not implemented, sorry!')

    def batch_format(self, tags_list=None, tokens_list=None, s_list=None, corpus_name=None, corpus_list=None, text_name_list=None, write_headings=True):
        all_rules = OrderedDict()
        if tags_list is None:
            raise ValueError('No tags_list given to batch_format().')
        for tags in tags_list:
            if tags is None or len(tags) != 2 or tags[0] is None or tags[1] is None:
                raise ValueError('Invalid tagger data in tags_list given to batch_format().')
            for rule_full_name, rule in tags[0].items():
                if rule_full_name not in all_rules:
                    all_rules[rule_full_name] = rule

        if len(all_rules.keys()) == 0:
            raise StandardError('Accumulated *zero* tags from all the tags in tags_list!')
        all_rules = OrderedDict(all_rules.iteritems(), key=lambda rule: rule[''])
        canonical_len = len(tags_list)
        for the_list in [tokens_list, s_list, text_name_list]:
            if the_list is None:
                continue
            if len(the_list) != canonical_len:
                raise ValueError('List of a different length than len(tags_list) given as input to batch_format().')

        self.output = StringIO.StringIO()
        self.writer = csv.writer(self.output)
        if write_headings:
            row = []
            if text_name_list is not None:
                row.append('Filename')
            if corpus_name is not None or corpus_list is not None and len(corpus_list) == canonical_len:
                row.append('Corpus')
            for rule_full_name in all_rules.keys():
                if rule_full_name not in self.special_rules:
                    row.append(rule_full_name)

            if tokens_list is not None:
                row.append('<# untagged tokens>')
                row.append('<# no-rules tokens>')
                row.append('<# excluded tokens>')
                row.append('<# word tokens>')
                row.append('<# punctuation tokens>')
                row.append('<# tokens>')
                row.append('<# tag maps>')
            self.writer.writerow(row)
        for index, tags in enumerate(tags_list):
            tag_maps = tags[1]
            tag_key_counts = OrderedDict()
            for rule_full_name in all_rules.keys():
                num_tag_maps_with_tag_key = 0
                for tag_map in tag_maps:
                    tag_key_strs = [ tag_key_tuple[0] for tag_key_tuple in tag_map['rules'] ]
                    if rule_full_name in tag_key_strs:
                        num_tag_maps_with_tag_key += 1

                if len(tag_maps) > 0:
                    count = num_tag_maps_with_tag_key
                else:
                    count = 0
                tag_key_counts[rule_full_name] = count

            row = []
            if text_name_list is not None:
                row.append(text_name_list[index])
            if corpus_list is not None and len(corpus_list) == canonical_len:
                row.append(corpus_list[index])
            else:
                if corpus_name is not None:
                    row.append(corpus_name)
                for rule_full_name, count in tag_key_counts.items():
                    if rule_full_name not in self.special_rules:
                        if len(tag_maps) > 0:
                            row.append(float(count) / len(tag_maps) * 100)
                        else:
                            row.append(0.0)

                for special_rule in self.special_rules:
                    try:
                        row.append(tag_key_counts[special_rule])
                    except KeyError:
                        row.append('0')

            if tokens_list is not None:
                if tokens_list[index] is not None:
                    row.append(len([ token for token in tokens_list[index] if token[Tokenizer.INDEXES['TYPE']] == Tokenizer.TYPES['WORD'] ]))
                    row.append(len([ token for token in tokens_list[index] if token[Tokenizer.INDEXES['TYPE']] == Tokenizer.TYPES['PUNCTUATION'] ]))
                    row.append(len(tokens_list[index]))
                row.append(len(tag_maps))
            self.writer.writerow(row)

        output_as_str = self.output.getvalue()
        self.output.close()
        return output_as_str