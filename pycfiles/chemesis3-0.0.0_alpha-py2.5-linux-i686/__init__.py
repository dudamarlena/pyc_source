# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/chemesis3/__init__.py
# Compiled at: 2011-09-09 23:43:12
"""!
@package chemesis3 Kinetic reaction and biochemical reaction pathways for G3.

"""
import os, pdb, sys
try:
    import chemesis3_base
except ImportError, e:
    sys.exit('Could not import compiled SWIG chemesis3 library: %s' % e)

import __cbi__
from components import SimObjChemesis3
AVOGADRO = chemesis3_base.AVOGADRO
RK_INT = chemesis3_base.RK_INT
TRAPEZOIDAL_INT = chemesis3_base.TRAPEZOIDAL_INT
GEAR_INT = chemesis3_base.GEAR_INT
EPC_INT = chemesis3_base.EPC_INT
FEULER_INT = chemesis3_base.FEULER_INT
EEULER_INT = chemesis3_base.EEULER_INT
AB2_INT = chemesis3_base.AB2_INT
AB3_INT = chemesis3_base.AB3_INT
AB4_INT = chemesis3_base.AB4_INT
AB5_INT = chemesis3_base.AB5_INT
BEULER_INT = chemesis3_base.BEULER_INT
CRANK_INT = chemesis3_base.CRANK_INT
CHEMESIS3_STATUS_PHASE_0 = chemesis3_base.CHEMESIS3_STATUS_PHASE_0
CHEMESIS3_STATUS_PHASE_1 = chemesis3_base.CHEMESIS3_STATUS_PHASE_1
CHEMESIS3_STATUS_PHASE_2 = chemesis3_base.CHEMESIS3_STATUS_PHASE_2
CHEMESIS3_STATUS_PHASE_3 = chemesis3_base.CHEMESIS3_STATUS_PHASE_3
CHEMESIS3_STATUS_PHASE_4 = chemesis3_base.CHEMESIS3_STATUS_PHASE_4
CHEMESIS3_STATUS_PHASE_5 = chemesis3_base.CHEMESIS3_STATUS_PHASE_5

class Chemesis3Error(Exception):
    pass


class Chemesis3:

    def __init__(self, name='Untitled Chemesis3', model=None, intermediary=None, event_distributor=None, event_querer=None):
        """!

        """
        self.name = name
        self.time_step = None
        self._chemesis3_core = SimObjChemesis3(self.name)
        if self._chemesis3_core is None:
            raise Chemesis3Error('Could not create a low level Chemesis 3 object')
        self._model_source = None
        self._is_constructed = False
        self._compiled_p1 = False
        self._compiled_p2 = False
        self._compiled_p3 = False
        if model is not None:
            self._model_source = model
        return

    def Initiate(self):
        if self._chemesis3_core is not None:
            chemesis3_base.Chemesis3Initiate(self._chemesis3_core)
        else:
            raise Chemesis3Error("Can't initiate, no Chemesis3 object allocated")
        return

    def GetCore(self):
        return self._chemesis3_core

    def SetCore(self, chem3):
        self._chemesis3_core = chem3

    def Construct(self, model=None):
        if self._chemesis3_core is None:
            raise Chemesis3Error("Can't construct Chemesis3, no object was created.")
        elif self._model_source is None:
            if model is None:
                raise Chemesis3Error("Can't construct Chemesis3, no model container present")
            else:
                self._model_source = model
        result = chemesis3_base.Chemesis3Construct(self._chemesis3_core, self._model_source.GetCore(), self._chemesis3_core.pcName, None, None)
        if result == 0:
            raise Chemesis3Error("Can't compile chemesis3 '%s'" % self._chemesis3_core.pcName)
        self._is_constructed = True
        return

    def Compile(self):
        """!
        @brief 
        """
        if self._chemesis3_core is None:
            raise Chemesis3Error("Can't compile, no Chemesis3 object has been allocated")
        if not self._is_constructed:
            self.Construct()
        self.CompileP1()
        self.CompileP2()
        self.CompileP3()
        self.Initiate()
        if self.time_step is None:
            self.time_step = self._chemesis3_core.dStep
        return

    def CompileP1(self):
        """!
        @brief 
        """
        if self._chemesis3_core is None:
            raise Chemesis3Error("Can't compile (P1), no Chemesis3 object has been allocated")
        if self._chemesis3_core.iStatus < CHEMESIS3_STATUS_PHASE_1:
            result = chemesis3_base.Chemesis3CompileP1(self._chemesis3_core)
            if result == 1:
                self._compiled_p1 = True
            else:
                raise Chemesis3Error('There was a problem compiling Chemesis3 (P1).')
        else:
            self._compiled_p1 = False
        return

    def CompileP2(self):
        self._compiled_p2 = True

    def CompileP3(self):
        self._compiled_p3 = True

    def GetName(self):
        return self.name

    def GetTimeStep(self):
        if self._chemesis3_core is None:
            return self.time_step
        else:
            return self._chemesis3_core.dStep
        return

    def SetTimeStep(self, time_step):
        if self._chemesis3_core is None:
            self.time_step = time_step
        else:
            self._chemesis3_core.dStep = time_step
        return

    def Step(self, time=0.0):
        if self._chemesis3_core is not None:
            return chemesis3_base.Chemesis3Advance(self._chemesis3_core, time)
        else:
            raise Chemesis3Error("Can't step, no Chemesis3 object has been allocated")
        return

    def GetAddress(self, path, field='concentration'):
        """!

        """
        address = None
        if self._chemesis3_core is None:
            raise Chemesis3Error("Can't look up address for %s, %s. No Chemesis3 is allocated" % (path, field))
        elif self._model_source is None:
            raise Chemesis3Error("Can't look up address for %s, %s. No model container present" % (path, field))
        else:
            serial = self._model_source.GetSerial(path)
            address = chemesis3_base.Chemesis3AddressVariable(self._chemesis3_core, serial, field)
        return address

    def Finish(self):
        pass