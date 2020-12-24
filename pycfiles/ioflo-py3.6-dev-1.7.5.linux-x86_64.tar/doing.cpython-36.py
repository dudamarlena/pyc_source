# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/base/doing.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 6124 bytes
"""
doing.py doer module for do verb behaviors
"""
import time, struct
from collections import deque, Mapping
from functools import wraps
import inspect, copy
from ..aid.sixing import *
from .globaling import INDENT_ADD
from ..aid.odicting import odict
from ..aid import aiding
from . import excepting
from . import registering
from . import storing
from . import acting
from ..aid.consoling import getConsole
console = getConsole()
from ..aid.classing import nonStringIterable
from ..aid.aiding import just, nameToPath

def doify(name, base=None, registry=None, parametric=None, inits=None, ioinits=None, parms=None):
    """ Parametrized decorator function that converts the decorated function
        into an Actor sub class with .action method and with class name name
        and registers the new subclass in the registry under name.
        If base is provided then register as subclass of base.
        Default base is Doer

        The parameters registry, parametric, inits, ioinits, and parms if provided,
        are used to create the class attributes for the new subclass
    """
    base = base or Doer
    if not issubclass(base, Doer):
        msg = "Base class '{0}' not subclass of Doer".format(base)
        raise excepting.RegisterError(msg)
    attrs = odict()
    if registry:
        attrs['Registry'] = odict()
    if parametric is not None:
        attrs['_Parametric'] = True if parametric else False
    if inits:
        attrs['Inits'] = odict(inits)
    if ioinits:
        attrs['Ioinits'] = odict(ioinits)
    if parms:
        attrs['Parms'] = odict(parms)
    cls = type(name, (base,), attrs)

    def implicit(func):

        @wraps(func)
        def inner(*pa, **kwa):
            return func(*pa, **kwa)

        cls.action = inner
        return inner

    return implicit


class Doer(acting.Actor):
    __doc__ = "\n    Provides object of 'do' command verb\n    The Doer's action method is the 'deed'\n    Base class has Doer specific Registry of Classes\n    Doer instance native actions context is recur\n    Doer defaults to converting iois into attributes\n    "
    Registry = odict()
    _Parametric = False


class DoerParam(Doer):
    __doc__ = '\n    Iois are converted to parms not attributes\n    '
    _Parametric = True


class DoerSince(Doer):
    __doc__ = '\n    Generic Super Class acts if input updated Since last time ran\n    knows time of current iteration and last time processed input\n\n    Should be subclassed\n\n    Attributes\n        .stamp = current time of doer evaluation in seconds\n\n    '

    def __init__(self, **kw):
        (super(DoerSince, self).__init__)(**kw)
        self.stamp = None

    def action(self, **kw):
        """Should call this on superclass  as first step of subclass action method  """
        console.profuse('Actioning DoerSince  {0}\n'.format(self.name))
        self.stamp = self.store.stamp

    def _expose(self):
        """     """
        print('Doer %s stamp = %s' % (self.name, self.stamp))


class DoerLapse(Doer):
    __doc__ = '\n    Generic base class for Doers that need to\n    keep track of lapsed time between iterations.\n    Should be subclassed\n\n    Attributes\n        .stamp =  current time stamp of doer evaluation in seconds\n        .lapse = elapsed time betweeen current and previous evaluation\n\n    has restart method when resuming after noncontiguous time interruption\n    builder creates implicit entry action of restarter for Doer\n    '

    def __init__(self, **kwa):
        (super(DoerLapse, self).__init__)(**kwa)
        self.stamp = None
        self.lapse = 0.0

    def restart(self):
        """
        Restart Doer
        Override in subclass
        This is called by restarter action in enter context
        """
        console.profuse('Restarting DoerLapse  {0}\n'.format(self.name))

    def updateLapse(self):
        """
        Calculates a new time lapse based on stamp
        or if stamp is None then use store stamp
        updates .stamp
        """
        stampLast, self.stamp = self.stamp, self.store.stamp
        try:
            self.lapse = max(0.0, self.stamp - stampLast)
        except TypeError:
            self.stamp = self.store.stamp
            self.lapse = 0.0

    def action(self, **kwa):
        """    """
        console.profuse('Actioning DoerLapse  {0}\n'.format(self.name))
        self.updateLapse()

    def _expose(self):
        """     """
        print('Doer %s stamp = %s lapse = %s' % (self.name, self.stamp, self.lapse))

    def _resolve(self, **kwa):
        parms = (super(DoerLapse, self)._resolve)(**kwa)
        restartActParms = {}
        restartAct = acting.SideAct(actor=self, parms=restartActParms,
          action='restart',
          human=(self._act.human),
          count=(self._act.count))
        found = False
        for i, enact in enumerate(self._act.frame.enacts):
            if enact is self._act:
                found = True
                self._act.frame.insertEnact(restartAct, i)
                break

        if not found:
            self._act.frame.addEnact(restartAct)
        console.profuse('{0}Added enact {1} SideAct for {2} with {3} in {4}\n'.format(INDENT_ADD, 'restart', self.name, restartAct.parms, self._act.frame.name))
        restartAct.resolve()
        return parms