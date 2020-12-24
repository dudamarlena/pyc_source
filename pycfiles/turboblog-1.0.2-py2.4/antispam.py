# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/turboblog/antispam.py
# Compiled at: 2007-03-25 08:41:47
"""
This function is (c) Jesus Roncero Franco <jesus at roncero.org>.
Modified to support old and new PIL versions by Steven Armstrong.
Modified to add distortion effect by Florent AIDE
        <florent d-o-t aide a-t gmail.com>.
"""
import os, random, StringIO
from PIL import ImageFont
from PIL.PngImagePlugin import Image
from PIL import ImageDraw
from PIL import ImageOps
XSTEP = 5
YSTEP = 5
WIDTH = 90
HEIGHT = 35
TEXT_POS_X = 25
TEXT_POS_Y = 11
IMAGE_SIZE = (WIDTH, HEIGHT)
BG_COLOR = (255, 255, 255)
GRID_INK = (200, 200, 200)
FONT_INK = (130, 130, 130)
FONT_SIZE = 14
FONT_PATH = os.path.abspath(os.path.join('turboblog', 'data', 'freesans.ttf'))
distortion_max = 15
distortion_min = 8

def generateImage(display_string):
    """
    generate a small image displaying a randomly distorted
    string using the passed argument.

    @param display_string: the string to display
    @type display_string: string
    """
    x1 = WIDTH - WIDTH + random.randrange(distortion_min, distortion_max)
    y1 = HEIGHT - HEIGHT + random.randrange(distortion_min, distortion_max)
    x2 = WIDTH - WIDTH + random.randrange(distortion_min, distortion_max)
    y2 = HEIGHT - random.randrange(distortion_min, distortion_max)
    x3 = WIDTH - random.randrange(distortion_min, distortion_max)
    y3 = HEIGHT - random.randrange(distortion_min, distortion_max)
    x4 = WIDTH - random.randrange(distortion_min, distortion_max)
    y4 = HEIGHT - HEIGHT + random.randrange(distortion_min, distortion_max)
    corners = (x1, y1, x2, y2, x3, y3, x4, y4)
    try:
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    except AttributeError:
        font = ImageFont()
        font._load_pilfont(FONT_PATH)

    img = Image.new('RGB', IMAGE_SIZE, BG_COLOR)
    draw = ImageDraw.Draw(img)
    (xsize, ysize) = img.size
    (x, y) = (0, 0)
    while x <= xsize:
        try:
            draw.line(((x, 0), (x, ysize)), fill=GRID_INK)
        except TypeError:
            draw.setink(GRID_INK)
            draw.line(((x, 0), (x, ysize)))

        x = x + XSTEP

    while y <= ysize:
        try:
            draw.line(((0, y), (xsize, y)), fill=GRID_INK)
        except TypeError:
            draw.setink(GRID_INK)
            draw.line(((0, y), (xsize, y)))

        y = y + YSTEP

    try:
        draw.text((TEXT_POS_X, TEXT_POS_Y), display_string, font=font, fill=FONT_INK)
    except TypeError:
        draw.setink(FONT_INK)
        draw.text((TEXT_POS_X, TEXT_POS_Y), display_string, font=font)

    return img.transform(img.size, Image.QUAD, corners, Image.BICUBIC)


def write_image(display_string):
    img = generateImage(display_string)
    s = StringIO.StringIO()
    img.save(s, 'PNG')
    return s.getvalue()