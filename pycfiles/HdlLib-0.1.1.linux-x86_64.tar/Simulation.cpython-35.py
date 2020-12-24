# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/HdlLib/SysGen/Simulation.py
# Compiled at: 2017-07-08 08:29:58
# Size of source mod 2**32: 26725 bytes
import sys, os, logging, re, shutil
from HdlLib.Utilities.Timer import TimeStamp
from HdlLib.Utilities import SafeRun
from HdlLib.SysGen.Module import Instance
from HdlLib.Utilities.RemoteOperations import RemoteOperations
from HdlLib.Utilities.UserConfig import UserConfig
from HdlLib.Utilities import Misc
from HdlLib.Utilities.Misc import cd as Localcd

class Simulation(RemoteOperations):
    __doc__ = '\n\tObject that represent a simulation.\n\tIt allows to configure/run simulation and fetch results.\n\t'

    def __init__(self, Module, ModInstance, OutputPath='./Simulation', RemoteHost=None):
        """
                Configure a new simulation environment.
                """
        RemoteOperations.__init__(self, RemoteSubFolder='Simulation')
        if not os.path.isdir(str(OutputPath)):
            logging.error("Unable to generate files for application: no such output directory '{0}'.".format(str(OutputPath)))
            return
        self.LocalSimuPath = os.path.abspath(OutputPath)
        self.Module = Module
        DepDict = Module.GetDependencies()
        self.DUT = Module.TB_DUT
        self.Packages = DepDict['package']
        self.Libraries = DepDict['library']
        self.TBName, self.TBSource, self.DependencyFiles = Module.GetTestBenchInfo()
        self.ModuleInstance = Instance(Name=self.TBName, Mod=None)
        self.ModuleInstance.AddInstanceAsInstance(Inst=ModInstance)
        self.SrcList = Module.Sources['RTL'] + Module.Sources['Behavioral']
        if len(self.SrcList) == 0:
            logging.error("No sources found in module '{0}'".format(Module))

    def SetRemoteHost(self, RemoteHost, PromptID=False, Config=None):
        """
                [OVERLOADED] Set Remote host.
                """
        RemoteOperations.SetRemoteHost(self, RemoteHost, PromptID=PromptID, Config=Config)

    def Run(self, Simulator='gHDL', ModuleList=[], InstanceList=[], SignalDepth=999999, NbCycles=1600, CycleLength=10):
        """
                Launch simulation with specified simulator. 
                """
        logging.info('----------------------------------')
        logging.info("Simulation path: '{0}'".format(self.LocalSimuPath))
        logging.info("Simulator      : '{0}'".format(Simulator))
        logging.info('----------------------------------')
        Simulator = Simulator.lower()
        if Simulator == 'myhdl':
            logging.error('myhdl simulation not supported yet. aborted.')
            return
            Simulate_myHDL()
        else:
            if Simulator == 'ghdl':
                SimuScriptPath = os.path.join(self.LocalSimuPath, 'SimulationScript_{0}_{1}.txt'.format(self.TBName, Simulator))
                with open(SimuScriptPath, 'w+') as (SimuScript):
                    SimuScript.write('\n# Analyze, elaborate and build an exe from the top level entity')
                    for FilePath in self.Libraries:
                        AbsFilePath = os.path.abspath(FilePath)
                        SimuScript.write('\nghdl -i {0}'.format(AbsFilePath))

                    for FilePath in self.Packages:
                        AbsFilePath = os.path.abspath(FilePath)
                        SimuScript.write('\nghdl -i {0}'.format(AbsFilePath))

                    for FilePath in self.SrcList:
                        AbsFilePath = os.path.abspath(FilePath)
                        SimuScript.write('\nghdl -i {0}'.format(AbsFilePath))

                    SimuScript.write('\nghdl -m --ieee=synopsys --ieee=mentor -fexplicit {0}'.format(self.TBName.lower()))
                    SimuScript.write('\n# Run the simulation and output a wave file')
                    WaveformFilePath = '{0}.vcd'.format(self.TBName)
                    SimuScript.write('\nghdl -r {0} --vcd={1}'.format(self.TBName.lower(), WaveformFilePath))
                    SimuScript.write('\n# Display VCD thanks to Gtkwave application.')
                    SimuScript.write('\ngtkwave ./{0}'.format(WaveformFilePath))
                if self.RemoteHost:
                    logging.error('Remote simulation with gHDL not supported yet.')
                else:
                    for FilePath in self.DependencyFiles:
                        AbsFilePath = os.path.abspath(FilePath)
                        shutil.copy(AbsFilePath, self.LocalSimuPath)

                    logging.debug("SimuScriptPath: '{0}'".format(SimuScriptPath))
                    with Localcd(self.LocalSimuPath):
                        if not SafeRun.SafeRun(not sys.platform.startswith('win'), [SimuScriptPath]):
                            logging.info('Simulation script execution success.')
                            return (
                             WaveformFilePath, WaveformFilePath)
                        else:
                            return
                return
            if Simulator in ('modelsim', 'questasim'):
                Conf = UserConfig()
                SetupScriptPath = Conf.GetValue(Sec='Simulation', Opt='SourceScript_Modelsim', Host=self.RemoteHost)
        if self.RemoteHost is None:
            if not os.path.isfile(SetupScriptPath):
                logging.error("No such source script '{0}'. Simulation aborted.".format(SetupScriptPath))
                return
            if not os.access(SetupScriptPath, os.R_OK):
                logging.error("You do not have the execution right access on script '{0}'. Simulation aborted.".format(SetupScriptPath))
                return
            SimuScriptPath = os.path.join(self.LocalSimuPath, 'SimulationScript_{0}_{1}.run'.format(self.TBName, Simulator))
            with open(SimuScriptPath, 'w+') as (SimuScript):
                SimuScript.write('\n# MODULES COMPILATION')
                SimuScript.write('\nsource "{SETUP_SCRIPT}" && vlib ./work'.format(SETUP_SCRIPT=SetupScriptPath))
                SimuScript.write('\nsource "{SETUP_SCRIPT}" && vmap work ./work'.format(SETUP_SCRIPT=SetupScriptPath))
                for FilePath in self.SrcList:
                    AbsFilePath = os.path.abspath(FilePath)
                    if self.RemoteHost is None:
                        SrcPath = AbsFilePath
                    else:
                        SrcPath = '/'.join(['./src', os.path.basename(FilePath)])
                    if FilePath.endswith('.vhd'):
                        SimuScript.write('\nsource "{SETUP_SCRIPT}" && vcom -work work "{SRC_PATH}"'.format(SRC_PATH=SrcPath, SETUP_SCRIPT=SetupScriptPath))
                    else:
                        if FilePath.endswith('.v'):
                            SimuScript.write('\nsource "{SETUP_SCRIPT}" && vlog -work work "{SRC_PATH}"'.format(SRC_PATH=SrcPath, SETUP_SCRIPT=SetupScriptPath))
                        else:
                            logging.error("Source format not recognized ('{0}')".format(AbsFilePath))

                SimuScript.write('\n\n# COMPILE THE PROJECT TESTBENCH')
                SimuScript.write("\nsource '{SETUP_SCRIPT}' && vsim -gui work.{TB}".format(TB=self.TBName, SETUP_SCRIPT=SetupScriptPath))
            logging.debug("SimuScriptPath: '{0}'".format(SimuScriptPath))
            if self.RemoteHost is None:
                for FilePath in self.DependencyFiles:
                    AbsFilePath = os.path.abspath(FilePath)
                    shutil.copy(AbsFilePath, self.LocalSimuPath)

                with Localcd(self.LocalSimuPath):
                    if not SafeRun.SafeRun(not sys.platform.startswith('win'), [SimuScriptPath]):
                        logging.info('Simulation script execution success.')
                        return ('', '')
                    else:
                        return
            else:
                SimulationPath = 'Simulation/{0}_Simulation_{1}'.format(self.TBName, TimeStamp())
                TargetSrcDirectory = '/'.join([SimulationPath, 'src'])
                DirList = [
                 TargetSrcDirectory]
                SetupFileDict = {SimuScriptPath: os.path.basename(SimuScriptPath)}
                SrcDict = {}
                for S in self.SrcList:
                    SrcDict[S] = os.path.basename(S)

                for FilePath in self.DependencyFiles:
                    SetupFileDict[os.path.abspath(FilePath)] = os.path.basename(FilePath)

                if self.CreateHostDir(DirList=DirList) is False:
                    return
                else:
                    if self.SendPathsRelative(FileDict=SetupFileDict, HostAbsPath=SimulationPath) is False:
                        return
                    if self.SendPathsRelative(FileDict=SrcDict, HostAbsPath=TargetSrcDirectory) is False:
                        return
                    RemoteSimuScriptPath = '/'.join([SimulationPath, os.path.basename(SimuScriptPath)])
                    Success = self.RemoteRun(Command='chmod 777 {SimuScript}'.format(SimuScript=RemoteSimuScriptPath), ScriptsToSource=[], abort_on_prompts='True', warn_only=True)
                    Success = self.RemoteRun(Command='./{SynthesisScript}'.format(SynthesisScript=os.path.basename(RemoteSimuScriptPath)), ScriptsToSource=[
                     SetupScriptPath], FromDirectory=SimulationPath, abort_on_prompts='True', warn_only=True, XForwarding=True)
                    if Success:
                        logging.info('Simulation success.')
                        self.RemoteRun(Command='rm -rf {SimulationPath}'.format(SimulationPath=SimulationPath), abort_on_prompts='True', warn_only=True)
                        return []
                    self.RemoteRun(Command='rm -rf {SimulationPath}'.format(SimulationPath=SimulationPath), abort_on_prompts='True', warn_only=True)
                    logging.info('Simulation failure.')
                    return
        elif Simulator == 'isim':
            Conf = UserConfig()
            SetupScriptPath = Conf.GetValue(Sec='Simulation', Opt='SourceScript_Isim', Host=self.RemoteHost)
        if self.RemoteHost is None:
            if not os.path.isfile(SetupScriptPath):
                logging.error("No such source script '{0}'. Simulation aborted.".format(SetupScriptPath))
                return
            if not os.access(SetupScriptPath, os.R_OK):
                logging.error("You do not have the execution right access on script '{0}'. Simulation aborted.".format(SetupScriptPath))
                return
            TCLFilePath = os.path.join(self.LocalSimuPath, 'TCLScript_{0}'.format(self.TBName))
            CombinedMod = '(' + ')|('.join(ModuleList) + ')'
            CombinedInst = '(' + ')|('.join(InstanceList) + ')'
            with open(TCLFilePath, 'w+') as (TCLScript):
                TCLScript.write("\n# TCL Script for TB '{0}'".format(self.TBName))
                TCLScript.write('\n# Shows current scope in design hierarchy.')
                TCLScript.write('\nscope')
                Instances = []
                for Inst, Path in self.ModuleInstance.WalkInstances(Depth=SignalDepth):
                    if len(InstanceList) > 0:
                        if Inst.Mod is None:
                            pass
                        else:
                            for I in InstanceList:
                                ReqPath = I.split('/')
                                if ReqPath == Path + [Inst.Name] and (
                                 Inst, Path) not in Instances:
                                    Instances.append((Inst, Path))
                                    continue

                        if len(ModuleList) > 0:
                            if Inst.Mod is None:
                                pass
                            else:
                                if re.match(CombinedMod, Inst.Mod.Name):
                                    Instances.append((Inst, Path))
                                continue

                if (len(InstanceList) != 0 or len(ModuleList) != 0) and len(Instances) == 0:
                    ErrorMsg = 'No instance or entity {0} found for chronogram display.'.format(InstanceList + ModuleList)
                    logging.error(ErrorMsg)
                    logging.error('Available:')
                    for Inst, Path in self.ModuleInstance.WalkInstances(Depth=SignalDepth):
                        logging.error('/'.join(Path + [str(Inst)]))

                    AskAgain = True
                    while AskAgain:
                        Answer = input('Force visualisation ? (Y/N)')
                        if Answer.lower() in ('y', 'yes'):
                            for Path in InstanceList:
                                TCLScript.write('\nwave add /{0}/'.format(Path))

                            AskAgain = False
                        else:
                            if Answer.lower() in ('n', 'no'):
                                AskAgain = False
                                return
                            AskAgain = True

                else:
                    if Instances:
                        for Inst, Path in Instances:
                            TCLScript.write('\ndivider add "{0}"'.format(Inst.Name))
                            if len(Path):
                                TCLScript.write('\nwave add /{0}/{1}/'.format('/'.join(Path), Inst.Name))
                            else:
                                TCLScript.write('\nwave add /{0}/'.format(Inst.Name))

                    else:
                        TCLScript.write('\nwave add /{0}/{1}/'.format(self.TBName, self.DUT))
                SimulationLength = int(NbCycles * CycleLength)
                TCLScript.write('\nvcd dumpfile {0}.vcd'.format(self.TBName))
                TCLScript.write('\nvcd dumpvars -m {0} -l 2'.format(self.DUT))
                TCLScript.write('\nrun 3000 ns')
                TCLScript.write('\nrun all')
                TCLScript.write('\nvcd dumpflush')
                TCLScript.write('\n# Quits simulation.')
                TCLScript.write('\nexit 0\n\n')
            SimuScriptPath = os.path.join(self.LocalSimuPath, 'SimulationScript_{0}_{1}.run'.format(self.TBName, Simulator))
            with open(SimuScriptPath, 'w+') as (SimuScript):
                SimuScript.write('\n# MODULES COMPILATION')
                for FilePath in self.SrcList:
                    AbsFilePath = os.path.abspath(FilePath)
                    if self.RemoteHost is None:
                        SrcPath = AbsFilePath
                    else:
                        SrcPath = '/'.join(['./src', os.path.basename(FilePath)])
                    if FilePath.endswith('.vhd'):
                        SimuScript.write('\nsource "{SETUP_SCRIPT}" && vhpcomp -work work "{0}"'.format(SrcPath, SETUP_SCRIPT=SetupScriptPath))
                    else:
                        if FilePath.endswith('.v'):
                            SimuScript.write('\nsource "{SETUP_SCRIPT}" && vlogcomp -work work "{0}"'.format(SrcPath, SETUP_SCRIPT=SetupScriptPath))
                        else:
                            logging.error("Source format not recognized ('{0}')".format(SrcPath))

                SimuScript.write('\n\n# COMPILE THE PROJECT TESTBENCH')
                SimuScript.write('\nsource "{SETUP_SCRIPT}" && fuse work.{TB} -L unisim -o {PATH}_with_isim.exe'.format(TB=self.TBName, PATH=os.path.join('./', self.TBName), SETUP_SCRIPT=SetupScriptPath))
                SimuScript.write('\n\n# Run the simulation script previously generated')
                SimuScript.write('\nsource "{SETUP_SCRIPT}" && {PATH}_with_isim.exe -intstyle xflow -wdb Results_{TB} -tclbatch {TCL}\n\n'.format(TB=self.TBName, PATH=os.path.join('./', self.TBName), TCL=TCLFilePath if not self.RemoteHost else os.path.basename(TCLFilePath), SETUP_SCRIPT=SetupScriptPath))
                WaveformFilePath = 'Results_{0}.wdb'.format(self.TBName)
                SimuScript.write('\n\nsource "{SETUP_SCRIPT}" && isimgui -view "{WAVE}" '.format(SETUP_SCRIPT=SetupScriptPath, WAVE=WaveformFilePath))
            if self.RemoteHost:
                SimulationPath = 'Simulation/{0}_Simulation_{1}'.format(self.TBName, TimeStamp())
                TargetSrcDirectory = '/'.join([SimulationPath, 'src'])
                DirList = [
                 TargetSrcDirectory]
                SetupFileDict = {SimuScriptPath: os.path.basename(SimuScriptPath)}
                SrcDict = {}
                for S in self.SrcList:
                    SrcDict[S] = os.path.basename(S)

                for FilePath in self.DependencyFiles:
                    SetupFileDict[os.path.abspath(FilePath)] = os.path.basename(FilePath)

                if self.CreateHostDir(DirList=DirList) is False:
                    return
                else:
                    if self.SendPathsRelative(FileDict=SetupFileDict, HostAbsPath=SimulationPath) is False:
                        return
                    if self.SendPathsRelative(FileDict=SrcDict, HostAbsPath=TargetSrcDirectory) is False:
                        return
                    RemoteSimuScriptPath = '/'.join([SimulationPath, os.path.basename(SimuScriptPath)])
                    Success = self.RemoteRun(Command='chmod 777 {SimuScript}'.format(SimuScript=RemoteSimuScriptPath), ScriptsToSource=[], abort_on_prompts='True', warn_only=True)
                    Success = self.RemoteRun(Command='./{SynthesisScript}'.format(SynthesisScript=os.path.basename(RemoteSimuScriptPath)), ScriptsToSource=[
                     SetupScriptPath], FromDirectory=SimulationPath, abort_on_prompts='True', warn_only=True, XForwarding=True)
                    ResultFiles = [
                     os.path.join(self.LocalSimuPath, WaveformFilePath), os.path.join(self.LocalSimuPath, '{0}.vcd'.format(self.TBName))]
                    if Success:
                        logging.info('Simulation success.')
                        if not self.DownloadFromHost(HostPath=WaveformFilePath, LocalPath=self.LocalSimuPath):
                            Misc.CleanTempFiles(Path=SimulationPath, Host=self.RemoteHost)
                            return
                        Misc.CleanTempFiles(Path=SimulationPath, Host=self.RemoteHost)
                        return ResultFiles
                    Misc.CleanTempFiles(Path=SimulationPath, Host=self.RemoteHost)
                    logging.info('Simulation failure.')
                    return
            else:
                SimulationPath = self.LocalSimuPath
                for FilePath in self.DependencyFiles:
                    AbsFilePath = os.path.abspath(FilePath)
                    shutil.copy(AbsFilePath, SimulationPath)

                logging.debug("SimuScriptPath: '{0}'".format(SimuScriptPath))
                with Localcd(SimulationPath):
                    if not SafeRun.SafeRun(not sys.platform.startswith('win'), [SimuScriptPath]):
                        logging.info('Simulation script execution success.')
                        logging.info('Now open waveform file.')
                        WaveformFilePath = 'Results_{0}.wdb'.format(self.TBName)
                        WaveformFilePath = os.path.join(SimulationPath, WaveformFilePath)
                        return (
                         WaveformFilePath, os.path.join(SimulationPath, '{0}.vcd'.format(self.TBName)))
                    else:
                        Misc.CleanTempFiles(Path=SimulationPath, Host=self.RemoteHost)
                        return
        else:
            logging.error("No such simulator supported '{0}'.".format(Simulator))
            return


class TrafficSimulation(Simulation):
    __doc__ = '\n\tSub class of simulation dedicated to NoC Traffic simulation.\n\t'

    def __init__(self, TopModule, TrafficMatrix={}, OutputPath='./'):
        """
                Configure traffic parameters.
                """
        Simulation.__init__(self, Module=TopModule, OutputPath=OutputPath)
        self.TrafficMatrix = TrafficMatrix

    def GetLatences(self):
        """
                Return dictionary of results for traffic sent by each router.
                """
        Latencies = {}
        return Latencies


class NoCTrafficModule:
    __doc__ = '\n\tmyHDL top module.\n\t'

    def __init__(self, Duration=500, TopModule=None):
        """
                Initialize testbench duration and list of instances.
                """
        self.InstancesList = InstancesList
        self.Duration = Duration
        self.NoCModule = TopModule.Get()
        self.Inputs = [HDL.Signal(HDL.intbv(0, min=0, max=DataWidth)) for k in range(0, NbInputs)]
        self.Outputs = [HDL.Signal(HDL.intbv(0, min=0, max=DataWidth)) for k in range(0, NbOutputs)]

    def nulls(self):
        """
                support method code
                """
        pass

    def Top(self):
        """
                myhdl module code
                """
        cmd = 'iverilog -o bin2gray -Dwidth=%s bin2gray.v dut_bin2gray.v'

        def NoC(B, G, width):
            os.system(cmd % width)
            return HDL.Cosimulation('vvp -m ./myhdl.vpi {0}'.format(self.NoCModule.Name), B=B, G=G)


def Simulate_myHDL():
    """
        myHDL testbench
        """
    reset = HDL.ResetSignal(0, active=0, async=True)
    Clk = HDL.Signal(bool(0))

    @HDL.always(HalfPeriod)
    def ClkDriver():
        Clk.next = not Clk

    @HDL.instance
    def Stimuli():
        Rst.next = 1
        yield Clk.negedge
        Rst.next = 0
        for i in range(Duration):
            for Index in range(len(Inputs)):
                Inputs[Index].next = RDM.randrange(len(Inputs))

            yield Clk.negedge

        raise HDL.StopSimulation

    @HDL.instance
    def monitor():

        @HDL.always_seq(Clk.posedge, reset=reset)
        def TestNewLatency():
            for S in self.Outputs:
                if S.edge():
                    print('[{0}] Received packet, latency={1}'.format(HDL.now(), S))

    TestedModule = NoCTrafficModule(Duration=500, TopModule=None)
    x = HDL.Signal(intbv(0, min=-8, max=8))
    y = HDL.Signal(intbv(0, min=-64, max=64))
    toVerilog(TestedModule.Top, clock, reset, x, y)
    toVHDL(TestedModule.Top, clock, reset, x, y)
    return HDL.instances()


class NullDevice:

    def write(self, s):
        pass

    def isatty(self):
        return False