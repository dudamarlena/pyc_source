# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/HdlLib/Utilities/UserConfig.py
# Compiled at: 2017-07-08 08:29:58
# Size of source mod 2**32: 2817 bytes
import os, sys, logging
try:
    import configparser
except ImportError:
    import configparser

UserConfigDict = {'Library': ['LibraryPath'], 
 'Simulation.localhost': ['SourceScript_Modelsim', 'SourceScript_Isim', 'SourceScript_Vivado', 'SourceScript_gHDL'], 
 'FpgaSynthesis.localhost': ['SourceScript_Vivado', 'SourceScript_Ise', 'SourceScript_Quartus']}

class UserConfig:

    def __init__(self):
        self.UserConfFilePath = FindUserConfigFile()
        self.UserConfig = configparser.RawConfigParser()
        self.UserConfig.read(self.UserConfFilePath)

    def GetValue(self, Sec, Opt, Host=None):
        """
                return value associated with option 'Opt' of section 'Sec'.
                """
        if self.UserConfig is None:
            logging.error("[UserConfig] User Configuration file not loaded. Check for '~/SyntheSys.conf'")
            return
        else:
            if Host is None:
                Host = 'localhost'
            Section = '.'.join([Sec, Host])
            if self.UserConfig.has_option(Section, Opt):
                Val = self.UserConfig.get(Section, Opt)
                if len(Val.strip()) == 0:
                    logging.error("[UserConfig] Option '{0}' not set (section '{1}' of configuration file '{2}').".format(Opt, Section, self.UserConfFilePath))
                return Val
            logging.error("[UserConfig] Configuration error. No such option '{0}' of section '{1}' in configuration file '{2}'.".format(Opt, Section, self.UserConfFilePath))
            return

    def WriteValue(slef, Sec, Opt):
        """
                Edit value associated with option 'Opt' of section 'Sec' 
                in user config file.
                """
        logging.error("'WriteValue' function not implemented yet")
        raise TypeError


def FindUserConfigFile():
    """
        return SyntheSysConf.ini user file or create new one if not found.
        """
    FilePath = os.path.expanduser('~/SyntheSys.conf')
    if not os.path.isfile(FilePath):
        CreateNewUserConfigFile(FilePath)
    return FilePath


def CreateNewUserConfigFile(FilePath):
    """
        return SyntheSysConf.ini user file or create new one if not found.
        """
    Config = configparser.RawConfigParser()
    for Section, OptionList in UserConfigDict.items():
        Config[Section] = {O:'' for O in OptionList}

    with open(FilePath, 'w+') as (ConfigFile):
        Config.write(ConfigFile)