# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gerardo/Projects/nlp_model_gen/nlp_model_gen/packages/wordProcessor/spanishNounConversor/Conversor.py
# Compiled at: 2019-06-14 18:07:58
# Size of source mod 2**32: 1731 bytes
import fnmatch

class Conversor:

    def __init__(self, general_configs):
        self._Conversor__configs = {'noun_groups':general_configs['groups'], 
         'exceptions':general_configs['exceptions']}

    def set_config(self, general_configs):
        self._Conversor__configs = {'noun_groups':general_configs['groups'], 
         'exceptions':general_configs['exceptions']}

    def a_plural(self, noun):
        words = noun.split()
        line = ''
        first_flag = True
        for word in words:
            if first_flag:
                first_flag = False
            else:
                line += ' '
            if word not in self._Conversor__configs['exceptions']:
                founded = False
                for group in self._Conversor__configs['noun_groups']:
                    if any(fnmatch.fnmatch(word, suffix) for suffix in group['suffixes']):
                        if 'backReplacements' in group.keys():
                            for backReplacement in group['backReplacements']:
                                if fnmatch.fnmatch(word, backReplacement['key']):
                                    word = word[0:len(word) - backReplacement['backCrop']]
                                    word = word + backReplacement['replacement']
                                    break

                        line += word + group['replacement']
                        founded = True
                        break

                if not founded:
                    line += word
            else:
                line += word

        if line == noun:
            return ''
        else:
            return line