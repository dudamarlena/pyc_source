# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/MangaCrawler/Manga.py
# Compiled at: 2017-03-19 15:39:15
# Size of source mod 2**32: 733 bytes
"""
  Made by Santeri Hetekivi.
  Licensed under Apache License 2.0.
  10/2016
"""

class Manga:
    malUrlStart = 'https://myanimelist.net/manga/'

    def __init__(self, _id, _name, my_status, _my_read_chapters, _synonyms=''):
        try:
            self.id = int(_id)
        except ValueError:
            self.id = -1

        self.url = self.mal_url()
        self.name = _name
        self.status = my_status
        if _synonyms:
            self.synonyms = _synonyms.split('; ')
        else:
            self.synonyms = []
        try:
            self.chapters = int(_my_read_chapters)
        except ValueError:
            self.chapters = -1

    def mal_url(self):
        return '%s%s' % (self.malUrlStart, self.id)