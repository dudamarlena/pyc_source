# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Support/Particles/Particle.py
# Compiled at: 2008-10-19 12:19:52
"""===============================================
Particle in a discrete time physics simulation
===============================================

The Particle class provides the basis for particles in a ParticleSystem
simulation. The particles handle their own physics interaction calculations.
You can have as many, or few, spatial dimensions as you like.

Extend this base class to add extra functionality, such as the ability to render
to a graphics display (see RenderingParticle for an example of this)

Example Usage
-------------
See ParticleSystem

How does it work?
-----------------

Particle maintains lists of other particles it is bonded to. The bonds have
direction, so the bonding information is stored in two lists - bondedTo and
bondedFrom.

Bonds are made and broken by calling the makeBond(...), breakBond(...) and
breakAllBonds(...) methods.

Particle calculates its interactions with other particles when the
doInteractions(...) method is called. This must be supplied with an object
containins the laws to apply, and another providing the ability to search for
particles within a given distance of a point. See SimpleLaws/MultipleLaws and
SpatialIndexer respectively. This updates the velocity of the particle but not
its actual position.

The particle's position is only updated when the update(...) method is called.

A simulation system should calculate each simulation cycle as a two step
process: First, for all particles, calling doInteractions(...). Second, for all
particles, calling update(...).

A particle can be frozen in place by calling freeze() and unFreeze(). This
forces the particle's velocity to zero, meaning it doesn't move because of
interactions with other particles.

The simulation must have a 'tick' counter, whose value changes (increments)
every simulation cycle. Particle stores the last tick value it was presented
with so that, when interacting with other particles, it can see which others
have already been processed in the current cycle. This way, it avoids
accidentaly calculating some interactions twice.
"""
from operator import sub as _sub
from operator import add as _add
from operator import mul as _mul

class Particle(object):
    """Particle within a physics system with an arbitrary number of dimensions.
    
    Represents a particle that interacts with other particles. One set of forces are applied for
    those particles that are unbonded. Interactions between bonded particles are controlled by another
    set of forces.
    
    Bonds are bi-directional. Establishing a bond from A to B, will also establish it back from B to A.
    Similarly, breaking the bond will do so in both directions too.
    """

    def __init__(self, position, initialTick=0, ptype=None, velocity=None, ID=None):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(Particle, self).__init__()
        self.pos = position
        self.tick = initialTick
        self.static = False
        self.ptype = ptype
        self.bondedTo = []
        self.bondedFrom = []
        if velocity != None:
            self.velocity = list(velocity)
        else:
            self.velocity = [ 0.0 for xx in self.pos ]
        if ID is None:
            self.ID = str(id(self))
        else:
            self.ID = ID
        return

    def getBonded(self):
        """Return list of particles this one is bonded to (outgoing bonds)."""
        return self.bondedTo

    getBondedTo = getBonded

    def getBondedFrom(self):
        """Return list of particles that bond to this one (incoming bonds)."""
        return self.bondedFrom

    def makeBond(self, particles, index):
        """       makeBond(particles, index) -> bonds to particle in particles[index]

       Make a bond between this particle and another.
       
       If the bond already exists, then this method does nothing.
       """
        target = particles[index]
        if target not in self.bondedTo:
            self.bondedTo += [particles[index]]
            particles[index].bondedFrom += [self]

    def breakBond(self, particles, index):
        """        breakBond(particles, index) -> breaks bond to particle in particles[index]

        Breaks the bond between this particle and another.

        If the bond doesnt already exist, this method will fail.
        """
        self.bondedTo.remove(particles[index])
        particles[index].bondedFrom.remove(self)

    def breakAllBonds(self, outgoing=True, incoming=True):
        """        breakAllBonds([outgoing][,incoming]) -> breaks all bonds

        Breaks all bonds between this particle and any others.

        If outgoing=True (default=True) then all bond *from* this particle to
        other particles are broken.

        If incoming=True (default=True) then all bonds *to* this particle from
        other particles are broken.
        """
        if outgoing:
            for bondTo in self.bondedTo:
                bondTo.bondedFrom.remove(self)

            self.bondedTo = []
        if incoming:
            for bondFrom in self.bondedFrom:
                bondFrom.bondedTo.remove(self)

            self.bondedFrom = []

    def getLoc(self):
        """Return current possition vector (x,y,z, ...)"""
        return self.pos

    def freeze(self):
        """Lock the particle in place"""
        self.static = True

    def unFreeze(self):
        """Allow the particle to move freely"""
        self.static = False

    def distSquared(self, altpos):
        """Returns the distance squared of this particle from the specified position"""
        return sum(map(lambda x1, x2: (x1 - x2) * (x1 - x2), self.pos, altpos))

    def doInteractions(self, particleIndex, laws, tick):
        """        Interact with other particles according to the provided laws, adjusting
        the velocities of this particles and those it interacts with.

        Updates current 'tick' to the supplied value and only interacts with
        particles not also on the same 'tick' value.

        Keyword args:
        
        - particleIndex  -- index of all particles, implementing withinRadius(...) method (see SpatialIndexer)
        - laws           -- object implementing interaction laws (see SimpleLaws)
        - tick           -- time index of current simulation cycle
        """
        self.tick = tick
        _bonded = laws.bonded
        _unbonded = laws.unbonded
        __add, __sub, __mul = _add, _sub, _mul
        bonded = self.getBondedTo() + self.getBondedFrom()
        for particle in bonded:
            if particle.tick != self.tick:
                ds = self.distSquared(particle.pos)
                if ds > 0.0:
                    dist = ds ** 0.5
                    dvelocity = _bonded(self.ptype, particle.ptype, dist, ds)
                    deltas = map(__sub, particle.pos, self.pos)
                    dv_d = dvelocity / dist
                    scaleddeltas = map(__mul, deltas, [dv_d] * len(deltas))
                    self.velocity = map(__add, self.velocity, scaleddeltas)
                    particle.velocity = map(__sub, particle.velocity, scaleddeltas)

        filter = lambda particle: particle.tick != self.tick and particle not in bonded + [self]
        particles = particleIndex.withinRadius(self.pos, laws.particleMaxInteractRadius(self.ptype), filter)
        for (particle, ds) in particles:
            if ds > 0.0:
                dist = ds ** 0.5
                dvelocity = _unbonded(self.ptype, particle.ptype, dist, ds)
                deltas = map(__sub, particle.pos, self.pos)
                dv_d = dvelocity / dist
                scaleddeltas = map(__mul, deltas, [dv_d] * len(deltas))
                self.velocity = map(__add, self.velocity, scaleddeltas)
                particle.velocity = map(__sub, particle.velocity, scaleddeltas)

    def update(self, laws):
        """Update this particle's position, also apply dampening to velocity
        
        laws.dampening( ptype, velocity ) should return the new velocity, that is then applied.
        """
        if self.static:
            self.velocity = [ 0 for x in self.velocity ]
        else:
            self.velocity = laws.dampening(self.ptype, self.velocity)
            self.pos = map(_add, self.pos, self.velocity)