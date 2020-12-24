# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/advancedcaching/gpsreader.py
# Compiled at: 2011-04-23 08:43:29
import geo
from socket import socket, AF_INET, SOCK_STREAM
from datetime import datetime
import logging
logger = logging.getLogger('gpsreader')
try:
    import location
except ImportError:
    logger.warning("If you're on maemo, please install python-location")

class Fix:
    BEARING_HOLD_EPD = 90
    last_bearing = 0
    min_timediff = datetime.utcnow() - datetime.utcfromtimestamp(0)

    def __init__(self, position=None, altitude=None, bearing=None, speed=None, sats=0, sats_known=0, dgps=False, quality=0, error=0, error_bearing=0, timestamp=None):
        self.position = position
        self.altitude = altitude
        self.bearing = bearing
        self.speed = speed
        self.sats = sats
        self.sats_known = sats_known
        self.dgps = dgps
        self.quality = quality
        self.error = error
        self.error_bearing = error_bearing
        if timestamp == None:
            self.timestamp = datetime.utcnow()
        else:
            self.timestamp = timestamp
        return


class GpsReader:
    BEARING_HOLD_SPEED = 0.62
    QUALITY_LOW_BOUND = 5.0
    DGPS_ADVANTAGE = 1
    PORT = 2947
    HOST = '127.0.0.1'
    EMPTY = Fix()

    def __init__(self):
        logger.info('Using GPSD gps reader on port %d host %s' % (self.PORT, self.HOST))
        self.status = 'connecting...'
        self.connected = False
        self.last_bearing = 0

    def connect(self):
        try:
            self.gpsd_connection = socket(AF_INET, SOCK_STREAM)
            self.gpsd_connection.connect((self.HOST, self.PORT))
            self.gpsd_connection.setblocking(False)
            self.status = 'connected'
            self.connected = True
        except:
            text = 'Could not connect to GPSD!'
            logger.warning(text)
            self.status = text
            self.connected = False

    def get_data(self):
        try:
            if not self.connected:
                self.connect()
                if not self.connected:
                    return self.EMPTY
            self.gpsd_connection.send('o\r\n')
            data = self.gpsd_connection.recv(512)
            self.gpsd_connection.send('y\r\n')
            quality_data = self.gpsd_connection.recv(512)
            if quality_data.strip() == 'GPSD,Y=?':
                sats = 0
                sats_known = 0
                dgps = False
            else:
                sats = 0
                dgps = False
                groups = quality_data.split(':')
                sats_known = int(groups[0].split(' ')[2])
                for i in xrange(1, sats_known):
                    sat_data = groups[i].split(' ')
                    if sat_data[4] == '1':
                        sats = sats + 1
                    if int(sat_data[0]) > 32:
                        dgps = True

                if data.strip() == 'GPSD,O=?':
                    self.status = 'No GPS signal'
                    return Fix(sats=sats, sats_known=sats_known, dgps=dgps)
                try:
                    splitted = data.split(' ')
                    (lat, lon, alt, err_hor) = splitted[3:7]
                    (track, speed) = splitted[8:10]
                    err_track = splitted[11]
                    time = datetime.utcfromtimestamp(int(float(splitted[1])))
                except:
                    logger.info('GPSD Output: \n%s\n  -- cannot be parsed.' % data)
                    self.status = 'Could not read GPSD output.'
                    return Fix()
                else:
                    alt = self.to_float(alt)
                    track = self.to_float(track)
                    speed = self.to_float(speed)
                    err_hor = self.to_float(err_hor)
                    err_track = self.to_float(err_track)
                    if dgps:
                        err_hor -= self.DGPS_ADVANTAGE
                    if err_hor <= 0:
                        quality = 1
                    elif err_hor > self.QUALITY_LOW_BOUND:
                        quality = 0
                    else:
                        quality = 1 - err_hor / self.QUALITY_LOW_BOUND

                return Fix(position=geo.Coordinate(float(lat), float(lon)), altitude=alt, bearing=track, speed=speed, sats=int(sats), sats_known=sats_known, dgps=dgps, quality=quality, error=err_hor, error_bearing=err_track, timestamp=time)
        except Exception, e:
            logger.exception('Fehler beim Auslesen der Daten: %s ' % e)
            return self.EMPTY

    @staticmethod
    def to_float(string):
        try:
            return float(string)
        except:
            return 0.0


class LocationGpsReader:
    TIMEOUT = 5
    BEARING_HOLD_SPEED = 2.5

    def __init__(self, cb_error, cb_changed):
        logger.info('Using liblocation GPS device')
        control = location.GPSDControl.get_default()
        device = location.GPSDevice()
        control.set_properties(preferred_method=location.METHOD_CWP | location.METHOD_ACWP | location.METHOD_GNSS | location.METHOD_AGNSS, preferred_interval=location.INTERVAL_1S)
        control.connect('error-verbose', cb_error)
        device.connect('changed', cb_changed)
        self.last_gps_bearing = 0
        self.control = control
        self.device = device

    def start(self):
        self.control.start()
        return False

    @staticmethod
    def get_error_from_code(error):
        if error == location.ERROR_USER_REJECTED_DIALOG:
            return 'Requested GPS method not enabled'
        if error == location.ERROR_USER_REJECTED_SETTINGS:
            return 'Location disabled due to change in settings'
        if error == location.ERROR_BT_GPS_NOT_AVAILABLE:
            return 'Problems with BT GPS'
        if error == location.ERROR_METHOD_NOT_ALLOWED_IN_OFFLINE_MODE:
            return 'Requested method is not allowed in offline mode'
        if error == location.ERROR_SYSTEM:
            return 'System error'

    def fix_from_tuple(self, f, device):
        a = Fix()
        if not f[1] & (location.GPS_DEVICE_LATLONG_SET | location.GPS_DEVICE_ALTITUDE_SET | location.GPS_DEVICE_TRACK_SET):
            return a
        a.sats = device.satellites_in_use
        a.sats_known = device.satellites_in_view
        a.dgps = False
        a.quality = 0
        if f[2] == f[2]:
            a.timestamp = datetime.utcfromtimestamp(f[2])
        else:
            a.timestamp = datetime.utcfromtimestamp(0)
        Fix.min_timediff = min(Fix.min_timediff, datetime.utcnow() - a.timestamp)
        if (datetime.utcnow() - a.timestamp - Fix.min_timediff).seconds > LocationGpsReader.TIMEOUT:
            logger.info('Discarding fix: Timestamp diff is %d, should not be > %d' % ((datetime.utcnow() - a.timestamp - Fix.min_timediff).seconds, LocationGpsReader.TIMEOUT))
            return a
        a.altitude = f[7]
        a.speed = f[11]
        if a.speed > self.BEARING_HOLD_SPEED:
            a.bearing = f[9]
            self.last_gps_bearing = a.bearing
        else:
            a.bearing = self.last_gps_bearing
        a.position = geo.Coordinate(f[4], f[5])
        a.error = f[6] / 100.0
        a.error_bearing = f[10]
        return a


class FakeGpsReader:
    INC = 0.0001

    def __init__(self, something):
        self.status = 'Fake GPS reader.'
        self.index = -1
        self.data = [ x.split('\t') for x in self.TESTDATA.split('\n') ]
        self.lastpos = None
        return

    @staticmethod
    def get_target():
        return geo.Coordinate(50.0000798795372, 6.99494680203497)

    def get_data(self):
        import random
        if self.index < len(self.data) - 1:
            self.index += 1
        if self.data[self.index][0] == '0':
            return Fix()
        else:
            pos = geo.Coordinate(float(self.data[self.index][0]), float(self.data[self.index][1]))
            if self.lastpos != None:
                bearing = self.lastpos.bearing_to(pos)
            else:
                bearing = 0
            self.lastpos = pos
            return Fix(position=pos, altitude=5, bearing=bearing, speed=4, sats=12, sats_known=6, dgps=True, quality=0, error=random.randrange(10, 100), error_bearing=10)

    TESTDATA = '0\t0\n0\t0\n0\t0\n50.0000000000000000\t7.0000000000000000\n49.9999706633389000\t7.0001229625195300\n49.9997950624675000\t7.0003442447632600\n49.9997997563332000\t7.0004659499973100\n49.9997218046337000\t7.0005903374403700\n49.9995578546077000\t7.0006271339952900\n49.9994435254484000\t7.0008635874837600\n49.9993037991226000\t7.0009828619659000\n49.9992146994919000\t7.0010608136653900\n49.9991217441857000\t7.0012173876166300\n49.9990843608975000\t7.0012444611638800\n49.9990095943213000\t7.0015110895037700\n49.9988885596395000\t7.0016821641475000\n0\t0\n0\t0\n0\t0\n49.9987537786365000\t7.0018086470663600\n49.9985118769109000\t7.0020990800112500\n49.9983842205256000\t7.0021572504192600\n49.9982605036348000\t7.0022816378623300\n49.9980872496963000\t7.0023336894810200\n49.9979986529797000\t7.0024224538356100\n49.9979185219854000\t7.0025429017841800\n49.9978181067854000\t7.0025481823831800\n49.9976762011647000\t7.0025224499404400\n49.9975882750005000\t7.0024726614356000\n49.9974449444562000\t7.0023075379431300\n49.9973412603140000\t7.0022041890770200\n49.9972049705684000\t7.0021101441234400\n0\t0\n0\t0\n0\t0\n49.9970952514559000\t7.0020336173474800\n49.9969987757504000\t7.0019501335918900\n49.9968421179801000\t7.0017190445214500\n49.9967520125210000\t7.0016104150563500\n49.9966504238546000\t7.0015143584460000\n49.9965638387948000\t7.0014302041381600\n49.9964761640877000\t7.0013357400894200\n49.9963049218059000\t7.0011528469622100\n49.9962143134326000\t7.0009845383465300\n49.9961593281478000\t7.0008703768253300\n49.9960857350379000\t7.0007528625428700\n49.9960248824209000\t7.0006081908941300\n49.9959259759635000\t7.0004951190203400\n49.9958231300116000\t7.0003485195338700\n49.9957155063748000\t7.0002043507993200\n49.9956013448536000\t7.0000658817589300\n49.9954995047301000\t6.9999083019793000\n49.9954301863909000\t6.9997342936694600\n49.9954084772617000\t6.9995050486177200\n49.9953969940543000\t6.9992866162210700\n49.9965626653284000\t6.9970068223774400\n49.9966021440923000\t6.9968105182051700\n49.9968151282519000\t6.9966180697083500\n49.9971344787627000\t6.9964923411607700\n49.9972403421998000\t6.9964339192956700\n49.9973804876208000\t6.9963862262666200\n49.9979287479073000\t6.9956857506185800\n49.9980570748448000\t6.9955223873257600\n49.9982320051640000\t6.9954270012676700\n49.9984868150204000\t6.9951742030680200\n49.9985938519239000\t6.9949829280376400\n49.9986792635173000\t6.9948330596089400\n49.9987863004208000\t6.9947258550673700\n49.9990340694785000\t6.9947269447147800\n49.9992224946618000\t6.9946833588182900\n49.9994972534478000\t6.9947828520089400\n49.9996298551559000\t6.9948167987167800\n49.9997046217322000\t6.9948615580797200\n49.9997673183680000\t6.9949107598513400\n49.9999811407179000\t6.9948655813932400\n50.0000479444861000\t6.9948898889124400\n50.0000799633563000\t6.9948716163635300\n50.0000798795372000\t6.9949468020349700'