# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/fisica/contact_listener.py
# Compiled at: 2016-08-25 20:52:02
import Box2D as box2d

class ObjetosContactListener(box2d.b2ContactListener):
    """Gestiona las colisiones de los objetos para ejecutar funcionés."""

    def __init__(self, pilas):
        box2d.b2ContactListener.__init__(self)
        self.pilas = pilas

    def BeginContact(self, *args, **kwargs):
        fixture_1 = args[0].fixtureA
        fixture_2 = args[0].fixtureB
        self.detener_figuras_estaticas(args[0])
        self.pilas.colisiones.notificar_colision(fixture_1, fixture_2)
        self.agregar_colision(fixture_1, fixture_2)

    def agregar_colision(self, fixture_1, fixture_2):
        actor_asociado_1 = fixture_1.userData.get('actor', None)
        actor_asociado_2 = fixture_2.userData.get('actor', None)
        figura_1 = fixture_1.userData.get('figura', None)
        figura_2 = fixture_2.userData.get('figura', None)
        if figura_1 and figura_2 and figura_1 != figura_2:
            figura_1.figuras_en_contacto.append(figura_2)
            figura_2.figuras_en_contacto.append(figura_1)
        return

    def eliminar_colision(self, fixture_1, fixture_2):
        actor_asociado_1 = fixture_1.userData.get('actor', None)
        actor_asociado_2 = fixture_2.userData.get('actor', None)
        figura_1 = fixture_1.userData.get('figura', None)
        figura_2 = fixture_2.userData.get('figura', None)
        if figura_1 and figura_2 and figura_1 != figura_2:
            if figura_2 in figura_1.figuras_en_contacto:
                figura_1.figuras_en_contacto.remove(figura_2)
            if figura_1 in figura_2.figuras_en_contacto:
                figura_2.figuras_en_contacto.remove(figura_1)
        return

    def EndContact(self, *args, **kwargs):
        fixture_1 = args[0].fixtureA
        fixture_2 = args[0].fixtureB
        self.detener_figuras_estaticas(args[0])
        self.eliminar_colision(fixture_1, fixture_2)

    def PreSolve(self, contact, old):
        fixture_1 = contact.fixtureA
        fixture_2 = contact.fixtureB
        self.detener_figuras_estaticas(contact)
        if fixture_1.userData['sensor'] or fixture_2.userData['sensor']:
            contact.enabled = False

    def PostSolve(self, contact, old):
        self.detener_figuras_estaticas(contact)

    def detener_figuras_estaticas(self, contact):
        fixture_1 = contact.fixtureA
        fixture_2 = contact.fixtureB

        def detener(body):
            body.linearVelocity = (0, 0)
            body.angularVelocity = 0

        if not fixture_1.userData['dinamica']:
            detener(fixture_1.body)
        if not fixture_2.userData['dinamica']:
            detener(fixture_2.body)