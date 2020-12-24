# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ggui\mastCrossSearch.py
# Compiled at: 2019-08-03 12:38:58
# Size of source mod 2**32: 7466 bytes
"""
.. module:: mastCrossSearch
    :synopsis: Search MAST Archive for matching observations on a given gPhoton GALEX WCS frame
.. moduleauthor:: Duy Nguyen <dtn5ah@virginia.edu>
"""
from astropy.io import fits
from astropy.wcs import WCS
import astropy.wcs.utils as pix2RaDec
from math import floor
from scipy.spatial import distance
import sys, json
try:
    import urllib.parse as urlencode
    from urllib.request import urlretrieve
except ImportError:
    from urllib import pathname2url as urlencode
    from urllib import urlretrieve

try:
    import http.client as httplib
except ImportError:
    import httplib

TEMPFILE = 'Messier060_coadd.fits'

def getFITSCornerCoords(filename):
    fitsImage = fits.open(filename)
    wcs = WCS(fitsImage[0].header)
    rangeX = fitsImage[0].header['NAXIS1']
    rangeY = fitsImage[0].header['NAXIS2']
    corner1 = pix2RaDec(rangeX, 0, wcs)
    corner2 = pix2RaDec(0, 0, wcs)
    corner3 = pix2RaDec(0, rangeY, wcs)
    corner4 = pix2RaDec(rangeX, rangeY, wcs)
    cornerCoords = [corner1, corner2, corner3, corner4]
    return cornerCoords


def getFITSCenterCoords(filename):
    fitsImage = fits.open(filename)
    wcs = WCS(fitsImage[0].header)
    rangeX = fitsImage[0].header['NAXIS1']
    rangeY = fitsImage[0].header['NAXIS2']
    center = pix2RaDec(floor(rangeX / 2.0), floor(rangeY / 2.0), wcs)
    return center


def minCircle(cornerList, center):
    radius = distance.euclidean((cornerList[0].ra.degree, cornerList[0].dec.degree), (center.ra.degree, center.dec.degree))
    return radius


def mastConeQuery(center, radius):
    server = 'mast.stsci.edu'
    requestsVersion = '.'.join(map(str, sys.version_info[:3]))
    requestParams = {'service':'Mast.Caom.Cone', 
     'params':{'ra':center.ra.degree, 
      'dec':center.dec.degree, 
      'radius':radius}, 
     'format':'json', 
     'pagesize':2000, 
     'removenullcolumns':True, 
     'timeout':30, 
     'removecache':True}
    JSONquery = urlencode(json.dumps(requestParams))
    httpHeaders = {'Content-type':'application/x-www-form-urlencoded', 
     'Accept':'text/plain', 
     'User-agent':'python-requests/' + requestsVersion}
    connMAST = httplib.HTTPSConnection(server)
    connMAST.request('POST', '/api/v0/invoke', 'request=' + JSONquery, httpHeaders)
    httpResponse = connMAST.getresponse()
    header = httpResponse.getheaders()
    data = httpResponse.read().decode('utf-8')
    return (header, data)


def extractGGUIFields(jsonReturn):
    gguiFields = []
    for i, obs in enumerate(jsonReturn['data']):
        mission = obs['obs_collection']
        project = obs['project']
        region = obs['s_region']
        dataType = obs['dataproduct_type']
        gguiFields.append((i, mission, project, dataType, region))

    return gguiFields


def appendRegionList(regOutFile, regionParse, paramIgnore):
    shape = regionParse[0]
    ds9Region = regionParse[0].lower() + '('
    for param in regionParse[paramIgnore:]:
        ds9Region = ds9Region + param + ', '

    ds9Region = ds9Region[:-2] + ')'
    print(ds9Region)
    mission = obs['obs_collection']
    project = obs['project']
    if type(project) is type(None):
        project = 'NULL'
    else:
        styleArgs = ' #'
        if project[:4] == 'hlsp':
            styleArgs = styleArgs + ' ' + 'color=yellow'
        else:
            if mission == 'HST' or mission == 'HLA':
                styleArgs = styleArgs + ' ' + 'color=red'
            else:
                if mission == 'KEPLER' or mission == 'K2':
                    styleArgs = styleArgs + ' ' + 'color=green'
                else:
                    if mission == 'PS1':
                        styleArgs = styleArgs + ' ' + 'color=blue'
                    else:
                        if mission == 'SWIFT':
                            styleArgs = styleArgs + ' ' + 'color=cyan'
                        else:
                            if mission == 'GALEX':
                                styleArgs = styleArgs + ' ' + 'color=magenta'
                            else:
                                styleArgs = styleArgs + ' ' + 'color=green dash=1'
    ds9Region = ds9Region + styleArgs
    print(ds9Region)
    regOutFile.write(ds9Region + '\n')


def exportDS9Regions(jsonReturn, fileOutputName):
    gguiFields = []
    regOutFile = open(fileOutputName, 'w')
    for i, obs in enumerate(jsonReturn['data']):
        region = obs['s_region']
        regionParse = region.split()
        ds9Region = ''
        paramIgnore = 0
        for param in regionParse:
            try:
                float(param)
                break
            except Exception:
                paramIgnore += 1

        if regionParse[0] != 'CIRCLE' and regionParse[0] != 'POLYGON':
            print('Illegal/Unimplemented Shape Detected: ', regionParse[0], '. Skipping Object')
        else:
            shape = regionParse[0]
            ds9Region = regionParse[0].lower() + '('
            for param in regionParse[paramIgnore:]:
                ds9Region = ds9Region + param + ', '

            ds9Region = ds9Region[:-2] + ')'
            print(ds9Region)
            mission = obs['obs_collection']
            project = obs['project']
            if type(project) is type(None):
                project = 'NULL'
            else:
                styleArgs = ' #'
                if project[:4] == 'hlsp':
                    styleArgs = styleArgs + ' ' + 'color=yellow'
                else:
                    if mission == 'HST' or mission == 'HLA':
                        styleArgs = styleArgs + ' ' + 'color=red'
                    else:
                        if mission == 'KEPLER' or mission == 'K2':
                            styleArgs = styleArgs + ' ' + 'color=green'
                        else:
                            if mission == 'PS1':
                                styleArgs = styleArgs + ' ' + 'color=blue'
                            else:
                                if mission == 'SWIFT':
                                    styleArgs = styleArgs + ' ' + 'color=cyan'
                                else:
                                    if mission == 'GALEX':
                                        styleArgs = styleArgs + ' ' + 'color=magenta'
                                    else:
                                        styleArgs = styleArgs + ' ' + 'color=green dash=1'
            ds9Region = ds9Region + styleArgs
            print(ds9Region)
            regOutFile.write(ds9Region + '\n')

    regOutFile.close()


cornerCoords = getFITSCornerCoords(TEMPFILE)
center = getFITSCenterCoords(TEMPFILE)
radius = minCircle(cornerCoords, center)
header, data = mastConeQuery(center, radius)
jsonReturn = json.loads(data)
gguiFields = extractGGUIFields(jsonReturn)
exportDS9Regions(jsonReturn, TEMPFILE + '.reg')