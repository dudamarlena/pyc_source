# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/HdlLib/SysGen/HW/HwConstraints.py
# Compiled at: 2017-07-08 08:29:58
# Size of source mod 2**32: 20374 bytes
import os, sys, re, logging, datetime, shutil, collections, configparser
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Utilities import Timer

def GetConstraintsFromFile(ConstraintsFile):
    """
        Return dictionnary of pair Net:Pad.
        """
    if not os.path.isfile(ConstraintsFile):
        logging.error("Constraints file '{0}' isn't a regular file: parse aborted.".format(ConstraintsFile))
        return {}
    Format = ConstraintsFile.split('.')[(-1)]
    logging.debug("Constraints file type '{0}'.".format(Format))
    Constraints = {}
    with open(ConstraintsFile, 'r') as (CFile):
        Key = '?'
        for Line in CFile.readlines():
            if Format == 'ucf':
                Matched = re.match('^\\s*NET\\s*"?(?P<PadName>[a-zA-Z0-9_()<>]+)"?\\s+LOC\\s*=\\s*"?(?P<PadID>[a-zA-Z0-9_]+)"?\\s*.*\\s*;(\\s*[#]*(?P<Comment>.*))*$', Line)
            else:
                if Format == 'tcl':
                    Matched = re.match('^\\s*set_location_assignment\\s*"?(?P<PadID>[a-zA-Z0-9_]+)"?.*\\s+-to\\s*"?(?P<PadName>[a-zA-Z0-9_()\\][]+)"?.*\\s*.*$', Line)
                elif Format == 'pdc':
                    Matched = re.match('^\\s*set_io\\s*"?(?P<PadName>[\\a-zA-Z0-9_()\\][]+)"?.*\\s+\\-pinname\\s*"?(?P<PadID>[a-zA-Z0-9_]+)"?.*\\s*.*$', Line)
            if Matched:
                PadName = Matched.group('PadName')
                PadID = Matched.group('PadID')
                PadName = PadName.replace('"', '').strip()
                if '<' in PadName:
                    RootName, Index = PadName.split('<')
                    Index = Index.replace('>', '')
                    Constraints['{0}:{1}'.format(RootName, Index)] = PadID
                else:
                    if '\\[' in PadName:
                        RootName, Index = PadName.split('\\[')
                        Index = Index.replace('\\]', '')
                        Constraints['{0}:{1}'.format(RootName, Index)] = PadID
                    else:
                        if '[' in PadName:
                            RootName, Index = PadName.split('[')
                            Index = Index.replace(']', '')
                            Constraints['{0}:{1}'.format(RootName, Index)] = PadID
                        else:
                            Constraints[PadName] = PadID

    return Constraints


def GenConstraintDict(Module, FPGAInterfaceDict):
    """
        return dictionary with bit-to-pad assignments.
        """
    ConstraintsList = []
    ClockManagerDict = {}

    def GetAvailablePads(FPGAInterfaceDict, PortDirection):
        AvailablePads = FPGAInterfaceDict[PortDirection]
        if len(AvailablePads) == 0:
            AvailablePads = FPGAInterfaceDict['INOUT']
        return AvailablePads

    if 'CLOCK' not in FPGAInterfaceDict:
        logging.error('[pyInterCo.HW.HWConstraints.GenConstraintDict] Empty interface dictionary.')
        return {}
    for Signal, PadType, Parameters in Module.GetPadConstraints():
        if Parameters is None:
            pass
        else:
            if Parameters.lower() == 'ignore':
                continue
            if PadType not in FPGAInterfaceDict:
                print('FPGAInterfaceDict:', list(FPGAInterfaceDict.keys()))
                logging.error("[GenConstraintDict] No {0} pads available for signal '{1}' on this FPGA board. Ignored.".format(PadType, Signal))
                Answer = ''
                while Answer not in ('y', 'n'):
                    Answer = input('Continue ? y/n : ').lower()

                if Answer == 'y':
                    continue
                else:
                    sys.exit(1)
                AvailablePads = FPGAInterfaceDict[PadType].copy()
                if len(AvailablePads) == 0:
                    logging.error("[GenConstraintDict] No more {0} pads available for clock signal '{0}' on this FPGA board. Ignored.".format(PadType, Signal))
                    Answer = ''
                    while Answer not in ('y', 'n'):
                        Answer = input('Continue ? y/n : ').lower()

                    if Answer == 'y':
                        continue
                    else:
                        sys.exit(1)
                    while len(AvailablePads):
                        Net, PadConstraintList = AvailablePads.popitem()
                        MatchConstraint = True
                        if Parameters is not None:
                            for i, Item in enumerate(Parameters.split(',')):
                                if i > len(PadConstraintList) - 2:
                                    logging.warning("[GenConstraintDict] Signal '{0}': Ignore remaining constraint parameter from '{1}' (included).".format(Signal, Item))
                                    continue
                                    if Item != PadConstraintList[(i + 1)]:
                                        MatchConstraint = False

                        elif PadConstraintList[4] is not None:
                            MatchConstraint = False
                            continue
                        if MatchConstraint is True:
                            PadConstraintList = FPGAInterfaceDict[PadType].pop(Net)
                            Pad, IOStandard, Voltage, Freq, DiffPair = PadConstraintList
                            ConstraintsList.append({'Port': Signal, 'Name': Signal.Name, 'Direction': Signal.Direction, 'Net': Net, 'TargetPad': Pad, 'CtrlPad': None, 'Tag': Parameters, 'IOStandard': IOStandard, 'Voltage': Voltage, 'Freq': Freq, 'DiffPair': DiffPair})
                            logging.debug("Assign pad '{0} to net '{1}' of module '{2}'.".format(Pad, Signal, Module))
                            break

                    if MatchConstraint is False:
                        if PadType == 'CLOCK' and len(FPGAInterfaceDict[PadType]) != 0:
                            logging.debug("Clock '{0}' has to be driven from a clock manager".format(Signal))
                            if Parameters is not None:
                                Params = Parameters.split(',')
                                if len(Params) >= 4:
                                    TargetFrequency = Params[3]
                                else:
                                    logging.warning("No frequency target is given for clock '{0}'.".format(Signal))
                                    TargetFrequency = None
                            else:
                                logging.warning("No frequency target is given for clock '{0}'.".format(Signal))
                                TargetFrequency = None
                            Pads, Diff = PopClock(FPGAInterfaceDict[PadType])
                            ClockManagerDict[Signal] = (TargetFrequency, Diff, Pads)
                            for PadAlias, (Pad, IOStandard, Voltage, Freq, DiffPair) in Pads:
                                ConstraintsList.append({'Port': Signal.Copy(), 'Name': PadAlias, 'Direction': Signal.Direction, 'Net': PadAlias, 'TargetPad': Pad, 'CtrlPad': None, 'Tag': Parameters, 'IOStandard': IOStandard, 'Voltage': Voltage, 'Freq': Freq, 'DiffPair': DiffPair})
                                logging.debug("Assign pad '{0}' to new clock net '{1}' of module '{2}'.".format(Pad, Signal, Module))

                        else:
                            logging.error("[GenConstraintDict] No {0} pads available for signal '{0}' on this FPGA board. Ignored.".format(Type, Signal))

    return (
     ConstraintsList, ClockManagerDict)


def GenConstraintDict_AVA(Module, InterfaceDict, CtrlInterfaceDict):
    ConstraintsList = []

    def GetAvailablePads(InterfaceDict, PortDirection):
        AvailablePads = InterfaceDict[PortDirection]
        if len(AvailablePads) == 0:
            AvailablePads = InterfaceDict['INOUT']
        return AvailablePads

    if 'CLOCK' not in InterfaceDict:
        logging.error('[pyInterCo.HW.HWConstraints.GenConstraintDict] Empty interface dictionary.')
        return {}
    AvailablePads = InterfaceDict['CLOCK']
    ClockResetList = Module.GetClockNames() + Module.GetResetNames()
    for ClockReset in ClockResetList:
        if len(AvailablePads) == 0:
            logging.warning("No more clock pads available for clock signal '{0}' on this FPGA board.".format(ClockReset))
            AvailablePads = GetAvailablePads(InterfaceDict, PortDirection='IN')
        ClockResetList.remove(ClockReset)
        Tag, TargetPad = AvailablePads.popitem(last=False)
        CtrlPads = CtrlInterfaceDict['CLOCK'] if 'CLOCK' in CtrlInterfaceDict else {}
        Found = False
        for OPName, OP in Module.OrthoPorts.items():
            if OP.OrthoName() == ClockReset:
                Found = True
                logging.debug("Assign clock pad '{0}' to net '{1}'.".format(TargetPad, ClockReset))
                Sig = OP.Copy()
                Sig.Name = ClockReset
                CtrlPad = CtrlPads[Tag] if Tag in CtrlPads else None
                ConstraintsList.append({'Port': Sig, 'Name': ClockReset, 'Direction': 'CLOCK', 'Net': ClockReset, 'TargetPad': TargetPad, 'CtrlPad': CtrlPad, 'Tag': Tag})
                break

        if Found is False:
            logging.error("[GenConstraintDict] Clock or reset signal '{0}' not found in module '{1}'".format(ClockReset, Module))

    for PName, Port in Module.GetExternalPorts(CalledServ=None).items():
        if len(InterfaceDict) == 0:
            logging.error('[GenConstraintDict] No pads available for this FPGA board.')
        PortSize = Port.GetSize()
        PortDirection = Port.Direction.upper()
        CtrlPads = CtrlInterfaceDict[PortDirection] if PortDirection in CtrlInterfaceDict else {}
        if PortSize != 1:
            SubMapping = []
            AvailablePads = InterfaceDict[PortDirection]
            if len(AvailablePads) == 0:
                AvailablePads = GetAvailablePads(InterfaceDict, PortDirection=PortDirection)
                if len(AvailablePads) == 0:
                    logging.error("[GenConstraintDict] No more '{1}' or 'INOUT' pads available for signal '{0}' on this FPGA board.".format(PName, PortDirection))
                continue
                for Index in reversed(range(PortSize)):
                    if len(AvailablePads) == 0:
                        logging.error("[GenConstraintDict] No more '{1}' or 'INOUT' pads available for signal '{0}' on this FPGA board.".format(PName, PortDirection))
                        break
                    Tag, TargetPad = AvailablePads.popitem(last=False)
                    CtrlPad = CtrlPads[Tag] if Tag in CtrlPads else None
                    SubMapping.append({'Port': Port, 'Name': PName, 'Direction': PortDirection, 'Net': PName, 'TargetPad': TargetPad, 'CtrlPad': CtrlPad, 'Index': Index, 'Tag': Tag})
                    logging.debug("Assign {2} pad '{0}' to net '{1}'.".format(TargetPad, PName + '[{0}]'.format(Index), PortDirection))

                ConstraintsList.append(SubMapping)
        else:
            AvailablePads = GetAvailablePads(InterfaceDict, PortDirection=PortDirection)
            if len(AvailablePads) == 0:
                AvailablePads = InterfaceDict[PortDirection]
                if len(AvailablePads) == 0:
                    logging.error("[GenConstraintDict] No more '{1}' or 'INOUT' pads available for signal '{0}' on this FPGA board.".format(PName, PortDirection))
                continue
                Tag, TargetPad = AvailablePads.popitem(last=False)
                CtrlPad = CtrlPads[Tag] if Tag in CtrlPads else None
                ConstraintsList.append({'Port': Port, 'Name': PName, 'Direction': PortDirection, 'Net': PName, 'TargetPad': TargetPad, 'CtrlPad': CtrlPad, 'Tag': Tag})
                logging.debug("Assign {2} pad '{0}' to net '{1}'.".format(TargetPad, PName, PortDirection))

    return ConstraintsList


def GenConstraintsFile(Module, HwModel, ControlHW, Library, OutputPath):
    """
        Create constraints file according to ConstraintsList.
        ConstraintsList is build from Signals type and board constraints dictionary.
        """
    global WriteConstraintFunc
    ConstraintFormat = HwModel.Config.GetConstraintFormat()
    if ConstraintFormat not in WriteConstraintFunc:
        logging.error("Unsupported constraint format '{0}'".format(ConstraintFormat))
        return (None, None)
    ModuleWrapper = None
    logging.debug('Generate constraints for standard synthesis.')
    FPGAInterfaceDict = HwModel.GetInterface()
    if len(FPGAInterfaceDict) == 0:
        return (None, None)
    ConstraintsList, ClockManagerDict = GenConstraintDict(Module, FPGAInterfaceDict)
    ModuleWrapper, NewClockSigs = Module.WrapForClocking(HwModel, ClockManagerDict, Library)
    if ModuleWrapper is None:
        return (None, None)
    ConstFilePath = os.path.join(OutputPath, '{0}_{1}.{2}'.format(Module.Name, HwModel, ConstraintFormat))
    with open(ConstFilePath, 'w+') as (ConstFile):
        ConstFile.write("\n# Constraints for '{0}'".format(HwModel))
        ConstFile.write('\n# Automatically generated file (date: {0})\n'.format(Timer.TimeStamp()))
        NameList = []
        PadNameList = []
        for Cons in ConstraintsList:
            if isinstance(Cons, list):
                for C in Cons:
                    NameList.append(C['Name'])
                    PadNameList.append(C['TargetPad'])

            else:
                NameList.append(Cons['Name'])
                PadNameList.append(Cons['TargetPad'])

        MaxNameWidth = max([len(x) for x in NameList]) + 2 if len(NameList) > 0 else 0
        MaxPadWidth = max([len(x) for x in PadNameList]) + 2 if len(NameList) > 0 else 0
        Comments = {'CLOCK': 'CLOCK,  associated with control FGPA clock pad "{0}"', 
         'OUT': 'OUTPUT, associated with control FGPA pad "{0}"', 
         'IN': 'INPUT,  associated with control FGPA pad "{0}"', 
         'INOUT': 'INOUT,  associated with control FGPA pad "{0}"'}
        for Cons in ConstraintsList:
            if isinstance(Cons, list):
                Size = len(Cons)
                for i, CDict in enumerate(Cons):
                    Port = CDict['Port']
                    Direction = CDict['Direction']
                    WriteConstraintFunc[ConstraintFormat](ConstFile, IO=Direction, MaxNameWidth=MaxNameWidth, MaxPadWidth=MaxPadWidth, PortName=CDict['Name'], Pad=CDict['TargetPad'], IOStandard=Cons['IOStandard'], Comments=Comments[Direction].format(CDict['CtrlPad']) if CDict['CtrlPad'] else '', Index=CDict['Index'])

            else:
                Port = Cons['Port']
                Direction = Cons['Direction']
                WriteConstraintFunc[ConstraintFormat](ConstFile, IO=Direction, MaxNameWidth=MaxNameWidth, MaxPadWidth=MaxPadWidth, PortName=Cons['Name'], Pad=Cons['TargetPad'], IOStandard=Cons['IOStandard'], Comments=Comments[Direction].format(Cons['CtrlPad'] if Cons['CtrlPad'] else ''))

        ConstFile.write('\n\n')
    return (ConstFilePath, ModuleWrapper, NewClockSigs)


def XDC_AssignNet(ConstFile, IO, MaxNameWidth, MaxPadWidth, PortName, Pad, IOStandard, Comments, Index=None):
    if Index is None:
        FullPortName = '{' + PortName + '}'
    else:
        FullPortName = '{' + PortName + '[{INDEX}]'.format(INDEX=Index) + '}'
    OptionalAttr = {'CLOCK': '\ncreate_clock -period 5.0 [get_ports {PORT}]\nset_input_jitter [get_clocks -of_objects [get_ports {PORT}]] 0.05', 
     'IN': '', 
     'OUT': '', 
     'INOUT': ''}
    Line = 'set_property PACKAGE_PIN {PAD} [get_ports {PORT}]\nset_property IOSTANDARD {IOSTD} [get_ports {PORT}]\n{OPT}'.format(PORT=FullPortName, PAD=Pad, IOSTD=IOStandard, OPT=OptionalAttr[IO])
    if Pad.upper() == 'NC':
        Line = '# ' + Line
    ConstFile.write('\n' + Line)


def UCF_AssignNet(ConstFile, IO, MaxNameWidth, MaxPadWidth, PortName, Pad, IOStandard, Comments, Index=None):
    if Index is None:
        FullPortName = '"' + PortName + '"'
    else:
        FullPortName = '"' + PortName + '<{0}>"'.format(Index)
    OptionalAttr = {'CLOCK': ' | IOB = TRUE | IOSTANDARD = LVCMOS25 | CLOCK_DEDICATED_ROUTE = TRUE', 
     'OUT': ' | IOB = TRUE | IOSTANDARD = LVCMOS25', 
     'IN': ' | IOB = TRUE | IOSTANDARD = LVCMOS25', 
     'INOUT': ' | IOB = TRUE | IOSTANDARD = LVCMOS25'}
    Line = ('NET {0: <' + str(MaxNameWidth) + '} LOC = {1: <' + str(MaxPadWidth) + '}{2}; ').format(FullPortName, '"' + Pad + '"', OptionalAttr[IO]) + '# ' + Comments
    if Pad.upper() == 'NC':
        Line = '# ' + Line
    ConstFile.write('\n' + Line)


def TCL_AssignNet(ConstFile, IO, MaxNameWidth, MaxPadWidth, PortName, Pad, IOStandard, Comments, Index=None):
    if Index is None:
        FullPortName = PortName
    else:
        FullPortName = PortName + '[{0}]'.format(Index)
    OptionalAttr = {'CLOCK': '', 
     'OUT': '', 
     'IN': '', 
     'INOUT': ''}
    Line = ('set_location_assignment {0: <' + str(MaxPadWidth - 2) + '} -to {1: <' + str(MaxNameWidth - 2) + '}{2} ').format(Pad, FullPortName, OptionalAttr[IO])
    if Pad.upper() == 'NC':
        Line = '# ' + Line
    ConstFile.write('\n#' + Comments)
    ConstFile.write('\n' + Line)


def PDC_AssignNet(ConstFile, IO, MaxNameWidth, MaxPadWidth, PortName, Pad, IOStandard, Comments, Index=None):
    if Index is None:
        FullPortName = '"' + PortName + '"'
    else:
        FullPortName = '"' + PortName + '\\[' + str(Index) + '\\]"'
    OptionalAttr = {'CLOCK': '', 
     'OUT': '', 
     'IN': '', 
     'INOUT': ''}
    Line = ('set_io {0: <' + str(MaxNameWidth + 2) + '}  -pinname {1: <' + str(MaxPadWidth) + '}{2}').format(FullPortName, '"' + Pad + '"', OptionalAttr[IO])
    if Pad.upper() == 'NC':
        Line = '# ' + Line
    ConstFile.write('\n' + Line)


def PopClock(AvailablePads):
    """
        Get single ended or differential pair clock from dict of pads.
        """
    if len(AvailablePads) != 0:
        Net, ConstraintList = AvailablePads.popitem()
        Pad, IOStandard, Voltage, Freq, DiffPair = ConstraintList
        if DiffPair:
            OtherNet, OtherConstraintList = GetDiffPair(AvailablePads, DiffPair)
            return (
             [
              (
               Net, ConstraintList), (OtherNet, OtherConstraintList)], True)
        return (
         [
          (
           Net, ConstraintList)], False)
    raise TypeError('[PopClock] Empty dictionary given !!!!')


def GetDiffPair(AvailablePads, DiffPair):
    """
        Get the other net forming a differential pair.
        """
    for OtherNet, ConstraintList in AvailablePads.items():
        if ConstraintList[4] == DiffPair:
            break

    OtherConstraintList = AvailablePads.pop(OtherNet)
    return (OtherNet, OtherConstraintList)


WriteConstraintFunc = {'ucf': UCF_AssignNet, 
 'tcl': TCL_AssignNet, 
 'pdc': PDC_AssignNet, 
 'xdc': XDC_AssignNet}
if __name__ == '__main__':
    logging.critical("No test bench for the module '{0}'.".format(__file__))