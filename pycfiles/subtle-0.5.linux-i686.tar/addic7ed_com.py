# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/subtle/webs/addic7ed_com.py
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

class addic7ed_com(Web):

    def __init__(self, video):
        self.sitio = b'http://www.addic7ed.com'
        self.video = video
        self.anotaciones = video.args.annotations
        self.idioma = self.idioma(video.args.language)
        self.link = None
        self.video.notificacion.n(b'Buscando en %s' % self.sitio, False)
        return

    def idioma(self, idioma):
        """Configura el idioma para que sea aceptado por la web"""
        idiomas = {b'en': 1, b'it': 7, 
           b'pt': 9, 
           b'pt-br': 10, 
           b'ro': 26, 
           b'es': 5, 
           b'es-lat': 6, 
           b'fr': 8, 
           b'el': 27, 
           b'ar': 38, 
           b'de': 11, 
           b'hr': 31, 
           b'da': 30, 
           b'id': 37, 
           b'he': 23, 
           b'ja': 32, 
           b'sv': 18, 
           b'ru': 19, 
           b'bg': 35, 
           b'zh': 24, 
           b'cs': 14, 
           b'nl': 17, 
           b'fi': 28, 
           b'hu': 20, 
           b'pl': 21, 
           b'sk': 25, 
           b'tr': 16}
        if idioma not in idiomas:
            idioma = idiomas[b'es']
        else:
            idioma = idiomas[idioma]
        return idioma

    def buscar_id(self):
        """Saca el id de la serie"""
        self.serie_sin_espacios = self.video.serie.replace(b' ', b'_')
        url_id = b'%s/search.php?search=%s' % (self.sitio, self.serie_sin_espacios)
        html_id = self.abrir_url(url_id)
        if html_id:
            sopa_id = BeautifulSoup(html_id)
            result = sopa_id.find(b'span', {b'class': b'titulo'})
            if result:
                self.id_serie = re.sub(b'/show/', b'', result.a[b'href'])
                return True
            return False
        else:
            self.id_serie = 0
            return False

    def buscar_subs(self):
        u"""Saca los subs encontrados para el capítulo y parsea el HTML"""
        url_temporada = b'%s/ajax_loadShow.php?show=%s&season=%s&langs=|%s|&hi=%d' % (self.sitio,
         self.id_serie,
         self.video.temporada,
         self.idioma,
         self.anotaciones)
        html_temporada = self.abrir_url(url_temporada)
        if html_temporada:
            sopa_temporada = BeautifulSoup(html_temporada)
            tabla_idiomas = sopa_temporada.find(b'div', {b'id': b'langs'})
            if tabla_idiomas.find_all(b'input', {b'id': b'lang%d' % self.idioma}):
                filas = sopa_temporada.find_all(b'tr', {b'class': b'epeven completed'})
                for fila in filas:
                    columnas = fila.find_all(b'td')
                    episodio_web = int(columnas[1].text)
                    completado = columnas[5].text
                    titulo_web = columnas[2].text
                    if self.video.titulo is None:
                        self.video.titulo = titulo_web
                    version_web = columnas[4].text
                    link_web = self.sitio + columnas[9].a[b'href']
                    if episodio_web == self.video.episodio:
                        if completado == b'Completed':
                            if self.comprobar_version(self.video.version, version_web):
                                self.link = link_web
                                return 0

        return 1

    def get_subtitles(self):
        u"""Principal, se conecta, busca y descarga los subtítulos"""
        if self.buscar_id():
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