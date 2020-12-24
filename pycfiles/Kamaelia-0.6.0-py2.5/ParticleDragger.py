# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Visualisation/PhysicsGraph/ParticleDragger.py
# Compiled at: 2008-10-19 12:19:52
"""================================
Drag handler for Topology Viewer
================================

A subclass of Kamaelia.UI.MH.DragHandler that implements "click and hold"
dragging of particles for the TopologyViewer.

Example Usage
-------------
See source for TopologyViewer.

How does it work?
-----------------
This is an implementation of Kamaelia.UI.MH.DragHandler. See that for more
details.

The detect() method uses the withinRadius method of the physics attribute of the
'app' to determine which (if any) particle the mouse is hovering over when the
drag is started. If there is no particle, then the drag does not begin.

At the start of the drag, the particle is 'frozen' to prevent motion due to the
physics model of the topology viewer. This is achieved by calling the freeze()
and unfreeze() methods of the particle. The particle is also 'selected'.

During the drag the particle's coordinates are updated and the physics model is
notified of the change.
"""
from Kamaelia.UI.MH import DragHandler

class ParticleDragger(DragHandler):
    """    ParticleDragger(event,app) -> new ParticleDragger object.
    
    Implements mouse dragging of particles in a topology viewer. Bind the
    handle(...) class method to the MOUSEBUTTONDOWN pygame event to use it (via
    a lambda function or equivalent)
                    
    Keyword Arguments:
    
    - event  -- pygame event object cuasing this
    - app    -- PyGameApp component this is happening in
    """

    def detect(self, pos, button):
        """detect( (x,y), button) -> (x,y) of particle or False if mouse (x,y) not over a particle"""
        pos = (
         int(pos[0] + self.app.left), int(pos[1] + self.app.top))
        inRange = self.app.physics.withinRadius(pos, self.app.biggestRadius)
        inRange = filter(lambda (p, rsquared): p.radius * p.radius >= rsquared, inRange)
        if len(inRange) > 0:
            best = -1
            for (p, rsquared) in inRange:
                if best < 0 or rsquared < best:
                    best = rsquared
                    self.particle = p

            self.particle.freeze()
            self.app.selectParticle(self.particle)
            return self.particle.getLoc()
        else:
            self.app.selectParticle(None)
            return False
        return

    def drag(self, newx, newy):
        """        Handler for the duration of the dragging operation.
        
        Updates the particle position as it is dragged.
        """
        self.particle.pos = (
         newx, newy)
        self.app.physics.updateLoc(self.particle)

    def release(self, newx, newy):
        """        Handler for the end of the dragging operation
        
        Updates the particle position before releasing it.
        """
        self.drag(newx, newy)
        self.particle.unFreeze()