# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/HdlLib/SysGen/Service.py
# Compiled at: 2017-07-08 08:29:58
# Size of source mod 2**32: 42900 bytes
import os, sys, logging, shutil, math, collections
from lxml import etree
from HdlLib.SysGen.PackageBuilder import PackageBuilder
from HdlLib.SysGen.Signal import Signal
from HdlLib.SysGen.Condition import Condition
from HdlLib.SysGen.Interface import Interface
from HdlLib.SysGen.Module import Module
from HdlLib.SysGen import HDLEditor as HDL
from HdlLib.SysGen import LibEditor
from HdlLib.SysGen.FiniteStateMachine import FSM, FSMState
from HdlLib.SysGen.Assignment import AssignmentStatement
from HdlLib.Utilities.Misc import SyntheSysError

class Service(PackageBuilder):

    def __init__(self, XMLElmt):
        """
                Set global service definition parameters from an XML Element.
                """
        super().__init__()
        self.Name = ''
        self.Alias = ''
        self.Type = ''
        self.Version = ''
        self.Category = ''
        self.Shared = False
        self.IsCommunication = False
        self.Params = collections.OrderedDict()
        self.Vars = {}
        self.Ports = collections.OrderedDict()
        self.ModList = []
        self.Interfaces = []
        self.Wrappers = []
        self.XMLElmt = XMLElmt
        try:
            if not self.SetFromXML(XMLElmt):
                logging.error('Unable to parse service XML content.')
        except SyntheSysError:
            logging.error("Service '{0}' parsing failure.".format(self.Name))
            raise SyntheSysError

    def DumpToFile(self, OutputPath):
        """
                Write XML informations to specified file.
                """
        ServiceFilePath = os.path.join(OutputPath, 'Service_{0}.xml'.format(self.Name))
        with open(ServiceFilePath, 'wb+') as (XMLFile):
            XMLFile.write(etree.tostring(self.XMLElmt, encoding='UTF-8', pretty_print=True))
        return ServiceFilePath

    def GetXMLElmt(self):
        """
                return XML representation of Service.
                """
        return self.XMLElmt

    def Copy(self):
        """
                Return a copy of the object.
                """
        S = Service(self.XMLElmt)
        S.Alias = self.Alias
        S.ModList = self.ModList[:]
        S.Wrappers = self.Wrappers[:]
        return S

    def UpdateXML(self):
        """
                Return XML representation of attributes.
                """
        self.XMLElmt = LibEditor.ServiceXml(self)

    def SetFromXML(self, XMLElmt):
        """
                Parse XML content and extract service information.
                """
        if XMLElmt.tag != 'service':
            logging.error('XML content do not describe a service.')
            raise SyntheSysError('XML content do not describe a service.')
        self.Name = XMLElmt.attrib.get('name')
        self.Alias = self.Name + '_0'
        self.Type = XMLElmt.attrib.get('type')
        self.Version = XMLElmt.attrib.get('version')
        self.Category = XMLElmt.attrib.get('category')
        self.Shared = XMLElmt.attrib.get('shared')
        self.IsCommunication = False
        if 'communication' in XMLElmt.attrib and XMLElmt.attrib.get('communication').lower() == 'true':
            self.IsCommunication = True
        for ParamElmt in XMLElmt.iterchildren('parameter'):
            Attr = ParamElmt.attrib
            self.Vars[Attr.get('name')] = Attr.get('default')

        for ParamElmt in XMLElmt.iterchildren('parameter'):
            Attr = ParamElmt.attrib
            P = self.AddParameter(Attr.get('name'), Attr.get('type'), Attr.get('typeimport'), Attr.get('size'), Attr.get('default'))

        for InputElmt in XMLElmt.iterchildren('input'):
            Attr = InputElmt.attrib
            self.AddPort(Attr.get('name'), 'IN', Attr.get('type'), Attr.get('typeimport'), Attr.get('size'), Attr.get('default'), Attr.get('modifier'))

        for OutputElmt in XMLElmt.iterchildren('output'):
            Attr = OutputElmt.attrib
            self.AddPort(Attr.get('name'), 'OUT', Attr.get('type'), Attr.get('typeimport'), Attr.get('size'), Attr.get('default'), Attr.get('modifier'))

        del self.Interfaces[:]
        self.Interfaces = []
        for InterfaceElmt in XMLElmt.iterchildren('interface'):
            self.AddInterface(InterfaceElmt)

        for P in list(self.Ports.values()):
            if P.Modifier != None:
                if P.Modifier == '':
                    P.Modifier = None
                else:
                    P.Modifier = self.Params[P.Modifier]

        return True

    def AddParameter(self, PName, PType, PTypeImport, PSize, PDefault, IdxDict={}):
        """
                Add a parameter (defined by Name/type/TypeImport/size/default_value) to this service.
                """
        Variables = self.Vars.copy()
        Variables.update(IdxDict)
        try:
            P = Signal(Name=PName, Type=PType, PTypeImport=PTypeImport, Size=PSize, Default=PDefault, ParamVars=Variables.copy())
        except:
            logging.error("Cannot evaluate parameter '{0}' in service '{1}'.".format(PName, self.Name))
            raise SyntheSysError

        self.Params[PName] = P
        self.Params[PName].IsParam = True
        self.Vars[PName] = self.Params[PName].integers(Base=10, Variables=Variables)
        return P

    def UpdateAllValues(self, ValueDict):
        """
                Change values of each port/params and their respective "usedparam" dictionary.
                """
        for PName, PVal in ValueDict.items():
            if PName in self.Params:
                self.Params[PName].SetValue(PVal)

        for PName, PSig in self.Params.items():
            PSig.UpdateAllValues(ValueDict)

        for M in self.GetModules(Constraints=None):
            M.UpdateAllValues(ValueDict)

        for I in self.Interfaces:
            I.UpdateAllValues(ValueDict)

    def AddPort(self, PName, PDir, PType, PTypeImport, PSize, PDefault, PModifier=None, IdxDict={}):
        """
                Add a port (defined by Name/type/TypeImport/size/default_value) to this service.
                """
        Variables = self.Vars.copy()
        Variables.update(IdxDict)
        self.Ports[PName] = Signal(Name=PName, Type=PType, PTypeImport=PTypeImport, Size=PSize, Default=PDefault, Dir=PDir, Modifier=PModifier, ParamVars=Variables.copy())

    def GetPortsDict(self):
        """
                Return the dictionary of module ports.
                """
        return self.Ports.copy()

    def AddInterface(self, Itf):
        """
                Add an interface object to this service.
                """
        ServVar = {}
        for Param in list(self.Params.values()):
            ServVar[Param.Name] = Param.Default if Param.Default != '' else 0

        if isinstance(Itf, etree._Element):
            NewITF = Interface(Service=self, XMLElmt=Itf)
        else:
            if isinstance(Itf, dict):
                NewITF = Interface(Service=self, Infos=Itf)
            else:
                if isinstance(Itf, Interface):
                    NewITF = Itf.Copy()
                else:
                    logging.error("[AddInterface] Bad format '{0}' for interface '{1}'. Unable to add it to service '{2}'.".format(type(Itf), repr(Itf), self))
                    return
        NewITF.ParamVars.update(self.Vars.copy())
        self.Interfaces.append(NewITF)

    def AddWrapper(self, WrappedServ):
        """
                Add wrapper in a list for this service.
                => mean new interfaces.
                """
        self.Wrappers.append(WrappedServ)
        return True

    def AddModule(self, Mod):
        """
                Add a module implementing this service.
                """
        self.ModList.append(Mod)

    def GetModule(self, Constraints=None):
        """
                Return the best (in terms of area) module implementing this service.
                """
        Candidates = self.GetModules(Constraints=Constraints)
        if len(Candidates):
            return Candidates[0]

    def GetModules(self, Constraints=None, Task=None):
        """
                Return a module implementing this service.
                """
        if self.Name == 'clock' or self.Name == 'reset':
            Constraints = None
        if Constraints is None:
            SelectedMod = self.ModList
        else:
            SelectedMod = [M for M in self.ModList if Constraints.SatisfiedFor(Module=M)]
        if self.Name not in ('Reduce', 'clock', 'reset', 'Switch', 'Select') and Task is not None:
            NewList = []
            for M in SelectedMod:
                if M.TypeSignature == Task.TypeSignature():
                    NewList.append(M)

            if len(NewList) == 0:
                Msg = "No module matches task '{0}' type signature '{1}'".format(Task, Task.TypeSignature())
                logging.error(Msg)
                raise SyntheSysError(Msg)
            SelectedMod = NewList
        for M in SelectedMod:
            M.PropagateServDefaultParam(self)

        return SelectedMod

    def PropagateModDefaultParam(self, Mod, ModMap):
        """
                Set default value for each parameters/port from module that requires this service.
                """
        for PName, P in Mod.Params.items():
            if PName in ModMap:
                SignalName = ModMap[PName][1]
                if SignalName != PName and PName in self.Params:
                    self.Params[PName].SetValue(SignalName)
                    self.Params[PName].SetValue(SignalName)

    def GetInterfaces(self, InterfaceName=None, Direction=None):
        """
                Return the interface object corresponding to the name if present, None otherwise.
                """
        if InterfaceName is None:
            if Direction is None:
                return self.Interfaces
            for ITF in self.Interfaces:
                if ITF.Direction == Direction:
                    return [
                     ITF]

        Interfaces = []
        for ITF in self.Interfaces:
            if ITF.Name == InterfaceName:
                Interfaces.append(ITF)

        if len(Interfaces) == 0:
            for W in self.Wrappers:
                for ITF in W.Interfaces:
                    if ITF.Name == InterfaceName:
                        Interfaces.append(ITF)

        return Interfaces

    def GetOutputDataSize(self):
        """
                Return the number of bits for output data.
                """
        GetSize = lambda Sig: eval(str(Sig.Size), Sig.GetUsedParam())
        Sizes = []
        for ITF in self.Interfaces:
            if 'OUT' in ITF.Direction:
                Sizes += [GetSize(x) for x in [x for x in ITF.DataList if x.Direction == 'OUT']]

        return sum(Sizes)

    def GenInputStim(self, TaskValues, **ParamDict):
        """
                Return sequence of stimuli values corresponding to stimuli names for service interface.
                """
        InputITF = self.GetInterfaces(Direction='IN')[0]
        StimValueDict = {}
        ValueDict = {}
        AddedValues = {}
        for InputStim, Comment in InputITF.GenStim(TaskValues, **ParamDict):
            for Name, Value in InputStim.items():
                if Name in AddedValues:
                    AddedValues[Name].append(Value)
                else:
                    AddedValues[Name] = [
                     Value]

        for Name in AddedValues:
            NormalizedValues = []
            NbData = len(AddedValues[Name])
            i = 0
            Tab = AddedValues[Name]
            while i < NbData:
                if isinstance(Tab[i], list) or isinstance(Tab[i], tuple):
                    Start = i
                    while isinstance(Tab[i], list) or isinstance(Tab[i], tuple):
                        i += 1
                        if i >= NbData:
                            break

                    for Elements in zip(*Tab[Start:i]):
                        for Element in Elements:
                            NormalizedValues.append(Element)

                else:
                    NormalizedValues.append(Tab[i])
                    i += 1

            if Name in StimValueDict:
                StimValueDict[Name] += NormalizedValues
            else:
                StimValueDict[Name] = NormalizedValues

        InputITF.Protocol
        for Name, Values in StimValueDict.items():
            ValueDict[Name] = []
            for i in range(0, len(Values), InputITF.Protocol.NbSteps()):
                ValueDict[Name].append(Values[i])

        return (
         StimValueDict, ValueDict)

    def GetCompatibleItf(self, TargetItf):
        """
                Return list of interfaces that fullfill compatibility constraints with TargetItf.
                """
        if len(TargetItf.Dirs):
            if 'IN' in TargetItf.Dirs:
                for I in self.Interfaces:
                    if 'IN' in I.Dirs:
                        return [
                         I]

            else:
                for I in self.Interfaces:
                    if 'OUT' in I.Dirs:
                        return [
                         I]

        else:
            CompatibleItf = []
            for I in self.Interfaces:
                if 'IN' in I.Dirs and 'OUT' in I.Dirs:
                    return [I]
                if 'IN' in I.Dirs:
                    if 'IN' not in [x.Dirs[0] for x in CompatibleItf]:
                        CompatibleItf.append(I)
                elif 'OUT' not in [x.Dirs[0] for x in CompatibleItf]:
                    CompatibleItf.append(I)
                if len(CompatibleItf) == 2:
                    return CompatibleItf

        return []

    def GenerateWrapper(self, Mod, InterfaceList, Name, AdapterServ, ClockServ, RstServ, OutputPath=None):
        """
                Return the interface object corresponding to the name if present, None otherwise.
                """
        GeneratedAdapters = []
        AdapterServ.Alias = 'NetworkAdapter'
        AdapterMod = AdapterServ.GetModule()
        if AdapterMod != None:
            Infos = {}
            Infos['Name'] = '{0}'.format(Name)
            Infos['Version'] = ''
            Infos['Title'] = 'Wrapper for adaptation to interfaces {0}'.format(list(map(str, InterfaceList)))
            Infos['Purpose'] = 'Wrapper for adaptation to interfaces {0}'.format(list(map(str, InterfaceList)))
            Infos['Desc'] = 'Wrapper for adaptation to interfaces {0}'.format(list(map(str, InterfaceList)))
            Infos['Tool'] = 'ISE 13.1'
            Infos['Area'] = ''
            Infos['Speed'] = ''
            Infos['Issues'] = ''
            Ports = []
            for I in InterfaceList:
                Ports += I.GetSignals(Ctrl=True, Data=True, Directions=['IN', 'OUT'])

            Params = collections.OrderedDict()
            Params.update(AdapterMod.Params)
            Params.update(self.Params)
            WrappedMod = LibEditor.NewModule(Infos=Infos, Params=list(Params.values()), Ports=Ports, Clocks=[], Resets=[], Sources=[])
            WrappedMod.AddResource(Dev='ALL', RName='', Rused=0)
            Mapping = collections.OrderedDict()
            ComponentMapping = collections.OrderedDict()
            for PName, P in self.Params.items():
                if PName in ComponentMapping:
                    logging.debug("[GenerateWrapper] Parameter '{0}' already mapped: overwritten.".format(PName))
                ComponentMapping[PName] = (
                 [
                  [
                   None, PName, None]], True, {})

            for I in InterfaceList:
                for Sig, Target in I.Mapping.items():
                    Mapping[Sig] = (
                     [
                      [
                       AdapterServ.Alias, Target, None]], True, {})

            for PName, P in AdapterServ.Params.items():
                if PName in Mapping:
                    logging.debug("[GenerateWrapper] Parameter '{0}' already mapped: overwritten.".format(PName))
                Mapping[PName] = (
                 [
                  [
                   None, PName, None]], True, {})

            for P in Ports:
                if P.Name in Mapping:
                    logging.debug("[GenerateWrapper] Port '{0}' already mapped: overwritten.".format(P.Name))
                Mapping[P.Name] = (
                 [
                  [
                   None, P.Name, None]], True, {})

            for PName, P in AdapterServ.Ports.items():
                if PName in Mapping:
                    pass
                else:
                    ComponentMapping[PName] = (
                     [
                      [
                       AdapterServ.Alias, PName, None]], True, {})

            if not (ClockServ is None or RstServ is None):
                WrappedMod.IdentifyServices([ClockServ, RstServ])
            Infos = {}
            Infos['Name'] = '{0}_Service'.format(Name)
            Infos['Type'] = self.Type
            Infos['Version'] = self.Version
            Infos['Category'] = self.Category
            WrapperInterfaces = [x.Copy() for x in InterfaceList]
            WrappedService = LibEditor.ProvidedServiceXml(Mod=WrappedMod, Interfaces=WrapperInterfaces, Infos=Infos, OutputPath=OutputPath)
            for Item in WrapperInterfaces:
                Item.ServiceAlias = WrappedService
                Item.Service = WrappedService

            WrappedService.Params.update(self.Params)
            self.AddWrapper(WrappedService)
            for Item in (WrappedService, WrappedMod):
                Item.UpdateXML()

            WrappedMod.MapSubServices(Services=[AdapterServ, self], Mappings=[Mapping, ComponentMapping])
            WrappedMod.Reload()
            WrappedMod.IdentifyServices([AdapterServ, WrappedService, self])
            return (
             WrappedService, WrappedMod, AdapterMod, AdapterServ)
        else:
            return (None, None, None, None)

    def GenerateAdapter(self, AdapterName, Interfaces, ClockServ, RstServ, OutputPath='./'):
        """
                Generate a new module and service associated for 
                wrapping ITF to be compatible with this interface.
                """
        if len(Interfaces) == 0:
            logging.error('No interfaces to adapt to. Aborted.')
            return (None, None)
        StateGraphs, Ports, FSMParams, Internals, AbsoluteAssignments = self.GetProtocolStates(AdapterName, Interfaces)
        if StateGraphs is None:
            logging.error('No state graphs generated. Aborted.')
            return (None, None)
        ClkName = 'Clk'
        RstName = 'Rst'
        Clock = Signal(Name=ClkName, Type='logic', PTypeImport=None, Size=1, Default=0, Dir='IN', Modifier=None)
        Reset = Signal(Name=RstName, Type='logic', PTypeImport=None, Size=1, Default=0, Dir='IN', Modifier=None)
        Declarations, Content = ('', '')
        for StateGraph in StateGraphs:
            D, C = HDL.FSM_2Blocks(StateGraph, Name=str(StateGraph), Clock=Clock, Reset=Reset)
            Declarations += D
            Content += C
            PNGPath = StateGraph.ToPNG(OutputPath)
            logging.info("Generate PNG for adapter FSM ('{0}')".format(PNGPath))

        PortNames = [x.GetName() for x in Ports]
        for Name, Sig in Internals.items():
            if Sig.GetName() in PortNames:
                pass
            else:
                HDLSig = Sig if isinstance(Sig, HDL.Signal) else Sig.HDLFormat()
                Declarations += HDLSig.Declare()

        Content += HDL.AbsoluteAssignment(AssignmentList=AbsoluteAssignments)
        I1, I2 = '_'.join(map(str, Interfaces)), str(self)
        Infos = {}
        Infos['Name'] = AdapterName
        Infos['Version'] = 'Automatically Generated'
        Infos['Title'] = 'Adapter for {0} adaptation to interface {1}'.format(I1, I2)
        Infos['Purpose'] = 'Protocol conversion'
        Infos['Desc'] = 'Adapter that Convert {0} protocol to {1}.'.format(I1, I2)
        Infos['Tool'] = 'ISE 13.1'
        Infos['Area'] = ''
        Infos['Speed'] = ''
        Infos['Issues'] = ''
        TargetFile = os.path.join(OutputPath, AdapterName)
        logging.info("Write HDL to file '{0}'.".format(TargetFile))
        UsedParam = []
        for PName, P in Interfaces[0].GetUsedParam(GetSignals=True).items():
            UsedParam.append(P)

        Parameters = UsedParam
        ClockNames = [ClkName]
        ResetNames = [RstName]
        AdapterMod = LibEditor.NewModule(Infos=Infos, Params=Parameters + list(FSMParams.values()), Ports=Ports + [Clock, Reset], Clocks=ClockNames, Resets=ResetNames, Sources=[])
        AdapterMod.UsedParams += [x.GetName() for x in list(FSMParams.values())]
        if not os.path.isdir(OutputPath):
            os.makedirs(OutputPath)
        AdapterMod.IdentifyServices([ClockServ, RstServ])
        AdapterMod.UpdateXML()
        logging.info('Generate HDL for adapter...')
        Packages = ['IEEE.std_logic_1164', 'IEEE.std_logic_signed', 'IEEE.numeric_std']
        TargetFile = LibEditor.HDLModule(OutputPath=OutputPath, Mod=AdapterMod, Packages=Packages, Libraries=[
         'IEEE'], Declarations=Declarations, Content=Content)
        AdapterMod.Sources['RTL'].append(TargetFile)
        AdapterMod.UpdateXML()
        AdapterMod.Reload()
        AdapterMod.IdentifyServices([ClockServ, RstServ])
        ResetNames = AdapterMod.GetResetNames()
        ClockNames = AdapterMod.GetClockNames()
        ImplicitSignals = ResetNames + ClockNames
        AMap = collections.OrderedDict()
        for PName, P in AdapterMod.Ports.items():
            if PName in ImplicitSignals:
                pass
            else:
                AMap[PName] = PName

        for PName, P in AdapterMod.Params.items():
            AMap[PName] = PName

        Infos = {}
        Infos['Name'] = AdapterName
        Infos['Type'] = 'adapter'
        Infos['Version'] = self.Version
        Infos['Category'] = self.Category
        AdapterInterfaces = [x.Copy() for x in Interfaces]
        AdapterServ = LibEditor.ProvidedServiceXml(Mod=AdapterMod, Interfaces=AdapterInterfaces, Infos=Infos, OutputPath=None)
        AdapterMod.ProvidedServMap[AdapterName] = AMap
        for Item in AdapterInterfaces:
            Item.Service = AdapterServ

        AdapterMod.IdentifyServices([AdapterServ])
        return (AdapterMod, AdapterServ)

    def GetProtocolStates(self, Name, Interfaces):
        """
                Return a list of states needed to perform protocol conversion and
                a networkx graph of states.
                        self[OUT] => ITF[IN]
                        ITF[OUT]  => self[IN]
                """
        AbsoluteAssignments = []
        RegisterDict = {}
        RegisterAssignDict = {}
        MasterRegValuesDict = {}
        SlaveRegValuesDict = {}
        MasterIn, MasterOut, SlaveIn, SlaveOut = (None, None, None, None)
        logging.debug('Adaptation of interfaces: {0}'.format([str(x) for x in self.Interfaces]))
        logging.debug('---------- to interfaces  : {0}'.format([str(x) for x in Interfaces]))
        for MasterItf in Interfaces:
            IProt = MasterItf.Protocol
            if MasterItf.Direction == 'IN':
                MasterIn = IProt
            else:
                if MasterItf.Direction == 'OUT':
                    MasterOut = IProt
                elif MasterItf.Direction == 'INOUT':
                    MasterIn = IProt
                    MasterOut = IProt
            RegisterDict.update(IProt.GetRegisters())
            RegisterAssignDict.update(IProt.GetRegisterAssignments())
            MasterRegValuesDict.update(IProt.RegValues)

        for SlaveItf in self.Interfaces:
            IProt = SlaveItf.Protocol
            if SlaveItf.Direction == 'IN':
                SlaveIn = IProt
            else:
                if SlaveItf.Direction == 'OUT':
                    SlaveOut = IProt
                elif SlaveItf.Direction == 'INOUT':
                    SlaveIn = IProt
                    SlaveOut = IProt
            RegisterDict.update(IProt.GetRegisters())
            RegisterAssignDict.update(IProt.GetRegisterAssignments())
            SlaveRegValuesDict.update(IProt.RegValues)

        FSMParams = {}
        for Prot in [MasterOut, SlaveIn, MasterIn, SlaveOut]:
            if Prot is None:
                logging.error('[Protocol adaptation] No interface to adapt to. Aborted.')
                return (None, None, None, None)
            Prot.Reset()

        InputAdapterFSM, InputFSMParams, InternalDict1 = self.GenerateAdapterFSM('InputAdapter', MasterOut, SlaveIn)
        OutputAdapterFSM, OutputFSMParams, InternalDict2 = self.GenerateAdapterFSM('OutputAdapter', SlaveOut, MasterIn)
        FSMParams.update(InputFSMParams)
        FSMParams.update(OutputFSMParams)
        InternalDict = InternalDict1.copy()
        InternalDict.update(InternalDict2)
        Ports = []
        for I in self.Interfaces + Interfaces:
            SigList = [x.Copy() for x in I.GetSignals(Ctrl=True, Data=True, Directions=['IN', 'OUT'])]
            for S in SigList:
                S.InverseDirection()

            Ports += SigList
            for AssigneeName, Assignor in I.Tags.items():
                Assignee = Assignor.Copy()
                Idx = Assignor.GetIndex()
                if Idx is not None:
                    Assignee.Size = str(Idx.start) + '+1-' + str(Idx.stop)
                Assignee.SetName(AssigneeName)
                Ports.append(Assignee)
                AA = AssignmentStatement(Assignee=Assignee.HDLFormat(), Assignor=Assignor.HDLFormat(), Cond=None, Desc='Set tag of register')
                AbsoluteAssignments.append(AA)

        for P in self.Ports.values():
            if P.GetName() in [x.GetName() for x in Ports]:
                pass
            else:
                PCopy = P.Copy()
                PCopy.InverseDirection()
                Ports.append(PCopy)

        return (
         [
          InputAdapterFSM, OutputAdapterFSM], Ports, FSMParams, InternalDict, AbsoluteAssignments)

    def GenerateAdapterFSM(self, Name, Master, Slave):
        """
                Generate FSM for a Master/slave adaptation.
                Assumptions:
                        - Master has no serialization factor
                        - Slave has only one step
                        - Master has only one data signal
                """
        Master, Slave = Rearrange(Master, Slave)
        AdapterFSM = FSM('{0}_FSM'.format(Name))
        FSMParams = {}
        MasterOutCtrls = []
        SlaveOutCtrls = []
        InternalDict = {}
        for Prot in [Master, Slave]:
            for R in list(Prot.GetRegisters().values()):
                R.SetIndex(None)
                SigName = R.GetName()
                InternalDict[SigName] = R

        AssignedCtrlList = []
        for Prot in [Master, Slave]:
            for C in Prot.GetAssignedCtrl():
                AssignedCtrlList.append(C.Copy())
                HDLSig = C.HDLFormat()
                RA = AssignmentStatement(Assignee=HDLSig, Assignor=0, Cond=None, Desc='Default value')
                AdapterFSM.AddResetAssignment(RA)

        logging.debug('* Steps Master out : {0}'.format(Master._Steps))
        logging.debug('* Steps slave in   : {0}'.format(Slave._Steps))
        for Step in Master.IterSteps():
            if len(Step.GetOutputs() + Step.GetInputs()) == 0:
                logging.error("[{0}] Empty protocol step '{1}'".format(Master, Step))
                return (AdapterFSM, FSMParams, {})

        for Step in Slave.IterSteps():
            if len(Step.GetOutputs() + Step.GetInputs()) == 0:
                logging.error("[{0}] Empty protocol step '{1}'".format(Slave, Step))
                return (AdapterFSM, FSMParams, {})

        IterCnt = 0
        MasterDataSaved = False
        while Slave.HasDataToBeWritten() or Master.HasDataToBeRead():
            IterCnt += 1
            if IterCnt > 50:
                logging.error('Reach the maximum number of iterations. Stop FSM generation.')
                break
            logging.debug('-- Slave step : {0}'.format(Slave.CurrentStep()))
            for MasterStep in Master.IterSteps():
                MasterInCtrls = []
                SlaveInCtrls = []
                if not MasterDataSaved:
                    MasterStep.Reset()
                logging.debug('-- Next MasterStep : {0}'.format(MasterStep))
                EnteringCond = None
                if MasterStep.HasCtrl('OUT'):
                    MasterInCtrls = MasterStep.GetCtrl('OUT')
                    if len(MasterInCtrls):
                        if EnteringCond is None:
                            EnteringCond = Condition()
                        EnteringCond.AddANDCond(*MasterInCtrls)
                if Slave.CurrentStep().HasCtrl('OUT'):
                    SlaveInCtrls = Slave.CurrentStep().GetCtrl('OUT')
                    if len(SlaveInCtrls):
                        if EnteringCond is None:
                            EnteringCond = Condition()
                        EnteringCond.AddANDCond(*SlaveInCtrls)
                    if MasterStep.HasData('OUT'):
                        if Master.HasRegToBeRead():
                            for Data in MasterStep.GetData('OUT'):
                                Reg = Master.PopRegToBeRead()
                                logging.debug("Assign register '{0} 'to '{1}'".format(Reg.Sig, Data.Sig))
                                A = Master.AssignRegister(Data, RegAssignment=Reg)
                                if A:
                                    AdapterFSM.AddAssignment(A)
                                else:
                                    logging.error("Unable to assign master interface input register (with Data '{0}')".format(Data))

                        else:
                            if Slave.CurrentStep().HasData('IN') and Slave.HasRegToBeWritten():
                                for Data in MasterStep.GetData('OUT'):
                                    DataName = Data.GetName()
                                    if MasterDataSaved:
                                        pass
                                    else:
                                        Reg = Data.Copy()
                                        Reg.SetName(DataName + '_TEMP')
                                        InternalDict[DataName] = Reg.Sig
                                        A = Slave.AssignRegister(Data, RegAssignment=Reg)
                                        if A:
                                            AdapterFSM.AddAssignment(A)
                                            Reg.Reset()
                                            MasterStep.AddData(Reg)
                                            MasterDataSaved = True

                                for Data in Slave.CurrentStep().GetData('IN'):
                                    Reg = Slave.PopRegToBeWritten()
                                    logging.debug("Assign register '{0} 'to '{1}'".format(Reg.Sig, Data.Sig))
                                    A = Slave.AssignRegister(Data, RegAssignment=Reg)
                                    if A:
                                        AdapterFSM.AddAssignment(A)
                                    else:
                                        logging.error("Unable to assign master interface input register (with Data '{0}')".format(Data))

                            else:
                                logging.debug('Assign data.')
                                A = Slave.AssignDataFrom(MasterStep, Cond=None)
                                AdapterFSM.AddAssignment(A)
                                AdapterFSM.SetTag(Tag='LoopMarker', Anteriority=None)
                        if MasterStep.HasCtrl('IN'):
                            MasterOutCtrls += [x.GetName() for x in MasterStep.GetCtrl('IN')]
                        if Master.IsLastStep(MasterStep) and not Slave.HasDataToBeWritten() and Slave.CurrentStep().HasCtrl('IN'):
                            SlaveOutCtrls += [x.GetName() for x in Slave.CurrentStep().GetCtrl('IN')]
                        for C in AssignedCtrlList:
                            CtrlName = C.GetName()
                            if CtrlName in MasterOutCtrls:
                                SyncCond = MasterStep.GetSyncCtrl(CtrlName=CtrlName)
                                CtrlAssignments = AssignmentStatement()
                                CtrlAssignments.Add(Assignee=C.HDLFormat(), Assignor=1, Cond=SyncCond, Desc='')
                                if SyncCond:
                                    CtrlAssignments.Add(Assignee=C.HDLFormat(), Assignor=0, Cond=None, Desc='')
                                AdapterFSM.AddAssignment(CtrlAssignments, OnTransition=False)
                            else:
                                if CtrlName in SlaveOutCtrls:
                                    SyncCond = Slave.CurrentStep().GetSyncCtrl(CtrlName=CtrlName)
                                    CtrlAssignments = AssignmentStatement()
                                    CtrlAssignments.Add(Assignee=C.HDLFormat(), Assignor=1, Cond=SyncCond, Desc='')
                                    if SyncCond:
                                        CtrlAssignments.Add(Assignee=C.HDLFormat(), Assignor=0, Cond=None, Desc='')
                                    AdapterFSM.AddAssignment(CtrlAssignments, OnTransition=False)
                                else:
                                    AdapterFSM.AddAssignment(AssignmentStatement(Assignee=C.HDLFormat(), Assignor=0, Cond=None, Desc=''), OnTransition=False)

                        MasterOutCtrls = []
                        SlaveOutCtrls = []
                        if Master.IsLastStep(MasterStep) and not Slave.HasDataToBeWritten() and not Master.HasDataToBeRead():
                            break
                        else:
                            if EnteringCond is None:
                                CurrentState = AdapterFSM.AddState()
                            else:
                                CurrentState = AdapterFSM.AddState(Cond=EnteringCond)
                            CurrentState.AddInputCtrl(SlaveInCtrls + MasterInCtrls)

            if Master.HasDataToBeRead():
                Slave.CurrentStep().Reset()
                Slave.Next(Loop=True)

        while not Slave.IsLastStep(Slave.CurrentStep()):
            Slave.CurrentStep().Reset()
            Slave.Next(Loop=True)
            if Slave.CurrentStep().HasCtrl('OUT'):
                SlaveInCtrls = Slave.CurrentStep().GetCtrl('OUT')
                if len(SlaveInCtrls):
                    EnteringCond = Condition()
                    EnteringCond.AddANDCond(*SlaveInCtrls)
                if Slave.CurrentStep().HasCtrl('IN'):
                    SlaveOutCtrls = [x.GetName() for x in Slave.CurrentStep().GetCtrl('IN')]
                for C in AssignedCtrlList:
                    if C.GetName() in SlaveOutCtrls + MasterOutCtrls:
                        AdapterFSM.AddAssignment(AssignmentStatement(Assignee=C.HDLFormat(), Assignor=1, Cond=None, Desc=''), OnTransition=False)
                    else:
                        AdapterFSM.AddAssignment(AssignmentStatement(Assignee=C.HDLFormat(), Assignor=0, Cond=None, Desc=''), OnTransition=False)

                MasterOutCtrls = []
                SlaveOutCtrls = []

        AdapterFSM.CloseLoop(EnteringCond, Serialization=Master.GetSerializationFactor(), LoopStep=AdapterFSM.GetStepByTag('LoopMarker'))
        return (AdapterFSM, FSMParams, InternalDict)

    def GenerateAdapterFSM(self, Name, Master, Slave):
        """
                Generate FSM for a Master/slave adaptation.
                Assumptions:
                        - Master has no serialization factor
                        - Slave has only one step
                        - Master has only one data signal
                """
        AdapterFSM = FSM('{0}_FSM'.format(Name))
        FSMParams, InternalDict = Master.MapAsFSM(AdapterFSM, Slave)
        return (
         AdapterFSM, FSMParams, InternalDict)

    def GenSrc(self, Synthesizable=True, OutputDir='./Output', IsTop=True, HwConstraints=None, ProcessedServ={}):
        """
                Generate source files or copy sources to output directory.
                Return True if success.
                """
        if self.IsOrthogonal():
            return []
        else:
            Mod = self.GetModule(Constraints=HwConstraints)
            if Mod is None:
                logging.error("[Service '{0}'] No module implementation for this service.".format(self))
                return []
            if self.Name in ProcessedServ:
                S = ProcessedServ[self.Name]
            else:
                S = None
            return Mod.GenSrc(Synthesizable=Synthesizable, OutputDir=OutputDir, IsTop=IsTop, HwConstraints=HwConstraints, ProcessedServ=ProcessedServ, ModInstance=S)

    def IsOrthogonal(self):
        """
                return True if service is of type 'orthogonal' else False.
                """
        return self.Type == 'orthogonal'

    def CollectPkg(self):
        """
                Update package dictionary with children package.
                """
        for Child in [self.GetModule()]:
            if Child is not None:
                Child.CollectPkg()
                PackageBuilder.CollectPkg(self, Child)
                self.PkgVars.update(Child.Vars.copy())

        PortNames = list(self.Ports.keys())
        ParamNames = list(self.Ports.keys())
        for S in list(self.Ports.values()):
            self.Package['TypeImport'].update(S.GetUsedTypes())

        for S in list(self.Params.values()):
            self.Package['TypeImport'].update(S.GetUsedTypes())

    def SetParam(self, Param, Value):
        """
                Change a parameter value.
                """
        if Param in self.Params:
            self.Params[Param].Default = Value
            self.Params[Param].SetValue(Value)
            return True
        else:
            return False

    def __repr__(self):
        """
                Print service parameters to stdout.
                """
        return "\n\t\tSERVICE: name='{0}', Type='{1}', Version='{2}'\n\t\t* Parameters = {3}\n\t\t* Ports      = {4}\n\t\t* Modules that implements it = {5}\n\t\t".format(self.Name, self.Type, self.Version, list(self.Params.keys()), list(self.Ports.keys()), [x.Name for x in self.ModList])

    def Display(self):
        print(repr(self))

    def __str__(self):
        return '{0}({1})[v{2}]'.format(self.Name, self.Type, self.Version)


def Rearrange(Master, Slave):
    """
        Meld master and slave protocols.
        """
    HasSync = False
    for CName, C in Slave.CtrlDict.items():
        if C.Direction == 'OUT':
            HasSync = True

    if HasSync:
        NewMaster = Master.Copy()
        NewSlave = Slave.Copy()
        for Step in NewSlave.IterSteps():
            NewStep = Step.Copy()
            NewStep.RemoveData()
            NewMaster._Steps.append(NewStep)
            Step.RemoveCtrl()

        return (
         NewMaster, NewSlave)
    else:
        return (
         Master, Slave)