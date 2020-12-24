# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/subtle/core.py
# Compiled at: 2013-11-02 19:51:56
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
import os, re, sys, guessit
try:
    import urllib2
    python_vers = 2
except:
    import urllib.request, urllib.error, urllib.parse
    python_vers = 3

from utils import *
from watchdog.events import FileSystemEventHandler

class Web(object):
    """Métodos relacionados con las webs, clase padre"""

    def abrir_url(self, url):
        """Lee el contenido de una url"""
        try:
            if python_vers == 2:
                html = urllib2.urlopen(url).read()
            else:
                html = urllib.request.urlopen(url).read()
            return html
        except urllib2.HTTPError as e:
            if e.code == 404:
                self.video.notificacion.n(b'No existe la página que se ha buscado.')
        except urllib2.URLError as e:
            self.video.notificacion.n(b'No se ha podido conectar a %s.' % self.sitio, False)
            return False

    def descargar(self):
        request = urllib2.Request(self.link)
        request.add_header(b'Referer', self.sitio)
        subs = self.abrir_url(request)
        if subs:
            self.video.guardar_archivo(subs)
            return 0
        else:
            return 1

    def sacar_id(self):
        pass

    def sacar_titulo(self):
        pass

    def existe_sub(self):
        pass

    def idioma(self):
        pass

    def version(self):
        pass

    def comprobar_version(self, version_video, version_web):
        u"""Comprueba si la versión de la web es la misma que la del archivo y 
        las equivalencias entre versiones"""
        if version_video.lower() in ('lol', 'sys', 'dimension', 'afg'):
            version_a_buscar = b'lol|sys|dimension|afg'
        elif version_video.lower() in ('xii', 'immerse', 'asap'):
            version_a_buscar = b'xii|immerse|asap'
        else:
            version_a_buscar = version_video
        return re.search(version_a_buscar, version_web, re.IGNORECASE)


def ruta_icono():
    """Devuelve la ruta del icono del programa"""
    if sys.platform == b'win32':
        rutas = os.path.join(os.getcwd(), b'subtle.ico')
    else:
        rutas = (
         b'/usr/share/pixmaps/subtle.ico', os.path.normpath(os.path.join(os.path.realpath(__file__), b'..', b'subtle.ico')))
    for ruta in rutas:
        if os.path.exists(ruta):
            return ruta

    return


class Video(object):
    """Métodos relacionados con los archivos"""

    def __init__(self, archivo, args):
        self.args = args
        self.archivo = archivo.decode(b'utf-8')
        self.ruta_original = os.path.dirname(self.archivo)
        self.ruta = (self.args.folder or self).ruta_original if 1 else self.args.folder
        self.nombre_video, self.extension = os.path.splitext(os.path.basename(self.archivo))
        ico = ruta_icono()
        self.notificacion = Notificacion(titulo=self.nombre_video + self.extension, icono=ico)
        self.hashfile()
        self.guess()

    def guess(self):
        """Extrae los datos del nombre del archivo y los carga en las variables"""
        self.version = None
        self.serie = None
        self.temporada = None
        self.episodio = None
        self.titulo = None
        self.codec = None
        self.formato = None
        self.tamano = None
        self.tipo = None
        guess = guessit.guess_video_info(self.archivo)
        if guess[b'type'] == b'episode':
            self.version = guess.get(b'releaseGroup')
            self.serie = guess.get(b'series')
            self.temporada = guess.get(b'season')
            self.episodio = guess.get(b'episodeNumber')
            self.titulo = guess.get(b'title')
            self.codec = guess.get(b'videoCodec')
            self.formato = guess.get(b'format')
            self.tamano = guess.get(b'screenSize')
            self.tipo = guess.get(b'type')
            self.buscar_por_nombre = True if self.version is not None else False
        elif guess[b'type'] == b'movie':
            self.tipo = guess.get(b'type')
            self.titulo = guess.get(b'title')
            self.buscar_por_nombre = False
        else:
            self.buscar_por_nombre = False
        if self.buscar_por_nombre == True:
            return 0
        else:
            return 1

    def guardar_archivo(self, datos):
        """Crea un archivo a partir de los datos de una variable"""
        try:
            if self.args.title:
                self.renombrar(self.titulo)
            archivo = open(os.path.join(self.ruta, b'%s.srt' % self.nombre_video), b'wb')
            archivo.write(datos)
            archivo.close()
            self.notificacion.n(b'Guardando archivo de subtítulos.')
            return 0
        except IOError as e:
            mensaje = b'Ha ocurrido un error al guardar el archivo.'
            mensaje += excepciones_archivos(e)
            self.notificacion.n(mensaje)
            return 2

    def renombrar(self, nuevo_nombre, insertar=True):
        """Renombra el archivo"""
        try:
            if insertar:
                patron = re.compile(b'.*E\\d\\d|.*\\dX\\d\\d', re.IGNORECASE)
                cadena1 = re.search(patron, self.nombre_video).group(0)
                cadena2 = re.sub(patron, b'', self.nombre_video)
                self.nombre_video = (b'.').join((cadena1, nuevo_nombre.replace(b' ', b'.') + cadena2))
            else:
                self.nombre_video = nuevo_nombre
            if os.path.exists(self.archivo):
                os.rename(self.archivo, os.path.join(self.ruta_original, self.nombre_video + self.extension))
            return 0
        except IOError as e:
            mensaje = b'Ha ocurrido un error al renombrar el archivo.'
            mensaje += excepciones_archivos(e)
            self.notificacion.n(mensaje)
            return 2

    def cambiar_ruta(self, nueva_ruta):
        u"""Cambia la ruta en la que se guardará el archivo de subtítulos"""
        self.ruta = nueva_ruta
        return 0

    def existe_archivo_subs(self):
        u"""Comprueba si ya existe un archivo de subtítulos"""
        if os.path.exists(os.path.join(self.ruta, b'%s.srt' % self.nombre_video)):
            return True
        else:
            return False

    def descomprimir(self, archivo):
        """Descomprime un archivo gzip"""
        import zlib
        try:
            return zlib.decompress(archivo, 16 + zlib.MAX_WBITS)
        except:
            self.notificacion.n(b'No se ha podido descomprimir el archivo')
            return 0

    def hashfile(self):
        u"""Crea el hash de un archivo, para buscar en Opensubtitles (código cogido de su página)"""
        import struct
        try:
            self.bytesize = os.path.getsize(self.archivo)
            longlongformat = str(b'q')
            bytesize = struct.calcsize(longlongformat)
            f = open(self.archivo, b'rb')
            filesize = os.path.getsize(self.archivo)
            hash_num = filesize
            if filesize < 131072:
                return b'SizeError'
            for x in range(65536 / bytesize):
                buff = f.read(bytesize)
                l_value, = struct.unpack(longlongformat, buff)
                hash_num += l_value
                hash_num = hash_num & 18446744073709551615

            f.seek(max(0, filesize - 65536), 0)
            for x in range(65536 / bytesize):
                buff = f.read(bytesize)
                l_value, = struct.unpack(longlongformat, buff)
                hash_num += l_value
                hash_num = hash_num & 18446744073709551615

            f.close()
            returnedhash = b'%016x' % hash_num
            self.hash = returnedhash
            self.buscar_por_hash = True
            return returnedhash
        except:
            self.hash = b'IOError'
            self.bytesize = 0
            self.buscar_por_hash = False
            return self.hash

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        if self.tipo == b'episode':
            variables = (
             self.ruta, self.nombre_video,
             self.extension, self.tipo, self.serie,
             self.temporada, self.episodio,
             self.version, self.codec,
             self.titulo,
             self.formato, self.tamano)
            variables = map(intercambiar, variables)
            datos = b'Ruta del archivo: %s\nNombre del vídeo: %s\nExtensión: %s\nTipo: %s\nSerie: %s\nTemporada: %s\nEpisodio: %s\nVersión: %s\nCódec: %s\nNombre del episodio: %s\nFormato: %s\nTamaño pantalla: %s\n' % tuple(variables)
        elif self.tipo == b'movie':
            variables = (
             self.ruta, self.nombre_video, self.extension, self.titulo)
            variables = map(intercambiar, variables)
            datos = b'Ruta del archivo: %s\nNombre del vídeo: %s\nExtensión: %s\nTipo de vídeo: Película\nTítulo: %s\n' % tuple(variables)
        else:
            datos = b'%s\nNo se han podido extraer los datos.' % self.archivo
        return datos


class AddedHandler(FileSystemEventHandler):
    """Controla qué hacer cuando aparecen nuevos archivos"""

    def __init__(self, args):
        self.args = args

    def on_created(self, event):
        get_subtitles(event.src_path, self.args)

    def on_moved(self, event):
        get_subtitles(event.dest_path, self.args)