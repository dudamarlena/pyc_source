# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\cvttf\__init__.py
# Compiled at: 2019-06-03 04:37:44
# Size of source mod 2**32: 3856 bytes
import os
from typing import Tuple, Optional, Union, List
import numpy as np, cv2, PIL.Image, PIL.ImageFont, PIL.ImageDraw
from .char_range import find_supported_range as _find_supported_range

class Font:

    def __init__(self, TTF_path: Union[(str, List[str])], size: int=32):
        if not os.path.isfile(TTF_path):
            raise FileNotFoundError(f"TTF file: {TTF_path} does not exist.")
        self._font = PIL.ImageFont.truetype(TTF_path, size)

    @property
    def font(self) -> PIL.ImageFont.FreeTypeFont:
        return self._font


_CVTTF_ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
FONT_NOTO_SANS = Font(f"{_CVTTF_ROOT_PATH}\\fonts\\NotoSansCJKtc-hinted\\NotoSansCJKtc-Regular.otf")
COLOR_RED = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (255, 0, 0)
COLOR_YELLOW = (0, 255, 255)
COLOR_PURPLE = (255, 0, 255)
COLOR_CYAN = (255, 255, 0)

def putText(img: np.ndarray, text: str, org: Tuple[(int, int)], fontFace: Optional[Font]=None, fontScale=0.5, color: Tuple[int]=(255, 255, 255), thickness=None, lineType=None, bottomLeftOrigin: bool=False, multi_line: bool=True, use_fallback_font: bool=True) -> None:
    """
    putText(img, text, org, fontFace, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]]) -> img
    .   @brief Draws a text string.
    .
    .   Renders the specified text string in the image.
    .   To use TTF/OTF font files, check "Cvttf.Font"
    .
    .   @param img Image.
    .   @param text Text string to be drawn.
    .   @param org Bottom-left corner of the text string in the image.
    .   @param fontFace Font type, see cv::HersheyFonts.
    .   @param fontScale Font scale factor that is multiplied by the font-specific base size.
    .   @param color Text color.
    .   @param thickness Thickness of the lines used to draw a text.
    .   @param lineType Line type. See the line for details.
    .   @param bottomLeftOrigin When true, the image data origin is at the bottom-left corner. Otherwise,
    .   it is at the top-left corner.
    .   @param multi_line Draw the text at the next line whenever text exceeds image width.
    .   Also, starts a new line if "
" appears in the text.
    .   @param use_fallback_font Line type. See the line for details.
    """
    if len(img.shape) > 4 or len(img.shape) < 2 or img.dtype != np.uint8:
        raise TypeError('argument "img" should be an OpenCV image. (np.array with dtype=uint8)')
    else:
        if len(org) != 2:
            raise ValueError('argument "org" should be in the format of (x,y)')
        else:
            if len(img.shape) == 2:
                gray = True
                if len(color) == 3:
                    color = (
                     color[2] * 0.2126 + color[1] * 0.7152 + color[0] * 0.0722,)
            else:
                gray = False
            if len(color) != 3:
                if gray and len(color) == 1:
                    pass
                else:
                    raise ValueError('The length of "color" should be 3(RGB) or 1(grayscale)')
        if fontFace is None:
            fontFace = FONT_NOTO_SANS
    img_h, img_w = img.shape[0:2]
    font_img = PIL.Image.new('RGB', (img_w, img_h), color=(0, 0, 0))
    draw = PIL.ImageDraw.Draw(font_img)
    draw.text(org, text, font=(fontFace.font), fill=(color + (0, )))
    font_img = np.array(font_img)
    img[:] = np.where(font_img > 0, font_img, img)


def _determine_font():
    raise NotImplementedError('not implemented yet.')