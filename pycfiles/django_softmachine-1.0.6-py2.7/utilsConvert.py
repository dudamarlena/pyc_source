# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/protoLib/utilsConvert.py
# Compiled at: 2014-05-29 10:16:48
import datetime, time
from decimal import Decimal
from django.utils.encoding import smart_str

def getTypedValue(sAux, sType):
    """ Retorna valores tipados segun el tipo definido 
    * se usa sobre todo para las UDP y los JsonField 
    """
    if sAux == 'None':
        sAux = ''
    sAux = smart_str(sAux)
    if sType == 'bool':
        sAux = toBoolean(sAux)
    elif sType in ('int', 'autofield', 'foreignid'):
        sAux = toInteger(sAux)
    elif sType == 'decimal':
        sAux = toDecimal(sAux)
    elif sType == 'date':
        sAux = toDate(sAux)
    elif sType == 'datetime':
        sAux = toDateTime(sAux)
    elif sType == 'time':
        sAux = toTime(sAux)
    elif sType == 'foreigntext':
        if sAux == 'None':
            sAux = ''
    return sAux


def isNumeric(s):
    try:
        i = float(s)
    except ValueError as TypeError:
        return False

    return True


def toInteger(s, iDefault=None):
    """
    Conversion a entero,  utilizada antes de cargar la Db 
    """
    try:
        iResult = int(s)
        return iResult
    except:
        return iDefault


def toFloat(s, iDefault=None):
    """
    Conversion a float,  utilizada antes de cargar la Db 
    """
    try:
        iResult = float(s)
        return iResult
    except:
        return iDefault


def toDecimal(s, iDefault=None):
    """
    Conversion a decimal,  utilizada antes de cargar la Db 
    """
    try:
        iResult = Decimal(s)
        return iResult
    except:
        return iDefault


def toBoolean(s):
    """
    Conversion a boolean,  utilizada antes de cargar la Db 
    """
    if type(s).__name__ in ('str', 'unicode'):
        return s.lower()[0] in ('y', 't', 'o', 's', '1')
    else:
        if type(s).__name__ == 'bool':
            return s
        if type(s).__name__ == 'int' and s != 0:
            return True
        return False


def toDate(sVal, iDefault=None):
    sVal = toDateTime(sVal, iDefault)
    if type(sVal).__name__ == 'date':
        return sVal
    else:
        if type(sVal).__name__ == 'datetime':
            return sVal.date()
        return


def toTime(sVal, iDefault=None):
    sVal = toDateTime(sVal, iDefault)
    if type(sVal).__name__ == 'time':
        return sVal
    if type(sVal).__name__ == 'datetime':
        return sVal.time()


def toDateTime(sVal, iDefault=None):
    """ Suponer formato Iso OrderingDate 
    """
    if sVal is None:
        return iDefault
    else:
        try:
            if sVal.count('T') > 0:
                date, time = sVal.split('T')
                an, mois, jour = date.split('-')
                h, m, s = time.split(':')
                return datetime.datetime(int(an), int(mois), int(jour), int(h), int(m), int(s))
            if sVal.count('-') == 2:
                an, mois, jour = sVal.split('-')
                return datetime.date(int(an), int(mois), int(jour))
            if sVal.count('/') == 2:
                if sVal.count(' ') > 0:
                    date, time = sVal.split(' ')
                    jour, mois, an = date.split('/')
                    h, m, s = time.split(':')
                    return datetime.datetime(int(an), int(mois), int(jour), int(h), int(m), int(s))
                else:
                    jour, mois, an = date.split('/')
                    return datetime.date(int(an), int(mois), int(jour))

        except:
            return iDefault

        return


def toDate__(sVal):
    strp_time = time.strptime(sVal, '%m/%d/%Y %H:%M:%S')
    date_django = datetime.datetime.fromtimestamp(time.mktime(strp_time))
    return date_django


def isinteger(astring):
    if not astring:
        return False
    import string
    for char in str(astring):
        if char not in string.digits:
            return False

    return True


def product(*args):
    pools = map(tuple, args)
    result = [[]]
    for pool in pools:
        result = [ x + [y] for x in result for y in pool ]

    return result