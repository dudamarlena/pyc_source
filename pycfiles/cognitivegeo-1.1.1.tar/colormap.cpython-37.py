# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:/Users/HDi/Google Drive/ProgramCodes/Released/PyPI/cognitivegeo\cognitivegeo\src\vis\colormap.py
# Compiled at: 2019-12-05 18:40:27
# Size of source mod 2**32: 9001 bytes
import numpy as np
import matplotlib.colors as clr
__all__ = [
 'colormap']
ColorMapList = [
 'Seismic', 'Phase', 'Frequency', 'Red-White-Blue', 'Gray',
 'Black-White-Red', 'Black-White-Green', 'Black-White-Blue',
 'White-Red-Black', 'White-Green-Black', 'White-Blue-Black',
 'Black-Red', 'Black-Green', 'Black-Blue']
OpacityList = [
 '0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%',
 '___|⁻⁻⁻', '⁻⁻⁻|___',
 '__|⁻⁻|__', '⁻⁻|__|⁻⁻']

def makeOpacity(opacityname=None):
    if opacityname is None:
        opacityname = '100%'
    opac = np.ones([2001, 1])
    if opacityname == '0%':
        opac = opac * 0.0
    if opacityname == '10%':
        opac = opac * 0.1
    if opacityname == '20%':
        opac = opac * 0.2
    if opacityname == '30%':
        opac = opac * 0.3
    if opacityname == '40%':
        opac = opac * 0.4
    if opacityname == '50%':
        opac = opac * 0.5
    if opacityname == '60%':
        opac = opac * 0.6
    if opacityname == '70%':
        opac = opac * 0.7
    if opacityname == '80%':
        opac = opac * 0.8
    if opacityname == '90%':
        opac = opac * 0.9
    if opacityname == '100%':
        opac = opac * 1.0
    if opacityname == OpacityList[11]:
        opac[0:1001, :] = opac[0:1001, :] * 0.0
    if opacityname == OpacityList[12]:
        opac[1000:, :] = opac[1000:, :] * 0.0
    if opacityname == OpacityList[13]:
        opac[0:667, :] = opac[0:667, :] * 0.0
        opac[1334:, :] = opac[1334:, :] * 0.0
    if opacityname == OpacityList[14]:
        opac[667:1334, :] = opac[667:1334, :] * 0.0
    return opac


def makeColorMap(cmapname=None, flip=False, opacity='100%'):
    """
    Make common colormap used for data visualization
    Argus:
        cmapname:   name of colormap as listed below:
                        'Seismic', 'Phase', 'Frequency',
                        'Red-White-Blue',
                        'Black-White-Red', 'Black-White-Green', 'Black-White-Blue',
                        'Gray',
                        'White-Red-Black', 'White-Green-Black', 'White-Blue-Black',
                        'Black-Red', 'Black-Green', 'Black-Blue'
                    Default is 'Red-White-Blue'
        flip:       flip colormap or not
    Return:
         colormap
    """
    if cmapname is None:
        cmapname = 'Red-White-Blue'
    colormap = {}
    col_a = makeOpacity(opacity)
    col_loc = np.array([-1.0, -0.33, -0.2, 0.0, 0.2, 0.33, 1.0])
    col_r = np.array([161.0, 0.0, 77.0, 204.0, 97.0, 191.0, 255.0]) / 255.0
    col_g = np.array([255.0, 0.0, 77.0, 204.0, 69.0, 0.0, 255.0]) / 255.0
    col_b = np.array([255.0, 191.0, 77.0, 204.0, 0.0, 0.0, 0.0]) / 255.0
    col_r = np.interp(np.linspace(-1.0, 1.0, 2001), col_loc, col_r)
    col_g = np.interp(np.linspace(-1.0, 1.0, 2001), col_loc, col_g)
    col_b = np.interp(np.linspace(-1.0, 1.0, 2001), col_loc, col_b)
    col_r = np.reshape(col_r, [2001, 1])
    col_g = np.reshape(col_g, [2001, 1])
    col_b = np.reshape(col_b, [2001, 1])
    seismic = np.concatenate((col_r, col_g, col_b), axis=1)
    colormap['Seismic'] = seismic
    col_loc = np.linspace(0.0, 1.0, 11)
    col_r = np.array([255.0, 255.0, 255.0, 255.0, 198.0, 0.0, 0.0, 0.0, 0.0, 161.0, 255.0]) / 255.0
    col_g = np.array([0.0, 0.0, 114.0, 228.0, 255.0, 255.0, 255.0, 228.0, 114.0, 0.0, 0.0]) / 255.0
    col_b = np.array([255.0, 161.0, 0.0, 0.0, 0.0, 0.0, 198.0, 255.0, 255.0, 255.0, 255.0]) / 255.0
    col_r = np.interp(np.linspace(0.0, 1.0, 2001), col_loc, col_r)
    col_g = np.interp(np.linspace(0.0, 1.0, 2001), col_loc, col_g)
    col_b = np.interp(np.linspace(0.0, 1.0, 2001), col_loc, col_b)
    col_r = np.reshape(col_r, [2001, 1])
    col_g = np.reshape(col_g, [2001, 1])
    col_b = np.reshape(col_b, [2001, 1])
    phase = np.concatenate((col_r, col_g, col_b), axis=1)
    colormap['Phase'] = phase
    col_loc = np.linspace(0.0, 1.0, 11)
    col_r = np.array([0.0, 255.0, 255.0, 240.0, 147.0, 0.0, 0.0, 0.0, 0.0, 170.0, 255.0]) / 255.0
    col_g = np.array([0.0, 0.0, 190.0, 255.0, 255.0, 255.0, 255.0, 208.0, 85.0, 0.0, 0.0]) / 255.0
    col_b = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 120.0, 225.0, 255.0, 255.0, 255.0, 255.0]) / 255.0
    col_r = np.interp(np.linspace(0.0, 1.0, 2001), col_loc, col_r)
    col_g = np.interp(np.linspace(0.0, 1.0, 2001), col_loc, col_g)
    col_b = np.interp(np.linspace(0.0, 1.0, 2001), col_loc, col_b)
    col_r = np.reshape(col_r, [2001, 1])
    col_g = np.reshape(col_g, [2001, 1])
    col_b = np.reshape(col_b, [2001, 1])
    frequency = np.concatenate((col_r, col_g, col_b), axis=1)
    colormap['Frequency'] = frequency
    col_r = np.concatenate((np.ones([1001]), np.linspace(0.999, 0.0, 1000)))
    col_r = np.reshape(col_r, [2001, 1])
    col_g = np.concatenate((np.linspace(0.0, 1.0, 1001), np.linspace(0.999, 0.0, 1000)))
    col_g = np.reshape(col_g, [2001, 1])
    col_b = np.concatenate((np.linspace(0.0, 0.999, 1000), np.ones([1001])))
    col_b = np.reshape(col_b, [2001, 1])
    red_white_blue = np.concatenate((col_r, col_g, col_b), axis=1)
    colormap['Red-White-Blue'] = red_white_blue
    col_1 = np.concatenate((np.linspace(0.0, 0.999, 1000), np.ones([1001])))
    col_1 = np.reshape(col_1, [2001, 1])
    col_2 = np.concatenate((np.linspace(0.0, 1.0, 1001), np.linspace(0.999, 0.0, 1000)))
    col_2 = np.reshape(col_2, [2001, 1])
    black_white_red = np.concatenate((col_1, col_2, col_2), axis=1)
    black_white_green = np.concatenate((col_2, col_1, col_2), axis=1)
    black_white_blue = np.concatenate((col_2, col_2, col_1), axis=1)
    colormap['Black-White-Red'] = black_white_red
    colormap['Black-White-Green'] = black_white_green
    colormap['Black-White-Blue'] = black_white_blue
    col = np.linspace(1.0, 0.0, 2001)
    col = np.reshape(col, [2001, 1])
    white_gray_black = np.concatenate((col, col, col), axis=1)
    colormap['Gray'] = white_gray_black
    col_1 = np.concatenate((np.ones([1001]), np.linspace(0.999, 0.0, 1000)))
    col_1 = np.reshape(col_1, [2001, 1])
    col_2 = np.concatenate((np.linspace(1.0, 0.0, 1001), np.zeros([1000])))
    col_2 = np.reshape(col_2, [2001, 1])
    white_red_black = np.concatenate((col_1, col_2, col_2), axis=1)
    white_green_black = np.concatenate((col_2, col_1, col_2), axis=1)
    white_blue_black = np.concatenate((col_2, col_2, col_1), axis=1)
    colormap['White-Red-Black'] = white_red_black
    colormap['White-Green-Black'] = white_green_black
    colormap['White-Blue-Black'] = white_blue_black
    col_1 = np.linspace(0.0, 1.0, 2001)
    col_1 = np.reshape(col_1, [2001, 1])
    col_2 = np.zeros([2001])
    col_2 = np.reshape(col_2, [2001, 1])
    black_red = np.concatenate((col_1, col_2, col_2), axis=1)
    black_green = np.concatenate((col_2, col_1, col_2), axis=1)
    black_blue = np.concatenate((col_2, col_2, col_1), axis=1)
    colormap['Black-Red'] = black_red
    colormap['Black-Green'] = black_green
    colormap['Black-Blue'] = black_blue
    cmapdata = colormap['Red-White-Blue']
    if cmapname in colormap:
        cmapdata = colormap[cmapname]
    if flip:
        cmapdata = np.flipud(cmapdata)
    cmapdata = np.concatenate((cmapdata, col_a), axis=1)
    return clr.ListedColormap(cmapdata)


class colormap:
    ColorMapList = ColorMapList
    OpacityList = OpacityList
    makeColorMap = makeColorMap