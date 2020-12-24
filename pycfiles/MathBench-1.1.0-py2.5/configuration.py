# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mathbench/basement/configuration.py
# Compiled at: 2008-02-07 14:10:42
"""
The tools to save/load/use the user's customisations.
"""
import sys, os
from ConfigParser import SafeConfigParser
import wx, wx.py.dispatcher as dispatcher
MB_DEFAULT_OPTIONS = '\n[Auto Completion]\nShow_Auto_Completion = 1\nInclude_Magic_Attributes = 1\nInclude_Single_Underscores = 1\nInclude_Double_Underscores = 0\n\n[Call Tips]\nShow_Call_Tips = 1\nInsert_Call_Tips = 1\n\n[View]\nWrap_Lines = 1\nShow_Line_Numbers = 1\n\n[Development]\nVerbosity_Level = INFO\n'

class MathBenchConfig(SafeConfigParser):
    """
        Hold the configuration for the whole application and makes it
        possible to save the default and prefered options of the users.

        It is implemented as a singleton.
        """
    __instance = None
    _filepath = '.config'

    def __init__(self):
        """
                Save the default if the file does not exists, else just read it.
                filepath should the the full path to the file (base + name)
                """
        if self.__instance is not None:
            raise Exception('Instanciating a second singleton... arg !')
        if not os.path.isfile(self._filepath):
            config_file = open(self._filepath, 'w')
            config_file.write(MB_DEFAULT_OPTIONS)
            config_file.close()
        SafeConfigParser.__init__(self)
        self.read(self._filepath)
        return

    def save(self):
        """
                Write the config in the file
                """
        config_file = open(self._filepath, 'w')
        self.write(config_file)
        config_file.close()

    @staticmethod
    def setFilePath(filepath):
        """
                Set the config file's path.
                To be called before any initialisation.
                """
        MathBenchConfig._filepath = filepath

    @staticmethod
    def getConfig():
        """
                Return the singleton's instance
                """
        if MathBenchConfig.__instance is None:
            MathBenchConfig.__instance = MathBenchConfig()
        return MathBenchConfig.__instance