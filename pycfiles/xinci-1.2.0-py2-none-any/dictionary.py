# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/lapis-hong/Documents/Sina/Project/xinci/xinci/dictionary.py
# Compiled at: 2018-06-20 00:34:26
"""This module contains common word dictionary."""
from __future__ import unicode_literals
import os, codecs
from utils import data_reader
import logging
COMMON_DIC_PATH = os.path.dirname(__file__) + b'/common.dic'

class Dictionary:
    """A class to load and update common words dictionary file: common.dic.
    xinci(new words) = all extraction words - common words 
    In order to improve xinci result, need to update common.dic with specific corpus.
    
    Examples:
    ---------
    >>> import xinci
    # initial with default `common.dic` or user dic path.
    >>> dic = xinci.Dictionary('user.dic')
    # load dic
    >>> dic.load()
    >>> dic.dictionary
    # iterable 
    >>> for word in dic:
           print(word)
    # return vocab size
    >>> len(dic)
    # add words
    >>> dic.add(['中国'])
    # add words from user dic file
    >>> dic.add_from_file('user.dic')
    # remove words
    >>>dic.remove(['中国'])
    # remove words from user dic file
    >>> dic.remove_from_file('user.dic')
    """

    def __init__(self, common_dic_path=None):
        if common_dic_path:
            self._common_dic_path = common_dic_path
            logging.info((b'Using user common words dic `{}`').format(self._common_dic_path))
        else:
            self._common_dic_path = COMMON_DIC_PATH
            logging.info((b'Using default common words dic `{}`').format(self._common_dic_path))
        self.dictionary = set()
        self._init()

    def _init(self):
        """Init common dic, access vocab by dictionary attr or load method."""
        common_dic = data_reader(self._common_dic_path)
        vocab = common_dic.strip().split(b'\n')
        for word in vocab:
            if word:
                self.dictionary.add(word)

        logging.info((b'Initialized `{}` common words from file `{}`').format(len(vocab), self._common_dic_path))

    def __contains__(self, item):
        return item in self.dictionary

    def __iter__(self):
        """Iterate over Dictionary instance."""
        for word in self.dictionary:
            yield word

    def __len__(self):
        return len(self.dictionary)

    def load(self):
        """Load common dic
        Returns:
            common words set.
        """
        return self.dictionary

    def add(self, vocab):
        """Add words to common dic by iterable object.
        Args:
            vocab: Iterable object, each element is a word.
        """
        with codecs.open(self._common_dic_path, b'a+') as (fo):
            for word in vocab:
                if word not in self.dictionary:
                    self.dictionary.add(word)
                    fo.write(b'\n' + word)
                    logging.info((b'Add word `{}` to file `{}`.').format(word, self._common_dic_path))

    def add_from_file(self, vocab_file):
        """Add words to common dic by vocab file.
        Args:
            vocab_file: user vocab file path.
        """
        user_dic = data_reader(vocab_file)
        vocab = user_dic.strip().split(b'\n')
        with codecs.open(self._common_dic_path, b'a+') as (fo):
            for word in vocab:
                if word not in self.dictionary:
                    self.dictionary.add(word)
                    fo.write(b'\n' + word)
                    logging.info((b'Add word `{}` to file `{}`.').format(word, self._common_dic_path))

    def remove(self, vocab):
        """Remove words from common dic by iterable object.
        Args:
            vocab: Iterable object, each element is a word.
        """
        for word in vocab:
            if word in self.dictionary:
                self.dictionary.remove(word)
                logging.info((b'Remove word `{}` to file `{}`.').format(word, self._common_dic_path))

        with codecs.open(self._common_dic_path, b'w', encoding=b'utf-8') as (fo):
            for word in self.dictionary:
                fo.write(word + b'\n')

    def remove_from_file(self, vocab_file):
        """Remove words from common dic by iterable object.
        Args:
            vocab_file: user vocab file path.
        """
        user_dic = data_reader(vocab_file)
        vocab = user_dic.strip().split(b'\n')
        for word in vocab:
            if word in self.dictionary:
                self.dictionary.remove(word)
                logging.info((b'Remove word `{}` to file `{}`.').format(word, self._common_dic_path))

        with codecs.open(self._common_dic_path, b'w') as (fo):
            for word in self.dictionary:
                fo.write(word + b'\n')