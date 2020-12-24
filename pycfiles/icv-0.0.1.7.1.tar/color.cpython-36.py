# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rensike/Workspace/icv/icv/vis/color.py
# Compiled at: 2019-09-13 12:30:16
# Size of source mod 2**32: 4598 bytes
from ..utils.itis import is_seq, is_str
STANDARD_COLORS = [
 'AliceBlue', 'Chartreuse', 'Aqua', 'Aquamarine', 'Azure', 'Beige', 'Bisque',
 'BlanchedAlmond', 'BlueViolet', 'BurlyWood', 'CadetBlue', 'AntiqueWhite',
 'Chocolate', 'Coral', 'CornflowerBlue', 'Cornsilk', 'Crimson', 'Cyan',
 'DarkCyan', 'DarkGoldenRod', 'DarkGrey', 'DarkKhaki', 'DarkOrange',
 'DarkOrchid', 'DarkSalmon', 'DarkSeaGreen', 'DarkTurquoise', 'DarkViolet',
 'DeepPink', 'DeepSkyBlue', 'DodgerBlue', 'FireBrick', 'FloralWhite',
 'ForestGreen', 'Fuchsia', 'Gainsboro', 'GhostWhite', 'Gold', 'GoldenRod',
 'Salmon', 'Tan', 'HoneyDew', 'HotPink', 'IndianRed', 'Ivory', 'Khaki',
 'Lavender', 'LavenderBlush', 'LawnGreen', 'LemonChiffon', 'LightBlue',
 'LightCoral', 'LightCyan', 'LightGoldenRodYellow', 'LightGray', 'LightGrey',
 'LightGreen', 'LightPink', 'LightSalmon', 'LightSeaGreen', 'LightSkyBlue',
 'LightSlateGray', 'LightSlateGrey', 'LightSteelBlue', 'LightYellow', 'Lime',
 'LimeGreen', 'Linen', 'Magenta', 'MediumAquaMarine', 'MediumOrchid',
 'MediumPurple', 'MediumSeaGreen', 'MediumSlateBlue', 'MediumSpringGreen',
 'MediumTurquoise', 'MediumVioletRed', 'MintCream', 'MistyRose', 'Moccasin',
 'NavajoWhite', 'OldLace', 'Olive', 'OliveDrab', 'Orange', 'OrangeRed',
 'Orchid', 'PaleGoldenRod', 'PaleGreen', 'PaleTurquoise', 'PaleVioletRed',
 'PapayaWhip', 'PeachPuff', 'Peru', 'Pink', 'Plum', 'PowderBlue', 'Purple',
 'Red', 'RosyBrown', 'RoyalBlue', 'SaddleBrown', 'Green', 'SandyBrown',
 'SeaGreen', 'SeaShell', 'Sienna', 'Silver', 'SkyBlue', 'SlateBlue',
 'SlateGray', 'SlateGrey', 'Snow', 'SpringGreen', 'SteelBlue', 'GreenYellow',
 'Teal', 'Thistle', 'Tomato', 'Turquoise', 'Violet', 'Wheat', 'White',
 'WhiteSmoke', 'Yellow', 'YellowGreen']
DARK_COLORS = [
 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgrey', 'darkgreen',
 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred',
 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkslategrey',
 'darkturquoise', 'darkviolet']
LIGHT_COLORS = [
 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgreen',
 'lightgray', 'lightgrey', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue',
 'lightslategray', 'lightslategrey', 'lightsteelblue', 'lightyellow']
VIS_COLOR = [
 (244, 67, 54),
 (233, 30, 99),
 (156, 39, 176),
 (103, 58, 183),
 (63, 81, 181),
 (33, 150, 243),
 (3, 169, 244),
 (0, 188, 212),
 (0, 150, 136),
 (76, 175, 80),
 (139, 195, 74),
 (205, 220, 57),
 (255, 235, 59),
 (255, 193, 7),
 (255, 152, 0),
 (255, 87, 34),
 (121, 85, 72),
 (158, 158, 158),
 (96, 125, 139)]
MASK_COLORS = [
 (0, 0, 139),
 (67, 205, 128),
 (0, 206, 209),
 (255, 106, 106),
 (192, 255, 62),
 (130, 130, 130),
 (139, 87, 66),
 (25, 25, 112)]

def get_color_tuple(color, alpha=None):
    if alpha is not None:
        alpha = min(255, int(alpha)) if alpha > 1 else int(alpha * 255)
    elif isinstance(color, (int, float)):
        if color < 1:
            color = int(255 * color)
        color = min(255, int(color))
        if alpha is not None:
            return (color, color, color, alpha)
        else:
            return (
             color, color, color)
    else:
        if is_seq(color):
            color = tuple(color)[:4]
            if alpha is None:
                return color
            else:
                if len(color) == 3:
                    color = color + (alpha,)
                else:
                    if len(color) == 4:
                        color = color[:3] + alpha
                    else:
                        raise ValueError('color value invalid: ', color)
                return color
        if is_str(color):
            from PIL import ImageColor
            return ImageColor.getrgb(color)
        import numpy as np
        if isinstance(color, np.ndarray):
            if color.ndim == 1:
                return get_color_tuple((color.tolist()), alpha=alpha)
    raise ValueError('color value invalid: ', color)


def get_text_color():
    return (255, 255, 255)


def get_reverse_color(color):
    c = get_color_tuple(color)
    reverse_color = []
    for i in c:
        reverse_color.append(255 - i)

    return tuple(reverse_color)