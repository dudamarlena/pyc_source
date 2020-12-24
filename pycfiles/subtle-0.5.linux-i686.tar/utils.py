# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/subtle/utils.py
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
import os, sqlite3

def separador(cadena, separador=b'=', pegar=True, doble_fila=False):
    u"""Añade una línea de caracteres para destacar / separar una cadena
    
    :param cadena:
            Cadena a destacar.
    :param separador:
            Carácter que se usará como separador.
    :param pegar:
            Devolver la cadena junto al separador o sólo el separador.
    """
    if pegar:
        cadena = cadena + b'\n' + b'%s' % separador * len(cadena)
        cadena += b'\n'
        return cadena
    return separador * len(cadena)


def recortar_url(url):
    """Elimina http://www. de una url si lo tiene, y cambia los puntos por guiones bajos.
    Para comprobar si existe en el array de webs de subtle"""
    import re
    url = re.sub(b'^http://', b'', url)
    url = re.sub(b'^www.', b'', url)
    return re.sub(b'\\.', b'_', url)


def extension(archivo):
    """Get the file extension."""
    return os.path.splitext(archivo)[(-1)].lower()


def excepciones_archivos(e):
    u"""Maneja los mensajes que se mostrarán en las excepciones de archivos"""
    mensaje = b''
    if e.errno == 13:
        mensaje = b'\nPermiso denegado.'
    elif e.errno == 28:
        mensaje = b'\nNo queda espacio en disco.'
    return mensaje


def intercambiar(variable, reemplazo=b'Desconocido'):
    """Intercambia un valor None por el reemplazo que se le diga"""
    if variable is not None:
        return variable
    else:
        return reemplazo
        return


class Notificacion(object):
    """Crea burbujas de notificación, guarda el log e imprime por pantalla"""

    def __init__(self, notificador=b'notify-send', titulo=None, icono=None, urgencia=b'normal', tiempo=None, kwargs={}):
        self.quiet = kwargs.get(b'quiet', False)
        self.verbose = kwargs.get(b'verbose', False)
        if not self.quiet:
            self.notificador = notificador
            self.comprobar_burbuja()
            if self.mostrar_burbuja:
                self.titulo = titulo
                self.icono = icono
                self.urgencia = urgencia
                self.tiempo = tiempo
        else:
            self.mostrar_burbuja = False
            self.registro = False

    def notificar(self, mensaje, mostrar_burbuja=True):
        """Principal, lanza las tres funciones"""
        if not self.quiet:
            if self.mostrar_burbuja and mostrar_burbuja or self.mostrar_burbuja and self.verbose:
                self.burbuja(mensaje)
            print mensaje

    def n(self, mensaje, mostrar_burbuja=True):
        u"""Máscara de notificar"""
        self.notificar(mensaje, mostrar_burbuja)

    def burbuja(self, mensaje):
        u"""Crea una burbuja de notificación"""
        import subprocess
        burbuja = [
         b'notify-send']
        if self.icono:
            burbuja.append(b'-i')
            burbuja.append(self.icono)
        if self.urgencia in ('low', 'normal', 'critical'):
            burbuja.append(b'-u')
            burbuja.append(self.urgencia)
        if self.tiempo:
            burbuja.append(b'-t')
            burbuja.append(str(self.tiempo))
        if self.titulo:
            burbuja.append(self.titulo)
        burbuja.append(mensaje)
        subprocess.Popen(burbuja)

    def comprobar_burbuja(self):
        u"""Comprueba si existe un método de crear burbujas de notificación"""
        from distutils.spawn import find_executable
        if find_executable(self.notificador) is not None:
            self.mostrar_burbuja = True
            return 0
        else:
            self.mostrar_burbuja = False
            return 1
            return

    def registro(self):
        pass


def subtle_extensiones():
    return ('.mp4', '.avi', '.mkv')


class Bbdd:
    """Abstrae la base de datos sqlite"""

    def __init__(self, ruta):
        self.con = None
        self.conectar(ruta)
        return

    def conectar(self, ruta):
        """Crea o conecta la base de datos"""
        try:
            try:
                self.con = sqlite3.connect(ruta)
            except Exception as e:
                notificar(b'Ha ocurrido un error al conectar a la base de datos.')
                notificar(e, False)

        finally:
            return self.con

    def desconectar(self):
        """Desconecta la base de datos"""
        self.con.close()

    def ex(self, sql, args=None, commit=False, many=False):
        u"""Ejecuta la sentencia sql, llamada ex (execute) para acortar
        args: array de variables de sustitución para los comodines del sql"""
        c = self.con.cursor()
        try:
            if args is not None:
                if not isinstance(args, (list, tuple)):
                    args = (
                     args,)
            else:
                args = ()
            if commit and many:
                c.executemany(sql, args)
            else:
                c.execute(sql, args)
            if not commit:
                return c.fetchall()
            self.con.commit()
        except Exception as e:
            notificar(b'Ha ocurrido un error al interactuar con la base de datos')
            print e
            self.con.rollback()
            return 1

        c.close()
        return

    def ex_m(self, sql, args=None, commit=False):
        """Ejecuta varias sentencias sql"""
        return self.ex(sql, args, commit, True)

    def w(self, sql, args=None):
        u"""Máscara de ex() para hacer commit en la bd, w(write) para acortar"""
        return self.ex(sql, args, True)

    def w_m(self, sql, args=None):
        u"""Máscara de ex() para hacer commit de varias sentencias en la bd, w(write) para acortar"""
        return self.ex(sql, args, True, True)

    def r(self, sql, args=None):
        u"""Máscara de ex() para leer de la base de datos"""
        return self.ex(sql, args, False)

    def r_range(self, sql, args=None, limit=1, offset=0):
        u"""Máscara de r() para leer X filas de la base de datos"""
        sql += b'LIMIT %d OFFSET %d' % (limit, offset)
        return self.r(sql, args)

    def r_one(self, sql, args=None):
        u"""Máscara de r() para leer la primera fila de la base de datos"""
        return self.r_range(sql, args)