# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mempy\ichingbase.py
# Compiled at: 2016-06-17 03:31:41
# Size of source mod 2**32: 8746 bytes
"""
[ichingbase.py] - Mempy Iching System Base module

이 모듈은 주역명리시스템(ex. 입춘/동지날짜와 계산)의 기본이 되는 
기능을 구현한 모듈입니다.

"""
__author__ = 'Herokims'
__ver__ = '160609'
__since__ = '2006-10-01'
__update__ = '2016-06-09'
__copyright__ = 'Copyright (c) TreeInsight.org'
__engine__ = 'Python 3.4.1'
try:
    from . import mytime
except:
    import mytime

class TimeTypeError(Exception):
    pass


GAPJA60 = {'0': 'ao', 
 '1': 'bp',  '2': 'cq',  '3': 'dr',  '4': 'es',  '5': 'ft',  '6': 'gu',  '7': 'hv',  '8': 'iw',  '9': 'jx',  '10': 'ay', 
 '11': 'bz',  '12': 'co',  '13': 'dp',  '14': 'eq',  '15': 'fr',  '16': 'gs',  '17': 'ht',  '18': 'iu',  '19': 'jv',  '20': 'aw', 
 '21': 'bx',  '22': 'cy',  '23': 'dz',  '24': 'eo',  '25': 'fp',  '26': 'gq',  '27': 'hr',  '28': 'is',  '29': 'jt',  '30': 'au', 
 '31': 'bv',  '32': 'cw',  '33': 'dx',  '34': 'ey',  '35': 'fz',  '36': 'go',  '37': 'hp',  '38': 'iq',  '39': 'jr',  '40': 'as', 
 '41': 'bt',  '42': 'cu',  '43': 'dv',  '44': 'ew',  '45': 'fx',  '46': 'gy',  '47': 'hz',  '48': 'io',  '49': 'jp',  '50': 'aq', 
 '51': 'br',  '52': 'cs',  '53': 'dt',  '54': 'eu',  '55': 'fv',  '56': 'gw',  '57': 'hx',  '58': 'iy',  '59': 'jz'}
GAPJA60h = {'0': '甲子', 
 '1': '乙丑',  '2': '丙寅',  '3': '丁卯',  '4': '戊辰',  '5': '己巳',  '6': '庚午',  '7': '辛未',  '8': '壬申',  '9': '癸酉',  '10': '甲戌', 
 '11': '乙亥',  '12': '丙子',  '13': '丁丑',  '14': '戊寅',  '15': '己卯',  '16': '庚辰',  '17': '辛巳',  '18': '壬午',  '19': '癸未',  '20': '甲申', 
 '21': '乙酉',  '22': '丙戌',  '23': '丁亥',  '24': '戊子',  '25': '己丑',  '26': '庚寅',  '27': '辛卯',  '28': '壬辰',  '29': '癸巳',  '30': '甲午', 
 '31': '乙未',  '32': '丙申',  '33': '丁酉',  '34': '戊戌',  '35': '己亥',  '36': '庚子',  '37': '辛丑',  '38': '壬人',  '39': '癸卯',  '40': '甲辰', 
 '41': '乙巳',  '42': '丙午',  '43': '丁未',  '44': '戊申',  '45': '己酉',  '46': '庚戌',  '47': '辛亥',  '48': '壬子',  '49': '癸丑',  '50': '甲寅', 
 '51': '乙卯',  '52': '丙辰',  '53': '丁巳',  '54': '戊午',  '55': '己未',  '56': '庚申',  '57': '辛酉',  '58': '壬戌',  '59': '癸亥'}
JEOLKI_GAP_FROM_IPCHUN = (0, 21355, 42843, 64498, 86335, 108366, 130578, 152958, 175471,
                          198077, 220728, 243370, 265955, 288432, 310767, 332928,
                          354903, 376685, 398290, 419736, 441060, 462295, 483493,
                          504693)
SYMBOL2UNICODE_TABLE = {'~a': '甲', 
 '~b': '乙',  '~c': '丙',  '~d': '丁',  '~e': '戊',  '~f': '己', 
 '~g': '庚',  '~h': '辛',  '~i': '壬',  '~j': '癸',  '_o': '子', 
 '_p': '丑',  '_q': '寅',  '_r': '卯',  '_s': '辰',  '_t': '巳', 
 '_u': '午',  '_v': '未',  '_w': '申',  '_x': '酉',  '_y': '戌', 
 '_z': '亥',  '@a': '蓬', 
 '@b': '任',  '@c': '衝',  '@d': '輔',  '@e': '英',  '@f': '芮', 
 '@g': '柱',  '@h': '心',  '@i': '禽',  '#a': '休', 
 '#b': '生',  '#c': '傷',  '#d': '杜',  '#e': '景', 
 '#f': '死',  '#g': '驚',  '#h': '開',  '$a': '符', 
 '$b': '蛇',  '$c': '陰',  '$d': '合',  '$e': '白', 
 '$f': '玄',  '$g': '地',  '$h': '天',  '?g': '공', 
 '?n': ''}

def get_ipchun_date(year):
    """get_ipchun_date(year) -> tuple
    Return target year ipchun date.
    - 'year' is an integer such as 2007
    - Returned tuple is like (2007, 4, 3, 2, 7). It is solar date.
    """
    tmin = mytime.get_mins_from_timedelta((1996, 2, 4, 22, 8), (year, 8, 1, 12, 0))
    tyear = tmin // 525949
    ipchun_date = mytime.get_date_after_mins(tyear * 525949, (1996, 2, 4, 22, 8))
    return ipchun_date


def get_dongji_date(year):
    """get_dongji_date(year) -> tuple
    Return target year ipchun date.
    - 'year' is an integer such as 2007
    - Returned tuple is like (2007, 4, 3, 2, 7). It is solar date.
    """
    ipchun_date = get_ipchun_date(year)
    dongji_date = mytime.get_date_after_mins(462295, ipchun_date)
    return dongji_date


def get_jeolki_date_list(year):
    """get_jeolki_date_list(year) -> list
    Return target year jeolki date list.
    - 'year' is an integer such as 2007
    - Returned tuple is like ((2007, 2, 4, 2, 7),(2007, 2, 15, 12,19),...,). It is solar date tuple.
    """
    global JEOLKI_GAP_FROM_IPCHUN
    result = []
    ipchun_date = get_ipchun_date(year)
    for gap in JEOLKI_GAP_FROM_IPCHUN:
        result.append(mytime.get_date_after_mins(gap, ipchun_date))

    return result


def get_jeolki_index(otime):
    """get_jeolki_index(otime) -> integer
    Return jeolki index otime belongs to.
    - 'otime' is a tuple like (2007,6,4,11,59). it should be solar date.
    - Returned integer is an index. For example, ipchun is indexed by 0.
    """
    if len(otime) != 5:
        raise TimeTypeError('Invalid input. It should be a tuple like (2007,6,4,11,59).')
        return
    otime_ipchun = get_ipchun_date(otime[0])
    if mytime.isEarlier(otime_ipchun, otime):
        min_from_ipchun = mytime.get_mins_from_timedelta(otime_ipchun, otime)
    else:
        min_from_ipchun = mytime.get_mins_from_timedelta(get_ipchun_date(otime[0] - 1), otime)
    jeolki_index = -1
    for j in JEOLKI_GAP_FROM_IPCHUN:
        if min_from_ipchun >= j:
            jeolki_index += 1
        else:
            break

    return jeolki_index


def get_current_jeolki_index():
    """get_current_jeolki_index() -> integer
    Return current jeolki index.
    - Returned tuple is like ('aa',ab',cd',cb')
    """
    otime = time.localtime()[:5]
    return get_jeolki_index(otime)


def isJeolkiChanging(otime):
    """isJeolkiChanging(otime) -> boolean
    Returns True if a jeolki is changing in otime (before & after 1 hour)
    - 'otime' is a tuple like (2007,6,4,11,59). it should be solar date.
    """
    otime_ipchun = get_ipchun_date(otime[0])
    otime_ji = get_jeolki_index(otime)
    if otime_ji == 23:
        otime_jn = 0
    else:
        otime_jn = otime_ji + 1
    boundary1 = mytime.get_date_after_mins(JEOLKI_GAP_FROM_IPCHUN[otime_ji] + 60, otime_ipchun)
    boundary2 = mytime.get_date_after_mins(JEOLKI_GAP_FROM_IPCHUN[otime_jn] - 60, otime_ipchun)
    if mytime.isEarlier(otime, boundary1) or mytime.isEarlier(boundary2, otime):
        return True
    else:
        return False


def symbol2unicode(symbol=None):
    """symbol2unicode(symbol=None) -> unicode
    Return unicode matching given symbol.
    - 'symbol' is a string like '~a'. It should be 2 strings or 0.
    It's ok 'aa', 'bf' but if too many strings are given, it will return ''.
    If no symbol is given, it will return whole symbol2unicode dictionary.
    - Returned unicode is like u'甲'.
    - Programmed by herokims (2007. 6. 24.)
    """
    global SYMBOL2UNICODE_TABLE
    if symbol:
        gan = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
        ji = ['o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        ganji = [g + j for g in gan for j in ji]
        if symbol in ganji:
            return SYMBOL2UNICODE_TABLE[('~' + symbol[0])] + SYMBOL2UNICODE_TABLE[('_' + symbol[1])]
        try:
            return SYMBOL2UNICODE_TABLE[symbol]
        except:
            return ''

    else:
        return SYMBOL2UNICODE_TABLE


def unicode2symbol(uni=None):
    """unicode2symbol(uni=None) -> string
    Return symbol matching given unicode.
    - 'uni' is a unicode like u'甲'. It should be 1 unicode or 0.
    Any unicode is ok but too many strings'll be igonored. It will return ''.
    If no unicode is given, it will return whole unicode2symbol dictionary.
    - Returned string is like '~a'.
    - Programmed by herokims (2007. 6. 24.)
    """
    uni2sym = dict([(v, k) for k, v in list(SYMBOL2UNICODE_TABLE.items())])
    if uni:
        try:
            return uni2sym[uni]
        except:
            return ''

    else:
        return uni2sym


def runTest():
    print('다음은 동작테스트입니다')
    print('이번년도 입춘은 ' + str(get_ipchun_date(time.localtime()[0])))
    print('이번년도 동지는 ' + str(get_dongji_date(time.localtime()[0])))
    print('이번년도 절기날짜 리스트는 ' + str(get_jeolki_date_list(time.localtime()[0])))


if __name__ == '__main__':
    runTest()