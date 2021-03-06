# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\papermap\markers.py
# Compiled at: 2019-12-17 14:34:08
# Size of source mod 2**32: 2436 bytes
from typing import Tuple
from PIL import Image, ImageDraw
from .utils import lat_to_y, lon_to_x, mm_to_px

class Ellipse(object):

    def __init__(self, lat: float, lon: float, width: int, height: int, color: str, outline: int=0, outline_color: str='white') -> None:
        self.lat = lat
        self.lon = lon
        self.width = width
        self.height = height
        self.outline = outline
        self.color = color
        self.outline_color = outline_color

    def render(self, image: Image, center_coord: Tuple[(int, int)], zoom: int, dpi: int=300, tile_size: int=256, antialias: int=4):
        self.width_px = round(mm_to_px(self.width, dpi))
        self.height_px = round(mm_to_px(self.height, dpi))
        self.outline_px = round(mm_to_px(self.outline, dpi))
        render_width = self.width_px + self.outline_px
        render_height = self.height_px + self.outline_px
        antialias_width = antialias * render_width
        antialias_height = antialias * render_height
        feature_image = Image.new('RGBA', (antialias_width, antialias_height), (255,
                                                                                0,
                                                                                0,
                                                                                0))
        draw = ImageDraw.Draw(feature_image)
        if self.outline:
            draw.ellipse(xy=[(0, 0), (antialias_width, antialias_height)], fill=(self.outline_color))
        draw.ellipse(xy=[(antialias * self.outline_px, antialias * self.outline_px),
         (
          antialias * self.width_px, antialias * self.height_px)],
          fill=(self.color))
        del draw
        feature_image = feature_image.resize((render_width, render_height), Image.ANTIALIAS)
        x = lon_to_x(self.lon, zoom)
        y = lat_to_y(self.lat, zoom)
        im_x_center, im_y_center = center_coord
        x_center = image.width / 2 - (im_x_center - x) * tile_size
        y_center = image.height / 2 - (im_y_center - y) * tile_size
        box = (
         round(x_center - render_width / 2),
         round(y_center - render_height / 2),
         round(x_center + render_width / 2),
         round(y_center + render_height / 2))
        image.paste(feature_image, box, feature_image)