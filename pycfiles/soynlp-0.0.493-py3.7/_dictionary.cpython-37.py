# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/soynlp/postagger/_dictionary.py
# Compiled at: 2018-08-27 09:22:57
# Size of source mod 2**32: 3611 bytes
import sys
if sys.version_info <= (2, 7):
    reload(sys)
    sys.setdefaultencoding('utf-8')
import json, os

class Dictionary:

    def __init__(self, pos_dict):
        if isinstance(pos_dict, dict):
            for key in pos_dict:
                if sys.version_info.major == 2:
                    pos_dict[key] = set(map(unicode, pos_dict[key]))
                else:
                    pos_dict[key] = set(pos_dict[key])

            self.pos_dict = pos_dict
            self.max_length = self._check_max_length(self.pos_dict)
        else:
            if isinstance(pos_dict, str):
                if os.path.exists(pos_dict):
                    self.load(pos_dict)
                else:
                    raise ValueError('dictionary file does not exist')

    def _check_max_length(self, pos_dict):
        return max((len(word) for words in pos_dict.values() for word in words))

    def get_pos(self, word):
        tags = []
        for pos, words in self.pos_dict.items():
            if word in words:
                tags.append(pos)

        return tags

    def word_is_tag(self, word, tag):
        return word in self.pos_dict.get(tag, {})

    def add_words(self, tag, words, force=False):
        words = self._type_check(words)
        if not force:
            if tag not in self.pos_dict:
                message = 'Check your tag or use add_words(tag, words, force=True)'.format(tag)
                raise ValueError(message)
        else:
            max_length = max((len(word) for word in words))
            if self.max_length < max_length:
                self.max_length = max_length
            if tag not in self.pos_dict:
                dictionary = words
            else:
                dictionary = self.pos_dict.get(tag, {})
                dictionary.update(words)
        self.pos_dict[tag] = dictionary

    def remove_words(self, tag, words=None):
        if tag not in self.pos_dict:
            raise ValueError('tag {} does not exist'.format(tag))
        if words == None:
            self.pos_dict.pop(tag)
            return
        words = self._type_check(words)
        dictionary = self.pos_dict[tag]
        dictionary -= words

    def _type_check(self, words):
        if isinstance(words, str):
            words = set(words.split())
        return words

    def load(self, filename):
        if sys.version_info.major == 2:
            with open(filename) as (fp):
                params = json.load(unicode(fp))
                self.max_length = params['max_length']
                self.pos_dict = {tag:set(words) for tag, words in params['pos_dict'].items()}
        else:
            with open(filename, encoding='utf-8') as (fp):
                params = json.load(fp)
                self.max_length = params['max_length']
                self.pos_dict = {tag:set(words) for tag, words in params['pos_dict'].items()}

    def save(self, filename):
        if sys.version_info.major == 2:
            with open(filename, 'w') as (fp):
                params = {'max_length':self.max_length,  'pos_dict':{pos:list(words) for pos, words in self.pos_dict.items()}}
                json.dump(params, fp, ensure_ascii=False, indent=2)
        else:
            with open(filename, 'w', encoding='utf-8') as (fp):
                params = {'max_length':self.max_length,  'pos_dict':{pos:list(words) for pos, words in self.pos_dict.items()}}
                json.dump(params, fp, ensure_ascii=False, indent=2)