# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dave/Dropbox/github_projects/dryxPython/dryxPython/atelparser.py
# Compiled at: 2013-08-06 05:24:10
"""
atelparser
===============
:Summary:
        Download and parse ATel to strip out RA, DEC & Names of objects into a MySQL DB table(s)

:Author:
        David Young

:Date Created:
        February 4, 2013

:dryx syntax:
        - ``xxx`` = come back here and do some more work
        - ``_someObject`` = a 'private' object that should only be changed for debugging

:Notes:
        - If you have any questions requiring this script please email me: d.r.young@qub.ac.uk
"""

def main():
    """Using the PESSTO Marshall database on mac to test & debug this module

        Key Arguments:
                -
                - dbConn -- mysql database connection
                - log -- logger

        Return:
                - None
        """
    import pmCommonUtils as p, dryxPython.commonutils as cu
    dbConn, log = p.settings()
    startTime = cu.get_now_sql_datetime()
    log.info('--- STARTING TO RUN THE atelparser AT %s' % (startTime,))
    downloadDirectory = '/tmp'
    dbTableName = 'atel_fullcontent'
    parse_atels(dbConn, log, '/Users/Dave/Desktop/')
    dbConn.commit()
    dbConn.close()
    endTime = cu.get_now_sql_datetime()
    runningTime = cu.calculate_time_difference(startTime, endTime)
    log.info('-- FINISHED ATTEMPT TO RUN THE atelparser AT %s (RUNTIME: %s) --' % (endTime, runningTime))


def download_atels(dbConn, log, lowerAtelIndex, upperAtelIndex, downloadDirectory):
    """download all atels within given range of atels

            Key Arguuments:
                - ``lowerAtelIndex`` -- lowest atel number to download
                - ``upperAtelIndex`` -- lowest atel number to download
                - ``downloadDirectory`` -- directory to download ATels to

            Returns
                - None
    """
    import dryxPython.webcrawlers as wc
    urlList = []
    baseUrl = 'http://www.astronomerstelegram.org/?read='
    for i in range(lowerAtelIndex, upperAtelIndex):
        urlList.extend([baseUrl + str(i)])

    try:
        log.info('downloading all ATels from %s to %s' % (lowerAtelIndex, upperAtelIndex))
        localUrls = wc.multiWebDocumentDownloader(urlList, downloadDirectory, log, dbConn, 0)
    except Exception as e:
        log.error('could not download atels : ' + str(e) + '\n')

    return localUrls


def atels_to_database(dbConn, log, dbTableName, downloadDirectory):
    """
        Parse ATels into a mysql db. Parser to add ATels into a mysql db - each ATel has 'element' data (top level - title, author ...) and 'item' data (object specific data - ra, dec, mag, name ...).
        The parser will add one row per 'item' (object) into the db table.

        Key Arguments:
            - ``dbConn`` -- database connection
            - ``log`` -- logger
            - ``dbTableName`` -- name of the db table to add ATels to
            - ``downloadDirectory`` -- directory to download the ATel HTML files to

        """
    import re, sys, dryxPython.mysql as m
    from datetime import datetime
    uniqueKeyList = [
     'atelNumber']
    checkRange = 10
    sqlQuery = 'SELECT atelNumber\n                        FROM %s\n                        ORDER BY atelNumber DESC\n                        LIMIT 1' % (dbTableName,)
    try:
        log.debug('attempting to find the last ingested atel number')
        rows = m.execute_mysql_read_query(sqlQuery, dbConn, log)
    except Exception as e:
        log.error('could not find the last ingested atel number - failed with this error: %s ' % (str(e),))
        return -1

    if len(rows) != 0:
        nextATel = int(rows[0]['atelNumber']) + 1
    else:
        nextATel = 3900
        checkRange = 1000
    nextFewAtels = nextATel + checkRange
    try:
        log.debug('attempting to download the html files of the next %s atels' % (checkRange,))
        localUrls = download_atels(dbConn, log, nextATel, nextFewAtels, downloadDirectory)
    except Exception as e:
        log.error('could not download the html files of the next %s atels - failed with this error: %s ' % (checkRange, str(e)))
        return -1

    for url in localUrls:
        rf = open(url, 'r')
        html = rf.read()
        elementDict = {}
        reTitle = re.compile('<TITLE>.*?#\\d{1,4}:\\s?(.*?)\\s?<\\/TITLE>', re.M | re.I)
        try:
            title = reTitle.search(html).group(1)
        except:
            return
            title = None

        elementDict['title'] = title
        reAtelNumber = re.compile('<P ALIGN=CENTER>\\s?ATel\\s?#(\\d{1,4})', re.M | re.I)
        try:
            atelNumber = reAtelNumber.search(html).group(1)
        except:
            atelNumber = None

        elementDict['atelNumber'] = atelNumber
        reWho = re.compile('<A HREF=\\"mailto:([\\w.\\-@]*)\\">(.*?)<', re.M | re.I)
        try:
            email = reWho.search(html).group(1)
            authors = reWho.search(html).group(2)
        except:
            email = None
            authors = None

        elementDict['email'] = email
        elementDict['authors'] = authors
        redateTime = re.compile('<STRONG>(\\d{1,2}\\s\\w{1,10}\\s\\d{4});\\s(\\d{1,2}:\\d{2})\\sUT</STRONG>', re.M | re.I)
        try:
            date = redateTime.search(html).group(1)
            time = redateTime.search(html).group(2)
        except:
            date = None
            time = None

        datePublished = date + ' ' + time
        datePublished = datetime.strptime(datePublished, '%d %b %Y %H:%M')
        elementDict['datePublished'] = datePublished
        reTags = re.compile('<p class="subjects">Subjects: (.*?)</p>', re.M | re.I)
        try:
            tags = reTags.search(html).group(1)
        except:
            tags = None

        elementDict['tags'] = tags
        reUserText = re.compile('</div id="subjects">.*?(<div id="references">.*?</div id="references">)?<P>(.*)</P>.*?(<a href="http://twitter.com/share|</TD><TD>)', re.S | re.I)
        try:
            userText = reUserText.search(html).group(2)
        except:
            userText = None

        elementDict['userText'] = userText
        refList = []
        reOneRef = re.compile('http:\\/\\/www.astronomerstelegram.org\\/\\?read=(\\d{1,4})', re.M | re.I)
        try:
            refIter = reOneRef.finditer(userText)
        except:
            refIter = None

        if refIter:
            for item in refIter:
                refList.extend([item.group(1)])

        refList = set(refList)
        refList = (', ').join(refList)
        elementDict['refList'] = refList
        reBacksRefs = re.compile('<div id="references">(.*?)</div id="references">', re.M | re.I)
        try:
            backRefs = reBacksRefs.search(html).group(1)
        except:
            backRefs = None

        backRefList = []
        reOneBackRef = re.compile('<A HREF="http:\\/\\/www.astronomerstelegram.org\\/\\?read=(\\d{1,4})">\\1</a>', re.M | re.I)
        try:
            backRefIter = reOneBackRef.finditer(backRefs)
        except:
            backRefIter = None

        if backRefIter:
            for item in backRefIter:
                backRefList.extend([item.group(1)])

        backRefList = set(backRefList)
        backRefList = (', ').join(backRefList)
        elementDict['backRefList'] = backRefList
        try:
            log.debug('attempting to convert ATELs to MySQL table')
            m.convert_dictionary_to_mysql_table(dbConn, log, elementDict, dbTableName, uniqueKeyList)
        except Exception as e:
            log.critical('could not convert ATELs to MySQL table - failed with this error: %s ' % (str(e),))
            return -1

        rf.close()

    return


def parse_atels(dbConn, log, mdFolder):
    """Parse the content of the ATels in the database, appending the various components and values to the db. Also includes the ability convert the atels to markdown, highlighting matches of the parsing regexs.

    **Key Arguments:**
        - ``dbConn`` -- mysql database connection
        - ``log`` -- logger
        - ``mdFolder`` -- where to write the md files to

    **Return:**
        - None
    """
    import re, dryxPython.mysql as m, utils as u, dryxPython.commonutils as cu, dryxPython.astrotools as at
    numReferences = 0
    tags = ''
    numCoords = 0
    numHeaderName = 0
    numTextName = 0
    discHead = 0
    obsHead = 0
    clasHead = 0
    correctionHead = 0
    discText = 0
    obsText = 0
    clasText = 0
    comment = 0
    sqlQuery = 'SELECT *\n                    FROM atel_fullcontent\n                    WHERE dateParsed is NULL\n                    ORDER BY atelNumber'
    try:
        log.debug('attempting to select the required atel text')
        rows = m.execute_mysql_read_query(sqlQuery, dbConn, log)
    except Exception as e:
        log.error('could not select the required atel text - failed with this error: %s ' % (str(e),))
        return -1

    start = '((R\\.?A\\.?\\b|Coord)[/()\\w\\d\\s,.]{0,9}(\\(J2000(\\.0)?\\)\\s?)?(=|:|\\s)|\\d{4}-\\d{2}-\\d{2})\\s{0,2}[+(]{0,2}'
    middle = "(\\sdeg)?(\\s?,|:)?\\s{0,2}(and\\s{1,2}|\\(?[\\ddeg.':\\s]{1,16}\\)?(;|,)?\\s{0,3})?(Decl?\\.?\\s*?[()\\w\\d\\s]{0,9}(=|:|\\s))?\\s?"
    end = '(\\sdeg)?'
    raSex = '(?P<raSex>(\n                            (?P<raHrs>\\d|[0-1]\\d|[2][0-3])(:\\s?|\\s|h\\s?)\n                            (?P<raMin>[0-5][0-9])(:\\s?|\\s|m\\s?)\n                            (?P<raSec>[0-5]\\d|\\d(?!\\d))s?(?P<raSubSec>\\.\\d{1,})?(\\s|\\s?s)?\n                        )\n                )'
    decSex = "(?P<decSex>(\n                            (?P<decDeg>(\\+|-|–)?[0-8]\\d)(:\\s?|\\s|d\\s?|deg\\s|o\\s?)\n                            (?P<decMin>[0-5][0-9])(:\\s?|\\s|m\\s?|'?\\s?)\n                            (?P<decSec>[0-5]?\\d)'?\\s?(?P<decSubSec>\\.\\d{1,3})?'?s?\n                        )\n                )"
    raDeg = '\n                (?P<raDDeg>\\d{1,3}(\\.\\d{1,}))\n            '
    decDeg = '\n                (?P<decDDeg>[\\+\\-\\–]?\\d{1,3}(\\.\\d{1,}))\n            '
    nameList = [
     '(PSN|PNV)\\s?J\\d{8}(\\+|-|–)\\d{3}(\\+|-|–)?\\d{3,4}',
     '(SN|Supernova)\\s?(19|20)\\d{2}[A-Za-z]{1,2}',
     'GX\\s?\\d{3}(\\+|-|–)\\d',
     'Fermi\\s?J\\d{4}(\\+|-|–)\\d{4}',
     'PHL\\s?\\d{3}',
     'QSO\\s?B\\d{4}(\\+|-|–)\\d{3}',
     'PTF(0|1)\\d[a-zA-Z]{1,3}',
     'MASTER\\s?((short\\s)?ot\\s)?J?\\d{6}\\.\\d{2}(\\+|-|–)\\d{6}\\.\\d',
     '(FSRQ\\s?)?PKS\\s?\\d{4}(\\+|-|–)\\d{3}',
     'BZQ\\s?J\\d{4}(\\+|-|–)\\d{4}',
     '(SN(-|–))?LSQ1\\d[a-zA-Z]{1,4}',
     'M31N\\s?(19|20)\\d{2}(\\+|-|–)\\d{2}[a-z]',
     'IGR\\s?J?\\d{5}(\\+|-|–)?\\d{1,4}',
     'GRS\\s?\\d{4}(\\+|-|–)\\d{1,4}',
     'PS1(-|–)?(0|1)\\d[a-zA-Z]{1,3}',
     'SDSS\\s(galaxy\\s)?J\\d{6}\\.\\d{2}(\\+|-|–)\\d{6}\\.\\d',
     '(CSS|MLS|SSS)\\d{6}:\\d{6}(\\+|-|–)\\d{6}',
     'XMM(U|SL1)\\s?J\\d{6}\\.\\d{1}(\\+|-|–)\\d{6}',
     'SAX\\s?J\\d{4}\\.\\d(\\+|-|–)\\d{3,4}',
     '1RXS\\s?J\\d{6}\\.\\d(\\+|-|–)\\d{6}',
     'USNO(-|–)(B1|A2)\\.0\\s?(catalogue\\s?)\\d{4}(-|–)\\d{7}',
     'KS\\s?\\d{4}(\\+|-|–)\\d{3}',
     'AX\\s?J\\d{4}\\.\\d(\\+|-|–)\\d{4}',
     '2MAS(S|X)\\s?J?\\d{8}(\\+|-|–)\\d{7}',
     'SWIFT\\s?J\\d{4,6}\\.\\d(\\+|-|–)\\d{1,6}',
     '4U\\s?\\d{4}(\\+|-|–)\\d{2,4}',
     'Hen\\s\\d{1}(\\+|-|–)\\d{4}',
     '(HMXB\\s?)?XTE\\s?J?\\d{4}(\\+|-|–)\\d{3}',
     'MAXI\\s?J?\\d{4}(\\+|-|–)\\d{3}',
     'PG\\s?J?\\d{4}(\\+|-|–)\\d{3}',
     'PMN\\s?J?\\d{4}(\\+|-|–)\\d{4}',
     'Guide\\sStar\\sCatalog\\sN4HU\\d{6}',
     'CXOGBS\\s?J?\\d{6}\\.8(\\+|-|–)\\d{6}',
     'Galactic\\sPlane\\s(gamma-ray\\s)?Transient\\sJ?\\d{4}(\\+|-|–)\\d{4}',
     'TXS\\s\\d{4}(\\+|-|–)\\d{3}',
     'V\\d{4}\\sSgr',
     'Aql\\sX(\\+|-|–)1',
     'BLAZAR\\s[a-zA-Z\\d]{2}\\s?\\d{3,4}((\\+|-|–)\\d{2})?',
     'SNhunt\\s\\d{1,5}',
     'Nova\\s[a-zA-Z]{3}\\s(19|20)\\d{2}',
     'GRB\\s?\\d{6}[a-zA-Z]{1,2}',
     '\\bV\\d{3,4}\\s(Sagittarii|cyg)',
     'SGR\\s\\d4(\\+|-|–)\\d{2}',
     '(QSO|3EG|2FGL)\\s?J?\\d{4}(\\.\\d)?(\\+|-|–)\\d{4}',
     'BL\\sLacertae',
     '\\bCTA\\s\\d{3}']
    nameStr = ('|').join(nameList)
    reName = re.compile('(%s)' % (nameStr,), re.S | re.I)
    reSexeg = '\n                    %s\n                    %s\n                    %s\n                    %s\n                    %s\n                ' % (start, raSex, middle, decSex, end)
    reSexeg = re.compile('%s' % reSexeg, re.S | re.I | re.X)
    reDegree = '\n                    %s\n                    %s\n                    (\\sdeg)?(\\s?,|:)?\\s{0,2}(and\\s{1,2}|\\(?%s\\)?(;|,)?\\s{0,3})?(Decl?\\.?\\s*?[()\\w\\d\\s]{0,9}(=|:|\\s))?\\s?\n                    %s\n                    %s' % (start, raDeg, raSex, decDeg, end)
    reDegree = re.compile('%s' % (reDegree,), re.S | re.I | re.X)
    reSexTable = '\n                    %s\n                    \\s?(\\||</td>\\s?<td>)?\\s?\n                    %s\n                ' % (raSex, decSex)
    reSexTable = re.compile('%s' % (reSexTable,), re.S | re.I | re.X)
    reSNType = re.compile('type\\s(I[abcilps]{1,3}n?)|(\\bI[abcilnps]{1,3}n?)\\s(SN|supernova)|<td>\\s?\\b(I[abcilps]{1,3}n?)\\b\\s?<\\/td>|(SN\\simpostor)|\\|\\s?\\b(I[abcilps]{1,3}n?)\\b\\s?\\||(SN|supernova)\\s?(I[abcilps]{1,3}n?)', re.S | re.I)
    filename = mdFolder + 'parsed_atels.md'
    for row in rows:
        atelNumber = row['atelNumber']
        userText = row['userText']
        header = '\n# %s: %s' % (row['atelNumber'], row['title'])
        references = '\n### **REFS:** %s' % (row['refList'],)
        numReferences = len(row['refList'])
        tags = '\n### **TAGS:** %s' % (row['tags'],)
        stringsToRemove = [
         '<p>',
         '</p>',
         '<P>',
         '</P>',
         "<P ALIGN=CENTER><EM><A HREF='http://'></A></EM>",
         '<pre>',
         '</pre>',
         '#',
         '<b>',
         '</b>',
         '<br>',
         '</br>',
         '<P ALIGN=CENTER>',
         '<EM>',
         '</EM>',
         '<sup>',
         '</center>',
         '<center>',
         '</sup>',
         '<sub>',
         '</sub>',
         '<SUP>',
         '</CENTER>',
         '<CENTER>',
         '</SUP>',
         '<SUB>',
         '</SUB>',
         '<br />',
         '<pre />',
         '<pre/>',
         '<PRE>',
         '<Pre>',
         '<it>',
         '</it>',
         '<A ',
         '</a>',
         '</A>',
         '<a ',
         '_',
         '--',
         '</BR>',
         '<BR>',
         '&deg;',
         '</div>',
         '<div>',
         'Ã?Â',
         '\xa0',
         '***',
         '<B>',
         '</B>',
         '\n']
        for item in stringsToRemove:
            userText = userText.replace(item, '')

        for i in range(0, 6):
            userText = userText.replace('  ', ' ')

        userText = userText.replace(';', ':')
        userText = userText.replace('&plusmn: 0.001', '')
        try:
            sIter = reSexeg.finditer(userText)
        except:
            sIter = None

        sList = []
        for item in sIter:
            raSec = item.group('raSec')
            if item.group('raSubSec'):
                raSec += item.group('raSubSec')
            decSec = item.group('decSec')
            if item.group('decSubSec'):
                decSec += item.group('decSubSec')
            _raSex = '%s:%s:%s' % (item.group('raHrs'), item.group('raMin'), raSec)
            _decSex = '%s:%s:%s' % (item.group('decDeg'), item.group('decMin'), decSec)
            raDegrees = u.sexToDec(_raSex, ra=True)
            decDegrees = u.sexToDec(_decSex)
            sList.extend([[str(raDegrees), str(decDegrees)]])
            userText = userText.replace(item.group('raSex'), ' **<font color=blue>' + item.group('raSex') + ' </font>** ')
            userText = userText.replace(item.group('decSex'), ' **<font color=blue>' + item.group('decSex') + ' </font>** ')

        try:
            sIter2 = reDegree.finditer(userText)
        except:
            sIter2 = None

        for item in sIter2:
            sList.extend([[item.group('raDDeg'), item.group('decDDeg')]])
            userText = userText.replace(item.group('raDDeg'), ' **<font color=green>' + item.group('raDDeg') + ' </font>** ')
            userText = userText.replace(item.group('decDDeg'), ' **<font color=green>' + item.group('decDDeg') + ' </font>** ')

        try:
            sIter3 = reSexTable.finditer(userText)
        except:
            sIter3 = None

        for item in sIter3:
            raSec = item.group('raSec')
            if item.group('raSubSec'):
                raSec += item.group('raSubSec')
            decSec = item.group('decSec')
            if item.group('decSubSec'):
                decSec += item.group('decSubSec')
            _raSex = '%s:%s:%s' % (item.group('raHrs'), item.group('raMin'), raSec)
            _decSex = '%s:%s:%s' % (item.group('decDeg'), item.group('decMin'), decSec)
            raDegrees = u.sexToDec(_raSex, ra=True)
            decDegrees = u.sexToDec(_decSex)
            sList.extend([[str(raDegrees), str(decDegrees)]])
            userText = userText.replace(item.group('raSex'), ' **<font color=#dc322f>' + item.group('raSex') + ' </font>** ')
            userText = userText.replace(item.group('decSex'), ' **<font color=#dc322f>' + item.group('decSex') + ' </font>** ')

        numCoords = len(sList)
        try:
            sIter4 = reName.finditer(header)
        except:
            sIter4 = None

        try:
            sIter5 = reName.finditer(userText)
        except:
            sIter5 = None

        hnList = []
        for item in sIter4:
            hnList.extend([item.group()])

        hnList = list(set(hnList))
        numHeaderName = len(hnList)
        tnList = []
        for item in sIter5:
            tnList.extend([item.group()])

        tnList = list(set(tnList))
        numTextName = len(tnList)
        nList = list(set(hnList + tnList))
        for i in range(len(nList)):
            nList[i] = at.clean_supernova_name(dbConn, log, nList[i])

        nList = list(set(nList))
        try:
            userText = reName.sub('**<font color=#2aa198>\\1</font>**', userText)
        except:
            pass

        try:
            header = reName.sub('**<font color=#2aa198>\\1</font>**', header)
        except:
            pass

        disc, obs, clas, correction, comment = (0, 0, 0, 0, 0)
        discHead, obsHead, clasHead, correctionHead = (0, 0, 0, 0)
        discText, obsText, clasText = (0, 0, 0)
        dList = []
        reDisc = re.compile('(discovered\\sby\\sMASTER|Detection.{1,20}MASTER|detection\\sof\\sa\\snew\\s|discovery|candidate.{1,10}discovered|\\ba\\s?candidate|\\d{1,4}:\\s((Bright|MASTER)\\sPSN\\sin|Possible\\snew\\s|(A\\s)?new.{1,30}(candidate|discovered)|(Bright|MASTER).{1,20}detection))', re.I | re.M)
        reDiscPhrase = re.compile('(We\\sreport\\sthe\\sdiscovery\\s)', re.I)
        try:
            dpIter = reDiscPhrase.finditer(userText)
        except:
            dpIter = None

        for item in dpIter:
            discHead = 1
            dList.extend([item.group()])

        try:
            dhIter = reDisc.finditer(header)
        except:
            dhIter = None

        for item in dhIter:
            discHead = 1
            dList.extend([item.group()])

        try:
            dtIter = reDisc.finditer(userText)
        except:
            dtIter = None

        for item in dtIter:
            discText = 1
            dList.extend([item.group()])

        dList = list(set(dList))
        if len(dList) > 0:
            try:
                userText = reDiscPhrase.sub('**<font color=#b58900>\\1</font>**', userText)
            except:
                pass

            try:
                userText = reDisc.sub('**<font color=#b58900>\\1</font>**', userText)
            except:
                pass

            try:
                header = reDisc.sub('**<font color=#b58900>\\1</font>**', header)
            except:
                pass

        cList = []
        reClass = re.compile('(classification|SNID|spectroscopic\\sconfirmation|GELATO|discovery.*?SN\\sI[abcilps]{1,3}n?)', re.I)
        try:
            chIter = reClass.finditer(header)
        except:
            chIter = None

        for item in chIter:
            clasHead = 1
            cList.extend([item.group()])

        try:
            ctIter = reClass.finditer(userText)
        except:
            ctIter = None

        for item in ctIter:
            clasText = 1
            cList.extend([item.group()])

        reClass2 = re.compile('(\\sis\\sa\\s|SN\\simpostor|type\\sI[abcilps]{0,3}n?|\\sI[abcilps]{0,3}n?\\ssupernova|\\sa\\sSN\\sI[abcilps]{0,3}n?)', re.I)
        try:
            cIter2 = reClass2.finditer(header)
        except:
            cIter2 = None

        for item in cIter2:
            clasHead = 1
            cList.extend([item.group()])

        cList = list(set(cList))
        if len(cList) > 0:
            try:
                userText = reClass.sub('**<font color=#b58900>\\1</font>**', userText)
            except:
                pass

            try:
                header = reClass.sub('**<font color=#b58900>\\1</font>**', header)
            except:
                pass

            try:
                header = reClass2.sub('**<font color=#b58900>\\1</font>**', header)
            except:
                pass

        oList = []
        reObs = re.compile('(observations?|Outburst\\sof\\s|increase\\sin\\sflux\\s|Progenitor\\sIdentification|observed?|detects|new\\soutburst|monitoring\\sof)', re.I)
        try:
            ohIter = reObs.finditer(header)
        except:
            ohIter = None

        for item in ohIter:
            obsHead = 1
            oList.extend([item.group()])

        try:
            otIter = reObs.finditer(userText)
        except:
            otIter = None

        for item in otIter:
            obsText = 1
            oList.extend([item.group()])

        oList = list(set(oList))
        if len(oList) > 0:
            try:
                userText = reObs.sub('**<font color=#b58900>\\1</font>**', userText)
            except:
                pass

            try:
                header = reObs.sub('**<font color=#b58900>\\1</font>**', header)
            except:
                pass

        tList = []
        reCor = re.compile('((Correction|Erratum|Errata)\\sto)', re.I)
        try:
            tIter = reCor.finditer(userText + header)
        except:
            tIter = None

        for item in tIter:
            tList.extend([item.group()])

        tList = list(set(tList))
        if len(tList) > 0:
            correctionHead = 1
            try:
                userText = reCor.sub('**<font color=#b58900>\\1</font>**', userText)
            except:
                pass

            try:
                header = reCor.sub('**<font color=#b58900>\\1</font>**', header)
            except:
                pass

        if 'Comment' in tags:
            comment = 1
        atelType = ''
        obs, clas, disc, correction = (0, 0, 0, 0)
        if clasHead == 1:
            clas = 1
        if obsHead == 1:
            obs = 1
        if discHead == 1:
            disc = 1
        if correctionHead == 1:
            correction = 1
        if comment == 1:
            comment = 1
        if clasText == 1 and disc == 0 and obs == 0:
            clas = 1
        if obsText == 1 and disc == 0 and clas == 0:
            obs = 1
        if discText == 1 and obs == 0 and clas == 0:
            disc = 1
        if comment == 1:
            comment = 1
        if comment == 1:
            atelType += ' comment '
        if correction == 1:
            atelType += ' correction '
        if disc == 1:
            atelType += ' discovery '
        if clas == 1:
            atelType += ' classification '
        if obs == 1:
            atelType += ' observation '
        header = header + atelType
        SNTypeList = []
        SNTypeReplace = []
        singleClassification = None
        oneType = None
        if 'classification' in atelType:
            try:
                SNTypeIter = reSNType.finditer(header + userText)
            except:
                SNTypeIter is None

            for item in SNTypeIter:
                SNTypeReplace.extend([item.group()])
                SNTypeList.extend([item.group(1)])
                SNTypeList.extend([item.group(2)])
                SNTypeList.extend([item.group(4)])
                SNTypeList.extend([item.group(5)])
                SNTypeList.extend([item.group(6)])
                SNTypeList.extend([item.group(8)])

            SNTypeList = list(set(SNTypeList))
            SNTypeReplace = list(set(SNTypeReplace))
            for item in SNTypeReplace:
                userText = userText.replace(item, ' ***<font color=#859900>' + item + ' </font>*** ')
                header = header.replace(item, ' ***<font color=#859900>' + item + ' </font>*** ')

            switch = 0
            for item in SNTypeList:
                if item:
                    if switch == 0:
                        oneType = item
                        switch = 1
                    else:
                        oneType = None
                    header = header + ' ***<font color=#859900>' + item + ' </font>*** '

        if not atelType:
            atelType = 'observation'
        dateParsed = cu.get_now_sql_datetime()
        sqlQuery = '\n                        UPDATE atel_fullcontent\n                        SET atelType = "%s",\n                        dateParsed = "%s"\n                        WHERE atelNUmber = %s\n                    ' % (atelType, dateParsed, atelNumber)
        try:
            log.debug('attempting to update the ateltype and parsedate for atel number %s' % (atelNumber,))
            m.execute_mysql_write_query(sqlQuery, dbConn, log)
        except Exception as e:
            log.error('could not update the ateltype and parsedate for atel number %s - failed with this error: %s ' % (atelNumber, str(e)))
            return -1

        isSN = 0
        if 'Supernovae' in tags:
            isSN = 1
            if oneType is not None:
                singleClassification = oneType
            else:
                singleClassification = None
        for item in sList:
            atelName = 'atel_' + str(atelNumber)
            atelUrl = 'http://www.astronomerstelegram.org/?read=' + str(atelNumber)
            survey = 'atel-coords'
            sqlQuery = 'INSERT INTO atel_coordinates (\n                                            atelNumber,\n                                            atelName,\n                                            atelUrl,\n                                            survey,\n                                            raDeg,\n                                            decDeg,\n                                            supernovaTag\n                                        )\n                    VALUES (\n                                %s,\n                                "%s",\n                                "%s",\n                                "%s",\n                                %s,\n                                %s,\n                                %s\n                            )' % (atelNumber, atelName, atelUrl, survey, item[0], item[1], isSN)
            try:
                log.debug('attempting to ingest the atel coordinates into the database')
                m.execute_mysql_write_query(sqlQuery, dbConn, log)
            except Exception as e:
                log.error('could not ingest the atel coordinates into the database - failed with this error: %s ' % (str(e),))
                return -1

            if singleClassification is not None:
                sqlQuery = 'UPDATE atel_coordinates\n                                SET singleClassification = "%s"\n                                WHERE atelNumber = %s' % (singleClassification, atelNumber)
            try:
                log.debug('attempting to update classification for atel %s' % (atelNumber,))
                m.execute_mysql_write_query(sqlQuery, dbConn, log)
            except Exception as e:
                log.error('could not update classification for atel %s - failed with this error: %s ' % (atelNumber, str(e)))
                return -1

        for item in nList:
            atelName = 'atel_' + str(atelNumber)
            atelUrl = 'http://www.astronomerstelegram.org/?read=' + str(atelNumber)
            survey = 'atel-names'
            sqlQuery = 'INSERT INTO atel_names (\n                                            atelNumber,\n                                            atelName,\n                                            atelUrl,\n                                            survey,\n                                            name,\n                                            supernovaTag\n                                        )\n                    VALUES (\n                                %s,\n                                "%s",\n                                "%s",\n                                "%s",\n                                "%s",\n                                %s\n                    )' % (atelNumber, atelName, atelUrl, survey, item, isSN)
            try:
                log.debug('attempting to ingest the atel names into the database')
                m.execute_mysql_write_query(sqlQuery, dbConn, log)
            except Exception as e:
                log.error('could not ingest the atel names into the database - failed with this error: %s ' % (str(e),))
                return -1

            if singleClassification is not None:
                sqlQuery = 'UPDATE atel_names\n                                SET singleClassification = "%s"\n                                WHERE atelNumber = %s' % (singleClassification, atelNumber)
            try:
                log.debug('attempting to update classification for atel %s' % (atelNumber,))
                m.execute_mysql_write_query(sqlQuery, dbConn, log)
            except Exception as e:
                log.error('could not update classification for atel %s - failed with this error: %s ' % (atelNumber, str(e)))
                return -1

    return


if __name__ == '__main__':
    main()