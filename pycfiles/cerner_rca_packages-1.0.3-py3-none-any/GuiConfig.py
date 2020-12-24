# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/gui/cGui/config/GuiConfig.py
# Compiled at: 2012-04-30 15:56:18
__doc__ = '\n.. module:: GuiConfig\n   :platform: Unix\n   :synopsis: Loads configuration info for the gui.\n\n.. moduleauthor:: Brian Kraus\n\n\n'

class GuiConfigError(Exception):
    """
    An exception signifying that the config file was incorrect.
    """


class GuiConfig:
    """
    The class that holds the loaded configuration info.
    """
    LOADED = False
    GuiPath = '/opt/cernent/etc/gui.cfg'
    Bg = None
    _NUM_ELEMS = 8
    Padx = None
    Pady = None
    foregroundColor = None
    labelBackground = None
    highlightBG = None
    highlightColor = None
    highlightThickness = 0


def getBackgroundColor():
    """
    Returns:
        The default background color.
    """
    if not GuiConfig.LOADED:
        _loadConfig()
    return GuiConfig.Bg


def getPadX():
    """
    Returns:
        The default x padding.
    """
    if not GuiConfig.LOADED:
        _loadConfig()
    return GuiConfig.Padx


def getPadY():
    """
    Returns:
        The default y padding.
    """
    if not GuiConfig.LOADED:
        _loadConfig()
    return GuiConfig.Pady


def _loadConfig():
    f = open(GuiConfig.GuiPath, 'r')
    tokens = f.read().split('|')
    if len(tokens) != GuiConfig._NUM_ELEMS:
        raise GuiConfigError('Incorrent number of arguments: ' + str(len(tokens)) + ', should be: ' + str(GuiConfig._NUM_ELEMS))
    GuiConfig.Bg = tokens[0]
    GuiConfig.Padx = int(tokens[1])
    GuiConfig.Pady = int(tokens[2])
    GuiConfig.labelBackground = tokens[3]
    GuiConfig.foregroundColor = tokens[4]
    GuiConfig.highlighBG = tokens[5]
    GuiConfig.highlightColor = tokens[6]
    GuiConfig.highlightThickness = int(tokens[7])
    GuiConfig.LOADED = True
    f.close()


def getHighlightBG():
    """
    Returns:
        The default highlight background color.
    """
    return GuiConfig.highlightBG


def getHighlightColor():
    """
    Returns:
        The default highlight color.
    """
    return GuiConfig.highlightColor


def getHighlightThickness():
    """
    Returns:
        The default highlight thickness.
    """
    return GuiConfig.highlightThickness


def getForegroundColor():
    """
    Returns:
        The default foreground color.
    """
    if not GuiConfig.LOADED:
        _loadConfig()
    return GuiConfig.foregroundColor


def getLabelBackgroundColor():
    """
    Returns:
        The default background color for CLabels.
    """
    if not GuiConfig.LOADED:
        _loadConfig()
    return GuiConfig.labelBackground


if __name__ == '__main__':
    print getBackgroundColor()
    print getPadX()
    print getPadY()
    print getForegroundColor()
    print getLabelBackgroundColor()