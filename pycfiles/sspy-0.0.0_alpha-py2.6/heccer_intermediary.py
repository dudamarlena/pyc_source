# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mando/neurospaces_project/sspy/source/snapshots/0/build/lib/sspy/plugins/services/heccer_intermediary/heccer_intermediary.py
# Compiled at: 2011-09-15 17:42:42
"""
This is the solver plugin for Heccer to interact with
the interface of SSPy.
"""
import os, pdb, sys
try:
    from heccer import Heccer
    from heccer import Compartment
    from heccer import Intermediary
except ImportError, e:
    sys.exit('Error importing the Heccer Python module: %s\n' % e)

class Service:

    def __init__(self, name='Untitled Heccer Intermediary', plugin=None, arguments=None, verbose=False):
        self._name = name
        self._plugin_data = plugin
        self.verbose = verbose
        self._intermediary = None
        self._method = ''
        self._ParseArguments(arguments)
        return

    def GetCore(self):
        """
        @brief Returns the constructed Heccer intermediary
        """
        return self._intermediary

    def GetName(self):
        return self._name

    def GetType(self):
        return self._plugin_data.GetName()

    def GetPluginName(self):
        return self._plugin_data.GetName()

    def GetArguments(self):
        return self._arguments

    def SetParameter(self, path, field, value):
        """!
        @brief Set's a parameter on the service
        """
        print 'Setting parameters is not avaialable on the Heccer Intermediary'

    def GetCoordinates(self):
        print 'Getting coordinates is not available on the Heccer Intermediary'
        return

    def _ParseArguments(self, arguments):
        """

        """
        method = ''
        comp2mech = []
        num_compartments = -1
        compartments = []
        if arguments.has_key('method'):
            method = arguments['method']
        if arguments.has_key('comp2mech'):
            comp2mech = arguments['comp2mech']
        if arguments.has_key('iCompartments'):
            num_compartments = arguments['iCompartments']
        if arguments.has_key('compartments'):
            compartments = self._CreateCompartmentArray(arguments['compartments'])
        self._arguments = arguments
        self._intermediary = Intermediary(compartments, comp2mech)

    def _CreateCompartmentArray(self, compartments):
        compartment_list = []
        try:
            for c in compartments:
                comp = Compartment()
                if c.has_key('dCm'):
                    comp.dCm = float(c['dCm'])
                if c.has_key('dEm'):
                    comp.dEm = c['dEm']
                if c.has_key('dInitVm'):
                    comp.dInitVm = c['dInitVm']
                if c.has_key('dRa'):
                    comp.dRa = c['dRa']
                if c.has_key('dRm'):
                    comp.dRm = float(c['dRm'])
                compartment_list.append(comp)

        except TypeError, e:
            raise Exception('Invalid arguments, cannot create Heccer Intermediary: %s', e)

        return compartment_list