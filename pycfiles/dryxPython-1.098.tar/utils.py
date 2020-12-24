# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dave/Dropbox/github_projects/dryxPython/dryxPython/kws/utils.py
# Compiled at: 2013-08-05 10:12:52
import time, os, sys
from datetime import datetime
import math, warnings
warnings.filterwarnings('ignore', '.*the sets module is deprecated.*', DeprecationWarning, 'MySQLdb')

def dbConnect(lhost, luser, lpasswd, ldb, quitOnError=True):
    import MySQLdb
    try:
        conn = MySQLdb.connect(host=lhost, user=luser, passwd=lpasswd, db=ldb)
    except MySQLdb.Error as e:
        print 'Error %d: %s' % (e.args[0], e.args[1])
        if quitOnError:
            sys.exit(1)
        else:
            conn = None

    return conn


def getDSS2Image(ra, dec, x, y):
    from BeautifulSoup import BeautifulSoup
    import urllib2, urllib, urlparse
    baseurl = 'http://archive.eso.org'
    url = baseurl + '/dss/dss/image'
    values = {'ra': ra, 'dec': dec, 
       'name': '', 
       'x': x, 
       'y': y, 
       'Sky-Survey': 'DSS-2-red', 
       'equinox': 'J2000'}
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    the_page = response.read()
    soup = BeautifulSoup(BeautifulSoup(the_page).prettify())
    for a in soup.findAll('a'):
        if not a['href'].startswith('http'):
            a['href'] = urlparse.urljoin(baseurl, a['href'])

    for img in soup.findAll('img'):
        if not img['src'].startswith('http'):
            img['src'] = urlparse.urljoin(baseurl, img['src'])

    return soup


def bin(x, digits=0):
    oct2bin = ['000', '001', '010', '011', '100', '101', '110', '111']
    binstring = [ oct2bin[int(n)] for n in oct(x) ]
    return ('').join(binstring).lstrip('0').zfill(digits)


def ra_to_sex(ra, delimiter=':'):
    ra_hh = int(ra / 15)
    ra_mm = int((ra / 15 - ra_hh) * 60)
    ra_ss = int(((ra / 15 - ra_hh) * 60 - ra_mm) * 60)
    ra_ff = int((((ra / 15 - ra_hh) * 60 - ra_mm) * 60 - ra_ss) * 100)
    return '%02d' % ra_hh + delimiter + '%02d' % ra_mm + delimiter + '%02d' % ra_ss + '.' + '%02d' % ra_ff


def dec_to_sex(dec, delimiter=':'):
    if dec >= 0:
        hemisphere = '+'
    else:
        hemisphere = '-'
        dec *= -1
    dec_deg = int(dec)
    dec_mm = int((dec - dec_deg) * 60)
    dec_ss = int(((dec - dec_deg) * 60 - dec_mm) * 60)
    dec_f = int((((dec - dec_deg) * 60 - dec_mm) * 60 - dec_ss) * 10)
    return hemisphere + '%02d' % dec_deg + delimiter + '%02d' % dec_mm + delimiter + '%02d' % dec_ss + '.' + '%01d' % dec_f


def coords_dec_to_sex(ra, dec, delimiter=':'):
    return (
     ra_to_sex(ra, delimiter), dec_to_sex(dec, delimiter))


def ra_in_decimal_hours(ra):
    return ra / 15.0


def baseN(num, base=26, numerals='abcdefghijklmnopqrstuvwxyz'):
    if num == 0:
        return numerals[0]
    else:
        if num < 0:
            return '-' + baseN(-1 * num, base, numerals)
        if not 2 <= base <= len(numerals):
            raise ValueError('Base must be between 2-%d' % len(numerals))
        left_digits = num // base
        if left_digits == 0:
            return numerals[(num % base)]
        return baseN(left_digits, base, numerals) + numerals[(num % base)]


def base26(num):
    if num < 0:
        raise ValueError('Number must be positive or zero')
    return baseN(num).rjust(3, 'a')


class DictLookup(dict):
    """
   a dictionary which can lookup value by key, or keys by value
   """

    def __init__(self, items=[]):
        """items can be a list of pair_lists or a dictionary"""
        dict.__init__(self, items)

    def get_key(self, value):
        """find the key(s) as a list given a value"""
        return [ item[0] for item in self.items() if item[1] == value ]

    def get_value(self, key):
        """find the value given a key"""
        return self[key]


def getFlagDefs(flags, dictionary, delimiter=' + '):
    flagDefs = []
    lookup = DictLookup(dictionary)
    for i in range(8):
        mask = 128 >> i
        try:
            if flags & mask:
                flagDefs.append(('').join(lookup.get_key(flags & mask)))
        except TypeError:
            return ''

    return delimiter.join(flagDefs)


def getCurrentMJD():
    jd = time.time() / 86400.0 + 2440587.5
    mjd = jd - 2400000.5
    return mjd


def getDateFromMJD(mjd):
    unixtime = (mjd + 2400000.5 - 2440587.5) * 86400.0
    theDate = datetime.utcfromtimestamp(unixtime)
    return theDate.strftime('%Y-%m-%d %H:%M:%S')


def getMJDFromSqlDate(sqlDate):
    mjd = None
    try:
        year, month, day = sqlDate[0:10].split('-')
        hours, minutes, seconds = sqlDate[11:19].split(':')
        t = (int(year), int(month), int(day), int(hours), int(minutes), int(seconds), 0, 0, 0)
        unixtime = int(time.mktime(t))
        mjd = unixtime / 86400.0 - 2400000.5 + 2440587.5
    except ValueError as e:
        mjd = None
        print 'String is not in SQL Date format.'

    return mjd


def getDateFractionMJD(mjd):
    unixtime = (mjd + 2400000.5 - 2440587.5) * 86400.0
    theDate = datetime.utcfromtimestamp(unixtime)
    dateString = theDate.strftime('%Y:%m:%d:%H:%M:%S')
    year, month, day, hour, min, sec = dateString.split(':')
    dayFraction = int(day) + int(hour) / 24.0 + int(min) / 1440.0 + int(sec) / 86400.0
    dateFraction = '%s %s %05.2f' % (year, month, dayFraction)
    return dateFraction


def sexToDec(sexv, ra=False, delimiter=':'):
    degrees = 0
    minutes = 0
    seconds = 0
    decimalDegrees = None
    sgn = 1
    try:
        degreesString, minutesString, secondsString = sexv.split(delimiter)
        if degreesString[0] == '-':
            sgn = -1
        else:
            sgn = 1
        degrees = abs(float(degreesString))
        minutes = float(minutesString)
        seconds = float(secondsString)
        if ra:
            degrees *= 15.0
            minutes *= 15.0
            seconds *= 15.0
        decimalDegrees = (degrees + minutes / 60.0 + seconds / 3600.0) * sgn
        if not ra and (decimalDegrees < -90.0 or decimalDegrees > 90.0):
            decimalDegrees = None
        elif ra and (decimalDegrees < 0.0 or decimalDegrees > 360.0):
            decimalDegrees = None
    except ValueError:
        decimalDegrees = None

    return decimalDegrees


def coords_sex_to_dec(ra, dec, delimiter=':'):
    return (
     sexToDec(ra, ra=True, delimiter=delimiter), sexToDec(dec, ra=False, delimiter=delimiter))


def wrapConeSearch(dbuser, dbpass, dbname, dbhost, tablename, ra, dec, radius):
    if dbpass == '':
        dbpass = ' "" '
    cmd = 'ConeSearch ' + dbuser + ' ' + dbpass + ' ' + dbname + ' ' + dbhost + ' quick ' + tablename + ' ' + str(ra) + ' ' + str(dec) + ' ' + str(radius)
    cmdout = os.popen(cmd)
    result = cmdout.readlines()
    if cmdout.close() != None:
        print 'Problem with command'
        return -1
    else:
        numberOfMatches = 0
        matchedRowNumberLinePrefix = 'Number of matched rows = '
        resultSetSortedBySep = []
        if len(result) == 1:
            pass
        else:
            resultSet = []
            for line in result:
                if line.startswith(matchedRowNumberLinePrefix):
                    numberOfMatches = int(line.replace(matchedRowNumberLinePrefix, '').rstrip())
                else:
                    id, separation = line.rstrip().lstrip().rstrip('"').lstrip('ID: ').replace(' Separation = ', '').split(',')
                    keyvaluepair = {'id': int(id), 'separation': float(separation)}
                    resultSet.append(keyvaluepair)

            resultSetSortedBySep = sorted(resultSet, key=lambda k: k['separation'])
        return (numberOfMatches, resultSetSortedBySep)


def calculate_cartesians(ra, dec):
    ra = math.radians(ra)
    dec = math.radians(dec)
    cos_dec = math.cos(dec)
    cx = math.cos(ra) * cos_dec
    cy = math.sin(ra) * cos_dec
    cz = math.sin(dec)
    cartesians = (
     cx, cy, cz)
    return cartesians


pi = 4 * math.atan(1.0)
DEG_TO_RAD_FACTOR = pi / 180.0
RAD_TO_DEG_FACTOR = 180.0 / pi

def getAngularSeparation(ra1, dec1, ra2, dec2):
    """
   Calculate the angular separation between two objects.  If either set of
   coordinates contains a colon, assume it's in sexagesimal and automatically
   convert into decimal before doing the calculation.
   """
    if ':' in str(ra1):
        ra1 = sexToDec(ra1, ra=True)
    if ':' in str(dec1):
        dec1 = sexToDec(dec1, ra=False)
    if ':' in str(ra2):
        ra2 = sexToDec(ra2, ra=True)
    if ':' in str(dec2):
        dec2 = sexToDec(dec2, ra=False)
    angularSeparation = None
    if ra1 and ra2 and dec1 and dec2:
        aa = (90.0 - dec1) * DEG_TO_RAD_FACTOR
        bb = (90.0 - dec2) * DEG_TO_RAD_FACTOR
        cc = (ra1 - ra2) * DEG_TO_RAD_FACTOR
        one = math.cos(aa) * math.cos(bb)
        two = math.sin(aa) * math.sin(bb) * math.cos(cc)
        three = one + two
        if three > 1.0:
            three = 1.0
        if three < -1.0:
            three = -1.0
        angularSeparation = math.acos(three) * RAD_TO_DEG_FACTOR * 3600.0
    return angularSeparation


QUICK = 1
FULL = 2
COUNT = 3
CAT_ID_RA_DEC_COLS = {'tcs_transient_objects': [
                           [
                            'id', 'ra_psf', 'dec_psf'], 0], 
   'tcs_2mass_psc_cat': [
                       [
                        'designation', 'ra', 'decl'], 1], 
   'tcs_cat_v_2mass_psc_noextended': [
                                    [
                                     'designation', 'ra', 'decl'], 1], 
   'tcs_2mass_xsc_cat': [
                       [
                        'designation', 'ra', 'decl'], 2], 
   'tcs_guide_star_cat': [
                        [
                         'hstID', 'RightAsc', 'Declination'], 3], 
   'tcs_cat_v_guide_star_ps': [
                             [
                              'hstID', 'RightAsc', 'Declination'], 3], 
   'tcs_ned_cat': [
                 [
                  'Object_Name', 'RA_deg', 'DEC_deg', 'Redshift_1'], 4], 
   'tcs_cat_v_ned_not_gal_qso': [
                               [
                                'Object_Name', 'RA_deg', 'DEC_deg', 'Redshift_1'], 4], 
   'tcs_cat_v_ned_qsos': [
                        [
                         'Object_Name', 'RA_deg', 'DEC_deg', 'Redshift_1'], 4], 
   'tcs_cat_v_ned_xrays': [
                         [
                          'Object_Name', 'RA_deg', 'DEC_deg', 'Redshift_1'], 4], 
   'tcs_cat_v_ned_galaxies': [
                            [
                             'Object_Name', 'RA_deg', 'DEC_deg', 'Redshift_1'], 4], 
   'tcs_sdss_galaxies_cat': [
                           [
                            'Objid', 'ra', 'dec_', 'z'], 5], 
   'tcs_cat_v_sdss_galaxies_notspec': [
                                     [
                                      'Objid', 'ra', 'dec_', 'z'], 5], 
   'tcs_sdss_spect_galaxies_cat': [
                                 [
                                  'Objid', 'ra', 'dec_', 'z'], 6], 
   'tcs_sdss_stars_cat': [
                        [
                         'Objid', 'ra', 'dec_'], 7], 
   'tcs_veron_cat': [
                   [
                    'recno', 'viz_RAJ2000', 'viz_DEJ2000', 'z'], 8], 
   'tcs_cat_deep2dr3': [
                      [
                       'OBJNAME', 'RA_deg', 'DEC_deg', 'Z'], 9], 
   'tcs_cat_md01_ned': [
                      [
                       'Object_Name', 'RA_deg', 'DEC_deg', 'Redshift'], 10], 
   'tcs_cat_md02_ned': [
                      [
                       'Object_Name', 'RA_deg', 'DEC_deg', 'Redshift'], 11], 
   'tcs_cat_md03_ned': [
                      [
                       'Object_Name', 'RA_deg', 'DEC_deg', 'Redshift'], 12], 
   'tcs_cat_md04_ned': [
                      [
                       'Object_Name', 'RA_deg', 'DEC_deg', 'Redshift'], 13], 
   'tcs_cat_md05_ned': [
                      [
                       'Object_Name', 'RA_deg', 'DEC_deg', 'Redshift'], 14], 
   'tcs_cat_md06_ned': [
                      [
                       'Object_Name', 'RA_deg', 'DEC_deg', 'Redshift'], 15], 
   'tcs_cat_md07_ned': [
                      [
                       'Object_Name', 'RA_deg', 'DEC_deg', 'Redshift'], 16], 
   'tcs_cat_md08_ned': [
                      [
                       'Object_Name', 'RA_deg', 'DEC_deg', 'Redshift'], 17], 
   'tcs_cat_md09_ned': [
                      [
                       'Object_Name', 'RA_deg', 'DEC_deg', 'Redshift'], 18], 
   'tcs_cat_md10_ned': [
                      [
                       'Object_Name', 'RA_deg', 'DEC_deg', 'Redshift'], 19], 
   'tcs_cat_md01_chiappetti2005': [
                                 [
                                  'recno', 'viz_RAJ2000', 'viz_DEJ2000'], 20], 
   'tcs_cat_md01_pierre2007': [
                             [
                              'recno', 'viz_RAJ2000', 'viz_DEJ2000'], 21], 
   'tcs_cat_md02_giacconi2002': [
                               [
                                'recno', 'viz_RAJ2000', 'viz_DEJ2000'], 22], 
   'tcs_cat_md02_lefevre2004': [
                              [
                               'recno', 'viz_RAJ2000', 'viz_DEJ2000', 'z'], 23], 
   'tcs_cat_md02_lehmer2005': [
                             [
                              'recno', 'viz_RAJ2000', 'viz_DEJ2000'], 24], 
   'tcs_cat_md02_virani2006': [
                             [
                              'recno', 'viz_RAJ2000', 'viz_DEJ2000'], 25], 
   'tcs_cat_md04_hasinger2007': [
                               [
                                'recno', 'viz_RAJ2000', 'viz_DEJ2000'], 26], 
   'tcs_cat_md04_trump2007': [
                            [
                             'recno', 'viz_RAJ2000', 'viz_DEJ2000', 'z'], 27], 
   'tcs_cat_md05_brunner2008': [
                              [
                               'recno', 'viz_RAJ2000', 'viz_DEJ2000'], 28], 
   'tcs_cat_md07_laird2009': [
                            [
                             'recno', 'viz_RAJ2000', 'viz_DEJ2000'], 29], 
   'tcs_cat_md07_nandra2005': [
                             [
                              'recno', 'viz_RAJ2000', 'viz_DEJ2000'], 30], 
   'tcs_cat_md08_manners2003': [
                              [
                               'recno', 'viz_RAJ2000', 'viz_DEJ2000'], 31], 
   'tcs_cat_sdss_stars_galaxies': [
                                 [
                                  'Objid', 'ra', 'dec_'], 32], 
   'tcs_cat_v_sdss_starsgalaxies_stars': [
                                        [
                                         'Objid', 'ra', 'dec_'], 32], 
   'tcs_cat_v_sdss_starsgalaxies_galaxies': [
                                           [
                                            'Objid', 'ra', 'dec_'], 32], 
   'tcs_cat_sdss_lrg': [
                      [
                       'Objid', 'ra', 'dec_'], 33], 
   'tcs_cat_slacs': [
                   [
                    'Objid', 'ra', 'dec_'], 34], 
   'tcs_cat_milliquas': [
                       [
                        'id', 'ra_deg', 'dec_deg', 'z'], 35], 
   'tcs_cat_sdss_dr9_photo_stars_galaxies': [
                                           [
                                            'objID', 'ra', 'dec_', 'z_'], 36], 
   'tcs_cat_v_sdss_dr9_galaxies_notspec': [
                                         [
                                          'objID', 'ra', 'dec_', 'z_'], 36], 
   'tcs_cat_v_sdss_dr9_stars': [
                              [
                               'objID', 'ra', 'dec_'], 36], 
   'tcs_cat_sdss_dr9_spect_galaxies_qsos': [
                                          [
                                           'objID', 'ra', 'dec_', 'z_'], 37], 
   'tcs_cat_v_sdss_dr9_spect_galaxies': [
                                       [
                                        'objID', 'ra', 'dec_', 'z_'], 37], 
   'tcs_cat_v_sdss_dr9_spect_qsos': [
                                   [
                                    'objID', 'ra', 'dec_', 'z_'], 37], 
   'tcs_cat_rosat_faint_1x29': [
                              [
                               'id', 'ra_deg', 'dec_deg'], 38], 
   'tcs_cat_rosat_bright_1x10': [
                               [
                                'id', 'ra_deg', 'dec_deg'], 39], 
   'tcs_cfa_detections': [
                        [
                         'cfa_designation', 'raDeg', 'decDeg'], 40], 
   'transientBucket': [
                     [
                      'primaryKeyId', 'raDeg', 'decDeg'], 1000], 
   'view_transientBucketMaster': [
                                [
                                 'primaryKeyId', 'raDeg', 'decDeg'], 1001]}

def coneSearch(ra, dec, radius, tableName, htmLevel=16, queryType=QUICK, conn=None, django=False):
    import MySQLdb, htmCircle
    message = ''
    if htmLevel not in (16, 20):
        return (
         'Must be HTM level 16 or 20', [])
    if ':' in str(ra):
        ra = sexToDec(ra, ra=True)
    if ':' in str(dec):
        dec = sexToDec(dec, ra=False)
    try:
        quickColumns = CAT_ID_RA_DEC_COLS[tableName][0]
    except KeyError as e:
        return (
         'Table %s not recognised.' % tableName, [])

    htmWhereClause = htmCircle.htmCircleRegion(htmLevel, ra, dec, radius)
    cartesians = calculate_cartesians(ra, dec)
    cartesianClause = 'and (cx * %.17f + cy * %.17f + cz * %.17f >= cos(%.17f))' % (cartesians[0], cartesians[1], cartesians[2], math.radians(radius / 3600.0))
    columns = [
     '*']
    if queryType == QUICK:
        columns = quickColumns
    elif queryType == COUNT:
        columns = [
         'count(*) number']
    query = 'select ' + (',').join(columns) + ' from %s' % tableName + htmWhereClause + cartesianClause
    results = []
    if conn:
        try:
            if django:
                cursor = conn.cursor()
            else:
                cursor = conn.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(query)
            if django:
                resultSet = [ dict((d[0], c) for d, c in zip(cursor.description, row)) for row in cursor ]
            else:
                resultSet = cursor.fetchall()
        except MySQLdb.Error as e:
            return (
             'Error %d: %s' % (e.args[0], e.args[1]), [])

        if resultSet:
            if queryType == COUNT:
                results = [
                 [
                  0.0, resultSet[0]['number']]]
                return (
                 'Count', results)
            for row in resultSet:
                if tableName == 'tcs_guide_star_cat':
                    separation = getAngularSeparation(ra, dec, math.degrees(row[CAT_ID_RA_DEC_COLS[tableName][0][1]]), math.degrees(row[CAT_ID_RA_DEC_COLS[tableName][0][2]]))
                else:
                    separation = getAngularSeparation(ra, dec, row[CAT_ID_RA_DEC_COLS[tableName][0][1]], row[CAT_ID_RA_DEC_COLS[tableName][0][2]])
                results.append([separation, row])

            results.sort()
        else:
            message = 'No matches from %s.' % tableName
    else:
        message = query
    return (message, results)


def htmID(ra, dec, htmLevel=16):
    id = None
    if htmLevel == 16 or htmLevel == 20:
        import htmCircle
        try:
            id = htmCircle.htmID(htmLevel, ra, dec)
        except Exception as e:
            pass

    return id


def bruteForceCMFConeSearch(filename, coordinatePairs, radius):
    import pyfits as p
    h = p.open(filename)
    t = h[1].data
    cols = h[1].columns
    mjd = h[0].header['MJD-OBS']
    filter = h[0].header['FPA.FILTERID'].replace('.00000', '')
    basename = os.path.basename(filename)
    raIndex = cols.names.index('RA_PSF')
    decIndex = cols.names.index('DEC_PSF')
    resultsTable = []
    i = 0
    for coord in coordinatePairs:
        for row in t:
            raCat = row[raIndex]
            decCat = row[decIndex]
            separation = getAngularSeparation(coord[0], coord[1], raCat, decCat)
            if separation < radius:
                resultsTable.append([row, i])

        i += 1

    if resultsTable:
        for name in cols.names:
            if name == 'RA_PSF':
                name = 'RA_J2000'
            if name == 'DEC_PSF':
                name = 'DEC_J2000'
            print '%s\t' % name,

        print '%s\t%s\t%s\t%s' % ('filter', 'mjd', 'filename', 'object_id')
        for row in resultsTable:
            for col in row[0]:
                print '%s\t' % col,

            print '%s\t%s\t%s\t%s' % (filter, mjd, basename, row[1])


J2000toGalactic = [
 -0.054875529, -0.873437105, -0.483834992,
 0.494109454, -0.444829594, 0.746982249,
 -0.867666136, -0.19807639, 0.455983795]

def transform(coords, matrix):
    pi = math.pi
    r0 = calculate_cartesians(coords[0], coords[1])
    s0 = [
     r0[0] * matrix[0] + r0[1] * matrix[1] + r0[2] * matrix[2],
     r0[0] * matrix[3] + r0[1] * matrix[4] + r0[2] * matrix[5],
     r0[0] * matrix[6] + r0[1] * matrix[7] + r0[2] * matrix[8]]
    r = math.sqrt(s0[0] * s0[0] + s0[1] * s0[1] + s0[2] * s0[2])
    result = [
     0.0, 0.0]
    result[1] = math.asin(s0[2] / r)
    cosaa = s0[0] / r / math.cos(result[1])
    sinaa = s0[1] / r / math.cos(result[1])
    result[0] = math.atan2(sinaa, cosaa)
    if result[0] < 0.0:
        result[0] = result[0] + pi + pi
    result[0] = math.degrees(result[0])
    result[1] = math.degrees(result[1])
    return result


def redshiftToDistance(z):
    WM = 0.3
    WV = 0.7
    H0 = 70.0
    h = H0 / 100.0
    WR = 4.165e-05 / (h * h)
    WK = 1.0 - WM - WV - WR
    c = 299792.458
    DCMR = 0.0
    DCMR_Mpc = 0.0
    DA = 0.0
    DA_Mpc = 0.0
    DA_scale = 0.0
    DL = 0.0
    DL_Mpc = 0.0
    DMOD = 0.0
    a = 0.0
    az = 1.0 / (1.0 + z)
    n = 1000
    for i in range(n):
        a = az + (1.0 - az) * (i + 0.5) / n
        adot = math.sqrt(WK + WM / a + WR / math.pow(a, 2) + WV * math.pow(a, 2))
        DCMR = DCMR + 1.0 / (a * adot)

    DCMR = (1.0 - az) * DCMR / n
    DCMR_Mpc = c / H0 * DCMR
    x = math.sqrt(abs(WK)) * DCMR
    if x > 0.1:
        if WK > 0.0:
            ratio = 0.5 * (math.exp(x) - math.exp(-x)) / x
        else:
            ratio = math.sin(x) / x
    else:
        y = math.pow(x, 2)
        if WK < 0.0:
            y = -y
        ratio = 1 + y / 6.0 + math.pow(y, 2) / 120.0
    DA = az * ratio * DCMR
    DA_Mpc = c / H0 * DA
    DA_scale = DA_Mpc / 206.264806
    DL = DA / math.pow(az, 2)
    DL_Mpc = c / H0 * DL
    DMOD = 5 * math.log10(DL_Mpc * 1000000.0) - 5
    results = {'dcmr_mpc': DCMR_Mpc, 
       'da_mpc': DA_Mpc, 
       'da_scale': DA_scale, 
       'dl_mpc': DL_Mpc, 
       'dmod': DMOD, 
       'z': z}
    return results


OK = 0
PAGE_NOT_FOUND = 1
BAD_SERVER_ADDRESS = 2
HTTP_ERROR = 3

def getRemoteWebPage(url, username=None, password=None, realm=None):
    import urllib2
    responseErrorCode = OK
    responsePage = ''
    if username and password:
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(realm, url, username, password)
        authhandler = urllib2.HTTPBasicAuthHandler(passman)
        opener = urllib2.build_opener(authhandler)
        urllib2.install_opener(opener)
    try:
        req = urllib2.Request(url)
        responsePage = urllib2.urlopen(req).read()
    except urllib2.HTTPError as e:
        if e.code == 404:
            print 'Page not found. Perhaps the server has not processed the request yet'
            responseErrorCode = PAGE_NOT_FOUND
        else:
            print e
            responseErrorCode = HTTP_ERROR
    except urllib2.URLError as e:
        print 'Bad URL'
        responseErrorCode = BAD_SERVER_ADDRESS

    return (responsePage, responseErrorCode)


def enum(**enums):
    return type('Enum', (), enums)