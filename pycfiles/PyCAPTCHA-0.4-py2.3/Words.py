# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Captcha/Words.py
# Compiled at: 2006-02-05 00:25:47
""" Captcha.Words

Utilities for managing word lists and finding random words
"""
import random, os, File

class WordList(object):
    """A class representing a word list read from disk lazily.
       Blank lines and comment lines starting with '#' are ignored.
       Any number of words per line may be used. The list can
       optionally ingore words not within a given length range.
       """
    __module__ = __name__

    def __init__(self, fileName, minLength=None, maxLength=None):
        self.words = None
        self.fileName = fileName
        self.minLength = minLength
        self.maxLength = maxLength
        return

    def read(self):
        """Read words from disk"""
        f = open(os.path.join(File.dataDir, 'words', self.fileName))
        self.words = []
        for line in f.xreadlines():
            line = line.strip()
            if not line:
                continue
            if line[0] == '#':
                continue
            for word in line.split():
                if self.minLength is not None and len(word) < self.minLength:
                    continue
                if self.maxLength is not None and len(word) > self.maxLength:
                    continue
                self.words.append(word)

        return

    def pick(self):
        """Pick a random word from the list, reading it in if necessary"""
        if self.words is None:
            self.read()
        return random.choice(self.words)
        return


basic_english = WordList('basic-english')
basic_english_restricted = WordList('basic-english', minLength=5, maxLength=8)
defaultWordList = basic_english_restricted