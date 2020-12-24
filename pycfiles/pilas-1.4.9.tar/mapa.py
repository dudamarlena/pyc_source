# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/actores/mapa.py
# Compiled at: 2016-08-25 20:52:02
import copy, math
from pilasengine.actores.actor import Actor

class Mapa(Actor):

    def pre_iniciar(self, x=0, y=0, grilla=None, filas=20, columnas=20, densidad=1.0, restitucion=0.56, friccion=10.5, amortiguacion=0.1):
        pass

    def iniciar(self, x=0, y=0, grilla=None, filas=20, columnas=20, densidad=1.0, restitucion=0.56, friccion=10.5, amortiguacion=0.1):
        u"""Inicializa el mapa.

        :param grilla: La imagen a utilizar cómo grilla con los bloques del escenario.
        :param x: Posición horizontal del mapa.
        :param y: Posición vertical del mapa.
        :param filas: Cantidad de filas que tendrá el mapa.
        :param columnas: Cantidad de columnas que tendrá el mapa.
        :param densidad: La densidad de la física de los bloques solidos.
        :param restitucion: La restitucion de la física de los bloques solidos.
        :param friccion: La friccion de la física de los bloques solidos.
        :param amortiguacion: La amortiguacion de la física de los bloques solidos.
        """
        self.x = x
        self.y = y
        self.imagen = 'invisible.png'
        self.radio_de_colision = 15
        self.densidad = densidad
        self.restitucion = restitucion
        self.friccion = friccion
        self.amortiguacion = amortiguacion
        self.filas = filas
        self.columnas = columnas
        self.matriz_de_bloques = self._generar_matriz_de_bloques(filas, columnas)
        if not grilla:
            grilla = self.pilas.imagenes.cargar_grilla('grillas/plataformas_10_10.png', 10, 10)
        self.grilla = grilla
        self.superficie = self.pilas.imagenes.cargar_superficie(columnas * self.grilla.cuadro_ancho, filas * self.grilla.cuadro_alto)
        self.imagen = self.superficie
        self.centro_mapa_x, self.centro_mapa_y = self.superficie.centro()
        self.fijo = False
        self.actores_con_figuras_solidas = []

    def definir_figura_de_colision(self, figura):
        pass

    def actualizar(self):
        pass

    def terminar(self):
        pass

    def _generar_matriz_de_bloques(self, filas, columnas):
        cols = copy.copy([False] * columnas)
        matriz_de_bloques = []
        for indice_fila in range(filas):
            matriz_de_bloques.append(copy.copy(cols))

        return matriz_de_bloques

    def pintar_bloque(self, fila, columna, indice, es_bloque_solido=True):
        u"""Define un bloque de la grilla.

        :param fila: La fila que se definirá (comenzando desde 0).
        :param columna: La columna que se definirá (comenzando desde 0).
        :param indice: El número de cuadro referente a la grilla (comenzando desde 0).
        :param es_bloque_solido: True o False para indicar si los objetos físicos deberán colisionar con este bloque.
        """
        self.matriz_de_bloques[fila][columna] = es_bloque_solido
        self.grilla.definir_cuadro(indice)
        ancho = self.grilla.cuadro_ancho
        alto = self.grilla.cuadro_alto
        x = columna * ancho
        y = fila * alto
        if es_bloque_solido:
            dx = self.ancho / 2
            dy = self.alto / 2
            nuevo_x = self.x + x - dx + alto / 2
            nuevo_y = self.y - y + dy - ancho / 2
            Rectangulo = self.pilas.fisica.Rectangulo
            figura_de_colision = Rectangulo(nuevo_x, nuevo_y, ancho, alto, densidad=self.densidad, restitucion=self.restitucion, friccion=self.friccion, amortiguacion=self.amortiguacion, plataforma=True)
            self.actores_con_figuras_solidas.append(figura_de_colision)
        self.grilla.dibujarse_sobre_una_pizarra(self.superficie, x, y)

    def pintar_limite_de_bloques(self):
        """Dibuja los bordes de cada bloque."""
        for fila in range(self.filas):
            for columna in range(self.columnas):
                self._pintar_borde_de_grilla(fila, columna)

    def _pintar_borde_de_grilla(self, fila, columna):
        ancho = self.grilla.cuadro_ancho
        alto = self.grilla.cuadro_alto
        x = columna * ancho
        y = fila * alto
        self.superficie.rectangulo(x + 1, y + 1, ancho - 2, alto - 2)
        texto_coordenada = '%d, %d' % (fila, columna)
        self.superficie.texto(texto_coordenada, x + 3, y - 3 + alto, magnitud=8)

    def obtener_distancia_al_suelo(self, x, y, maximo):
        u"""Retorna la distancia en pixels desde un punto del mundo al suelo.

        Es importante mostrar que las coordenadas x e y son coordenadas del
        mundo, no coordenadas de mouse o relativas al mapa.

        El argumento maximo es la cantidad de pixels que tomaremos como
        valor limite de la busqueda. Por ejemplo, si colocamos 100 como
        limite y la funcion nos retorna 100 es porque no encontró un suelo
        a menos de 100 pixels. Este límite existe por una cuestión de
        eficiencia.

        :param x: Posición horizontal de referencia.
        :param y: Posición vertical de referencia.
        :param maximo: Cantidad máxima de pixels a leer.
        """
        try:
            x, y = self.convertir_de_coordenada_absoluta_a_coordenada_mapa(x, y)
            resto = int(y % self.grilla.cuadro_alto)
            if not resto and self.es_punto_solido_coordenada_mapa(x, y):
                return 0
            inicial = self.grilla.cuadro_alto - resto
            for distancia in range(inicial, maximo, self.grilla.cuadro_alto):
                if self.es_punto_solido_coordenada_mapa(x, y + distancia):
                    return distancia

        except Exception:
            return maximo

        return maximo

    def es_bloque_solido(self, fila, columna):
        u"""Indica si un determinado bloque es solido.

        Los bloques sólidos se utilizan para marcar paredes y plataformas, es
        decir que son bloques que generalmente no se pueden sobrepasar.

        :param fila: La fila que se observará.
        :param columna: La columna que se observará.
        """
        if not 0 <= fila < self.filas or not 0 <= columna < self.columnas:
            return True
            raise Exception('La fila y columna consultadas estan fuera del area del mapa.')
        return self.matriz_de_bloques[fila][columna]

    def es_punto_solido(self, x, y):
        u"""Indica si una coordenada del escenario está sobre un bloque solido.

        :param x: Posición horizontal a consultar.
        :param y: Posición vertical a consultar.

        """
        x, y = self.convertir_de_coordenada_absoluta_a_coordenada_mapa(x, y)
        return self.es_punto_solido_coordenada_mapa(x, y)

    def convertir_de_coordenada_absoluta_a_coordenada_mapa(self, x, y):
        """Toma un punto de pantalla y lo convierte a una coordenada dentro del mapa.

        :param x: Coordenada horizontal de pantalla.
        :param y: Coordenada vertical de pantalla.
        """
        try:
            dx = self.centro[0]
            dy = self.centro[1]
            x = x + dx - self.x
            y = -y + dy + self.y
        except Exception as e:
            print e

        return (
         x, y)

    def es_punto_solido_coordenada_mapa(self, x, y):
        u"""Consulta si un punto (x, y) está señalando un bloque sólido.

        :param x: Coordenada horizontal.
        :param y: Coordenada vertical.
        """
        fila = self.obtener_numero_de_fila(y)
        columna = self.obtener_numero_de_columna(x)
        return self.es_bloque_solido(fila, columna)

    def obtener_numero_de_fila(self, y):
        u"""Retorna el número de fila correspondiente a una coordenada vertical.

        :param y: La coordenada vertical (relativa al mapa, no a la pantalla).
        """
        return self._convertir_en_int(y / self.grilla.cuadro_alto)

    def obtener_numero_de_columna(self, x):
        u"""Retorna el número de columna correspondiente a una coordenada horizontal.

        :param x: La coordenada horizontal (relativa al mapa, no a la pantalla).
        """
        return self._convertir_en_int(x / self.grilla.cuadro_ancho)

    def _convertir_en_int(self, valor):
        return int(math.floor(valor))

    def _eliminar_todos_los_actores_con_figuras(self):
        u"""Elimina todos los actores que tienen física asociada.

        Este método se invoca automáticamente cuando se reinicia
        el mapa, por ejemplo cuando se edita desde tiled y se vulve
        a grabar.
        """
        for x in list(self.actores_con_figuras_solidas):
            x.eliminar()

        self.actores_con_figuras_solidas = []
        self.pilas.fisica.iterar()