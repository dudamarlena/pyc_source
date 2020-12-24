# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/subtle/webs/opensubtitles_org.py
# Compiled at: 2013-11-02 19:46:44
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
from subtle.core import Web

class opensubtitles_org(Web):

    def __init__(self, video):
        self.sitio = b'http://www.opensubtitles.org'
        self.servidor = b'http://api.opensubtitles.org/xml-rpc'
        self.conexion = self.conectar()
        self.token = None
        self.idsub = None
        self.sub = None
        self.useragent = b'Pysubtle'
        self.video = video
        self.anotaciones = video.args.annotations
        self.idioma = self.idioma(video.args.language)
        self.video.notificacion.n(b'Buscando en %s' % self.sitio, False)
        return

    def idioma(self, idioma):
        """Configura el idioma para que sea aceptado por la web"""
        idiomas = {b'en': b'eng', 
           b'fr': b'fre', 
           b'hu': b'hun', 
           b'cs': b'cze', 
           b'pl': b'pol', 
           b'sk': b'slo', 
           b'pt': b'por', 
           b'pt-br': b'pob', 
           b'es': b'spa', 
           b'el': b'ell', 
           b'ar': b'ara', 
           b'sq': b'alb', 
           b'hy': b'arm', 
           b'ay': b'ass', 
           b'bs': b'bos', 
           b'bg': b'bul', 
           b'ca': b'cat', 
           b'zh': b'chi', 
           b'hr': b'hrv', 
           b'da': b'dan', 
           b'nl': b'dut', 
           b'eo': b'epo', 
           b'et': b'est', 
           b'fi': b'fin', 
           b'gl': b'glg', 
           b'ka': b'geo', 
           b'de': b'ger', 
           b'he': b'heb', 
           b'hi': b'hin', 
           b'is': b'ice', 
           b'id': b'ind', 
           b'it': b'ita', 
           b'ja': b'jpn', 
           b'kk': b'kaz', 
           b'ko': b'kor', 
           b'lv': b'lav', 
           b'lt': b'lit', 
           b'lb': b'ltz', 
           b'mk': b'mac', 
           b'ms': b'may', 
           b'no': b'nor', 
           b'oc': b'oci', 
           b'fa': b'per', 
           b'ro': b'rum', 
           b'ru': b'rus', 
           b'sr': b'scc', 
           b'sl': b'slv', 
           b'sv': b'swe', 
           b'th': b'tha', 
           b'tr': b'tur', 
           b'uk': b'ukr', 
           b'vi': b'vie'}
        if idioma not in idiomas:
            idioma = idiomas[b'es']
        else:
            idioma = idiomas[idioma]
        return idioma

    def conectar(self):
        import xmlrpclib
        return xmlrpclib.ServerProxy(self.servidor)

    def serverinfo(self):
        return self.conexion.ServerInfo()

    def login(self, username=b'', password=b''):
        try:
            estado = self.conexion.LogIn(username, password, self.idioma, self.useragent)
            if estado[b'status'] == b'200 OK':
                self.token = estado[b'token']
                return estado[b'token']
        except:
            return

        return

    def logout(self):
        self.conexion.LogOut(self.token)

    def buscar_subs(self):
        u"""Busca subtítulos por hash o por datos del vídeo"""
        if self.video.buscar_por_hash:
            datos = {b'sublanguageid': self.idioma, b'moviehash': self.video.hash, b'moviebytesize': unicode(self.video.bytesize)}
        elif self.video.buscar_por_nombre:
            if self.video.tipo == b'episode':
                datos = {b'sublanguageid': self.idioma, b'query': self.video.serie, b'season': self.video.temporada, 
                   b'episode': self.video.episodio}
            else:
                datos = {b'sublanguageid': self.idioma, b'query': self.video.titulo}
        else:
            return {}
        return self.conexion.SearchSubtitles(self.token, [datos])

    def descargar(self):
        result = self.conexion.DownloadSubtitles(self.token, [self.idsub])
        if result[b'status'] == b'200 OK':
            import base64
            self.sub = base64.b64decode(result[b'data'][0][b'data'])
            self.sub = self.video.descomprimir(self.sub)
            self.video.guardar_archivo(self.sub)
            return 0
        else:
            return 2

    def elegir_sub(self, resultados):
        u"""Elige el subtítulo más óptimo de entre los que se encuentren"""
        if not self.anotaciones:
            self.video.titulo = resultados[b'data'][0][b'MovieName']
            return resultados[b'data'][0][b'IDSubtitleFile']
        else:
            for resultado in resultados[b'data']:
                if resultado[b'SubHearingImpaired'] == b'1':
                    self.video.titulo = resultado[b'IDSubtitleFile']
                    return resultado[b'IDSubtitleFile']

            return False

    def get_subtitles(self, username=b'', password=b''):
        u"""Principal, se conecta, busca y descarga los subtítulos"""
        ret = 0
        if self.login(username, password):
            result = self.buscar_subs()
            if result.get(b'data'):
                self.idsub = self.elegir_sub(result)
                if self.idsub:
                    if not self.video.args.check:
                        self.descargar()
                    else:
                        self.video.notificacion.n(b'Subtítulos encontrados en %s' % self.sitio)
                else:
                    self.video.notificacion.n(b'No se han encontrado subtítulos en %s' % self.sitio, False)
                    ret = 1
            else:
                self.video.notificacion.n(b'No se ha encontrado el vídeo en %s' % self.sitio, False)
                ret = 1
            self.logout()
        else:
            self.video.notificacion.n(b'No se ha podido conectar a %s' % self.sitio, False)
            ret = 1
        return ret