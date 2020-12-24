# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\ProgramData\lib\site-packages\arelle\FunctionIxt.py
# Compiled at: 2018-02-26 09:10:06
# Size of source mod 2**32: 38171 bytes
"""
Created on July 5, 2011

@author: Mark V Systems Limited
(c) Copyright 2011 Mark V Systems Limited, All rights reserved.
"""
try:
    import regex as re
except ImportError:
    import re

from arelle.PluginManager import pluginClassMethods
from arelle import XPathContext
from datetime import datetime

class ixtFunctionNotAvailable(Exception):

    def __init__(self):
        self.args = (
         _('ixt function not available'),)

    def __repr__(self):
        return self.args[0]


def call(xc, p, qn, args):
    try:
        _ixtFunction = ixtNamespaceFunctions[qn.namespaceURI][qn.localName]
    except KeyError:
        raise XPathContext.FunctionNotAvailable(str(qn))

    if len(args) != 1:
        raise XPathContext.FunctionNumArgs()
    if len(args[0]) != 1:
        raise XPathContext.FunctionArgType(1, 'xs:string')
    return _ixtFunction(str(args[0][0]))


dateslashPattern = re.compile('^\\s*(\\d+)/(\\d+)/(\\d+)\\s*$')
daymonthslashPattern = re.compile('^\\s*([0-9]{1,2})/([0-9]{1,2})\\s*$')
monthdayslashPattern = re.compile('^\\s*([0-9]{1,2})/([0-9]{1,2})\\s*$')
datedotPattern = re.compile('^\\s*(\\d+)\\.(\\d+)\\.(\\d+)\\s*$')
daymonthPattern = re.compile('^\\s*([0-9]{1,2})[^0-9]+([0-9]{1,2})\\s*$')
monthdayPattern = re.compile('^\\s*([0-9]{1,2})[^0-9]+([0-9]{1,2})[A-Za-z]*\\s*$')
daymonthyearPattern = re.compile('^\\s*([0-9]{1,2})[^0-9]+([0-9]{1,2})[^0-9]+([0-9]{4}|[0-9]{1,2})\\s*$')
monthdayyearPattern = re.compile('^\\s*([0-9]{1,2})[^0-9]+([0-9]{1,2})[^0-9]+([0-9]{4}|[0-9]{1,2})\\s*$')
dateUsPattern = re.compile('^\\s*(\\w+)\\s+(\\d+),\\s+(\\d+)\\s*$')
dateEuPattern = re.compile('^\\s*(\\d+)\\s+(\\w+)\\s+(\\d+)\\s*$')
daymonthDkPattern = re.compile('^\\s*([0-9]{1,2})[^0-9]+(jan|feb|mar|apr|maj|jun|jul|aug|sep|okt|nov|dec)([A-Za-z]*)([.]*)\\s*$', re.IGNORECASE)
daymonthEnPattern = re.compile('^\\s*([0-9]{1,2})[^0-9]+(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC|JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER)\\s*$')
monthdayEnPattern = re.compile('^\\s*(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC|JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER)[^0-9]+([0-9]{1,2})[A-Za-z]{0,2}\\s*$')
daymonthyearDkPattern = re.compile('^\\s*([0-9]{1,2})[^0-9]+(jan|feb|mar|apr|maj|jun|jul|aug|sep|okt|nov|dec)([A-Za-z]*)([.]*)[^0-9]*([0-9]{4}|[0-9]{1,2})\\s*$', re.IGNORECASE)
daymonthyearEnPattern = re.compile('^\\s*([0-9]{1,2})[^0-9]+(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC|JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER)[^0-9]+([0-9]{4}|[0-9]{1,2})\\s*$')
daymonthyearInPattern = re.compile('^\\s*([0-9\\u0966-\\u096F]{1,2})\\s([\\u0966-\\u096F]{2}|[^\\s0-9\\u0966-\\u096F]+)\\s([0-9\\u0966-\\u096F]{2}|[0-9\\u0966-\\u096F]{4})\\s*$')
monthdayyearEnPattern = re.compile('^\\s*(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC|JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER)[^0-9]+([0-9]+)[^0-9]+([0-9]{4}|[0-9]{1,2})\\s*$')
monthyearDkPattern = re.compile('^\\s*(jan|feb|mar|apr|maj|jun|jul|aug|sep|okt|nov|dec)([A-Za-z]*)([.]*)[^0-9]*([0-9]{4}|[0-9]{1,2})\\s*$', re.IGNORECASE)
monthyearEnPattern = re.compile('^\\s*(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC|JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER)[^0-9]+([0-9]{1,2}|[0-9]{4})\\s*$')
monthyearInPattern = re.compile('^\\s*([^\\s0-9\\u0966-\\u096F]+)\\s([0-9\\u0966-\\u096F]{4})\\s*$')
yearmonthEnPattern = re.compile('^\\s*([0-9]{1,2}|[0-9]{4})[^0-9]+(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC|JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER)\\s*$')
dateLongUkTR1Pattern = re.compile('^\\s*(\\d|\\d{2,2}) (January|February|March|April|May|June|July|August|September|October|November|December) (\\d{2,2}|\\d{4,4})\\s*$')
dateShortUkTR1Pattern = re.compile('^\\s*(\\d|\\d{2,2}) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (\\d{2,2}|\\d{4,4})\\s*$')
dateLongUsTR1Pattern = re.compile('^\\s*(January|February|March|April|May|June|July|August|September|October|November|December) (\\d|\\d{2,2}), (\\d{2,2}|\\d{4,4})\\s*$')
dateShortUsTR1Pattern = re.compile('^\\s*(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (\\d|\\d{2,2}), (\\d{2,2}|\\d{4,4})\\s*$')
daymonthLongEnTR1Pattern = re.compile('^\\s*(\\d|\\d{2,2}) (January|February|March|April|May|June|July|August|September|October|November|December)\\s*$')
daymonthShortEnTR1Pattern = re.compile('^\\s*([0-9]{1,2})\\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\\s*$')
monthdayLongEnTR1Pattern = re.compile('^\\s*(January|February|March|April|May|June|July|August|September|October|November|December) (\\d|\\d{2,2})\\s*$')
monthdayShortEnTR1Pattern = re.compile('^\\s*(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\\s+([0-9]{1,2})[A-Za-z]{0,2}\\s*$')
monthyearShortEnTR1Pattern = re.compile('^\\s*(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\\s+([0-9]{2}|[0-9]{4})\\s*$')
monthyearLongEnTR1Pattern = re.compile('^\\s*(January|February|March|April|May|June|July|August|September|October|November|December)\\s+([0-9]{2}|[0-9]{4})\\s*$')
yearmonthShortEnTR1Pattern = re.compile('^\\s*([0-9]{2}|[0-9]{4})\\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\\s*$')
yearmonthLongEnTR1Pattern = re.compile('^\\s*([0-9]{2}|[0-9]{4})\\s+(January|February|March|April|May|June|July|August|September|October|November|December)\\s*$')
erayearmonthjpPattern = re.compile('^[\\s\xa0]*(明治|明|大正|大|昭和|昭|平成|平)[\\s\xa0]*([0-9]{1,2}|元)[\\s\xa0]*年[\\s\xa0]*([0-9]{1,2})[\\s\xa0]*月[\\s\xa0]*$')
erayearmonthdayjpPattern = re.compile('^[\\s\xa0]*(明治|明|大正|大|昭和|昭|平成|平)[\\s\xa0]*([0-9]{1,2}|元)[\\s\xa0]*年[\\s\xa0]*([0-9]{1,2})[\\s\xa0]*月[\\s\xa0]*([0-9]{1,2})[\\s\xa0]*日[\\s\xa0]*$')
yearmonthcjkPattern = re.compile('^[\\s\xa0]*([0-9]{4}|[0-9]{1,2})[\\s\xa0]*年[\\s\xa0]*([0-9]{1,2})[\\s\xa0]*月\\s*$')
yearmonthdaycjkPattern = re.compile('^[\\s\xa0]*([0-9]{4}|[0-9]{1,2})[\\s\xa0]*年[\\s\xa0]*([0-9]{1,2})[\\s\xa0]*月[\\s\xa0]*([0-9]{1,2})[\\s\xa0]*日[\\s\xa0]*$')
monthyearPattern = re.compile('^[\\s\xa0]*([0-9]{1,2})[^0-9]+([0-9]{4}|[0-9]{1,2})[\\s\xa0]*$')
yearmonthdayPattern = re.compile('^[\\s\xa0]*([0-9]{4}|[0-9]{1,2})[^0-9]+([0-9]{1,2})[^0-9]+([0-9]{1,2})[\\s\xa0]*$')
zeroDashPattern = re.compile('^\\s*([-]|\\u002D|\\u002D|\\u058A|\\u05BE|\\u2010|\\u2011|\\u2012|\\u2013|\\u2014|\\u2015|\\uFE58|\\uFE63|\\uFF0D)\\s*$')
numDotDecimalPattern = re.compile('^\\s*[0-9]{1,3}([, \\xA0]?[0-9]{3})*(\\.[0-9]+)?\\s*$')
numDotDecimalInPattern = re.compile('^(([0-9]{1,2}[, \\xA0])?([0-9]{2}[, \\xA0])*[0-9]{3})([.][0-9]+)?$|^([0-9]+)([.][0-9]+)?$')
numCommaDecimalPattern = re.compile('^\\s*[0-9]{1,3}([. \\xA0]?[0-9]{3})*(,[0-9]+)?\\s*$')
numUnitDecimalPattern = re.compile('^([0]|([1-9][0-9]{0,2}([.,\\uFF0C\\uFF0E]?[0-9]{3})*))[^0-9,.\\uFF0C\\uFF0E]+([0-9]{1,2})[^0-9,.\\uFF0C\\uFF0E]*$')
numUnitDecimalInPattern = re.compile('^(([0-9]{1,2}[, \\xA0])?([0-9]{2}[, \\xA0])*[0-9]{3})([^0-9]+)([0-9]{1,2})([^0-9]*)$|^([0-9]+)([^0-9]+)([0-9]{1,2})([^0-9]*)$')
numCommaPattern = re.compile('^\\s*[0-9]+(,[0-9]+)?\\s*$')
numCommaDotPattern = re.compile('^\\s*[0-9]{1,3}(,[0-9]{3,3})*([.][0-9]+)?\\s*$')
numDashPattern = re.compile('^\\s*-\\s*$')
numDotCommaPattern = re.compile('^\\s*[0-9]{1,3}([.][0-9]{3,3})*(,[0-9]+)?\\s*$')
numSpaceDotPattern = re.compile('^\\s*[0-9]{1,3}([ \\xA0][0-9]{3,3})*([.][0-9]+)?\\s*$')
numSpaceCommaPattern = re.compile('^\\s*[0-9]{1,3}([ \\xA0][0-9]{3,3})*(,[0-9]+)?\\s*$')
monthnumber = {'January':1, 
 'February':2,  'March':3,  'April':4,  'May':5,  'June':6,  'July':7, 
 'August':8,  'September':9,  'October':10,  'November':11,  'December':12,  'Jan':1, 
 'Feb':2,  'Mar':3,  'Apr':4,  'May':5,  'Jun':6,  'Jul':7, 
 'Aug':8,  'Sep':9,  'Oct':10,  'Nov':11,  'Dec':12,  'JAN':1, 
 'FEB':2,  'MAR':3,  'APR':4,  'MAY':5,  'JUN':6,  'JUL':7, 
 'AUG':8,  'SEP':9,  'OCT':10,  'NOV':11,  'DEC':12,  'JANUARY':1, 
 'FEBRUARY':2,  'MARCH':3,  'APRIL':4,  'MAY':5,  'JUNE':6,  'JULY':7, 
 'AUGUST':8,  'SEPTEMBER':9,  'OCTOBER':10,  'NOVEMBER':11,  'DECEMBER':12,  'jan':1, 
 'feb':2,  'mar':3,  'apr':4,  'maj':5,  'jun':6,  'jul':7, 
 'aug':8,  'sep':9,  'okt':10,  'nov':11,  'dec':12}
maxDayInMo = {'01':'30', 
 '02':'29',  '03':'31',  '04':'30',  '05':'31',  '06':'30',  '07':'31', 
 '08':'31',  '09':'30',  '10':'31',  '11':'30',  '12':'31',  1:'30', 
 2:'29',  3:'31',  4:'30',  5:'31',  6:'30',  7:'31', 
 8:'31',  9:'30',  10:'31',  11:'30',  12:'31'}
gLastMoDay = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
gregorianHindiMonthNumber = {'जनवरी':'01', 
 'फरवरी':'02', 
 'मार्च':'03', 
 'अप्रैल':'04', 
 'मई':'05', 
 'जून':'06', 
 'जुलाई':'07', 
 'अगस्त':'08', 
 'सितंबर':'09', 
 'अक्तूबर':'10', 
 'नवम्बर':'11', 
 'दिसम्बर':'12'}
sakaMonthNumber = {'Chaitra':1, 
 'चैत्र':1,  'Vaisakha':2, 
 'Vaishakh':2,  'Vaiśākha':2,  'वैशाख':2,  'बैसाख':2,  'Jyaishta':3, 
 'Jyaishtha':3,  'Jyaistha':3,  'Jyeṣṭha':3,  'ज्येष्ठ':3,  'Asadha':4, 
 'Ashadha':4,  'Āṣāḍha':4,  'आषाढ':4,  'आषाढ़':4,  'Sravana':5, 
 'Shravana':5,  'Śrāvaṇa':5,  'श्रावण':5,  'सावन':5,  'Bhadra':6, 
 'Bhadrapad':6,  'Bhādrapada':6,  'Bhādra':6,  'Proṣṭhapada':6,  'भाद्रपद':6,  'भादो':6,  'Aswina':7, 
 'Ashwin':7,  'Asvina':7,  'Āśvina':7,  'आश्विन':7,  'Kartiak':8, 
 'Kartik':8,  'Kartika':8,  'Kārtika':8,  'कार्तिक':8,  'Agrahayana':9, 
 'Agrahāyaṇa':9,  'Margashirsha':9,  'Mārgaśīrṣa':9,  'मार्गशीर्ष':9,  'अगहन':9,  'Pausa':10, 
 'Pausha':10,  'Pauṣa':10,  'पौष':10,  'Magha':11, 
 'Magh':11,  'Māgha':11,  'माघ':11,  'Phalguna':12, 
 'Phalgun':12,  'Phālguna':12,  'फाल्गुन':12}
sakaMonthPattern = re.compile('(C\\S*ait|\\u091A\\u0948\\u0924\\u094D\\u0930)|(Vai|\\u0935\\u0948\\u0936\\u093E\\u0916|\\u092C\\u0948\\u0938\\u093E\\u0916)|(Jy|\\u091C\\u094D\\u092F\\u0947\\u0937\\u094D\\u0920)|(dha|\\u1E0Dha|\\u0906\\u0937\\u093E\\u0922|\\u0906\\u0937\\u093E\\u0922\\u093C)|(vana|\\u015Ar\\u0101va\\u1E47a|\\u0936\\u094D\\u0930\\u093E\\u0935\\u0923|\\u0938\\u093E\\u0935\\u0928)|(Bh\\S+dra|Pro\\u1E63\\u1E6Dhapada|\\u092D\\u093E\\u0926\\u094D\\u0930\\u092A\\u0926|\\u092D\\u093E\\u0926\\u094B)|(in|\\u0906\\u0936\\u094D\\u0935\\u093F\\u0928)|(K\\S+rti|\\u0915\\u093E\\u0930\\u094D\\u0924\\u093F\\u0915)|(M\\S+rga|Agra|\\u092E\\u093E\\u0930\\u094D\\u0917\\u0936\\u0940\\u0930\\u094D\\u0937|\\u0905\\u0917\\u0939\\u0928)|(Pau|\\u092A\\u094C\\u0937)|(M\\S+gh|\\u092E\\u093E\\u0918)|(Ph\\S+lg|\\u092B\\u093E\\u0932\\u094D\\u0917\\u0941\\u0928)')
sakaMonthLength = (30, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 30)
sakaMonthOffset = ((3, 22, 0), (4, 21, 0), (5, 22, 0), (6, 22, 0), (7, 23, 0), (8, 23, 0),
                   (9, 23, 0), (10, 23, 0), (11, 22, 0), (12, 22, 0), (1, 21, 1),
                   (2, 20, 1))

def checkDate(y, m, d):
    try:
        datetime(_INT(y), _INT(m), _INT(d))
        return True
    except ValueError:
        return False


def z2(arg):
    if len(arg) == 1:
        return '0' + arg
    else:
        return arg


def yr(arg):
    if len(arg) == 1:
        return '200' + arg
    else:
        if len(arg) == 2:
            return '20' + arg
        return arg


def yrin(arg, _mo, _day):
    if len(arg) == 2:
        if arg > '21' or arg == '21' and _mo >= 10 and _day >= 11:
            return '19' + arg
        return '20' + arg
    else:
        return arg


def devanagariDigitsToNormal(devanagariDigits):
    normal = ''
    for d in devanagariDigits:
        if '०' <= d <= '९':
            normal += chr(ord(d) - 2406 + ord('0'))
        else:
            normal += d

    return normal


def jpDigitsToNormal(jpDigits):
    normal = ''
    for d in jpDigits:
        if '０' <= d <= '９':
            normal += chr(ord(d) - 65296 + ord('0'))
        else:
            normal += d

    return normal


def sakaToGregorian(sYr, sMo, sDay):
    gYr = sYr + 78
    sStartsInLeapYr = gYr % 4 == 0 and (not gYr % 100 == 0 or gYr % 400 == 0)
    if gYr < 0:
        raise ValueError(_('Saka calendar year not supported: {0} {1} {2} '), sYr, sMo, sDay)
    if sMo < 1 or sMo > 12:
        raise ValueError(_('Saka calendar month error: {0} {1} {2} '), sYr, sMo, sDay)
    sMoLength = sakaMonthLength[(sMo - 1)]
    if sStartsInLeapYr:
        if sMo == 1:
            sMoLength += 1
    if sDay < 1 or sDay > sMoLength:
        raise ValueError(_('Saka calendar day error: {0} {1} {2} '), sYr, sMo, sDay)
    gMo, gDayOffset, gYrOffset = sakaMonthOffset[(sMo - 1)]
    if sStartsInLeapYr:
        if sMo == 1:
            gDayOffset -= 1
    gYr += gYrOffset
    gMoLength = gLastMoDay[(gMo - 1)]
    if gMo == 2:
        if gYr % 4 == 0:
            if not gYr % 100 == 0 or gYr % 400 == 0:
                gMoLength += 1
    gDay = gDayOffset + sDay - 1
    if gDay > gMoLength:
        gDay -= gMoLength
        gMo += 1
        if gMo == 13:
            gMo = 1
            gYr += 1
    return (
     gYr, gMo, gDay)


eraStart = {'平成':1988, 
 '平':1988, 
 '明治':1867, 
 '明':1867, 
 '大正':1911, 
 '大':1911, 
 '昭和':1925, 
 '昭':1925}

def eraYear(era, yr):
    return eraStart[era] + (1 if yr == '元' else _INT(yr))


def booleanfalse(arg):
    return 'false'


def booleantrue(arg):
    return 'true'


def dateslashus(arg):
    m = dateslashPattern.match(arg)
    if m:
        if m.lastindex == 3:
            return '{0}-{1}-{2}'.format(yr(m.group(3)), z2(m.group(1)), z2(m.group(2)))
    raise XPathContext.FunctionArgType(1, 'xs:date')


def dateslasheu(arg):
    m = dateslashPattern.match(arg)
    if m:
        if m.lastindex == 3:
            return '{0}-{1}-{2}'.format(yr(m.group(3)), z2(m.group(2)), z2(m.group(1)))
    raise XPathContext.FunctionArgType(1, 'xs:date')


def datedotus(arg):
    m = datedotPattern.match(arg)
    if m:
        if m.lastindex == 3:
            return '{0}-{1}-{2}'.format(yr(m.group(3)), z2(m.group(1)), z2(m.group(2)))
    raise XPathContext.FunctionArgType(1, 'xs:date')


def datedoteu(arg):
    m = datedotPattern.match(arg)
    if m:
        if m.lastindex == 3:
            return '{0}-{1}-{2}'.format(yr(m.group(3)), z2(m.group(2)), z2(m.group(1)))
    raise XPathContext.FunctionArgType(1, 'xs:date')


def datelongusTR1(arg):
    m = dateLongUsTR1Pattern.match(arg)
    if m:
        if m.lastindex == 3:
            return '{0}-{1:02}-{2}'.format(yr(m.group(3)), monthnumber[m.group(1)], z2(m.group(2)))
    raise XPathContext.FunctionArgType(1, 'xs:date')


def dateshortusTR1(arg):
    m = dateShortUsTR1Pattern.match(arg)
    if m:
        if m.lastindex == 3:
            return '{0}-{1:02}-{2}'.format(yr(m.group(3)), monthnumber[m.group(1)], z2(m.group(2)))
    raise XPathContext.FunctionArgType(1, 'xs:date')


def datelongukTR1(arg):
    m = dateLongUkTR1Pattern.match(arg)
    if m:
        if m.lastindex == 3:
            return '{0}-{1:02}-{2}'.format(yr(m.group(3)), monthnumber[m.group(2)], z2(m.group(1)))
    raise XPathContext.FunctionArgType(1, 'xs:date')


def dateshortukTR1(arg):
    m = dateShortUkTR1Pattern.match(arg)
    if m:
        if m.lastindex == 3:
            return '{0}-{1:02}-{2}'.format(yr(m.group(3)), monthnumber[m.group(2)], z2(m.group(1)))
    raise XPathContext.FunctionArgType(1, 'xs:date')


def datelongeu(arg):
    m = dateEuPattern.match(arg)
    if m:
        if m.lastindex == 3:
            return '{0}-{1:02}-{2}'.format(yr(m.group(3)), monthnumber[m.group(2)], z2(m.group(1)))
    raise XPathContext.FunctionArgType(1, 'xs:date')


def datedaymonth(arg):
    m = daymonthPattern.match(arg)
    if m:
        if m.lastindex == 2:
            mo = z2(m.group(2))
            day = z2(m.group(1))
            if '01' <= day <= maxDayInMo.get(mo, '00'):
                return '--{0}-{1}'.format(mo, day)
    raise XPathContext.FunctionArgType(1, 'xs:gMonthDay')


def datemonthday(arg):
    m = monthdayPattern.match(arg)
    if m:
        if m.lastindex == 2:
            mo = z2(m.group(1))
            day = z2(m.group(2))
            if '01' <= day <= maxDayInMo.get(mo, '00'):
                return '--{0}-{1}'.format(mo, day)
    raise XPathContext.FunctionArgType(1, 'xs:gMonthDay')


def datedaymonthSlashTR1(arg):
    m = daymonthslashPattern.match(arg)
    if m:
        if m.lastindex == 2:
            mo = z2(m.group(2))
            day = z2(m.group(1))
            return '--{0}-{1}'.format(mo, day)
    raise XPathContext.FunctionArgType(1, 'xs:gMonthDay')


def datemonthdaySlashTR1(arg):
    m = monthdayslashPattern.match(arg)
    if m:
        if m.lastindex == 2:
            mo = z2(m.group(1))
            day = z2(m.group(2))
            return '--{0}-{1}'.format(mo, day)
    raise XPathContext.FunctionArgType(1, 'xs:gMonthDay')


def datedaymonthdk(arg):
    m = daymonthDkPattern.match(arg)
    if m:
        if m.lastindex == 4:
            day = z2(m.group(1))
            mon3 = m.group(2).lower()
            mon3 = m.group(2).lower()
            monEnd = m.group(3)
            monPer = m.group(4)
            if mon3 in monthnumber:
                mo = monthnumber[mon3]
                if not monEnd and not monPer or not monEnd and monPer or monEnd and not monPer:
                    if '01' <= day <= maxDayInMo.get(mo, '00'):
                        return '--{0:02}-{1}'.format(mo, day)
    raise XPathContext.FunctionArgType(1, 'xs:gMonthDay')


def datedaymonthen(arg):
    m = daymonthEnPattern.match(arg)
    if m:
        if m.lastindex == 2:
            _mo = monthnumber[m.group(2)]
            _day = z2(m.group(1))
            if '01' <= _day <= maxDayInMo.get(_mo, '00'):
                return '--{0:02}-{1}'.format(_mo, _day)
    raise XPathContext.FunctionArgType(1, 'xs:gMonthDay')


def datedaymonthShortEnTR1(arg):
    m = daymonthShortEnTR1Pattern.match(arg)
    if m:
        if m.lastindex == 2:
            _mo = monthnumber[m.group(2)]
            _day = z2(m.group(1))
            return '--{0:02}-{1}'.format(_mo, _day)
    raise XPathContext.FunctionArgType(1, 'xs:gMonthDay')


def datedaymonthLongEnTR1(arg):
    m = daymonthLongEnTR1Pattern.match(arg)
    if m:
        if m.lastindex == 2:
            _mo = monthnumber[m.group(2)]
            _day = z2(m.group(1))
            return '--{0:02}-{1}'.format(_mo, _day)
    raise XPathContext.FunctionArgType(1, 'xs:gMonthDay')


def datemonthdayen(arg):
    m = monthdayEnPattern.match(arg)
    if m:
        if m.lastindex == 2:
            _mo = monthnumber[m.group(1)]
            _day = z2(m.group(2))
            if '01' <= _day <= maxDayInMo.get(_mo, '00'):
                return '--{0:02}-{1}'.format(_mo, _day)
    raise XPathContext.FunctionArgType(1, 'xs:gMonthDay')


def datemonthdayLongEnTR1(arg):
    m = monthdayLongEnTR1Pattern.match(arg)
    if m:
        if m.lastindex == 2:
            _mo = monthnumber[m.group(1)]
            _day = z2(m.group(2))
            return '--{0:02}-{1}'.format(_mo, _day)
    raise XPathContext.FunctionArgType(1, 'xs:gMonthDay')


def datemonthdayShortEnTR1(arg):
    m = monthdayShortEnTR1Pattern.match(arg)
    if m:
        if m.lastindex == 2:
            _mo = monthnumber[m.group(1)]
            _day = z2(m.group(2))
            return '--{0:02}-{1}'.format(_mo, _day)
    raise XPathContext.FunctionArgType(1, 'xs:gMonthDay')


def datedaymonthyear(arg):
    m = daymonthyearPattern.match(arg)
    if m:
        if m.lastindex == 3:
            if checkDate(yr(m.group(3)), m.group(2), m.group(1)):
                return '{0}-{1}-{2}'.format(yr(m.group(3)), z2(m.group(2)), z2(m.group(1)))
    raise XPathContext.FunctionArgType(1, 'xs:date')


def datemonthdayyear(arg):
    m = monthdayyearPattern.match(arg)
    if m:
        if m.lastindex == 3:
            _yr = yr(m.group(3))
            _mo = z2(m.group(1))
            _day = z2(m.group(2))
            if checkDate(_yr, _mo, _day):
                return '{0}-{1}-{2}'.format(_yr, _mo, _day)
    raise XPathContext.FunctionArgType(1, 'xs:date')


def datemonthyear(arg):
    m = monthyearPattern.match(arg)
    if m:
        if m.lastindex == 2:
            _mo = z2(m.group(1))
            if '01' <= _mo <= '12':
                return '{0}-{1:2}'.format(yr(m.group(2)), _mo)
    raise XPathContext.FunctionArgType(1, 'xs:gYearMonth')


def datemonthyeardk(arg):
    m = monthyearDkPattern.match(arg)
    if m:
        if m.lastindex == 4:
            mon3 = m.group(1).lower()
            monEnd = m.group(2)
            monPer = m.group(3)
            if mon3 in monthnumber:
                if not monEnd and not monPer or not monEnd and monPer or monEnd and not monPer:
                    return '{0}-{1:02}'.format(yr(m.group(4)), monthnumber[mon3])
    raise XPathContext.FunctionArgType(1, 'xs:gYearMonth')


def datemonthyearen(arg):
    m = monthyearEnPattern.match(arg)
    if m:
        if m.lastindex == 2:
            return '{0}-{1:02}'.format(yr(m.group(2)), monthnumber[m.group(1)])
    raise XPathContext.FunctionArgType(1, 'xs:gYearMonth')


def datemonthyearShortEnTR1(arg):
    m = monthyearShortEnTR1Pattern.match(arg)
    if m:
        if m.lastindex == 2:
            return '{0}-{1:02}'.format(yr(m.group(2)), monthnumber[m.group(1)])
    raise XPathContext.FunctionArgType(1, 'xs:gYearMonth')


def datemonthyearLongEnTR1(arg):
    m = monthyearLongEnTR1Pattern.match(arg)
    if m:
        if m.lastindex == 2:
            return '{0}-{1:02}'.format(yr(m.group(2)), monthnumber[m.group(1)])
    raise XPathContext.FunctionArgType(1, 'xs:gYearMonth')


def datemonthyearin(arg):
    m = monthyearInPattern.match(arg)
    try:
        return '{0}-{1}'.format(yr(devanagariDigitsToNormal(m.group(2))), gregorianHindiMonthNumber[m.group(1)])
    except (AttributeError, IndexError, KeyError):
        pass

    raise XPathContext.FunctionArgType(1, 'xs:gYearMonth')


def dateyearmonthen(arg):
    m = yearmonthEnPattern.match(arg)
    if m:
        if m.lastindex == 2:
            return '{0}-{1:02}'.format(yr(m.group(1)), monthnumber[m.group(2)])
    raise XPathContext.FunctionArgType(1, 'xs:gYearMonth')


def dateyearmonthShortEnTR1(arg):
    m = yearmonthShortEnTR1Pattern.match(arg)
    if m:
        if m.lastindex == 2:
            return '{0}-{1:02}'.format(yr(m.group(1)), monthnumber[m.group(2)])
    raise XPathContext.FunctionArgType(1, 'xs:gYearMonth')


def dateyearmonthLongEnTR1(arg):
    m = yearmonthLongEnTR1Pattern.match(arg)
    if m:
        if m.lastindex == 2:
            return '{0}-{1:02}'.format(yr(m.group(1)), monthnumber[m.group(2)])
    raise XPathContext.FunctionArgType(1, 'xs:gYearMonth')


def datedaymonthyeardk(arg):
    m = daymonthyearDkPattern.match(arg)
    if m:
        if m.lastindex == 5:
            _yr = yr(m.group(5))
            _day = z2(m.group(1))
            _mon3 = m.group(2).lower()
            _monEnd = m.group(3)
            _monPer = m.group(4)
            if _mon3 in monthnumber:
                if not _monEnd and not _monPer or not _monEnd and _monPer or _monEnd and not _monPer:
                    _mo = monthnumber[_mon3]
                    if checkDate(_yr, _mo, _day):
                        return '{0}-{1:02}-{2}'.format(_yr, _mo, _day)
    raise XPathContext.FunctionArgType(1, 'xs:date')


def datedaymonthyearen(arg):
    m = daymonthyearEnPattern.match(arg)
    if m:
        if m.lastindex == 3:
            _yr = yr(m.group(3))
            _mo = monthnumber[m.group(2)]
            _day = z2(m.group(1))
            if checkDate(_yr, _mo, _day):
                return '{0}-{1:02}-{2}'.format(_yr, _mo, _day)
    raise XPathContext.FunctionArgType(1, 'xs:date')


def datedaymonthyearin(arg):
    m = daymonthyearInPattern.match(arg)
    try:
        _yr = yr(devanagariDigitsToNormal(m.group(3)))
        _mo = gregorianHindiMonthNumber.get(m.group(2), devanagariDigitsToNormal(m.group(2)))
        _day = z2(devanagariDigitsToNormal(m.group(1)))
        if checkDate(_yr, _mo, _day):
            return '{0}-{1}-{2}'.format(_yr, _mo, _day)
    except (AttributeError, IndexError, KeyError):
        pass

    raise XPathContext.FunctionArgType(1, 'xs:date')


def calindaymonthyear(arg):
    m = daymonthyearInPattern.match(arg)
    try:
        _mo = sakaMonthPattern.search(m.group(2)).lastindex
        _day = _INT(devanagariDigitsToNormal(m.group(1)))
        _yr = _INT(devanagariDigitsToNormal(yrin(m.group(3), _mo, _day)))
        gregorianDate = sakaToGregorian(_yr, _mo, _day)
        return '{0}-{1:02}-{2:02}'.format(gregorianDate[0], gregorianDate[1], gregorianDate[2])
    except (AttributeError, IndexError, KeyError, ValueError):
        pass

    raise XPathContext.FunctionArgType(1, 'xs:date')


def datemonthdayyearen(arg):
    m = monthdayyearEnPattern.match(arg)
    if m:
        if m.lastindex == 3:
            _yr = yr(m.group(3))
            _mo = monthnumber[m.group(1)]
            _day = z2(m.group(2))
            if checkDate(_yr, _mo, _day):
                return '{0}-{1:02}-{2}'.format(_yr, _mo, _day)
    raise XPathContext.FunctionArgType(1, 'xs:date')


def dateerayearmonthdayjp(arg):
    m = erayearmonthdayjpPattern.match(jpDigitsToNormal(arg))
    if m:
        if m.lastindex == 4:
            _yr = eraYear(m.group(1), m.group(2))
            _mo = z2(m.group(3))
            _day = z2(m.group(4))
            if checkDate(_yr, _mo, _day):
                return '{0}-{1}-{2}'.format(_yr, _mo, _day)
    raise XPathContext.FunctionArgType(1, 'xs:date')


def dateyearmonthday(arg):
    m = yearmonthdayPattern.match(jpDigitsToNormal(arg))
    if m:
        if m.lastindex == 3:
            _yr = yr(m.group(1))
            _mo = z2(m.group(2))
            _day = z2(m.group(3))
            if checkDate(_yr, _mo, _day):
                return '{0}-{1}-{2}'.format(_yr, _mo, _day)
    raise XPathContext.FunctionArgType(1, 'xs:date')


def dateerayearmonthjp(arg):
    m = erayearmonthjpPattern.match(jpDigitsToNormal(arg))
    if m:
        if m.lastindex == 3:
            _yr = eraYear(m.group(1), m.group(2))
            _mo = z2(m.group(3))
            if '01' <= _mo <= '12':
                return '{0}-{1}'.format(_yr, _mo)
    raise XPathContext.FunctionArgType(1, 'xs:gYearMonth')


def dateyearmonthdaycjk(arg):
    m = yearmonthdaycjkPattern.match(jpDigitsToNormal(arg))
    if m:
        if m.lastindex == 3:
            _yr = yr(m.group(1))
            _mo = z2(m.group(2))
            _day = z2(m.group(3))
            if checkDate(_yr, _mo, _day):
                return '{0}-{1}-{2}'.format(_yr, _mo, _day)
    raise XPathContext.FunctionArgType(1, 'xs:date')


def dateyearmonthcjk(arg):
    m = yearmonthcjkPattern.match(jpDigitsToNormal(arg))
    if m:
        if m.lastindex == 2:
            _mo = z2(m.group(2))
            if '01' <= _mo <= '12':
                return '{0}-{1}'.format(yr(m.group(1)), _mo)
    raise XPathContext.FunctionArgType(1, 'xs:date')


def nocontent(arg):
    return ''


def numcommadecimal(arg):
    if numCommaDecimalPattern.match(arg):
        return arg.replace('.', '').replace(',', '.').replace(' ', '').replace('\xa0', '')
    raise XPathContext.FunctionArgType(1, 'ixt:nonNegativeDecimalType')


def numcommadot(arg):
    if numCommaDotPattern.match(arg):
        return arg.replace(',', '')
    raise XPathContext.FunctionArgType(1, 'ixt:numcommadot')


def numdash(arg):
    if numDashPattern.match(arg):
        return arg.replace('-', '0')
    raise XPathContext.FunctionArgType(1, 'ixt:numdash')


def numspacedot(arg):
    if numSpaceDotPattern.match(arg):
        return arg.replace(' ', '').replace('\xa0', '')
    raise XPathContext.FunctionArgType(1, 'ixt:numspacedot')


def numcomma(arg):
    if numCommaPattern.match(arg):
        return arg.replace(',', '.')
    raise XPathContext.FunctionArgType(1, 'ixt:numcomma')


def numdotcomma(arg):
    if numDotCommaPattern.match(arg):
        return arg.replace('.', '').replace(',', '.')
    raise XPathContext.FunctionArgType(1, 'ixt:numdotcomma')


def numspacecomma(arg):
    if numSpaceCommaPattern.match(arg):
        return arg.replace(' ', '').replace('\xa0', '').replace(',', '.')
    raise XPathContext.FunctionArgType(1, 'ixt:numspacecomma')


def zerodash(arg):
    if zeroDashPattern.match(arg):
        return '0'
    raise XPathContext.FunctionArgType(1, 'ixt:zerodashType')


def numdotdecimal(arg):
    if numDotDecimalPattern.match(arg):
        return arg.replace(',', '').replace(' ', '').replace('\xa0', '')
    raise XPathContext.FunctionArgType(1, 'ixt:numdotdecimalType')


def numdotdecimalin(arg):
    m = numDotDecimalInPattern.match(arg)
    if m:
        m2 = [g for g in m.groups() if g is not None]
        if m2[(-1)].startswith('.'):
            fract = m2[(-1)]
        else:
            fract = ''
        return m2[0].replace(',', '').replace(' ', '').replace('\xa0', '') + fract
    raise XPathContext.FunctionArgType(1, 'ixt:numdotdecimalinType')


def numunitdecimal(arg):
    m = numUnitDecimalPattern.match(jpDigitsToNormal(arg))
    if m:
        if m.lastindex > 1:
            return m.group(1).replace('.', '').replace(',', '').replace('，', '').replace('．', '') + '.' + z2(m.group(m.lastindex))
    raise XPathContext.FunctionArgType(1, 'ixt:nonNegativeDecimalType')


def numunitdecimalin(arg):
    m = numUnitDecimalInPattern.match(arg)
    if m:
        m2 = [g for g in m.groups() if g is not None]
        return m2[0].replace(',', '').replace(' ', '').replace('\xa0', '') + '.' + z2(m2[(-2)])
    raise XPathContext.FunctionArgType(1, 'ixt:numunitdecimalinType')


tr1Functions = {'dateslashus':dateslashus, 
 'dateslasheu':dateslasheu, 
 'datedotus':datedotus, 
 'datedoteu':datedoteu, 
 'datelongus':datelongusTR1, 
 'dateshortus':dateshortusTR1, 
 'datelonguk':datelongukTR1, 
 'dateshortuk':dateshortukTR1, 
 'numcommadot':numcommadot, 
 'numdash':numdash, 
 'numspacedot':numspacedot, 
 'numdotcomma':numdotcomma, 
 'numcomma':numcomma, 
 'numspacecomma':numspacecomma, 
 'datelongdaymonthuk':datedaymonthLongEnTR1, 
 'dateshortdaymonthuk':datedaymonthShortEnTR1, 
 'datelongmonthdayus':datemonthdayLongEnTR1, 
 'dateshortmonthdayus':datemonthdayShortEnTR1, 
 'dateslashdaymontheu':datedaymonthSlashTR1, 
 'dateslashmonthdayus':datemonthdaySlashTR1, 
 'datelongyearmonth':dateyearmonthLongEnTR1, 
 'dateshortyearmonth':dateyearmonthShortEnTR1, 
 'datelongmonthyear':datemonthyearLongEnTR1, 
 'dateshortmonthyear':datemonthyearShortEnTR1}
tr2Functions = {'booleanfalse':booleanfalse, 
 'booleantrue':booleantrue, 
 'datedaymonth':datedaymonth, 
 'datedaymonthen':datedaymonthen, 
 'datedaymonthyear':datedaymonthyear, 
 'datedaymonthyearen':datedaymonthyearen, 
 'dateerayearmonthdayjp':dateerayearmonthdayjp, 
 'dateerayearmonthjp':dateerayearmonthjp, 
 'datemonthday':datemonthday, 
 'datemonthdayen':datemonthdayen, 
 'datemonthdayyear':datemonthdayyear, 
 'datemonthdayyearen':datemonthdayyearen, 
 'datemonthyearen':datemonthyearen, 
 'dateyearmonthdaycjk':dateyearmonthdaycjk, 
 'dateyearmonthen':dateyearmonthen, 
 'dateyearmonthcjk':dateyearmonthcjk, 
 'nocontent':nocontent, 
 'numcommadecimal':numcommadecimal, 
 'zerodash':zerodash, 
 'numdotdecimal':numdotdecimal, 
 'numunitdecimal':numunitdecimal}
tr3Functions = tr2Functions
tr3Functions.update({'calindaymonthyear':calindaymonthyear, 
 'datedaymonthdk':datedaymonthdk, 
 'datedaymonthyeardk':datedaymonthyeardk, 
 'datedaymonthyearin':datedaymonthyearin, 
 'datemonthyear':datemonthyear, 
 'datemonthyeardk':datemonthyeardk, 
 'datemonthyearin':datemonthyearin, 
 'dateyearmonthday':dateyearmonthday, 
 'numdotdecimalin':numdotdecimalin, 
 'numunitdecimalin':numunitdecimalin})
deprecatedNamespaceURI = 'http://www.xbrl.org/2008/inlineXBRL/transformation'
ixtNamespaceFunctions = {'http://www.xbrl.org/inlineXBRL/transformation/2010-04-20':tr1Functions, 
 'http://www.xbrl.org/inlineXBRL/transformation/2011-07-31':tr2Functions, 
 'http://www.xbrl.org/inlineXBRL/transformation/2015-02-26':tr3Functions, 
 'http://www.xbrl.org/2008/inlineXBRL/transformation':tr1Functions}