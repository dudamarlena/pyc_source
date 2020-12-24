# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/HdlLib/SysGen/FpgaOperations.py
# Compiled at: 2017-07-08 08:29:58
# Size of source mod 2**32: 14996 bytes
import os, re, argparse, logging, sys, os, datetime, getpass, shlex, shutil, string, tempfile
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '..')))
from HdlLib.Utilities import Timer, Misc
from HdlLib.Utilities.RemoteOperations import RemoteOperations
from HdlLib.Utilities import SafeRun

class FpgaOperations(RemoteOperations):

    def __init__(self, RemoteSubFolder='UnknownTool'):
        """
                Environment variables settings
                """
        RemoteOperations.__init__(self, RemoteSubFolder=RemoteSubFolder)

    def Synthesize(self, HwModel, TopName, SourceList, ConstraintFile, SrcDirectory, OutputPath, RscEstimation=False):
        """
                Execute a_safe_run.exe remotely with synthesis scripts. 
                        * Source paths are given relatively to SrcDirectory
                """
        ResultFilesDict = {}
        LocalSynthesisPath = os.path.abspath(OutputPath)
        if not os.path.isdir(LocalSynthesisPath):
            os.makedirs(LocalSynthesisPath)
        if RscEstimation is True:
            SynthesisScript = HwModel.GetRscEstimationScript()
        else:
            SynthesisScript = HwModel.GetSynthesisScript()
        if SynthesisScript is None:
            logging.error('No synthesis script found in configuration file. Aborted.')
            return ResultFilesDict
        if not os.path.isfile(SynthesisScript):
            logging.error("Synthesis script found in configuration file ('{0}') is not a proper file. Synthesis aborted.".format(SynthesisScript))
            return ResultFilesDict
        shutil.copy(SynthesisScript, LocalSynthesisPath)
        SynthesisScript = os.path.join(LocalSynthesisPath, os.path.basename(SynthesisScript))
        SourcesFileName = HwModel.GetSourcesFileName()
        if SourcesFileName is None:
            logging.error('No SourcesFileName option found in configuration file. Synthesis aborted.')
            return ResultFilesDict
        LocalSourceList = os.path.join(LocalSynthesisPath, SourcesFileName)
        if self.RemoteHost:
            SynthesisPath = 'FpgaSynthesis/{0}_Synthesis_{1}'.format(TopName, Timer.TimeStamp())
            TargetSrcDirectory = '/'.join([SynthesisPath, 'src'])
        else:
            SynthesisPath = LocalSynthesisPath
            TargetSrcDirectory = SrcDirectory
            if not os.path.isdir(SynthesisPath):
                os.makedirs(SynthesisPath)
            SLT = HwModel.GetSourcesTemplate()
            if SLT is None:
                logging.error('No template found for source list file. Aborted.')
                return ResultFilesDict
            SourceListTemplate = string.Template(SLT)
            LanguageDict = {'.vho': 'vhdl', '.vhd': 'vhdl', '.vhdl': 'vhdl', '.vh': 'verilog', '.v': 'verilog', '.xci': 'ip', '.xdc': 'xdc'}
            ConstrSrcPath = os.path.relpath(ConstraintFile, os.path.abspath(SrcDirectory))
            with open(LocalSourceList, 'w+') as (SourceListFile):
                for RelSourcePath in SourceList + [ConstrSrcPath]:
                    Extension = '.' + RelSourcePath.split('.')[(-1)]
                    try:
                        Language = LanguageDict[Extension]
                    except:
                        logging.error("Unknown extension of source '{0}'".format(RelSourcePath))
                        continue

                    Library = 'work'
                    AbsSrcPath = os.path.normpath(os.path.join(TargetSrcDirectory, RelSourcePath))
                    PathFromSynthesis = os.path.relpath(AbsSrcPath, SynthesisPath)
                    Substitutes = {'Library': Library, 
                     'Language': Language, 
                     'Source': PathFromSynthesis}
                    SourceListFile.write('\n' + SourceListTemplate.safe_substitute(Substitutes))

            SetupVars = {'FPGA': HwModel.GetFPGA(), 
             'TOPENTITY': TopName, 
             'CONSTRAINTS': '"{0}"'.format('/'.join([TargetSrcDirectory, RelSourcePath])), 
             'OUTPUTPATH': SynthesisPath, 
             'SRCLIST': '/'.join([SynthesisPath, os.path.basename(LocalSourceList)]) if self.RemoteHost else LocalSourceList}
            Templates = HwModel.GetTemplates(SetupVars, SynthesisPath if self.RemoteHost is False else LocalSynthesisPath)
            SetupSafeRun = '/'.join([LocalSynthesisPath, 'SafeRun_SynthesisSetup.run'])
            with open(SetupSafeRun, 'w+') as (SetupFile):
                for VarName, VarValue in SetupVars.items():
                    SetupFile.write('\n{0}={1}'.format(VarName, VarValue))

                SetupFile.write('\n\n')
            if self.RemoteHost:
                DirList = [
                 TargetSrcDirectory]
                SetupFileDict = {SetupSafeRun: os.path.basename(SetupSafeRun), 
                 ConstraintFile: '/src/' + os.path.basename(ConstraintFile), 
                 SynthesisScript: os.path.basename(SynthesisScript), 
                 LocalSourceList: os.path.basename(LocalSourceList)}
                SrcDict = {}
                for S in SourceList:
                    AbsSrcPath = os.path.abspath(os.path.join(SrcDirectory, S))
                    SrcDict[AbsSrcPath] = S

                for T in Templates:
                    SetupFileDict[os.path.abspath(T)] = os.path.basename(T)

                if self.CreateHostDir(DirList=DirList) is False:
                    return ResultFilesDict
                else:
                    if self.SendPathsRelative(FileDict=SetupFileDict, HostAbsPath=SynthesisPath) is False:
                        return ResultFilesDict
                    if self.SendPathsRelative(FileDict=SrcDict, HostAbsPath=TargetSrcDirectory) is False:
                        return ResultFilesDict
                    RemoteSetupSafeRun = '/'.join([SynthesisPath, os.path.basename(SetupSafeRun)])
                    RemoteSynthesisScript = '/'.join([SynthesisPath, os.path.basename(SynthesisScript)])
                    Success = self.RemoteRun(Command='chmod 777 {SynthesisScript}'.format(SynthesisScript=RemoteSynthesisScript), ScriptsToSource=[
                     HwModel.GetSetupEnvScript()], abort_on_prompts='True', warn_only=True)
                    Success = self.RemoteRun(Command='./{SynthesisScript}'.format(SetupSafeRun=RemoteSetupSafeRun, SynthesisScript=os.path.basename(RemoteSynthesisScript)), ScriptsToSource=[], FromDirectory=SynthesisPath, abort_on_prompts='True', warn_only=True)
                    if Success:
                        if RscEstimation is True:
                            RemoteResultFilesDict = {}
                        else:
                            BitStreamExt = HwModel.GetBitStreamExt()
                            if BitStreamExt is None:
                                return ResultFilesDict
                            BitStreamPath = '/'.join([SynthesisPath, '{0}{1}'.format(TopName, BitStreamExt)])
                            RemoteResultFilesDict = {'Binary': BitStreamPath}
                        MapReportExt = HwModel.GetMapReportExt()
                        if MapReportExt is None:
                            return RemoteResultFilesDict
                        ParReportExt = HwModel.GetParReportExt()
                        if ParReportExt is None:
                            return RemoteResultFilesDict
                        MapReportPath = '/'.join([SynthesisPath, '{0}{1}'.format(TopName, MapReportExt)])
                        ParReportPath = '/'.join([SynthesisPath, '{0}{1}'.format(TopName, ParReportExt)])
                        RemoteResultFilesDict.update({'PlaceReport': MapReportPath, 'RouteReport': ParReportPath})
                        ResultFilesDict = {}
                        for FileType, ResultFilePath in RemoteResultFilesDict.items():
                            if not self.DownloadFromHost(HostPath=ResultFilePath, LocalPath=LocalSynthesisPath):
                                return {}
                            ResultFilesDict[FileType] = os.path.join(LocalSynthesisPath, os.path.basename(ResultFilePath))

                        logging.info("'{0}' binary generation success.".format(TopName))
                        self.RemoteRun(Command='rm -rf {SynthesisPath}'.format(SynthesisPath=SynthesisPath), abort_on_prompts='True', warn_only=True)
                        return ResultFilesDict
                    self.RemoteRun(Command='rm -rf {SynthesisPath}'.format(SynthesisPath=SynthesisPath), abort_on_prompts='True', warn_only=True)
                    logging.error("'{0}' binary generation failure.".format(TopName))
                    return ResultFilesDict
            else:
                with Misc.cd(SynthesisPath):
                    if not SafeRun.SafeRun(CaseInsensitive=not sys.platform.startswith('win'), CommandFiles=[SetupSafeRun, SynthesisScript]):
                        logging.info("'{0}' binary generation success.".format(TopName))
                        BitStreamExt = HwModel.GetBitStreamExt()
                        if BitStreamExt is None:
                            return ResultFilesDict
                        BitStreamPath = os.path.join(SynthesisPath, '{0}.{1}'.format(TopName, HwModel.GetBinaryExtension()))
                        ResultFilesDict = {'Binary': BitStreamPath}
                        return ResultFilesDict
                    else:
                        logging.error("'{0}' binary generation failure.".format(TopName))
                        return ResultFilesDict


def Synthesize(HwModel, ConstraintFile, Module, SrcDirectory, OutputPath='./FpgaSynthesis', RscEstimation=False, RemoteHost=None):
    """
        Synthesize module design onto HwModel architecture with ConstraintFile as pad assignment constraints.
        """
    LocalUser = getpass.getuser()
    FpgaFlow = FpgaOperations(RemoteSubFolder='{0}-{1}'.format(LocalUser, Timer.TimeStamp()))
    FpgaFlow.SetRemoteHost(RemoteHost)
    EntityName, TopPath = Module.GetTop()
    SourceList = Module.Sources['RTL']
    ConstrSourceList = Module.GetLastCreatedInstance().GatherConstraintSources(FromInst=Module.Name)
    RelSources = [os.path.relpath(S, SrcDirectory) for S in SourceList + ConstrSourceList]
    ResultFilesDict = FpgaFlow.Synthesize(HwModel=HwModel, TopName=EntityName, SourceList=RelSources, ConstraintFile=ConstraintFile, SrcDirectory=SrcDirectory, OutputPath=OutputPath, RscEstimation=RscEstimation)
    if RemoteHost:
        FpgaFlow.Disconnect()
    return ResultFilesDict


def Upload(HwModel, BinaryPath, ScanChainPos=1, Remote=True):
    """
        Upload specified binary to FPGA on HwModel.
        """
    if BinaryPath is None or not os.path.isfile(str(BinaryPath)):
        logging.error('No binary specified for upload.')
        return False
    UploadDirPath = tempfile.mkdtemp(prefix='Upload_{0}_'.format(Timer.TimeStamp()))
    UploadScript = HwModel.GetUploadScript(UploadDirPath)
    if UploadScript is None:
        logging.error('No upload script found. Aborted.')
        return
    SetupVars = {'SCANCHAINPOS': str(ScanChainPos), 
     'BITSTREAM': str(BinaryPath)}
    UploadSetupFile = HwModel.GetUploadSetupFile(SetupVars, UploadDirPath)
    if UploadSetupFile is None:
        logging.error('Upload Setup File not found. Aborted.')
        return
    SetupVars['UPLOAD_SETUP_SCRIPT'] = '/'.join([UploadDirPath, os.path.basename(UploadSetupFile)]) if Remote else os.path.abspath(UploadSetupFile)
    SetupSafeRun = '/'.join([UploadDirPath, 'SafeRun_UploadSetup.run']) if Remote else os.path.join()
    MaxNameWidth = max(*list(map(len, list(SetupVars.keys())))) + 2
    with open(SetupSafeRun, 'w+') as (SetupFile):
        for VarName, VarValue in SetupVars.items():
            SetupFile.write(('\n{0: <' + str(MaxNameWidth) + '} = {1}').format(VarName, VarValue))

    with Misc.cd(UploadDirPath):
        if not SafeRun.SafeRun(CaseInsensitive=not sys.platform.startswith('win'), CommandFiles=[SetupSafeRun, UploadScript]):
            logging.info("'{0}' upload success.".format(HwModel.Name))
            return True
        else:
            logging.error("'{0}' upload failure.".format(HwModel.Name))
            return False