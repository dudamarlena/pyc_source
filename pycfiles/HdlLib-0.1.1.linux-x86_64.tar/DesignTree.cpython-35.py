# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/HdlLib/Utilities/DesignTree.py
# Compiled at: 2017-07-08 08:29:58
# Size of source mod 2**32: 16137 bytes
import os, sys, re, logging, io
PYTHON_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
from HdlLib.Utilities.ExtensionSilence import ExtensionSilence

class Design:

    def __init__(self, FileList=[]):
        logging.debug('New design with these files: {0}'.format(FileList))
        self.VerilogList = list(filter(IsVerilog, FileList))
        self.VHDLList = list(filter(IsVHDL, FileList))
        self.TopComponentList = []
        self.ComponentList = []
        self.ParserMsg = ''
        self.GetComponentList(self.VHDLList)
        try:
            with open('./ADACSYS_PARSER_STDOUT.txt', 'r') as (StdOutFile):
                self.ParserMsg = StdOutFile.read()
            os.remove('./ADACSYS_PARSER_STDOUT.txt')
            os.remove('./ADACSYS_PARSER_STDERR.txt')
        except:
            pass

        self.BuildDesign()
        self.BuildPathNames()
        if len(self.TopComponentList):
            self.TopComponentList[0].IsSelected = True

    def GetComponentList(self, FileList):
        """
                Build a list component object with help of Parser C++ module.
                """
        self.ComponentList = []
        print(Parser.__file__)
        DataBase = Parser.GuiInterface()
        for FilePath in FileList:
            DataBase.resetParse()
            if re.match('.*\\.(vhd)', FilePath):
                logging.info("Parse file '{0}'.".format(FilePath))
                if sys.platform.startswith('win'):
                    if DataBase.singleFileParse(FilePath, 'work'):
                        break
                else:
                    with ExtensionSilence(stdout='./ADACSYS_PARSER_STDOUT.txt', stderr='./ADACSYS_PARSER_STDERR.txt', mode='wb'):
                        if DataBase.singleFileParse(FilePath, 'work'):
                            break
                logging.debug('Parse succeeded.')

        EntityList = Parser.StringVector()
        DataBase.getEntityList(EntityList)
        for i in range(len(EntityList)):
            EntityName = EntityList[i]
            self.ComponentList.append(Component(EntityName, DataBase=DataBase, FilePath=FilePath))

        return True

    def BuildDesign(self):
        """
                Connect the components to each others according to their entity name.
                """
        logging.debug('Connect the components to each others according to their entity name')
        CompLeft = self.ComponentList[:]
        while CompLeft != []:
            MyComponent = CompLeft.pop()
            for MissingInstance in MyComponent.MissingInstanceList:
                for Comp in self.ComponentList:
                    if Comp.EntityName == MissingInstance.EntityName:
                        Comp.AddParent(MyComponent, MissingInstance.InstanceName)
                        break

        for Component in self.ComponentList:
            if Component.IsTop:
                self.TopComponentList.append(Component)
            for MissingInstance in Component.MissingInstanceList:
                Found = False
                for FullInstance in Component.InstanceList:
                    if FullInstance.EntityName == MissingInstance.EntityName:
                        Found = True

                if Found == False:
                    MissingInstance.IsTop = False
                    Component.InstanceList.append(MissingInstance)

            Component.MissingInstanceList = []

    def GetComponent(self, EntityName=''):
        """
                Seach entity in component list and return it.
                """
        if EntityName == '':
            return
        for Component in self.ComponentList:
            if Component.EntityName == EntityName:
                return Component

    def GetComponentInstance(self, DUTInstanceName):
        """
                Seach instance in component list and return it.
                """
        for C in self.ComponentList:
            if C.InstanceName == DUTInstanceName:
                return C

    def BuildPathNames(self):
        """
                Build path name of every signal in every component.
                """
        for Component in self.ComponentList:
            CurComponent = Component
            while CurComponent != None:
                if not CurComponent.IsTop:
                    for Port in Component.PortList:
                        Port.AddPath(CurComponent.InstanceName)

                    for IntSig in Component.IntSigList:
                        IntSig.AddPath(CurComponent.InstanceName)

                    CurComponent = CurComponent.GetParent()
                else:
                    break


class Component:

    def __init__(self, TopEntityName=None, InstanceName=None, ArchiName=None, DataBase=None, Parent=None, FilePath=None):
        if TopEntityName == None:
            raise NameError('[Design.__init__] - Nothing to parse')
        self.IsTop = True
        self.IsSelected = False
        self.Parent = Parent
        self.DataBase = DataBase
        self.EntityName = TopEntityName
        self.InstanceName = '' if InstanceName == None else InstanceName
        self.FilePath = FilePath
        self.InstanceList = []
        if self.DataBase != None:
            DataBase.setTop(self.EntityName)
            self.IsMissing = False
            self.ArchiName = ArchiName
            self.PortList = self.GetPorts()
            self.IntSigList = self.GetIntSigs()
            self.MissingInstanceList = self.GetMissingInstances()
            self.ConstList = []
        else:
            self.IsMissing = True
            self.ArchiName = None
            self.PortList = []
            self.IntSigList = []
            self.MissingInstanceList = []
            self.ConstList = []

    def GetGenerics(self):
        """
                Return a list of generics declared in the component entity.
                """
        logging.debug('List generics available for this component')
        Generics = {}
        return Generics

    def GetPorts(self):
        """
                Return a list of ports of this component entity.
                """
        logging.debug('List ports available for this component')
        Ports = Parser.SignalVector()
        PortList = []
        if not self.DataBase.getPorts('', Ports):
            for i in range(len(Ports)):
                Port = Ports[i]
                PortList.append(Signal(Name=Port.getName(), IO=Port.getIO(), Type=Port.getType(), Size=Port.getSize(), IsInstru=Port.getInstrumentable()))

        else:
            logging.error("Error looking for entity '" + self.EntityName + "' to get ports.")
        return PortList

    def GetIntSigs(self):
        """
                Return a list of internal signals of this component entity.
                """
        logging.debug('List internal signals available for this component')
        IntSigs = Parser.SignalVector()
        IntSigList = []
        if not self.DataBase.getInternalSignals('', IntSigs):
            for i in range(len(IntSigs)):
                IntSig = IntSigs[i]
                IntSigList.append(Signal(Name=IntSig.getName(), Type=IntSig.getType(), Size=IntSig.getSize(), IsInstru=IntSig.getInstrumentable()))

        else:
            logging.error("Error looking for model of entity '" + self.EntityName + "' and archi '" + self.ArchiName + "' to get internal sigs.")
        return IntSigList

    def GetMissingInstances(self):
        """
                Return a list of instances of this component that source file are not found.
                """
        logging.debug('List instances without source')
        Instances = Parser.ComponentVector()
        InstanceList = []
        if self.DataBase.getInstances('', Instances):
            logging.error('Unable to get list of instance of {0}.'.format(' '.join([self.EntityName])))
            return []
        for i in range(len(Instances)):
            Instance = Instances[i]
            InstanceList.append(Component(TopEntityName=Instance.getEntityName(), InstanceName=Instance.getInstanceName(), ArchiName=Instance.getArchitectureName(), DataBase=None))

        return InstanceList

    def GetParent(self):
        """
                Return a component parent in its hierarchy.
                """
        return self.Parent

    def AddParent(self, ParentComponent, InstanceName):
        """
                Set this component as a child of its parent.
                Tag it as not a TOP any more if it was, and give it a instance name.
                """
        ParentComponent.InstanceList.append(self)
        self.IsTop = False
        self.InstanceName = InstanceName
        self.Parent = ParentComponent

    def GetSources(self):
        """
                Return a list of HDL source paths in a dependancy order (last=top).
                """
        SourceList = []
        for Instance in self.InstanceList:
            SourceList += Instance.GetSources()

        if self.FilePath:
            SourceList.append(self.FilePath)
        return SourceList

    def __str__(self):
        CompString = "* Entity:'" + str(self.EntityName) + "'\n"
        CompString += "* Architecture:'" + str(self.ArchiName) + "'\n"
        CompString += "* InstanceName:'" + str(self.InstanceName) + "'\n"
        CompString += "* PortList:'" + str(self.PortList) + "'\n"
        CompString += "* IntSigList:'" + str(self.IntSigList) + "'\n"
        CompString += "* ConstList:'" + str(self.ConstList) + "'\n"
        return CompString


class Signal:
    __doc__ = 'Contains all the features that are part of a signal'

    def __init__(self, Name='Unkown_signal', IO=None, Type=[], Size=None, IsInstru=False):
        self.Name = Name
        self.IO = IO.upper() if isinstance(IO, str) else None
        self.Type = Type
        self.Size = Size
        self.IsInstru = IsInstru
        if self.Size > 1:
            self.PathName = self.Name + '(' + str(self.Size - 1) + ':0)'
        else:
            self.PathName = self.Name

    def AddPath(self, Path):
        self.PathName = Path + ' ' + self.PathName
        self.PathName = self.PathName.strip()

    def __repr__(self):
        return self.PathName

    def __str__(self):
        return self.PathName


def IsVerilog(FilePath):
    if re.match('.*\\.v$', FilePath):
        return True
    return False


def IsVHDL(FilePath):
    if re.match('.*\\.vhd$', FilePath):
        return True
    return False


if __name__ == '__main__':
    from HdlLib.Utilities import ColoredLogging
    ColoredLogging.SetActive(True)
    from HdlLib.Utilities import ConsoleInterface
    ConsoleInterface.ConfigLogging(Version='1.0', ModuleName='pySystems')
    FileList = [
     '../../IP/calculus8bit/src/add4bit.vhd', '../../IP/calculus8bit/src/calculus4bit.vhd', '../../IP/calculus8bit/src/mux4bit.vhd', '../../IP/calculus8bit/src/shift4bit.vhd', '../../IP/calculus8bit/src/sub4bit.vhd']
    D = Design(FileList)