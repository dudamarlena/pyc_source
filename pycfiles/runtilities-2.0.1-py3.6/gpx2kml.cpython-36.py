# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\running\gpx2kml.py
# Compiled at: 2012-12-15 11:57:46
# Size of source mod 2**32: 7339 bytes
import pdb, optparse, datetime, os.path
from lxml import etree
from pykml.factory import KML_ElementMaker as KML
from pykml.factory import GX_ElementMaker as GX
import gpxpy, gpxpy.geo
from loutilities import timeu
METERPMILE = 1609.3439941
t = timeu.asctime('%Y-%m-%dT%H:%M:%SZ')

def main():
    usage = 'usage: %prog [options] <gpxfile>\n\n'
    usage += 'where:\n'
    usage += '  <gpxfile>\tgpx formatted file'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-p', '--points', dest='points', action='store_true', help='specify if points output is desired', default=False)
    parser.add_option('-f', '--flyover', dest='flyover', action='store_true', help='specify if flyover output is desired', default=False)
    parser.add_option('-c', '--color', dest='color', help='track color if not flyover', default='641400FF')
    parser.add_option('-o', '--output', dest='output', help='output file', default=None)
    options, args = parser.parse_args()
    colors = {'pink':'64781EF0', 
     'blue':'64F01E14'}
    gpxfile = args.pop(0)
    if options.output == None:
        outfile = os.path.basename(gpxfile) + '.kml'
    else:
        outfile = options.output
    _GPX = open(gpxfile, 'r')
    gpx = gpxpy.parse(_GPX)
    stylename = 'sn_shaded_dot'
    color = colors[options.color]
    sty = KML.Style((KML.IconStyle(KML.scale(1.2), KML.Icon(KML.href('http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png')), KML.color(colors[options.color]))),
      id=stylename)
    iconstylename = '#sn_shaded_dot'
    doc = KML.Document(KML.Name('generated from {0}'.format(gpxfile)), KML.open(1))
    doc.append(sty)
    times = []
    coords = []
    dists = []
    points = []
    lastpoint = None
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                if not lastpoint:
                    lastpoint = point
                plon = point.longitude
                plat = point.latitude
                pelev = point.elevation
                points.append(point)
                thisdist = gpxpy.geo.distance(lastpoint.latitude, lastpoint.longitude, lastpoint.elevation, plat, plon, pelev)
                lastpoint = point
                dists.append(thisdist)
                ptime = t.dt2asc(point.time)
                times.append(ptime)
                coords.append('{lon},{lat},{alt}'.format(lon=plon, lat=plat, alt=0))

    if options.flyover:
        plm = KML.Placemark()
        doc.append(plm)
        track = GX.track()
        plm.append(track)
        for when in times:
            track.append(KML.when(when))

        for coord in coords:
            track.append(KML.coordinates(coord))

    else:
        if options.points:
            lasttime = t.asc2epoch(times[0])
            totdist = 0
            for i in range(len(times)):
                thistime = t.asc2epoch(times[i])
                dur = thistime - lasttime
                lasttime = thistime
                totdist += dists[i]
                ex = KML.ExtendedData(KML.Data(KML.displayName('time'), KML.value(times[i])), KML.Data(KML.displayName('duration'), KML.value(dur)), KML.Data(KML.displayName('totdistance'), KML.value(int(round(totdist)))))
                plm = KML.Placemark(KML.name(''), KML.styleUrl(iconstylename))
                plm.append(ex)
                plm.append(KML.Point(KML.altitudeMode('clampToGround'), KML.coordinates(coords[i])))
                doc.append(plm)

        else:
            if options.color:
                doc.append(KML.Style((KML.LineStyle(KML.color(colors[options.color]), KML.width(5))),
                  id=(options.color)))
                stylename = '#{0}'.format(options.color)
            plm = KML.Placemark(KML.name('runtrack'))
            if options.color:
                plm.append(KML.styleUrl(stylename))
            doc.append(plm)
            ls = KML.LineString(KML.altitudeMode('clampToGround'))
            plm.append(ls)
            kcoords = ''
            for coord in coords:
                kcoords += coord + ' \n'

            ls.append(KML.coordinates(kcoords))
    _GPX.close()
    kml = KML.kml(doc)
    docstr = etree.tostring(kml, pretty_print=True)
    OUT = open(outfile, 'w')
    OUT.write(docstr)
    OUT.close()


if __name__ == '__main__':
    main()