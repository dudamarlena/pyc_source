# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/subtle/__main__.py
# Compiled at: 2013-07-07 08:15:11
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
import os, sys, argparse, time
from watchdog.observers import Observer
from core import *
from utils import *
import webs
nombre_programa = b'Subtle'
version_programa = b'0.3'
autor_programa = b'Fran Macía (fj.macia.espin@gmail.com)'

def main():
    u"""Controla si se monitoriza una carpeta o se buscan subtítulos normalmente"""
    parser = argumentos()
    args = parser.parse_args()
    ico = ruta_icono()
    notificacion = Notificacion(titulo=nombre_programa, icono=ico)
    if args.videos:
        if args.daemon:
            if os.path.isdir(args.videos[0]):
                notificacion.n(b'Monitorizando carpeta %s' % args.videos[0].decode(b'utf-8'), kwargs=args.__dict__)
                ret = monitorizar()
                notificacion.n(b'Finalizando monitorización')
            else:
                notificacion.n(b'Se debe introducir una carpeta a monitorizar.')
        else:
            for video in args.videos:
                ret = get_subtitles(video, args)

        return ret
    parser.print_help()
    return 0


def monitorizar(args):
    event_handler = AddedHandler(args)
    observer = Observer()
    observer.schedule(event_handler, args.videos[0], recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()

    observer.join()
    return 0


def argumentos():
    """Parsea los argumentos que le lleguen al programa"""
    parser = argparse.ArgumentParser(description=b'Descarga archivos de subtítulos para series', usage=b'Uso: %(prog)s [opciones] video1 [video2 ...]', add_help=False)
    parser.add_argument(b'-v', b'--verbose', action=b'store_true', help=b'Ver mensajes de depuración')
    parser.add_argument(b'-q', b'--quiet', action=b'store_true', help=b'No mostrar nada por pantalla')
    parser.add_argument(b'-h', b'--help', action=b'store_true', help=b'Muestra este mensaje de ayuda')
    parser.add_argument(b'-i', b'--info', action=b'store_true', help=b'Mostrar la información del vídeo y salir')
    parser.add_argument(b'-f', b'--force', action=b'store_true', help=b'Forzar sobreescritura de subtítulos ya existentes')
    parser.add_argument(b'-t', b'--title', action=b'store_true', help=b'Añade el título al nombre del archivo de vídeo si no lo tiene')
    parser.add_argument(b'-c', b'--check', action=b'store_true', help=b'Solo comprueba la existencia del subtítulo sin descargarlo')
    parser.add_argument(b'-w', b'--web', help=b'Especificar directamente la web en la que buscar')
    parser.add_argument(b'-d', b'--daemon', action=b'store_true', help=b'Ejecutar en segundo plano y autodescargar subtítulos cuando aparezcan vídeos nuevos')
    parser.add_argument(b'-l', b'--language', help=b'Especificar el idioma. Por defecto, español')
    parser.add_argument(b'-a', b'--annotations', action=b'store_true', help=b'Especificar si se quieren subtítulos con anotaciones')
    parser.add_argument(b'-V', b'--version', action=b'version', version=b'%s versión %s, creado por %s' % (nombre_programa, version_programa, autor_programa), help=b'Muestra la versión del programa')
    parser.add_argument(b'-F', b'--folder', help=b'Especificar la ruta donde se descargarán los subtítulos')
    parser.add_argument(b'videos', nargs=b'*')
    return parser


def get_subtitles(archivo, args):
    u"""Busca subtítulos para un archivo"""
    ret = None
    video = Video(archivo, args)
    video.notificacion.n(separador(b'\nVídeo: %s' % (video.nombre_video + video.extension)), False)
    if args.info or args.force or not os.path.exists(os.path.join(video.ruta, b'%s.srt' % video.nombre_video)):
        if not args.web:
            if not video.buscar_por_hash and not video.buscar_por_nombre:
                video.notificacion.n(b'No se puede buscar subtítulos para este archivo..')
            if video.buscar_por_hash:
                web = webs.opensubtitles_org(video)
                ret = web.get_subtitles()
            if ret != 0 and video.buscar_por_nombre:
                for sitio in webs.sitios:
                    web = getattr(webs, sitio)(video)
                    ret = web.get_subtitles()
                    if ret == 0:
                        break

        else:
            web_recortada = recortar_url(args.web)
            if web_recortada in webs.sitios:
                web = getattr(webs, web_recortada)(video)
                ret = web.get_subtitles()
            else:
                video.notificacion.n(b'No se pueden buscar subtítulos en %s' % args.web)
            if ret == 1:
                video.notificacion.n(b'No se han encontrado subtítulos.')
            return ret
        video.notificacion.n(b'Ya existen los subtítulos.')
    else:
        video.notificacion.n(video.__str__())
        ret = 0
    return ret


if __name__ == b'__main__':
    sys.exit(main())