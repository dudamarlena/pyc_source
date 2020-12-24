# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Captcha/Words.py
# Compiled at: 2006-02-05 00:25:47
__doc__ = ' Captcha.Words\n\nUtilities for managing word lists and finding random words\n'
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