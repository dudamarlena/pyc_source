# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/gopro2gpx/gpshelper.py
# Compiled at: 2020-04-17 10:12:09
# Size of source mod 2**32: 7049 bytes
from datetime import datetime
import time, os

class GPSPoint:

    def __init__(self, latitude=0.0, longitude=0.0, elevation=0.0, time=datetime.fromtimestamp(time.time()), speed=0.0):
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation
        self.time = time
        self.speed = speed
        self.hr = 0
        self.cad = 0
        self.cadence = 0
        self.temperature = 0
        self.atemp = 0
        self.power = 0
        self.distance = 0
        self.left_pedal_smoothness = 0
        self.left_torque_effectiveness = 0


def UTCTime(timedata):
    return timedata.strftime('%Y-%m-%dT%H:%M:%SZ')


def generate_GPX(points, trk_name='exercise'):
    """
    Creates a GPX in 1.1 Format
    """
    xml = '<?xml version="1.0" encoding="UTF-8"?>\r\n'
    gpx_attr = [
     'xmlns="http://www.topografix.com/GPX/1/1"',
     'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
     'xmlns:wptx1="http://www.garmin.com/xmlschemas/WaypointExtension/v1"',
     'xmlns:gpxtrx="http://www.garmin.com/xmlschemas/GpxExtensions/v3"',
     'xmlns:gpxtpx="http://www.garmin.com/xmlschemas/TrackPointExtension/v2"',
     'xmlns:gpxx="http://www.garmin.com/xmlschemas/GpxExtensions/v3"',
     'xmlns:trp="http://www.garmin.com/xmlschemas/TripExtensions/v1"',
     'xmlns:adv="http://www.garmin.com/xmlschemas/AdventuresExtensions/v1"',
     'xmlns:prs="http://www.garmin.com/xmlschemas/PressureExtension/v1"',
     'xmlns:tmd="http://www.garmin.com/xmlschemas/TripMetaDataExtensions/v1"',
     'xmlns:vptm="http://www.garmin.com/xmlschemas/ViaPointTransportationModeExtensions/v1"',
     'xmlns:ctx="http://www.garmin.com/xmlschemas/CreationTimeExtension/v1"',
     'xmlns:gpxacc="http://www.garmin.com/xmlschemas/AccelerationExtension/v1"',
     'xmlns:gpxpx="http://www.garmin.com/xmlschemas/PowerExtension/v1"',
     'xmlns:vidx1="http://www.garmin.com/xmlschemas/VideoExtension/v1"',
     'creator="Garmin Desktop App"',
     'version="1.1"',
     'xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd http://www.garmin.com/xmlschemas/WaypointExtension/v1 http://www8.garmin.com/xmlschemas/WaypointExtensionv1.xsd http://www.garmin.com/xmlschemas/TrackPointExtension/v2 http://www.garmin.com/xmlschemas/TrackPointExtensionv2.xsd http://www.garmin.com/xmlschemas/GpxExtensions/v3 http://www8.garmin.com/xmlschemas/GpxExtensionsv3.xsd http://www.garmin.com/xmlschemas/ActivityExtension/v1 http://www8.garmin.com/xmlschemas/ActivityExtensionv1.xsd http://www.garmin.com/xmlschemas/AdventuresExtensions/v1 http://www8.garmin.com/xmlschemas/AdventuresExtensionv1.xsd http://www.garmin.com/xmlschemas/PressureExtension/v1 http://www.garmin.com/xmlschemas/PressureExtensionv1.xsd http://www.garmin.com/xmlschemas/TripExtensions/v1 http://www.garmin.com/xmlschemas/TripExtensionsv1.xsd http://www.garmin.com/xmlschemas/TripMetaDataExtensions/v1 http://www.garmin.com/xmlschemas/TripMetaDataExtensionsv1.xsd http://www.garmin.com/xmlschemas/ViaPointTransportationModeExtensions/v1 http://www.garmin.com/xmlschemas/ViaPointTransportationModeExtensionsv1.xsd http://www.garmin.com/xmlschemas/CreationTimeExtension/v1 http://www.garmin.com/xmlschemas/CreationTimeExtensionsv1.xsd http://www.garmin.com/xmlschemas/AccelerationExtension/v1 http://www.garmin.com/xmlschemas/AccelerationExtensionv1.xsd http://www.garmin.com/xmlschemas/PowerExtension/v1 http://www.garmin.com/xmlschemas/PowerExtensionv1.xsd http://www.garmin.com/xmlschemas/VideoExtension/v1 http://www.garmin.com/xmlschemas/VideoExtensionv1.xsd"']
    xml += '<gpx ' + ' '.join(gpx_attr) + '>\r\n'
    xml += '<metadata>\r\n'
    xml += '  <time>%s</time>\r\n' % UTCTime(points[0].time)
    xml += '</metadata>\r\n'
    xml += '<trk>\r\n'
    xml += '  <name>%s</name>\r\n' % trk_name
    xml += '<trkseg>\r\n'
    for p in points:
        hr = p.hr
        cadence = p.cad
        speed = p.speed
        distance = p.distance
        pts = '\t<trkpt lat="%s" lon="%s">\r\n' % (p.latitude, p.longitude)
        pts += '\t\t<ele>%s</ele>\r\n' % p.elevation
        pts += '\t\t<time>%s</time>\r\n' % UTCTime(p.time)
        pts += '\t\t<extensions>\r\n'
        pts += '\t\t<gpxtpx:TrackPointExtension>\r\n'
        pts += '\t\t    <gpxtpx:hr>%s</gpxtpx:hr>\r\n' % hr
        pts += '\t\t    <gpxtpx:cad>%s</gpxtpx:cad>\r\n' % cadence
        pts += '\t\t    <gpxtpx:speed>%s</gpxtpx:speed>\r\n' % speed
        pts += '\t\t    <gpxtpx:distance>%s</gpxtpx:distance>\r\n' % distance
        pts += '\t\t   </gpxtpx:TrackPointExtension>\r\n'
        pts += '\t\t<gpxx:TrackPointExtension/>\r\n'
        pts += '\t\t</extensions>\r\n'
        pts += '\t</trkpt>\r\n'
        xml += pts
    else:
        xml += '</trkseg>\r\n'
        xml += '</trk>\r\n'
        xml += '</gpx>\r\n'
        return xml


def generate_KML(gps_points):
    """
    
    use this for color
    http://www.zonums.com/gmaps/kml_color/

    """
    kml_template = '<?xml version="1.0" encoding="UTF-8"?>\n    <kml xmlns="http://www.opengis.net/kml/2.2"> <Document>\n    <name>Demo</name>\n    <description>Description Demo</description> \n    <Style id="yellowLineGreenPoly">\n        <LineStyle>\n            <color>FF1400BE</color>\n            <width>4</width>\n            </LineStyle>\n        <PolyStyle>\n            <color>7f00ff00</color>\n        </PolyStyle>\n    </Style>\n    <Placemark>\n        <name>Track Title</name>\n        <description>Track Description</description>\n        <styleUrl>#yellowLineGreenPoly</styleUrl>\n        <LineString>\n            <extrude>1</extrude>\n            <tessellate>1</tessellate>\n            <altitudeMode>absolute</altitudeMode>\n            <coordinates> \n                %s\n            </coordinates>\n        </LineString> \n    </Placemark>\n    </Document>\n    </kml>\n    '
    lines = []
    for p in gps_points:
        s = '%s,%s,%s' % (p.longitude, p.latitude, p.elevation)
        lines.append(s)
    else:
        coords = os.linesep.join(lines)
        kml = kml_template % coords
        return kml