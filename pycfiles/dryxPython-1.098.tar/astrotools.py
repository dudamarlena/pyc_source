# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dave/Dropbox/github_projects/dryxPython/dryxPython/astrotools.py
# Compiled at: 2013-09-11 02:41:30
"""
**astrotools**

| Created by David Young on December 10, 2012
| If you have any questions requiring this script please email me: d.r.young@qub.ac.uk

dryx syntax:
    - ``xxx`` = come back here and do some more work
    - ``_someObject`` = a 'private' object that should only be changed for debugging

notes:
    - Dave started work on this file on December 10, 2012
    - Dave 'completed' this code on ... not complete yet!
"""
import math
PARSEC_2_METRES = 3.08567758e+16
PARSEC_2_CMS = PARSEC_2_METRES * 100
KPC_2_METRES = 1000.0 * PARSEC_2_METRES
KPC_2_CMS = 1000.0 * PARSEC_2_CMS
MPC_2_METRES = 1000000.0 * PARSEC_2_METRES
MPC_2_CMS = 1000000.0 * PARSEC_2_CMS
pi = 4 * math.atan(1.0)
DEG_TO_RAD_FACTOR = pi / 180.0
RAD_TO_DEG_FACTOR = 180.0 / pi

def check_for_sdss_coverage(dbConn, log, ra, decl):
    """Check an ra and dec for SDSS DR9 image coverage

        **Key Arguments:**
            - ``dbConn`` -- db dbConnection
            - ``log`` -- python logger
            - ``ra`` -- ra in decimal degrees
            - ``dec`` -- dec in decimal degrees

        **Return:**
            - ``None``
    """
    import sdss_sqlcl as s, dryxPython.mysql as m
    raUpper = ra + 0.0001
    raLower = ra - 0.0001
    declUpper = decl + 0.001
    declLower = decl - 0.001
    sqlQuery = 'SELECT TOP 1 rerun, camcol, field FROM PhotoObj WHERE ra BETWEEN %s and %s AND dec BETWEEN %s and %s' % (raLower, raUpper, declLower, declUpper)
    try:
        log.debug('attempting to determine whether object is in SDSS DR9 footprint')
        result = s.query(sqlQuery)
        result = result.read()
    except Exception as e:
        log.error('could not determine whether object is in SDSS DR9 footprint - failed with this error %s: ' % (str(e),))
        return -1

    if 'No objects have been found' in result:
        match = False
    else:
        match = True
    return match


def create_cbet_url(dbConn, log, cbet):
    """
    Create the CBET URL given a CBET number.
    The URL contains a *fiddly* middle number before the CBET txt file - this function calculates this number before returning the valid URL.

    **Key Arguments:**
        - ``dbConn`` -- mysql database connection
        - ``log`` -- logger
        - ``cbet`` -- cbet number

    **Return:**
        - ``cbetUrl`` -- CBET URL
    """
    cbet = int(cbet)
    pcbetNumber = ('{0:006.0f}').format(cbet)
    middleNumber = cbet / 100
    middleNumber = middleNumber * 100
    pmiddleNumber = ('{0:006.0f}').format(middleNumber)
    cbetUrl = 'http://www.cbat.eps.harvard.edu/iau/cbet/' + str(pmiddleNumber) + '/CBET' + str(pcbetNumber) + '.txt'
    return cbetUrl


def clean_supernova_name(dbConn, log, snName):
    """Clean a SN name. As a string, this function will attempt to clean up the name so that it is somewhat homogeneous with SN/transient from the same survey/atel system.

        **Key Arguments:**
                - ``dbConn`` -- mysql database connection
                - ``log`` -- logger
                - ``snName`` -- sn name to be cleaned (string)

        **Return:**
                - ``snName`` -- cleaned sn name (string)
        """
    import re
    snName = snName.replace(' ', '')
    snName = snName.replace('–', '-')
    snName = snName.replace('FSRQ', '')
    snName = snName.replace('Catalogue', '-')
    regex = re.compile('swift|css|sss|mls|master|^sn', re.I)
    if regex.search(snName):
        snName = regex.sub(regex.search(snName).group().upper(), snName)
    snName = snName.replace('SDSSgalaxy', 'SDSS')
    snName = snName.replace('MASTERShort', 'MASvTER')
    snName = snName.replace('MASTEROT', 'MASTER')
    reMaster = re.compile('MASTER([^J])')
    snName = reMaster.sub('MASTERJ\\g<1>', snName)
    regex = re.compile('SN.LSQ', re.I)
    snName = regex.sub('LSQ', snName)
    regex = re.compile('supernova', re.I)
    snName = regex.sub('SN', snName)
    regex = re.compile('GuideStarCatalog', re.I)
    snName = regex.sub('GSC-', snName)
    regex = re.compile('sdssgalaxy', re.I)
    snName = regex.sub('SDSS', snName)
    return snName


def luminosity_to_flux(lumErg_S, dist_Mpc):
    """Convert luminosity to a flux

    **Key Arguments:**
        - ``lumErg_S`` -- luminosity in ergs/sec
        - ``dist_Mpc`` -- distance in Mpc

    **Return:**
        - ``fluxErg_cm2_S`` -- flux in ergs/cm2/s
    """
    import numpy as np
    distCm = dist_Mpc * MPC_2_CMS
    fluxErg_cm2_S = lumErg_S / (4 * np.pi * distCm ** 2)
    return fluxErg_cm2_S


def ra_to_sex(ra, delimiter=':'):
    """Convert ra in decimal degrees to sexigesimal"""
    ra_hh = int(ra / 15)
    ra_mm = int((ra / 15 - ra_hh) * 60)
    ra_ss = int(((ra / 15 - ra_hh) * 60 - ra_mm) * 60)
    ra_ff = int((((ra / 15 - ra_hh) * 60 - ra_mm) * 60 - ra_ss) * 100)
    return '%02d' % ra_hh + delimiter + '%02d' % ra_mm + delimiter + '%02d' % ra_ss + '.' + '%02d' % ra_ff


def dec_to_sex(dec, delimiter=':'):
    """Convert dec in decimal degrees to sexigesimal"""
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
    """Convert ra and dec in decimal degrees to sexigesimal"""
    return (
     ra_to_sex(ra, delimiter), dec_to_sex(dec, delimiter))


def ra_in_decimal_hours(ra):
    """Convert ra in decimal degrees to hours"""
    return ra / 15.0


def getCurrentMJD():
    """Get the current MJD"""
    jd = time.time() / 86400.0 + 2440587.5
    mjd = jd - 2400000.5
    return mjd


def getDateFromMJD(mjd):
    """convert mjd to a date"""
    from datetime import datetime
    unixtime = (mjd + 2400000.5 - 2440587.5) * 86400.0
    theDate = datetime.utcfromtimestamp(unixtime)
    return theDate.strftime('%Y-%m-%d %H:%M:%S.%f')


def getSQLDateFromMJD(mjd):
    """convert mjd to a date"""
    unixtime = (mjd + 2400000.5 - 2440587.5) * 86400.0
    theDate = datetime.utcfromtimestamp(unixtime)
    return theDate.strftime('%Y-%m-%dT%H:%M:%S.%f')


def getMJDFromSqlDate(sqlDate):
    """convert a sql date to mjd"""
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
    """convert mjd to date fraction"""
    unixtime = (mjd + 2400000.5 - 2440587.5) * 86400.0
    theDate = datetime.utcfromtimestamp(unixtime)
    dateString = theDate.strftime('%Y:%m:%d:%H:%M:%S')
    year, month, day, hour, min, sec = dateString.split(':')
    dayFraction = int(day) + int(hour) / 24.0 + int(min) / 1440.0 + int(sec) / 86400.0
    dateFraction = '%s %s %05.2f' % (year, month, dayFraction)
    return dateFraction


def sexToDec(sexv, ra=False, delimiter=':'):
    """convert sexigesimal to decimal degrees"""
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
    """Convert sexagesimal ra and dec to decimal degrees"""
    return (
     sexToDec(ra, ra=True, delimiter=delimiter), sexToDec(dec, ra=False, delimiter=delimiter))


def calculate_cartesians(ra, dec):
    """Convert decimal degrees ra and dec to cartesians"""
    ra = math.radians(ra)
    dec = math.radians(dec)
    cos_dec = math.cos(dec)
    cx = math.cos(ra) * cos_dec
    cy = math.sin(ra) * cos_dec
    cz = math.sin(dec)
    cartesians = (
     cx, cy, cz)
    return cartesians


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


def convert_redshift_to_distance(z):
    """Convert a redshift to various distance units

    **Key Arguments:**
        - ``z`` -- the redshift to be converted

    **Return:**
        - ``results`` -- result dictionary including
            - ``dcmr_mpc`` -- co-moving radius distance
            - ``da_mpc`` -- angular distance
            - ``da_scale`` -- angular distance scale
            - ``dl_mpc`` -- luminosity distance (usually use this one)
            - ``dmod`` -- distance modulus (determined from luminosity distance)
    """
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


def convert_mpc_to_redshift(DL_Mpc):
    """Convert a luminosity distance to a redshift

    **Key Arguments:**
        - ``DL_Mpc`` -- luminosity distance (Mpc)

    **Return:**
        - ``redshift`` -- the calculated redshift
    """
    import math
    lowerLimit = 0.0
    upperLimit = 30.0
    redshift = upperLimit - lowerLimit
    distGuess = float(convert_redshift_to_distance(redshift)['dl_mpc'])
    distDiff = DL_Mpc - distGuess
    while math.fabs(distDiff) > 0.0001:
        if distGuess < DL_Mpc:
            lowerLimit = redshift
            redshift = lowerLimit + (upperLimit - lowerLimit) / 2.0
            distGuess = float(convert_redshift_to_distance(redshift)['dl_mpc'])
        elif distGuess > DL_Mpc:
            upperLimit = redshift
            redshift = lowerLimit + (upperLimit - lowerLimit) / 2.0
            distGuess = float(convert_redshift_to_distance(redshift)['dl_mpc'])
        distDiff = DL_Mpc - distGuess

    redshift = float('%5.4f' % (redshift,))
    return redshift


if __name__ == '__main__':
    main()