# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:/Users/HDi/Google Drive/ProgramCodes/Released/PyPI/cognitivegeo/cognitivegeo/src\core\settings.py
# Compiled at: 2019-12-05 17:01:42
# Size of source mod 2**32: 7510 bytes
import numpy as np, os, sys
__all__ = [
 'settings']
GUI = {}
GUI['Toolbar'] = {}
GUI['Toolbar']['Left'] = True
GUI['Toolbar']['Right'] = True
GUI['Toolbar']['Top'] = True
GUI['Toolbar']['Bottom'] = True
General = {}
General['RootPath'] = os.path.dirname(__file__)[:-15]
Visual = {}
Visual['Font'] = {}
Visual['Font']['Name'] = 'Times New Roman'
Visual['Font']['Color'] = 'Green'
Visual['Font']['Style'] = 'Normal'
Visual['Font']['Weight'] = 'Normal'
Visual['Font']['Size'] = 16
Visual['Line'] = {}
Visual['Line']['Color'] = 'Red'
Visual['Line']['Width'] = 3
Visual['Line']['Style'] = 'Solid'
Visual['Line']['MarkerStyle'] = 'None'
Visual['Line']['MarkerSize'] = 5
Visual['Image'] = {}
Visual['Image']['Colormap'] = 'Red-White-Blue'
Visual['Image']['Interpolation'] = 'Quadric'
Viewer = {}
Viewer['Viewer3D'] = {}
Viewer['Viewer3D']['GoHome'] = 'U'
Viewer['Viewer3D']['ViewFrom'] = {}
Viewer['Viewer3D']['ViewFrom']['Inline'] = 'I'
Viewer['Viewer3D']['ViewFrom']['Crossline'] = 'X'
Viewer['Viewer3D']['ViewFrom']['Z'] = 'Z'
Viewer['Player'] = {}
Viewer['Player']['First'] = 'A'
Viewer['Player']['Previous'] = 'S'
Viewer['Player']['Next'] = 'D'
Viewer['Player']['Last'] = 'F'
Viewer['Player']['Backward'] = 'Q'
Viewer['Player']['Forward'] = 'W'
Viewer['Player']['Pause'] = 'P'
Viewer['Player']['Interval'] = 1

def checkGUI(gui):
    """
    Check if the GUI setting good to use

    Args:
        gui:    GUI setting dictionary

    Return:
        True or false
    """
    if len(gui.keys()) < 1:
        return False
    else:
        if 'Toolbar' not in gui.keys():
            return False
        else:
            if len(gui['Toolbar'].keys()) < 1:
                return False
            if 'Left' not in gui['Toolbar'].keys() or 'Right' not in gui['Toolbar'].keys() or 'Top' not in gui['Toolbar'].keys() or 'Bottom' not in gui['Toolbar'].keys():
                return False
        return True


def checkGeneral(general):
    """
    Check if the general setting good to use

    Args:
        general:    general setting dictionary

    Return:
        True or false
    """
    if len(general.keys()) < 1:
        return False
    else:
        if 'RootPath' not in general.keys():
            return False
        if len(general['RootPath']) < 1:
            return False
        return True


def checkVisual(visual):
    """
    Check if the Visual setting good to use

    Args:
        visual: Visual setting dictionary

    Return:
        True or false
    """
    if len(visual.keys()) < 1:
        return False
    else:
        if 'Font' not in visual.keys():
            return False
        else:
            if len(visual['Font'].keys()) < 1:
                return False
            else:
                if 'Name' not in visual['Font'].keys() or 'Color' not in visual['Font'].keys() or 'Style' not in visual['Font'].keys() or 'Weight' not in visual['Font'].keys() or 'Size' not in visual['Font'].keys():
                    return False
                else:
                    if 'Line' not in visual.keys():
                        return False
                    else:
                        if len(visual['Line'].keys()) < 1:
                            return False
                        if 'Color' not in visual['Line'].keys() or 'Width' not in visual['Line'].keys() or 'Style' not in visual['Line'].keys() or 'MarkerStyle' not in visual['Line'].keys() or 'MarkerSize' not in visual['Line'].keys():
                            return False
                        if 'Image' not in visual.keys():
                            return False
                    if len(visual['Image'].keys()) < 1:
                        return False
                if 'Colormap' not in visual['Image'].keys():
                    return False
            if 'Interpolation' not in visual['Image'].keys():
                return False
        return True


def checkViewer(viewer):
    """
    Check if the Viewer setting good to use

    Args:
        viewer: Viewer setting dictionary

    Return:
        True or false
    """
    if len(viewer.keys()) < 1:
        return False
    else:
        if 'Viewer3D' not in viewer.keys():
            return False
        else:
            if len(viewer['Viewer3D'].keys()) < 1:
                return False
            else:
                if 'GoHome' not in viewer['Viewer3D'].keys():
                    return False
                else:
                    if 'ViewFrom' not in viewer['Viewer3D'].keys():
                        return False
                    else:
                        if len(viewer['Viewer3D']['ViewFrom'].keys()) < 1:
                            return False
                        else:
                            if 'Inline' not in viewer['Viewer3D']['ViewFrom'].keys():
                                return False
                            else:
                                if 'Crossline' not in viewer['Viewer3D']['ViewFrom'].keys():
                                    return False
                                else:
                                    if 'Z' not in viewer['Viewer3D']['ViewFrom'].keys():
                                        return False
                                    else:
                                        if 'Player' not in viewer.keys():
                                            return False
                                        if len(viewer['Player'].keys()) < 1:
                                            return False
                                        if 'First' not in viewer['Player'].keys():
                                            return False
                                    if 'Previous' not in viewer['Player'].keys():
                                        return False
                                if 'Next' not in viewer['Player'].keys():
                                    return False
                            if 'Last' not in viewer['Player'].keys():
                                return False
                        if 'Backward' not in viewer['Player'].keys():
                            return False
                    if 'Forward' not in viewer['Player'].keys():
                        return False
                if 'Pause' not in viewer['Player'].keys():
                    return False
            if 'Interval' not in viewer['Player'].keys():
                return False
        return True


def checkSettings(gui={}, general={}, visual={}, viewer={}):
    """
    Check if the Viewer setting good to use

    Args:
        viewer: Viewer setting dictionary

    Return:
        True or false
    """
    if checkGUI(gui) is False or checkGeneral(general) is False or checkVisual(visual) is False or checkViewer(viewer) is False:
        return False
    else:
        return True


class settings:
    GUI = GUI
    General = General
    Visual = Visual
    Viewer = Viewer
    checkGUI = checkGUI
    checkGeneral = checkGeneral
    checkVisual = checkVisual
    checkViewer = checkViewer
    Settings = {}
    Settings['General'] = General
    Settings['Gui'] = GUI
    Settings['Visual'] = Visual
    Settings['Viewer'] = Viewer
    checkSettings = checkSettings