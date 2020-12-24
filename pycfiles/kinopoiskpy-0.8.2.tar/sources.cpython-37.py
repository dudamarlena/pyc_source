# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/kinopoiskpy/kinopoisk/person/sources.py
# Compiled at: 2019-07-02 23:07:19
# Size of source mod 2**32: 5155 bytes
"""
Sources for Person
"""
from __future__ import unicode_literals
import re
from builtins import str
from lxml import html
from ..utils import KinopoiskPage, KinopoiskImagesPage

class PersonCastLink(KinopoiskPage):
    __doc__ = '\n    Parser of person info in movie cast link\n    '
    xpath = {'id':'.//p[@type="stars"]/@objid', 
     'name':'.//div[@class="name"]/a/text()', 
     'name_en':'.//div[@class="name"]/span[@class="gray"]/text()'}

    def parse(self):
        self.instance.id = self.extract('id', to_int=True)
        self.instance.name = self.extract('name', to_str=True)
        self.instance.name_en = re.sub('^(.+) \\(в титрах:.+\\)$', '\\1', self.extract('name_en', to_str=True))
        self.instance.set_source('cast_link')


class PersonRoleLink(KinopoiskPage):
    __doc__ = '\n    Parser of person role info from career list\n    '
    xpath = {'note': './/span[@class="role"]/text()'}

    def parse(self):
        from kinopoisk.movie import Movie
        self.instance.movie = Movie.get_parsed('career_link', self.content)
        role = self.extract('note', to_str=True)
        role = self.split_triple_dots(role)
        role_name = None
        if len(role) > 1:
            role_name = self.prepare_str(role[1]).replace(', озвучка', '').replace('; короткометражка', '')
            if 'короткометражка' in role[1]:
                self.instance.movie.genres.append('короткометражка')
            if 'озвучка' in role[1]:
                self.instance.voice = True
        self.instance.name = role_name
        self.instance.set_source('role_link')


class PersonShortLink(KinopoiskPage):
    __doc__ = '\n    Parser of person info short link\n    '

    def parse(self):
        link = re.compile('<a[^>]+href="/name/(\\d+)/">(.+?)</a>').findall(self.content)
        if link:
            self.instance.id = self.prepare_int(link[0][0])
            self.instance.name = self.prepare_str(link[0][1])
        self.instance.set_source('short_link')


class PersonLink(KinopoiskPage):
    __doc__ = '\n    Parser of person info in link\n    '
    xpath = {'link':'.//p[@class="name"]/a', 
     'years':'.//span[@class="year"]/text()', 
     'name_en':'.//span[@class="gray"][1]/text()'}

    def parse(self):
        self.content = html.fromstring(self.content)
        link = self.extract('link')[0]
        years = self.extract('years')
        self.instance.id = self.prepare_int(link.get('href').split('/')[2])
        self.instance.name = self.prepare_str(link.text)
        self.instance.name_en = self.extract('name_en', to_str=True)
        if years:
            years = years.split(' – ')
            self.instance.year_birth = self.prepare_int(years[0])
            if len(years) > 1:
                self.instance.year_death = self.prepare_int(years[1])
        self.instance.set_source('link')


class PersonMainPage(KinopoiskPage):
    __doc__ = '\n    Parser of main person page\n    '
    url = '/name/{id}/'
    xpath = {'movies':'//div[@class="personPageItems"]/div[@class="item"]', 
     'id':'//link[@rel="canonical"]/@href', 
     'name':'//h1[@class="moviename-big"][@itemprop="name"]/text()', 
     'name_en':'//span[@itemprop="alternateName"]/text()'}

    def parse(self):
        content_info = re.compile('<tr\\s*>\\s*<td class="type">(.+?)</td>\\s*<td[^>]*>(.+?)</td>\\s*</tr>', re.S).findall(self.content)
        for name, value in content_info:
            if str(name) == 'дата рождения':
                year_birth = re.compile(' <a href="/lists/m_act\\[birthday\\]\\[year\\]/\\d{4}/">(\\d{4})</a>').findall(value)
                if year_birth:
                    self.instance.year_birth = self.prepare_int(year_birth[0])

        if self.instance.id:
            token = re.findall("xsrftoken = \\'([^\\']+)\\'", self.content)
            obj_type = re.findall("objType: \\'([^\\']+)\\'", self.content)
            if token:
                if obj_type:
                    content = self.request.get_content(self.instance.get_url('info', token=(token[0]), type=(obj_type[0])))
                    if content:
                        self.instance.information = content.replace(' class="trivia"', '')
        self.content = html.fromstring(self.content)
        person_id = re.compile('.+/name/(\\d+)/').findall(self.extract('id'))[0]
        self.instance.id = self.prepare_int(person_id)
        self.instance.name = self.extract('name', to_str=True)
        self.instance.name_en = self.extract('name_en', to_str=True)
        from kinopoisk.person import Role
        for element in self.extract('movies'):
            type = [t.get('data-work-type') for t in element.iterancestors()][0]
            self.instance.career.setdefault(type, [])
            self.instance.career[type].append(Role.get_parsed('role_link', element))

        self.instance.set_source('main_page')


class PersonPhotosPage(KinopoiskImagesPage):
    __doc__ = '\n    Parser of person photos page\n    '
    url = '/name/{id}/photos/'
    field_name = 'photos'