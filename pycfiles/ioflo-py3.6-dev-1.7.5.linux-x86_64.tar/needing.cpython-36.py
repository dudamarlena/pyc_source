# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/base/needing.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 21170 bytes
"""needing.py need action module

"""
import time, struct
from collections import deque
import inspect
from ..aid.sixing import *
from .globaling import *
from ..aid.odicting import odict
from ..aid import aiding
from ..aid.timing import tuuid
from . import excepting
from . import registering
from . import storing
from . import acting
from . import tasking
from . import framing
from ..aid.consoling import getConsole
console = getConsole()

class Need(acting.Actor):
    __doc__ = 'Need Class for conditions  such as entry or trans\n    '
    Registry = odict()

    def __init__(self, **kwa):
        (super(Need, self).__init__)(**kwa)
        self._tracts = []

    def _expose(self):
        """
        """
        print('Need %s ' % self.name)

    @staticmethod
    def Check(state, comparison, goal, tolerance):
        """Check state compared to goal with tolerance
           tolerance ignored unless comparison == or !=
        """
        if comparison == '==':
            try:
                result = goal - abs(tolerance) <= state <= goal + abs(tolerance)
            except TypeError:
                result = goal == state

        else:
            if comparison == '<':
                result = state < goal
            else:
                if comparison == '<=':
                    result = state <= goal
                else:
                    if comparison == '>=':
                        result = state >= goal
                    else:
                        if comparison == '>':
                            result = state > goal
                        elif comparison == '!=':
                            try:
                                result = not goal - abs(tolerance) <= state <= goal + abs(tolerance)
                            except TypeError:
                                result = goal != state

                        else:
                            result = False
            return result

    def addTract(self, act):
        """
        Add act to ._tracts list
        """
        self._tracts.append(act)
        act.frame = self._act.frame.name
        act.context = ActionSubContextNames[TRANSIT]


class NeedAlways(Need):
    __doc__ = 'NeedAlways Need  Special Need'

    def action(self, **kw):
        """Always return true"""
        result = True
        console.profuse('Need Always = {0}\n'.format(result))
        return result


class NeedDone(Need):
    __doc__ = '\n    NeedDone Need Special Need\n    '

    def _resolve(self, tasker, **kwa):
        parms = (super(NeedDone, self)._resolve)(**kwa)
        parms['tasker'] = tasker = tasking.resolveTasker(tasker, who=(self._act.frame.name),
          desc='need done',
          contexts=[],
          human=(self._act.human),
          count=(self._act.count))
        return parms

    def action(self, tasker, **kw):
        """
        Check if  tasker done
        parameters:
            tasker
        """
        result = tasker.done
        console.profuse('Need Tasker {0} done = {1}\n'.format(tasker.name, result))
        return result


class NeedDoneAux(Need):
    __doc__ = '\n    NeedDoneAux Need Special Need\n    '

    def _resolve(self, tasker, framer, frame, **kwa):
        parms = (super(NeedDoneAux, self)._resolve)(**kwa)
        if framer:
            if framer == 'me':
                framer = self._act.frame.framer
            parms['framer'] = framer = framing.resolveFramer(framer, who=(self._act.frame.name),
              desc='need done',
              contexts=[],
              human=(self._act.human),
              count=(self._act.count))
        if frame:
            if frame == 'me':
                frame = self._act.frame
            parms['frame'] = frame = framing.resolveFrameOfFramer(frame, framer,
              who=(self._act.frame.name),
              desc='need done',
              human=(self._act.human),
              count=(self._act.count))
        if tasker not in ('any', 'all'):
            parms['tasker'] = tasker = framing.resolveAuxOfFramer(tasker, framer,
              who=(self._act.frame.name),
              desc='need done aux',
              contexts=[],
              human=(self._act.human),
              count=(self._act.count))
        return parms

    def action(self, tasker, framer, frame, **kw):
        """
        Check if  aux done
        parameters:
            aux
            framer
            frame
        """
        if frame:
            if tasker == 'any':
                result = any([aux.done for aux in frame.auxes])
            else:
                if tasker == 'all':
                    result = frame.auxes and all([aux.done for aux in frame.auxes])
                else:
                    if tasker in frame.auxes:
                        result = tasker.done
                    else:
                        result = False
            name = tasker if tasker in ('any', 'all') else tasker.tag
            console.profuse('Need Aux {0} done = {1} in {2}<{3}\n'.format(name, result, framer.name, frame.name))
        else:
            result = tasker.done
            console.profuse('Need Aux {0} done = {1}\n'.format(tasker.name, result))
        return result


class NeedStatus(Need):
    __doc__ = 'NeedStatus Need Special Need '

    def _resolve(self, tasker, **kwa):
        parms = (super(NeedStatus, self)._resolve)(**kwa)
        if tasker == 'me':
            tasker = self._act.frame.framer
        parms['tasker'] = tasker = tasking.resolveTasker(tasker, who=(self.name),
          desc='need status tasker',
          contexts=[],
          human=(self._act.human),
          count=(self._act.count))
        return parms

    def action(self, tasker, status, **kw):
        """
        Check if  tasker done
        parameters:
          tasker
          status
        """
        result = tasker.status == status
        console.profuse('Need Tasker {0} status is {1} = {2}\n'.format(tasker.name, StatusNames[status], result))
        return result


class NeedState(Need):
    __doc__ = '\n    NeedState is a base class for Needs that must resolve a state share ref\n    '

    def _resolve(self, state, stateField, **kwa):
        parms = (super(NeedState, self)._resolve)(**kwa)
        parms['state'] = state = self._resolvePath(ipath=state, warn=True)
        if not stateField:
            if state:
                if 'value' in state:
                    stateField = 'value'
                else:
                    msg = "ResolveError: Can't determine field for state '{0}'".format(state.name)
                    raise excepting.ResolveError(msg, 'state', self.name, self._act.human, self._act.count)
            else:
                stateField = 'value'
        if stateField not in state:
            console.profuse("     Warning: Non-existent field '{0}' in state {1} ... creating anyway".format(stateField, state.name))
            state[stateField] = 0.0
        parms['stateField'] = stateField
        return parms


class NeedBoolean(NeedState):
    __doc__ = 'NeedBoolean Need Special Need\n\n       if state\n    '

    def action(self, state, stateField, **kw):
        """ Check if state[stateField] evaluates to True
            parameters:
              state = share of state
              stateField = field key

        """
        if state[stateField]:
            result = True
        else:
            result = False
        console.profuse('Need Boolean, if {0}[{1}]: = {2}\n'.format(state.name, stateField, result))
        return result


class NeedDirect(NeedState):
    __doc__ = 'NeedDirect Need\n\n       if state comparison goal [+- tolerance]\n    '

    def action(self, state, stateField, comparison, goal, tolerance, **kw):
        """ Check if state[field] comparison to goal +- tolerance is True
            parameters:
                state = share of state
                stateField = field key
                comparison
                goal
                tolerance

        """
        result = self.Check(state[stateField], comparison, goal, tolerance)
        console.profuse('Need Direct, if {0}[{1}] {2} {3} +- {4}: = {5}\n'.format(state.name, stateField, comparison, goal, tolerance, result))
        return result


class NeedIndirect(NeedState):
    __doc__ = 'NeedIndirect Need\n\n       if state comparison goal [+- tolerance]\n    '

    def _resolve(self, goal, goalField, **kwa):
        parms = (super(NeedIndirect, self)._resolve)(**kwa)
        parms['goal'] = goal = self._resolvePath(ipath=goal, warn=True)
        if not goalField:
            if goal:
                if 'value' in goal:
                    goalField = 'value'
                else:
                    goalField = stateField
            else:
                goalField = 'value'
        if goalField not in goal:
            console.profuse("     Warning: Non-existent field '{0}' in goal {1} ... creating anyway".format(goalField, goal.name))
            goal[goalField] = 0.0
        parms['goalField'] = goalField
        return parms

    def action(self, state, stateField, comparison, goal, goalField, tolerance, **kwa):
        """ Check if state[field] comparison to goal[goalField] +- tolerance is True
                       parameters:
              state = share of state
              stateField = field key
              comparison
              goal
              goalField
              tolerance

        """
        result = self.Check(state[stateField], comparison, goal[goalField], tolerance)
        console.profuse('Need Indirect, if {0}[{1}] {2} {3}[{4}] +- %s: = {5}\n'.format(state.name, stateField, comparison, goal, goalField, tolerance, result))
        return result


class NeedMarker(Need):
    __doc__ = '\n    NeedMarker is base class for needs that insert markers on resolvelinks\n    Special Need\n\n    '

    def _resolve(self, share, frame, kind, marker, **kwa):
        parms = (super(NeedMarker, self)._resolve)(**kwa)
        framer = self._act.frame.framer
        enacted = True if frame else False
        if not frame or frame == 'me':
            frame = self._act.frame
        else:
            frame = framing.resolveFrameOfFramer(frame, framer,
              who=(self.name),
              desc='need marker',
              human=(self._act.human),
              count=(self._act.count))
            parms['share'] = share = self._resolvePath(ipath=share, warn=True)
            parts = [framer.name]
            if marker:
                parts.append(marker)
            else:
                parts.append(frame.name)
        marker = '<'.join(parts)
        parms['marker'] = marker
        if not share.marks.get(marker):
            share.marks[marker] = storing.Mark()
        if kind not in acting.Actor.Registry:
            msg = 'ResolveError: Bad need marker link'
            raise excepting.ResolveError(msg, kind, self.name, self._act.human, self._act.count)
        markerParms = dict(share=share, marker=marker)
        markerAct = acting.Act(actor=kind, registrar=(acting.Actor),
          parms=markerParms,
          human=(self._act.human),
          count=(self._act.count))
        self.addTract(markerAct)
        console.profuse('     Added {0} {1} with {2} at {3} in {4} of framer {5}\n'.format('tract', markerAct, markerAct.parms['share'].name, markerAct.parms['marker'], self._act.frame.name, framer.name))
        markerAct.resolve()
        if enacted:
            found = False
            for enact in frame.enacts:
                if isinstance(enact.actor, acting.Actor) and enact.actor.name == kind and enact.parms['share'].name == share.name and enact.parms['marker'] == marker:
                    found = True
                    break

            if not found:
                markerParms = dict(share=share, marker=marker)
                markerAct = acting.Act(actor=kind, registrar=(acting.Actor),
                  parms=markerParms,
                  human=(self._act.human),
                  count=(self._act.count))
                frame.insertEnact(markerAct)
                console.profuse('     Added {0} {1} with {2} at {3} in {4} of framer {5}\n'.format('enact', markerAct, markerAct.parms['share'].name, markerAct.parms['marker'], frame.name, framer.name))
                markerAct.resolve()
        return parms


class NeedUpdate(NeedMarker):
    __doc__ = ' NeedUpdate Need Special Need '

    def action(self, share, marker, **kw):
        """
        Check if share updated since mark in share was updated by marker
        Default is False

        Parameters:
            share is resolved share that is marked with .mark[marker]
            marker is marker key
        """
        result = False
        mark = share.marks.get(marker)
        if mark:
            if share.stamp is not None:
                result = mark.stamp is None or share.stamp > mark.stamp or share.stamp == mark.stamp and mark.used != mark.stamp
        console.profuse('Marker update {0} for {1} of Share {2} {3}  {4} mark {5} used {6} at {7}\n'.format(result, marker, share.name, share.stamp, '>=', mark.stamp, mark.used, self.store.stamp))
        return result


class NeedChange(NeedMarker):
    __doc__ = 'NeedChange Need Special Need'

    def action(self, share, marker, **kw):
        """
        Check if share data changed while denoted by marker key if any
        Default is False

        Parameters:
            share is resolved share that is marked with .mark[marker]
            marker is marker key
        """
        result = False
        mark = share.marks.get(marker)
        if mark:
            if mark.data is None:
                result = True
            else:
                for field, value in share.items():
                    try:
                        if getattr(mark.data, field) != value:
                            result = True
                    except AttributeError as ex:
                        result = True

                    if result:
                        break

        console.profuse('Marker change {0} for {1} of data {2} of share {3} at {4}\n'.format(result, marker, mark.data if mark else None, share.name, self.store.stamp))
        return result