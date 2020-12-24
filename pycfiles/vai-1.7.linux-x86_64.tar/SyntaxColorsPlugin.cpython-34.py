# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vai/sdk/SyntaxColorsPlugin.py
# Compiled at: 2015-05-02 14:07:56
# Size of source mod 2**32: 794 bytes
from yapsy.IPlugin import IPlugin
from ..models import SyntaxColors

class SyntaxColorsPlugin(IPlugin):

    def getSchema(self, num_colors):
        """
        To be reimplement in the plugin to return a new schema.
        """
        pass

    def name(self):
        """
        To be reimplement in the plugin
        """
        pass

    def supportsNumColors(self, num_colors):
        """
        To be reimplement in the plugin
        """
        return False

    def _defaultSchema(num_colors=None):
        """
        Returns the default color schema for a given number of colors,
        or for the current number of colors if not specified
        """
        num_colors = num_colors or self.numColors()
        return SyntaxColors.defaultColorSchema(num_colors)