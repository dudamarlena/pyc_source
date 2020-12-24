# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Visualisation/ER/ERLaws.py
# Compiled at: 2008-10-19 12:19:52
import Kamaelia.Visualisation
from Kamaelia.Visualisation.PhysicsGraph import TopologyViewerServer, BaseParticle
from Kamaelia.Support.Particles import SimpleLaws, MultipleLaws
from pygame.locals import *
_COMPONENT_RADIUS = 32

class AxonLaws(MultipleLaws):

    def __init__(self, relationBondLength=100):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        damp = 0.19999999999999996
        dampcutoff = 0.4
        maxvel = 32
        forceScaler = 1.0
        entity_entity = SimpleLaws(bondLength=relationBondLength, maxRepelRadius=2.3 * relationBondLength, repulsionStrength=10.0 * forceScaler, maxBondForce=0.0 * forceScaler, damp=damp, dampcutoff=dampcutoff, maxVelocity=maxvel)
        relation_relation = SimpleLaws(bondLength=relationBondLength, maxRepelRadius=_COMPONENT_RADIUS * 2.0, repulsionStrength=1 * forceScaler, maxBondForce=3.0 * forceScaler, damp=damp, dampcutoff=dampcutoff, maxVelocity=maxvel)
        entity_attribute = SimpleLaws(bondLength=_COMPONENT_RADIUS * 2, maxRepelRadius=_COMPONENT_RADIUS * 2, repulsionStrength=2.0 * forceScaler, maxBondForce=10.0 * forceScaler, damp=damp, dampcutoff=dampcutoff, maxVelocity=maxvel)
        entity_relation = SimpleLaws(bondLength=_COMPONENT_RADIUS * 3, maxRepelRadius=_COMPONENT_RADIUS * 3, repulsionStrength=2.0 * forceScaler, maxBondForce=10.0 * forceScaler, damp=damp, dampcutoff=dampcutoff, maxVelocity=maxvel)
        typesToLaws = {('entity', 'entity'): entity_entity, ('relation', 'relation'): relation_relation, 
           ('isa', 'relation'): relation_relation, 
           ('relation', 'isa'): relation_relation, 
           ('isa', 'isa'): relation_relation, 
           ('entity', 'relation'): entity_relation, 
           ('entity', 'isa'): entity_relation, 
           ('relation', 'entity'): entity_relation, 
           ('isa', 'entity'): entity_relation, 
           ('entity', 'attribute'): entity_attribute}
        super(AxonLaws, self).__init__(typesToLaws=typesToLaws, defaultLaw=entity_relation)