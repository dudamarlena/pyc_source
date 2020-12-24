# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/brentpayne/anaconda/lib/python2.7/site-packages/phrase/corpus.py
# Compiled at: 2014-08-28 17:58:28
import os
__author__ = 'brentpayne'

class FileCorpus(object):

    def __init__(self, *files):
        """
        Initializes the FileCorpus with a list of files.
        :param files: a list of filepaths
        :return: None
        """
        self.files = []
        self.files.extend(files)

    def extend(self, *files):
        self.files.extend(files)

    def append(self, file):
        self.files.append(file)

    def add_folder(self, folder):
        for root, dirs, files in os.walk(folder, topdown=False):
            self.files.extend([ os.path.join(root, name) for name in files ])

    def get_iterator(self):
        return FileBackedDocumentIterator(self)


class FileBackedDocumentIterator(object):

    def __init__(self, corpus):
        """
        Initializes the FileCorpus with a list of files.
        :param files: a list of filepaths
        :return: None
        """
        self.files = []
        self.files.extend(corpus.files)
        self.idx = -1

    def reset(self):
        self.idx = -1

    def __iter__(self):
        return self

    def next(self):
        self.idx += 1
        if self.idx >= len(self.files):
            self.idx = -1
            raise StopIteration
        filepath = self.files[self.idx]
        file_lines = []
        with open(filepath) as (fp):
            for line in fp:
                file_lines.append(line.split())

        return file_lines