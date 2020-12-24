# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/i3theme/utils/filebridge.py
# Compiled at: 2016-07-15 05:04:55
import os, subprocess, re

class FileBridge:
    """
        Class to convert a theme to an understandable configuration for i3.
        This class can also apply a theme (act on a configuration file).
    """

    def __init__(self, themeParser, configFilePath=None):
        self.theme = themeParser.getTheme()
        if configFilePath == None:
            self.configFilePath = os.path.join(os.environ['HOME'], '.i3/config')
        return

    def getBarConfig(self):
        """
            Build the color block configuration (in the block bar)
        """
        configFormat = 'colors {\n'
        configFormat += '\tbackground %s\n' % self.theme['bar_colors']['background']
        configFormat += '\tseparator %s\n' % self.theme['bar_colors']['separator']
        configFormat += '\tstatusline %s\n\n' % self.theme['bar_colors']['statusline']
        for barType, barValues in self.theme['bar_colors'].iteritems():
            if type(barValues) is dict:
                configFormat += '\t%s' % barType
                for key in ['border', 'background', 'text']:
                    color = self.theme['bar_colors'][barType][key]
                    if color[0] != '#':
                        configFormat += ' $%s' % color
                    else:
                        configFormat += ' %s' % color

                configFormat += '\n'
            else:
                configFormat += '\t%s' % barType
                color = self.theme['bar_colors'][barType]
                if color[0] != '#':
                    configFormat += ' $%s' % color
                else:
                    configFormat += ' %s' % color
                configFormat += '\n'

        configFormat += '}'
        return configFormat

    def getWindowConfig(self):
        configFormat = ''
        for windowType, windowValues in self.theme['window_colors'].iteritems():
            configFormat += 'client.%s' % windowType
            for key in ['border', 'background', 'text', 'indicator']:
                if self.theme['window_colors'][windowType][key][0] != '#':
                    configFormat += ' $%s' % self.theme['window_colors'][windowType][key]
                else:
                    configFormat += ' %s' % self.theme['window_colors'][windowType][key]

            configFormat += '\n'

        return configFormat

    def apply(self):
        """
            Apply theme to config file
        """
        if os.path.isfile(self.configFilePath):
            FileBridge.cleanConfigFile(self.configFilePath)
            configFile = open(self.configFilePath, 'r+')
            configFileContent = self.getColorConfig() + configFile.read() + self.getWindowConfig()
            s = re.compile('\n(\\s)*bar.*{', re.DOTALL)
            configFileContent = re.sub(s, '\nbar { \n' + self.getBarConfig(), configFileContent)
            configFile.seek(0)
            configFile.truncate()
            configFile.write(configFileContent)
            configFile.close()
            FileBridge.reloadConfig()

    @staticmethod
    def reloadConfig():
        try:
            subprocess.Popen(['i3-msg', 'reload'], stdout=subprocess.PIPE)
        except:
            print 'i3-msg not found. Please install it to be able to reload the configuration.'

    @staticmethod
    def cleanConfigFile(configFilePath):
        """
            Clear all theme informations from a configuration file
        """
        if os.path.isfile(configFilePath):
            configFile = open(configFilePath, 'r+')
            configFileContent = re.sub('client\\..*\\n', '', configFile.read())
            configFileContent = re.sub('set.*\\#.*\\n', '', configFileContent)
            expr = re.compile('(colors[^}]*\\}[^\n]*\n)?', re.DOTALL)
            configFileContent = re.sub(expr, '', configFileContent)
            configFile.seek(0)
            configFile.truncate()
            configFile.write(configFileContent)
            configFile.close()

    def getColorConfig(self):
        """
            Build color variable assignment
        """
        configFormat = ''
        if 'colors' in self.theme:
            for varName, varValue in self.theme['colors'].iteritems():
                configFormat += 'set $%s %s\n' % (varName, varValue)

        return configFormat