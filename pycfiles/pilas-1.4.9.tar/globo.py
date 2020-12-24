# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/actores/globo.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.actores.actor import Actor

class Globo(Actor):
    """Representa un cuadro de dialogo estilo historietas.

    El actor se tiene que inicializar con una cadena de texto:

        >>> globo = pilas.actores.Globo("Hola mundo")

    .. image:: ../../pilas/data/manual/imagenes/actores/globo.png
    """

    def __init__(self, pilas, texto='', x=0, y=0, dialogo=None, avance_con_clicks=True, autoeliminar=False, ancho_globo=0, alto_globo=0, objetivo=None):
        u""" Constructor del Globo

        :param texto: Texto a mostrar en el globo.
        :type texto: boolean
        :param x: posicion horizontal del globo.
        :type x: int
        :param y: posicion vertical del globo.
        :type y: int
        :param dialogo: Dialogo que contiene las frases a mostrar en el globo.
        :type dialogo: Dialogo
        :param avance_con_clicks: Permite avanzar el dialogo pulsando el ratón.
        :type avance_con_clicks: boolean
        :param autoeliminar: Indica si se desea eliminar el globo cuando
                             pasen 3 segundos.
        :type autoeliminar: boolean
        :param ancho_globo: Estabece el ancho del globo en pixeles.
        :type ancho_globo: int
        :param alto_globo: Estabece el alto del globo en pixeles.
        :type alto_globo: int

        """
        self.dialogo = dialogo
        Actor.__init__(self, pilas, x=x, y=y)
        self.imagen = 'invisible.png'
        self.objetivo = objetivo
        ancho, alto = pilas.utils.obtener_area_de_texto(texto)
        if ancho_globo == 0:
            ancho = int(ancho + 12 - ancho % 12)
        elif ancho_globo > ancho:
            ancho = ancho_globo
        else:
            ancho = int(ancho + 12 - ancho % 12)
        if alto_globo == 0:
            alto = int(alto + 12 - alto % 12)
        else:
            alto = alto + alto_globo
        self.imagen = pilas.imagenes.cargar_superficie(ancho + 36, alto + 24 + 35)
        self._pintar_globo(ancho, alto)
        self.imagen.texto(texto, 17, 20)
        self.centro = ('derecha', 'abajo')
        self.escala = 0.1
        self.escala = ([1], 0.2)
        self.ancho_globo = ancho
        self.alto_globo = alto
        if avance_con_clicks:
            self.pilas.escena_actual().click_de_mouse.conectar(self.cuando_quieren_avanzar)
        if autoeliminar:
            pilas.escena_actual().tareas.una_vez(3, self.eliminar)
        self.x = x
        self.y = y

    def colocar_origen_del_globo(self, x, y):
        u""" Cambia la posicion del globo para que el punto de donde se emite el
        globo sea (x, y).
        :param x: Posición horizontal del globo.
        :type x: int
        :param y: Posición vertical del globo.
        :type y: int
        """
        self.x = x
        self.y = y

    def cuando_quieren_avanzar(self, *k):
        u"""Función que se ejecuta al hacer click para avanzar o
        eliminar el globo.
        """
        if self.dialogo:
            self.dialogo.avanzar_al_siguiente_dialogo()
        else:
            self.eliminar()

    def _pintar_globo(self, ancho, alto):
        imagen = self.pilas.imagenes.cargar('globo.png')
        self.imagen.pintar_parte_de_imagen(imagen, 0, 0, 12, 12, 0, 0)
        for x in range(0, int(ancho) + 12, 12):
            self.imagen.pintar_parte_de_imagen(imagen, 12, 0, 12, 12, 12 + x, 0)

        self.imagen.pintar_parte_de_imagen(imagen, 100, 0, 12, 12, 12 + int(ancho) + 12, 0)
        for y in range(0, int(alto) + 12, 12):
            self.imagen.pintar_parte_de_imagen(imagen, 0, 12, 12, 12, 0, 12 + y)
            for x in range(0, int(ancho) + 12, 12):
                self.imagen.pintar_parte_de_imagen(imagen, 12, 12, 12, 12, 12 + x, 12 + y)

            self.imagen.pintar_parte_de_imagen(imagen, 100, 12, 12, 12, 12 + int(ancho) + 12, 12 + y)

        self.imagen.pintar_parte_de_imagen(imagen, 0, 35, 12, 12, 0, 0 + int(alto) + 12 + 12)
        for x in range(0, int(ancho) + 12, 12):
            self.imagen.pintar_parte_de_imagen(imagen, 12, 35, 12, 12, 12 + x, 0 + int(alto) + 12 + 12)

        self.imagen.pintar_parte_de_imagen(imagen, 100, 35, 12, 12, 12 + int(ancho) + 12, 0 + int(alto) + 12 + 12)
        self.imagen.pintar_parte_de_imagen(imagen, 67, 35, 33, 25, int(ancho) - 12, 0 + int(alto) + 12 + 12)

    def actualizar(self):
        if self.objetivo:
            self.x = self.objetivo.x
            self.y = self.objetivo.y