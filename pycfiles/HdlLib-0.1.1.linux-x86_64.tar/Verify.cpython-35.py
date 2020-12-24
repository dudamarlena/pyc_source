# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/HdlLib/SysGen/Verify.py
# Compiled at: 2017-07-08 08:29:58
# Size of source mod 2**32: 2434 bytes
import sys, os, logging, re
from HdlLib.SysGen import LibEditor, HDLEditor, Constraints, Module
import HdlLib.SysGen

def WrapForTest(Module):
    """
        Return a service made up of the basic block and sharing component services.
        """
    logging.debug('Wrap module for verifying')
    if Module is None:
        logging.error('[HdlLib.SysGen.Verify.WrapForTest] No Module specified. Aborted.')
        return False
    Infos = {'Name': 'DUT', 
     'Version': '', 
     'Title': 'DUT wrapper for {0} to be verified.'.format(Module.Name), 
     'Purpose': 'DEVICE UNDER TEST module.', 
     'Desc': '', 
     'Tool': '', 
     'Area': '', 
     'Speed': '', 
     'Issues': ''}
    Ports = [
     HDLEditor.Signal('Outputs', Direction='OUT', Size=96, Type='logic'),
     HDLEditor.Signal('Inputs', Direction='IN', Size=96, Type='logic'),
     HDLEditor.Signal('Clk', Direction='IN', Size=1, Type='logic')]
    DUTMod = LibEditor.NewModule(Infos=Infos, Params=[], Ports=Ports, Clocks=[], Resets=[], Sources=[])
    DUTMod.UpdateXML()
    CopyMod, CopyServ, Mapping, StimuliList, TracesList, ClocksList = Module.CopyModule(Module)
    DUTMod.IdentifyServices([CopyServ])
    SubServices = [
     CopyServ]
    Mappings = [Mapping]
    DUTMod.MapSubServices(Services=SubServices, Mappings=Mappings)
    XMLElmt = DUTMod.UpdateXML()
    DUTMod.Reload()
    DUTMod.IdentifyServices([CopyServ])
    return (
     DUTMod, StimuliList, TracesList, ClocksList)


def GetTopVerif(HwArchi):
    """
        return verif controller top module.
        """
    Library = HdlLib.SysGen.XmlLibManager.XmlLibManager(HdlLib.SysGen.BBLIBRARYPATH)
    ControlVerifServ = Library.Service('ControlVerif')
    ControlVerifServ.Alias = 'Ctrl'
    return ControlVerifServ.GetModule(Constraints=Constraints.Constraints(None, HwModel=HwArchi))