# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/bill/py3/.virtualenvs/pytest/lib/python2.7/site-packages/Csys/Edits.py
# Compiled at: 2011-10-05 15:40:44
import re, string, sys, Csys
from FixedPoint import FixedPoint
__version__ = '1.1'
_Mac_Table = dict([ (name, len(name)) for name in ('MacDonald', 'MacKay', 'Macaque',
                                                   'Macassar', 'Macbeth', 'Macdonald',
                                                   'Macedon', 'Macedonia', 'Machiavelli',
                                                   'Machination', 'Machine', 'Machinelike',
                                                   'Machinery', 'Machismo', 'Mackay',
                                                   'Mackerel', 'Mackey', 'Mackinac',
                                                   'Mackintosh', 'Macmillan', 'Macrame',
                                                   'Macromolecular', 'Macromolecule',
                                                   'Macrophage', 'Macroprocessor',
                                                   'Macroscopic', 'Macrostructure')
                  ])

class Error(Exception):
    """Base class for Csys.Edits exceptions"""

    def __init__(self, msg=''):
        self.message = msg
        Exception.__init__(self, msg)

    def __repr__(self):
        return self.message

    __str__ = __repr__


class BadData(Error):

    def __init__(self, field, msg):
        """Bad Data in field"""
        Error.__init__(self, msg)
        self.field = field
        self.msg = msg


def uplow(str, n=None):
    """Capitalize including handling proper names"""
    _delim = ' \t/.,\';!@#$%^&()-=+[]*?"|'
    while str:
        if _delim.find(str[0]) < 0:
            break
        str = str[1:]

    while str:
        if _delim.find(str[-1:]) < 0:
            break
        str = str[:-1]

    if n is None:
        n = len(str)
    else:
        str = str[:n]
    if not str:
        return str
    else:
        words = str.split()
        wordsOut = []
        for word in words:
            while True:
                if len(word) <= 2 or word in _Mac_Table:
                    break
                word = word[:1].upper() + word[1:]
                if word[:2] == 'De':
                    break
                word = word[:1] + word[1:].lower()
                i = 0
                if word[:3] == 'Mac':
                    i = 3
                else:
                    if word[:2] == 'Mc':
                        i = 2
                    try:
                        if i:
                            word = word[:i] + word[i].upper() + word[i + 1:]
                    except:
                        pass

                break

            wordsOut.append(word)

        return (' ').join(wordsOut)


def phone(phonein):
    """phone(string) -> (area) nnn-nnnn"""
    if phonein:
        phonein = str(phonein).strip()
        phonein = re.sub('[-.()\\s]', '', phonein)
        phonein = phonein[:10]
        phonein = phonein[:-4] + '-' + phonein[-4:]
        if len(phonein) > 8:
            phonein = '(%s) %s' % (phonein[:3], phonein[3:])
    return phonein


alpha2numbs = string.maketrans('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', '2223334445556667777888999922233344455566677778889999')

def telenum(phonein):
    """telenum(phonein) -> all numeric phone number"""
    return phone(phonein.translate(alpha2numbs))


def allup(str):
    return str.upper()


def lower(str):
    return str.lower()


_txt1 = ('One ', 'Two ', 'Three ', 'Four ', 'Five ', 'Six ', 'Seven ', 'Eight ', 'Nine ',
         'Ten ', 'Eleven ', 'Twelve ', 'Thirteen ', 'Fourteen ', 'Fifteen ', 'Sixteen ',
         'Seventeen ', 'Eighteen ', 'Nineteen ', 'Twenty ')
_txt2 = ('Twenty ', 'Thirty ', 'Forty ', 'Fifty ', 'Sixty ', 'Seventy ', 'Eighty ',
         'Ninety ', 'One Hundred ')

def amttext(n=0, buf=''):
    """amttext(n, buf) -> amount as text"""
    if n == 0:
        return buf
    if n <= 20:
        return buf + _txt1[(n - 1)]
    if n <= 100:
        tens = int(n / 10)
        units = int(n % 10)
        buf = buf + _txt2[(tens - 2)]
        return amttext(units, buf)
    if n < 10000:
        hundreds = int(n / 100)
        rem = int(n % 100)
        buf = amttext(hundreds, buf) + 'Hundred '
        return amttext(rem, buf)
    if n < 1000000:
        thousands = long(n / 1000)
        rem = long(n % 1000)
        buf = amttext(thousands, buf) + 'Thousand '
        return amttext(rem, buf)
    if n < 1000000000:
        millions = long(n / 1000000)
        rem = long(n % 1000000)
        buf = amttext(millions, buf) + 'Million '
        return amttext(rem, buf)
    if n < 1000000000000:
        billions = long(n / 1000000000)
        rem = long(n % 1000000000)
        buf = amttext(billions, buf) + 'Billion '
        return amttext(rem, buf)
    return '***TILT***'


def spellamt(amt=0, currency='Dollars'):
    """spellamt(longint, currency) -> spelled out amount"""
    n = long(long(amt) * 100 + 0.5)
    if n <= 0:
        return '**VOID**VOID**VOID**VOID**VOID**VOID**VOID**VOID**'
    dollars = long(n / 100)
    cents = int(n % 100)
    if dollars == 0:
        buf = '***Zero '
    else:
        buf = '***' + amttext(dollars)
    buf = buf + 'and '
    if cents > 0:
        buf = buf + '%02d/100' % cents
    else:
        buf = buf + 'No/100'
    return '%s %s***' % (buf, currency)


def amttxt(amt):
    return spellamt(amt)


_signpat = re.compile('^(-*)(.*)$')

def d2s(str):
    """d2s(str) -> [-]nnn,nnn,nnn.nn"""
    str = '%s' % FixedPoint(str)
    rc, str = str[-3:], str[:-3]
    regex = _signpat.search(str)
    sign = regex.group(1)
    str = regex.group(2)
    while len(str) > 3:
        rc = ',%s%s' % (str[-3:], rc)
        str = str[:-3]

    return sign + str + rc


def amtcomma(str):
    return d2s(str)


def i2s(str):
    """i2s(str) -> [-]nnn,nnn,nnn"""
    str = '%d' % long(str)
    regex = _signpat.search(str)
    sign = regex.group(1)
    str = regex.group(2)
    rc = ''
    while len(str) > 3:
        rc = ',%s%s' % (str[-3:], rc)
        str = str[:-3]

    return sign + str + rc


def ssn(str, n=None):
    """Return ssn as nnn-nn-nnnn"""
    if n is None:
        n = 11
    str = str.replace('-', '')
    str = str[:3] + '-' + str[3:5] + '-' + str[5:]
    return str[:n]


def detab(src, ts=4):
    """Expand tabs to spaces with tab stops at ts intervals"""
    assert ts > 0, 'detab: ts tab stop must be > 0'
    lines = src.split('\n')
    outlines = []
    for src in lines:
        dst = ''
        while len(src):
            n = src.find('\t')
            if n == -1:
                dst += src
                break
            dst += src[:n] + ' '
            while len(dst) % ts:
                dst += ' '

            src = src[n + 1:]

        outlines.append(dst)

    return ('\n').join(outlines)


def yesno(inp):
    """Yes or No returned in upper case"""
    inp = str(inp)[:1].upper()
    if inp in ('Y', 'N'):
        return inp
    raise ValueError


_ipaddrPattern = re.compile('^([0-9]{1,3})\\.([0-9]{1,3})\\.([0-9]{1,3})\\.([0-9]{1,3})$')

def ipaddr(ip):
    """Simpleminded IP edit"""
    if ip:
        R = _ipaddrPattern.match(str(ip))
        if not R:
            raise BadData('ipaddr', 'ipaddr: invalid IP >%s<' % ip)
        for i in R.groups():
            i = int(i)
            if not 0 <= i <= 255:
                raise BadData('ipaddr', '>%s<: octet %d out of range' % (ip, i))

    return ip


_intPattern = re.compile('^([-+]{0,1}[0-9]+)')

def str2int(value):
    """Convert leading digits of string to integer"""
    try:
        rc = int(value)
    except ValueError:
        R = _intPattern.match(str(value))
        if R:
            rc = int(R.group(1))
        else:
            rc = 0

    return rc


def _myoct(R):
    i = chr(eval(R.group(1)))
    return i


def _myhex(R):
    i = chr(eval(R.group(1)))
    return i


def _my999(R):
    return chr(R.group(1)) & 127


def _myord(R):
    return chr(ord(R.group(1)) & 31)


def _mychr(R):
    return R.group(1)


_stringPatterns = (
 (
  re.compile('\\\\E'), '\x1b'),
 (
  re.compile('\\200'), chr(0)),
 (
  re.compile('\\\\(0\\d\\d)'), _myoct),
 (
  re.compile('\\\\(0x[0-9A-Fa-f][0-9A-Fa-f])'), _myhex),
 (
  re.compile('\\\\(\\d\\d\\d)'), _my999),
 (
  re.compile('\\\\n'), '\n'),
 (
  re.compile('\\\\r'), '\r'),
 (
  re.compile('\\\\t'), '\t'),
 (
  re.compile('\\\\b'), '\x08'),
 (
  re.compile('\\\\f'), '\x0c'),
 (
  re.compile('\\\\\\^'), b'\xff'),
 (
  re.compile('\\^\\?'), '\x7f'),
 (
  re.compile('\\^(.)'), _myord),
 (
  re.compile('\\377'), '^'),
 (
  re.compile('\\\\(.)'), _mychr))

def termcap2chars(value, debug=False):
    """Convert termcap encoded string to binary characters"""
    i = 0
    for pat, repl in _stringPatterns:
        i += 1
        try:
            value = pat.sub(repl, value)
        except Exception as e:
            if debug:
                print 'error pattern %d' % i
                print 'error = >%s< i = %d value = >%s<' % (e, i, value)

    return value


_specialChars = re.compile('([\'";])')

def sqlrepr(str):
    """Convert string to SQL safe string"""
    str = "'" + _specialChars.sub('\\\\\\1', str) + "'"
    return str


if __name__ == '__main__':
    print sqlrepr('t\'est;s""t\\\\uff')
    sys.exit(0)
    d = detab('ab\tcd\t\tef')
    print str2int('13.7')
    print 'n = %d >%s<' % (len(d), d)
    print '12345678901234567890'
    print d
    print ipaddr('192.136.111.207')