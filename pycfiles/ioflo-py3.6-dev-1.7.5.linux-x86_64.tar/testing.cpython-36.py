# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/test/testing.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 9983 bytes
"""
testing.py unit test module support classes and functions
"""
import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest
import os, importlib
from ..aid.consoling import getConsole
console = getConsole()
from ..aid import odict, oset
from ..base import globaling
from ..base import storing
from ..base import housing
from ..base import logging
from ..base import framing
from ..base import acting
from ..base import doing
from .. import __version__
if sys.platform == 'win32':
    TEMPDIR = 'c:/temp'
    if not os.path.exists(TEMPDIR):
        os.mkdir(TEMPDIR)
else:
    TEMPDIR = '/tmp'
BEHAVIORS = []

def setUpModule():
    console.reinit(verbosity=(console.Wordage.concise))
    if BEHAVIORS:
        for behavior in BEHAVIORS:
            mod = importlib.import_module(behavior)


def tearDownModule():
    pass


def initPathToData(store, path, data):
    """
    Returns share at path in store after creating and assigning data items
    to fields in share
    """
    share = store.create(path)
    verifyShareFields(share, data.keys())
    share.update(data)
    return share


def verifyShareFields(share, fields):
    """
    Verifies that updating fields in share won't violate the
       condition that when a share has field == 'value'
       it will be the only field

       share is  Share
       fields is list of field names

       raises ValueError exception if condition would be violated
    """
    if len(fields) > 1:
        if 'value' in fields:
            raise ValueError("Invalid field named 'value' in {0}".format(fields))
    if share:
        for field in fields:
            if field not in share and ('value' in share or field == 'value'):
                raise ValueError("Candidate field '{0}' when fields = '{1}' exist".format(field, share.keys()))


class IofloTestCase(unittest.TestCase):
    __doc__ = '\n    Base TestCase for Ioflo TestCases with cleared house class registried\n    '

    def setUp(self, behaviors=None):
        if behaviors:
            if self.behaviors:
                for behavior in self.behaviors:
                    mod = importlib.import_module(behavior)

        housing.House.Clear()
        housing.ClearRegistries()

    def tearDown(self):
        housing.House.Clear()
        housing.ClearRegistries()


class StoreIofloTestCase(IofloTestCase):
    __doc__ = '\n    TestCase with only .store\n    '

    def setUp(self):
        super(StoreIofloTestCase, self).setUp()
        self.store = storing.Store(stamp=0.0)

    def tearDown(self):
        super(StoreIofloTestCase, self).tearDown()


class HouseIofloTestCase(IofloTestCase):
    __doc__ = '\n    TestCase with .store from .house, .metas, and .preloads\n    Sets up .house with .metas and .preloads and resolves\n    '

    def setUp(self):
        super(HouseIofloTestCase, self).setUp()
        self.house = housing.House(name='HouseTest')
        self.store = self.house.store
        self.house.assignRegistries()
        self.metas = [
         (
          'name', 'meta.name', odict(value='Tester')),
         (
          'period', 'meta.period', odict(value=0.125)),
         (
          'real', 'meta.real', odict(value=False)),
         (
          'mode', 'meta.mode', odict(value=None)),
         (
          'plan', 'meta.plan', odict(value='Test.flo')),
         (
          'filepath', 'meta.filepath', odict(value='')),
         (
          'behaviors', 'meta.behaviors', odict(value=BEHAVIORS)),
         (
          'credentials', 'meta.credentials',
          odict([('username', 'Testee'), ('password', 'Password')])),
         (
          'failure', 'meta.failure', odict(value='')),
         (
          'framers', 'meta.framers', odict()),
         (
          'taskables', 'meta.taskables', odict(value=(oset())))]
        self.setupMetas()
        self.preloads = [
         (
          'ioflo.version', odict(value=__version__)),
         (
          'ioflo.platform',
          odict([('os', sys.platform),
           (
            'python', ('{0}.{1}.{2}'.format)(*sys.version_info))]))]
        self.setupPreloads()

    def tearDown(self):
        super(HouseIofloTestCase, self).tearDown()

    def setupMetas(self, extras=None):
        """
        Create and add meta shares to house and store
        add the extras to the default metas

        extras is a list of triples of the form (key, path, odict()
        """
        if extras:
            self.metas.extend(extras)
        for name, path, data in self.metas:
            self.house.metas[name] = initPathToData(self.store, path, data)

        self.house.metas['house'] = initPathToData(self.store, '.meta.house', odict(value=(self.house.name)))

    def setupPreloads(self, extras=None):
        """
        Create and add preload shares to store
        add the extras to the default preloads
        extras  is a list of duples of the form (path, odict())
        """
        if extras:
            self.preloads.extend(extras)
        for path, data in self.preloads:
            initPathToData(self.store, path, data)

    def resolve(self):
        """
        Resolve the house
        """
        self.house.resolve()


class LoggerIofloTestCase(HouseIofloTestCase):
    __doc__ = '\n    TestCase with .logger in .house and .store from .house\n    '

    def setUp(self):
        super(LoggerIofloTestCase, self).setUp()
        prefix = '/tmp/log/ioflo'
        self.logger = logging.Logger(name='LoggerTest', store=(self.store),
          schedule=(globaling.ACTIVE),
          prefix=prefix)
        self.house.taskers.append(self.logger)
        self.house.mids.append(self.logger)
        self.house.orderTaskables()

    def tearDown(self):
        super(LoggerIofloTestCase, self).tearDown()


class FramerIofloTestCase(HouseIofloTestCase):
    __doc__ = '\n    TestCase with .framer in .house and .store from .house\n    '

    def setUp(self):
        super(FramerIofloTestCase, self).setUp()
        self.framer = framing.Framer(name='FramerTest', store=(self.store))
        self.house.taskers.append(self.framer)
        self.house.framers.append(self.framer)
        self.house.mids.append(self.framer)
        self.house.orderTaskables()
        self.framer.assignFrameRegistry()

    def tearDown(self):
        super(FramerIofloTestCase, self).tearDown()


class FrameIofloTestCase(FramerIofloTestCase):
    __doc__ = '\n    TestCase with .frame in .framer in .house and .store from .house\n    '

    def setUp(self):
        super(FrameIofloTestCase, self).setUp()
        self.frame = framing.Frame(name='FrameTest', store=(self.store),
          framer=(self.framer))
        self.framer.first = self.frame

    def tearDown(self):
        super(FrameIofloTestCase, self).tearDown()

    def addDoer(self, kind, context=globaling.RECUR, inits=None, ioinits=None, parms=None, prerefs=None):
        """
        Create act to run doer class name given by kind and
        add to context.
        """
        act = acting.Act(actor=kind, registrar=(doing.Doer),
          inits=inits,
          ioinits=ioinits,
          parms=parms,
          prerefs=prerefs)
        if context == globaling.NATIVE:
            context = globaling.RECUR
        self.frame.addByContext(act, context)
        return act

    def addBenterDoer(self, kind, **kwa):
        """
        Create Act with actor of kind and add doer at BENTER context
        """
        return (self.addDoer)(kind, context=globaling.BENTER, **kwa)

    def addEnterDoer(self, kind, **kwa):
        """
        Create Act with actor of kind and add doer at ENTER context
        """
        return (self.addDoer)(kind, context=globaling.ENTER, **kwa)

    def addRenterDoer(self, kind, **kwa):
        """
        Create Act with actor of kind and add doer at RENTER context
        """
        return (self.addDoer)(kind, context=globaling.RENTER, **kwa)

    def addRecurDoer(self, kind, **kwa):
        """
        Create Act with actor of kind and add doer at RECUR context
        """
        return (self.addDoer)(kind, context=globaling.RECUR, **kwa)

    def addPrecurDoer(self, kind, **kwa):
        """
        Create Act with actor of kind and add doer at PRECUR context
        """
        return (self.addDoer)(kind, context=globaling.PRECUR, **kwa)

    def addExitDoer(self, kind, **kwa):
        """
        Create Act with actor of kind and add doer at EXIT context
        """
        return (self.addDoer)(kind, context=globaling.EXIT, **kwa)

    def addRexitDoer(self, kind, **kwa):
        """
        Create Act with actor of kind and add doer at REXIT context
        """
        return (self.addDoer)(kind, context=globaling.REXIT, **kwa)

    addDeed = addDoer
    addBenterDeed = addBenterDoer
    addEnterDeed = addEnterDoer
    addRenterDeed = addRenterDoer
    addRecurDeed = addRecurDoer
    addPrecurDeed = addPrecurDoer
    addExitDeed = addExitDoer
    addRexitDeed = addRexitDoer