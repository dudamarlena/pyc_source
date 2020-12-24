# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/HdlLib/SysGen/HW/HwLib.py
# Compiled at: 2017-07-08 08:29:58
# Size of source mod 2**32: 34742 bytes
import os, sys, logging, string, re
try:
    import configparser
except ImportError:
    import configparser

import shutil, subprocess, collections
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Utilities.Misc import ReplaceTextInFile, IterFiles
from SysGen.HW import HwConstraints
from SysGen import HWLIBRARYPATH

def ListArchi(LibraryPaths=[]):
    """
        Create a constraint file for specified Ctrl and Target.
        """
    LibraryPaths.append(HWLIBRARYPATH)
    ArchiList = []
    for FilePath in IterFiles(SearchPaths=LibraryPaths, Name='*.ini'):
        Config = configparser.RawConfigParser()
        Config.read(FilePath)
        Sections = Config.sections()
        if 'Common' in Sections:
            if Config.has_option('Common', 'Architecture'):
                ArchiList.append(Config.get('Common', 'Architecture').strip())
            else:
                logging.error("No such option 'Architecture' found in configuration file '{0}'.".format(FilePath))
                continue
        else:
            logging.warning("Ignoring configuration file '{0}'.".format(FilePath))
            continue

    return ArchiList


class ArchiConfig:
    __doc__ = '\n\tObject for reading HW library configuration parameters.\n\tEach config is written in a "*.ini" configuration file.\n\t'

    def __init__(self, Architecture, LibraryPaths=[]):
        """
                Parse configuration file.
                """
        if Architecture is None:
            logging.error('No Architecture name available.')
            raise NameError
        self.Architecture = Architecture
        self.Config = None
        self.ConfigPath = None
        self.FlowConfig = None
        self.ReloadConfig(LibraryPaths=list(set(LibraryPaths)))

    def ReloadConfig(self, LibraryPaths=[]):
        """                
                Read architecture configuration file and return true if success else False.
                """
        LibraryPaths.append(HWLIBRARYPATH)
        logging.debug('Browse library paths \n * {0}'.format('\n * '.join(LibraryPaths)))
        for FilePath in IterFiles(SearchPaths=LibraryPaths, Name='*.ini'):
            Config = configparser.RawConfigParser()
            Config.read(FilePath)
            Sections = Config.sections()
            if 'Common' in Sections:
                if Config.has_option('Common', 'Architecture') and Config.get('Common', 'Architecture').lower() == self.Architecture.lower():
                    self.Config = Config
                    self.ConfigPath = FilePath
                    logging.debug("Configuration file found for architecture '{0}'.".format(self.Architecture))
                    if Config.has_option('Common', 'ImplementFlow'):
                        self.FlowConfig = FlowConfig(Config.get('Common', 'ImplementFlow'))
                        return True
                    else:
                        logging.error("No such option 'ImplementFlow' found in configuration of architecture '{0}'.".format(self.Architecture))
                        return False
                else:
                    continue
            else:
                logging.error("No such option 'Architecture' found in configuration file '{0}'.".format(FilePath))
                return False

        logging.error("No configuration file found for architecture '{0}'.".format(self.Architecture))
        return False

    def GetConfigDict(self):
        """                
                return List of available section in config file.
                """
        if self.Config is None:
            logging.error("Configuration file not loaded for architecture '{0}'.".format(self.Architecture))
            return []
        Sections = self.Config.sections()
        if 'Common' in Sections:
            Sections.remove('Common')
        else:
            logging.error("'Common'.".format(self.Architecture))
            return []
        ConfigDict = {}
        for S in Sections:
            if self.Config.has_option(S, 'AcceptedTargetArchitectures'):
                T = self.Config.get(S, 'AcceptedTargetArchitectures')
                if T in ConfigDict:
                    ConfigDict[T].append(S)
                else:
                    ConfigDict[T] = [
                     S]

        return ConfigDict

    def GetFPGA(self, FullId=True):
        """                
                Read command configuration file and return value of FPGAFullId option.
                """
        if self.Config is None:
            logging.error("Configuration file not loaded for architecture '{0}'.".format(self.Architecture))
            return
        else:
            if FullId:
                Key = 'FPGAFullId'
            else:
                Key = 'FPGAId'
            if self.Config.has_option('Common', Key):
                return self.Config.get('Common', Key)
            logging.error("'{0}' configuration error. No such option '{2}' in configuration file ('{1}').".format(self.Architecture, self.ConfigPath, Key))
            return

    def GetAvailableRsc(self):
        """                
                Read command configuration file and return value of FPGAFullId option.
                """
        if self.Config is None:
            logging.error("Configuration file not loaded for architecture '{0}'.".format(self.Architecture))
            return
        RscDict = {}
        if self.Config.has_option('Common', 'AvailableRegister'):
            RscDict['REGISTER'] = (
             int(self.Config.get('Common', 'AvailableRegister')), -1, -1)
        else:
            logging.warning("'{0}' configuration warning. No such option '{2}' in configuration file ('{1}').".format(self.Architecture, self.ConfigPath, 'AvailableRegister'))
        if self.Config.has_option('Common', 'AvailableLUT'):
            RscDict['LUT'] = (
             int(self.Config.get('Common', 'AvailableLUT')), -1, -1)
        else:
            logging.warning("'{0}' configuration warning. No such option '{2}' in configuration file ('{1}').".format(self.Architecture, self.ConfigPath, 'AvailableLUT'))
        if self.Config.has_option('Common', 'AvailableRAM'):
            RscDict['RAM'] = (
             int(self.Config.get('Common', 'AvailableRAM')), -1, -1)
        else:
            logging.warning("'{0}' configuration warning. No such option '{2}' in configuration file ('{1}').".format(self.Architecture, self.ConfigPath, 'AvailableRAM'))
        return RscDict

    def GetCtrlIO(self, ConfigName):
        """                
                Read command configuration file and return value of CtrlIO option.
                """
        if self.Config is None:
            logging.error("Configuration file not loaded for architecture '{0}'.".format(self.Architecture))
            return
        else:
            if ConfigName not in self.Config.sections():
                logging.error("ConfigName '{0}' not in sections of configuration file '{1}'.".format(ConfigName, self.ConfigPath))
                return
            if self.Config.has_option(ConfigName, 'CtrlIO'):
                CtrlIO = self.Config.get(ConfigName, 'CtrlIO')
                return os.path.normpath(os.path.join(os.path.dirname(self.ConfigPath), CtrlIO))
            logging.error("'{0}' configuration error. No such option 'CtrlIO' in configuration file ('{1}').".format(self.Architecture, self.ConfigPath))
            return

    def GetFreq(self, ConfigName):
        """                
                Read command configuration file and return value of Frequency option.
                """
        if self.Config is None:
            logging.error("Configuration file not loaded for architecture '{0}'.".format(self.Architecture))
            return
        else:
            if ConfigName not in self.Config.sections():
                logging.error("ConfigName '{0}' not in sections of configuration file '{1}'.".format(ConfigName, self.ConfigPath))
                return
            if self.Config.has_option(ConfigName, 'Frequency'):
                Freq = self.Config.get(ConfigName, 'Frequency')
                return Freq
            logging.error("'{0}' configuration error. No such option 'Frequency' in configuration file ('{1}').".format(self.Architecture, self.ConfigPath))
            return

    def GetMinDividor(self, ConfigName):
        """                
                Read command configuration file and return value of 'MinDividor' option.
                """
        if self.Config is None:
            logging.error("Configuration file not loaded for architecture '{0}'.".format(self.Architecture))
            return
        else:
            if ConfigName not in self.Config.sections():
                logging.error("ConfigName '{0}' not in sections of configuration file '{1}'.".format(ConfigName, self.ConfigPath))
                return
            if self.Config.has_option(ConfigName, 'MinDividor'):
                MinDividor = int(self.Config.get(ConfigName, 'MinDividor'))
                return MinDividor
            logging.error("'{0}' configuration error. No such option 'MinDividor' in configuration file ('{1}').".format(self.Architecture, self.ConfigPath))
            return

    def GetSynthesisScript(self):
        """
                Read flow configuration file and return value of SynthesisScript option.
                """
        if self.FlowConfig is None:
            logging.error("No flow configuration associated with architecture '{0}': no implement script found.".format(self.Architecture))
            return
        else:
            return self.FlowConfig.GetSynthesisScript()

    def GetSetupEnvScript(self):
        """
                Read flow configuration file and return value of SetupEnvScript option.
                """
        if self.FlowConfig is None:
            logging.error("No flow configuration associated with architecture '{0}': no SetupEnvScript option found.".format(self.Architecture))
            return
        else:
            return self.FlowConfig.GetSetupEnvScript()

    def GetRscEstimationScript(self):
        """                
                Read flow configuration file and return value of Resource estimation script option 'RscEstimationScript'.
                """
        if self.FlowConfig is None:
            logging.error("No flow configuration associated with architecture '{0}': no Resource estimation script found.".format(self.Architecture))
            return
        else:
            return self.FlowConfig.GetRscEstimationScript()

    def GetUploadScript(self):
        """                
                Read flow configuration file and return value of UploadScript option.
                """
        if self.FlowConfig is None:
            logging.error("No flow configuration associated with architecture '{0}': no implement script found.".format(self.Architecture))
            return
        else:
            return self.FlowConfig.GetUploadScript()

    def GetCtrlImplementScript(self):
        """                
                Read flow configuration file and return value of CtrlImplementScript option.
                """
        if self.FlowConfig is None:
            logging.error("No flow configuration associated with architecture '{0}': no ctrl implement script found.".format(self.Architecture))
            return
        else:
            return self.FlowConfig.GetCtrlImplementScript()

    def GetSourcesTemplate(self):
        """                
                Read flow configuration file and return value of SourceListTemplate option.
                """
        if self.FlowConfig is None:
            logging.error("No flow configuration associated with architecture '{0}': no Source-List Template found.".format(self.Architecture))
            return
        else:
            return self.FlowConfig.GetSourcesTemplate()

    def GetSourcesFileName(self):
        """                
                Read flow configuration file and return value of SourcesFileName option.
                """
        if self.FlowConfig is None:
            logging.error("No flow configuration associated with architecture '{0}': no SourcesFileName found.".format(self.Architecture))
            return
        else:
            return self.FlowConfig.GetSourcesFileName()

    def GetTemplates(self, SetupVars, DestinationPath):
        """                
                Read flow configuration file and return value of SetupScript option.
                """
        Templates = self.FlowConfig.GetTemplates()
        if DestinationPath is None:
            pass
        else:
            if not os.path.isdir(DestinationPath):
                logging.error("No such directory '{0}'".format(DestinationPath))
                return []
            TemplateList = []
            for T in Templates:
                if DestinationPath is not None:
                    shutil.copy(T, DestinationPath)
                    T = os.path.join(DestinationPath, os.path.basename(T))
                for VarName, VarValue in SetupVars.items():
                    ReplaceTextInFile(FileName=T, OldText='${0}'.format(VarName), NewText='{0}'.format(VarValue))

                TemplateList.append(T)

        return TemplateList

    def GetBitStreamExt(self):
        """                
                Return value of "BinaryExtension" field of a flow configuration.
                """
        return self.FlowConfig.GetBitStreamExt()

    def GetMapReportExt(self):
        """                
                Return value of "MapReportExt" field of a flow configuration.
                """
        return self.FlowConfig.GetMapReportExt()

    def GetParReportExt(self):
        """
                Return value of "ParReportExt" field of a flow configuration.
                """
        return self.FlowConfig.GetParReportExt()

    def GetCtrlInputExtension(self):
        """                
                Read flow configuration file and return value of dependency ext option.
                """
        if self.FlowConfig is None:
            logging.error("No flow configuration associated with architecture '{0}': no constraint format found.".format(self.Architecture))
            return
        else:
            DepExt = self.FlowConfig.GetCtrlInputExtension()
            return DepExt

    def GetConstraintFormat(self):
        """                
                Read flow configuration file and return value of ConstraintFormat option.
                """
        if self.FlowConfig is None:
            logging.error("No flow configuration associated with architecture '{0}': no constraint format found.".format(self.Architecture))
            return
        else:
            return self.FlowConfig.GetConstraintFormat()

    def GetBaseCtrlConstraints(self):
        """                
                Read flow configuration file and return value of BaseCtrlConstraints option.
                """
        if self.Config is None:
            logging.error("Configuration file not loaded for architecture '{0}'.".format(self.Architecture))
            return
        else:
            if 'Common' not in self.Config.sections():
                logging.error("No section 'Common' in configuration file '{1}'.".format(self.ConfigPath))
                return
            if self.Config.has_option('Common', 'BaseCtrlConstraints'):
                BaseCtrlConstraints = self.Config.get('Common', 'BaseCtrlConstraints')
                return os.path.normpath(os.path.join(os.path.dirname(self.ConfigPath), BaseCtrlConstraints))
            logging.error("'{0}' configuration error. No such option 'BaseCtrlConstraints' in configuration file ('{1}').".format(self.Architecture, self.ConfigPath))
            return

    def GetCompatibleConfig(self, NbClk, NbStim, NbTrace, NbBiDir, Target):
        """                
                Find compatible config (nb stim/trace/inout) and return config name.
                """
        logging.debug('Seek compatible configuration of architecture {0} as controller (C={1}, S={2}, T={3}, B={4}).'.format(self.Architecture, NbClk, NbStim, NbTrace, NbBiDir))
        if self.Config is None:
            logging.error("Configuration file not loaded for architecture '{0}'.".format(self.Architecture))
            return
        ClockMode = 'mult' if int(NbClk) > 1 else 'mono'
        logging.debug("ClockMode: '{0}'".format(ClockMode))
        Sections = self.Config.sections()
        logging.debug("Sections: '{0}'".format(Sections))
        for Sec in Sections:
            if Sec == 'Common':
                continue
            elif self.Config.has_option(Sec, 'MaxStimuli') and self.Config.has_option(Sec, 'MaxTraces') and self.Config.has_option(Sec, 'MaxBidir') and self.Config.has_option(Sec, 'ClockMode'):
                FoundClockMode = self.Config.get(Sec, 'ClockMode')
                MaxStimuli = int(self.Config.get(Sec, 'MaxStimuli'))
                MaxTraces = int(self.Config.get(Sec, 'MaxTraces'))
                MaxBidir = int(self.Config.get(Sec, 'MaxBidir'))
                logging.debug("Found config '{0}': '{1}'".format(Sec, [MaxStimuli, MaxTraces, MaxBidir, FoundClockMode]))
                if NbStim <= MaxStimuli and NbBiDir <= MaxBidir and FoundClockMode == ClockMode:
                    if self.Config.has_option(Sec, 'AcceptedTargetArchitectures'):
                        Targets = self.Config.get(Sec, 'AcceptedTargetArchitectures')
                        if Target in [x.strip() for x in Targets.split(',')]:
                            logging.debug("Found controller compatible configuration: '{0}'.".format(Sec))
                            return Sec
                            continue
                        else:
                            logging.error("Bad format of configuration file. Section '{0}' Missing options 'AcceptedTargetArchitectures'.".format(Sec))
                        continue
                    else:
                        continue
                else:
                    logging.error("Bad format of configuration file. Section '{0}' Missing one or more options among those [Stimuli, Traces, Bidir, ClockMode]".format(Sec))
                continue

    def GetInterface(self):
        """                
                return number of port pads and clocks.
                """
        if self.Config is None:
            logging.error("Configuration file not loaded for architecture '{0}'.".format(self.Architecture))
            return (None, None)
        ConfigPath = HWLIBRARYPATH
        BoardsCo = GetInterfaceDict(BoardName=self.Architecture, ConfigPath=ConfigPath)
        return BoardsCo

    def GetConfigIO(self, ConfigName):
        """                
                Find compatible config (nb stim/trace/inout) and return config name.
                """
        if self.Config is None:
            logging.error("Configuration file not loaded for architecture '{0}'.".format(self.Architecture))
            return
        Sections = self.Config.sections()
        if ConfigName in Sections:
            if self.Config.has_option(ConfigName, 'MaxStimuli') and self.Config.has_option(ConfigName, 'MaxTraces') and self.Config.has_option(ConfigName, 'MaxBidir') and self.Config.has_option(ConfigName, 'ClockMode'):
                return (
                 int(self.Config.getint(ConfigName, 'MaxStimuli')),
                 int(self.Config.getint(ConfigName, 'MaxTraces')),
                 int(self.Config.get(ConfigName, 'MaxBidir')),
                 self.Config.get(ConfigName, 'ClockMode'))
        else:
            logging.error("No configuration '{0}' found in '.ini' Sections.")
            return

    def GetCompatibleTargets(self):
        """                
                Return list of compatible targets.
                """
        TargetList = []
        logging.debug('Seek compatible targets with architecture {0} as controller.'.format(self.Architecture))
        if self.Config is None:
            logging.error("Configuration file not loaded for architecture '{0}'.".format(self.Architecture))
            return TargetList
        Sections = self.Config.sections()
        logging.debug("Sections: '{0}'".format(Sections))
        for Sec in Sections:
            if Sec == 'Common':
                continue
            elif self.Config.has_option(Sec, 'AcceptedTargetArchitectures'):
                TargetList.append(self.Config.get(Sec, 'AcceptedTargetArchitectures'))
                continue

        return TargetList


class FlowConfig:
    __doc__ = '\n\tObject for reading HW library flow configuration parameters.\n\tEach config is written in a "*.ini" configuration file.\n\t'

    def __init__(self, FlowName, LibraryPaths=[]):
        """
                Parse configuration file.
                """
        self.FlowName = FlowName
        self.Config = None
        self.ConfigPath = None
        if not self.ReloadConfig(LibraryPaths=LibraryPaths):
            logging.error("No configuration file found for flow '{0}'.".format(FlowName))

    def ReloadConfig(self, LibraryPaths=[]):
        """                
                Read flow configuration file and return true if success else False.
                """
        LibraryPaths.append(os.path.join(HWLIBRARYPATH, 'Scripts'))
        for FilePath in IterFiles(SearchPaths=LibraryPaths, Name='Flow*.ini'):
            Config = configparser.RawConfigParser()
            Config.read(FilePath)
            Sections = Config.sections()
            logging.debug("Configuration file found for '{0}' flow.".format(self.FlowName))
            if self.FlowName in Sections:
                self.Config = Config
                self.ConfigPath = FilePath
                return True
            else:
                logging.error("No such flow '{0}' in configuration file '{1}' (available={2}).".format(self.FlowName, FilePath, Sections))
                return False

        logging.error("No configuration file found for flow '{0}'.".format(self.FlowName))
        return False

    def GetBitStreamExt(self):
        """                
                Return value of "BinaryExtension" field of a flow configuration.
                """
        if self.Config is None:
            logging.error("Configuration file not loaded for architecture '{0}'.".format(self.Architecture))
            return
        else:
            if self.Config.has_option(self.FlowName, 'BinaryExtension'):
                return self.Config.get(self.FlowName, 'BinaryExtension')
            logging.error("'{0}' configuration error. No such option 'BinaryExtension' in configuration file ('{1}').".format(self.FlowName, self.ConfigPath))
            return

    def GetMapReportExt(self):
        """                
                Return value of "MapReportExt" field of a flow configuration.
                """
        if self.Config is None:
            logging.error("Configuration file not loaded for architecture '{0}'.".format(self.Architecture))
            return
        else:
            if self.Config.has_option(self.FlowName, 'MapReportExt'):
                return self.Config.get(self.FlowName, 'MapReportExt')
            logging.error("'{0}' configuration error. No such option 'MapReportExt' in configuration file ('{1}').".format(self.FlowName, self.ConfigPath))
            return

    def GetParReportExt(self):
        """                
                Return value of "ParReportExt" field of a flow configuration.
                """
        if self.Config is None:
            logging.error("Configuration file not loaded for architecture '{0}'.".format(self.Architecture))
            return
        else:
            if self.Config.has_option(self.FlowName, 'ParReportExt'):
                return self.Config.get(self.FlowName, 'ParReportExt')
            logging.error("'{0}' configuration error. No such option 'ParReportExt' in configuration file ('{1}').".format(self.FlowName, self.ConfigPath))
            return

    def GetCtrlImplementScript(self):
        """                
                Read flow configuration file and return value of CtrlImplementScript option.
                """
        if self.Config is None:
            logging.error("Configuration file not loaded for '{0}' flow.".format(self.FlowName))
            return
        else:
            if self.Config.has_option(self.FlowName, 'CtrlImplementScript'):
                Script = self.Config.get(self.FlowName, 'CtrlImplementScript')
                return os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(self.ConfigPath), Script)))
            logging.error("'{0}' configuration error. No such option 'CtrlImplementScript' in configuration file ('{1}').".format(self.FlowName, self.ConfigPath))
            return

    def GetSynthesisScript(self):
        """                
                Read flow configuration file and return value of SynthesisScript option.
                """
        if self.Config is None:
            logging.error("Configuration file not loaded for '{0}' flow.".format(self.FlowName))
            return
        else:
            if self.Config.has_option(self.FlowName, 'SynthesisScript'):
                Script = self.Config.get(self.FlowName, 'SynthesisScript')
                return os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(self.ConfigPath), Script)))
            logging.error("'{0}' configuration error. No such option 'SynthesisScript' in configuration file ('{1}').".format(self.FlowName, self.ConfigPath))
            return

    def GetSetupEnvScript(self):
        """                
                Read flow configuration file and return value of 'SetupEnvScript' option.
                """
        if self.Config is None:
            logging.error("Configuration file not loaded for '{0}' flow.".format(self.FlowName))
            return
        else:
            if self.Config.has_option(self.FlowName, 'SetupEnvScript'):
                return self.Config.get(self.FlowName, 'SetupEnvScript')
            logging.error("'{0}' configuration error. No such option 'SynthesisScript' in configuration file ('{1}').".format(self.FlowName, self.ConfigPath))
            return

    def GetSourcesFileName(self):
        """                
                Read flow configuration file and return value of 'SourcesFileName' option.
                """
        if self.Config is None:
            logging.error("Configuration file not loaded for '{0}' flow.".format(self.FlowName))
            return
        else:
            if self.Config.has_option(self.FlowName, 'SourcesFileName'):
                return self.Config.get(self.FlowName, 'SourcesFileName')
            logging.error("'{0}' configuration error. No such option 'SourcesFileName' in configuration file ('{1}').".format(self.FlowName, self.ConfigPath))
            return

    def GetRscEstimationScript(self):
        """                
                Read flow configuration file and return value of RscEstimationScript option.
                """
        if self.Config is None:
            logging.error("Configuration file not loaded for '{0}' flow.".format(self.FlowName))
            return
        else:
            if self.Config.has_option(self.FlowName, 'RscEstimationScript'):
                Script = self.Config.get(self.FlowName, 'RscEstimationScript')
                return os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(self.ConfigPath), Script)))
            logging.error("'{0}' configuration error. No such option 'RscEstimationScript' in configuration file ('{1}').".format(self.FlowName, self.ConfigPath))
            return

    def GetUploadScript(self):
        """                
                Read flow configuration file and return value of UploadScript option.
                """
        if self.Config is None:
            logging.error("Configuration file not loaded for '{0}' flow.".format(self.FlowName))
            return
        else:
            if self.Config.has_option(self.FlowName, 'UploadScript'):
                Script = self.Config.get(self.FlowName, 'UploadScript')
                return os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(self.ConfigPath), Script)))
            logging.error("'{0}' configuration error. No such option 'UploadScript' in configuration file ('{1}').".format(self.FlowName, self.ConfigPath))
            return

    def GetSourcesTemplate(self):
        """                
                Read flow configuration file and return value of SourcesTemplate option.
                """
        if self.Config is None:
            logging.error("Configuration file not loaded for '{0}' flow.".format(self.FlowName))
            return
        else:
            if self.Config.has_option(self.FlowName, 'SourcesTemplate'):
                SourceListTemplate = self.Config.get(self.FlowName, 'SourcesTemplate')
                return SourceListTemplate
            logging.error("'{0}' configuration error. No such option 'SourcesTemplate' in configuration file ('{1}').".format(self.FlowName, self.ConfigPath))
            return

    def GetTemplates(self):
        """                
                Read flow configuration file and return value of ImplementScript option.
                """
        TemplateList = []
        if self.Config is None:
            logging.error("Configuration file not loaded for '{0}' flow.".format(self.FlowName))
            return []
        else:
            if self.Config.has_option(self.FlowName, 'Templates'):
                Templates = self.Config.get(self.FlowName, 'Templates')
                for Template in Templates.split(','):
                    TemplateList.append(os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(self.ConfigPath), Template.strip()))))

                return TemplateList
            logging.error("'{0}' configuration error. No such option 'Templates' in configuration file ('{1}').".format(self.FlowName, self.ConfigPath))
            return []

    def GetUploadSetupFile(self):
        """                
                Read flow configuration file and return value of UploadScript option.
                """
        if self.Config is None:
            logging.error("Configuration file not loaded for '{0}' flow.".format(self.FlowName))
            return
        else:
            if self.Config.has_option(self.FlowName, 'UploadSetupFile'):
                SetupFile = self.Config.get(self.FlowName, 'UploadSetupFile')
                return os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(self.ConfigPath), SetupFile)))
            logging.error("'{0}' configuration error. No such option 'SetupScript' in configuration file ('{1}').".format(self.FlowName, self.ConfigPath))
            return

    def GetConstraintFormat(self):
        """                
                Read flow configuration file and return value of ConstraintFormat option.
                """
        if self.Config is None:
            logging.error("Configuration file not loaded for '{0}' flow.".format(self.FlowName))
            return
        else:
            if self.Config.has_option(self.FlowName, 'ConstraintFormat'):
                ConstraintFormat = self.Config.get(self.FlowName, 'ConstraintFormat')
                return ConstraintFormat
            logging.error("'{0}' configuration error. No such option 'ConstraintFormat' in configuration file ('{1}').".format(self.FlowName, self.ConfigPath))
            return

    def GetCtrlInputExtension(self):
        """                
                Read flow configuration file and return value of Ctrl Input ext option.
                """
        if self.Config is None:
            logging.error("Configuration file not loaded for '{0}' flow.".format(self.FlowName))
            return
        else:
            if self.Config.has_option(self.FlowName, 'CtrlInputExtension'):
                CtrlInputExtension = self.Config.get(self.FlowName, 'CtrlInputExtension')
                return CtrlInputExtension
            logging.error("'{0}' configuration error. No such option 'CtrlInputExtension' in configuration file ('{1}').".format(self.FlowName, self.ConfigPath))
            return


def GetInterfaceDict(BoardName, ConfigPath):
    """
        Fetch hardware interface parameters.
        """
    CfgFileList = []
    for Root, Dirs, Files in os.walk(ConfigPath, topdown=True):
        for FileName in Files:
            if FileName.endswith('.co'):
                CfgFileList.append(os.path.join(Root, FileName))

    HwInterfaceDict = {}
    for CfgFile in CfgFileList:
        Config = configparser.RawConfigParser()
        Config.read(CfgFile)
        for Section in Config.sections():
            if Section == BoardName:
                logging.debug("-> Found config for board '{0}'".format(Section))
                Infos = Config.items(Section)
                for Param, Value in Infos:
                    Param = Param.upper()
                    Options = [x.upper().strip() for x in Value.split(',')]
                    if len(Options) < 6:
                        Options.extend([None for i in range(6 - len(Options))])
                    Pad, Type, IOStandard, Voltage, Freq, DiffPair = Options[:6]
                    if Type is None:
                        logging.error("Net '{0}', pad '{1}' has no type associated with it. Ignored.".format(Param, Pad))
                    else:
                        if Type not in HwInterfaceDict:
                            HwInterfaceDict[Type] = collections.OrderedDict()
                        HwInterfaceDict[Type][Param.upper()] = [
                         Pad, IOStandard, Voltage, Freq, DiffPair]

                return HwInterfaceDict

    logging.error("Board '{0}' interface configuration file (.co) not found.".format(BoardName))
    return HwInterfaceDict