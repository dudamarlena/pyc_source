# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:/Users/HDi/Google Drive/ProgramCodes/Released/PyPI/cognitivegeo\cognitivegeo\src\vis\font.py
# Compiled at: 2019-12-13 22:46:40
# Size of source mod 2**32: 2684 bytes
import matplotlib.pyplot as plt
import sys, os
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
import cognitivegeo.src.vis.color as color
__all__ = [
 'font']
FontNameList = [
 'Arial', 'Helvetica', 'Segoe UI', 'Tahoma', 'Times New Roman', 'Verdana']
FontStyleList = ['Normal', 'Italic', 'Oblique']
FontWeightList = ['Normal', 'Light', 'Medium', 'Bold', 'Semibold', 'Heavy', 'Black']
FontSizeList = [i for i in range(1, 50)]

def updatePltFont(fontstyle):
    """
    Update the font style in matplotlib

    Args:
        fontstyle: Font style dictionary with the following keys: Name, Size, Weight, Color,

    Return:
        N/A
    """
    if fontstyle is None or len(fontstyle.keys()) < 1:
        return
    if 'Name' in fontstyle.keys():
        plt.rcParams['font.sans-serif'] = fontstyle['Name']
    if 'Size' in fontstyle.keys():
        plt.rcParams['font.size'] = fontstyle['Size']
        plt.rcParams['axes.titlesize'] = fontstyle['Size']
        plt.rcParams['axes.labelsize'] = fontstyle['Size']
    if 'Weight' in fontstyle.keys():
        plt.rcParams['font.weight'] = fontstyle['Weight'].lower()
        plt.rcParams['axes.titleweight'] = fontstyle['Weight'].lower()
        plt.rcParams['axes.labelweight'] = fontstyle['Weight'].lower()
    if 'Color' in fontstyle.keys():
        plt.rcParams['text.color'] = fontstyle['Color'].lower()
        plt.rcParams['axes.labelcolor'] = fontstyle['Color'].lower()
        plt.rcParams['xtick.color'] = fontstyle['Color'].lower()
        plt.rcParams['ytick.color'] = fontstyle['Color'].lower()


class font:
    FontNameList = FontNameList
    FontColorList = color.ColorList
    FontStyleList = FontStyleList
    FontWeightList = FontWeightList
    FontSizeList = FontSizeList
    updatePltFont = updatePltFont