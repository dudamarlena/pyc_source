# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/subtle/webs/subtitulos_es.py
# Compiled at: 2013-11-02 19:06:15
"""
Subtle is an automatic subtitle downloader for videos
Copyright (C) 2013 Francisco Jesús Macía Espín (fmacia)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from __future__ import unicode_literals
import re
from bs4 import BeautifulSoup
from subtle.core import Web

class subtitulos_es(Web):

    def __init__(self, video):
        self.sitio = b'http://www.subtitulos.es'
        self.video = video
        self.anotaciones = video.args.annotations
        self.idioma = self.idioma(video.args.language)
        self.link = None
        self.video.notificacion.n(b'Buscando en %s' % self.sitio, False)
        return

    def idioma(self, idioma):
        """Configura el idioma para que sea aceptado por la web"""
        idiomas = {b'en': b'English', b'es': b'Español (España)', 
           b'es-lat': b'Español (Latinoamérica)', 
           b'cat': b'Català'}
        if idioma not in idiomas:
            idioma = idiomas[b'es']
        else:
            idioma = idiomas[idioma]
        return idioma

    def buscar_nombre(self):
        """Consigue el nombre de la serie usado en la web.
        Esto sirve para series como spartacus, que en la web es spartacus:blood and sand
        """
        url_indice = b'%s/series' % self.sitio
        html_indice = self.abrir_url(url_indice)
        if html_indice:
            sopa_indice = BeautifulSoup(html_indice)
            serie_web = sopa_indice.find(b'a', text=re.compile(self.video.serie))
            if serie_web:
                self.nombre_serie = serie_web.text
                return True
            return False
        else:
            self.nombre_serie = b''
            return False

    def buscar_subs(self):
        u"""Saca los subs encontrados para el capítulo y parsea el HTML"""
        serie_sin_espacios = self.nombre_serie.replace(b' ', b'-')
        url_episodio = b'%s/%s/%dx%d' % (self.sitio, serie_sin_espacios, self.video.temporada, self.video.episodio)
        html_episodio = self.abrir_url(url_episodio)
        if html_episodio:
            sopa_episodio = BeautifulSoup(html_episodio)
            if self.video.titulo is None:
                self.video.titulo = re.sub(b'.* - ', b'', sopa_episodio.find(b'h1', {b'id': b'cabecera-subtitulo'}).text)
            versiones = sopa_episodio.find_all(b'div', {b'id': b'version'})
            for version in versiones:
                version_web = version.find(b'p', {b'class': b'title-sub'}).text
                if self.comprobar_version(self.video.version, version_web):
                    idiomas = version.find_all(b'ul', {b'class': b'sslist'})
                    for idioma in idiomas:
                        idioma_web = idioma.find(b'strong').text
                        if idioma_web == self.idioma:
                            completado = porcentaje_completado = idioma.find(b'li', {b'class': b'li-estado green'})
                            if completado:
                                self.link = idioma.next_sibling.next_sibling.a[b'href']
                                return 0

        return 1

    def get_subtitles(self):
        u"""Principal, se conecta, busca y descarga los subtítulos"""
        if self.anotaciones:
            self.video.notificacion.n(b'No se pueden buscar subtítulos con anotaciones para sordos en %s' % self.sitio, False)
            ret = 1
        elif self.buscar_nombre():
            self.buscar_subs()
            if self.link:
                if not self.video.args.check:
                    self.descargar()
                else:
                    self.video.notificacion.n(b'Subtítulos encontrados en %s' % self.sitio)
                ret = 0
            else:
                self.video.notificacion.n(b'No se han encontrado subtítulos en %s' % self.sitio, False)
                ret = 1
        else:
            self.video.notificacion.n(b'No se ha encontrado el vídeo en %s' % self.sitio, False)
            ret = 1
        return ret