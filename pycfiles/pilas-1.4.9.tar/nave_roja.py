# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/actores/nave_roja.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.actores.actor import Actor

class NaveRoja(Actor):

    def pre_iniciar(self, x=0, y=0):
        self.x = x
        self.y = y
        self.ruta_imagen_normal = 'nave_roja/nave.png'
        self.ruta_imagen_izquierda = 'nave_roja/nave_izquierda.png'
        self.ruta_imagen_derecha = 'nave_roja/nave_derecha.png'
        self.radio_de_colision = 33
        self.velocidad_x = 0
        self.velocidad_y = 0
        self.velocidad = 5
        self.disparos = []
        self._contador_demora = 6
        self.demora_entre_disparos = 5
        self.disparo_doble = True
        self.cuando_elimina_enemigo = False
        self.aprender(self.pilas.habilidades.PuedeExplotar)

    def actualizar(self):
        control = self.pilas.control
        self.x += self.velocidad_x
        self.y += self.velocidad_y
        if control.izquierda:
            self.velocidad_x -= self.velocidad
            self.imagen = self.ruta_imagen_izquierda
        elif control.derecha:
            self.velocidad_x += self.velocidad
            self.imagen = self.ruta_imagen_derecha
        else:
            self.imagen = self.ruta_imagen_normal
        if control.arriba:
            self.velocidad_y += self.velocidad
        elif control.abajo:
            self.velocidad_y -= self.velocidad
        if control.boton:
            self.intenta_disparar()
        self._contador_demora += 1
        self.velocidad_x *= 0.5
        self.velocidad_y *= 0.5

    def disparar(self):
        self.intenta_disparar()

    def terminar(self):
        pass

    def intenta_disparar(self):
        if self._contador_demora > self.demora_entre_disparos:
            self._contador_demora = 0
            self.crear_disparo()

    def crear_disparo(self):
        if self.disparo_doble:
            disparo1 = self.pilas.actores.DisparoLaser(x=self.izquierda + 10, y=self.y, rotacion=90)
            self.disparos.append(disparo1)
            disparo1.cuando_se_elimina = self._cuando_elimina_disparo
            disparo2 = self.pilas.actores.DisparoLaser(x=self.derecha - 10, y=self.y, rotacion=90)
            self.disparos.append(disparo2)
            disparo2.cuando_se_elimina = self._cuando_elimina_disparo
            disparo1.z = self.z + 1
            disparo2.z = self.z + 1
        else:
            disparo1 = self.pilas.actores.DisparoLaser(x=self.x, y=self.y, rotacion=90)
            self.disparos.append(disparo1)
            disparo1.z = self.z + 1
            disparo1.cuando_se_elimina = self._cuando_elimina_disparo

    def _cuando_elimina_disparo(self, disparo):
        if disparo in self.disparos:
            self.disparos.remove(disparo)

    def definir_enemigos(self, grupo, cuando_elimina_enemigo=None):
        """Hace que una nave tenga como enemigos a todos los actores del grupo."""
        self.cuando_elimina_enemigo = cuando_elimina_enemigo
        self.pilas.colisiones.agregar(self.disparos, grupo, self.hacer_explotar_al_enemigo)

    def hacer_explotar_al_enemigo(self, mi_disparo, el_enemigo):
        u"""Es el método que se invoca cuando se produce una colisión 'tiro <-> enemigo'
        """
        mi_disparo.eliminar()
        el_enemigo.eliminar()
        if self.cuando_elimina_enemigo:
            self.cuando_elimina_enemigo()