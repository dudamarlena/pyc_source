# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/MangaCrawler/MAL.py
# Compiled at: 2017-04-24 15:48:41
# Size of source mod 2**32: 2040 bytes
"""
  Made by Santeri Hetekivi.
  Licensed under Apache License 2.0.
  10/2016
"""
from .XML import XML
from .Manga import Manga

class MAL:
    mangas = []
    statuses = {'Reading':1, 
     'Completed':2,  'On-Hold':3,  'Dropped':4,  'Plan to Read':6}

    def __init__(self):
        self.XML = XML()

    def print_names(self, mangas=None):
        if not mangas:
            mangas = self.mangas
        for manga in mangas:
            print('%s %s %s' % (manga.name, manga.status, manga.chapters))

    def parse(self, file_path=None):
        root = self.XML.get_xml_root(file_path)
        if root:
            for manga in root.iter('manga'):
                self.mangas.append(Manga(self.get_all_info(manga, ['manga_mangadb_id', 'series_animedb_id', 'series_mangadb_id']), self.get_all_info(manga, ['manga_title', 'series_title']), self.get_info(manga, 'my_status'), self.get_info(manga, 'my_read_chapters'), self.get_info(manga, 'series_synonyms')))

            return True
        else:
            return False

    def get_all_info(self, manga, info_names):
        for info_name in info_names:
            value = self.get_info(manga, info_name)
            if value:
                return value

        return ''

    @staticmethod
    def get_info(manga, info_name):
        field = manga.find(info_name)
        if field is not None:
            return field.text
        else:
            return ''

    def get_mangas_by_status(self, status):
        mangas_by_status = []
        if status in self.statuses:
            number = self.statuses[status]
        else:
            number = False
        for manga in self.mangas:
            if manga.status == status:
                mangas_by_status.append(manga)
            else:
                if number and str(manga.status) == str(number):
                    mangas_by_status.append(manga)

        return mangas_by_status