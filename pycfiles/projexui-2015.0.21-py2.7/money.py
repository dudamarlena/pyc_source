# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/projex/money.py
# Compiled at: 2016-07-03 23:28:12
__doc__ = ' Module for managing money information. '
import locale, re, urllib2
from .text import nativestring as nstr
_expr = re.compile('^(?P<symbol>[^\\w\\d-])?(?P<amount>[-\\d,]+\\.?\\d*)\\s*(?P<currency>.*)$')
_inited = False
DEFAULT = locale.getdefaultlocale()[0].split('_')[(-1)].lower()
SYMBOLS = {'USD': '$', 
   'PND': b'\xa3', 
   'JPY': b'\xa5'}
CURRENCIES = {'au': ('Australia', 'AUD'), 
   'gb': ('Great Britain', 'PND'), 
   'eu': ('European Union', 'EUR'), 
   'jp': ('Japan', 'JPY'), 
   'us': ('United States', 'USD')}

def currencies():
    """
    Returns a dictionary of currencies from the world.
    
    :return     {<str> geoname: (<str> country, <str> code), ..}
    """
    global CURRENCIES
    init()
    return CURRENCIES.copy()


def fromString(money):
    """
    Returns the amount of money based on the inputted string.
    
    :param      money   | <str>
    
    :return     (<double> amount, <str> currency)
    """
    result = _expr.match(money)
    if not result:
        return (0, DEFAULT)
    data = result.groupdict()
    amount = float(data['amount'].replace(',', ''))
    if data['currency']:
        return (amount, data['currency'])
    symbol = data['symbol']
    for key, value in SYMBOLS.items():
        if symbol == value:
            return (amount, key)

    return (amount, DEFAULT)


def init():
    """
    Initializes the currency list from the internet.
    
    :sa     lookup
    
    :return     <bool> | success
    """
    global _inited
    if _inited:
        return
    codes = lookup()
    if codes:
        _inited = True
        CURRENCIES.update(codes)
        return True
    return False


def lookup():
    """
    Initializes the global list of currencies from the internet
    
    :return     {<str> geoname: (<str> country, <str> symbol), ..}
    """
    url = 'http://download.geonames.org/export/dump/countryInfo.txt'
    try:
        data = urllib2.urlopen(url)
    except StandardError:
        return {}

    ccodes = {}
    for line in data.read().split('\n'):
        if line.startswith('#'):
            continue
        line = line.split('\t')
        try:
            geoname = line[0].lower()
            code = line[10]
            country = line[4]
        except IndexError:
            continue

        if not code:
            continue
        ccodes[geoname] = (
         country, code)

    return ccodes


def toString(amount, currency=None, rounded=None):
    """
    Converts the inputted amount of money to a string value.
    
    :param      amount         | <bool>
                currency       | <str>
                rounded        | <bool> || None
    
    :return     <str>
    """
    init()
    if currency is None:
        currency = DEFAULT
    if currency in CURRENCIES:
        symbol = SYMBOLS.get(CURRENCIES[currency][1])
    else:
        symbol = SYMBOLS.get(currency, '')
    astr = nstr(int(abs(amount)))
    alen = len(astr)
    if len(astr) > 3:
        arange = range(alen, -1, -3)
        parts = reversed([ astr[i - 3:i] for i in arange ])
        astr = astr[:alen % 3] + (',').join(parts)
        astr = astr.strip(',')
    if amount < 0:
        astr = '-' + astr
    if (amount % 1 or rounded is False) and rounded is True:
        astr += ('%0.2f' % (amount % 1)).lstrip('0')
    if not symbol:
        return astr + ' ' + CURRENCIES.get(currency, ('', ''))[1]
    else:
        return symbol + astr


def symbol(currency):
    """
    Returns the monetary symbol used for the given currency.
    
    :param      currency | <str.
    
    :return     <str>
    """
    init()
    if currency in CURRENCIES:
        return SYMBOLS.get(CURRENCIES[currency][1], '')
    return SYMBOLS.get(currency, '')