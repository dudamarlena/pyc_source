# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/base/tasking.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 8463 bytes
"""tasking.py weightless thread scheduling

"""
from ..aid.sixing import *
from .globaling import *
from ..aid.odicting import odict
from . import excepting
from . import registering
from . import storing
from ..aid.consoling import getConsole
console = getConsole()

def CreateInstances(store):
    """Create server instances which automatically get registered on object creation
       must be function so can recreate after clear registry
    """
    tasker = Tasker(name='tasker', store=store)


class Tasker(registering.StoriedRegistrar):
    __doc__ = 'Task class, Base class for weightless threads\n\n    '
    Counter = 0
    Names = {}

    def __init__(self, period=0.0, schedule=INACTIVE, **kw):
        """
        Initialize instance.

        Inherited instance attributes
            .name = unique name for tasker
            .store = data store

        Instance attributes
            .period = desired time in seconds between runs,non negative, zero means asap
            .stamp = depends on subclass default is time tasker last RUN
            .status = operational status of tasker
            .desire = desired control asked by this or other taskers
            .done = tasker completion state True or False
            .schedule = initial scheduling context for this tasker vis a vis skedder
            .runner = generator to run tasker

         The registry class will supply unique name when name is empty by using
         the .__class__.__name__ as the default preface to the name.
         To use a different default preface add this to the .__init__ method
         before the super call

         if 'preface' not in kw:
             kw['preface'] = 'MyDefaultPreface'

        """
        (super(Tasker, self).__init__)(**kw)
        self.period = float(abs(period))
        self.stamp = 0.0
        self.presolved = False
        self.resolved = False
        self.status = STOPPED
        self.desire = STOP
        self.done = True
        self.schedule = schedule
        self.runner = None
        self.remake()

    def reinit(self, period=None, schedule=None, **kw):
        if period is not None:
            self.period = period
        if schedule is not None:
            self.schedule = schedule

    def remake(self):
        """Re make runner generator

           .send(None) same as .next()
        """
        self.runner = self.makeRunner()
        status = self.runner.send(None)
        if console._verbosity >= console.Wordage.profuse:
            self.expose()

    def expose(self):
        """

        """
        print('     Task %s status = %s' % (self.name, StatusNames[self.status]))

    def presolve(self, **kwa):
        """Presolves any links to aux clones"""
        self.presolved = True

    def resolve(self, **kwa):
        """Resolves any by name links to other objects   """
        self.resolved = True

    def ready(self):
        """ready runner

        """
        return self.runner.send(READY)

    def start(self):
        """start runner

        """
        return self.runner.send(START)

    def run(self):
        """run runner

        """
        return self.runner.send(RUN)

    def stop(self):
        """stop runner

        """
        return self.runner.send(STOP)

    def abort(self):
        """abort runner

        """
        return self.runner.send(ABORT)

    def makeRunner(self):
        """generator factory function to create generator to run this tasker

           Should be overridden in sub class
        """
        console.profuse('     Making Task Runner {0}\n'.format(self.name))
        self.status = STOPPED
        self.desire = STOP
        self.done = True
        count = 0
        try:
            while True:
                control = yield self.status
                console.profuse('\n     Iterate Tasker {0} with control = {1} status = {2}\n'.format(self.name, ControlNames.get(control, 'Unknown'), StatusNames.get(self.status, 'Unknown')))
                if control == RUN:
                    if self.status == STARTED or self.status == RUNNING:
                        console.profuse('     Running Tasker {0} ...\n'.format(self.name))
                        self.status = RUNNING
                    else:
                        console.profuse('     Need to Start Tasker {0}\n'.format(self.name))
                        self.desire = START
                else:
                    if control == READY:
                        console.profuse('     Readying Tasker {0} ...\n'.format(self.name))
                        self.desire = START
                        self.status = READIED
                    else:
                        if control == START:
                            console.terse('     Starting Tasker {0} ...\n'.format(self.name))
                            self.desire = RUN
                            self.status = STARTED
                            self.done = False
                        else:
                            if control == STOP:
                                if self.status == RUNNING or self.status == STARTED:
                                    console.terse('     Stopping Tasker {0} ...\n'.format(self.name))
                                    self.desire = STOP
                                    self.status = STOPPED
                                    self.done = True
                                else:
                                    console.terse('     Tasker {0} not started or running.\n'.format(self.name))
                            else:
                                if control == ABORT:
                                    console.profuse('     Aborting Tasker {0} ...\n'.format(self.name))
                                    self.desire = ABORT
                                    self.status = ABORTED
                                    self.done = True
                                else:
                                    self.desire = ABORT
                                    self.status = ABORTED
                                    console.profuse('     Aborting Tasker {0}, bad control = {1}\n'.format(self.name, CommandNames[control]))
                                    break
                    self.stamp = self.store.stamp

        finally:
            console.profuse('     Exception causing Abort Tasker {0} ...\n'.format(self.name))
            self.desire = ABORT
            self.status = ABORTED


def resolveTasker(tasker, who='', desc='tasker', contexts=None, human='', count=None):
    """ Returns resolved tasker instance from tasker
        tasker may be name of tasker or instance
        who is optional name of object owning the link
        such as framer or frame or actor
        desc is string description of tasker link such as 'aux' or 'framer'
        contexts is list of allowed schedule contexts, None or empty means any.
        Taskers.Names registry must already be setup
    """
    if not isinstance(tasker, Tasker):
        if tasker not in Tasker.Names:
            raise excepting.ResolveError('ResolveError: Bad {0} link name'.format(desc), tasker, who, human, count)
        tasker = Tasker.Names[tasker]
        if contexts:
            if tasker.schedule not in contexts:
                raise excepting.ResolveError('ResolveError: Bad {0} link not scheduled as one of {1}'.format(desc, contexts), tasker.name, who, human, count)
        console.concise("         Resolved {0} Tasker '{1}' in '{2}'\n".format(desc, tasker.name, who))
    return tasker


ResolveTasker = resolveTasker