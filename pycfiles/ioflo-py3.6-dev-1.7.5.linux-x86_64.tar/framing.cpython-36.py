# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/base/framing.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 64735 bytes
"""framing.py hierarchical action framework module

"""
import sys
if sys.version > '3':
    xrange = range
import copy
from collections import deque, Mapping
import uuid
from ..aid.sixing import *
from ..aid.odicting import odict
from .globaling import *
from . import excepting
from . import registering
from . import storing
from . import tasking
from ..aid.consoling import getConsole
console = getConsole()

class Framer(tasking.Tasker):
    __doc__ = ' Framer Task Patron Registry Class for running hierarchical action framework\n\n        inherited instance attributes\n            .name = unique name for machine\n            .store = data store\n\n            .period = desired time in seconds between runs must be non negative, zero means asap\n            .stamp = time of last outline change beginning time to compute elapsed time\n            .status = operational status of tasker\n            .desire = desired control asked by this or other taskers\n            .done = tasker completion state True or False\n            .schedule = scheduling context of this Task for Skedder\n            .runner = generator to run tasker\n\n       instance attributes\n            .main = main frame when this framer is an auxiliary\n            .original = clone state, False if clone True if not clone\n            .insular = clone that is visible only to main framer\n            .razeable = clone that can be explicitly razed at run time\n            .done = auxiliary completion state True or False when an auxiliary\n            .elapsed = elapsed time from outline change\n            .elapsedShr = share where .elapsed is stored for logging and need checks\n\n            .recurred = number of completed recurrences of the current outline\n                     recurred is zeroed upon entry\n                     during first iteration recurred is 0\n                     during second iteration (before trans evaluated) recurred is 1\n                     so a trans check on recurred == 2 means its already iterated twice\n            .recurredShr = share where recurred is stored for logging and need checks\n\n            .first = first frame (default frame to start at)\n            .active = active frame\n            .actives = active outline list of frames\n            .activeShr = share where .active name is stored for logging\n\n            .human = human readable version of active outline\n            .humanShr = share where .human is stored for logging\n\n            .frameNames = frame name registry , name space of frame names\n            .frameCounter = frame name registry counter\n\n            .moots = odict of moot framers to be cloned keyed by clone tag\n            .inode = prefix string for inode ioinit of do verb objects in framer\n            .tag = main framer local unique clone tag when cloned or aux name if not\n            .insularCount = number of insular clones used to create unique clone tag\n            .auxes = odict of cloned auxes keyed by tag name of clone\n    '

    def __init__(self, tag='', **kw):
        """
        Initialize instance.

        Parameters:
            tag = unique to framer clone tag name if clone otherwise same as .name if empty

        """
        (super(Framer, self).__init__)(**kw)
        self.main = None
        self.original = True
        self.insular = False
        self.razeable = False
        self.done = True
        self.stamp = 0.0
        self.elapsed = 0.0
        path = 'framer.' + self.name + '.state.elapsed'
        self.elapsedShr = self.store.create(path)
        self.elapsedShr.update(value=(self.elapsed))
        self.recurred = 0
        path = 'framer.' + self.name + '.state.recurred'
        self.recurredShr = self.store.create(path)
        self.recurredShr.update(value=(self.recurred))
        self.first = None
        self.active = None
        self.actives = []
        path = 'framer.' + self.name + '.state.active'
        self.activeShr = self.store.create(path)
        self.activeShr.update(value=(self.active.name if self.active else ''))
        self.human = ''
        path = 'framer.' + self.name + '.state.human'
        self.humanShr = self.store.create(path)
        self.humanShr.update(value=(self.human))
        self.frameNames = odict()
        self.frameCounter = 0
        self.moots = odict()
        self.inode = ''
        self.tag = tag if tag else self.name
        self.auxes = odict()

    @property
    def mains(self):
        """
        Property that returns tuple of framer hierarchy of current framer
        from current framer to an including first non clone framer
        (framername,clonetag,clonetag,clonetag)
        """
        framer = self
        mains = [framer]
        while not framer.original:
            framer = framer.main.framer
            mains.append(framer)

        return tuple(reversed(mains))

    @property
    def surname(self):
        """
        Property that returns underscore separated string representing namespaced
        clone framer hierarchy
        For non cloned framers the .surname should be the same as .name
        Uses .mains property so assumes that .main is resolved if any
        """
        return '_'.join((framer.name if framer.original else framer.tag) for framer in self.mains)

    def clone(self, name, tag='', period=0.0, schedule=AUX):
        """
        Return clone of self named name with tag

        """
        self.store.house.assignRegistries()
        if name:
            if not REO_IdentPub.match(name):
                msg = "CloneError: Invalid framer name '{0}'.".format(name)
                raise excepting.CloneError(msg)
        if name in Framer.Names:
            msg = "CloneError: Framer '{0}' already exists.".format(name)
            raise excepting.CloneError(msg)
        clone = Framer(name=name, store=(self.store),
          period=period,
          schedule=schedule,
          tag=tag)
        console.terse("         Cloning contents of Framer original '{0}' to clone '{1}'\n".format(self.name, clone.name))
        clone.schedule = schedule
        clone.first = self.first
        clone.moots = copy.deepcopy(self.moots)
        clone.inode = self.inode
        clone.assignFrameRegistry()
        for frame in self.frameNames.values():
            frame.clone(framer=clone)

        return clone

    def prune(self):
        """
        Recursively Prune (destroy) all insular auxiliary clones in all frames
        Force exit if not done
        Called by Razer Actor when razing insular auxes from frame
        """
        if not self.done:
            console.profuse("Force exiting '{0}'\n".format(self.name))
            self.exitAll()
        for frame in self.frameNames.values():
            prunables = [aux for aux in frame.auxes if aux.insular]
            for aux in prunables:
                aux.prune()
                frame.auxes.remove(aux)
                if aux.tag in self.auxes:
                    del self.auxes[aux.tag]

        if self.name in Framer.Names:
            if Framer.Names[self.name] == self:
                del Framer.Names[self.name]

    def presolve(self):
        """
        Convert namestrings or data of moots into clones
        """
        console.terse('     Presolving Framer {0}\n'.format(self.name))
        self.resolveMoots()
        self.assignFrameRegistry()
        if self.first:
            self.first = resolveFrame((self.first), who=(self.name), desc='first')
        else:
            raise excepting.ResolveError('No first frame link', self.name, self.first)
        console.terse('       Presolving frames for framer {0}\n'.format(self.name))
        for frame in Frame.Names.values():
            frame.presolve()

        self.presolved = True

    def resolve(self):
        """
        Convert all the name strings for links to references to instance
        by that name
        """
        if not self.presolved:
            raise excepting.ResolveError('Not presolved', self.name, self.main)
        console.terse('     Resolving Framer {0}\n'.format(self.name))
        self.assignFrameRegistry()
        console.terse('       Resolving frames for framer {0}\n'.format(self.name))
        for frame in Frame.Names.values():
            frame.resolve()

        self.traceOutlines()
        self.resolved = True

    def resolveMoots(self):
        """
        Resolves .moots by cloning as appropriate.
        .moots is odict keyed by clone tag with value that are dicts of form
        {
            original: framername,
            clone: string,
            schedule: constant,
            human: string,
            count: number,
            inode: pathstring,
            insular: boolean
        }

        creates clone and adds to taskables if named clone
        resolution looks up name string in appropriate registry and replaces
        name string with link to object

        Assumes Framer.names is .house's registry
        """
        console.terse('       Resolving original moots for named clones ...\n')
        for tag, data in self.moots.items():
            original = data['original']
            name = data['clone']
            schedule = data['schedule']
            human = data['human']
            count = data['count']
            inode = data['inode']
            insular = data['insular']
            console.terse("         Cloning original '{0}' as {1} clone '{2}'\n".format(original, 'insular' if insular else 'named', name))
            if name != tag:
                raise excepting.ResolveError('Mismatch clone tag', name=name,
                  value=tag,
                  human=human,
                  count=count)
            if name == 'mine':
                raise excepting.ResolveError("Invalid named clone name of 'mine'", name=original,
                  value=(self.name),
                  human=human,
                  count=count)
            original = resolveFramer(original, who=(self.name),
              desc='original',
              contexts=[
             MOOT],
              human=human,
              count=count)
            if tag in self.auxes:
                raise excepting.ResolveError('Clone tag already in use', name=(self.name),
                  value=tag,
                  human=human,
                  count=count)
            name = '_'.join((self.surname, tag))
            clone = original.clone(name=name, tag=tag, schedule=schedule)
            self.auxes[tag] = clone
            if inode != 'mine':
                clone.inode = inode
            clone.original = False
            clone.insular = insular
            self.store.house.presolvables.append(clone)
            self.store.house.taskers.append(clone)
            self.store.house.framers.append(clone)
            if schedule == AUX:
                self.store.house.auxes.append(clone)

        self.moots.clear()

    def newMootTag(self, base=None, count=0):
        """
        Returns new unique among .moots insular tag by incrementing count
        """
        if not base:
            base = self.tag
        count += 1
        tag = '{0}{1}'.format(base, count)
        while tag in self.moots:
            count += 1
            tag = '{0}{1}'.format(base, count)

        return tag

    def newAuxTag(self, base=None, count=0):
        """
        Returns new unique among .auxes insular tag by using .insularCount
        """
        if not base:
            base = self.tag
        count += 1
        tag = '{0}{1}'.format(base, count)
        while tag in self.auxes:
            count += 1
            tag = '{0}{1}'.format(base, count)

        return tag

    @staticmethod
    def nameUid(prefix='clone', size=8):
        """
        Returns unique name for Framer composed of prefix and random bytes
        prefix is prefix to name
        size is number of random bytes

        Uses uuid.uuid4
        """
        size = int(max(size, 1))
        return '{0}_{1}'.format(prefix, uuid.uuid4().hex[:size])

    def traceOutlines(self):
        """Trace and assign outlines for each frame in framer
        """
        console.terse('       Tracing outlines for framer {0}\n'.format(self.name))
        self.assignFrameRegistry()
        for frame in Frame.Names.values():
            frame.traceOutline()
            frame.traceHead()
            frame.traceHuman()
            frame.traceHeadHuman()

    def assignFrameRegistry(self):
        """Point Frame class name registry dict and counter to .frameNames
           and .frameCounter.

           Subsequent Frame instance creation with then be registered locally
        """
        Frame.Names = self.frameNames
        Frame.Counter = self.frameCounter

    def restartTimer(self):
        """reset the start time and elapsed time of framer for changed outline

        """
        self.stamp = self.store.stamp
        self.elapsed = 0.0
        self.updateElapsed()

    def updateTimer(self):
        """update the elapsed time of framer in  current outline
           use store.stamp for current time reference
        """
        try:
            self.elapsed = self.store.stamp - self.stamp
        except TypeError:
            self.stamp = self.store.stamp
            self.elapsed = 0.0

        self.updateElapsed()

    def updateElapsed(self):
        """update store value of the elapsed time of framer in  current outline

        """
        console.profuse('     Updating {0} from {1:0.4f} to {2:0.4f}\n'.format(self.elapsedShr.name, self.elapsedShr.value, self.elapsed))
        self.elapsedShr.update(value=(self.elapsed))

    def restartCounter(self):
        """restart at 0 the recurred counter and share of framer in current outline

        """
        self.recurred = 0
        self.updateRecurred()

    def updateCounter(self):
        """update the recurred counter and share of framer in current outline

        """
        self.recurred += 1
        self.updateRecurred()

    def updateRecurred(self):
        """update store value of the recurred count of framer in  current outline

        """
        console.profuse('     Updating {0} from {1:d} to {2:d}\n'.format(self.recurredShr.name, self.recurredShr.value, self.recurred))
        self.recurredShr.update(value=(self.recurred))

    def change(self, actives, human=''):
        """set .actives and .human to new outline actives
           and human readable version human
           Used by conditional aux to truncate actives
        """
        self.actives = actives
        self.human = human
        self.humanShr.update(value=(self.human))

    def activate(self, active):
        """make parm active the active starting point for framework.
           used to activate far frame to complete transition
           assumes frame exits handled before this
           generates outline. does not change default = first
        """
        self.active = active
        self.activeShr.update(value=(self.active.name))
        self.reactivate()

    def reactivate(self):
        """set .actives to the .active.outline
           used to restore full outline after conditional aux truncates it
        """
        self.change(self.active.outline, self.active.human)

    def deactivate(self):
        """clear .active .actives
        """
        self.actives = []
        self.human = ''
        self.active = None

    def checkStart(self):
        """checks if framer can be started from first frame
           checking entry needs for first frame's outline
           returns result of checkEnter()

        """
        return self.checkEnter(enters=(self.first.outline))

    def checkEnter(self, enters=[], exits=[]):
        """checks beacts for frames in enters list
           return on first failure do not keep testing
           assumes enters outline in top down order
           exits list is used by frame.checkEnters to test for original auxiliaries
           that would be exited from thier main frame if transition where allowed
        """
        console.profuse('{0}Check enters of {1} Framer {2}\n'.format('    ' if self.schedule == AUX or self.schedule == SLAVE else '', ScheduleNames[self.schedule], self.name))
        if not enters:
            console.profuse('    False, empty enters\n')
            return False
        else:
            for frame in enters:
                if not frame.checkEnter(exits=exits):
                    return False

            console.profuse('    True all {0}\n'.format(self.name))
            return True

    def enterAll(self):
        """sets .done to False
           activates first frame
           calls enterActions for frames in active outline

        """
        console.profuse('{0}Enter All {1} Framer {2}\n'.format('    ' if self.schedule == AUX or self.schedule == SLAVE else '', ScheduleNames[self.schedule], self.name))
        self.done = False
        self.activate(self.first)
        self.enter(self.actives)

    def enter(self, enters=[]):
        """calls entryActions for frames in enters list
           assumes enters outline is in top down order

        """
        if enters:
            self.restartTimer()
            self.restartCounter()
        for frame in enters:
            frame.enter()

    def renter(self, renters=[]):
        """calls entryActions for frames in renters list
           assumes renters outline is in top down order

        """
        for frame in renters:
            frame.renter()

    def recur(self):
        """calls recurActions for frames in active outline
           assumes actives outline is in top down order

        """
        console.profuse('{0}Recur {1} Framer {2}\n'.format('    ' if self.schedule == AUX or self.schedule == SLAVE else '', ScheduleNames[self.schedule], self.name))
        for frame in self.actives:
            frame.recur()

    def segue(self):
        """Uses stored outline comparison to find exit enter outlines
           Update Elapsed timer and Recurred counter
           Perform transitions for auxiliaries in active outline top down
           Start performing transitions for frames in active outline top down until
             find successful transition or complete without finding
        """
        console.profuse('{0}Segue {1} Framer {2}\n'.format('    ' if self.schedule == AUX or self.schedule == SLAVE else '', ScheduleNames[self.schedule], self.name))
        self.updateTimer()
        self.updateCounter()
        for frame in self.actives:
            frame.segueAuxes()

        for frame in self.actives:
            if frame.precur():
                return True

    def exitAll(self, abort=False):
        """sets exits to .actives and reverses so in bottom up order
           calls exitActions for frames in exits list

           sets .done to True
           deactivates so restart required to run again
        """
        console.profuse('{0}Exit All {1} Framer {2}\n'.format('    ' if self.schedule == AUX or self.schedule == SLAVE else '', ScheduleNames[self.schedule], self.name))
        exits = self.actives[:]
        self.exit(exits)
        self.deactivate()
        if not abort:
            self.done = True

    def exit(self, exits=[]):
        """calls exitActions for frames in exits list
           assumes exits outline is in top down order
           so reverses it to bottom up
        """
        exits.reverse()
        for frame in exits:
            frame.exit()

    def rexit(self, rexits=[]):
        """calls exitActions for frames in rexits list
           assumes rexits outline is in top down order
           so reverses it to bottom up
        """
        rexits.reverse()
        for frame in rexits:
            frame.rexit()

    def showHierarchy(self):
        """Prints out Framework Hierachy for this framer
        """
        console.terse('\nFramework Hierarchy for {0}:\n'.format(self.name))
        names = self.frameNames
        tops = [x for x in names.itervalues() if not x.over if x.unders]
        console.terse('Tops: {0}\n'.format(' '.join([x.name for x in tops])))
        bottoms = [x for x in names.itervalues() if x.over if not x.unders]
        console.terse('Bottoms: {0}\n'.format(' '.join([x.name for x in bottoms])))
        loose = [x for x in names.itervalues() if not x.over if not x.unders]
        console.terse('Loose: {0}\n'.format(' '.join([x.name for x in loose])))
        console.terse('Hierarchy: \n')
        upper = tops
        lower = []
        count = 0
        while upper:
            lframes = []
            for u in upper:
                path = u.name
                over = u.over
                while over:
                    path = over.name + '>' + path
                    over = over.over

                lframes.append(path)

            lower = []
            for u in upper:
                for b in u.unders:
                    lower.append(b)

            upper = lower
            count += 1
            console.terse('Level {0}: {1}\n'.format(count, ' '.join(lframes)))

        console.terse('\n')

    def makeRunner(self):
        """generator factory function to create generator to run this framer

           yield self if no trans(ition)
           yields next frame on a trans(ition)
        """
        console.profuse("   Making Framer '{0}' runner\n".format(self.name))
        self.status = STOPPED
        self.desire = STOP
        self.done = True
        try:
            while True:
                control = yield self.status
                status = self.status
                console.profuse("\n   Iterate Framer '{0}' with control = {1} status = {2}\n".format(self.name, ControlNames.get(control, 'Unknown'), StatusNames.get(status, 'Unknown')))
                if control == RUN:
                    if status == RUNNING or status == STARTED:
                        self.segue()
                        self.recur()
                        console.profuse("     Ran Framer '{0}'\n".format(self.name))
                        self.status = RUNNING
                    else:
                        if status == STOPPED or status == READIED:
                            console.profuse("   Need to Start Framer '{0}'\n".format(self.name))
                            self.desire = START
                        else:
                            console.profuse("   Aborting Framer '{0}', bad status = {1} control = {2}\n".format(self.name, StatusNames.get(status, 'Unknown'), ControlNames.get(control, 'Unknown')))
                            self.desire = ABORT
                            self.status = ABORTED
                elif control == READY:
                    if status == STOPPED or status == READIED:
                        console.profuse("   Attempting Ready Framer '{0}'\n".format(self.name))
                        if self.checkStart():
                            console.profuse("   Readied Framer '{0}' ...\n".format(self.name))
                            self.status = READIED
                        else:
                            console.profuse("   Failed Ready Framer '{0}'\n".format(self.name))
                            self.desire = STOP
                            self.status = STOPPED
                    else:
                        if status == RUNNING or status == STARTED:
                            console.profuse("   Framer '{0}', aleady Started\n".format(self.name))
                        else:
                            console.profuse("   Aborting Framer '{0}', bad status = {1} control = {2}\n".format(self.name, StatusNames.get(status, 'Unknown'), ControlNames.get(control, 'Unknown')))
                            self.desire = ABORT
                            self.status = ABORTED
                elif control == START:
                    if status == STOPPED or status == READIED:
                        console.profuse("   Attempting Start Framer '{0}'\n".format(self.name))
                        if self.checkStart():
                            console.terse("   Starting Framer '{0}' ...\n".format(self.name))
                            msg = 'To: {0}<{1} at {2}\n'.format(self.name, self.first.human, round(self.store.stamp, 6))
                            console.terse(msg)
                            self.desire = RUN
                            self.enterAll()
                            self.recur()
                            self.status = STARTED
                        else:
                            console.profuse('   Failed Start Framer {0}\n'.format(self.name))
                            self.desire = STOP
                            self.status = STOPPED
                    else:
                        if status == RUNNING or status == STARTED:
                            console.profuse("   Framer '{0}', aleady Started\n".format(self.name))
                            self.desire = RUN
                        else:
                            console.profuse("   Aborting Framer '{0}', bad status = {1} control = {2}\n".format(self.name, StatusNames.get(status, 'Unknown'), ControlNames.get(control, 'Unknown')))
                            self.desire = ABORT
                            self.status = ABORTED
                elif control == STOP:
                    if status == RUNNING or status == STARTED:
                        msg = "   Stopping Framer '{0}' in {1} at {2:0.3f}\n".format(self.name, self.active.name, self.store.stamp)
                        self.desire = STOP
                        console.terse(msg)
                        self.exitAll(abort=True)
                        console.profuse("   Stopped Framer '{0}'\n".format(self.name))
                        self.status = STOPPED
                    else:
                        if status == STOPPED or status == READIED:
                            console.profuse("   Framer '{0}', aleady Stopped\n".format(self.name))
                        else:
                            console.profuse("   Aborting Framer '{0}', bad status = {1} control = {2}\n".format(self.name, StatusNames.get(status, 'Unknown'), ControlNames.get(control, 'Unknown')))
                            self.desire = ABORT
                            self.status = ABORTED
                else:
                    console.profuse("   Framer '{0}' aborting with control = {1}\n".format(self.name, ControlNames.get(control, 'Unknown')))
                    if status == RUNNING or status == STARTED:
                        msg = '   Aborting %s in %s at %0.3f\n' % (
                         self.name, self.active.name, self.store.stamp)
                        console.terse(msg)
                        self.exitAll()
                    else:
                        if status == STOPPED or status == READIED:
                            msg = '   Aborting %s at %0.3f\n' % (
                             self.name, self.store.stamp)
                            console.terse(msg)
                        else:
                            if status == ABORTED:
                                console.profuse("   Framer '{0}', aleady Aborted\n".format(self.name))
                    self.desire = ABORT
                    self.status = ABORTED

        finally:
            console.profuse("   Exception causing Abort Framer '{0}' ...\n".format(self.name))
            self.desire = ABORT
            self.status = ABORTED

    @staticmethod
    def ExEn(nears, far):
        """Computes the relative differences (uncommon  and common parts) between
           the outline lists nears and fars.
           Assumes outlines are in top down order
           Supports forced transition when far is in nears
              in this case
                 the common part of nears from far down is exited and
                 the common part of fars from far down is entered

           returns tuple (exits, enters, reexens):
              the exits as list of frames to be exited from near (uncommon)
              the enters as list of frame to be entered in far (uncommon)
              the reexens as list of frames for reexit reenter from near (common)
        """
        fars = far.outline
        l = min(len(nears), len(fars))
        for i in xrange(l):
            if nears[i] is far or nears[i] is not fars[i]:
                return (
                 nears[i:], fars[i:], nears[:i])

        return ([], [], nears[:])

    @staticmethod
    def Uncommon(near, far):
        """Computes the relative differences (uncommon part) between
           the outline lists near and far.
           Assumes outlines are in top down order
           returns tuple (exits, enters):
              the exits as list of frames to be exited from near bottom up
              the enters as list of frame to be entered in far top down
        """
        n = near
        f = far
        l = min(len(n), len(f))
        for i in xrange(l):
            if n[i] is not f[i]:
                exits = n[i:]
                enters = f[i:]
                return (exits, enters)

        exits = []
        enters = []
        return (exits, enters)


class Frame(registering.StoriedRegistrar):
    __doc__ = " Frame Class for hierarchical action framework object\n\n        inherited instance attributes\n            .name = unique name for frame\n            .store = data store\n\n        instance attributes\n            .framer = link to framer that executes this frame\n            .inode = inode path to prepend to data store path refs\n            .over = link to frame immediately above this one in hierarchy\n            .under = property link to primary frame immediately below this one in hierarchy\n            .unders = list of all frames immediately below this one\n            .outline = list of frames in outline for this frame top down order\n            .head = list of frames from top down to self\n            .human = string of names of frames in outline top down '>' separated\n            .headHuman = string of names of frames in head top down '>' separated\n            .next = next frame used by builder for transitions to next\n\n            .beacts = before entry action (need) acts or entry checks\n            .preacts = precur action acts (pre transition recurrent actions and transitions)\n            .enacts = enter action acts\n            .renacts = renter action acts\n            .reacts = recur action acts\n            .exacts = exit action acts\n            .rexacts = rexit action acts\n\n            .auxes = auxiliary framers\n\n    "
    Counter = 0
    Names = odict()

    def __init__(self, framer=None, inode='', **kw):
        """Initialize instance.

        """
        if 'preface' not in kw:
            kw['preface'] = 'Frame'
        (super(Frame, self).__init__)(**kw)
        self.framer = framer
        self.inode = inode
        self.over = None
        self.unders = []
        self.outline = []
        self.head = []
        self.human = ''
        self.headHuman = ''
        self.next_ = None
        self.beacts = []
        self.preacts = []
        self.enacts = []
        self.renacts = []
        self.reacts = []
        self.exacts = []
        self.rexacts = []
        self.auxes = []

    def clone(self, framer):
        """ Return clone of self by creating new frame in framer and by
            frame links, acts, and auxes

            Assumes that the Frame Registry is pointing to framer
            which is a clone of this Frame's Framer
            so all new Frames will be in the cloned registry.

        """
        clone = Frame(name=(self.name), store=(self.store),
          framer=(framer.name),
          inode=(self.inode))
        console.terse("           Cloning Frame '{0}' into Framer '{1}'\n".format(clone.name, framer.name))
        for aux in self.auxes:
            clone.addAux(aux)

        if self.over:
            if isinstance(self.over, Frame):
                msg = "CloneError: Attempting to clone resolved over frame  '{0}'.".format(self.over.name)
                raise excepting.CloneError(msg)
            clone.over = self.over
        if self.next_:
            if isinstance(self.next_, Frame):
                msg = "CloneError: Attempting to clone resolved next frame  '{0}'.".format(self.next_.name)
                raise excepting.CloneError(msg)
            clone.next_ = self.next_
        for under in self.unders:
            if isinstance(under, Frame):
                msg = "CloneError: Attempting to clone resolved under frame  '{0}'.".format(under.name)
                raise excepting.CloneError(msg)
            clone.unders.append(under)

        for act in self.beacts:
            clone.addBeact(act.clone())

        for act in self.preacts:
            clone.addPreact(act.clone())

        for act in self.enacts:
            clone.addEnact(act.clone())

        for act in self.renacts:
            clone.addRenact(act.clone())

        for act in self.reacts:
            clone.addReact(act.clone())

        for act in self.exacts:
            clone.addExact(act.clone())

        for act in self.rexacts:
            clone.addRexact(act.clone())

        return clone

    def presolve(self):
        """
        Resolve auxiliary links where links are instance name strings assigned during building
           need to be converted to object references using instance name registry

        """
        console.concise('        Presolving Frame {0}\n'.format(self.name))
        self.resolveFramerLink()
        self.resolveAuxLinks()

    def resolve(self):
        """
        Resolve links where links are instance name strings assigned during building
           need to be converted to object references using instance name registry

        """
        console.concise('        Resolving Frame {0}\n'.format(self.name))
        self.resolveNextLink()
        self.resolveOverLinks()
        self.resolveUnderLinks()
        for act in self.beacts:
            act.resolve()

        for act in self.enacts:
            act.resolve()

        for act in self.reacts:
            act.resolve()

        for act in self.preacts:
            act.resolve()

        for act in self.exacts:
            act.resolve()

        for act in self.rexacts:
            act.resolve()

        for act in self.renacts:
            act.resolve()

    def resolveFramerLink(self):
        """Resolve framer link """
        if self.framer:
            self.framer = framer = resolveFramer((self.framer), who=(self.name),
              desc="frame's")

    def resolveAuxLinks(self):
        """
        Resolve aux links

        If aux.original
           aux.main for each aux is not assigned here but is assigned when
          frame.enter before aux.enterAll() so can reuse aux in other frames.
        Otherwise
           assign aux.main to self
        """
        for i, aux in enumerate(self.auxes):
            cloned = False
            if isinstance(aux, Mapping):
                tag = aux.get('tag')
                if not tag:
                    msg = "Empty aux clone tag link '{0}'".format(aux)
                    raise excepting.ResolveError(msg, name=(self.name), value=aux)
                aux = tag
                cloned = True
            if isinstance(aux, Framer) or cloned:
                self.auxes[i] = aux = resolveAuxOfFramer(aux, (self.framer),
                  who=(self.name),
                  desc='aux',
                  contexts=[
                 AUX],
                  human=(self.human),
                  count=None)
                if aux.original:
                    msg = "Aux clone tag already in use by original aux '{0}' in '{1}'".format(aux.name, self.framer.name)
                    raise excepting.ResolveError(msg, name=(aux.name), value=(self.name))
                if aux.main:
                    msg = "Aux already assigned to main '{0}'".format(aux.main.name)
                    raise excepting.ResolveError(msg, name=(aux.name),
                      value=(self.name))
                aux.main = self
            else:
                self.auxes[i] = aux = resolveFramer(aux, who=(self.name),
                  desc='aux',
                  contexts=[
                 AUX],
                  human=(self.human),
                  count=None)
                if not aux.original:
                    msg = "Unexpected non-original aux name '{0}' in '{1}'".format(aux.name, self.framer.name)
                    raise excepting.ResolveError(msg, name=(aux.name), value=(self.name))
                if aux.name not in self.framer.auxes:
                    self.framer.auxes[aux.name] = aux
                else:
                    if self.framer.auxes[aux.name] is not aux:
                        msg = "Aux name '{0}' already in use in '{1}'".format(aux.name, self.framer.name)
                        raise excepting.ResolveError(msg, name=(aux.name), value=(self.name))

    def resolveNextLink(self):
        """Resolve next link

        """
        if self.next_:
            self.next_ = resolveFrame((self.next_), who=(self.name), desc='next')

    def resolveOverLinks(self):
        """Starting with self.over climb over links resolving the links as needed along the way

        """
        over = self.over
        under = self
        while over:
            if not isinstance(over, Frame):
                name = over
                try:
                    over = Frame.Names[name]
                except KeyError:
                    raise excepting.ResolveError('Bad over link in outline', self.name, name)

                if over == self:
                    raise excepting.ResolveError('Outline overs create loop', self.name, under.name)
                if under.name in over.unders:
                    index = over.unders.index(under.name)
                    over.unders[index] = under
                else:
                    over.unders.append(under)
                under.over = over
            else:
                if over == self:
                    raise excepting.ResolveError('Outline overs create loop', self.name, under.name)
            under = over
            over = over.over

    def resolveUnderLinks(self):
        """ Resolve under links """
        for i, under in enumerate(self.unders):
            self.unders[i] = resolveFrame(under, who=(self.name), desc='under')

        if len(set(self.unders)) != len(self.unders):
            raise excepting.ResolveError('Duplicate under', name=(self.name), value=(self.unders))

    def expose(self):
        """Prints out instance variables.

        """
        if self.framer:
            framername = self.framer.name
        else:
            framername = ''
        print('name = %s, framer = %s, over = %s, under = %s' % (
         self.name, framername, self.over, self.under))

    def getUnder(self):
        """getter for under property

        """
        if self.unders:
            return self.unders[0]

    def setUnder(self, under):
        """setter for under property
           changes primary under frame and fixes links
        """
        if under not in self.unders:
            under.attach(over=self)
        index = self.unders.index(under)
        if index != 0:
            self.unders.remove(under)
            self.unders.insert(0, under)

    under = property(fget=getUnder, fset=setUnder, doc='Primary under frame')

    def detach(self):
        """detach self from .over. Fix under links in .over

        """
        if self.over:
            while self in self.over.unders:
                self.over.unders.remove(self)

            self.over = None

    def attach(self, over):
        """attaches self to over frame if attaching would not create loop

           detach from existing over
           setting self.over to over
           adding self to over.unders and
           if no primary under for over make self overs's primary under

        """
        if self.over == over:
            return
        else:
            if self.checkLoop(over):
                raise excepting.ParameterError('Attaching would create loop', 'frame', frame)
            else:
                self.detach()
                over.unders.append(self)
                self.over = over

    def checkLoop(self, over):
        """Check if attachment to over param would create loop
        """
        frame = over
        while frame:
            if frame is self:
                return True
            frame = frame.over

        return False

    def findBottom(self):
        """Finds the bottom most frame for outline that this frame lives in

        """
        bottom = self
        while bottom.under:
            bottom = bottom.under

        return bottom

    def findTop(self):
        """Finds the top most frame for outline that this frame lives in

        """
        top = self
        while top.over:
            top = top.over

        return top

    def traceOutline(self):
        """traces outline

           called by framer.traceOutlines near end of build
        """
        outline = []
        frame = self
        while frame:
            outline.append(frame)
            frame = frame.over

        outline.reverse()
        frame = self.under
        while frame:
            outline.append(frame)
            frame = frame.under

        self.outline = outline
        return outline

    def traceHead(self):
        """traces head portion of outline.
           top down to this frame inclusive
           Useful for truncated outline for conditional aux

           called by framer.traceOutlines near end of build
        """
        head = []
        frame = self
        while frame:
            head.append(frame)
            frame = frame.over

        head.reverse()
        self.head = head
        return head

    def traceHuman(self):
        """traces human readable version of outline as '> <'separated string
           where this frame has '<>'

           called by framer.traceOutlines near end of build
        """
        names = []
        frame = self
        while frame:
            names.append(frame.name)
            frame = frame.over

        names.reverse()
        human = '<' + '<'.join(names)
        names = []
        frame = self.under
        while frame:
            names.append(frame.name)
            frame = frame.under

        human += '>' + '>'.join(names)
        self.human = human
        return human

    def traceHeadHuman(self):
        """traces human readable version of head as '<'separated string
           where this frame has  '<>'

           called by framer.traceOutlines near end of build
        """
        names = []
        frame = self
        while frame:
            names.append(frame.name)
            frame = frame.over

        names.reverse()
        human = '<' + '<'.join(names) + '>'
        self.headHuman = human
        return human

    def checkEnter(self, exits=[]):
        """Check beacts for self and auxes
           exits is list of exit frames to test if aux main frame would be exited
           if transition allowed
        """
        console.profuse('    Check enter into {0}\n'.format(self.name))
        for need in self.beacts:
            if not need():
                return False

        for aux in self.auxes:
            if aux.main:
                if aux.main is not self:
                    if aux.main not in exits:
                        console.concise("    False. Invalid aux '{0}' in use by another frame '{1}'\n".format(aux.name, aux.main.name))
                        return False
                if not aux.checkStart():
                    return False

        console.profuse('    True all {0}\n'.format(self.name))
        return True

    def enter(self):
        """calls enacts enter  acts for self and auxes
        """
        console.profuse('    Enter {0}\n'.format(self.name))
        for act in self.enacts:
            act()

        for aux in self.auxes:
            msg = 'To: {0}<{1} at {2}\n'.format(aux.name, aux.first.human, round(aux.store.stamp, 6))
            console.terse(msg)
            if aux.original:
                aux.main = self
            aux.enterAll()

    def renter(self):
        """calls  renacts renter acts for self
        """
        console.profuse('    Renter {0}\n'.format(self.name))
        for act in self.renacts:
            act()

    def recur(self):
        """calls reacts recurring acts for self and runs auxes
        """
        console.profuse('    Recur {0}\n'.format(self.name))
        for act in self.reacts:
            act()

        for aux in self.auxes:
            aux.recur()

    def segueAuxes(self):
        """performs transitions for auxes
           called by self.framer.segue()
           segue Auxes is its own context
        """
        console.profuse('    Seque auxes of {0}\n'.format(self.name))
        for aux in self.auxes:
            aux.segue()

    def precur(self):
        """Calls preacts pre-recurring acts for self
           Preacts are used for:
              1) Setting up conditions for transitions and conditional auxes
              2) Interrupting the frame flow such as
                 a) transitions
                 b) conditional auxiliaries
                 or other actor subclasses of Interrupter

              setup is considered part of the transition evaluation process.

              When the act.actor action returns truthy
                 return then preact execution is aborted as per a successful
                 transition or conditional aux

           called by self.framer.segue()
        """
        console.profuse('    Precur {0}\n'.format(self.name))
        for act in self.preacts:
            if act():
                return True

        return False

    def exit(self):
        """calls exacts exit acts for self
        """
        console.profuse('    Exit {0}\n'.format(self.name))
        for aux in self.auxes:
            aux.exitAll()
            if aux.original:
                aux.main = None

        for act in self.exacts:
            act()

    def rexit(self):
        """calls  rexacts rexit acts for self
        """
        console.profuse('    Rexit {0}\n'.format(self.name))
        for act in self.rexacts:
            act()

    def addBeact(self, act):
        """        """
        self.beacts.append(act)
        act.frame = self.name
        act.context = ActionContextNames[BENTER]

    def addEnact(self, act):
        """         """
        self.enacts.append(act)
        act.frame = self.name
        act.context = ActionContextNames[ENTER]

    def insertEnact(self, act, index=0):
        """         """
        self.enacts.insert(index, act)
        act.frame = self.name
        act.context = ActionContextNames[ENTER]

    def addRenact(self, act):
        """         """
        self.renacts.append(act)
        act.frame = self.name
        act.context = ActionContextNames[RENTER]

    def addReact(self, act):
        """         """
        self.reacts.append(act)
        act.frame = self.name
        act.context = ActionContextNames[RECUR]

    def addPreact(self, act):
        """         """
        self.preacts.append(act)
        act.frame = self.name
        act.context = ActionContextNames[PRECUR]

    def addExact(self, act):
        """         """
        self.exacts.append(act)
        act.frame = self.name
        act.context = ActionContextNames[EXIT]

    def addRexact(self, act):
        """         """
        self.rexacts.append(act)
        act.frame = self.name
        act.context = ActionContextNames[REXIT]

    def addAux(self, aux):
        """         """
        self.auxes.append(aux)

    def addByContext(self, act, context):
        """Add act to appropriate list given context
           called by builder
        """
        if context == ENTER:
            self.addEnact(act)
        else:
            if context == RECUR:
                self.addReact(act)
            else:
                if context == PRECUR:
                    self.addPreact(act)
                else:
                    if context == EXIT:
                        self.addExact(act)
                    else:
                        if context == RENTER:
                            self.addRenact(act)
                        else:
                            if context == REXIT:
                                self.addRexact(act)
                            else:
                                if context == BENTER:
                                    self.addBeact(act)
                                else:
                                    return False
        return True


def resolveAuxOfFramer(aux, framer, who='', desc='aux', contexts=None, human='', count=None):
    """ Returns resolved aux framer instance from framer
        aux is either name of aux framer to resolve or pre-resolved instance
        framer is framer instance that contains aux.
        who is optional name of object owning the aux framer link
            such as main framer or main frame or actor
        desc is string description of framer link such as 'aux' or 'clone'
        contexts is list of allowed schedule contexts, None or empty means any.
        human is human readable version of associated declaration
        count is line number of associated declaration

        Framer.Names registry must already be setup
    """
    if not isinstance(aux, Framer):
        if aux not in framer.auxes:
            msg = "ResolveError: Bad {0} link name '{1}'".format(desc, aux)
            raise excepting.ResolveError(msg, framer.name, who, human, count)
        aux = framer.auxes[aux]
        if contexts:
            if aux.schedule not in contexts:
                raise excepting.ResolveError('ResolveError: Bad {0} link not scheduled as one of {1}'.format(desc, [ScheduleNames.get(context, context) for context in contexts]), aux.name, who, human, count)
        console.concise("         Resolved {0} Framer '{1}' with tag '{2}' in {3}\n".format(desc, aux.name, aux.tag, who))
    return aux


def resolveFramer(framer, who='', desc='framer', contexts=None, human='', count=None):
    """ Returns resolved framer instance from framer
        framer may be name of framer or instance
        who is optional name of object owning the link
        such as framer or frame or actor
        desc is string description of framer link such as 'aux' or 'framer'
        contexts is list of allowed schedule contexts, None or empty means any.
        human is human readable version of associated declaration
        cout is line number of associated declaration

        Framer.Names registry must already be setup
    """
    if not isinstance(framer, Framer):
        if framer not in Framer.Names:
            raise excepting.ResolveError('ResolveError: Bad {0} link name'.format(desc), framer, who, human, count)
        else:
            framer = Framer.Names[framer]
            if not isinstance(framer, Framer):
                raise excepting.ResolveError('ResolveError: Bad {0} link name, tasker not framer'.format(desc), self.name, aux.name, human, count)
            if contexts:
                if framer.schedule not in contexts:
                    raise excepting.ResolveError('ResolveError: Bad {0} link not scheduled as one of {1}'.format(desc, [ScheduleNames.get(context, context) for context in contexts]), framer.name, who, human, count)
        console.concise("         Resolved {0} Framer '{1}' in {2}\n".format(desc, framer.name, who))
    return framer


ResolveFramer = resolveFramer

def resolveFrame(frame, who='', desc='act', human='', count=None):
    """ Returns resolved frame instance from frame
        frame may be name of frame or instance

        Frame.Names registry must be setup
        This is usuall done in the Framer and Frame .resolve since the registry
        is setup in this case. In other cases use resolveFrameOfFramer
    """
    if not isinstance(frame, Frame):
        if frame not in Frame.Names:
            raise excepting.ResolveError('ResolveError: Bad {0} Frame link name'.format(desc), frame, who, human, count)
        frame = Frame.Names[frame]
        console.concise("         Resolved {0} Frame '{1}' in {2}\n".format(desc, frame.name, who))
    return frame


ResolveFrame = resolveFrame

def resolveFrameOfFramer(frame, framer, who='', desc='act', human='', count=None):
    """ Returns resolved frame instance from frame
        frame may be name of frame or instance

        Resolves relative to the framer's .frameNames registry
        This is appropriate for Actor.resolve since it guarantees the context
        of the frame name space
    """
    if not isinstance(frame, Frame):
        if frame not in framer.frameNames:
            raise excepting.ResolveError("ResolveError: Bad {0} Frame link name in Framer '{1}'".format(desc, framer.name), frame, who, human, count)
        frame = framer.frameNames[frame]
        console.concise("         Resolved {0} Frame '{1}' in {2}\n".format(desc, frame.name, who))
    return frame


ResolveFrameOfFramer = resolveFrameOfFramer