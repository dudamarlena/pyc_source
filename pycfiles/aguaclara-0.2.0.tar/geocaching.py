# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/advancedcaching/geocaching.py
# Compiled at: 2011-04-23 08:59:57
try:
    from simplejson import dumps, loads
except (ImportError, AttributeError):
    from json import loads, dumps

from datetime import datetime
import logging, time, geo
logger = logging.getLogger('geocaching')

class GeocacheCoordinate(geo.Coordinate):
    LOG_NO_LOG = 0
    LOG_AS_FOUND = 1
    LOG_AS_NOTFOUND = 2
    LOG_AS_NOTE = 3
    TYPE_REGULAR = 'regular'
    TYPE_MULTI = 'multi'
    TYPE_VIRTUAL = 'virtual'
    TYPE_EVENT = 'event'
    TYPE_MYSTERY = 'mystery'
    TYPE_WEBCAM = 'webcam'
    TYPE_UNKNOWN = 'unknown'
    TYPE_EARTH = 'earth'
    TYPES = [
     TYPE_REGULAR,
     TYPE_MULTI,
     TYPE_VIRTUAL,
     TYPE_EVENT,
     TYPE_MYSTERY,
     TYPE_WEBCAM,
     TYPE_UNKNOWN,
     TYPE_EARTH]
    STATUS_NORMAL = 0
    STATUS_DISABLED = 1
    STATUS_ARCHIVED = 2
    STATUS_TEXT = ['normal', 'not available!']
    LOG_TYPE_FOUND = 'smile'
    LOG_TYPE_NOTFOUND = 'sad'
    LOG_TYPE_NOTE = 'note'
    LOG_TYPE_MAINTENANCE = 'maint'
    LOG_TYPE_PUBLISHED = 'greenlight'
    LOG_TYPE_DISABLED = 'disabled'
    LOG_TYPE_NEEDS_MAINTENANCE = 'needsmaint'
    LOG_TYPE_WILLATTEND = 'rsvp'
    LOG_TYPE_ATTENDED = 'attended'
    LOG_TYPE_UPDATE = 'coord_update'
    SIZES = [
     'other', 'micro', 'small', 'regular', 'big', 'other']
    TYPE_MAPPING = {TYPE_MULTI: 'Multi-cache', 
       TYPE_REGULAR: 'Traditional Cache', 
       TYPE_EARTH: 'Earthcache', 
       TYPE_UNKNOWN: 'Unknown Cache', 
       TYPE_EVENT: 'Event Cache', 
       TYPE_WEBCAM: 'Webcam Cache', 
       TYPE_VIRTUAL: 'Virtual Cache'}
    USER_TYPE_COORDINATE = 0
    USER_TYPE_CALC_STRING = 1
    USER_TYPE_CALC_STRING_OVERRIDE = 2
    ATTRS = ('lat', 'lon', 'title', 'name', 'shortdesc', 'desc', 'hints', 'type', 'size',
             'difficulty', 'terrain', 'owner', 'found', 'waypoints', 'images', 'notes',
             'fieldnotes', 'logas', 'logdate', 'marked', 'logs', 'status', 'vars',
             'alter_lat', 'alter_lon', 'updated', 'user_coordinates')
    SQLROW = {'lat': 'REAL', 
       'lon': 'REAL', 
       'name': 'TEXT PRIMARY KEY', 
       'title': 'TEXT', 
       'shortdesc': 'TEXT', 
       'desc': 'TEXT', 
       'hints': 'TEXT', 
       'type': 'TEXT', 
       'size': 'INTEGER', 
       'difficulty': 'INTEGER', 
       'terrain': 'INTEGER', 
       'owner': 'TEXT', 
       'found': 'INTEGER', 
       'waypoints': 'text', 
       'images': 'text', 
       'notes': 'TEXT', 
       'fieldnotes': 'TEXT', 
       'logas': 'INTEGER', 
       'logdate': 'TEXT', 
       'marked': 'INTEGER', 
       'logs': 'TEXT', 
       'status': 'INTEGER', 
       'vars': 'TEXT', 
       'alter_lat': 'REAL', 
       'alter_lon': 'REAL', 
       'updated': 'INTEGER', 
       'user_coordinates': 'TEXT'}

    def __init__(self, lat, lon=None, name='', data=None):
        geo.Coordinate.__init__(self, lat, lon, name)
        if data != None:
            self.unserialize(data)
            self.calc = None
            return
        else:
            self.calc = None
            self.title = ''
            self.shortdesc = ''
            self.desc = ''
            self.hints = ''
            self.type = ''
            self.size = -1
            self.difficulty = -1
            self.terrain = -1
            self.owner = ''
            self.found = False
            self.waypoints = ''
            self.images = ''
            self.notes = ''
            self.fieldnotes = ''
            self.logas = self.LOG_NO_LOG
            self.logdate = ''
            self.marked = False
            self.logs = ''
            self.status = self.STATUS_NORMAL
            self.vars = ''
            self.alter_lat = 0
            self.alter_lon = 0
            self.updated = 0
            self.user_coordinates = ''
            return

    def clone(self):
        n = GeocacheCoordinate(self.lat, self.lon)
        for k in self.ATTRS:
            setattr(n, k, getattr(self, k))

        return n

    def updated(self):
        self.updated = int(time.mktime(datetime.now().timetuple()))

    def get_updated(self):
        return datetime.fromtimestamp(self.updated)

    def get_difficulty(self):
        if self.difficulty != -1:
            return '%.1f' % (self.difficulty / 10.0)
        return '?'

    def get_terrain(self):
        if self.difficulty != -1:
            return '%.1f' % (self.terrain / 10.0)
        return '?'

    def get_status(self):
        if self.status != None:
            return self.STATUS_TEXT[self.status]
        else:
            return ''

    def serialize(self):
        ret = {}
        for key in self.ATTRS:
            ret[key] = self.serialize_one(key)

        return ret

    def serialize_one(self, attribute):
        if attribute == 'found':
            if self.found:
                return 1
            return 0
        else:
            if attribute == 'marked':
                if self.marked:
                    return 1
                return 0
            if attribute == 'vars':
                if self.calc != None:
                    return dumps(self.calc.get_vars())
                return ''
            if attribute == 'user_coordinates':
                try:
                    return dumps(self.saved_user_coordinates)
                except AttributeError:
                    return self.user_coordinates

            elif attribute == 'waypoints':
                try:
                    return dumps(self.saved_waypoints)
                except AttributeError:
                    return self.waypoints

            else:
                return getattr(self, attribute)
            return

    def unserialize(self, data):
        ret = {}
        for key in self.ATTRS:
            ret[key] = data[key]

        if ret['notes'] == None:
            self.notes = ''
        if ret['fieldnotes'] == None:
            self.fieldnotes = ''
        if ret['logs'] == None:
            self.logs = ''
        if ret['vars'] == None:
            self.vars = ''
        ret['found'] = ret['found'] == 1
        self.__dict__ = ret
        return

    def get_waypoints(self):
        try:
            return self.saved_waypoints
        except AttributeError:
            if self.waypoints in (None, '{}', ''):
                self.saved_waypoints = []
            else:
                self.saved_waypoints = loads(self.waypoints)
            return self.saved_waypoints

        return

    def get_user_coordinates(self, ctype):
        try:
            self.saved_user_coordinates
        except AttributeError:
            if self.user_coordinates in (None, '{}', ''):
                self.saved_user_coordinates = []
            else:
                self.saved_user_coordinates = loads(self.user_coordinates)
                if type(self.saved_user_coordinates) != list:
                    logger.debug('Creating new list!')
                    self.saved_user_coordinates = []

        return [ (id, point) for (id, point) in zip(range(len(self.saved_user_coordinates)), self.saved_user_coordinates) if point['type'] == ctype ]

    def get_user_coordinate(self, id):
        try:
            return self.saved_user_coordinates[id]
        except AttributeError:
            logger.exception('Call get_user_coordinates first!')
        except KeyError:
            raise Exception('No user coordinate with id %d' % id)

    def get_logs(self):
        if self.logs == None or self.logs == '':
            return []
        else:
            return loads(self.logs)

    def get_images(self):
        if self.images == None or self.images == '':
            return []
        else:
            try:
                return self.saved_images
            except AttributeError:
                self.saved_images = loads(self.images)
                return self.saved_images

            return

    def set_waypoints(self, wps):
        self.saved_waypoints = wps

    def set_logs(self, ls):
        self.logs = dumps(ls)

    def set_images(self, imgs):
        self.images = dumps(imgs)
        try:
            del self.saved_images
        except:
            pass

    def was_downloaded(self):
        return self.shortdesc != '' or self.desc != ''

    def get_bounds(self):
        minlat = maxlat = self.lat
        minlon = maxlon = self.lon
        for wpt in self.get_waypoints():
            if wpt['lat'] != -1 and wpt['lon'] != -1:
                minlat = min(minlat, wpt['lat'])
                maxlat = max(maxlat, wpt['lat'])
                minlon = min(minlon, wpt['lon'])
                maxlon = max(maxlon, wpt['lon'])

        return {'minlat': '%.5f' % minlat, 'maxlat': '%.5f' % maxlat, 'minlon': '%.5f' % minlon, 'maxlon': '%.5f' % maxlon}

    def get_size_string(self):
        if self.size == -1:
            return '?'
        else:
            return self.SIZES[self.size]

    def get_gs_type(self):
        if self.TYPE_MAPPING.has_key(self.type):
            return self.TYPE_MAPPING[self.type]
        else:
            return self.TYPE_MAPPING[self.TYPE_UNKNOWN]

    def set_alternative_position(self, coord):
        self.alter_lat = coord.lat
        self.alter_lon = coord.lon

    def start_calc(self, stripped_desc):
        from coordfinder import CalcCoordinateManager
        if self.vars == None or self.vars == '':
            vars = {}
        else:
            vars = loads(self.vars)
        self.calc = CalcCoordinateManager(vars)
        self.calc.add_text(stripped_desc, 'Description')
        for (id, local) in self.get_user_coordinates(self.USER_TYPE_CALC_STRING_OVERRIDE):
            (signature, replacement_text) = local['value']
            self.calc.add_replacement(signature, replacement_text, id)

        for (id, local) in self.get_user_coordinates(self.USER_TYPE_CALC_STRING):
            self.calc.add_text(local['value'], id)

        for w in self.get_waypoints():
            self.calc.add_text(w['comment'], 'Waypoint %s' % w['name'])

        self.calc.update()
        return

    def set_user_coordinate(self, type, value, name, id=None):
        d = {'value': value, 'type': type, 'name': name}
        try:
            if id == None:
                new_id = len(self.saved_user_coordinates)
                self.saved_user_coordinates.append(d)
                return new_id
            else:
                self.saved_user_coordinates[id] = d
                return id
        except AttributeError:
            raise Exception('get_user_coordinates has to be called first!')

        return

    def delete_user_coordinate(self, id):
        try:
            del self.saved_user_coordinates[id]
        except AttributeError:
            raise Exception('get_user_coordinates has to be called first!')

    def get_collected_coordinates(self, format, include_unknown=True, htmlcallback=lambda x: x, shorten_callback=lambda x: x):
        cache = self
        cache.display_text = 'Geocache: %s' % cache.get_latlon(format)
        cache.comment = 'Original coordinate given in the cache description.'
        cache.user_coordinate_id = None
        clist = {0: cache}
        check_double = []
        i = 1
        for w in self.get_waypoints():
            if not (w['lat'] == -1 and w['lon'] == -1):
                coord = geo.Coordinate(w['lat'], w['lon'], w['name'])
                coord.comment = htmlcallback(w['comment'])
                latlon = coord.get_latlon(format)
            elif not include_unknown:
                continue
            else:
                coord = geo.Coordinate(None, None, w['name'])
                coord.comment = htmlcallback(w['comment'])
                latlon = '???'
            check_double.append(latlon)
            coord.user_coordinate_id = None
            coord.display_text = '%s - %s - %s\n%s' % (w['name'], latlon, w['id'], shorten_callback(htmlcallback(w['comment'])))
            clist[i] = coord
            i += 1

        for (id, local) in self.get_user_coordinates(self.USER_TYPE_COORDINATE):
            coord = geo.Coordinate(*local['value'])
            text = local['name'] if local['name'] != '' else 'manually entered'
            coord.display_text = '%s: %s' % (text, coord.get_latlon(format))
            coord.comment = 'This coordinate was manually entered.'
            coord.user_coordinate_id = id
            clist[i] = coord
            i += 1

        if self.calc != None:
            for (coord, source) in self.calc.get_solutions():
                if coord == False:
                    continue
                if type(source) == int:
                    source_string = self.get_user_coordinate(source)['name']
                    coord.user_coordinate_id = source
                else:
                    source_string = source
                    coord.user_coordinate_id = None
                coord.display_text = '%s: %s = %s' % (source_string, coord.name, coord.get_latlon(format))
                coord.comment = 'From %s:\n%s = %s' % (source_string, coord.name, coord.get_latlon(format))
                clist[i] = coord
                i += 1

            for (coord, source) in self.calc.get_plain_coordinates():
                if coord == False:
                    continue
                if type(source) == int:
                    source_string = self.get_user_coordinate(source)['name']
                    coord.user_coordinate_id = source
                else:
                    source_string = source
                    coord.user_coordinate_id = None
                latlon = coord.get_latlon(format)
                if latlon in check_double:
                    continue
                coord.display_text = '%s: %s' % (source_string, latlon)
                coord.comment = 'Found in %s.' % source_string
                clist[i] = coord
                i += 1

        for coord in geo.search_coordinates(self.notes):
            coord.display_text = 'from notes: %s' % coord.get_latlon(format)
            coord.comment = 'This coordinate was manually entered in the notes field.'
            coord.user_coordinate_id = None
            clist[i] = coord
            i += 1

        return clist