# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: troy/overlay/overlay.py
# Compiled at: 2014-02-24 20:40:00
__author__ = 'TROY Development Team'
__copyright__ = 'Copyright 2013, RADICAL'
__license__ = 'MIT'
import radical.utils as ru, troy.utils as tu
from troy.constants import *
import troy

@ru.Lockable
class Overlay(tu.Properties, tu.Timed):
    """
    The `Overlay` class represents a resource overlay which is managed by Troy,
    i.e. in application and user space.  It contains a set of :class:`Pilots`, 
    which represent the resource capabilities of the overlay.

    Overlay instances are owned by the :class:`OverlayManager` class -- only
    that class should change its composition and state (but Overlay may get
    created by the :class:`troy.Planner`).

    An overlay undergoes a series of transformations before being able to run
    workloads.  Those transformations are orchestrated by the overlay manager.
    To support that orchestration, an overlay will be lockable, and it will have
    a state attribute.  The valid states are listed below.

    Internally, a overlay is represented by a set of :class:`troy.Pilot`
    instances.  As the overlay undergoes transformations, it is enriched by
    additional information, although those are kept solely within the
    :class:`Pilot` instances -- see there for more details.

    The overlay transformations are:

    * *Scheduling:* A overlay is mapped onto resourced.

    * *Dispatching:* A scheduled overlay is provisioned to the respective
      resources.

    Overlay States
    ---------------

    An overlay can be in different states, depending on the transformations
    performed on it.  Specifically, it can be in `DESCRIBED`,
    `TRANSLATED`, `SCHEDULED`, `PROVISIONED`, `COMPLETED` or `FAILED`.

    A overlay enters the overlay manager in `DESCRIBED` state, and all follow-up
    state transitions are kept within the overlay manager.

    Those states are ill defined in case of partial transformations -- if, for
    example, a scheduling step may only schedule some of the pilots, but not
    others.  As a general rule, a overlay will remain in a state until the
    transformation has been performed on all applicable overlay components
    (pilots).

    Even on fully transformed overlay, the actual overlay state may not be
    trivial to determine -- for example, a specific pilot may have failed, and
    my turn out to be impossible to re-run on its target resource, so it needs
    to be rescheduled to a different resource.  Those feedback loops are
    considered out-of-scope for Troy at this point, so that state transitions
    are considered irreversible.  
    """

    def __init__(self, session, descr=None):
        """
        Create a new overlay instance, based on the given overlay description

        Each new overlay is assigned a new ID.

        Later (service oriented) Troy implementations may allow for an
        additional id parameter, to reconnect to the thus identified overlay
        instance.
        """
        if session:
            self.session = session
        else:
            self.session = troy.Session()
        if not descr:
            descr = troy.OverlayDescription()
        if isinstance(descr, dict):
            descr = troy.OverlayDescription(descr)
        self.id = ru.generate_id('ol.')
        tu.Timed.__init__(self, 'troy.Overlay', self.id)
        self.session.timed_component(self, 'troy.Overlay', self.id)
        tu.Properties.__init__(self, descr)
        self.register_property('id')
        self.register_property('state')
        self.register_property('description')
        self.register_property('pilots')
        self.register_property('manager')
        self.state = DESCRIBED
        self.description = descr
        self.pilots = dict()
        troy.OverlayManager.register_overlay(self)

    def __del__(self):
        """
        Destructor -- cancels the overlay
        """
        self.cancel()

    def cancel(self):
        """
        cancel all pilots
        """
        for pid in self.pilots.keys():
            pilot = self.pilots[pid]
            pilot.cancel()

    def _add_pilot(self, p_descr):
        """
        Add a pilot to the overlay
        """
        if self.state != DESCRIBED:
            raise RuntimeError('overlay is not in DESCRIBED state -- cannot add pilots')
        if not isinstance(p_descr, troy.PilotDescription):
            raise TypeError('expected PilotDescription, got %s' % type(p_descr))
        p = troy.Pilot(self.session, p_descr, _overlay=self)
        self.pilots[p.id] = p
        return p.id