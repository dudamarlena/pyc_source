# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/brentpayne/anaconda/lib/python2.7/site-packages/phrase/word_list.py
# Compiled at: 2014-08-28 17:58:28
__author__ = 'brentpayne'

class WordList(dict):

    def __init__(self):
        self.id2word = {}
        self.next_id = 1

    def get_next_id(self):
        rv = self.next_id
        self.next_id += 1
        return rv

    def add(self, word, id=None):
        """
        Adds a new word to the WordList and assigns it an id.  If id is set,
        :param word: The word token
        :param id: (Optional) The token id can be set, but bypasses the automatic id assignment.  Only specify the id
          if you plan to specify it on all add calls.
        :return: None
        """
        word_id = id if id is not None else self.get_next_id()
        self[word] = word_id
        self.id2word[word_id] = word
        return

    def contains(self, id):
        """
        Determines if an ID is part of the word lis
        :param id: the id to check
        :return: True if the id is in the word list
        """
        return id in self.id2word