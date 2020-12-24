# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/instrumentino/controllers/labsmith_eib/labsmith_comps.py
# Compiled at: 2015-11-23 10:12:58
from __future__ import division
from instrumentino.controllers.labsmith_eib import SysCompLabSmith, SysVarDigitalLabSmith_SyringeSpeed, SysVarDigitalLabSmith_SyringePower, SysVarDigitalLabSmith_SyringeMaxVolume, SysVarDigitalLabSmith_SyringePlunger, LabSmithEIB, SysVarDigitalLabSmith_SyringeFlowrate
from ctypes import *
from threading import Semaphore, Thread
__author__ = 'yoelk'
from instrumentino import cfg
import wx, time
from instrumentino.comp import SysVarDigital, SysComp

class LabSmithSensors4AM01(SysCompLabSmith):

    def __init__(self, name, analVars):
        SysCompLabSmith.__init__(self, name, analVars, 'sensors')
        for var in analVars:
            var.SetManifold(self)

    def getSensor(self, port):
        return self.GetController().GetSensorValue(port)


class LabSmithValves4VM01(SysCompLabSmith):

    def __init__(self, name, digiVars):
        SysCompLabSmith.__init__(self, name, digiVars, 'open/close valves')
        for var in digiVars:
            var.SetController(self)

    def setValve(self, port, state):
        if port == 1:
            self.GetController().SetValves(valve1=state)
        if port == 2:
            self.GetController().SetValves(valve2=state)
        if port == 3:
            self.GetController().SetValves(valve3=state)
        if port == 4:
            self.GetController().SetValves(valve4=state)

    def getValve(self, port):
        valves = self.GetController().GetValves()
        return valves[(port - 1)]


class LabSmithSPS01SyringePump(SysCompLabSmith):
    """
    A LabSmith SPS01 syringe pump
    """
    syringeVolumeMicroLitToDiameterMiliMeter = {100: 3.256, 50: 2.304, 
       20: 1.458, 
       10: 1.031, 
       5: 0.729}
    syringeVolumeMicroLitToFlowrateRange = {100: [1, 5600], 20: [
          0.2, 1100], 
       5: [
         0.05, 280]}

    def __init__(self, name, volumeMicroLit, address, helpline='', defaultSpeedPercent=50, defaultPowerPercent=75):
        self.address = address
        self.defaultSpeedPercent = defaultSpeedPercent
        self.defaultPowerPercent = defaultPowerPercent
        self.diameterMiliMeter = self.syringeVolumeMicroLitToDiameterMiliMeter[volumeMicroLit]
        self.volume = SysVarDigitalLabSmith_SyringeMaxVolume(name, self)
        self.plunger = SysVarDigitalLabSmith_SyringePlunger(name, self)
        self.speed = SysVarDigitalLabSmith_SyringeSpeed(name, self)
        self.flowrate = SysVarDigitalLabSmith_SyringeFlowrate(name, self, range=self.syringeVolumeMicroLitToFlowrateRange[volumeMicroLit])
        self.power = SysVarDigitalLabSmith_SyringePower(name, self)
        SysCompLabSmith.__init__(self, name, (self.volume, self.plunger, self.speed, self.flowrate, self.power), 'move syringe pump')

    def FirstTimeOnline(self):
        maxVolume = self.GetMaxVolume()
        self.volume.SetMaxVolume(maxVolume)
        self.plunger.SetMaxVolume(maxVolume)
        self.speed.Set(self.defaultSpeedPercent)
        self.power.Set(self.defaultPowerPercent)
        self.plunger.Set(5)

    def SetPressure(self, sensorPort, PressureRangeKiloPascals, regChannel=LabSmithEIB.REG_CHANNEL_A):
        eib = self.GetController()
        eib.accessSemaphore.acquire(True)
        eib.DLL.AssignSensorToChannelRegulation(eib.sensors, c_int(sensorPort), c_int(regChannel), c_double(PressureRangeKiloPascals[0]), c_double(PressureRangeKiloPascals[1]))
        eib.DLL.MoveSyringeAccordingToChannel(eib.syringePumps[self.address], c_int(regChannel))
        eib.accessSemaphore.release()

    def StopPressure(self, sensorPort):
        eib = self.GetController()
        eib.accessSemaphore.acquire(True)
        eib.DLL.StopSyringe(eib.syringePumps[self.address])
        eib.DLL.CancelSensorChannelRegulation(eib.sensors, c_int(sensorPort))
        eib.accessSemaphore.release()

    def SetSyringePower(self, percent):
        eib = self.GetController()
        eib.accessSemaphore.acquire(True)
        eib.DLL.SetSyringePower(eib.syringePumps[self.address], c_int(int(percent / 100 * LabSmithEIB.SYRINGE_PUMP_MAX_POWER)))
        eib.accessSemaphore.release()

    def SetSyringeSpeed(self, percent):
        eib = self.GetController()
        eib.accessSemaphore.acquire(True)
        eib.DLL.SetSyringeSpeedPercent(eib.syringePumps[self.address], c_double(percent))
        eib.accessSemaphore.release()

    def SetSyringeFlowrate(self, flowrate_uL_per_min):
        eib = self.GetController()
        eib.accessSemaphore.acquire(True)
        eib.DLL.SetSyringeFlowrate(eib.syringePumps[self.address], c_double(flowrate_uL_per_min))
        eib.accessSemaphore.release()

    def GetMaxVolume(self):
        eib = self.GetController()
        eib.accessSemaphore.acquire(True)
        eib.DLL.GetSyringeMaxVolume.restype = c_double
        max_volume = eib.DLL.GetSyringeMaxVolume(eib.syringePumps[self.address])
        eib.accessSemaphore.release()
        return max_volume

    def MoveSyringeToPosition(self, pos):
        eib = self.GetController()
        thread = Thread(target=eib.DLL.MoveSyringeToPosition, args=(eib.syringePumps[self.address], c_int(pos)))
        thread.start()
        while thread.isAlive():
            if cfg.userStopped:
                self.StopSyringe()

        thread.join()

    def MoveSyringeToVolumePercent(self, percent, maxVolume):
        eib = self.GetController()
        thread = Thread(target=eib.DLL.MoveSyringeToVolume, args=(eib.syringePumps[self.address], c_double(percent / 100 * maxVolume)))
        thread.start()
        while thread.isAlive():
            if cfg.userStopped:
                self.StopSyringe()

        thread.join()

    def MoveSyringeToVolume(self, volume):
        eib = self.GetController()
        thread = Thread(target=eib.DLL.MoveSyringeToVolume, args=(eib.syringePumps[self.address], c_double(volume)))
        thread.start()
        while thread.isAlive():
            if cfg.userStopped:
                self.StopSyringe()

        thread.join()

    def StopSyringe(self):
        eib = self.GetController()
        eib.accessSemaphore.acquire(True)
        eib.DLL.StopSyringe(eib.syringePumps[self.address])
        eib.accessSemaphore.release()