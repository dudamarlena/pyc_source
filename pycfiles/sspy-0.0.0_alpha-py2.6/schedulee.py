# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mando/neurospaces_project/sspy/source/snapshots/0/build/lib/sspy/schedulee.py
# Compiled at: 2011-09-15 17:42:42
"""!
@file schedulee.py

This file contains the implementation for a basic schedulee.
This was formerly called SimpleHeccer in a previous implementation.
The name is kept general since it will become pluggable. This class
mainly functions as an abstraction to handle error checking
and strict typing. 
"""
import pdb, sys
from errors import ScheduleeError
schedulee_types = [
 'solver', 'input', 'output']

class Schedulee:
    """!
    @brief Abstraction class for schedulee objects.
    """

    def __init__(self, schedulee=None, schedulee_type=None, verbose=False):
        if schedulee is None:
            raise ScheduleeError('Not defined')
        if schedulee_type is None:
            raise ScheduleeError('Type not defined')
        if schedulee_type not in schedulee_types:
            raise ScheduleeError("Invalid type '%s'" % schedulee_type)
        try:
            self.time_step = schedulee.GetTimeStep()
        except Exception, e:
            raise ScheduleeError("Can't obtain time step: %s\n" % e)

        if self.time_step < 0.0 or self.time_step is None:
            raise ScheduleeError("Invalid step value: '%s'\n" % self.time_step)
        self.current_time = 0.0
        self.current_step = 0
        self._schedulees_type = schedulee_type
        self._schedulee = schedulee
        self.type = schedulee_type
        self.verbose = verbose
        return

    def Finish(self):
        """

        """
        try:
            self._schedulee.Finish()
        except Exception, e:
            raise ScheduleeError('%s' % e)

    def GetCore(self):
        """

        """
        return self._schedulee

    def GetName(self):
        return self._schedulee.GetName()

    def GetType(self):
        return self.type

    def New(self, model, name, filename):
        """
        not needed?
        """
        pass

    def Pause(self):
        """
        not sure how this will work
        """
        pass

    def Step(self):
        try:
            self._schedulee.Step(self.current_time)
        except Exception, e:
            raise ScheduleeError('%s' % e)

        self.current_time += self.time_step
        self.current_step += 1

    def SetTimeStep(self, time_step):
        """

        """
        try:
            return self._schedulee.SetTimeStep(time_step)
        except TypeError, e:
            return ScheduleeError("Can't set time step: %s" % e)

    def GetTimeStep(self):
        """

        """
        try:
            return self._schedulee.GetTimeStep()
        except TypeError, e:
            return ScheduleeError("Can't retrieve time step: %s" % e)

    def GetCurrentStep(self):
        """
        @brief Returns the current step
        """
        return self.current_step

    def GetCurrentTime(self):
        """
        @brief Returns the current simulation time
        """
        return self.current_time

    def Compile(self):
        try:
            self._schedulee.Compile()
        except Exception, e:
            raise ScheduleeError('%s' % e)

    def Initialize(self):
        try:
            self._schedulee.Initialize()
        except Exception, e:
            raise ScheduleeError('%s' % e)

        self.current_time = 0.0

    def Report(self):
        """

        """
        if self.verbose:
            pass
        try:
            self._schedulee.Report()
        except Exception, e:
            raise ScheduleeError("Can't report schedulee for '%s': %s" % (self.GetName(), e))

    def Run(self, time):
        pass