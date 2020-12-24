# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/subtle/main.py
# Compiled at: 2013-02-21 11:08:14
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
import sys, os
sys.path.insert(0, os.path.abspath('..'))
from subtle import Video

def main():
    u"""
    Función principal del script
    """
    args = sys.argv
    if len(args) > 1:
        ret = 0
        for arg in args[1:]:
            capi = Video(arg)
            if capi.cargar_datos() == 0:
                subs_es = capi.descargar_sub_subtitulos_es()
                add = 0
                if subs_es == 1:
                    add = capi.descargar_sub_addic7ed()
                    if add == 1:
                        print 'No se han encontrado subtítulos'
                if subs_es == 2 or add == 2:
                    ret = 2
                ret = 0
            else:
                ret = 3

        return ret
    print 'Uso: subtle [nombre del vídeo]'
    return 0


if __name__ == '__main__':
    sys.exit(main())