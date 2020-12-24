# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dave/Dropbox/github_projects/dryxPython/dryxPython/fitstools.py
# Compiled at: 2013-09-08 10:23:38
"""
fitstools
===============
:Summary:
    Some helpful tools to work with FITS files

:Author:
    David Young

:Date Created:
    March 19, 2013

:dryx syntax:
    - ``xxx`` = come back here and do some more work
    - ``_someObject`` = a 'private' object that should only be changed for debugging

:Notes:
    - If you have any questions requiring this script please email me: d.r.young@qub.ac.uk
"""
import sys, os

def main():
    """Used for debugging

    Key Arguments:
        -
        - dbConn -- mysql database connection
        - log -- logger

    Return:
        - None
    """
    import pesstoMarshallPythonPath as pp
    pp.set_python_path()
    import pmCommonUtils as p, dryxPython.commonutils as cu
    dbConn, log = p.settings()
    startTime = cu.get_now_sql_datetime()
    log.info('--- STARTING TO RUN THE fitstools AT %s' % (startTime,))
    dbConn.commit()
    dbConn.close()
    endTime = cu.get_now_sql_datetime()
    runningTime = cu.calculate_time_difference(startTime, endTime)
    log.info('-- FINISHED ATTEMPT TO RUN THE fitstools AT %s (RUNTIME: %s) --' % (
     endTime, runningTime))


def convert_fits_header_to_dictionary(log, pathToFitsFile, headerExtension=0):
    """Convert a FITS file header keywords / values into a python dictionary

    **Key Arguments:**
        - ``log`` -- logger
        - ``pathToFitsFile`` -- path to the fits file
        - ``headerExtension`` -- the header extension to look in

    **Return:**
        - ``headerDictionary`` -- the header converted to a dictionary suitable for mysql ingest
    """
    log.info('starting the ``convert_fits_header_to_dictionary`` function')
    if not isinstance(pathToFitsFile, str):
        raise TypeError('pathToFitsFile argument needs to be a string')
    try:
        with open(pathToFitsFile):
            fileExists = True
    except IOError:
        fileExists = False
        raise IOError('the fits file %s does not exist' % (pathToFitsFile,))

    headerDictionary = {}
    try:
        fitsHeader = get_fits_header(log, pathToFitsFile, headerExtension=headerExtension)
        cardList = fitsHeader.ascardlist()
        print cardList
    except:
        headerDictionary['corrupted'] = [
         True, 'file is corrupted']
        return headerDictionary

    for cl in cardList:
        if len(cl.key) > 0:
            headerDictionary[cl.key] = [cl.value, cl.comment]

    log.info('finished the ``convert_fits_header_to_dictionary`` function')
    return headerDictionary


def get_fits_header(log, pathToFits, headerExtension=0):
    """Return the HDU for the given fits file

    **Key Arguments:**
        - ``log`` -- logger
        - ``pathToFits`` -- the absolute path to the fits file
        - ``headerExtension`` -- the header extension to look in

    **Return:**
        - ``hdu`` -- the FITS header requested
    """
    import pyfits as pf
    try:
        hdu = pf.getheader(pathToFits, headerExtension)
    except:
        try:
            _correct_extended_fits_keywords(pathToFits)
        except:
            sys.exit('image ' + str(pathToFits) + ' is corrupted, delete it and start again')
            hdu = pf.getheader(pathToFits, headerExtension)

    return hdu


def _correct_extended_fits_keywords(log, pathToFits):
    """Values within the fits header should be no longer than 80 characters

    **Key Arguments:**
        - ``log`` -- logger
        - ``pathToFits`` -- path the the FITS file

    **Return:**
        - None
    """
    import re
    from pyfits import open as popen
    from numpy import asarray
    hdulist = popen(pathToFits)
    a = hdulist[0]._verify('fix')
    _header = hdulist[0].header
    for i in range(len(a)):
        if not a[i]:
            a[i] = [
             '']

    ww = asarray([ i for i in range(len(a)) if re.sub(' ', '', a[i][0]) != '' ])
    if len(ww) > 0:
        newheader = []
        headername = []
        for j in _header.items():
            headername.append(j[0])
            newheader.append(j[1])

        hdulist.close()
        imm = popen(pathToFits, mode='update')
        _header = imm[0].header
        for i in ww:
            if headername[i]:
                try:
                    _header.update(headername[i], newheader[i])
                except:
                    _header.update(headername[i], 'xxxx')

        imm.flush()
        imm.close()


def remove_keyword_from_file(log, pathToFitsFile, keyword):
    """Remove a given keyword card from a fits file

    **Return:**
        - None
    """
    import pyfits as pf
    hduList = pf.open(pathToFitsFile)
    fitsData = hduList[0].data
    primHeader = hduList[0].header
    hduList.close()
    os.remove(pathToFitsFile)
    primCardList = primHeader.ascardlist()
    thisCardList = []
    for key in primCardList.keys():
        if key != keyword:
            thisCardList.append(primCardList[key])

    primHeader = pf.Header(cards=thisCardList)
    primHdu = pf.PrimaryHDU(header=primHeader, data=fitsData)
    thisHduList = pf.HDUList([primHdu])
    thisHduList.writeto(pathToFitsFile, checksum=True)
    log.debug('primHeader %s' % (primHeader,))


def add_or_replace_keyword_to_fits(log, pathToFitsFile, keywordName, keywordValue, keywordComment):
    """Add or replace a given keyword card from a fits file

    **Return:**
        - None
    """
    import pyfits as pf
    hduList = pf.open(pathToFitsFile)
    fitsData = hduList[0].data
    primHeader = hduList[0].header
    hduList.close()
    os.remove(pathToFitsFile)
    primCardList = primHeader.ascardlist()
    if keywordName in primCardList.keys():
        primCardList[keywordName].comment = keywordComment
        primCardList[keywordName].value = keywordValue
    else:
        card = pf.Card(keywordName, keywordValue, keywordComment)
        primCardList.append(card)
    primHeader = pf.Header(cards=primCardList)
    primHdu = pf.PrimaryHDU(header=primHeader, data=fitsData)
    thisHduList = pf.HDUList([primHdu])
    thisHduList.writeto(pathToFitsFile, checksum=True)
    log.debug('primHeader %s' % (primHeader,))


if __name__ == '__main__':
    main()