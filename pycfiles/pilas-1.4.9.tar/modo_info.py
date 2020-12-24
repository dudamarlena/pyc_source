# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/depurador/modo_info.py
# Compiled at: 2016-08-25 21:09:54
import sys, pilasengine
from pilasengine.depurador.modo import ModoDepurador

class ModoInformacionDeSistema(ModoDepurador):
    tecla = 'F7'

    def __init__(self, pilas, depurador):
        ModoDepurador.__init__(self, pilas, depurador)
        usa_aceleracion = self._usa_aceleracion_de_video()
        self.informacion = [
         'Usa aceleración de video: %s' % usa_aceleracion,
         'Sistema: ' + sys.platform,
         'Version de pilas: ' + pilasengine.VERSION,
         'Version de python: ' + sys.subversion[0] + ' ' + sys.subversion[1],
         '',
         '',
         '',
         '',
         '']

    def _usa_aceleracion_de_video(self):
        if self.pilas.usa_aceleracion():
            return 'Sí'
        return 'No'

    def realizar_dibujado(self, painter):
        izquierda, derecha, _, abajo = self.pilas.widget.obtener_bordes()
        interpolaciones = self.pilas.utils.obtener_cantidad_de_interpolaciones()
        ancho, alto = self.pilas.obtener_area()
        self.informacion[4] = 'Interpolaciones en curso: %d' % interpolaciones
        self.informacion[5] = 'Area de juego: (%d, %d)' % (ancho, alto)
        self.informacion[6] = 'Posición de la cámara: (%d, %d)' % (self.pilas.camara.x, self.pilas.camara.y)
        self.informacion[7] = 'Rendimiento: %s cuadros por segundo' % self.pilas.widget.fps.obtener_cuadros_por_segundo()
        self.informacion[8] = 'Cantidad de actores: %d' % self.pilas.escena_actual().obtener_cantidad_de_actores()
        for i, texto in enumerate(self.informacion[::-1]):
            posicion_y = abajo + 20 + i * 20
            self._texto_absoluto(painter, texto, izquierda + 11, posicion_y - 1, color=pilasengine.colores.negro)
            self._texto_absoluto(painter, texto, izquierda + 10, posicion_y, color=pilasengine.colores.blanco)

        texto = 'Posición del mouse: (%d, %d)' % self.pilas.obtener_posicion_del_mouse()
        self._texto_absoluto(painter, texto, derecha - 9, abajo + 7, color=pilasengine.colores.negro, alineado_a_derecha=True)
        self._texto_absoluto(painter, texto, derecha - 10, abajo + 8, color=pilasengine.colores.blanco, alineado_a_derecha=True)

    def dibujar_actor(self, actor, painter):
        pass