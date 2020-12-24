# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/HdlLib/SysGen/FiniteStateMachine.py
# Compiled at: 2017-07-08 08:29:58
# Size of source mod 2**32: 12717 bytes
import os, sys, logging, networkx as nx
from HdlLib.SysGen.Signal import Signal
from HdlLib.SysGen.Condition import Condition
from HdlLib.SysGen.Assignment import AssignmentStatement
import collections

class FSMState:
    __doc__ = '\n\tState object used as Node in Networkx graph.\n\t'

    def __init__(self, Name, Position):
        """
                Initialize Name, Entering Condition object and list of assignments.
                """
        self.__name__ = Name
        self.EnteringCondition = {}
        self.Assignments = []
        self.FollowingStates = {}
        self._AssignedSignals = []
        self.Position = Position
        self.InputCtrlSignals = []
        self._TransitionAssignment = []

    def GetEnteringCondition(self, FromState=None):
        """
                return Entering Condition object.
                """
        if FromState is None:
            return self.EnteringCondition
        if FromState in self.EnteringCondition:
            self.EnteringCondition[FromState]
        else:
            return

    def AddEnteringConditionFrom(self, State, Cond):
        """
                Update dictionary of Entering Conditions.
                When State => 
                        if Cond then 
                                FutureStep => self
                """
        self.EnteringCondition[State] = Cond
        State.FollowingStates[self] = Cond

    def GetAssignments(self, ReqList=[], SkipList=[]):
        """
                return list of assignments.
                """
        if len(SkipList) == 0 and len(ReqList) == 0:
            for A in self.Assignments:
                yield A

        else:
            if len(SkipList) == 0:
                for A in self.Assignments:
                    Skip = False
                    for AS in A.GetAssignedSignals():
                        if AS.Name not in ReqList:
                            Skip = True

                    if Skip is True:
                        continue
                    else:
                        yield A

            else:
                for A in self.Assignments:
                    Skip = False
                    for AS in A.GetAssignedSignals():
                        if AS.Name in SkipList:
                            Skip = True

                    if Skip is True:
                        continue
                    else:
                        yield A

    def AddAssignment(self, Assignment):
        """
                Add assignment to list of assignments.
                """
        if Assignment is None:
            raise TypeError("[FSMState:AddAssignment] Cannot use 'None' as Assignment")
        self.Assignments.insert(0, Assignment)
        self._AssignedSignals += Assignment.GetAssignedSignals()

    def AddTransitionAssignment(self, Assignment):
        """
                Add assignment to list of assignments BUT ON STATE TRANSITION.
                Set TransitionAssignment Attribute
                """
        if Assignment is None:
            raise TypeError("[FSMState:AddAssignment] Cannot use 'None' as Assignment")
        self._TransitionAssignment.insert(0, Assignment)
        self._AssignedSignals += Assignment.GetAssignedSignals()

    def GetTransitionAssignments(self):
        """
                return self._TransitionAssignment attribute
                """
        return self._TransitionAssignment

    def AddInputCtrl(self, InCtrls):
        """
                Set InputCtrlSignals attribute.
                """
        self.InputCtrlSignals += InCtrls

    def GetName(self):
        """
                return name of FSM state
                """
        return self.__name__

    def __repr__(self):
        """
                return name of FSM state
                """
        return '<FSMState {0}>'.format(self.__name__)

    def __str__(self):
        """
                return name of FSM state
                """
        return self.__name__


class FSM:
    __doc__ = '\n\tState object used as FSM using Networkx graph.\n\t'

    def __init__(self, Name):
        """
                Initialize Name, Entering Condition object and list of assignments.
                """
        self.__name__ = Name
        self.Graph = nx.DiGraph()
        self.EndStates = []
        self._Names = []
        self._Tags = {}
        self.FSMInitState = self.AddState(Cond=None, Name='Init')
        self.ResetAssignments = []
        self._UsedRegisters = []
        self.CounterSignals = []

    def InitState(self):
        """
                return Initialization state.
                """
        return self.FSMInitState

    def AddState(self, Cond=None, Name=None):
        """
                return name of FSM state.
                """
        if Name is None:
            Name = str(len(self._Names))
        if Name in self._Names:
            NB = 0
            for N in self._Names:
                if N == Name:
                    NB += 1

            self._Names.append(Name)
            Name += '_' + str(NB + 1)
        else:
            self._Names.append(Name)
        Name = 'STATE_{0}'.format(Name.upper())
        NewState = FSMState(Name=Name, Position=len(self.Graph.nodes()))
        self.Graph.add_node(NewState, color='black', style='filled', fillcolor='white')
        Previous = self.EndStates.pop(0) if len(self.EndStates) != 0 else None
        self.EndStates.append(NewState)
        if Previous != None:
            if Cond:
                C = Cond
                self.Graph.add_edge(Previous, Previous, weight=1, label=str(C.Complement()), arrowhead='open')
                Previous.AddEnteringConditionFrom(Previous, None)
            else:
                C = Condition()
            NewState.AddEnteringConditionFrom(Previous, C)
            self.Graph.add_edge(Previous, NewState, weight=1, label=str(C), arrowhead='open')
        logging.debug("Add new state '{0}'".format(NewState))
        return NewState

    def SetTag(self, Tag, Anteriority=None):
        """
                Add tag to tag dictionary to mark a specific step with a tag.
                """
        if len(self.EndStates) == 0:
            logging.error("No states are currently set up as 'end state'. Unable to tag end states as '{0}'. Maybe the FSM is already closed.".format(Tag))
            return False
        else:
            if Anteriority is None or Anteriority == 1:
                self._Tags[Tag] = self.EndStates[0]
                return True
            PList = self.EndStates
            for A in range(Anteriority - 1):
                PList = self.Graph.predecessors(PList[0])

            self._Tags[Tag] = PList[0]
            return True

    def GetStepByTag(self, Tag):
        """
                Return step tagged with tag from tag dictionary.
                """
        if Tag in self._Tags:
            return self._Tags[Tag]
        else:
            return

    def CloseLoop(self, InitEnteringCondition=None, Serialization=1, LoopStep=None):
        """
                Link last state to Init state
                """
        for S in self.EndStates:
            if Serialization != 1:
                if LoopStep is None:
                    logging.error("Loop step cannot be None if Serialization!=1 (here Serialization='{0}').".format(Serialization))
                    continue
                else:
                    CounterSignal = Signal(Name='SerializationCounter', Type='numeric')
                    LoopCondition = Condition()
                    HDLCounterSignal = CounterSignal.HDLFormat()
                    HDLCounterSignal.SetValue(Serialization, TypeOfValue='logic')
                    HDLCounterSignal.SetTestCondition('__lt__')
                    LoopCondition.AddANDCond(HDLCounterSignal)
                    HDLCounterSignal.SetTestCondition('__eq__')
                    LoopStep.AddEnteringConditionFrom(S, LoopCondition)
                    Label = str(LoopCondition)
                    self.Graph.add_edge(S, LoopStep, weight=1, label=Label, arrowhead='open')
                    self._UsedRegisters.append(CounterSignal)
                    self.CounterSignals.append(CounterSignal.Name)
                    CntResetAssign = AssignmentStatement(Assignee=HDLCounterSignal, Assignor=0, Cond=None, Desc='Reset loop counter')
                    LoopStepSuccessors = self.Graph.successors(LoopStep)
                    for N in self.Nodes():
                        if not N == LoopStep:
                            if N in LoopStepSuccessors:
                                N.AddAssignment(AssignmentStatement(Assignee=HDLCounterSignal, Assignor=HDLCounterSignal, Cond=None, Desc='Increment loop counter'))
                            else:
                                N.AddAssignment(CntResetAssign)
                        else:
                            Cond = None
                            for Successor in self.Graph.successors(N):
                                Cond = Successor.GetEnteringCondition()[N]
                                if Cond is not None:
                                    break

                            N.AddAssignment(AssignmentStatement(Assignee=HDLCounterSignal, Assignor='{0}+1'.format(HDLCounterSignal.GetName()), Cond=Cond, Desc='Increment loop counter'))

                if InitEnteringCondition:
                    Label = '' if InitEnteringCondition is None else str(InitEnteringCondition.Complement())
                    self.Graph.add_edge(S, S, weight=1, label=Label, arrowhead='open')
                    S.AddEnteringConditionFrom(S, None)
                self.FSMInitState.AddEnteringConditionFrom(S, InitEnteringCondition)
                Label = '' if InitEnteringCondition is None else str(InitEnteringCondition)
                self.Graph.add_edge(S, self.FSMInitState, weight=1, label=Label, arrowhead='open')

        self.EndStates = []

    def GetUsedSignals(self, HDLFormat=True):
        """
                Return list of internally used signals as HDL format.
                """
        if HDLFormat:
            return [x.HDLFormat() for x in self._UsedRegisters]
        else:
            return self._UsedRegisters

    def Nodes(self):
        """
                return list of state nodes in graph.
                """
        return self.Graph.nodes()

    def AddAssignment(self, Assignment, OnTransition=False):
        """
                Add assignment in state.
                """
        LastState = self.EndStates[0] if len(self.EndStates) != 0 else None
        if LastState is None or Assignment is None:
            return
        if OnTransition is True:
            LastState.AddTransitionAssignment(Assignment)
        else:
            LastState.AddAssignment(Assignment)

    def AddResetAssignment(self, Assignment):
        """
                Add assignment to list of reset assignments.
                """
        if Assignment is None:
            raise TypeError("[FSMState:AddAssignment] Cannot use 'None' as Assignment")
        self.ResetAssignments.insert(0, Assignment)

    def AddResetAssignmentSignals(self, SignalList):
        """
                Add assignment to list of reset assignments.
                """
        for S in SignalList:
            HDLSig = S.HDLFormat()
            RA = AssignmentStatement(Assignee=HDLSig, Assignor=HDLSig.GetInitialValue(), Cond=None, Desc='Default value')
            self.AddResetAssignment(RA)

    def GetResetAssignments(self):
        """
                return list of reset assignments.
                """
        return self.ResetAssignments

    def CompleteAssignments(self, CtrlSigs=[], OnTransition=False):
        """
                For each node, if a control signal is not assigned, add it. 
                """
        for N in self.Graph.nodes():
            AS = [x.Name for x in N._AssignedSignals]
            for C in CtrlSigs:
                if C.Name not in AS:
                    A = AssignmentStatement(Assignee=C, Assignor=None, Cond=None, Desc='')
                    if OnTransition is True:
                        N.AddTransitionAssignment(A)
                    else:
                        N.AddAssignment(A)

    def ToPNG(self, OutputPath='./'):
        """
                Dumb graph to PNG file using pyGraphviz.
                """
        try:
            G = nx.to_agraph(self.Graph)
        except:
            logging.error('Unable to draw FSM graph (pygraphviz installation or python3 incompatibility may be the cause)')
            return

        G.layout('dot', args='-Nfontsize=10 -Nwidth=".2" -Nheight=".2" -Nmargin=0 -Gfontsize=8 -Efontsize=8')
        FilePath = os.path.join(OutputPath, '{0}.png'.format(self.__name__))
        if not os.path.isdir(OutputPath):
            os.makedirs(OutputPath)
        G.draw(FilePath)
        return FilePath

    def GetName(self):
        """
                return name of FSM state
                """
        return self.__name__

    def __str__(self):
        """
                return name of FSM state
                """
        return self.__name__