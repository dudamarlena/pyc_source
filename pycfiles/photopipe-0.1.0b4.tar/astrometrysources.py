# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/max/Workspaces/gsfc/photometry_pipeline/code/reduction/astrom/astrometrysources.py
# Compiled at: 2016-11-15 15:22:29
import sys, numpy, os, astrometrystats, urllib, pyfits as pf
from astropy import wcs

class Obj:
    ra = 0.0
    dec = 0.0
    mag = 0.0
    ra_rad = 0.0
    dec_rad = 0.0

    def __init__(self, inra, indec, inmag):
        self.ra = inra
        self.dec = indec
        self.ra_rad = inra * numpy.pi / 180
        self.dec_rad = indec * numpy.pi / 180
        self.mag = inmag

    def rotate(self, dpa_deg, ra0, dec0):
        dpa_rad = dpa_deg * numpy.pi / 180
        sindpa = numpy.sin(dpa_rad)
        cosdpa = numpy.cos(dpa_rad)
        rascale = numpy.cos(dec0 * numpy.pi / 180)
        x = (self.ra - ra0) * rascale
        y = self.dec - dec0
        xrot = cosdpa * x - sindpa * y
        yrot = sindpa * x + cosdpa * y
        self.ra = xrot / rascale + ra0
        self.dec = yrot + dec0
        self.ra_rad = self.ra * numpy.pi / 180
        self.dec_rad = self.dec * numpy.pi / 180


class SexObj(Obj):
    x = 0.0
    y = 0.0
    mag = 0.0
    magerr = 0.0
    ellip = 0.0
    fwhm = 0.0
    flag = 0

    def __init__(self, row):
        self.x = row[0]
        self.y = row[1]
        self.ra = row[2]
        self.dec = row[3]
        self.mag = row[4]
        self.magerr = row[5]
        self.ellip = row[6]
        self.fwhm = row[7]
        self.flag = row[8]
        self.ra_rad = self.ra * numpy.pi / 180
        self.dec_rad = self.dec * numpy.pi / 180


def sextract(sexfilename, nxpix, nypix, border=3, corner=12, minfwhm=1.5, maxfwhm=25, maxellip=0.5, saturation=-1, sexpath='', quiet=False):
    if maxellip == -1:
        maxellip = 0.5
    if saturation > 0:
        sexsaturation = saturation
    else:
        sexsaturation = 900000.0
    try:
        if quiet == False:
            print sexpath + 'sex ' + sexfilename + ' -c sex.config -SATUR_LEVEL ' + str(sexsaturation)
        os.system(sexpath + 'sex ' + sexfilename + ' -c sex.config -SATUR_LEVEL ' + str(sexsaturation))
    except:
        print ' Error: Problem running sextractor'
        print ' Check that program is installed and runs at command line using ' + sexpath + 'sex'
        sys.exit(1)

    try:
        cat = numpy.loadtxt('temp.cat', dtype='float', comments='#')
    except:
        print 'Cannot load sextractor output file!'
        sys.exit(1)

    if len(cat) == 0:
        print 'Sextractor catalog is empty: try a different catalog?'
        sys.exit(1)
    minx = border
    miny = border
    maxx = nxpix - border
    maxy = nypix - border
    x = cat[:, 0]
    y = cat[:, 1]
    ra = cat[:, 2]
    dec = cat[:, 3]
    mag = cat[:, 4]
    magerr = cat[:, 5]
    ellip = cat[:, 6]
    fwhm = cat[:, 7]
    flag = cat[:, 8]
    a_imag = cat[:, 9]
    b_imag = cat[:, 10]
    mask = (ellip <= maxellip) & (fwhm >= minfwhm) & (fwhm <= maxfwhm) & (x >= minx) & (x <= maxx) & (y >= miny) & (y <= maxy) & (x + y >= corner) & (x + nypix - y >= corner) & (nxpix - x >= corner) & (nxpix - x + nypix - y >= corner) & (a_imag > 1) & (b_imag > 1)
    if saturation > 0:
        mask = mask & (flag == 0)
    fwhmlist = fwhm[mask]
    if len(fwhmlist) > 5:
        sfwhmlist = sorted(fwhmlist)
        fwhm20 = sfwhmlist[(len(fwhmlist) / 5)]
        fwhmmode = astrometrystats.most(sfwhmlist, vmax=0, vmin=0)
    else:
        fwhmmode = minfwhm
        fwhm20 = minfwhm
    refinedminfwhm = numpy.median([0.75 * fwhmmode, 0.9 * fwhm20, minfwhm])
    if quiet == False:
        print 'Refined min FWHM:', refinedminfwhm, 'pix'
    refwhmmask = fwhm > refinedminfwhm
    newmask = refwhmmask & mask
    goodsext = cat[newmask]
    sortedgoodsext = goodsext[goodsext[:, 4].argsort()]
    if quiet == False:
        print len(fwhmlist), 'objects detected in image (' + str(len(fwhmlist) - len(sortedgoodsext)) + ' discarded)'
    goodsexlist = []
    for value in sortedgoodsext:
        indObj = SexObj(value)
        goodsexlist.append(indObj)

    return goodsexlist


def getcatalog(catalog, ra, dec, boxsize, rawidth, decwidth, minmag=8.0, maxmag=-1, maxpm=60.0):
    if maxmag == -1:
        maxmag = 999
        if catalog == 'tmpsc':
            maxmag = 20.0
        if catalog == 'ub2':
            maxmag = 21.0
        if catalog == 'sdss':
            maxmag = 22.0
        if catalog == 'tmc':
            maxmag = 20.0
    if catalog == 'tmpsc' or catalog == 'ub2' or catalog == 'sdss' or catalog == 'tmc':
        usercat = 0
        racolumn = 1
        deccolumn = 2
        magcolumn = 6
        if catalog == 'tmpsc' or catalog == 'tmc':
            magcolumn = 3
        pmracolumn = 10
        pmdeccolumn = 11
        if catalog == 'sdss':
            queryurl = 'http://cas.sdss.org/dr7/en/tools/search/x_rect.asp?min_ra=' + str(ra - rawidth / 3600.0) + '&max_ra=' + str(ra + rawidth / 3600.0) + '&min_dec=' + str(dec - decwidth / 3600.0) + '&max_dec=' + str(dec + decwidth / 3600.0) + '&entries=top&topnum=6400&format=csv'
            racolumn = 7
            deccolumn = 8
            magcolumn = 12
            pmracolumn = 99
            pmdeccolumn = 99
            print queryurl
        else:
            queryurl = 'http://tdc-www.harvard.edu/cgi-bin/scat?catalog=' + catalog + '&ra=' + str(ra) + '&dec=' + str(dec) + '&system=J2000&dra=' + str(rawidth) + '&ddec=' + str(decwidth) + '&sort=mag&epoch=2000.00000&nstar=6400'
        cat = urllib.urlopen(queryurl)
        catlines = cat.readlines()
        cat.close()
        if len(catlines) > 6380:
            print 'WARNING: Reached maximum catalog query size.'
            print '         Gaps may be present in the catalog, leading to a poor solution or no solution.'
            print '         Decrease the search radius.'
    else:
        usercat = 1
        try:
            cat = open(catalog, 'r')
            print 'Reading user catalog ', catalog
        except:
            print 'Failed to open user catalog ', catalog
            print 'File not found or invalid online catalog.  Specify tmpsc, ub2, sdss, or tmc.'
            return []

        racolumn = 0
        deccolumn = 1
        magcolumn = -1
        catlines = cat.readlines()
        cat.close()
    if usercat == 1:
        comment = False
    else:
        comment = True
    catlist = []
    if catalog == 'sdss':
        comment = False
        catlines = catlines[1:]
    for line in catlines:
        if not comment:
            if catalog == 'sdss':
                cline = line.split(',')
            else:
                cline = line.split()
            narg = len(cline)
            if line[0:2] == '#:':
                inlinearg = line[2:].split(',')
                racolumn = int(inlinearg[0]) - 1
                deccolumn = int(inlinearg[1]) - 1
                if len(inlinearg) > 2:
                    magcolumn = int(inlinearg[2]) - 1
                continue
            if cline[racolumn].find(':') == -1:
                ra = float(cline[racolumn])
            else:
                ra = astrometrystats.rasex2deg(cline[racolumn])
            if cline[deccolumn].find(':') == -1:
                dec = float(cline[deccolumn])
            else:
                dec = astrometrystats.decsex2deg(cline[deccolumn])
            if magcolumn >= 0 and narg > magcolumn:
                try:
                    mag = float(cline[magcolumn])
                except:
                    mag = float(cline[magcolumn][0:-2])

            else:
                mag = maxmag
            if usercat == 0 and narg > pmracolumn and narg > pmdeccolumn:
                pmra = float(cline[pmracolumn])
                pmdec = float(cline[pmdeccolumn])
            else:
                pmra = pmdec = 0
            if mag > maxmag:
                continue
            if mag < minmag:
                continue
            if abs(pmra) > maxpm or abs(pmdec) > maxpm:
                continue
            iobj = Obj(ra, dec, mag)
            catlist.append(iobj)
        if line.find('---') != -1:
            comment = False

    catlist.sort(astrometrystats.magcomp)
    return catlist