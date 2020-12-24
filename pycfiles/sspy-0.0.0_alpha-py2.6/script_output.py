# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/sspy/plugins/outputs/script_out/script_output.py
# Compiled at: 2011-09-15 17:42:42
"""
This is the output plugin for outputting data
from connected solvers into a live data structure
"""
import os, pdb, sys

class Output:

    def __init__(self, name='Untitled Output', plugin=None, arguments=None, verbose=False):
        self._name = name
        self._plugin_data = plugin
        self.verbose = verbose
        self.time_step = 0.0
        self._solver = None
        self._command = None
        self._command_object = None
        return

    def Compile(self):
        """
        @brief 
        """
        self._line_output.Compile()

    def Finish(self):
        """
        @brief 
        """
        self._line_output.Finish()

    def GetName(self):
        """
        @brief 
        """
        return self._name

    def Name(self):
        return self._name

    def SetOutputs(self, outputs):
        """
        @brief Sets the list of outputs

        Needs to be saved for later since they cannot be set
        until the solver is created after a connect. 
        """
        self.outputs = outputs

    def AddOutput(self, name, field):
        """!

        @brief Adds an output to the solver

        Performs a check for the solver type. Any issues after the solver check
        should throw an exception. 
        """
        if self._solver is None:
            self.outputs.append(dict(field=field, component_name=name))
        else:
            solver_type = self._solver.GetType()
            if solver_type == 'heccer':
                my_heccer = self._solver.GetCore()
                address = my_heccer.GetAddress(name, field)
                self._line_output.AddOutput(name, address)
        return

    def GetTimeStep(self):
        """
        """
        return self.time_step

    def SetTimeStep(self, time_step):
        """
        """
        self.time_step = time_step

    def GetType(self):
        return self._plugin_data.GetName()

    def Finish(self):
        self._line_output.Finish()

    def Initialize(self):
        self.current_simulation_time = 0.0
        self.current_step = 0

    def Reset(self):
        """!
        @brief Destroys and recreates the core output object
        """
        self._line_output = None
        self.Initialize()
        return

    def Connect(self, solver):
        """!
        @brief Connects the output to a solver

        To properly connect a solver and an output you must:

            1. Retrieve the timestep from the solver and set it
            with the SetTimeStep method to ensure the scheudlee
            properly updates the object.

            2. Connect the solver core to the output core.

            3. Add the outputs via whatever method the cores use
            to communicate.

        """
        self._solver = solver
        solver_type = solver.GetType()
        self.Initialize()
        if solver_type == 'heccer':
            my_heccer = solver.GetCore()
            time_step = my_heccer.GetTimeStep()
            self.SetTimeStep(time_step)
        else:
            raise Exception("Incompatible solver '%s'" % solver_type)

    def Step(self, time=None):
        """

        """
        self.current_simulation_time += self.time_step
        self.current_step += 1

    def Report(self):
        pass

    def Command(self, cmd):
        pass

    def CommandObject(self, obj):
        pass