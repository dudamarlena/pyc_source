# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: kinopoisk/tests/person.py
# Compiled at: 2018-08-23 12:28:41
from __future__ import unicode_literals
from kinopoisk.person import Person
from .base import BaseTest

class PersonTest(BaseTest):

    def test_person_manager_with_one_result(self):
        persons = Person.objects.search(b'Гуальтиеро Якопетти')
        self.assertEqual(len(persons), 1)
        p = persons[0]
        self.assertEqual(p.id, 351549)
        self.assertEqual(p.name, b'Гуалтьеро Якопетти')
        self.assertEqual(p.year_birth, 1919)
        self.assertEqual(p.name_en, b'Gualtiero Jacopetti')

    def test_person_manager_with_many_results(self):
        persons = Person.objects.search(b'malkovich')
        self.assertGreater(len(persons), 1)
        p = persons[0]
        self.assertEqual(p.id, 24508)
        self.assertEqual(p.name, b'Джон Малкович')
        self.assertEqual(p.year_birth, 1953)
        self.assertEqual(p.name_en, b'John Malkovich')
        p = persons[4]
        self.assertEqual(p.name, b'Др. Марк Малкович III')
        self.assertEqual(p.year_birth, 1930)
        self.assertEqual(p.year_death, 2010)

    def test_person_main_page_source(self):
        p = Person(id=6245)
        p.get_content(b'main_page')
        self.assertEqual(p.id, 6245)
        self.assertEqual(p.name, b'Джонни Депп')
        self.assertEqual(p.year_birth, 1963)
        self.assertEqual(p.name_en, b'Johnny Depp')
        self.assertGreater(len(p.information), 50)
        self.assertGreaterEqual(len(p.career[b'actor']), 86)
        self.assertGreaterEqual(len(p.career[b'producer']), 7)
        self.assertGreaterEqual(len(p.career[b'director']), 3)
        self.assertGreaterEqual(len(p.career[b'writer']), 1)
        self.assertGreaterEqual(len(p.career[b'hrono_titr_male']), 11)
        self.assertGreaterEqual(len(p.career[b'himself']), 124)
        self.assertEqual(p.career[b'actor'][0].movie.title, b'Человек-невидимка')
        self.assertEqual(p.career[b'actor'][0].movie.title_en, b'The Invisible Man')
        self.assertEqual(p.career[b'actor'][0].name, b'Dr. Griffin')
        self.assertEqual(p.career[b'actor'][1].movie.title, b'Ричард прощается')
        self.assertEqual(p.career[b'actor'][1].movie.year, 2018)
        self.assertEqual(p.career[b'actor'][1].movie.title_en, b'Richard Says Goodbye')
        self.assertEqual(p.career[b'actor'][4].movie.title, b'Шерлок Гномс')
        self.assertEqual(p.career[b'actor'][4].movie.title_en, b'Sherlock Gnomes')
        self.assertEqual(p.career[b'actor'][4].movie.year, 2018)
        self.assertEqual(p.career[b'actor'][4].name, b'Sherlock Gnomes')
        self.assertEqual(p.career[b'actor'][5].movie.title_en, b'Murder on the Orient Express')
        self.assertAlmostEqual(p.career[b'actor'][5].movie.rating, 6.68)
        self.assertGreaterEqual(p.career[b'actor'][5].movie.votes, 64162)
        self.assertAlmostEqual(p.career[b'actor'][5].movie.imdb_rating, 6.6)
        self.assertGreaterEqual(p.career[b'actor'][5].movie.imdb_votes, 70581)
        self.assertEqual(p.career[b'actor'][6].name, b'Abel')

    def test_person_photos_page_source(self):
        p = Person(id=8217)
        p.get_content(b'photos')
        self.assertGreaterEqual(len(p.photos), 11)

    def test_person_repr(self):
        instance = Person(name=b'Чарльз Чаплин', name_en=b'Charles Chaplin', year_birth=b'1950')
        self.assertEqual(instance.__repr__(), b'Чарльз Чаплин (Charles Chaplin), 1950')