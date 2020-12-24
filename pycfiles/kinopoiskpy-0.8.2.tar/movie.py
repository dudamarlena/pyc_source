# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: kinopoisk/tests/movie.py
# Compiled at: 2018-08-23 14:38:46
from __future__ import unicode_literals
from datetime import datetime
from kinopoisk.movie import Movie
from .base import BaseTest

class MovieTest(BaseTest):

    def test_movie_posters_page_source(self):
        m = Movie(id=51319)
        m.get_content(b'posters')
        self.assertGreaterEqual(len(m.posters), 34)

    def test_movie_search_manager_redacted(self):
        movies = Movie.objects.search(b'Без цензуры 2007')
        self.assertGreater(len(movies), 1)
        m = movies[0]
        self.assertEqual(m.id, 278229)
        self.assertEqual(m.year, 2007)
        self.assertEqual(m.title, b'Без цензуры')
        self.assertEqual(m.title_en, b'Redacted')
        self.assertEqual(m.runtime, 90)
        self.assertEqual(m.rating, 6.126)
        self.assertGreaterEqual(m.votes, 1760)

    def test_movie_search_manager_pulp_fiction(self):
        movies = Movie.objects.search(b'pulp fiction')
        self.assertGreater(len(movies), 1)
        m = movies[0]
        self.assertEqual(m.id, 342)
        self.assertEqual(m.title, b'Криминальное чтиво')
        self.assertEqual(m.year, 1994)
        self.assertEqual(m.title_en, b'Pulp Fiction')

    def test_movie_search_manager_warcraft(self):
        movies = Movie.objects.search(b'Варкрафт')
        self.assertEqual(len(movies), 1)
        m = movies[0]
        self.assertEqual(m.id, 277328)
        self.assertEqual(m.title, b'Варкрафт')
        self.assertEqual(m.year, 2016)
        self.assertEqual(m.title_en, b'Warcraft')

    def test_movie_main_page_id_278229(self):
        """
        Test of movie manager, movie obtain by id (not via search)
        """
        m = Movie(id=278229)
        m.get_content(b'main_page')
        self.assertEqual(m.id, 278229)
        self.assertEqual(m.year, 2007)
        self.assertEqual(m.title, b'Без цензуры')
        self.assertEqual(m.title_en, b'Redacted')
        self.assertEqual(m.plot, b'В центре картины — небольшой отряд американских солдат на контрольно-пропускном пункте в Ираке. Причём восприятие их истории постоянно меняется. Мы видим события глазами самих солдат, представителей СМИ, иракцев и понимаем, как на каждого из них влияет происходящее, их встречи и столкновения друг с другом.')
        self.assertEqual(m.runtime, 90)
        self.assertEqual(m.tagline, b'«Фильм, запрещенный к прокату во многих странах»')
        self.assertEqualPersons(m.actors, [b'Иззи Диаз', b'Роб Дивейни', b'Ти Джонс', b'Анас Веллман', b'Майк Фигуроа',
         b'Яналь Кассай', b'Дхиая Калиль', b'Кел О’Нил', b'Дэниэл Стюарт-Шерман',
         b'Патрик Кэрролл'])

    def test_movie_main_page_id_746251(self):
        m = Movie(id=746251)
        m.get_content(b'main_page')
        self.assertEqual(m.year, None)
        self.assertEqual(m.title, b'Ловкость')
        self.assertEqual(m.genres, [b'драма'])
        self.assertEqual(m.countries, [b'США'])
        return

    def test_movie_main_page_empty_actors(self):
        m = Movie(id=926005)
        m.get_content(b'main_page')
        self.assertEqual(m.actors, [])

    def test_movie_main_page_id_4374(self):
        """
        Test of movie manager, movie obtain by id (not via search)
        """
        m = Movie(id=4374)
        m.get_content(b'main_page')
        self.assertEqual(m.id, 4374)
        self.assertEqual(m.year, 2003)
        self.assertEqual(m.title, b'Пираты Карибского моря: Проклятие Черной жемчужины')
        self.assertEqual(m.title_en, b'Pirates of the Caribbean: The Curse of the Black Pearl')
        self.assertEqual(m.plot, b'Жизнь харизматичного авантюриста, капитана Джека Воробья, полная увлекательных приключений, резко меняется, когда его заклятый враг — капитан Барбосса — похищает корабль Джека, Черную Жемчужину, а затем нападает на Порт Ройал и крадет прекрасную дочь губернатора, Элизабет Свонн. Друг детства Элизабет, Уилл Тернер, вместе с Джеком возглавляет спасательную экспедицию на самом быстром корабле Британии, в попытке вызволить девушку из плена и заодно отобрать у злодея Черную Жемчужину. Вслед за этой парочкой отправляется амбициозный коммодор Норрингтон, который к тому же числится женихом Элизабет. Однако Уилл не знает, что над Барбоссой висит вечное проклятие, при лунном свете превращающее его с командой в живых скелетов. Проклятье будет снято лишь тогда, когда украденное золото Ацтеков будет возвращено пиратами на старое место.')
        self.assertEqual(m.runtime, 143)
        self.assertEqual(m.rating, 8.338)
        self.assertEqual(m.imdb_rating, 8.0)
        self.assertGreaterEqual(m.votes, 327195)
        self.assertGreaterEqual(m.imdb_votes, 859395)
        self.assertEqual(m.tagline, b"«Over 3000 Islands of Paradise -- For Some it's A Blessing -- For Others... It's A Curse»")
        self.assertEqual(m.genres, [b'фэнтези', b'боевик', b'приключения'])
        self.assertEqual(m.countries, [b'США'])
        self.assertGreaterEqual(m.budget, 140000000)
        self.assertGreaterEqual(m.marketing, 40000000)
        self.assertGreaterEqual(m.profit_usa, 305413918)
        self.assertGreaterEqual(m.profit_russia, 9060000)
        self.assertGreaterEqual(m.profit_world, 654264015)
        self.assertEqualPersons(m.actors, [b'Джонни Депп', b'Джеффри Раш', b'Орландо Блум', b'Кира Найтли', b'Джек Девенпорт',
         b'Кевин МакНэлли', b'Джонатан Прайс', b'Ли Аренберг', b'Макензи Крук', b'Дэвид Бэйли'])
        self.assertEqualPersons(m.directors, [b'Гор Вербински'])
        self.assertEqualPersons(m.screenwriters, [b'Тед Эллиот', b'Терри Россио', b'Стюарт Битти'])
        self.assertEqualPersons(m.producers, [b'Джерри Брукхаймер', b'Пол Дисон', b'Брюс Хендрикс'])
        self.assertEqualPersons(m.operators, [b'Дариуш Вольски'])
        self.assertEqualPersons(m.composers, [b'Клаус Бадельт'])
        self.assertEqualPersons(m.art_direction_by, [b'Брайан Моррис', b'Дерек Р. Хилл', b'Майкл Пауэлс'])
        self.assertEqualPersons(m.editing_by, [b'Стивен Е. Ривкин', b'Артур Шмидт', b'Крэйг Вуд'])

    def test_movie_main_page_id_258687(self):
        """
        Test of movie manager, movie obtain by id (not via search)
        """
        m = Movie(id=258687)
        m.get_content(b'main_page')
        self.assertEqual(m.id, 258687)
        self.assertEqual(m.year, 2014)
        self.assertEqual(m.title, b'Интерстеллар')
        self.assertEqual(m.title_en, b'Interstellar')
        self.assertEqual(m.plot, b'Когда засуха приводит человечество к продовольственному кризису, коллектив исследователей и учёных отправляется сквозь червоточину (которая предположительно соединяет области пространства-времени через большое расстояние) в путешествие, чтобы превзойти прежние ограничения для космических путешествий человека и переселить человечество на другую планету.')
        self.assertEqual(m.runtime, 169)
        self.assertEqual(m.tagline, b'«Следующий шаг человечества станет величайшим»')
        self.assertEqual(m.genres, [b'фантастика', b'драма', b'приключения'])
        self.assertEqual(m.countries, [b'США', b'Великобритания'])
        self.assertGreaterEqual(m.profit_usa, 158445319)
        self.assertGreaterEqual(m.profit_russia, 24110578)
        self.assertGreaterEqual(m.profit_world, 592845319)
        self.assertEqualPersons(m.directors, [b'Кристофер Нолан'])
        self.assertEqualPersons(m.screenwriters, [b'Джонатан Нолан', b'Кристофер Нолан'])
        self.assertEqualPersons(m.producers, [b'Кристофер Нолан', b'Линда Обст', b'Эмма Томас'])
        self.assertEqualPersons(m.operators, [b'Хойте Ван Хойтема'])
        self.assertEqualPersons(m.composers, [b'Ханс Циммер'])

    def test_movie_by_id_1552(self):
        m = Movie(id=1552)
        m.get_content(b'main_page')
        self.assertEqual(m.profit_russia, 41000)
        self.assertEqual(m.budget, 10000000)

    def test_movie_repr(self):
        instance = Movie(title=b'Молчание ягнят', title_en=b'The Silence of the Lambs', year=b'1990')
        self.assertEqual(instance.__repr__(), b'Молчание ягнят (The Silence of the Lambs), 1990')

    def test_movie_series_search_glee(self):
        movies = Movie.objects.search(b'glee')
        self.assertGreaterEqual(len(movies), 1)
        m = movies[0]
        self.assertTrue(m.series)
        m.get_content(b'series')
        self.assertGreaterEqual(len(m.seasons), 4)
        f = m.seasons[0]
        self.assertEqual(len(f.episodes), 22)
        self.assertEqual(f.year, 2010)
        e = m.seasons[0].episodes[5]
        self.assertEqual(e.title, b'Витамин D')
        self.assertEqual(e.release_date, datetime(2010, 11, 20).date())

    def test_movie_series_search_killing(self):
        movies = Movie.objects.search(b'the killing')
        self.assertGreaterEqual(len(movies), 1)
        m = movies[0]
        self.assertTrue(m.series)
        m.get_content(b'series')
        ls = m.seasons[(-1)]
        le = ls.episodes[(-1)]
        self.assertEqual(le.title, b'Эдем')

    def test_movie_series_main_page_kickass(self):
        m = Movie(id=419200)
        m.get_content(b'main_page')
        self.assertFalse(m.series)
        self.assertRaises(ValueError, m.get_content, ('series', ))

    def test_movie_series_main_page_bigband(self):
        m = Movie(id=306084)
        m.get_content(b'main_page')
        self.assertTrue(m.series)

    def test_movie_rating_from_search_result(self):
        movies = Movie.objects.search(b'the big bang theory')
        self.assertGreaterEqual(len(movies), 1)
        m = movies[0]
        self.assertGreaterEqual(m.rating, 8.5)