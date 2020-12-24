# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/advancedcaching/abstractmap.py
# Compiled at: 2011-04-23 08:43:29
import openstreetmap, logging
logger = logging.getLogger('abstractmap')
import geo, math

class AbstractMap():
    MAP_FACTOR = 0
    RADIUS_EARTH = 6371000.0
    CLICK_MAX_RADIUS = 7
    CLICK_CHECK_RADIUS = 17

    @classmethod
    def set_config(Map, map_providers, map_path, placeholder_cantload, placeholder_loading):
        Map.noimage_cantload = Map._load_tile(placeholder_cantload)
        Map.noimage_loading = Map._load_tile(placeholder_loading)
        Map.tile_loaders = []
        for (name, params) in map_providers:
            tl = openstreetmap.get_tile_loader(**dict([ (str(a), b) for (a, b) in params.items() ]))
            tl.noimage_loading = Map.noimage_loading
            tl.noimage_cantload = Map.noimage_cantload
            tl.base_dir = map_path
            Map.tile_loaders.append((name, tl))

    def __init__(self, center, zoom, tile_loader=None):
        self.active_tile_loaders = []
        self.double_size = False
        self.layers = []
        self.osd_message = None
        if tile_loader == None:
            self.tile_loader = self.tile_loaders[0][1]
        else:
            self.tile_loader = tile_loader
        self.dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.zoom = zoom
        self.total_map_width = 256 * 2 ** zoom
        self.set_center(center, False)
        return

    def add_layer(self, layer):
        self.layers.append(layer)
        layer.attach(self)

    def set_osd_message(self, message):
        self.osd_message = message

    def set_center(self, coord, update=True):
        if self.dragging:
            return
        (self.map_center_x, self.map_center_y) = self.deg2num(coord)
        self.center_latlon = coord
        self.draw_at_x = 0
        self.draw_at_y = 0
        if update:
            self._draw_map()

    def set_center_lazy(self, coord):
        if self.dragging:
            return
        (old_center_x, old_center_y) = self.coord2point(self.center_latlon)
        (new_center_x, new_center_y) = self.coord2point(coord)
        if abs(old_center_x - new_center_x) > self.map_width * self.LAZY_SET_CENTER_DIFFERENCE or abs(old_center_y - new_center_y) > self.map_height * self.LAZY_SET_CENTER_DIFFERENCE:
            self.set_center(coord)
            logger.debug('Not lazy!')
            return True
        logger.debug('Lazy!')
        return False

    def get_center(self):
        return self.center_latlon

    def relative_zoom(self, direction=None, update=True):
        if direction != None:
            self.set_zoom(self.zoom + direction, update)
        return

    def relative_zoom_preserve_center_at(self, screenpoint, direction):
        offs = (screenpoint[0] - self.map_width / 2.0, screenpoint[1] - self.map_height / 2.0)
        self.set_center(self.screenpoint2coord(screenpoint), False)
        self.relative_zoom(direction, False)
        self._move_map_relative(-offs[0], -offs[1])

    def set_zoom(self, newzoom, update=True):
        if newzoom < 0 or newzoom > self.tile_loader.MAX_ZOOM:
            return
        logger.debug('New zoom level: %d' % newzoom)
        self.zoom = newzoom
        self.total_map_width = 256 * 2 ** self.zoom
        self.set_center(self.center_latlon, update)

    def get_zoom(self):
        return self.zoom

    def get_max_zoom(self):
        return self.tile_loader.MAX_ZOOM

    def get_min_zoom(self):
        return 0

    def _move_map_relative(self, offset_x, offset_y, update=True):
        self.map_center_x += float(offset_x) / self.tile_loader.TILE_SIZE
        self.map_center_y += float(offset_y) / self.tile_loader.TILE_SIZE
        (self.map_center_x, self.map_center_y) = self.check_bounds(self.map_center_x, self.map_center_y)
        self.center_latlon = self.num2deg(self.map_center_x, self.map_center_y)
        if update:
            self._draw_map()

    def fit_to_bounds(self, minlat, maxlat, minlon, maxlon):
        if minlat == maxlat and minlon == maxlon:
            self.set_center(geo.Coordinate(minlat, minlon))
            self.set_zoom(self.get_max_zoom())
            return
        logger.debug('Settings Bounds: lat(%f, %f) lon(%f, %f)' % (minlat, maxlat, minlon, maxlon))
        req_deg_per_pix_lat = (maxlat - minlat) / self.map_height
        prop_zoom_lat = math.log(180.0 / req_deg_per_pix_lat / self.tile_loader.TILE_SIZE, 2)
        req_deg_per_pix_lon = (maxlon - minlon) / self.map_width
        prop_zoom_lon = math.log(360.0 / req_deg_per_pix_lon / self.tile_loader.TILE_SIZE, 2)
        target_zoom = math.floor(min(prop_zoom_lat, prop_zoom_lon))
        logger.debug('Proposed zoom lat: %f, proposed zoom lon: %f, target: %f' % (prop_zoom_lat, prop_zoom_lon, target_zoom))
        center = geo.Coordinate((maxlat + minlat) / 2.0, (maxlon + minlon) / 2.0)
        logger.debug('New Center: %s' % center)
        self.set_center(center, False)
        self.set_zoom(max(min(target_zoom, self.get_max_zoom()), self.get_min_zoom()))

    def set_double_size(self, ds):
        self.double_size = ds

    def get_double_size(self):
        return self.double_size

    def set_tile_loader(self, loader):
        self.tile_loader = loader
        self.emit('tile-loader-changed', loader)
        self.relative_zoom(0)

    def set_placeholder_images(self, cantload, loading):
        self.noimage_cantload = self._load_tile(cantload)
        self.noimage_loading = self._load_tile(loading)

    def point_in_screen(self, point):
        a = point[0] >= 0 and point[1] >= 0 and point[0] < self.map_width and point[1] < self.map_height
        return a

    def coord2point(self, coord):
        point = self.deg2num(coord)
        size = self.tile_loader.TILE_SIZE
        p_x = int(point[0] * size + self.map_width / 2) - self.map_center_x * size
        p_y = int(point[1] * size + self.map_height / 2) - self.map_center_y * size
        return (
         p_x % self.total_map_width, p_y)

    def coord2point_float(self, coord):
        point = self.deg2num(coord)
        size = self.tile_loader.TILE_SIZE
        p_x = point[0] * size + self.map_width / 2 - self.map_center_x * size
        p_y = point[1] * size + self.map_height / 2 - self.map_center_y * size
        return (
         p_x % self.total_map_width, p_y)

    def screenpoint2coord(self, point):
        size = self.tile_loader.TILE_SIZE
        coord = self.num2deg((point[0] - self.draw_at_x + self.map_center_x * size - self.map_width / 2) / size, (point[1] - self.draw_at_y + self.map_center_y * size - self.map_height / 2) / size)
        return coord

    def get_visible_area(self):
        a = self.screenpoint2coord((0, 0))
        b = self.screenpoint2coord((self.map_width, self.map_height))
        return (
         geo.Coordinate(min(a.lat, b.lat), min(a.lon, b.lon)), geo.Coordinate(max(a.lat, b.lat), max(a.lon, b.lon)))

    @staticmethod
    def in_area(coord, area):
        return coord.lat > area[0].lat and coord.lat < area[1].lat and coord.lon > area[0].lon and coord.lon < area[1].lon

    def _check_click(self, offset_x, offset_y, ev_x, ev_y):
        if offset_x ** 2 + offset_y ** 2 < self.CLICK_MAX_RADIUS ** 2:
            c = self.screenpoint2coord((ev_x, ev_y))
            c1 = self.screenpoint2coord([ev_x - self.CLICK_CHECK_RADIUS, ev_y - self.CLICK_CHECK_RADIUS])
            c2 = self.screenpoint2coord([ev_x + self.CLICK_CHECK_RADIUS, ev_y + self.CLICK_CHECK_RADIUS])
            for l in reversed(self.layers):
                if l.clicked_screen((ev_x, ev_y)) == False:
                    break
                if l.clicked_coordinate(c, c1, c2) == False:
                    break

            return True
        return False

    def tile_size(self):
        return self.tile_loader.TILE_SIZE

    def get_meters_per_pixel(self, lat):
        return math.cos(lat * math.pi / 180.0) * 2.0 * math.pi * self.RADIUS_EARTH / self.total_map_width

    def deg2tilenum(self, lat_deg, lon_deg):
        lat_rad = math.radians(lat_deg)
        n = 2 ** self.zoom
        xtile = int((lon_deg + 180) / 360 * n)
        ytile = int((1.0 - math.log(math.tan(lat_rad) + 1.0 / math.cos(lat_rad)) / math.pi) / 2.0 * n)
        return (
         xtile, ytile)

    def deg2num(self, coord):
        lat_rad = math.radians(coord.lat)
        n = 2 ** self.zoom
        xtile = (coord.lon + 180.0) / 360 * n
        ytile = (1.0 - math.log(math.tan(lat_rad) + 1.0 / math.cos(lat_rad)) / math.pi) / 2.0 * n
        return (
         xtile, ytile)

    def num2deg(self, xtile, ytile):
        n = 2 ** self.zoom
        lon_deg = xtile / n * 360.0 - 180.0
        lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
        lat_deg = lat_rad * 180.0 / math.pi
        return geo.Coordinate(lat_deg, lon_deg)

    def check_bounds(self, xtile, ytile):
        max_x = 2 ** self.zoom
        max_y = 2 ** self.zoom
        return (
         xtile % max_x,
         ytile % max_y)


class AbstractMapLayer():

    def __init__(self):
        self.result = None
        return

    def draw(self):
        pass

    def clicked_screen(self, screenpoint):
        pass

    def clicked_coordinate(self, center, topleft, bottomright):
        pass

    def resize(self):
        pass

    def attach(self, map):
        self.map = map

    def refresh(self):
        self.draw()
        self.map.refresh()


logger = logging.getLogger('abstractmarkslayer')

class AbstractMarksLayer(AbstractMapLayer):
    ARROW_OFFSET = 1.0 / 3.0
    ARROW_SHAPE = [(0, -2 + ARROW_OFFSET), (1, +1 + ARROW_OFFSET), (0, 0 + ARROW_OFFSET), (-1, 1 + ARROW_OFFSET), (0, -2 + ARROW_OFFSET)]

    def __init__(self):
        AbstractMapLayer.__init__(self)
        self.current_target = None
        self.gps_target_distance = None
        self.gps_target_bearing = None
        self.gps_data = None
        self.gps_last_good_fix = None
        self.gps_has_fix = None
        self.follow_position = False
        return

    def set_follow_position(self, value):
        logger.info('Setting "Follow position" to :' + repr(value))
        if value and not self.follow_position and self.gps_last_good_fix != None:
            self.map.set_center(self.gps_last_good_fix.position)
        self.follow_position = value
        return

    def get_follow_position(self):
        return self.follow_position

    def on_target_changed(self, caller, cache, distance, bearing):
        self.current_target = cache
        self.gps_target_distance = distance
        self.gps_target_bearing = bearing

    def on_good_fix(self, core, gps_data, distance, bearing):
        self.gps_data = gps_data
        self.gps_last_good_fix = gps_data
        self.gps_has_fix = True
        self.gps_target_distance = distance
        self.gps_target_bearing = bearing
        if self.map.dragging:
            return
        if self.follow_position and not self.map.set_center_lazy(self.gps_data.position) or not self.follow_position:
            self.draw()
            self.map.refresh()

    def on_no_fix(self, caller, gps_data, status):
        self.gps_data = gps_data
        self.gps_has_fix = False

    @staticmethod
    def _get_arrow_transformed(root_x, root_y, width, height, angle):
        multiply = height / (2 * (2 - AbstractMarksLayer.ARROW_OFFSET))
        offset_x = width / 2
        offset_y = height / 2
        s = multiply * math.sin(math.radians(angle))
        c = multiply * math.cos(math.radians(angle))
        arrow_transformed = [ (int(x * c + offset_x - y * s) + root_x, int(y * c + offset_y + x * s) + root_y) for (x, y) in AbstractMarksLayer.ARROW_SHAPE
                            ]
        return arrow_transformed


class AbstractGeocacheLayer(AbstractMapLayer):
    CACHE_SIZE = 20
    TOO_MANY_POINTS = 30
    CACHES_ZOOM_LOWER_BOUND = 9
    CACHE_DRAW_SIZE = 10
    MAX_NUM_RESULTS_SHOW = 100

    def __init__(self, get_geocaches_callback, show_cache_callback):
        AbstractMapLayer.__init__(self)
        self.show_name = False
        self.get_geocaches_callback = get_geocaches_callback
        self.visualized_geocaches = []
        self.show_cache_callback = show_cache_callback
        self.current_cache = None
        self.select_found = None
        return

    def set_show_name(self, show_name):
        self.show_name = show_name

    def set_current_cache(self, cache):
        self.current_cache = cache

    def clicked_coordinate(self, center, topleft, bottomright):
        mindistance = (center.lat - topleft.lat) ** 2 + (center.lon - topleft.lon) ** 2
        mincache = None
        for c in self.visualized_geocaches:
            dist = (c.lat - center.lat) ** 2 + (c.lon - center.lon) ** 2
            if dist < mindistance:
                mindistance = dist
                mincache = c

        if mincache != None:
            self.show_cache_callback(mincache)
        return False

    @staticmethod
    def shorten_name(s, chars):
        max_pos = chars
        min_pos = chars - 10
        NOT_FOUND = -1
        suffix = '…'
        length = len(s)
        if length <= max_pos:
            return s
        else:
            try:
                end = s.rindex('.', min_pos, max_pos)
            except ValueError:
                end = s.rfind(' ', min_pos, max_pos)
                if end == NOT_FOUND:
                    end = max_pos

            return s[0:end] + suffix