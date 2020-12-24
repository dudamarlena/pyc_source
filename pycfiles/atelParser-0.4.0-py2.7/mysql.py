# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/atelParser/mysql.py
# Compiled at: 2020-05-04 14:34:29
"""
*Import ATel into MySQL database and parse for names and coordinates*

:Author:
    David Young
"""
from builtins import str
from builtins import range
from builtins import object
import sys, os
os.environ['TERM'] = 'vt100'
from fundamentals import tools, times
import re, sys
from datetime import datetime
from fundamentals.mysql import database, readquery, writequery, convert_dictionary_to_mysql_table
import codecs
from astrocalc.coords import unit_conversion

class mysql(object):
    """
    *The worker class for the mysql module*

    **Key Arguments**

    - ``log`` -- logger
    - ``settings`` -- the settings dictionary
    - ``reParse`` -- re-parse all existing atels? Useful if new names have been added to the parse-list
    

    **Usage**

    To setup your logger, settings and database connections, please use the ``fundamentals`` package (`see tutorial here <http://fundamentals.readthedocs.io/en/latest/#tutorial>`_). 

    To initiate a mysql object, use the following:

    ```python
    from atelParser import mysql
    parser = mysql(
        log=log,
        settings=settings
    ) 
    ```
    
    """

    def __init__(self, log, settings=False, reParse=False):
        self.log = log
        log.debug("instansiating a new 'mysql' object")
        self.settings = settings
        self.reParse = reParse
        self.dbSettings = settings['database settings']
        self.dbConn = database(log=log, dbSettings=self.dbSettings).connect()
        return

    def atels_to_database(self):
        """*Parse ATels into a mysql db. Parser to add ATels into a mysql db - each ATel has 'element' data (top level - title, author ...) and 'item' data (object specific data - ra, dec, mag, name ...).
            The parser will add one row per 'item' (object) into the db table*

        **Return**

        - None
        

        **Usage**

        ```python
        from atelParser import mysql
        parser = mysql(
            log=log,
            settings=settings
        )
        parser.atels_to_database()
        ```
        
        """
        self.log.debug('starting the ``atels_to_database`` method')
        self._create_atel_database_tables()
        sqlQuery = '\n            SELECT distinct atelNumber\n                        FROM atel_fullcontent\n                        ORDER BY atelNumber DESC\n        ' % locals()
        rows = readquery(log=self.log, sqlQuery=sqlQuery, dbConn=self.dbConn, quiet=False)
        databaseAtels = []
        databaseAtels = []
        databaseAtels[:] = [ int(l['atelNumber']) for l in rows ]
        basePath = self.settings['atel-directory']
        atelDownloaded = []
        atelDownloaded[:] = [ int(d.replace('.html', '')) for d in os.listdir(basePath) if os.path.isfile(os.path.join(basePath, d)) and '.html' in d
                            ]
        atelsToParse = []
        atelsToParse[:] = [ self.settings['atel-directory'] + '/%(a)0.8d.html' % locals() for a in atelDownloaded if a not in databaseAtels
                          ]
        for atel in atelsToParse:
            if not atel:
                continue
            try:
                self.log.debug('attempting to open the file %s' % (atel,))
                readFile = codecs.open(atel, encoding='utf-8', mode='r')
                html = readFile.read()
                readFile.close()
            except IOError as e:
                message = 'could not open the file %s' % (atel,)
                self.log.critical(message)
                raise IOError(message)

            elementDict = {}
            reTitle = re.compile('<TITLE>.*?#\\d{1,5}:\\s?(.*?)\\s?<\\/TITLE>', re.M | re.I)
            try:
                title = reTitle.search(html).group(1)
            except:
                continue
                title = None

            elementDict['title'] = title
            reAtelNumber = re.compile('<P ALIGN=CENTER>\\s?ATel\\s?#(\\d{1,5})', re.M | re.I)
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
            reOneRef = re.compile('http:\\/\\/www.astronomerstelegram.org\\/\\?read=(\\d{1,5})', re.M | re.I)
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
            reOneBackRef = re.compile('<A HREF="http:\\/\\/www.astronomerstelegram.org\\/\\?read=(\\d{1,7})">\\1</a>', re.M | re.I)
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
            convert_dictionary_to_mysql_table(dbConn=self.dbConn, log=self.log, dictionary=elementDict, dbTableName='atel_fullcontent', uniqueKeyList=[
             'atelNumber'], dateModified=False, returnInsertOnly=False, replace=False, batchInserts=False, reDatetime=re.compile('^[0-9]{4}-[0-9]{2}-[0-9]{2}T'))

        self.log.debug('completed the ``atels_to_database`` method')
        return

    def parse_atels(self):
        """*Parse the content of the ATels in the database, appending the various components and values to the db. Also includes the ability convert the atels to markdown, highlighting matches of the parsing regexs.*

        **Return**

        - None
        

        **Usage**

        - write a command-line tool for this method
            - update package tutorial with command-line tool info if needed

        ```python
        from atelParser import mysql
        parser = mysql(
            log=log,
            settings=settings
        )
        parser.parse_atels()
        ```
        
        """
        self.log.debug('starting the ``parse_atels`` method')
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
        converter = unit_conversion(log=self.log)
        if self.reParse == False:
            whereClause = 'dateParsed is NULL'
        else:
            whereClause = '1=1'
        sqlQuery = 'SELECT *\n                        FROM atel_fullcontent\n                        where %(whereClause)s \n                        ORDER BY atelNumber' % locals()
        rows = readquery(log=self.log, sqlQuery=sqlQuery, dbConn=self.dbConn, quiet=False)
        start = '((R\\.?A\\.?\\b|Coord)[/()\\w\\d\\s,.]{0,9}(\\(J2000(\\.0)?\\)\\s?)?(=|:|\\s)|\\d{4}-\\d{2}-\\d{2})\\s{0,2}[+(]{0,2}'
        middle = "(\\sdeg)?(\\s?,|:)?\\s{0,2}(and\\s{1,2}|\\(?[\\ddeg.':\\s]{1,16}\\)?(;|,)?\\s{0,3})?(Decl?\\.?\\s*?[()\\w\\d\\s]{0,9}(=|:|\\s))?\\s?"
        end = '(\\sdeg)?'
        raSex = '(?P<raSex>(\n                                (?P<raHrs>\\d|[0-1]\\d|[2][0-3])(:\\s?|\\s|h\\s?)\n                                (?P<raMin>[0-5][0-9])(:\\s?|\\s|m\\s?)\n                                (?P<raSec>[0-5]\\d|\\d(?!\\d))s?(?P<raSubSec>\\.\\d{1,})?(\\s|\\s?s)?\n                            )\n                    )'
        decSex = "(?P<decSex>(\n                                (?P<decDeg>(\\+|-|–)?[0-8]\\d)(:\\s?|\\s|d\\s?|deg\\s|o\\s?)\n                                (?P<decMin>[0-5][0-9])(:\\s?|\\s|m\\s?|'?\\s?)\n                                (?P<decSec>[0-5]?\\d)'?\\s?(?P<decSubSec>\\.\\d{1,3})?'?s?\n                            )\n                    )"
        raDeg = '\n                    (?P<raDDeg>\\d{1,3}(\\.\\d{1,}))\n                '
        decDeg = '\n                    (?P<decDDeg>[\\+\\-\\–]?\\d{1,3}(\\.\\d{1,}))\n                '
        nameList = [
         '(PSN|PNV)\\s?J\\d{8}(\\+|-|–)\\d{3}(\\+|-|–)?\\d{3,4}',
         '(SN|Supernova)\\s?(19|20)\\d{2}[A-Za-z]{1,4}',
         'GX\\s?\\d{3}(\\+|-|–)\\d',
         'Fermi\\s?J\\d{4}(\\+|-|–)\\d{4}',
         'PHL\\s?\\d{3}',
         'QSO\\s?B\\d{4}(\\+|-|–)\\d{3}',
         'i?PTF(0|1)\\d[a-zA-Z]{1,3}',
         'MASTER\\s?((short\\s)?ot\\s)?J?\\d{6}\\.\\d{2}(\\+|-|–)\\d{6}\\.\\d',
         '(FSRQ\\s?)?PKS\\s?\\d{4}(\\+|-|–)\\d{3}',
         'BZQ\\s?J\\d{4}(\\+|-|–)\\d{4}',
         '(SN(-|–))?LSQ1\\d[a-zA-Z]{1,4}',
         'M31N\\s?(19|20)\\d{2}(\\+|-|–)\\d{2}[a-z]',
         'IGR\\s?J?\\d{5}(\\+|-|–)?\\d{1,4}',
         'GRS\\s?\\d{4}(\\+|-|–)\\d{1,4}',
         'PS1(-|–)?(0|1)\\d[a-zA-Z]{1,3}',
         'PS1\\d[a-zA-Z]{1,3}',
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
         '\\bCTA\\s\\d{3}',
         'ASASSN( |–|-)1\\d[a-zA-Z]{1,4}',
         'OGLE-201\\d-(SN|NOVA)-\\d{1,4}',
         'OGLE ?1\\d[a-zA-Z]{1,4}',
         'Gaia ?1\\d[a-zA-Z]{1,4}',
         'DES1\\d[a-zA-Z]\\d[a-zA-Z]{1,4}',
         'HFF1\\d[a-zA-Z]{1,4}',
         'HSC-SN1\\d[a-zA-Z]{1,4}',
         'MASTER ?J\\d{5,6}\\.\\d{2}\\+\\d{5,6}\\.\\d{1,2}',
         'SKY( |-|–|_)J\\d{6,8}(-|–|\\+)\\d{6,8}',
         'SMT ?\\d{6,8}(-|–|\\+)\\d{6,8}',
         'SN20\\d{2}[a-zA-Z]{1,4}',
         'TCP ?J\\d{6,8}(-|–|\\+)\\d{6,8}',
         'ATLAS\\d{2}\\w{1,8}',
         'AT20\\d{2}[a-zA-Z]{1,4}',
         'ZTF\\d{2}[a-zA-Z]{1,15}']
        nameStr = ('|').join(nameList)
        reName = re.compile('(%s)' % (nameStr,), re.S | re.I)
        reSexeg = '\n                        %s\n                        %s\n                        %s\n                        %s\n                        %s\n                    ' % (start, raSex, middle, decSex, end)
        reSexeg = re.compile('%s' % reSexeg, re.S | re.I | re.X)
        reDegree = '\n                        %s\n                        %s\n                        (\\sdeg)?(\\s?,|:)?\\s{0,2}(and\\s{1,2}|\\(?%s\\)?(;|,)?\\s{0,3})?(Decl?\\.?\\s*?[()\\w\\d\\s]{0,9}(=|:|\\s))?\\s?\n                        %s\n                        %s' % (start, raDeg, raSex, decDeg, end)
        reDegree = re.compile('%s' % (reDegree,), re.S | re.I | re.X)
        reSexTable = '\n                        %s\n                        \\s?(\\||</td>\\s?<td>)?\\s?\n                        %s\n                    ' % (raSex, decSex)
        reSexTable = re.compile('%s' % (reSexTable,), re.S | re.I | re.X)
        reSNType = re.compile('type\\s(I[abcilps]{1,3}n?)|(\\bI[abcilnps]{1,3}n?)\\s(SN|supernova)|<td>\\s?\\b(I[abcilps]{1,3}n?)\\b\\s?<\\/td>|(SN\\simpostor)|\\|\\s?\\b(I[abcilps]{1,3}n?)\\b\\s?\\||(SN|supernova)\\s?(I[abcilps]{1,3}n?)', re.S | re.I)
        for row in rows:
            atelNumber = row['atelNumber']
            userText = row['userText']
            self.log.info('parsing atel: `%(atelNumber)s`' % locals())
            if isinstance(userText, (('').__class__, ('').__class__)):
                try:
                    userText = str(userText, encoding='utf-8', errors='replace')
                except:
                    pass

            header = '\n# %s: %s' % (row['atelNumber'], row['title'])
            references = '\n### **REFS:** %s' % (row['refList'],)
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
                _raSex = '%s:%s:%s' % (
                 item.group('raHrs'), item.group('raMin'), raSec)
                _decSex = '%s:%s:%s' % (
                 item.group('decDeg'), item.group('decMin'), decSec)
                raDegrees = converter.ra_sexegesimal_to_decimal(ra=_raSex)
                decDegrees = converter.dec_sexegesimal_to_decimal(dec=_decSex)
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
                _raSex = '%s:%s:%s' % (
                 item.group('raHrs'), item.group('raMin'), raSec)
                _decSex = '%s:%s:%s' % (
                 item.group('decDeg'), item.group('decMin'), decSec)
                raDegrees = converter.ra_sexegesimal_to_decimal(ra=_raSex)
                decDegrees = converter.dec_sexegesimal_to_decimal(dec=_decSex)
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
                nList[i] = clean_supernova_name(self.log, nList[i])

            nList = list(set(nList))
            userText = reName.sub('**<font color=#2aa198>\\1</font>**', userText)
            header = reName.sub('**<font color=#2aa198>\\1</font>**', header)
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
            dateParsed = times.get_now_sql_datetime()
            sqlQuery = '\n                            UPDATE atel_fullcontent\n                            SET atelType = "%s",\n                            dateParsed = "%s"\n                            WHERE atelNUmber = %s\n                        ' % (atelType.strip(), dateParsed, atelNumber)
            writequery(log=self.log, sqlQuery=sqlQuery, dbConn=self.dbConn, Force=False)
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
                sqlQuery = 'INSERT INTO atel_coordinates (\n                                                atelNumber,\n                                                atelName,\n                                                atelUrl,\n                                                survey,\n                                                raDeg,\n                                                decDeg,\n                                                supernovaTag\n                                            )\n                        VALUES (\n                                    %s,\n                                    "%s",\n                                    "%s",\n                                    "%s",\n                                    %s,\n                                    %s,\n                                    %s\n                                )' % (atelNumber, atelName, atelUrl, survey, item[0], item[1], isSN)
                writequery(log=self.log, sqlQuery=sqlQuery, dbConn=self.dbConn)
                if singleClassification is not None:
                    sqlQuery = 'UPDATE atel_coordinates\n                                    SET singleClassification = "%s"\n                                    WHERE atelNumber = %s' % (singleClassification, atelNumber)
                    writequery(log=self.log, sqlQuery=sqlQuery, dbConn=self.dbConn)

            for item in nList:
                atelName = 'atel_' + str(atelNumber)
                atelUrl = 'http://www.astronomerstelegram.org/?read=' + str(atelNumber)
                survey = 'atel-names'
                sqlQuery = 'INSERT INTO atel_names (\n                                                atelNumber,\n                                                atelName,\n                                                atelUrl,\n                                                survey,\n                                                name,\n                                                supernovaTag\n                                            )\n                        VALUES (\n                                    %s,\n                                    "%s",\n                                    "%s",\n                                    "%s",\n                                    "%s",\n                                    %s\n                        )' % (atelNumber, atelName, atelUrl, survey, item, isSN)
                writequery(log=self.log, sqlQuery=sqlQuery, dbConn=self.dbConn)
                if singleClassification is not None:
                    sqlQuery = 'UPDATE atel_names\n                                    SET singleClassification = "%s"\n                                    WHERE atelNumber = %s' % (singleClassification, atelNumber)
                    writequery(log=self.log, sqlQuery=sqlQuery, dbConn=self.dbConn)

        self.log.debug('completed the ``parse_atels`` method')
        return

    def populate_htm_columns(self):
        """*populate htm columns in the atel_coordinates table*

        **Usage**

        To add the HTM columns (levels 10, 13 & 16) to the atel_coordinates database add this to your code:

        ```python
        from atelParser import mysql
        parser = mysql(
            log=log,
            settings=settings
        )
        parser.populate_htm_columns()
        ```
        
        """
        self.log.debug('starting the ``populate_htm_columns`` method')
        from HMpTy.mysql import add_htm_ids_to_mysql_database_table
        add_htm_ids_to_mysql_database_table(raColName='raDeg', declColName='decDeg', tableName='atel_coordinates', dbConn=self.dbConn, log=self.log, primaryIdColumnName='primaryId', dbSettings=self.dbSettings)
        self.log.debug('completed the ``populate_htm_columns`` method')
        return

    def _create_atel_database_tables(self):
        """*create the database tables required to host the atel information*

        **Key Arguments**

        # -
        

        **Usage**

        

        ```python
        usage code 
        ```

        ---

        ```eval_rst
        .. todo::

            - add usage info
            - create a sublime snippet for usage
            - write a command-line tool for this method
            - update package tutorial with command-line tool info if needed
        ```
        """
        self.log.debug('starting the ``_create_atel_database_tables`` method')
        sqlQuery = "CREATE TABLE IF NOT EXISTS `atel_coordinates` (\n              `primaryId` bigint(20) NOT NULL AUTO_INCREMENT,\n              `atelNumber` int(11) NOT NULL,\n              `raDeg` double NOT NULL,\n              `decDeg` double NOT NULL,\n              `crossMatchDate` datetime DEFAULT NULL,\n              `singleClassification` varchar(45) DEFAULT NULL,\n              `supernovaTag` int(11) DEFAULT NULL,\n              `ingested` int(11) DEFAULT '0',\n              `atelName` varchar(45) NOT NULL,\n              `atelUrl` varchar(200) NOT NULL,\n              `htm16ID` bigint(20) DEFAULT NULL,\n              `summaryRow` tinyint(4) DEFAULT NULL,\n              `survey` varchar(45) NOT NULL,\n              `titleToComment` tinyint(4) NOT NULL DEFAULT '0',\n              `htm13ID` int(11) DEFAULT NULL,\n              `htm10ID` int(11) DEFAULT NULL,\n              `updated` tinyint(1) DEFAULT '0',\n              `dateLastModified` datetime DEFAULT CURRENT_TIMESTAMP,\n              `dateCreated` datetime DEFAULT CURRENT_TIMESTAMP,\n              PRIMARY KEY (`primaryId`),\n              UNIQUE KEY `atelnumber_ra_dec` (`atelNumber`,`raDeg`,`decDeg`),\n              KEY `ra_deg` (`raDeg`,`decDeg`),\n              KEY `atelNumber` (`atelNumber`),\n              KEY `idx_htm16ID` (`htm16ID`),\n              KEY `idx_htm10ID` (`htm13ID`),\n              KEY `idx_htm13ID` (`htm13ID`),\n              KEY `i_htm10ID` (`htm10ID`),\n              KEY `i_htm13ID` (`htm13ID`),\n              KEY `i_htm16ID` (`htm16ID`)\n            ) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPRESSED KEY_BLOCK_SIZE=8;" % locals()
        writequery(log=self.log, sqlQuery=sqlQuery, dbConn=self.dbConn)
        sqlQuery = "CREATE TABLE IF NOT EXISTS `atel_fullcontent` (\n              `primaryId` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'An internal counter',\n              `atelNumber` int(11) DEFAULT NULL,\n              `authors` mediumtext,\n              `backRefList` varchar(2000) DEFAULT NULL,\n              `dateCreated` datetime DEFAULT NULL,\n              `dateLastModified` datetime DEFAULT NULL,\n              `dateLastRead` datetime DEFAULT NULL,\n              `email` varchar(450) DEFAULT NULL,\n              `refList` varchar(450) DEFAULT NULL,\n              `tags` varchar(450) DEFAULT NULL,\n              `title` varchar(450) DEFAULT NULL,\n              `userText` mediumtext,\n              `datePublished` datetime NOT NULL,\n              `atelType` varchar(500) DEFAULT NULL,\n              `dateParsed` datetime DEFAULT NULL COMMENT 'The date the ATel text was parsed for names and coordinates',\n              `updated` tinyint(4) DEFAULT '0',\n              PRIMARY KEY (`primaryId`),\n              UNIQUE KEY `atelnumber` (`atelNumber`)\n            ) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPRESSED KEY_BLOCK_SIZE=8;\n            " % locals()
        writequery(log=self.log, sqlQuery=sqlQuery, dbConn=self.dbConn)
        sqlQuery = "CREATE TABLE IF NOT EXISTS `atel_names` (\n              `primaryId` bigint(20) NOT NULL AUTO_INCREMENT,\n              `atelNumber` int(11) NOT NULL,\n              `name` varchar(200) NOT NULL,\n              `crossMatchDate` datetime DEFAULT NULL,\n              `singleClassification` varchar(45) DEFAULT NULL,\n              `supernovaTag` int(11) DEFAULT NULL,\n              `ingested` int(11) DEFAULT '0',\n              `atelName` varchar(45) NOT NULL,\n              `atelUrl` varchar(200) NOT NULL,\n              `survey` varchar(45) NOT NULL,\n              `titleToComment` tinyint(4) NOT NULL DEFAULT '0',\n              `summaryRow` tinyint(4) DEFAULT NULL,\n              PRIMARY KEY (`primaryId`),\n              UNIQUE KEY `atelnumber_name` (`atelNumber`,`name`),\n              KEY `atelNumber` (`atelNumber`),\n              KEY `name` (`name`)\n            ) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPRESSED KEY_BLOCK_SIZE=8;\n        " % locals()
        writequery(log=self.log, sqlQuery=sqlQuery, dbConn=self.dbConn)
        self.log.debug('completed the ``_create_atel_database_tables`` method')
        return


def clean_supernova_name(log, snName):
    """
    *Clean a SN name. As a string, this function will attempt to clean up the name so that it is somewhat homogeneous with SN/transient from the same survey/atel system.*

    **Key Arguments**

    - ``log`` -- logger
    - ``snName`` -- sn name to be cleaned (string)
    

    **Return**

    - ``snName`` -- cleaned sn name (string)
    
    """
    if isinstance(snName, (('').__class__, ('').__class__)):
        try:
            snName = str(snName, encoding='utf-8', errors='replace')
        except:
            pass

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