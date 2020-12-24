# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Visualisation/Axon/AxonLaws.py
# Compiled at: 2008-10-19 12:19:52
import Kamaelia.Visualisation
from Kamaelia.Visualisation.PhysicsGraph import TopologyViewerServer, BaseParticle
from Kamaelia.Support.Particles import SimpleLaws, MultipleLaws
from pygame.locals import *
_COMPONENT_RADIUS = 32

class AxonLaws(MultipleLaws):
    """    AxonLaws([postboxBondLength]) -> new AxonLaws object.
    
    Encapsulates laws for interactions between particles of types "Component"
    and "Postbox" in a physics simulation. Subclass of MultipleLaws.
    
    Keyword arguments:
    
    - postboxBondLength  -- length of bond that represents Axon linkages (default=100)
    """

    def __init__(self, postboxBondLength=100):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        damp = 0.19999999999999996
        dampcutoff = 0.4
        maxvel = 32
        forceScaler = 1.0
        component_component = SimpleLaws(bondLength=postboxBondLength, maxRepelRadius=2.3 * postboxBondLength, repulsionStrength=10.0 * forceScaler, maxBondForce=0.0 * forceScaler, damp=damp, dampcutoff=dampcutoff, maxVelocity=maxvel)
        postbox_postbox = SimpleLaws(bondLength=postboxBondLength, maxRepelRadius=_COMPONENT_RADIUS * 1.0, repulsionStrength=0.05 * forceScaler, maxBondForce=5.0 * forceScaler, damp=damp, dampcutoff=dampcutoff, maxVelocity=maxvel)
        component_postbox = SimpleLaws(bondLength=_COMPONENT_RADIUS * 1.5, maxRepelRadius=_COMPONENT_RADIUS, repulsionStrength=0.0 * forceScaler, maxBondForce=10.0 * forceScaler, damp=damp, dampcutoff=dampcutoff, maxVelocity=maxvel)
        typesToLaws = {('component', 'component'): component_component, ('postbox', 'postbox'): postbox_postbox, 
           ('component', 'postbox'): component_postbox, 
           ('postbox', 'component'): component_postbox}
        super(AxonLaws, self).__init__(typesToLaws=typesToLaws)