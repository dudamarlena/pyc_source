# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\papermap\papermap.py
# Compiled at: 2019-12-17 17:45:10
# Size of source mod 2**32: 14583 bytes
import argparse, sys
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from io import BytesIO
from itertools import count
from math import ceil, floor
from pathlib import Path
from random import choice
from subprocess import Popen
from typing import Dict
import requests
from cachecontrol import CacheControl
from PIL import Image
from .constants import *
from .defaults import *
from .gpx import GPX
from .tile import Tile
from .utils import add_attribution_scale, add_grid, compute_scale, compute_scaled_size, compute_zoom, lat_to_y, lon_to_x, mm_to_px, utm_to_wgs84, rd_to_wgs84

class PaperMap(object):

    def __init__(self, lat: float, lon: float, tile_server: str=TILE_SERVER_DEFAULT, scale: int=SCALE_DEFAULT, size: str=SIZE_DEFAULT, dpi: int=DPI_DEFAULT, margin_top: int=MARGIN_DEFAULT, margin_bottom: int=MARGIN_DEFAULT, margin_left: int=MARGIN_DEFAULT, margin_right: int=MARGIN_DEFAULT, grid: str=GRID_DEFAULT, nb_workers: int=NB_WORKERS_DEFAULT, nb_retries: int=NB_RETRIES_DEFAULT, landscape: bool=False, quiet: bool=False, gpx: GPX=None, **kwargs) -> None:
        """
        Initialize the papermap

        Args:
            lat (float): latitude
            lon (float): longitude
            tile_server (str): Tile server to serve as the base of the paper map. Default: OpenStreetMap
            scale (int): scale of the paper map (in cm). Default: 25000
            size (str): size of the paper map. Default: A4
            dpi (int): dots per inch. Default: 300
            margin_top (int): top margin (in mm), Default: 12
            margin_bottom (int): bottom margin (in mm), Default: 12
            margin_left (int): left margin (in mm), Default: 12
            margin_right (int): right margin (in mm), Default: 12
            grid (str): coordinate grid to display on the paper map. Default: None
            nb_workers (int): number of workers (for parallelization). Default: 4
            nb_retries (int): number of retries (for failed tiles). Default: 3
            landscape (bool): use landscape orientation. Default: False
            quiet (bool): activate quiet mode. Default: False
            gpx (GPX): GPX object. Default: None
        """
        self.lat = lat
        self.lon = lon
        self.scale = scale
        self.dpi = dpi
        self.margin_top = mm_to_px(margin_top, self.dpi)
        self.margin_bottom = mm_to_px(margin_bottom, self.dpi)
        self.margin_left = mm_to_px(margin_left, self.dpi)
        self.margin_right = mm_to_px(margin_right, self.dpi)
        self.grid = grid
        self.nb_workers = nb_workers
        self.nb_retries = nb_retries
        self.use_landscape = landscape
        self.quiet_mode = quiet
        self.gpx = gpx
        try:
            self.tile_server = TILE_SERVERS_DICT[tile_server]
        except KeyError:
            if not self.quiet_mode:
                raise ValueError(f"Invalid tile server. Please choose one of {TILE_SERVER_CHOICES}")
            sys.exit()
        else:
            try:
                self.size = SIZES_DICT[size]
            except KeyError:
                if not self.quiet_mode:
                    raise ValueError(f"Invalid paper size. Please choose one of {SIZES_DICT}")
                sys.exit()
            else:
                self.zoom, self.zoom_scaled = compute_zoom(self.lat, self.scale, self.dpi)
                if self.zoom_scaled < self.tile_server['zoom_min'] or self.zoom_scaled > self.tile_server['zoom_max']:
                    if not self.quiet_mode:
                        raise ValueError('Scale out of bounds')
                    sys.exit()
                self.grid_size = mm_to_px(GRID_SIZE / self.scale, self.dpi)
                self.width = mm_to_px(self.size['h'] if self.use_landscape else self.size['w'], self.dpi)
                self.height = mm_to_px(self.size['w'] if self.use_landscape else self.size['h'], self.dpi)
                self.im_width = self.width - self.margin_left - self.margin_right
                self.im_height = self.height - self.margin_top - self.margin_bottom
                self.im_width_scaled, self.im_height_scaled = compute_scaled_size((
                 self.im_width, self.im_height), self.zoom, self.zoom_scaled)
                self.x_center = lon_to_x(self.lon, self.zoom_scaled)
                self.y_center = lat_to_y(self.lat, self.zoom_scaled)
                self.x_min = floor(self.x_center - 0.5 * self.im_width_scaled / TILE_SIZE)
                self.y_min = floor(self.y_center - 0.5 * self.im_height_scaled / TILE_SIZE)
                self.x_max = ceil(self.x_center + 0.5 * self.im_width_scaled / TILE_SIZE)
                self.y_max = ceil(self.y_center + 0.5 * self.im_height_scaled / TILE_SIZE)
                self.tiles = []
                for x in range(self.x_min, self.x_max):
                    for y in range(self.y_min, self.y_max):
                        max_tile = 2 ** self.zoom_scaled
                        x_tile = (x + max_tile) % max_tile
                        y_tile = (y + max_tile) % max_tile
                        box = (
                         round((x_tile - self.x_center) * TILE_SIZE + self.im_width_scaled / 2),
                         round((y_tile - self.y_center) * TILE_SIZE + self.im_height_scaled / 2),
                         round((x_tile + 1 - self.x_center) * TILE_SIZE + self.im_width_scaled / 2),
                         round((y_tile + 1 - self.y_center) * TILE_SIZE + self.im_height_scaled / 2))
                        self.tiles.append(Tile(x_tile, y_tile, self.zoom_scaled, box))
                    else:
                        self.paper_map = Image.new('RGB', (self.width, self.height), '#fff')
                        self.map_image_scaled = Image.new('RGB', (self.im_width_scaled, self.im_height_scaled), '#fff')
                        self.session = CacheControl(requests.Session())
                        self.session.headers = HEADERS

    def download_tiles--- This code section failed: ---

 L. 164         0  LOAD_GLOBAL              count
                2  LOAD_CONST               1
                4  CALL_FUNCTION_1       1  ''
                6  GET_ITER         
             8_10  FOR_ITER            300  'to 300'
               12  STORE_FAST               'nb_retry'

 L. 166        14  LOAD_LISTCOMP            '<code_object <listcomp>>'
               16  LOAD_STR                 'PaperMap.download_tiles.<locals>.<listcomp>'
               18  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               20  LOAD_DEREF               'self'
               22  LOAD_ATTR                tiles
               24  GET_ITER         
               26  CALL_FUNCTION_1       1  ''
               28  STORE_FAST               'tiles'

 L. 169        30  LOAD_FAST                'tiles'
               32  POP_JUMP_IF_TRUE     40  'to 40'

 L. 170        34  POP_TOP          
            36_38  JUMP_ABSOLUTE       300  'to 300'
             40_0  COME_FROM            32  '32'

 L. 173        40  LOAD_FAST                'nb_retry'
               42  LOAD_DEREF               'self'
               44  LOAD_ATTR                nb_retries
               46  COMPARE_OP               >
               48  POP_JUMP_IF_FALSE    92  'to 92'

 L. 174        50  LOAD_DEREF               'self'
               52  LOAD_ATTR                quiet_mode
               54  POP_JUMP_IF_TRUE     84  'to 84'

 L. 175        56  LOAD_GLOBAL              RuntimeError
               58  LOAD_STR                 'Could not download '
               60  LOAD_GLOBAL              len
               62  LOAD_FAST                'tiles'
               64  CALL_FUNCTION_1       1  ''
               66  FORMAT_VALUE          0  ''
               68  LOAD_STR                 ' tiles after '
               70  LOAD_DEREF               'self'
               72  LOAD_ATTR                nb_retries
               74  FORMAT_VALUE          0  ''
               76  LOAD_STR                 ' retries.'
               78  BUILD_STRING_5        5 
               80  CALL_FUNCTION_1       1  ''
               82  RAISE_VARARGS_1       1  'exception instance'
             84_0  COME_FROM            54  '54'

 L. 176        84  LOAD_GLOBAL              sys
               86  LOAD_METHOD              exit
               88  CALL_METHOD_0         0  ''
               90  POP_TOP          
             92_0  COME_FROM            48  '48'

 L. 179        92  LOAD_GLOBAL              ThreadPoolExecutor
               94  LOAD_DEREF               'self'
               96  LOAD_ATTR                nb_workers
               98  LOAD_CONST               ('max_workers',)
              100  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              102  SETUP_WITH          292  'to 292'
              104  STORE_DEREF              'executor'

 L. 180       106  LOAD_CLOSURE             'executor'
              108  LOAD_CLOSURE             'self'
              110  BUILD_TUPLE_2         2 
              112  LOAD_LISTCOMP            '<code_object <listcomp>>'
              114  LOAD_STR                 'PaperMap.download_tiles.<locals>.<listcomp>'
              116  MAKE_FUNCTION_8          'closure'

 L. 181       118  LOAD_FAST                'tiles'

 L. 180       120  GET_ITER         
              122  CALL_FUNCTION_1       1  ''
              124  STORE_FAST               'futures'

 L. 183       126  LOAD_GLOBAL              zip
              128  LOAD_FAST                'tiles'
              130  LOAD_FAST                'futures'
              132  CALL_FUNCTION_2       2  ''
              134  GET_ITER         
              136  FOR_ITER            288  'to 288'
              138  UNPACK_SEQUENCE_2     2 
              140  STORE_FAST               'tile'
              142  STORE_FAST               'future'

 L. 184       144  SETUP_FINALLY       230  'to 230'

 L. 185       146  LOAD_FAST                'future'
              148  LOAD_METHOD              result
              150  CALL_METHOD_0         0  ''
              152  STORE_FAST               'r'

 L. 187       154  LOAD_FAST                'r'
              156  LOAD_ATTR                status_code
              158  LOAD_CONST               200
              160  COMPARE_OP               ==
              162  POP_JUMP_IF_FALSE   196  'to 196'

 L. 189       164  LOAD_GLOBAL              Image
              166  LOAD_METHOD              open
              168  LOAD_GLOBAL              BytesIO
              170  LOAD_FAST                'r'
              172  LOAD_ATTR                content
              174  CALL_FUNCTION_1       1  ''
              176  CALL_METHOD_1         1  ''
              178  LOAD_METHOD              convert
              180  LOAD_STR                 'RGBA'
              182  CALL_METHOD_1         1  ''
              184  LOAD_FAST                'tile'
              186  STORE_ATTR               image

 L. 190       188  LOAD_CONST               True
              190  LOAD_FAST                'tile'
              192  STORE_ATTR               success
              194  JUMP_FORWARD        226  'to 226'
            196_0  COME_FROM           162  '162'

 L. 192       196  LOAD_DEREF               'self'
              198  LOAD_ATTR                quiet_mode
              200  POP_JUMP_IF_TRUE    226  'to 226'

 L. 193       202  LOAD_GLOBAL              print
              204  LOAD_STR                 'Request failed ['
              206  LOAD_FAST                'r'
              208  LOAD_ATTR                status_code
              210  FORMAT_VALUE          0  ''
              212  LOAD_STR                 ']: '
              214  LOAD_FAST                'r'
              216  LOAD_ATTR                url
              218  FORMAT_VALUE          0  ''
              220  BUILD_STRING_4        4 
              222  CALL_FUNCTION_1       1  ''
              224  POP_TOP          
            226_0  COME_FROM           200  '200'
            226_1  COME_FROM           194  '194'
              226  POP_BLOCK        
              228  JUMP_BACK           136  'to 136'
            230_0  COME_FROM_FINALLY   144  '144'

 L. 194       230  DUP_TOP          
              232  LOAD_GLOBAL              ConnectionError
              234  COMPARE_OP               exception-match
          236_238  POP_JUMP_IF_FALSE   284  'to 284'
              240  POP_TOP          
              242  STORE_FAST               'e'
              244  POP_TOP          
              246  SETUP_FINALLY       272  'to 272'

 L. 195       248  LOAD_DEREF               'self'
              250  LOAD_ATTR                quiet_mode
          252_254  POP_JUMP_IF_TRUE    268  'to 268'

 L. 196       256  LOAD_GLOBAL              print
              258  LOAD_GLOBAL              str
              260  LOAD_FAST                'e'
              262  CALL_FUNCTION_1       1  ''
              264  CALL_FUNCTION_1       1  ''
              266  POP_TOP          
            268_0  COME_FROM           252  '252'
              268  POP_BLOCK        
              270  BEGIN_FINALLY    
            272_0  COME_FROM_FINALLY   246  '246'
              272  LOAD_CONST               None
              274  STORE_FAST               'e'
              276  DELETE_FAST              'e'
              278  END_FINALLY      
              280  POP_EXCEPT       
              282  JUMP_BACK           136  'to 136'
            284_0  COME_FROM           236  '236'
              284  END_FINALLY      
              286  JUMP_BACK           136  'to 136'
              288  POP_BLOCK        
              290  BEGIN_FINALLY    
            292_0  COME_FROM_WITH      102  '102'
              292  WITH_CLEANUP_START
              294  WITH_CLEANUP_FINISH
              296  END_FINALLY      
              298  JUMP_BACK             8  'to 8'

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 36_38

    def render_base_layer(self):
        self.download_tiles()
        for tile in self.tiles:
            self.map_image_scaled.paste(tile.image, tile.box, tile.image)

    def render_gpx(self):
        if self.gpx is not None:
            self.gpx.render_tracks(self.map_image_scaled, (self.x_center, self.y_center), self.zoom_scaled, self.dpi, TILE_SIZE)
            self.gpx.render_waypoints(self.map_image_scaled, (self.x_center, self.y_center), self.zoom_scaled, self.dpi, TILE_SIZE)

    def render(self):
        self.render_base_layer()
        self.render_gpx()
        self.map_image = self.map_image_scaled.resize((self.im_width, self.im_height), Image.LANCZOS)
        if self.grid:
            add_grid(self.map_image, self.grid, self.grid_size, self.lat, self.lon, self.scale, self.dpi)
        add_attribution_scale(self.map_image, self.tile_server['attribution'], self.scale)
        self.paper_map.paste(self.map_image, (self.margin_left, self.margin_top))

    def show(self):
        self.paper_map.show()

    def save(self, file: Path, title: str=NAME, author: str=NAME):
        self.file = file
        self.paper_map.save((self.file), resolution=(self.dpi), title=title, author=author)

    def open(self):
        Popen([str(self.file)], shell=True)

    def __repr__(self):
        return f"PaperMap({self.lat}, {self.lon})"


def main():
    parser = argparse.ArgumentParser(prog=NAME, description=DESCRIPTION)
    parser.version = VERSION
    subparsers = parser.add_subparsers(title='inputs', dest='input', required=True)
    parser.add_argument('file', type=str, metavar='PATH', help='File path to save the paper map to')
    parser.add_argument('-t', '--tile_server', type=str, default=TILE_SERVER_DEFAULT, choices=TILE_SERVER_CHOICES,
      help='Tile server to serve as the base of the paper map')
    parser.add_argument('-sz', '--size', type=str, default=SIZE_DEFAULT, choices=SIZES_CHOICES,
      help='Size of the paper map')
    parser.add_argument('-sc', '--scale', type=int, default=SCALE_DEFAULT, metavar='CENTIMETERS',
      help='Scale of the paper map')
    parser.add_argument('-mt', '--margin_top', type=int, default=MARGIN_DEFAULT, metavar='MILLIMETERS',
      help='Top margin')
    parser.add_argument('-mb', '--margin_bottom', type=int, default=MARGIN_DEFAULT, metavar='MILLIMETERS',
      help='Bottom margin')
    parser.add_argument('-ml', '--margin_left', type=int, default=MARGIN_DEFAULT, metavar='MILLIMETERS',
      help='Left margin')
    parser.add_argument('-mr', '--margin_right', type=int, default=MARGIN_DEFAULT, metavar='MILLIMETERS',
      help='Right margin')
    parser.add_argument('-d', '--dpi', type=int, default=DPI_DEFAULT, metavar='NUMBER', help='Dots per inch')
    parser.add_argument('-g', '--grid', type=str, default=GRID_DEFAULT, choices=GRID_CHOICES, help='Coordinate grid to display on the paper map')
    parser.add_argument('-w', '--nb_workers', type=int, default=NB_WORKERS_DEFAULT, metavar='NUMBER',
      help='Number of workers (for parallelization)')
    parser.add_argument('-o', '--open', action='store_true', help='Open paper map after generating')
    parser.add_argument('-l', '--landscape', action='store_true', help='Use landscape orientation')
    parser.add_argument('-q', '--quiet', action='store_true', help='Activate quiet mode')
    parser.add_argument('-v', '--version', action='version', help=f"Display the current version of {NAME}")
    wgs84_parser = subparsers.add_parser('wgs84')
    wgs84_parser.add_argument('lat', type=float, metavar='LAT', help='Latitude')
    wgs84_parser.add_argument('lon', type=float, metavar='LON', help='Longitude')
    utm_parser = subparsers.add_parser('utm')
    utm_parser.add_argument('east', type=float, metavar='EASTING', help='Easting')
    utm_parser.add_argument('north', type=float, metavar='NORTHING', help='Northing')
    utm_parser.add_argument('zone', type=int, metavar='NUMBER', help='Zone number')
    utm_parser.add_argument('letter', type=str, metavar='LETTER', help='Zone letter')
    rd_parser = subparsers.add_parser('rd')
    rd_parser.add_argument('x', type=float, metavar='X', help='X')
    rd_parser.add_argument('y', type=float, metavar='Y', help='Y')
    gpx_parser = subparsers.add_parser('gpx')
    gpx_parser.add_argument('gpx_file', type=str, metavar='PATH', help='File path to the GPX file')
    gpx_parser.add_argument('-tc', '--track_color', type=str, default=TRACK_COLOR_DEFAULT, metavar='COLOR', help='Color to render tracks as')
    gpx_parser.add_argument('-wc', '--waypoint_color', type=str, default=WAYPOINT_COLOR_DEFAULT, metavar='COLOR', help='Color to render waypoints as')
    args = parser.parse_args()
    if args.input == 'wgs84':
        pass
    elif args.input == 'utm':
        args.lat, args.lon = utm_to_wgs84(args.east, args.north, args.zone, args.letter)
    else:
        if args.input == 'rd':
            args.lat, args.lon = rd_to_wgs84(args.x, args.y)
        else:
            if args.input == 'gpx':
                args.gpx = GPX(args.gpx_file, args.track_color, args.waypoint_color)
                args.lat, args.lon = args.gpx.center
            else:
                raise ValueError('Invalid input method. Please choose one of: wgs84, utm, rd or gpx')
    pm = PaperMap(**vars(args))
    pm.render()
    try:
        pm.save(args.file)
    except PermissionError:
        if not args.quiet:
            raise RuntimeError("Could not save paper map, please make sure you don't have it opened elsewhere")
        sys.exit()
    else:
        if args.open:
            pm.open()


if __name__ == '__main__':
    main()