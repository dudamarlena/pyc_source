# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/base/skedding.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 16135 bytes
"""skedding.py weightless thread scheduling

"""
import sys
if sys.version > '3':
    xrange = range
import os, time
from collections import deque
from ..aid.consoling import getConsole
console = getConsole()
from ..aid.sixing import *
from ..aid import odict, oset
from .globaling import *
from ..aid import timing
from . import excepting
from . import registering
from . import storing
from . import tasking
from . import building
from ..__metadata__ import __version__
from ..aid.consoling import getConsole
console = getConsole()

class Skedder(object):
    __doc__ = "Schedules weightless tasker objects based on generators.\n\n       run method runs the skedder main loop until interrupted or all taskers\n       completed\n\n       taskers is a dictionary of taskers indexed by tasker name\n\n       The skedder maintains lists of taskers in various execution states\n          Each list determines what the skedder does with the tasker.\n          The skedder has methods that move taskers between the lists and\n              also notifies taskers of their control\n\n          Skedder runs tasker and sends it a control\n          Tasker runs using control and yields its status\n\n          Each tasker as a .desire attribute that indicates what the next\n          desired control should be.\n\n          Each tasker as a .period attribute that indicates how ofter the tasker\n          should be run\n\n          There are three deques the skedder maintains. Each entry in each deque\n          is a tuple (tasker, retime, period)\n             tasker is reference to tasker object\n             retime is time that the tasker should next be run\n                a retime of zero means runs asap or always\n             period is the time period between runs\n\n          ready = deque of tuples where taskers are ready to be run\n             If need different priorities then need to add a\n                ready list for each priority\n\n          stopped = deque of tuples where taskers stopped awaiting start\n\n          aborted = deque of tuples where taskers aborted can't be restarted\n\n          addStoppedTask(tasker) adds tasker to stopped list\n          addReadyTask(tasker) adds tasker to ready list\n\n       Everytime a tasker runs it yields a status that the skedder uses to determine\n       what to do with the tasker\n\n       instance attributes:\n       .name = skedder name string\n       .period = time seconds between iterations of skedder\n       .stamp = current iteration time of skedder\n       .real = real time IF True ELSE simulated time\n       .timer = timer to time loops in real time\n       .elapsed = timer to time elapsed in mission\n\n       .houses = list of houses to be scheduled\n\n       .ready = deque of tasker  tuples ready to run\n       .aborted = deque of tasker tuples aborted\n    "

    def __init__(self, name='skedder', period=0.125, stamp=0.0, real=False, retro=True, filepath='', behaviors=None, username='', password='', mode=None, houses=None, metas=None, preloads=None):
        """
        Initialize Skedder instance.
        parameters:
            name = name string
            period = iteration period
            stamp = initial time stamp value
            real = time mode real time True or simulated time False
            retro = shift timers if retrograded system clock detected
            filepath = filepath to build file
            behaviors = list of pathnames to packages with external behavior modules
            username = username
            password = password
            mode = parsing mode
            houses = list of houses
            metas = list of triples of (name, path, data) where
                name = name string of house attribute, path = path string, data = odict
            preloads = list of duples of (path, data) to preload Store where
               path = path string, data = odict
        """
        self.name = name
        self.period = float(abs(period))
        self.stamp = float(abs(stamp))
        self.real = True if real else False
        self.timer = timing.MonoTimer(duration=(self.period), retro=retro)
        self.elapsed = timing.MonoTimer(retro=retro)
        self.filepath = os.path.abspath(filepath)
        self.plan = os.path.split(self.filepath)[1]
        self.behaviors = behaviors or []
        self.username = username
        self.password = password
        self.mode = mode or []
        self.houses = houses or []
        self.metas = [
         (
          'name', 'meta.name', odict(value=(self.name))),
         (
          'period', 'meta.period', odict(value=(self.period))),
         (
          'real', 'meta.real', odict(value=(self.real))),
         (
          'mode', 'meta.mode', odict(value=(self.mode))),
         (
          'plan', 'meta.plan', odict(value=(self.plan))),
         (
          'filepath', 'meta.filepath', odict(value=(self.filepath))),
         (
          'behaviors', 'meta.behaviors', odict(value=(self.behaviors))),
         (
          'credentials', 'meta.credentials',
          odict([('username', self.username), ('password', self.password)])),
         (
          'failure', 'meta.failure', odict(value='')),
         (
          'framers', 'meta.framers', odict()),
         (
          'taskables', 'meta.taskables', odict(value=(oset())))]
        if metas:
            self.metas.extend(metas)
        self.preloads = [
         (
          'ioflo.version', odict(value=__version__)),
         (
          'ioflo.platform',
          odict([('os', sys.platform),
           (
            'python', ('{0}.{1}.{2}'.format)(*sys.version_info))]))]
        if preloads:
            self.preloads.extend(preloads)
        self.ready = deque()
        self.aborted = deque()
        self.built = False

    def addReadyTask(self, tasker):
        """
        Prepare tasker to be started and add to ready list
        """
        if tasker.schedule == ACTIVE:
            tasker.desire = START
        else:
            tasker.desire = STOP
        tasker.status = STOPPED
        retime = tasker.store.stamp
        period = tasker.period
        trp = (tasker, retime, period)
        self.ready.append(trp)
        console.profuse('     Add ready: {0} retime: {1} period: {2} desire {3}\n'.format(tasker.name, retime, period, ControlNames[tasker.desire]))

    def build(self, filepath='', mode=None, metas=None, preloads=None):
        """ Build houses from file given by filepath """
        console.terse("Building Houses for Skedder '{0}' ...\n".format(self.name))
        self.built = False
        if filepath:
            self.filepath = filepath
        if mode:
            self.mode.extend(mode)
        if metas:
            self.metas.extend(metas)
        if preloads:
            self.preloads.extend(preloads)
        b = building.Builder(fileName=(self.filepath), mode=(self.mode),
          metas=(self.metas),
          preloads=(self.preloads),
          behaviors=(self.behaviors))
        if not b.build():
            return False
        else:
            self.built = True
            self.houses = b.houses
            for house in self.houses:
                console.profuse("Meta Data for House '{0}':\n{1}\n".format(house.name, house.metas))

            return True

    def run(self, growable=False):
        """runs all generator taskers in running list by calling next() method.

           Keyboard interrupt (cntl-c) to end forever loop
           Since finally clause closes taskers they must be restarted before
           run can be executed again

           if growable is True then allow adding new taskers at runtime
              via  house metas['taskables']

        """
        console.terse("Starting Skedder '{0}' ...\n".format(self.name))
        stamp = self.stamp
        for house in self.houses:
            house.store.changeStamp(stamp)
            'Initialized store {0}:  stamp = {1} with {2}\n'.format(house.store.name, house.store.stamp, stamp)
            for tasker in house.taskables:
                self.addReadyTask(tasker)

        console.profuse('Ready Taskers: {0}\n'.format(', '.join([tasker.name for tasker, r, p in self.ready])))
        console.profuse('Aborted Taskers: {0}\n'.format(', '.join([tasker.name for tasker, r, p in self.aborted])))
        self.timer.restart()
        self.elapsed.restart()
        ready = self.ready
        aborted = self.aborted
        try:
            while True:
                try:
                    console.profuse("\nRunning Skedder '{0}' at stamp = {1} real elapsed = {2:0.4f}\n".format(self.name, self.stamp, self.elapsed.elapsed))
                    more = False
                    for i in xrange(len(ready)):
                        tasker, retime, period = ready.popleft()
                        if retime > stamp:
                            ready.append((tasker, retime, period))
                            status = tasker.status
                        else:
                            try:
                                status = tasker.runner.send(tasker.desire)
                                if status == ABORTED:
                                    aborted.append((tasker, stamp, period))
                                    console.profuse('     Tasker Self Aborted: {0}\n'.format(tasker.name))
                                else:
                                    ready.append((tasker,
                                     retime + tasker.period,
                                     tasker.period))
                            except StopIteration:
                                aborted.append((tasker, stamp, period))
                                console.profuse('     Tasker Aborted due to StopIteration: {0}\n'.format(tasker.name))

                        if status == RUNNING or status == STARTED:
                            more = True

                    if growable:
                        pass
                    if not ready:
                        console.terse('No ready taskers. Shutting down skedder ...\n')
                        break
                    if not more:
                        console.terse('No running or started taskers. Shutting down skedder ...\n')
                        break
                    if self.real:
                        console.profuse('     Time remaining skedder = {0:0.4f}\n'.format(self.timer.remaining))
                        while not self.timer.expired:
                            time.sleep(self.timer.remaining)

                        self.timer.repeat()
                    self.stamp += self.period
                    stamp = self.stamp
                    for house in self.houses:
                        house.store.changeStamp(stamp)

                except KeyboardInterrupt:
                    console.terse('KeyboardInterrupt forcing shutdown of Skedder ...\n')
                    break
                except SystemExit:
                    console.terse('SystemExit forcing shutdown of Skedder ...\n')
                    raise
                except Exception:
                    console.terse('Surprise exception forcing shutdown of Skedder ...\n')
                    raise

            console.terse('Total elapsed real time = {0:0.4f}\n'.format(self.elapsed.elapsed))
        finally:
            console.terse('Aborting all ready Taskers ...\n')
            for i in xrange(len(ready)):
                tasker, retime, period = ready.popleft()
                try:
                    status = tasker.runner.send(ABORT)
                    console.terse("Tasker '{0}' aborted\n".format(tasker.name))
                except StopIteration:
                    console.terse("Tasker '{0}' generator already exited\n".format(tasker.name))

        if console._verbosity >= console.Wordage.concise:
            for house in self.houses:
                console.concise('\nData Store for {0}\n'.format(house.name))
                house.store.expose(valued=(console._verbosity >= console.Wordage.terse))


def Test(real=False, verbose=False):
    """Module Common self test

    """
    import housing
    reload(housing)
    housing.ClearRegistries()
    print(housing.Registries)
    print('')
    print(housing.Registries['tasker'].Names)
    print(housing.Registries['tasker'].Counter)
    print('')
    house = housing.House()
    t1 = tasking.Tasker(name='t1', store=(house.store))
    t2 = tasking.Tasker(name='t2', store=(house.store))
    t3 = tasking.Tasker(name='t3', store=(house.store), period=0.125)
    t4 = tasking.Tasker(name='t4', store=(house.store), period=0.125)
    t5 = tasking.Tasker(name='t5', store=(house.store), period=0.5)
    t6 = tasking.Tasker(name='t6', store=(house.store), period=1.0)
    house.actives = [
     t1, t6, t2, t5, t3, t4]
    skedder = Skedder(name='TestTasker', period=0.125, real=real, houses=[house])
    skedder.run()


def TestProfile(real=False, verbose=False):
    """Module Common self test

    """
    import cProfile, pstats, housing
    reload(housing)
    housing.ClearRegistries()
    print(housing.Registries)
    print('')
    print(housing.Registries['tasker'].Names)
    print(housing.Registries['tasker'].Counter)
    print('')
    house = housing.House()
    t1 = Tasker(name='t1', store=(house.store))
    t2 = Tasker(name='t2', store=(house.store))
    t3 = Tasker(name='t3', store=(house.store), period=0.125)
    t4 = Tasker(name='t4', store=(house.store), period=0.125)
    t5 = Tasker(name='t5', store=(house.store), period=0.5)
    t6 = Tasker(name='t6', store=(house.store), period=1.0)
    house.actives = [
     t1, t6, t2, t5, t3, t4]
    skedder = Skedder(name='TestSkedder', period=0.125, real=real, houses=[house])
    cProfile.runctx('skedder.run()', globals(), locals(), './test/profiles/skeddertest')
    p = pstats.Stats('./test/profiles/skeddertest')
    p.sort_stats('time').print_stats()
    p.print_callers()
    p.print_callees()


if __name__ == '__main__':
    Test()