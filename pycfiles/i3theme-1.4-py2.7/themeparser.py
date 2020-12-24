# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/i3theme/utils/themeparser.py
# Compiled at: 2016-07-17 13:58:29
import yaml, os, re, subprocess
from voluptuous import Schema, Required

class ThemeParser:
    """
        Theme parser used to check and read a theme file.
    """

    def __init__(self, themeFilePath):
        """
            Initialise a ThemeParser
        """
        try:
            themeFile = open(themeFilePath, 'r')
            themeFileContent = themeFile.read()
            themeFile.close()
            self.theme = yaml.load(themeFileContent)
            self.buildThemeSchema()
            self.schema(self.theme)
        except Exception as exception:
            print 'Error during the loading of "' + os.path.basename(themeFilePath) + '" :'
            print exception.__str__()
            exit(1)

    def buildThemeSchema(self):
        """
            Build the validating schema
        """
        window_colors_leaf = {Required('border'): str, 
           Required('background'): str, 
           Required('text'): str, 
           Required('indicator'): str}
        bar_colors_leaf = {Required('border'): str, 
           Required('background'): str, 
           Required('text'): str}
        self.schema = Schema({'meta': {'author': str, 
                    'version': int, 
                    'description': str}, 
           Required('window_colors'): {Required('focused'): window_colors_leaf, 
                                       Required('focused_inactive'): window_colors_leaf, 
                                       Required('unfocused'): window_colors_leaf, 
                                       Required('urgent'): window_colors_leaf}, 
           Required('bar_colors'): {Required('focused_workspace'): bar_colors_leaf, 
                                    Required('active_workspace'): bar_colors_leaf, 
                                    Required('inactive_workspace'): bar_colors_leaf, 
                                    Required('urgent_workspace'): bar_colors_leaf}}, extra=True)

    def getTheme(self):
        """
            Get the loaded theme
        """
        return self.theme