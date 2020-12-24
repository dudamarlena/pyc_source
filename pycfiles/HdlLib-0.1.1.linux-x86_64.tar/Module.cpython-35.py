# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/HdlLib/SysGen/Module.py
# Compiled at: 2017-07-08 08:29:58
# Size of source mod 2**32: 107864 bytes
import os, sys, logging, shutil, re, math, random, glob
from lxml import etree
import collections
from HdlLib.SysGen.PackageBuilder import PackageBuilder
from HdlLib.SysGen.Signal import Signal, SigName
from HdlLib.SysGen.Condition import Condition
from HdlLib.SysGen import HDLEditor as HDL
from HdlLib.SysGen import LibEditor
from functools import reduce
from HdlLib.SysGen.HW.HwResources import HwResources
from HdlLib.Utilities.Misc import ReplaceTextInFile, SyntheSysError

class Instance:

    def __init__(self, Name, Mod):
        """
                Module instance that gather information during design generation.
                """
        self.Name = Name
        self.Mod = Mod
        self.Instances = []
        if self.Mod:
            self.Mod.LastCreatedInstance = self

    def AddInstance(self, Name, Mod):
        """
                Create instance and add it to instance list.
                """
        I = Instance(Name=Name, Mod=Mod)
        self.Instances.append(I)
        return I

    def AddInstanceAsInstance(self, Inst):
        """
                Add existing instance it to instance list.
                """
        self.Instances.append(Inst)
        return Inst

    def WalkInstances(self, Path=[], Max=9999999, Depth=999999):
        """
                Yield sub instances recursively.
                """
        if Depth > 0:
            Cnt = 1
            yield (self, Path)
            for Inst in self.Instances:
                for I, P in Inst.WalkInstances(Path=Path + [self.Name], Max=Max, Depth=Depth - 1):
                    if Cnt > Max:
                        break
                    yield (
                     I, P)
                    Cnt += 1

    def Copy(self):
        """
                Create instance and add it to instance list.
                """
        ICopy = Instance(Name=self.Name, Mod=self.Mod)
        ICopy.Instances = self.Instances[:]
        return ICopy

    def GetPathName(self, InstanceName):
        """
                Return Path name of this instance from top module.
                """
        for Inst, Path in self.WalkInstances():
            if Inst.Mod is None:
                pass
            elif Inst.Name == InstanceName:
                return '/'.join(Path[1:] + [Inst.Name])

        logging.error("[GetPathName] Instance name '{0}' not found from instance '{1}'".format(InstanceName, self))

    def GatherConstraintSources(self, FromInst=None):
        """
                return the constraints source file list of the module.
                """
        CList = []
        for Inst in reversed(self.Instances):
            ConstrSources = Inst.Mod.GetConstraintSources()
            if len(ConstrSources) == 0:
                if self.Name == FromInst:
                    CList += Inst.GatherConstraintSources(FromInst=None)
                else:
                    CList += Inst.GatherConstraintSources(FromInst=FromInst)
                    continue
                    PN = self.Mod.LastCreatedInstance.GetPathName(InstanceName=Inst.Name)
                    if PN is None:
                        sys.exit(1)
                    if FromInst is None:
                        PN = '/'.join([self.Name, PN])
                    PatternDict = {'INSTANCE_PATH_NAME': PN}
                    for SrcPath in ConstrSources:
                        for VarName, VarValue in PatternDict.items():
                            ReplaceTextInFile(FileName=SrcPath, OldText='${0}'.format(VarName), NewText='{0}'.format(VarValue))

                        CList.append(SrcPath)

        return CList

    def DisplayTree(self):
        """
                Return instance name.
                """
        for Inst, Path in self.WalkInstances():
            print('-->'.join(Path) + '-->' + Inst.Name)

    def __str__(self):
        """
                Return instance name.
                """
        return self.Name


class Module(PackageBuilder):
    Instances = []

    def __init__(self, XMLElmt, FilePath=None):
        """
                Set global Module definition parameters.
                """
        Module.Instances.append(self)
        PackageBuilder.__init__(self)
        self.Name = ''
        self.Version = ''
        self.Title = ''
        self.Purpose = ''
        self.Desc = ''
        self.Issues = ''
        self.Speed = ''
        self.Area = ''
        self.Tool = ''
        self.Latency = None
        self.MaxFreq = {}
        self.DataIntroductionInterval = 1
        self.Params = collections.OrderedDict()
        self.Const = collections.OrderedDict()
        self.Ports = collections.OrderedDict()
        self.OrthoPorts = collections.OrderedDict()
        self.Sources = {'RTL': [], 'Behavioral': [], 'Constraints': []}
        self.Dependencies = {'package': collections.OrderedDict((('IEEE.std_logic_1164', None), )), 
         'library': collections.OrderedDict((('IEEE', None), ))}
        self.Resources = {}
        self.Latency = None
        self.ReqServ = collections.OrderedDict()
        self.ServAlias = collections.OrderedDict()
        self.ProvidedServMap = collections.OrderedDict()
        self.ProvidedServ = collections.OrderedDict()
        self.IO = []
        self.Vars = {}
        self.XmlFilePath = FilePath
        self.UsedParams = []
        self.XMLElmt = XMLElmt
        self.AbstractModule = True
        self.TBEntity = None
        self.TBSource = None
        self.TBDependencies = []
        self.NoOrthoPorts = False
        self.LastCreatedInstance = None
        if XMLElmt is None:
            pass
        elif not self.SetFromXML(XMLElmt):
            logging.error('Unable to parse module XML content.')

    def Copy(self):
        """
                return New instance of module class.
                """
        M = Module(XMLElmt=None)
        M.Name = self.Name
        M.Version = self.Version
        M.Title = self.Title
        M.Purpose = self.Purpose
        M.Desc = self.Desc
        M.Issues = self.Issues
        M.Speed = self.Speed
        M.Area = self.Area
        M.Tool = self.Tool
        M.Latency = self.Latency
        M.MaxFreq = self.MaxFreq
        M.DataIntroductionInterval = self.DataIntroductionInterval
        M.Params = self.Params
        M.Const = self.Const
        M.Ports = self.Ports
        M.OrthoPorts = self.OrthoPorts
        M.Sources = self.Sources
        M.Dependencies = self.Dependencies
        M.Resources = self.Resources
        M.Latency = self.Latency
        M.ReqServ = self.ReqServ
        M.ServAlias = self.ServAlias
        M.ProvidedServMap = self.ProvidedServMap
        M.ProvidedServ = self.ProvidedServ
        M.IO = self.IO
        M.Vars = self.Vars
        M.XmlFilePath = self.XmlFilePath
        M.UsedParams = self.UsedParams
        M.XMLElmt = self.XMLElmt
        M.AbstractModule = self.AbstractModule
        M.TBEntity = self.TBEntity
        M.TBSource = self.TBSource
        M.TBDependencies = self.TBDependencies
        return M

    def GetTestBenchInfo(self):
        """
                return testbench entity name, top source and a list of dependency files.
                """
        return (
         self.TBEntity, self.TBSource, self.TBDependencies)

    def UpdateXML(self):
        """
                Return XML representation of attributes.
                """
        self.XMLElmt = LibEditor.ModuleXml(self)
        return self.XMLElmt

    def GetXMLElmt(self):
        """
                return XML representation of Service.
                """
        return self.XMLElmt

    def DumpToFile(self, OutputPath):
        """
                Write XML informations to specified file.
                """
        ModuleFilePath = os.path.join(OutputPath, 'Module_{0}.xml'.format(self.Name))
        if os.path.isfile(ModuleFilePath):
            Answer = ''
            while Answer not in ('y', 'n'):
                Answer = input("Found existing file '{0}' overwrite ?".format(ModuleFilePath))

            if Answer == 'n':
                logging.warning('XML generation aborted by user.')
                return
        logging.debug("Generate '{0}'.".format(ModuleFilePath))
        self.UpdateXML()
        with open(ModuleFilePath, 'wb+') as (XMLFile):
            XMLFile.write(etree.tostring(self.XMLElmt, encoding='UTF-8', pretty_print=True))
        self.XmlFilePath = ModuleFilePath
        return self.XmlFilePath

    def DisplayXML(self):
        """
                Print to std out xml content.
                """
        print(etree.tostring(self.XMLElmt, encoding='UTF-8', pretty_print=True).decode('utf-8'))

    def DumpToLibrary(self):
        """
                Write XML informations to library xml file.
                """
        logging.debug("Re-write '{0}'.".format(self.XmlFilePath))
        with open(self.XmlFilePath, 'wb+') as (XMLFile):
            XMLFile.write(etree.tostring(self.XMLElmt, encoding='UTF-8', pretty_print=True))
        return self.XmlFilePath

    def GetLastCreatedInstance(self):
        """
                Si a une instance retoune la dernière. Sinon en crée une.
                """
        if self.LastCreatedInstance is None:
            return Instance(Name=self.Name + '_0', Mod=self)
        else:
            return self.LastCreatedInstance

    def EditParam(self, PName, PVal):
        """
                Parse XML content and extract module information.
                """
        Param = self.Params[PName]
        Param.Default = PVal
        Param.Value = PVal
        for ParamElmt in self.XMLElmt.iterchildren('parameter'):
            if ParamElmt.get('name') == PName:
                ParamElmt.attrib['default'] = str(PVal)

    def Reload(self):
        """
                RE-Parse XML content and extract module information.
                """
        self.ReqServ = collections.OrderedDict()
        self.SetFromXML(self.XMLElmt)

    def SetFromXML(self, XMLElmt):
        """
                Parse XML content and extract module information.
                """
        PythonTypes = {'float': float, 
         'integer': int, 
         'fixed': int}
        self.Name = XMLElmt.attrib.get('name')
        self.Version = XMLElmt.attrib.get('version')
        self.Title = XMLElmt.attrib.get('title')
        self.Purpose = XMLElmt.attrib.get('purpose')
        self.Desc = XMLElmt.attrib.get('description')
        self.Issues = XMLElmt.attrib.get('issues')
        self.Speed = XMLElmt.attrib.get('speed')
        self.Area = XMLElmt.attrib.get('area')
        self.Tool = XMLElmt.attrib.get('tool')
        TS = XMLElmt.attrib.get('typesignature')
        if TS is None:
            self.TypeSignature = tuple()
        else:
            self.TypeSignature = tuple([PythonTypes[T] for T in TS.split()])
        ParamDict = collections.OrderedDict()
        for ParamElmt in XMLElmt.iterchildren('parameter'):
            Attr = ParamElmt.attrib
            try:
                Val = int(Attr.get('default'))
            except:
                Val = Attr.get('default')

            ParamDict[Attr.get('name').replace('.', '_')] = Val

        for ParamElmt in XMLElmt.iterchildren('parameter'):
            self.AddParameter(ParamElmt, VarDict=ParamDict)

        for InputElmt in XMLElmt.iterchildren('input'):
            Attr = InputElmt.attrib
            self.AddPort(PName=Attr.get('name'), PDir='IN', PType=Attr.get('type'), PTypeImport=Attr.get('typeimport'), PSize=Attr.get('size'), PDefault=Attr.get('default'))

        for OutputElmt in XMLElmt.iterchildren('output'):
            Attr = OutputElmt.attrib
            self.AddPort(PName=Attr.get('name'), PDir='OUT', PType=Attr.get('type'), PTypeImport=Attr.get('typeimport'), PSize=Attr.get('size'), PDefault=Attr.get('default'))

        for CoreElmt in XMLElmt.iterchildren('core'):
            for BehavElmt in CoreElmt.iter('behavioral'):
                self.AddSource(None, None, BehavElmt.attrib.get('path'), Synthesizable=False)

            for RTLElmt in CoreElmt.iter('rtl'):
                RTLType = RTLElmt.attrib.get('type')
                RTLName = RTLElmt.attrib.get('name')
                RTLPath = RTLElmt.attrib.get('path')
                self.AddSource(RTLType, RTLName, RTLPath, Synthesizable=True)

            for ConstraintsElmt in CoreElmt.iter('constraints'):
                ConstraintsType = ConstraintsElmt.attrib.get('type')
                ConstraintsName = ConstraintsElmt.attrib.get('name')
                ConstraintsPath = ConstraintsElmt.attrib.get('path')
                self.AddConstraintSource(ConstraintsType, ConstraintsName, ConstraintsPath)

        for FeatureElmt in XMLElmt.iterchildren('features'):
            for DesignElmt in FeatureElmt.iterchildren('design'):
                try:
                    Latency = int(DesignElmt.get('Latency'))
                    self.Latency = Latency
                except:
                    logging.warning("Attribute 'Latency' of 'design' element (line '{0}') cannot be interpreted as an integer. Ignored.".format(DesignElmt.sourceline))

                try:
                    DII = int(DesignElmt.get('DataIntroductionInterval'))
                    self.DataIntroductionInterval = DII
                except:
                    logging.warning("Attribute 'DataIntroductionInterval' of 'design' element (line '{0}') cannot be interpreted as an integer. Ignored.".format(DesignElmt.sourceline))

            for FPGAElmt in FeatureElmt.iterchildren('fpga'):
                FPGA = FPGAElmt.attrib.get('id').upper()
                for RscElmt in FPGAElmt.iterchildren('resources'):
                    Attr = RscElmt.attrib
                    for RName, Rused in Attr.items():
                        self.AddResource(FPGA, RName.upper(), Rused)

                for ClockElmt in FPGAElmt.iterchildren('clock'):
                    try:
                        MaxFreq = int(ClockElmt.attrib.get('MaxFreq'))
                    except:
                        logging.warning("Attribute 'MaxFreq' of 'clock' element (line '{0}') cannot be interpreted as an integer. Ignored.".format(ClockElmt.sourceline))
                        continue

                    self.MaxFreq[FPGA] = MaxFreq

        for ServElmt in XMLElmt.iterchildren('services'):
            for ReqElmt in ServElmt.iter('required'):
                ReqMapping = collections.OrderedDict()
                ReqName = ReqElmt.get('name')
                ReqID = ReqName.split(':')
                if len(ReqID) > 1:
                    RVars = ReqID[1:]
                else:
                    RVars = []
                for MapElmt in ReqElmt.iter('map'):
                    VDict = self.Vars.copy()
                    if MapElmt.get('formal'):
                        Formal = MapElmt.get('formal')
                        ActualList = SigName(MapElmt.get('actual'), RVars, VDict)
                        if MapElmt.get('when') is None:
                            Cond = True
                        else:
                            Cond = Condition(eval(str(MapElmt.get('when')), VDict))
                        ReqMapping[Formal] = [
                         ActualList, Cond, {}]
                    else:
                        self.IO.append(MapElmt.get('actual'))

                for V in RVars:
                    V = eval(V, VDict)

                Alias = ReqElmt.get('alias')
                if not Alias:
                    Alias = ReqName
                self.AddReqServ(ReqID[0], ReqElmt.attrib.get('type'), ReqElmt.attrib.get('version'), ReqMapping, UniqueName=ServName(Alias))

            for OffElmt in ServElmt.iterchildren('offered'):
                OffMapping = collections.OrderedDict()
                for MapElmt in OffElmt.iter('map'):
                    OffMapping[MapElmt.get('formal')] = MapElmt.get('actual')

                self.AddProvServ(OffElmt.attrib.get('name'), OffElmt.attrib.get('alias'), OffMapping)

        for LoopElmt in XMLElmt.iterchildren('loop'):
            self.ParseLoops(LoopElmt)

        if len(self.Sources['RTL']) > 0:
            self.AbstractModule = False
        return True

    def ParseLoops(self, LoopElmt, Indexes=[], IdxDict={}):
        """
                Parse each service requirement in XML loop element.
                """
        Var, InitVal, LastVal = self.ParseIndex(LoopElmt.get('index'))
        if Var:
            if not Indexes.count(Var):
                Indexes.append(Var)
            for Index in range(InitVal, LastVal + 1):
                LocalParams = {}
                IdxDict[Var] = Index
                SigVars = self.Vars.copy()
                for ParamElmt in LoopElmt.iterchildren('parameter'):
                    Attr = ParamElmt.attrib
                    BaseName = Attr.get('name')
                    CName = BaseName + '_' + ''.join([x + str(IdxDict[x]) for x in Indexes])
                    CType = Attr.get('type')
                    CTypeImport = Attr.get('typeimport')
                    CSize = Attr.get('size')
                    CDefault = Attr.get('default')
                    SigVars.update(IdxDict)
                    Constant = Signal(CName, CType, CTypeImport, CSize, CDefault, ParamVars=SigVars.copy()).HDLFormat(SigVars.copy())
                    if not list(self.Const.keys()).count(BaseName):
                        self.Const[BaseName] = {}
                    self.Const[BaseName][CName] = Constant
                    LocalParams[BaseName] = CName

                for ServElmt in LoopElmt.iterchildren('services'):
                    for ReqElmt in ServElmt.iter('required'):
                        ReqName = ReqElmt.get('name')
                        ReqID = ReqName.split(':')
                        if len(ReqID) > 1:
                            RVars = ReqID[1:]
                        else:
                            RVars = []
                        ReqMapping = collections.OrderedDict()
                        for MapElmt in ReqElmt.iter('map'):
                            VDict = self.Vars.copy()
                            VDict.update(IdxDict.copy())
                            Formal = MapElmt.get('formal')
                            ActualList = SigName(MapElmt.get('actual'), RVars, VDict, LocalParams=LocalParams)
                            for Actual in ActualList:
                                Original = Actual[1][:]
                                Ref = Actual[1].replace('*', '_').replace('+', '_').replace('-', '_').replace('/', '_').replace('(', '_').replace(')', '_')
                                OpList = []
                                for A0 in Actual[1].split('*'):
                                    for A1 in Actual[1].split('+'):
                                        for A2 in Actual[1].split('-'):
                                            for A3 in Actual[1].split('/'):
                                                for A4 in Actual[1].split('('):
                                                    for A5 in Actual[1].split(')'):
                                                        OpList.append(A5)

                                for i, Operand in enumerate(OpList):
                                    if Operand in IdxDict:
                                        OpList[i] = str(IdxDict[Operand])

                                Actual[1] = ''
                                Cnt = 0
                                i = 0
                                while len(Actual[1]) != len(Ref):
                                    if i >= len(Original) or i >= len(Ref):
                                        logging.warning('{0}>=len(Original) ({1}) or {0}>=len(Ref) ({2})'.format(i, Original, Ref))
                                        break
                                    if Original[i] != Ref[i]:
                                        Actual[1] += Ref[i]
                                        Cnt += 1
                                        i += 1
                                    else:
                                        Actual[1] += OpList[Cnt]
                                        i += len(OpList[Cnt])
                                        Cnt += 1

                            if MapElmt.get('when') is None:
                                Cond = True
                            else:
                                Cond = Condition(eval(str(MapElmt.get('when')), VDict))
                            ReqMapping[Formal] = [
                             ActualList, Cond, IdxDict.copy()]

                        for V in RVars:
                            V = eval(V, VDict)

                        Alias = ReqElmt.get('alias')
                        if not Alias:
                            Alias = ReqName
                        else:
                            Alias += ':{0}'.format(Var)
                        self.AddReqServ(ReqID[0], ReqElmt.attrib.get('type'), ReqElmt.attrib.get('version'), ReqMapping, UniqueName=ServName(Alias, Vars=IdxDict.copy()))

                for SubLoopElmt in LoopElmt.iterchildren('loop'):
                    self.ParseLoops(SubLoopElmt, Indexes[:], IdxDict.copy())

        else:
            logging.error("[Module '{0}'] Can't find index name in loop.".format(self))

    def ParseIndex(self, String):
        """
                Parse index string in loop. Ex: "r=[0,rows[" <=> for r in range(0,rows,1)
                """
        if String:
            try:
                Var, Range = String.split('=')
            except:
                logging.error("[Module '{0}'] It should be one (and only one) '=' symbol in index description '{1}'.".format(self, String))

            try:
                Left, Right = Range.split(',')
            except:
                logging.error("[Module '{0}'] It should be one (and only one) ',' symbol in index description '{1}'.".format(self, String))

            InitVal = eval(Left[1:], self.Vars.copy())
            if Left.startswith('['):
                pass
            else:
                if Left.startswith(']'):
                    InitVal += 1
                else:
                    logging.error("[Module '{0}'] Wrong range description '{1}'. Expected brakets range format (ex: '[0,rows[').".format(self, Range))
                LastVal = eval(Right[:-1], self.Vars.copy())
                if Right.endswith('['):
                    LastVal -= 1
                else:
                    if Left.endswith(']'):
                        pass
                    else:
                        logging.error("[Module '{0}'] Wrong range description '{1}'. Expected brakets range format (ex: '[0,rows[').".format(self, Range))
            return (
             Var, InitVal, LastVal)
        else:
            return (None, 0, 0)

    def IdentifyServices(self, ServList):
        """
                Replace ID by a Service object
                and find the corresponding service in library
                """
        RequiredServ = collections.OrderedDict()
        for ID, ServReq in self.ReqServ.items():
            SName, SType, SVersion, UniqueName = ID.split('#')
            if SName in RequiredServ:
                RequiredServ[SName].append(ServReq)
            else:
                RequiredServ[SName] = [
                 ServReq]

        for S in ServList:
            if S.Name in RequiredServ:
                for Req in RequiredServ[S.Name]:
                    Req[0] = S

            elif S.Name in self.ProvidedServ:
                self.ProvidedServ[S.Name] = S

    def AddReqServ(self, SName, SType, SVersion, Mapping={}, UniqueName='', Serv=None):
        """
                Add a required service (defined by SName, SType, SVersion) to this module.
                """
        ID = '#'.join([SName, SType, SVersion, UniqueName])
        if SType == 'orthogonal':
            Constraints = None
            for Formal in Mapping:
                if Formal.lower() == 'constraints':
                    ActualList = Mapping.pop(Formal)
                    Constraints = ActualList[0][0][1]
                    break

            self.ReqServ[ID] = [
             Serv, Mapping, True, Constraints]
        else:
            self.ReqServ[ID] = [
             Serv, Mapping, False, None]

    def GetReqServMap(self, ReqServName):
        """
                Return the mapping dictionary of requested service if it exists. Return Empty dictionary otherwise.
                """
        ReqDict = collections.OrderedDict()
        for ReqServ, Mappings, IsOrtho, Constraints in list(self.ReqServ.values()):
            if ReqServ != None and ReqServ.Name == ReqServName:
                for Formal, Map in Mappings.items():
                    ActualList, Cond, IdxDict = Map
                    if len(ActualList) > 1:
                        pass
                    elif len(ActualList) == 1:
                        InstName, SigName, Index = ActualList[0]
                        if SigName in self.Ports:
                            ReqDict[SigName] = self.Ports[SigName]
                        elif SigName in self.OrthoPorts:
                            ReqDict[SigName] = self.OrthoPorts[SigName]
                        else:
                            logging.error('No mapping for formal port {0}. Unable to get required service associated.'.format(Formal))

        return ReqDict

    def GetReqServ(self, ReqServName=None):
        SList = [x[0] for x in list(self.ReqServ.values())]
        if ReqServName is None:
            return SList
        else:
            return [x for x in SList if x.Name == ReqServName and x is not None]

    def AddProvServ(self, SName, SAlias, mapping):
        """
                Add a service (defined by name and alias) to this module.
                """
        self.ServAlias[SAlias] = SName
        self.ProvidedServMap[SName] = mapping
        if SName not in self.ProvidedServ:
            self.ProvidedServ[SName] = None

    def AddParameter(self, XMLElmt, VarDict={}):
        """
                Add a parameter (defined by Name/type/size/default value) to this module.
                """
        Variables = self.Vars.copy()
        Variables.update(VarDict.copy())
        Param = Signal()
        Param.SetFrom(XMLElmt, Vars=Variables)
        self.Params[Param.Name] = Param
        self.Params[Param.Name].IsParam = True
        self.Vars[Param.Name] = Param.GetDefaultValue(NoEval=False, Vars=Variables)
        self.DependencyPkg(Param.TypeImport)

    def AddParameterAsSignal(self, Sig, VarDict={}):
        """
                Add a parameter (defined by Name/type/size/default value) to this module.
                """
        Variables = self.Vars.copy()
        Variables.update(VarDict.copy())
        Param = Sig
        self.Params[Param.Name] = Param
        self.Params[Param.Name].IsParam = True
        self.Vars[Param.Name] = Param.GetDefaultValue(NoEval=False, Vars=Variables)
        self.DependencyPkg(Param.TypeImport)

    def GetParametersDict(self):
        """
                Return the dictionary of module parameters.
                """
        return self.Params

    def GetConstants(self):
        """
                Return the dictionary of module parameters used for python eval() function.
                """
        return {k:v.GetDefaultValue() for k, v in self.Params.items()}

    def GetUsedParam(self):
        """
                Return the dictionary of USED module parameters.
                """
        UsedParams = self.UsedParams[:]
        for PName, Port in self.Ports.items():
            UsedParams += Port.GetUsedParam()

        return UsedParams

    def UpdateAllValues(self, ValueDict):
        """
                Change values of each port/params and their respective "usedparam" dictionary.
                """
        for PName, PVal in ValueDict.items():
            if PName in self.Params:
                self.Params[PName].SetValue(PVal)

        for PName, PSig in self.Params.items():
            PSig.UpdateAllValues(ValueDict)

    def AddPortAsSignal(self, Sig):
        """
                Add a port (defined by Name/type/size/default value) to this module.
                """
        self.Ports[Sig.GetName()] = Sig
        self.DependencyPkg(Sig.TypeImport)

    def AddPort(self, PName, PDir, PType, PTypeImport, PSize, PDefault, PModifier=None, PShare=False, IdxDict={}):
        """
                Add a port (defined by Name/type/size/default value) to this module.
                """
        Variables = self.Vars.copy()
        Variables.update(IdxDict.copy())
        PName = PName.replace('.', '_')
        Default = None if PDefault == '' else PDefault
        self.Ports[PName] = Signal(PName, PType, PTypeImport, PSize, Default, PDir, PModifier, bool(PShare), ParamVars=Variables.copy())
        self.DependencyPkg(PTypeImport)

    def SetupPortsFunc(self):
        """
                Add functions to each port from standard input.
                """
        for PName, P in self.Ports.items():
            P.GetFuncFromStdInput()

    def GetPortsDict(self):
        """
                Return the dictionary of module ports.
                """
        Ports = collections.OrderedDict()
        Rsts = list(self.GetReqServMap('reset').keys())
        Clks = list(self.GetReqServMap('clock').keys())
        INs = list(self.GetReqServMap('FPGA_Input').keys())
        OUTs = list(self.GetReqServMap('FPGA_Output').keys())
        for k, v in self.Ports.items():
            if k not in Rsts + Clks + INs + OUTs:
                Ports[k] = v

        return Ports

    def AddSources(self, SourceFileList, IsDependency=True):
        """
                Add a source files to this module Sources['RTL'] attribute.
                > Avoid double adds
                """
        NewSrcList = []
        for S in SourceFileList:
            if S in self.Sources['RTL']:
                self.Sources['RTL'].remove(S)
            NewSrcList.append(S)

        if IsDependency is True:
            self.Sources['RTL'] = NewSrcList + self.Sources['RTL']
        else:
            self.Sources['RTL'] = self.Sources['RTL'] + NewSrcList
        return NewSrcList

    def AddSource(self, SrcType, SrcName, SrcPathPattern, Synthesizable=False):
        """
                Add a source file to this module.
                """
        CurDir = os.path.abspath('./')
        if self.XmlFilePath is not None:
            os.chdir(os.path.dirname(self.XmlFilePath))
        for SrcPath in glob.glob(SrcPathPattern):
            if not os.path.isfile(SrcPath):
                logging.error("[Module '{0}'] No such file '{1}'. Fix the XML lib file ('{2}')".format(self.Name, SrcPath, self.XmlFilePath))
                sys.exit(1)
            if Synthesizable:
                if SrcType != None:
                    SupportedTypes = [
                     'package', 'library']
                    if SrcType.lower() in SupportedTypes:
                        if SrcName in self.Dependencies[SrcType]:
                            self.Dependencies[SrcType][SrcName].append(os.path.abspath(SrcPath))
                        else:
                            self.Dependencies[SrcType][SrcName] = [
                             os.path.abspath(SrcPath)]
                    else:
                        logging.error("Attribute 'type' of 'rtl' not recognized. Expected {0}. Found '{1}'".format(' or '.join(SupportedTypes), SrcType))
                else:
                    self.Sources['RTL'].append(os.path.abspath(SrcPath))
            else:
                self.Sources['Behavioral'].append(os.path.abspath(SrcPath))

        if self.XmlFilePath is not None:
            os.chdir(CurDir)

    def AddConstraintSource(self, SrcType, SrcName, SrcPath):
        """
                Add a source file to this module.
                """
        CurDir = os.path.abspath('./')
        if self.XmlFilePath is not None:
            os.chdir(os.path.dirname(self.XmlFilePath))
        self.Sources['Constraints'].append(os.path.abspath(SrcPath))
        if self.XmlFilePath is not None:
            os.chdir(CurDir)

    def GetConstraintSources(self, ReplacePatternDict={}):
        """
                return the constraints source file list of the module.
                """
        if len(ReplacePatternDict) > 0:
            for SrcPath in self.Sources['Constraints']:
                for VarName, VarValue in ReplacePatternDict.items():
                    ReplaceTextInFile(FileName=SrcPath, OldText='${0}'.format(VarName), NewText='{0}'.format(VarValue))

        return self.Sources['Constraints']

    def GetDependencies(self):
        """
                Return dictionary of Libname:[library paths,].
                """
        Dep = self.Dependencies.copy()
        for ReqServ, Mapping, IsOrtho, Constraints in list(self.ReqServ.values()):
            if ReqServ is None:
                logging.error('[Module.GetDependencies] No requested service for mapping !')
                continue
                SubMod = ReqServ.GetModule()
                if SubMod != None:
                    Dep.update(SubMod.GetDependencies())

        return Dep

    def AddResource(self, Dev, RName, Rused=0):
        """
                Add a resource information for an FPGA to this module.
                """
        if Dev in self.Resources:
            HwR = self.Resources[Dev]
        else:
            HwR = HwResources()
            self.Resources[Dev] = HwR
        return HwR.AddResources(Name=RName.upper(), Used=Rused, Available=-1, Percentage=-1)

    def CompatibleFPGAs(self):
        """
                Return list of referenced FPGA.
                """
        return [FPGA.upper() for FPGA in self.Resources.keys()]

    def GetUsedResources(self, DeviceName):
        """
                Add a resource information for an FPGA to this module.
                """
        if self.Name == 'SimuCom':
            return HwResources()
        if DeviceName in self.Resources:
            return self.Resources[DeviceName]
        logging.debug("{0}'s resources: {1}".format(self, self.Resources))
        logging.warning("[Module.GetUsedResources] Device '{0}' not in module '{1}' resources.".format(DeviceName, self))

    def GetOutputDataSize(self):
        """
                Return the number of bits for output data.
                """
        Sum = 0
        for SName, S in self.ProvidedServ.items():
            if SName.lower() in ('userclock', 'userreset'):
                pass
            else:
                Sum += S.GetOutputDataSize()

        return Sum

    def GetMaxFreq(self, FPGA):
        """
                Return highest frequency associated with an FPGA.
                """
        if 'ALL' in self.MaxFreq:
            return self.MaxFreq['ALL']
        else:
            if FPGA.upper() in self.MaxFreq:
                return self.MaxFreq[FPGA]
            return

    def GetLatency(self):
        """
                Return latency of the module.
                """
        return self.Latency

    def GetDataIntroductionInterval(self):
        """
                Return Data Introduction Interval value.
                """
        return self.DataIntroductionInterval

    def GetThroughput(self, FPGA):
        """
                Return highest throughput associated with an FPGA.
                """
        if 'ALL' in self.MaxFreq:
            return self.MaxFreq['ALL'] / self.DataIntroductionInterval
        else:
            if FPGA.upper() in self.MaxFreq:
                return self.MaxFreq[FPGA] / self.DataIntroductionInterval
            return

    def IsAbstract(self):
        """
                Return False if RequiredServices list is empty, True otherwise.
                """
        return self.AbstractModule

    def GetAbsFileName(self):
        """
                Return abstract name of top file if module is abstract.
                """
        if self.IsAbstract():
            return '{0}.vhd'.format(self.Name)
        else:
            return

    def GetTop(self):
        """
                return entity name and path of HDL Top source.
                """
        Sources = self.Sources['RTL']
        if len(Sources) == 0:
            return (None, None)
        return (
         self.Name, Sources[(-1)])

    def GetSources(self, Synthesizable=True, Constraints=None, IsTop=False, IgnorePkg=True):
        """
                Return the list of source files of this module and its dependencies.
                """
        SrcList = []
        if Synthesizable:
            TYPE = 'RTL'
        else:
            TYPE = 'Behavioral'
        for Src in self.Sources[TYPE]:
            if Src not in SrcList:
                SrcList.append(Src)

        if not IgnorePkg:
            for PackSrcList in list(self.Dependencies['package'].values()):
                for PackSrc in PackSrcList:
                    if PackSrc not in SrcList:
                        SrcList.append(PackSrc)

        if IsTop:
            SrcList.append(os.path.abspath(self.GetTopPackName()))
        for ID, (Serv, Map, IsOrtho, Constraints) in self.ReqServ.items():
            if Serv is None:
                logging.error("[Module {0}] Required service '{1}' missing: source fetch skipped.".format(self, ID))
            elif not IsOrtho:
                SubMod = Serv.GetModule(Constraints=Constraints)
                if SubMod != None:
                    SubModSrcList = SubMod.GetSources(Synthesizable=Synthesizable, Constraints=Constraints)
                    SrcList += [x for x in SubModSrcList if x not in SrcList]

        if self.IsAbstract():
            SrcList.append(os.path.join(os.path.dirname(self.XmlFilePath), self.GetAbsFileName()))
        return SrcList

    def RemoveSources(self, SourceList, Synthesizable=True):
        """
                Remove HDL src to the list of source files of this module.
                """
        if Synthesizable:
            TYPE = 'RTL'
        else:
            TYPE = 'Behavioral'
        for Src in SourceList:
            if Src in self.Sources[TYPE]:
                self.Sources[TYPE].remove(Src)

        return True

    def ReplaceSource(self, OldPath, NewPath, Synthesizable=True):
        """
                Remove HDL src to the list of source files of this module and replace it by New pat.
                """
        if Synthesizable:
            TYPE = 'RTL'
        else:
            TYPE = 'Behavioral'
        if OldPath in self.Sources[TYPE]:
            Idx = self.Sources[TYPE].index(OldPath)
            self.Sources[TYPE].remove(OldPath)
            self.Sources[TYPE].insert(Idx, NewPath)
        return True

    def ReplaceConstraintSource(self, OldPath, NewPath):
        """
                Remove HDL src to the list of source files of this module and replace it by New path.
                Replace each pattern by its value.
                """
        if OldPath in self.Sources['Constraints']:
            Idx = self.Sources['Constraints'].index(OldPath)
            self.Sources['Constraints'].remove(OldPath)
            self.Sources['Constraints'].insert(Idx, NewPath)
        return True

    def Provide(self, SName):
        """
                Return True if this module implement the specified service (identified by its name).
                """
        if SName in self.ProvidedServ:
            return True
        else:
            return False

    def GetProvidedService(self, Name=None):
        """
                Return first item found in self.ProvidedServ.
                """
        if len(self.ProvidedServ) == 0:
            logging.warning('Module {0} provide no services !'.format(self))
            return
        if Name is None:
            for Key, Value in self.ProvidedServ.items():
                return Value

        else:
            return self.ProvidedServ[Name]

    def GetPadConstraints(self):
        Constraints = []
        UniqueList = []
        for PName, P in self.Ports.items():
            if P.Name in UniqueList:
                continue
            else:
                UniqueList.append(P.Name)
            if P.Constraints is None:
                Constraints.append((P, None, 'Ignore'))
            else:
                Type, Identifier, FormalMap = P.Constraints
                PadType = FormalMap.upper()
                Constraints.append((P, PadType, Identifier))

        if self.IsAbstract():
            for PName, P in self.OrthoPorts.items():
                if P.Name in UniqueList:
                    continue
                else:
                    UniqueList.append(P.Name)
                OP = P.Copy()
                OP.Name = PName
                if OP.Constraints is None:
                    Constraints.append((OP, None, 'Ignore'))
                else:
                    Type, Identifier, FormalMap = OP.Constraints
                    PadType = FormalMap.upper()
                    Constraints.append((OP, PadType, Identifier))

        return Constraints

    def GetClockNames(self, MappedName=False):
        """
                Return the list of clock names connected to service 'clock'.
                """
        ClockList = []
        for ServID, (Serv, ClkMapping, IsOrtho, Constraints) in self.ReqServ.items():
            if ServID.startswith('clock'):
                for Formal, ActualCond in ClkMapping.items():
                    if Formal in Serv.Params:
                        pass
                    else:
                        ActualList, Cond, OtherDict = ActualCond
                        ActualName = ActualList[0][1]
                        if ActualName in self.Ports:
                            if MappedName:
                                ClockList.append(SharedName(Formal=Formal, Params=Serv.Params, ReqMap=ClkMapping))
                            else:
                                ClockList.append(ActualName)
                        else:
                            ClockList.append(SharedName(Formal=Formal, Params=Serv.Params, ReqMap=ClkMapping))

            if Serv is None:
                logging.warning("[GetClockNames] Service '{0}' not a referenced service.".format(ServID))
                continue
                Mod = Serv.GetModule()
                if Mod:
                    ClockList += Mod.GetClockNames(MappedName=True)

        ClockList = list(set(ClockList))
        return ClockList

    def GetResetNames(self, MappedName=False):
        """
                Return the list of reset names connected to service 'reset'.
                """
        ResetList = []
        for ServID, (Serv, ResetMapping, IsOrtho, Constraints) in self.ReqServ.items():
            if Serv is None:
                logging.warning("[GetResetNames] Service '{0}' not a referenced service.".format(ServID))
                continue
            else:
                if ServID.startswith('reset'):
                    for Formal, ActualCond in ResetMapping.items():
                        if Formal in Serv.Params:
                            pass
                        else:
                            ActualList, Cond, OtherDict = ActualCond
                            ActualName = ActualList[0][1]

                    if ActualName in self.Ports:
                        if MappedName:
                            ResetList.append(SharedName(Formal=Formal, Params=Serv.Params, ReqMap=ResetMapping))
                        else:
                            ResetList.append(ActualName)
                else:
                    ResetList.append(SharedName(Formal=Formal, Params=Serv.Params, ReqMap=ResetMapping))
            Mod = Serv.GetModule()
            if Mod:
                ResetList += Mod.GetResetNames(MappedName=True)

        ResetList = list(set(ResetList))
        return ResetList

    def GetStimuliNames(self):
        """
                Return the list of stimuli names.
                """
        return [P.Rename(N).AVAName() for N, P in self.GetExternalPorts().items() if P.Direction == 'IN']

    def GetTraceNames(self):
        """
                Return the list of Trace names.
                """
        return [P.Rename(N).AVAName() for N, P in self.GetExternalPorts().items() if P.Direction == 'OUT']

    def GetBidirNames(self):
        """
                Return the list of bidirectionals names.
                """
        return [P.Rename(N).AVAName() for N, P in self.GetExternalPorts().items() if P.Direction == 'INOUT']

    def GetDataPorts(self):
        """
                return list of port without reset and clocks.
                """
        DataPortDict = {}
        for PName, P in self.Ports.items():
            if not PName in self.GetClockNames():
                if PName in self.GetResetNames():
                    continue
                else:
                    DataPortDict[PName] = P

        return DataPortDict

    def GetExternalPorts(self, CalledServ=None):
        """
                Return the list of clock names connected to service 'clock'.
                CalledServ is the service that this module provide.
                """
        PortDict = collections.OrderedDict()
        ItfPorts = self.Ports.copy()
        ItfPorts.update(dict((OP.OrthoName(), OP) for OP in list(self.OrthoPorts.values())))
        for ServID, (Serv, PortMapping, IsOrtho, Constraints) in self.ReqServ.items():
            if Serv is None:
                logging.warning("[GetClockNames] Service '{0}' not a referenced service.".format(ServID))
                continue
                Mod = Serv.GetModule()
                if Mod:
                    PortDict.update(Mod.GetExternalPorts(CalledServ=Serv))
                if ServID.startswith('FPGAPads'):
                    PortDict.update({PortMapping[x][0][0][1]:ItfPorts[PortMapping[x][0][0][1]] for x in list(PortMapping.keys())})

        return PortDict

    def Characteristics(self):
        """
                Return the number of clocks, stimuli, traces, bidirectionals of the module.
                """
        NbClk = len(self.GetClockNames())
        NbStim = len(self.GetStimuliNames() + self.GetResetNames())
        NbTrace = len(self.GetTraceNames())
        NbBiDir = len(self.GetBidirNames())
        return (NbClk, NbStim, NbTrace, NbBiDir)

    def PropagateServDefaultParam(self, Serv):
        """
                Set default value for each parameters/port from provided service.
                """
        for PName, P in Serv.Params.items():
            Mapping = self.ProvidedServMap[Serv.Name]
            if PName in Mapping:
                MappedName = Mapping[PName]
                if MappedName in self.Params:
                    V = P.GetValue()
                    self.Params[MappedName].SetValue(V)
                    self.Params[MappedName].SetDefault(V)

    def GenSrc(self, Synthesizable=True, OutputDir='./Output', TestBench=False, IsTop=True, ProcessedServ={}, ModInstance=None, TBValues={}, TBClkCycles=1600, TBCycleLength=10, CommunicationService=None, Recursive=True, NewPkg=True, HwConstraints=None):
        """
                Generate source files or copy sources to output directory.
                Return list of generated sources if success.
                """
        if IsTop is False:
            OutputDir = os.path.join(OutputDir, self.Name)
        if not os.path.isdir(OutputDir):
            os.makedirs(OutputDir)
        self.XmlFilePath = self.DumpToFile(OutputPath=OutputDir)
        for SName, S in self.ProvidedServ.items():
            if S is None:
                logging.error("[{0}:GenSrc] No service associated with '{1}'.".format(self.Name, SName))
                continue
                S.XmlFilePath = S.DumpToFile(OutputPath=OutputDir)

        if Synthesizable:
            TYPE = 'RTL'
        else:
            TYPE = 'Behavioral'
        ArchName = TYPE
        self.IntSignals = collections.OrderedDict()
        self.Connections = collections.OrderedDict()
        if ModInstance is None:
            ModInstance = Instance(self.Name, self)
        if self.IsAbstract():
            ArchName = 'RTL'
            Content = ''
            Declarations = ''
            for BaseName, CDict in self.Const.items():
                for C in sorted(CDict.keys()):
                    Declarations += CDict[C].Declare(Constant=True)

            SubMod = None
            for ServID in sorted(self.ReqServ.keys()):
                SubServ, SubModMap, IsOrtho, Constraints = self.ReqServ[ServID]
                if SubServ:
                    if SubServ.Name == 'FPGAPads':
                        pass
                    else:
                        SubMod = SubServ.GetModule(Constraints=HwConstraints)
                        if SubMod is None:
                            Msg = "[HdlLib.SysGen.Module.GenSrc] no module associated with service '{0}' in instances of {1} for constraints '{2}'.".format(SubServ.Name, self.Name, HwConstraints)
                            logging.error(Msg)
                            raise SyntheSysError(Msg)
                        if not IsOrtho:
                            self.AddOrtho(SubServ, SubMod, SubModMap, Constraints, HwConstraints=HwConstraints)
                        for ParameterName in list(SubModMap.keys()):
                            if ParameterName in SubServ.Params:
                                for Actual in SubModMap[ParameterName][0]:
                                    Val = str(Actual[1])
                                    if Val in self.Params:
                                        SubServ.Params[ParameterName].SetValue(self.Params[Val].GetDefaultValue())

                        if SubMod is None:
                            logging.warning('Service {0} ignored due to absence of implementation module.'.format(SubServ))
                        else:
                            InstanceName = ServID.split('#')[(-1)]
                            INSTANCE = None
                            if SubServ.Name not in ProcessedServ:
                                if not SubServ.IsOrthogonal():
                                    INSTANCE = ModInstance.AddInstance(Name=InstanceName, Mod=SubMod)
                                ProcessedServ[SubServ.Name] = INSTANCE
                                if Recursive is True:
                                    SubServSrc = SubServ.GenSrc(Synthesizable=Synthesizable, OutputDir=OutputDir, IsTop=False, HwConstraints=HwConstraints, ProcessedServ=ProcessedServ)
                                    self.AddSources(SubServSrc, IsDependency=True)
                            elif not SubServ.IsOrthogonal():
                                INSTANCE = ProcessedServ[SubServ.Name].Copy()
                                INSTANCE.Name = InstanceName
                                ModInstance.AddInstanceAsInstance(INSTANCE)
                                self.AddSources(INSTANCE.Mod.Sources['RTL'], IsDependency=True)
                            if SubServ.IsOrthogonal():
                                OrthoPorts = []
                                for S in list(SubMod.Ports.values()):
                                    SCopy = S.Copy()
                                    SCopy.Name = '_'.join([InstanceName, S.Name])
                                    OrthoPorts.append(SCopy)

                                ODict = collections.OrderedDict()
                                for O in OrthoPorts:
                                    ODict[O.Name] = O

                                self.OrthoPorts.update(ODict)
                                continue
                                self.OrthoPorts.update(SubMod.OrthoPorts)
                                SubServMap = SubMod.ProvidedServMap[SubServ.Name]
                                PortDict, GenericDict, Cont, IntSignals = self.BuildMap(SubServ, SubModMap, SubMod, SubServMap, InstanceName)
                                Content += HDL.Instantiate(InstanceName=InstanceName, Module=SubMod.Name, Architecture=TYPE, SignalDict=PortDict, GenericDict=GenericDict, Comment=str(SubMod.Title))
                                Content += Cont + '\n' + '-' * 65
                                self.IntSignals.update(IntSignals)
                                ConstMap = {k.replace(k.split(':')[0], SubServMap[k.split(':')[0]]):v for k, v in SubModMap.items() if k.split(':')[0] in SubServMap}
                                for IntSigName in sorted(IntSignals.keys()):
                                    if IntSigName not in self.OrthoPorts:
                                        IntSignals[IntSigName].MapConstants(Mapping=ConstMap)

                            else:
                                logging.warning('[Module.GenSrc] In module {0}, no service associated with requested {1}.'.format(self, ServID))

            for IntSigName in sorted(self.IntSignals.keys()):
                if IntSigName not in self.OrthoPorts:
                    self.IntSignals[IntSigName].InitVal = ''
                    Declarations += self.IntSignals[IntSigName].Declare(UnConstrained=False)

            TopPath = LibEditor.HDLModule(OutputPath=OutputDir, Mod=self, Packages=self.Dependencies['package'].keys(), Libraries=[
             'IEEE'], Declarations=Declarations, Content=Content)
            self.AddSources([os.path.abspath(TopPath)], IsDependency=False)
            if IsTop is True and NewPkg is True:
                self.CollectPkg()
                Pkg, PkgPath = self.GenPackage(self.Name, OutputDir)
                if Pkg:
                    self.AddSources([os.path.abspath(PkgPath)], IsDependency=True)
            else:
                Pkg = None
        else:
            if IsTop is True:
                DepSources = [P for P in self.Dependencies['package'].values() if P is not None]
            else:
                DepSources = []
            for Src in self.Sources['RTL'] + DepSources:
                for SrcItem in glob.iglob(Src):
                    NewSource = os.path.join(os.path.abspath(OutputDir), os.path.basename(SrcItem))
                    if os.path.abspath(SrcItem) != NewSource:
                        shutil.copy(SrcItem, OutputDir)
                        self.ReplaceSource(Src, NewSource, Synthesizable=True)

            for Src in self.GetConstraintSources():
                for SrcItem in glob.iglob(Src):
                    NewSource = os.path.join(os.path.abspath(OutputDir), os.path.basename(SrcItem))
                    if os.path.abspath(SrcItem) != NewSource:
                        shutil.copy(SrcItem, OutputDir)
                        self.ReplaceConstraintSource(Src, NewSource)

            for SubServ, SubModMap, IsOrtho, Constraints in list(self.ReqServ.values()):
                if SubServ:
                    if SubServ.Name == 'FPGAPads':
                        pass
                    else:
                        SubMod = SubServ.GetModule(Constraints=HwConstraints)
                        if SubMod:
                            self.AddOrtho(SubServ, SubMod, SubModMap, Constraints, HwConstraints=HwConstraints)
                            if SubServ.Name not in ProcessedServ:
                                if Recursive is True:
                                    SubServSrc = SubServ.GenSrc(Synthesizable=Synthesizable, OutputDir=OutputDir, IsTop=False, HwConstraints=HwConstraints, ProcessedServ=ProcessedServ)
                                    self.AddSources(SubServSrc, IsDependency=True)
                            else:
                                self.AddSources(SubMod.Sources['RTL'], IsDependency=True)
                        else:
                            Msg = "[HdlLib.SysGen.Module.GenSrc] no module associated with service '{0}' in instances of {1} for following constraints:{2}.".format(SubServ.Name, self.Name, HwConstraints)
                            logging.error(Msg)
                            raise SyntheSysError(Msg)

            if IsTop is True:
                self.CollectPkg()
                Pkg, PkgPath = self.GenPackage(self.Name, OutputDir)
                if Pkg:
                    self.AddSources([os.path.abspath(PkgPath)], IsDependency=True)
            else:
                Pkg = None
        if TestBench:
            self.GenTB(Pkg, TYPE, OutputDir, TBValues=TBValues, NbCycles=TBClkCycles, CycleLength=TBCycleLength, CommunicationService=CommunicationService, ParamVars=self.Vars.copy())
        if IsTop is True and NewPkg is True:
            AlreadyModified = []
            AlreadyModified.append(self.Sources['RTL'][1])
            for SrcPath in self.Sources['RTL'][1:]:
                if not AlreadyModified.count(SrcPath) and SrcPath.endswith('.vhd'):
                    AlreadyModified.append(SrcPath)
                    with open(SrcPath, 'r') as (SrcFile):
                        Code = SrcFile.read()
                    with open(SrcPath, 'w+') as (SrcFile):
                        SrcFile.write(HDL.Packages(['work.' + Pkg]))
                        SrcFile.write('\n' + Code)

            if Pkg not in self.Dependencies['package']:
                self.Dependencies['package']['work.' + Pkg] = PkgPath
            return self.Sources['RTL']
        return self.Sources['RTL']

    def BuildMap(self, SubServ, SubModMap, SubMod, SubServMap, InstanceName):
        """
                Instanciate a Service in this module for HDL deployement.
                Fill PortDict, GenericDict, declaration and content for interconnections.
                """
        Connections = collections.OrderedDict()
        GenericDict = collections.OrderedDict()
        PortDict = collections.OrderedDict()
        OrthoMap = collections.OrderedDict()
        OrthoPorts = collections.OrderedDict()
        IntSignals = collections.OrderedDict()
        if SubMod.IsAbstract():
            for Actual, FormalSig in SubMod.OrthoPorts.items():
                OrthoPorts[FormalSig.OrthoName()] = FormalSig
                if SubMod.IsAbstract():
                    OName = FormalSig.OrthoName()
                    OrthoMap[OName] = OName
                else:
                    OrthoMap[Actual] = FormalSig.OrthoName()

            PortDict.update(OrthoMap)
        else:
            for PName, P in SubMod.Ports.items():
                if PName not in SubModMap and PName in SubMod.OrthoPorts:
                    PortDict[PName] = SubMod.OrthoPorts[PName].Name

        ModuleMap = []
        for Formal, ActualCond in SubModMap.items():
            F = Formal.split(':')[0]
            if F not in SubServMap:
                if F in SubMod.OrthoPorts:
                    ModuleMap.append([Formal, ActualCond])
                else:
                    logging.error("[Module '{0}'] No such formal signal '{1}' in {2} mapping.".format(self, F, SubServ.Name))
                    logging.error('SubServ:    {0}'.format(SubServ))
                    logging.error('SubServMap: {0}'.format(SubServMap))
                    logging.error('SubMod.OrthoPorts: {0}'.format(list(SubMod.OrthoPorts.keys())))
                    sys.exit(1)
                    continue
                    if SubServMap[F] in SubMod.Params:
                        ModuleMap.insert(0, [Formal, ActualCond])
                    else:
                        ModuleMap.append([Formal, ActualCond])

        for Formal, ActualCond in ModuleMap:
            Actuals, Condition, Vars = ActualCond
            FormalSigName = None
            IntermediateSignal = False
            if Formal:
                SplitFormal = Formal.split(':')
                if SplitFormal[0] == '':
                    SplitFormal[0] = Formal
                if SplitFormal[0] in SubServMap:
                    FormalSigName = SubServMap[SplitFormal[0]]
                else:
                    if SplitFormal[0] in OrthoPorts:
                        FormalSigName = SplitFormal[0]
                    else:
                        FormalSigName = SplitFormal[0]
                        logging.warning("[BuildMap:Module {0}] Service port '{1}' not mapped in this module".format(self, SplitFormal[0]))
                    if len(SplitFormal) > 1:
                        IntermediateSignal = True
                        FormalIndex = SplitFormal[1]
                    else:
                        FormalIndex = None
                ReverseServMap = collections.OrderedDict()
                for k, v in list(SubServMap.items()):
                    ReverseServMap[v] = k

                if FormalSigName:
                    if FormalSigName in SubMod.Ports:
                        FormalSig = SubMod.Ports[FormalSigName]
                    else:
                        if FormalSigName in SubMod.Params:
                            FormalSig = SubMod.Params[FormalSigName]
                            self.UsedParams.append(FormalSigName)
                        else:
                            if FormalSigName in SubMod.OrthoPorts:
                                FormalSig = SubMod.OrthoPorts[FormalSigName]
                            else:
                                logging.error("Formal signal '{0}' not found in ports or parameters of '{1}'".format(FormalSigName, SubMod))
                                logging.debug('SubMod.OrthoPorts:'.format(list(SubMod.OrthoPorts.keys())))
                                raise NameError("Formal signal '{0}' not found in ports or parameters of '{1}'".format(FormalSigName, SubMod))
                            CopyVars = SubMod.Vars.copy()
                            CopyVars.update(self.Vars)
                            CopyVars.update(Vars)

                            def CheckCondition(Condition):
                                if Condition is True:
                                    return True
                                else:
                                    if Condition is None or Condition is False:
                                        return False
                                    if Condition.Evaluate(CopyVars.copy()):
                                        return True
                                    return False

                            if CheckCondition(Condition):
                                ConcatList = []
                                for InstName, SigName, AIndex in Actuals:
                                    try:
                                        SVal = int(SigName)
                                    except:
                                        SVal = None

                                    if SVal is None:
                                        HDLActual = None
                                        if FormalSigName in SubMod.Params:
                                            HDLActual = SubMod.Params[FormalSigName].HDLFormat(ParamVars=self.Vars)
                                            HDLActual.Name = SigName
                                            self.UsedParams.append(SigName)
                                            if AIndex is not None:
                                                HDLActual.SetIndex(AIndex)
                                        else:
                                            if InstName == InstanceName or InstName == '' or InstName is None:
                                                if SigName in self.Ports:
                                                    ActualName = '_'.join([InstanceName, SigName])
                                                    HDLActual = self.Ports[SigName].HDLFormat(ParamVars=self.Vars)
                                                    if AIndex is not None:
                                                        HDLActual.SetIndex(AIndex)
                                                else:
                                                    if SigName in self.Params:
                                                        logging.error("[BuildMap] Formal signal '{0}' is connected to parameter '{1}'".format(FormalSigName, SigName))
                                                        exit(1)
                                                    else:
                                                        if SigName in OrthoPorts:
                                                            ActualName = SigName
                                                            HDLActual = OrthoPorts[SigName].HDLFormat(ParamVars=self.Vars)
                                                            if AIndex is not None:
                                                                HDLActual.SetIndex(AIndex)
                                                        else:
                                                            ActualName = '_'.join([InstanceName, SigName])
                                                            HDLActual = GetInternalSigFrom(Sig=FormalSig, FIndex=FormalIndex, AIndex=AIndex, WithName=ActualName, Mod=SubMod, IntSigs=IntSignals)
                                            else:
                                                ActualName = '_'.join([InstName, SigName])
                                                if SigName in SubMod.Params:
                                                    logging.error("[BuildMap] Connection of parameters '{0}' between instances (one of them is '{1}'). This will fail to compile.".format(SigName, SubMod))
                                                    exit(1)
                                                if SigName in self.Params:
                                                    FormalSig = self.Params[SigName]
                                                HDLActual = GetInternalSigFrom(Sig=FormalSig, FIndex=FormalIndex, AIndex=AIndex, WithName=ActualName, Mod=SubMod, IntSigs={})
                                        ConcatList.append(HDLActual)
                                    elif FormalSigName in SubMod.Ports:
                                        Port = SubMod.Ports[FormalSigName]
                                        ConcatList.append(Port.HDLFormat(CopyVars).GetValue(SVal, WriteBits=True))
                                    else:
                                        Param = SubMod.Params[FormalSigName]
                                        ConcatList.append(Param.HDLFormat(CopyVars).GetValue(SVal, WriteBits=True))

                                if len(ConcatList) > 1:
                                    IntermediateSignal = True
                                HDLActual = reduce(lambda x, y: x + y, ConcatList)
                            else:
                                continue
                        if IntermediateSignal is False:
                            if FormalSigName in SubMod.Ports:
                                PortDict[FormalSigName] = HDLActual
                            else:
                                if FormalSigName in SubMod.Params:
                                    GenericDict[FormalSigName] = HDLActual
                                else:
                                    if FormalSigName in SubMod.OrthoPorts:
                                        PortDict[FormalSigName] = HDLActual
                                    else:
                                        logging.error('No such formal signal {0} mapped to submodule {1}'.format(repr(FormalSigName), SubMod))
                                        logging.error('Available ports:')
                                        for P in SubMod.Ports:
                                            logging.error('\t> {0}'.format(repr(P)))

                                        logging.error('Available parameters:')
                                        for P in SubMod.Params:
                                            logging.error('\t> {0}'.format(repr(P)))

                                        sys.exit(1)
                        else:
                            InterSigName = InstanceName + '_' + ReverseServMap[FormalSigName]
                            InterSig = IndirectConnection(InterSigName, FormalIndex, FormalSig, HDLActual, Connections, IntSigs=IntSignals, Vars=CopyVars)
                            if FormalSigName in SubMod.Ports:
                                PortDict[FormalSigName] = InterSig
                            else:
                                if FormalSigName in SubMod.Params:
                                    GenericDict[FormalSigName] = InterSig
                                else:
                                    if FormalSigName in OrthoPorts:
                                        PortDict[FormalSigName] = InterSig
                                    else:
                                        logging.error('No such formal {1} signal mapped to submodule {0}'.format(SubMod, FormalSigName))
                    continue

        Content = ''
        for FormalSig in sorted(Connections.keys()):
            ActualSignals = Connections[FormalSig]
            Zeros = self.GetMissing(ActualSignals, FormalSig, SubMod.Vars.copy())
            if isinstance(ActualSignals, dict):
                FullConnections = ActualSignals.copy()
                FullConnections.update(Zeros)
                for Index in sorted(FullConnections.keys()):
                    ActualSig = FullConnections[Index]
                    if ActualSig.Name != FormalSig.Name:
                        FormalSig.SetIndex(Index)
                        if Index not in Zeros:
                            if FormalSig.Direction.upper() == 'IN':
                                Content += ActualSig.Connect(FormalSig, False)
                            else:
                                Content += FormalSig.Connect(ActualSig, False)
                            FormalSig.SetIndex(None)

            else:
                if FormalSig.Direction.upper() == 'OUT':
                    Content += ActualSignals.Connect(FormalSig, False)
                else:
                    Content += FormalSig.Connect(ActualSignals, False)

        self.Connections.update(Connections)
        return (
         PortDict, GenericDict, Content, IntSignals)

    def GenTB(self, Pkg, TYPE, OutputDir, TBValues={}, NbCycles=1600, CycleLength=10, CommunicationService=None, ParamVars={}):
        """
                Generate TestBench files 'module_tb.vhd' and 'module_tb_io.txt'.
                """
        logging.debug("Create testbench for design '{0}'".format(self.Name))
        V = {k:v.GetValue() for k, v in self.Params.items()}
        for P in list(self.Ports.values()) + list(self.OrthoPorts.values()):
            P.UpdateVars(V)

        TB_FilePath = os.path.join(OutputDir, '{0}_tb.vhd'.format(self.Name))
        self.TBEntity = '{0}_tb'.format(self.Name)
        self.TBSource = TB_FilePath
        self.Sources['Behavioral'].append(TB_FilePath)
        with open(TB_FilePath, 'w+') as (TB_File):
            TB_File.write(HDL.Header('{0}_tb'.format(self.Name), "Generate {0}'s stimuli".format(self.Name), 'Perform testbench', 'Use TextIO module to get stimuli.', 'no known issues', 'No speed information', 'No area information', 'Xilinx isim', self.Version))
            TB_File.write(HDL.Libraries(['IEEE']))
            TB_File.write(HDL.Packages(['IEEE.std_logic_1164']))
            TB_File.write(HDL.Packages(['std.textio']))
            if Pkg:
                TB_File.write(HDL.Packages(['work.' + Pkg]))
            Generics = []
            Ports = []
            TB_File.write(HDL.Entity('{0}_tb'.format(self.Name), Generics, Ports, "{0}'s testbench module".format(self.Name)))
            Content = '\n'
            Params = [P for N, P in self.Params.items() if N in self.UsedParams]
            Signals = list(self.Ports.values())
            for OPName, OP in self.OrthoPorts.items():
                if OPName not in self.Ports:
                    Signals.append(OP)

            Signals = RemoveDuplicated(Signals)
            Aliases = []
            PortDict = collections.OrderedDict()
            GenericDict = collections.OrderedDict()
            for Par in Params:
                GenericDict[Par.Name] = Par.HDLFormat(ParamVars.copy())

            for Sig in Signals:
                PortDict[Sig.OrthoName()] = Sig.HDLFormat(ParamVars.copy())

            self.TB_DUT = 'DUT_' + self.Name
            Content += HDL.Instantiate(self.TB_DUT, self.Name, TYPE, PortDict, GenericDict, Comment=str('Instantiate DUT module'))
            Declarations = '\n'
            Stim = Signal('Stimuli', Type='logic', Size=99999)
            for P in Params:
                Declarations += P.HDLFormat(ParamVars.copy()).Declare(Constant=True)

            Declarations += '\n'
            CurIdx = 0
            for S in Signals:
                ParamVars.update(S.GetUsedParam())
                if S.Direction.upper() == 'OUT':
                    Declarations += S.HDLFormat(ParamVars.copy()).Declare()
                elif S.Type.lower() == 'logic':
                    Size = S.FullSize if S.FullSize != None else S.Size
                    EndIdx = eval(str(Size) + '-1', ParamVars) + CurIdx
                    Declarations += S.HDLFormat(ParamVars.copy()).AliasOf(Stim.HDLFormat(ParamVars.copy())[EndIdx:CurIdx])
                    Aliases.append(S)
                    CurIdx += eval(Size, ParamVars)
                elif S.Type.lower() == 'numeric':
                    Declarations += S.HDLFormat(ParamVars.copy()).Declare()
                    S_bits = S.Copy()
                    S_bits.Name = 'TO_INTEGER({0})'.format(S.Name + '_bits')
                    Content += S.HDLFormat(ParamVars.copy()).Connect(S_bits.HDLFormat(ParamVars.copy()))
                    S_bits.Name = S.Name + '_bits'
                    S_bits.Type = 'logic'
                    if S.Size == '':
                        logging.warning("Size of signal '{0}' undefined.".format(S))
                        S.Size = 1
                    Size = S.FullSize if S.FullSize != None and S.FullSize != '' else S.Size
                    if Size is None:
                        logging.error("Signal '{0}' don't have a predefined size: aborted.'".format(S))
                        raise 'Size error'
                    EndIdx = eval(str(Size), ParamVars) + CurIdx
                    Declarations += S_bits.HDLFormat(ParamVars.copy()).AliasOf(Stim.HDLFormat(ParamVars.copy())[CurIdx:EndIdx])
                    Aliases.append(S_bits)
                    CurIdx += eval(S_bits.FullSize, ParamVars)
                else:
                    S.ComputeType()
                    Declarations += S.HDLFormat(ParamVars.copy()).Declare()
                    S_bits = S.Copy()
                    S_bits.TypeImport = None
                    S_bits.Size = eval(str(S.Size) + '*' + S.Type.split('*')[0], ParamVars)
                    S_bits.FullSize = S_bits.Size
                    S_bits.Type = 'logic'
                    S_bits.Name += '_bits'
                    S_bits2 = S_bits.Copy()
                    S_bits2.Name += '_link'
                    S_bits2_bis = S_bits2.Copy()
                    S_bits2_bis.Name += '((i+1)*{0}-1 downto i*{0})'.format(S.Type.split('*')[0])
                    Content += '\n' + HDL.For(Name='ArrayToSig_{0}'.format(S.Name), Var='i', Start=0, Stop=str(S.FullSize) + '-1', Content=S.HDLFormat(ParamVars.copy())['i'].Connect(S_bits2_bis.HDLFormat(ParamVars.copy())), Comments='TB array to signal conversion')
                    Declarations += S_bits.HDLFormat(ParamVars.copy()).AliasOf(Stim.HDLFormat(ParamVars.copy())[CurIdx:S_bits.Size + CurIdx])
                    HDL_S_bits2 = S_bits2.HDLFormat(ParamVars.copy())
                    Declarations += HDL_S_bits2.Declare()
                    Content += '\n' + S_bits2.HDLFormat(ParamVars.copy()).Connect(S_bits.HDLFormat(ParamVars.copy()))
                    Aliases.append(S_bits)
                    CurIdx += S_bits.Size

            Stim.Size = CurIdx
            Stim.FullSize = CurIdx
            StimSize = Signal('NbStimuli', Type='numeric', Default=CurIdx)
            Declarations = StimSize.HDLFormat(ParamVars.copy()).Declare(Constant=True) + Declarations
            Declarations = Stim.HDLFormat(ParamVars.copy()).Declare() + Declarations
            Content += HDL.GetTBProcess(self.Name)
            TB_File.write(HDL.Architecture('TestIO_TB', '{0}_tb'.format(self.Name), Declarations, Content, 'Use TextIO module to get stimuli.'))
        IO_FilePath = os.path.join(OutputDir, 'stimValues.txt')
        self.TBDependencies.append(IO_FilePath)
        Aliases.reverse()
        Aliases_names = [str(x) for x in Aliases]
        with open(IO_FilePath, 'w+') as (IO_File):
            IO_File.write('# Test vectors for {0} ports\n'.format(self.Name))
            IO_File.write('# 0 means force 0\n')
            IO_File.write('# 1 means force 1\n')
            IO_File.write('# L means expect 0\n')
            IO_File.write('# H means expect 1\n')
            IO_File.write("# X means don't care\n")
            IO_File.write('#' * 50 + '\n')
            NTemplates = []
            Names = []
            for i, Alias in enumerate(Aliases):
                NTemplates.append('{0:' + str(eval(str(Alias.FullSize), ParamVars)) + '}')
                Names.append(NTemplates[(-1)].format(Aliases_names[i]))

            IO_File.write('#Time   ' + '    '.join(Names))
            Template = ''
            for n, S in enumerate(Aliases):
                SSize = eval(str(S.FullSize), ParamVars)
                Template += '{' + '{0}:0'.format(n + 1) + str(SSize) + 'b}' + '    '
                if len(S.Name) > SSize:
                    Template += ' ' * (len(str(S)) - SSize)

            Template = '\n{0:3}     ' + Template
            ClockStim = collections.OrderedDict()
            ClockNames = self.GetClockNames()
            for C in ClockNames:
                ClockStim[C] = 0

            ResetStim = collections.OrderedDict()
            ResetNames = self.GetResetNames()
            for R in ResetNames:
                ResetStim[R] = 1

            TimeStep = int(CycleLength / 2)
            MaxTime = NbCycles * TimeStep * 2
            ResetClockCycles = 32
            TBValues_Renamed = {}
            for Name, Values in TBValues.items():
                Values = [0 for i in range(ResetClockCycles + 4)] + Values
                TBValues_Renamed[str(CommunicationService.Alias) + '_' + Name] = Values

            RisingEdge = True
            OldValues = []
            for t in range(0, MaxTime, TimeStep):
                if 0 in list(ClockStim.values()):
                    RisingEdge = True
                else:
                    RisingEdge = False
                Aliases_val = [
                 t]
                for n, S in enumerate(Aliases):
                    SName = str(S)
                    FullSize = eval(str(S.FullSize), ParamVars)
                    if SName in ClockNames:
                        Aliases_val.append(ClockStim[SName])
                        ClockStim[SName] = 0 if ClockStim[SName] == 1 else 1
                    elif SName in ResetNames:
                        Aliases_val.append(ResetStim[SName])
                        if t > ResetClockCycles:
                            ResetStim[SName] = 0
                    elif 1 in list(ResetStim.values()):
                        Aliases_val.append(0)
                    else:
                        if RisingEdge is True:
                            Value = OldValues[(n + 1)]
                        else:
                            AliasName = str(S)
                            if AliasName in TBValues_Renamed:
                                if len(TBValues_Renamed[AliasName]) > 0:
                                    Value = int(TBValues_Renamed[AliasName].pop(0))
                                else:
                                    Value = 0
                            else:
                                if OldValues[(n + 1)] == 0:
                                    Value = 1
                                else:
                                    Value = 0
                        Aliases_val.append(Value)

                OldValues = Aliases_val[:]
                IO_File.write(Template.format(*Aliases_val))

    def AddOrtho(self, SubServ, SubMod, ReqMap, Constraints, HwConstraints):
        """
                Propagate orthogonal signals upward through the hierarchy
                """
        if SubServ.IsOrthogonal():
            for Formal, ActuaData in ReqMap.items():
                ActualList, Cond, IdxDict = ActuaData
                InstName, SigName, Index = ActualList[0]
                if Formal in SubServ.Params:
                    pass
                else:
                    if SigName not in self.Ports:
                        logging.error("No such port '{0}' in module {1} ports ({2})".format(SigName, self.Name, [x for x in self.Ports]))
                        sys.exit(1)
                    P = self.Ports[SigName]
                    Type, Identifier = SubServ.Name, Constraints
                    if Identifier is None:
                        P.Constraints = (
                         Type, None, Formal)
                    else:
                        Identifier = Identifier.lower()
                        P.Constraints = (Type, Identifier, Formal)
                        if Identifier != 'ignore':
                            continue
                        Port = P.Copy()
                        if SubServ.Shared:
                            Port.Name = SharedName(Formal, SubServ.Params, ReqMap)
                self.OrthoPorts[SigName] = Port

        else:
            for ServID in sorted(SubMod.ReqServ.keys()):
                SubS, RMap, IsOrtho, Constraints = SubMod.ReqServ[ServID]
                SubM = SubS.GetModule(Constraints=HwConstraints)
                if SubM is None:
                    Msg = "[HdlLib.SysGen.Module.AddOrtho] no module associated with service '{0}' in instances of {1} for following constraints:{2}.".format(SubS.Name, SubMod.Name, HwConstraints)
                    logging.error(Msg)
                    raise SyntheSysError(Msg)
                SubMod.AddOrtho(SubS, SubM, RMap, Constraints, HwConstraints)

            for ActualPName, FormalP in SubMod.OrthoPorts.items():
                self.OrthoPorts[FormalP.Name] = FormalP

    def GetMissing(self, Connections, Sig, ParamVars={}):
        """
                Return a dictionary for connection to default of signals missing in Connections.
                Connections={Index0: ActualSig0, Index1: ActualSig1 (...) }
                        or 
                Connections=<Signal>
                """
        if isinstance(Connections, dict):
            Zeros = {}
            for i in range(eval(str(Sig.Size), ParamVars)):
                if not list(Connections.keys()).count(i):
                    Zero = Sig.Copy()
                    Zero.SetIndex(i)
                    Zeros[i] = Zero

            return Zeros
        else:
            return {}

    def CollectPkg(self):
        """
                Update PkgObject package dictionary with this package.
                """
        for Child in [x[0] for x in list(self.ReqServ.values())]:
            if Child != None:
                Child.CollectPkg()
                PackageBuilder.CollectPkg(self, Child)
                self.PkgVars.update(Child.Vars.copy())

        for SName, S in self.Ports.items():
            self.Package['TypeImport'].update(S.GetUsedTypes())

        for SName, S in self.Params.items():
            self.Package['TypeImport'].update(S.GetUsedTypes())

        for SubSize, SubType, Pkg, UsedConst in list(self.Package['TypeImport'].values()):
            for U in UsedConst:
                if U in self.Params:
                    self.Package['Constants'][U] = self.Params[U].HDLFormat()

    def DependencyPkg(self, TypeImport):
        """
                Add dependency package to empty package list. 
                They will be declared empty in top package. 
                The top package declare all type/constants.
                This will prevent error when calling old packages.
                """
        if TypeImport != None:
            PkgType = TypeImport.split('.')
            if len(PkgType) > 1:
                Pkg, NewType = PkgType
                self.Package['EmptyPkg'].append(Pkg)

    def AddXMLReqServ(self, Serv, InstanceName, Mapping=None):
        """
                Fetch service in XML library and return a XML etree
                object of required service child.
                """
        if Serv is None:
            logging.error('[{0}] AddXMLReqServ : No service specified.'.format(self))
            return
        XMLServices = etree.SubElement(self.XMLElmt, 'services')
        ReqElmt = etree.SubElement(XMLServices, 'required', name=Serv.Name, type=Serv.Type, version=Serv.Version, alias=InstanceName)
        if Mapping is not None:
            for Formal, ActualCond in Mapping.items():
                ActualList, ACond, AVars = ActualCond
                InstName, SigName, Index = ActualList[0]
                ActualName = SigName if InstName is None or InstName == '' else '.'.join((InstName, SigName))
                if Index is not None:
                    ActualName += ':{0}'.format(Index)
                MapElmt = etree.SubElement(ReqElmt, 'map', formal=Formal, actual=ActualName)

            self.AddReqServ(Serv.Name, Serv.Type, Serv.Version, Mapping=Mapping, UniqueName=InstanceName, Serv=Serv)
        else:
            self.AddReqServ(Serv.Name, Serv.Type, Serv.Version, Mapping={}, UniqueName=InstanceName, Serv=Serv)
        return XMLServices

    def Connect(self, Interface1, Interface2):
        """
                Map each signal of the first interface to a signal of the other interface.
                Respect the XML format of YANGO (Service.signal).
                """
        if Interface1 == None or Interface2 == None:
            logging.error('[[0]] Nothing to connect.'.format(self))
            return False
        if isinstance(Interface1, list):
            if isinstance(Interface1, list):
                logging.error('Multiple interface connection: not supported.')
            else:
                logging.error('Multiple interface connection: not supported.')
            return True
        if isinstance(Interface1, list):
            if isinstance(Interface1, list):
                logging.error('Multiple interface connection: not supported.')
            else:
                logging.error('Multiple interface connection: not supported.')
            return True
        if not Interface1.IsCompatibleWith(Interface2):
            logging.error("[{0}] Interface '{1}' incompatible with interface '{2}'.".format(self, Interface1, Interface2))
            return False
        for XMLServ in self.XMLElmt.iterchildren('services'):
            for XMLReq in XMLServ.iterchildren('required'):
                if XMLReq.attrib['alias'] == Interface1.Service.Alias:
                    Interface1.Connect(Interface2, XMLReq, Ref=False)
                elif XMLReq.attrib['alias'] == Interface2.Service.Alias:
                    Interface2.Connect(Interface1, XMLReq, Ref=True)

        return True

    def MapSubServices(self, Services, Mappings):
        """
                Instanciate and connect the services RefServ with Services.
                Respect the XML format of YANGO.
                """
        if len(Services) > len(Mappings):
            logging.error('[MapSubServices] Unable to map services ({0}) because not enough mapping ({1}) specified.'.format(len(Services), len(Mappings)))
            logging.error('Mappings:' + str(Mappings[0]))
            sys.exit(1)
        for i, Serv in enumerate(Services):
            Mod = Serv.GetModule()
            ServMapping = collections.OrderedDict()
            MappedSigs = collections.OrderedDict()
            for IndexedName, Map in Mappings[i].items():
                MappedSigs[IndexedName] = IndexedName.split(':')[0]

            ResetNames = Mod.GetResetNames(MappedName=False)
            ClockNames = Mod.GetClockNames(MappedName=False)
            ImplicitSignals = ResetNames + ClockNames
            MappedSigNames = list(MappedSigs.values())
            InvertedOffMap = dict((v, k) for k, v in Mod.ProvidedServMap[Serv.Name].items())
            for PName, P in Mod.Ports.items():
                if PName in ImplicitSignals:
                    pass
                else:
                    if PName in MappedSigNames:
                        pass
                    elif PName not in InvertedOffMap:
                        logging.warning("[{4}] Port signal '{0}' of instance module '{1}' (service '{2}') not mapped to service, and not clock or reset ({3})".format(PName, Mod.Name, Serv.Name, ImplicitSignals, self))
                        continue
                        FormalName = InvertedOffMap[PName]
                        if FormalName in Mod.GetExternalPorts():
                            pass
                        else:
                            ServMapping[FormalName] = (
                             [
                              [
                               Serv.Alias, PName, None]], True, Mod.Vars)

            for IndexedName, Map in Mappings[i].items():
                ServMapping[IndexedName] = Mappings[i][IndexedName]

            XMLServ = self.AddXMLReqServ(Serv, InstanceName=Serv.Alias, Mapping=ServMapping)

        return True

    def SpreadUpward(self, ModInterface, Prefix=''):
        """
                Link interface to port to spread signal upward.
                Respect the XML format of YANGO.
                """
        if ModInterface == None:
            logging.error('[[0]] Nothing to spread upward.'.format(self))
            return False
        IntSignals = None
        for XMLServ in self.XMLElmt.iterchildren('services'):
            for XMLReq in XMLServ.iterchildren('required'):
                if XMLReq.attrib['alias'] == ModInterface.Service.Alias:
                    IntSignals = ModInterface.Connect(None, XMLReq, Ref=True)

        if IntSignals == None:
            logging.error("Cannot find XML element for required service '{0}'.".format(ModInterface.Service.Alias))
            return False
        for Port in IntSignals:
            if Port.Type.lower().find('std_logic') != -1:
                TYPE = 'logic'
            else:
                if Port.Type.lower().find('integer') != -1:
                    TYPE = 'numeric'
                else:
                    if Port.Type.lower().find('natural') != -1:
                        TYPE = 'numeric'
                    else:
                        TYPE = Port.Type
            if Port.Direction == 'IN':
                etree.SubElement(self.XMLElmt, 'input', name=Prefix + Port.Name, size=str(eval(str(Port.Size), ModInterface.Service.Vars)), type=TYPE, default='')
            else:
                etree.SubElement(self.XMLElmt, 'output', name=Prefix + Port.Name, size=str(eval(str(Port.Size), ModInterface.Service.Vars)), type=TYPE, default='')

        return True

    def WrapForClocking(self, HwModel, ClockManagerDict, Library):
        """
                Generate a wrapper with clock management.
                """
        WrapperName = self.Name + '_{0}'.format(HwModel.Name)
        Mapping, StimuliList, TracesList, ClocksList, ResetList = DefaultMapping(self)
        Vars = {}
        Mapping = collections.OrderedDict()
        for PName in self.Params:
            Mapping[PName] = (
             [
              [
               None, PName, None]], True, Vars)

        for PName in self.Ports:
            Mapping[PName] = (
             [
              [
               None, PName, None]], True, Vars)

        if self.IsAbstract():
            for PName, P in self.OrthoPorts.items():
                Mapping[P.Name] = (
                 [
                  [
                   None, P.Name, None]], True, Vars)

        Infos = {'Name': self.Name, 
         'Type': '', 
         'Version': '', 
         'Category': ''}
        ModServ = LibEditor.ProvidedServiceXml(self, Interfaces=[], Infos=Infos, OutputPath=None)
        Infos = {'Name': WrapperName, 
         'Version': '', 
         'Title': '{0} wrapper for {1}.'.format(HwModel.Name, self.Name), 
         'Purpose': 'Add clock management for {1} instanciation on {0}.'.format(HwModel.Name, self.Name), 
         'Desc': '', 
         'Tool': '', 
         'Area': '', 
         'Speed': '', 
         'Issues': ''}
        Mappings = [
         Mapping]
        NewServices = [ModServ]
        NewPorts = {P.Name:P for PName, P in self.Ports.items()}
        if self.IsAbstract():
            NewPorts.update({P.Name:P for PName, P in self.OrthoPorts.items()})
        NewClockSigs = {}
        for Sig, (TargetFrequency, Diff, Nets) in ClockManagerDict.items():
            for PName, P in self.OrthoPorts.items():
                if PName == Sig.Name:
                    if PName in NewPorts:
                        del NewPorts[PName]
                        break
                    else:
                        logging.warning("[WrapForClocking] Cannot remove the '{0}' signal from ports of module '{1}': no such port.".format(PName, self.Name))

            for Net, (Pad, IOStandard, Voltage, Freq, DiffPair) in Nets:
                S = Signal(Net, Dir='IN', Size=1, Type='logic')
                NewPorts[Net] = S
                NewClockSigs[Net] = S

            if len(Nets) == 2:
                ClockMapping = {'clock_in1_p': ([[None, Nets[0][0], None]], True, Vars), 'clock_in1_n': ([[None, Nets[1][0], None]], True, Vars), 'clock_out1': ([['ClockManager21', Sig.Name, None]], True, Vars)}
                ClockManagerServName = 'ClockManager21'
            else:
                ClockMapping = {'clock_in1': ([[None, Nets[0][0], None]], True, Vars), 'clock_out1': ([['ClockManager21', Sig.Name, None]], True, Vars)}
                ClockManagerServName = 'ClockManager11'
            Mapping[Sig.Name] = (
             [
              [
               'ClockManager21', Sig.Name, None]], True, Vars)
            ClockManagerServ = Library.Service(ClockManagerServName)
            if ClockManagerServ is None:
                logging.error("[SyntheSys.HdlLib.SysGen.Module.WrapForClocking] No such service '{0}'".format(ClockManagerServName))
                return
            Mappings.append(ClockMapping)
            NewServices.append(ClockManagerServ)

        Ports = [P.HDLFormat() for P in NewPorts.values()]
        Params = [P.HDLFormat() for P in self.Params.values()]
        ModuleWrapper = LibEditor.NewModule(Infos=Infos, Params=Params, Ports=Ports, Clocks=list(NewClockSigs.keys()), Resets=[], Sources=[])
        XMLElmt = ModuleWrapper.UpdateXML()
        ModuleWrapper.Reload()
        ModuleWrapper.MapSubServices(Services=NewServices, Mappings=Mappings)
        ModuleWrapper.IdentifyServices(NewServices)
        for P, PPath in self.Dependencies['package'].items():
            if P not in ModuleWrapper.Dependencies['package']:
                ModuleWrapper.Dependencies['package'][P] = PPath

        ModuleWrapper.NoOrthoPorts = True
        return (ModuleWrapper, NewClockSigs)

    def UpdateResources(self, FpgaId, HWRsc):
        """
                Edit XML file with specified resources.
                """
        self.Resources[FpgaId] = HWRsc
        RscDict = HWRsc.GetResourcesDict()
        FeaturesElmt_Found = None
        FpgaElmt_Found = None
        for FeaturesElmt in self.XMLElmt.iterchildren('features'):
            FpgaElmt_Found = FeaturesElmt_Found
            for FpgaElmt in FeaturesElmt.iterchildren('fpga'):
                if FpgaElmt.get('id') == FpgaId:
                    FpgaElmt_Found = FpgaElmt
                    for RscElmt in FpgaElmt.iterchildren('resources'):
                        for Item in ('lut', 'ram', 'register'):
                            RscType = Item.upper()
                            if RscType in RscDict:
                                RscElmt.attrib[Item] = str(RscDict[RscType][0])
                            else:
                                RscElmt.attrib[Item] = '0'
                                logging.debug('Given resources: {0}'.format(RscDict))
                                logging.warning("[UpdateResources] No information about '{0}' resource : set to '0'.".format(RscType))

                    return True

        if FpgaElmt_Found is None:
            if FeaturesElmt_Found is None:
                FeaturesElmt_Found = etree.SubElement(self.XMLElmt, 'features')
            FpgaElmt_Found = etree.SubElement(FeaturesElmt_Found, 'fpga')
        FpgaElmt_Found.attrib['id'] = FpgaId
        RscElmt = etree.SubElement(FpgaElmt_Found, 'resources')
        for Item in ('lut', 'ram', 'register'):
            RscType = Item.upper()
            if RscType in RscDict:
                RscElmt.attrib[Item] = str(RscDict[RscType][0])
            else:
                RscElmt.attrib[Item] = '0'
                logging.debug('Given resources: {0}'.format(RscDict))
                logging.warning("[UpdateResources] No information about '{0}' resource : set to '0'.".format(Item))

        return True

    def Display(self):
        """
                Display service parameters in log.
                """
        print('MODULE:')
        print("\tname='{0}', Version='{1}'".format(self.Name, self.Version))
        print('\tTitle   =' + self.Title + '(Speed={0}, Area={1}, Tool={2}, Issues={3})'.format(self.Speed, self.Area, self.Tool, self.Issues))
        print('\tPurpose =' + self.Purpose)
        print('\tDesc    =' + self.Desc)
        print('\tParameters =' + str([str(i) for i in self.Params.values()]))
        print('\tPorts      =' + str([str(i) for i in self.Ports.values()]))
        print('\tServices implemented =' + str(list(self.ProvidedServ.keys())))
        ReqVal = [x.split('#')[(-1)] for x in [x for x in list(self.ReqServ.keys()) if self.ReqServ[x][0] != None]]
        print('\tServices required    =' + str(ReqVal))
        print('\tSources:')
        for Type in list(self.Sources.keys()):
            print('\t\t*{0}'.format(Type))
            for S in self.Sources[Type]:
                print('\t\t\t{0}'.format(S))

        print('\tResources =' + str(self.Resources))

    def __repr__(self):
        """
                Return module minimal info.
                """
        return 'HdlLib.SysGen.Module(XMLElmt={0}, FilePath={1})'.format(repr(self.XMLElmt), repr(self.XmlFilePath))

    def __str__(self):
        """
                Return module name.
                """
        return self.Name

    def ID(self):
        """
                Return module unique ID.
                """
        return self.Name + "'" + str(Module.Instances.index(self))


def ServName(Code, Vars={}):
    """
        Parse required service name and return normalized name format.
        """
    ServID = Code.split(':')
    if ServID[0] == '':
        ServID[0] = Code
    if len(ServID) > 1:
        for i in range(1, len(ServID)):
            ServID[i] = ServID[i] + str(eval(ServID[i], Vars))

        InstanceName = '_'.join([ServID[0], ''.join(ServID[1:])])
    else:
        InstanceName = ServID[0]
    return InstanceName


def RemoveDuplicated(SignalList):
    """
        Build a new list and fill it with a set of unique signals from argument list.
        """
    SignalSet = []
    SignalNameSet = []
    for Sig in SignalList:
        if str(Sig) not in SignalNameSet:
            SignalSet.append(Sig)
            SignalNameSet.append(str(Sig))

    return SignalSet


def GetInternalSigFrom(Sig, FIndex=None, AIndex=None, WithName=None, Mod=None, IntSigs={}):
    """
        return a signal copied from Sig with "WithName" and indexed with "AIndex".
        """
    ActualSignal = Sig.Copy()
    if AIndex is None and FIndex is not None:
        ActualSignal = ActualSignal[eval(FIndex, Sig.GetUsedParam())]
    if WithName is None:
        WithName = Sig.GetName()
    ActualSignal.SetName(WithName)
    ActualSignal.SetIndex(AIndex)
    HDLActual = ActualSignal.HDLFormat()
    if WithName not in IntSigs:
        try:
            eval(WithName)
        except:
            IntSigs[WithName] = HDLActual

    return HDLActual


def IndirectConnection(InterSigName, InterSigIndex, FormalSig, HDLActual, Connections=[], IntSigs={}, Vars={}):
    """
        Connect formal and actual through an intermediate signal.
        """
    if InterSigName in IntSigs:
        InterSig = IntSigs[InterSigName]
    else:
        InterSig = FormalSig.HDLFormat()
        InterSig.InverseDirection()
        InterSig.Name = InterSigName
        IntSigs[InterSigName] = InterSig
    if InterSigIndex is None:
        Connections[InterSig] = HDLActual
    else:
        if InterSig not in Connections:
            IndexDict = {}
            Connections[InterSig] = IndexDict
        else:
            IndexDict = Connections[InterSig]
        IndexVal = eval(InterSigIndex, Vars.copy())
        IndexDict[IndexVal] = HDLActual
    return InterSig


def DefaultMapping(Mod):
    """
        return default mapping.
        """
    Mapping = collections.OrderedDict()
    StimuliList = []
    TracesList = []
    ClockNames = Mod.GetClockNames(MappedName=False)
    ResetNames = Mod.GetResetNames()
    for N, P in Mod.GetExternalPorts().items():
        if N not in ClockNames:
            if P.Direction == 'IN':
                S = P.Copy(WithName=N)
                StimuliList.append(S)
            if P.Direction == 'OUT':
                S = P.Copy(WithName=N)
                TracesList.append(S)

    ClocksList = [Signal(x, Size=1, Dir='IN') for x in ClockNames]
    ResetList = [Signal(x, Size=1, Dir='IN') for x in ResetNames]
    InIndex = OutIndex = 95
    for S in StimuliList:
        Size = S.GetSize()
        if Size != 1:
            Idx = slice(InIndex + 1, InIndex + 1 - Size, -1)
        else:
            Idx = InIndex
        Mapping[S.GetName()] = (
         [
          [
           None, 'Inputs', Idx]], True, {})
        InIndex -= Size

    for T in TracesList:
        Size = T.GetSize()
        if Size != 1:
            Idx = slice(OutIndex + 1, OutIndex + 1 - Size, -1)
        else:
            Idx = OutIndex
        Mapping[T.GetName()] = (
         [
          [
           None, 'Outputs', Idx]], True, {})
        OutIndex -= Size

    if len(ClocksList):
        Mapping[ClocksList[0].GetName()] = (
         [
          [
           None, 'Clk', None]], True, {})
    Params = [P for N, P in Mod.Params.items()]
    for P in Params:
        Mapping[P.GetName()] = (
         [
          [
           None, str(P.GetDefaultValue()), None]], True, {})

    return (Mapping, StimuliList, TracesList, ClocksList, ResetList)


def CopyModule(Mod):
    """
        return copies of module and its provided service.
        This is needed to avoid issues with orthoports that are propagated throught the DUT wrapper.
        """
    Infos = {}
    Infos = {'Name': Mod.Name, 
     'Version': '', 
     'Title': 'Copy of {0} to be verified.'.format(Mod.Name), 
     'Purpose': 'DEVICE UNDER TEST module.', 
     'Desc': '', 
     'Tool': '', 
     'Area': '', 
     'Speed': '', 
     'Issues': ''}
    Mapping, StimuliList, TracesList, ClocksList, ResetList = DefaultMapping(Mod)
    Ports = StimuliList + TracesList + ClocksList + ResetList
    Params = [P for N, P in Mod.Params.items()]
    CopyMod = LibEditor.NewModule(Infos=Infos, Params=Params, Ports=Ports, Clocks=[], Resets=[], Sources=[])
    Infos = {'Name': Mod.Name, 
     'Type': '', 
     'Version': '', 
     'Category': ''}
    CopyServ = LibEditor.ProvidedServiceXml(Mod=CopyMod, Interfaces=[], Infos=Infos)
    CopyServ.Alias = Mod.Name + '_DUT'
    return (
     CopyMod, CopyServ, Mapping, StimuliList, TracesList, ClocksList)


def GenerateEmptyWrapper(Mod=None, CopyMod=False):
    """
        Generate new abstract module instantiating specified module.
        Mapping is default.
        """
    logging.debug('Wrap module for verifying')
    if Mod is None:
        logging.error('[SyntheSys.HdlLib.SysGen.Module.GenerateEmptyWrapper] No Module specified. Aborted.')
        return
    if CopyMod is True:
        CopyMod, CopyServ, Mapping, StimuliList, TracesList, ClocksList = CopyModule(Mod)
    else:
        Mapping, StimuliList, TracesList, ClocksList, ResetList = DefaultMapping(Mod)
        CopyMod = Mod
        Infos = {'Name': Mod.Name, 
         'Type': '', 
         'Version': '', 
         'Category': ''}
        CopyServ = LibEditor.ProvidedServiceXml(Mod, Interfaces=[], Infos=Infos, OutputPath=None)
    Infos = {'Name': 'NoC', 
     'Version': '', 
     'Title': 'Empty wrapper for {0} to be verified.'.format(Mod.Name), 
     'Purpose': 'DEVICE UNDER TEST module for resource estimation.', 
     'Desc': '', 
     'Tool': '', 
     'Area': '', 
     'Speed': '', 
     'Issues': ''}
    Ports = []
    DUTMod = LibEditor.NewModule(Infos=Infos, Params=[], Ports=Ports, Clocks=[], Resets=[], Sources=[])
    DUTMod.UpdateXML()
    DUTMod.IdentifyServices([CopyServ])
    SubServices = [
     CopyServ]
    Mappings = [Mapping]
    DUTMod.MapSubServices(Services=SubServices, Mappings=Mappings)
    XMLElmt = DUTMod.UpdateXML()
    DUTMod.Reload()
    DUTMod.IdentifyServices([CopyServ])
    return DUTMod


def SharedName(Formal, Params, ReqMap):
    """
        Build a signal name for share orthogonal signals.
        """
    BaseName = Formal
    for PName in sorted(Params):
        if PName in ReqMap:
            ActualList, Cond, IdxDict = ReqMap[PName]
            InstName, SigName, Index = ActualList[0]
            BaseName += '_' + SigName

    return BaseName