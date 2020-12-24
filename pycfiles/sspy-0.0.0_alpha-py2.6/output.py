# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mando/neurospaces_project/sspy/source/snapshots/0/build/lib/sspy/plugins/outputs/output/output.py
# Compiled at: 2011-09-15 17:42:41
"""
This is the output plugin for outputting data
from connected solvers
"""
import os, pdb, sys
try:
    import experiment.output as og
except ImportError, e:
    sys.exit('Error importing the Experiment Output Python module: %s\n' % e)

_default_filename = '/tmp/OutputGenerator'

class Output:

    def __init__(self, name='Untitled Output', plugin=None, filename=None, arguments=None, verbose=False):
        self._name = name
        self._plugin_data = plugin
        self.verbose = verbose
        self.time_step = 0.0
        self._output_gen = None
        self.filename = _default_filename
        self.format = None
        self.mode = None
        self.resolution = None
        self.outputs = []
        self._solver = None
        if arguments is not None:
            self._ParseArguments(arguments)
        return

    def Compile(self):
        """
        @brief 
        """
        self._output_gen.Compile()

    def Finish(self):
        """
        @brief 
        """
        self._output_gen.Finish()

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
            try:
                solver_type = self._solver.GetType()
                my_solver = self._solver.GetCore()
                address = my_solver.GetAddress(name, field)
                self._output_gen.AddOutput(name, address)
            except Exception, e:
                raise Exception("Output error: can't add output for %s, %s: %s" % (name, field, e))

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
        self._output_gen.Finish()

    def Initialize(self):
        if self._output_gen is None:
            self._output_gen = og.Output(self.filename)
            if self._output_gen is None:
                raise Exception("Can't create output generator object '%s'" % self.GetName())
        if self.format is not None:
            self._output_gen.SetFormat(self.format)
        if self.mode is not None:
            if self.mode == 'steps':
                self._output_gen.SetSteps(1)
        if self.resolution is not None:
            self._output_gen.SetResolution(self.resolution)
        return

    def Reset(self):
        """!
        @brief Destroys and recreates the core output object
        """
        self._output_gen = None
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
        my_solver = solver.GetCore()
        time_step = my_solver.GetTimeStep()
        self.SetTimeStep(time_step)
        self._ParseOutputs()

    def Step(self, time=None):
        """

        """
        self._output_gen.Step(time)

    def Report(self):
        pass

    def SetMode(self, mode=None):
        """

        """
        self.mode = mode

    def SetResolution(self, res=None):
        """

        """
        self.resolution = res

    def SetFormat(self, strfmt=None):
        """

        """
        self.format = strfmt

    def SetFilename(self, filename=None):
        """
        
        """
        if not filename:
            return
        self.filename = filename

    def GetFilename(self):
        return self.filename

    def _ParseArguments(self, arguments):
        """
        @brief Parses the output initialization data

        Ignored keys:

            ['double_2_ascii']['options']['package']
            ['double_2_ascii']['module_name']
        """
        if arguments.has_key('double_2_ascii'):
            configuration = arguments['double_2_ascii']
        else:
            raise Exception("No 'double_2_ascii' configuration block present")
        output_mode = None
        resolution = None
        string_format = None
        if configuration.has_key('options'):
            options = configuration['options']
            if options.has_key('output_mode'):
                output_mode = options['output_mode']
            if options.has_key('resolution'):
                resolution = options['resolution']
            if options.has_key('format'):
                string_format = options['format']
            if options.has_key('filename'):
                self.filename = options['filename']
            else:
                self.filename = None
        self._output_gen = og.Output(self.filename)
        self.SetMode(output_mode)
        self.SetResolution(resolution)
        self.SetFormat(string_format)
        return

    def _ParseOutputs(self):
        """!

        @brief Parses the set outputs from the schedule configuration.

        Outputs can also be set via a yaml string fed to the parse method.
        """
        if self.outputs is not None:
            component_name = ''
            field = ''
            for (i, o) in enumerate(self.outputs):
                if o.has_key('outputclass'):
                    if o['outputclass'] != 'double_2_ascii':
                        continue
                if o.has_key('component_name'):
                    component_name = o['component_name']
                else:
                    print 'Output Error, no component name for output %d' % i
                    continue
                if o.has_key('field'):
                    field = o['field']
                else:
                    print 'Output Error, no field given for output %d' % i
                    continue
                if self.verbose:
                    print "\tAdding output %d, '%s' with field '%s'" % (i + 1, component_name, field)
                self.AddOutput(component_name, field)

        return