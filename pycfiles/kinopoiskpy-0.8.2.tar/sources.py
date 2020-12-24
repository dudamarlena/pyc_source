# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: kinopoisk/person/sources.py
# Compiled at: 2018-08-23 14:50:25
"""
Sources for Person
"""
from __future__ import unicode_literals
import re
from builtins import str
from lxml import html
from ..utils import KinopoiskPage, KinopoiskImagesPage, HEADERS

class PersonRoleLink(KinopoiskPage):
    """
    Parser person role info from career list
    """
    xpath = {b'note': b'.//span[@class="role"]/text()'}

    def parse(self):
        from kinopoisk.movie import Movie
        note = self.extract(b'note').strip().split(b'...')
        role_name = None
        if len(note) > 1:
            role_name = self.prepare_str(note[1]).replace(b', озвучка', b'').replace(b'; короткометражка', b'')
        self.instance.name = role_name
        self.instance.movie = Movie.get_parsed(b'career_link', self.content)
        self.instance.set_source(b'role_link')
        return


class PersonShortLink(KinopoiskPage):
    """
    Parser person info from short links
    """

    def parse(self):
        link = re.compile(b'<a[^>]+href="/name/(\\d+)/">(.+?)</a>').findall(self.content)
        if link:
            self.instance.id = self.prepare_int(link[0][0])
            self.instance.name = self.prepare_str(link[0][1])
        self.instance.set_source(b'short_link')


class PersonLink(KinopoiskPage):
    """
    Parser person info from links
    """
    xpath = {b'link': b'.//p[@class="name"]/a', 
       b'years': b'.//span[@class="year"]/text()', 
       b'name_en': b'.//span[@class="gray"][1]/text()'}

    def parse(self):
        self.content = html.fromstring(self.content)
        link = self.extract(b'link')[0]
        years = self.extract(b'years')
        self.instance.id = self.prepare_int(link.get(b'href').split(b'/')[2])
        self.instance.name = self.prepare_str(link.text)
        self.instance.name_en = self.extract(b'name_en', to_str=True)
        if years:
            years = years.split(b' – ')
            self.instance.year_birth = self.prepare_int(years[0])
            if len(years) > 1:
                self.instance.year_death = self.prepare_int(years[1])
        self.instance.set_source(b'link')


class PersonMainPage(KinopoiskPage):
    """
    Parser of main person page
    """
    url = b'/name/{id}/'
    xpath = {b'movies': b'//div[@class="personPageItems"]/div[@class="item"]', 
       b'id': b'//link[@rel="canonical"]/@href', 
       b'name': b'//h1[@class="moviename-big"][@itemprop="name"]/text()', 
       b'name_en': b'//span[@itemprop="alternateName"]/text()'}

    def parse(self):
        content_info = re.compile(b'<tr\\s*>\\s*<td class="type">(.+?)</td>\\s*<td[^>]*>(.+?)</td>\\s*</tr>', re.S).findall(self.content)
        for name, value in content_info:
            if str(name) == b'дата рождения':
                year_birth = re.compile(b'<a href="/lists/m_act%5Bbirthday%5D%5Byear%5D/\\d{4}/">(\\d{4})</a>').findall(value)
                if year_birth:
                    self.instance.year_birth = self.prepare_int(year_birth[0])

        if self.instance.id:
            token = re.findall(b"xsrftoken = \\'([^\\']+)\\'", self.content)
            obj_type = re.findall(b"objType: \\'([^\\']+)\\'", self.content)
            if token and obj_type:
                response = self.request.get(self.instance.get_url(b'info', token=token[0], type=obj_type[0]), headers=HEADERS)
                response.connection.close()
                if response.content:
                    self.instance.information = response.content.decode(b'windows-1251', b'ignore').replace(b' class="trivia"', b'')
        self.content = html.fromstring(self.content)
        person_id = re.compile(b'.+/name/(\\d+)/').findall(self.extract(b'id'))[0]
        self.instance.id = self.prepare_int(person_id)
        self.instance.name = self.extract(b'name', to_str=True)
        self.instance.name_en = self.extract(b'name_en', to_str=True)
        from kinopoisk.person import Role
        for element in self.extract(b'movies'):
            type = [ t.get(b'data-work-type') for t in element.iterancestors() ][0]
            self.instance.career.setdefault(type, [])
            self.instance.career[type].append(Role.get_parsed(b'role_link', element))

        self.instance.set_source(b'main_page')


class PersonPhotosPage(KinopoiskImagesPage):
    """
    Parser of person photos page
    """
    url = b'/name/{id}/photos/'
    field_name = b'photos'