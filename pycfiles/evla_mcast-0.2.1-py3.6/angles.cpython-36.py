# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/evla_mcast/angles.py
# Compiled at: 2018-02-26 13:33:20
# Size of source mod 2**32: 57287 bytes
from __future__ import print_function, division, absolute_import, unicode_literals
from builtins import bytes, dict, object, range, map, input, str
from future.utils import itervalues, viewitems, iteritems, listvalues, listitems
from io import open
import warnings, math, re

def r2d(r):
    """Convert radians into degrees."""
    return math.degrees(r)


def d2r(d):
    """Convert degrees into radians."""
    return math.radians(d)


def h2d(h):
    """Convert hours into degrees."""
    return h * 15.0


def d2h(d):
    """Convert degrees into hours."""
    return d * 0.06666666666666667


def arcs2d(arcs):
    """Convert arcseconds into degrees."""
    return arcs / 3600.0


def d2arcs(d):
    """Convert degrees into arcseconds."""
    return d * 3600.0


def h2r(h):
    """Convert hours into radians."""
    return d2r(h2d(h))


def r2h(r):
    """Convert radians into hours."""
    return d2h(r2d(r))


def arcs2r(arcs):
    """Convert arcseconds into radians."""
    return d2r(arcs2d(arcs))


def r2arcs(r):
    """Convert radians into arcseconds."""
    return d2arcs(r2d(r))


def arcs2h(arcs):
    """Convert arcseconds into hours."""
    return d2h(arcs2d(arcs))


def h2arcs(h):
    """Convert hours into arcseconds."""
    return d2arcs(h2d(h))


def normalize(num, lower=0, upper=360, b=False):
    """Normalize number to range [lower, upper) or [lower, upper].

    Parameters
    ----------
    num : float
        The number to be normalized.
    lower : int
        Lower limit of range. Default is 0.
    upper : int
        Upper limit of range. Default is 360.
    b : bool
        Type of normalization. Default is False. See notes.

    Returns
    -------
    n : float
        A number in the range [lower, upper) or [lower, upper].

    Raises
    ------
    ValueError
      If lower >= upper.

    Notes
    -----
    If the keyword `b == False`, then the normalization is done in the
    following way. Consider the numbers to be arranged in a circle,
    with the lower and upper ends sitting on top of each other. Moving
    past one limit, takes the number into the beginning of the other
    end. For example, if range is [0 - 360), then 361 becomes 1 and 360
    becomes 0. Negative numbers move from higher to lower numbers. So,
    -1 normalized to [0 - 360) becomes 359.

    If the keyword `b == True`, then the given number is considered to
    "bounce" between the two limits. So, -91 normalized to [-90, 90],
    becomes -89, instead of 89. In this case the range is [lower,
    upper]. This code is based on the function `fmt_delta` of `TPM`.

    Range must be symmetric about 0 or lower == 0.

    Examples
    --------
    >>> normalize(-270,-180,180)
    90.0
    >>> import math
    >>> math.degrees(normalize(-2*math.pi,-math.pi,math.pi))
    0.0
    >>> normalize(-180, -180, 180)
    -180.0
    >>> normalize(180, -180, 180)
    -180.0
    >>> normalize(180, -180, 180, b=True)
    180.0
    >>> normalize(181,-180,180)
    -179.0
    >>> normalize(181, -180, 180, b=True)
    179.0
    >>> normalize(-180,0,360)
    180.0
    >>> normalize(36,0,24)
    12.0
    >>> normalize(368.5,-180,180)
    8.5
    >>> normalize(-100, -90, 90)
    80.0
    >>> normalize(-100, -90, 90, b=True)
    -80.0
    >>> normalize(100, -90, 90, b=True)
    80.0
    >>> normalize(181, -90, 90, b=True)
    -1.0
    >>> normalize(270, -90, 90, b=True)
    -90.0
    >>> normalize(271, -90, 90, b=True)
    -89.0
    """
    from math import floor, ceil
    res = num
    if not b:
        if lower >= upper:
            raise ValueError('Invalid lower and upper limits: (%s, %s)' % (
             lower, upper))
        else:
            res = num
            if num > upper or num == lower:
                num = lower + abs(num + upper) % (abs(lower) + abs(upper))
            if num < lower or num == upper:
                num = upper - abs(num - lower) % (abs(lower) + abs(upper))
        res = lower if num == upper else num
    else:
        total_length = abs(lower) + abs(upper)
        if num < -total_length:
            num += ceil(num / (-2 * total_length)) * 2 * total_length
        if num > total_length:
            num -= floor(num / (2 * total_length)) * 2 * total_length
        if num > upper:
            num = total_length - num
        if num < lower:
            num = -total_length - num
        res = num
    res *= 1.0
    return res


def d2d(d):
    """Normalize angle in degree to [0, 360)."""
    return normalize(d, 0, 360)


def h2h(h):
    """Normalize angle in hours to [0, 24.0)."""
    return normalize(h, 0, 24)


def r2r(r):
    """Normalize angle in radians to [0, 2π)."""
    return normalize(r, 0, 2 * math.pi)


def deci2sexa(deci, pre=3, trunc=False, lower=None, upper=None, b=False, upper_trim=False):
    """Returns the sexagesimal representation of a decimal number.

    Parameters
    ----------
    deci : float
        Decimal number to be converted into sexagesimal. If `lower` and
        `upper` are given then the number is normalized to the given
        range before converting to sexagesimal.
    pre : int
        The last part of the sexagesimal number is rounded to these
        many decimal places. This can be negative. Default is 3.
    trunc : bool
        If True then the last part of the sexagesimal number is
        truncated and not rounded to `pre` decimal places. Default is
        False.
    lower : int
        Lower bound of range to which number is to be normalized.
    upper : int
        Upper bound of range to which number is to be normalized.
    b : bool
        Affects type of normalization. See docstring for `normalize`.
    upper_trim : bool
        If `lower` and `upper` are given and this is True, then if the
        first part of the sexagesimal number is equal to `upper`, it is
        replaced with `lower`. This converts numbers such as "24 00
        00.000" to "00 00 00.000". Default value is False.

    Returns
    -------
    s : 4 element tuple; (int, int, int, float)
        A tuple of sign and the three parts of the sexagesimal
        number. Sign is 1 for positive and -1 for negative values. The
        sign applies to the whole angle and not to any single part,
        i.e., all parts are positive and the sign multiplies the
        angle. The first and second parts of the sexagesimal number are
        integers and the last part is a float.

    Notes
    -----
    The given decimal number `deci` is converted into a sexagesimal
    number. The last part of the sexagesimal number is rounded to `pre`
    number of decimal points. If `trunc == True` then instead of
    rounding, the last part is truncated.

    If `lower` and `upper` are given then the number is normalized to
    the given range before converting into sexagesimal format. The `b`
    argument determines the type of normalization. See docstring of the
    `normalize` function for details.

    If `upper_trim` is True then, if after convertion to sexagesimal
    the first part is equal to `upper`, it is replaced with `lower`.
    This is useful in cases where numbers such as "24 00 00.00" needs
    to be converted into "00 00 00.00"

    The returned sign, first element of tuple, applies to the whole
    number and not just to a single part.

    Examples
    --------
    >>> deci2sexa(-11.2345678)
    (-1, 11, 14, 4.444)
    >>> deci2sexa(-11.2345678, pre=5)
    (-1, 11, 14, 4.44408)
    >>> deci2sexa(-11.2345678, pre=4)
    (-1, 11, 14, 4.4441)
    >>> deci2sexa(-11.2345678, pre=4, trunc=True)
    (-1, 11, 14, 4.444)

    >>> deci2sexa(-11.2345678, pre=1)
    (-1, 11, 14, 4.4)
    >>> deci2sexa(-11.2345678, pre=0)
    (-1, 11, 14, 4.0)
    >>> deci2sexa(-11.2345678, pre=-1)
    (-1, 11, 14, 0.0)

    >>> x = 23+59/60.0+59.99999/3600.0

    To 3 decimal places, this number is 24 or 0 hours.

    >>> deci2sexa(x, pre=3, lower=0, upper=24, upper_trim=True)
    (1, 0, 0, 0.0)
    >>> deci2sexa(x, pre=3, lower=0, upper=24, upper_trim=False)
    (1, 24, 0, 0.0)

    To 5 decimal places, we get back the full value.

    >>> deci2sexa(x, pre=5, lower=0, upper=24, upper_trim=True)
    (1, 23, 59, 59.99999)

    """
    if lower != None:
        if upper != None:
            deci = normalize(deci, lower=lower, upper=upper, b=b)
        else:
            sign = 1
            if deci < 0:
                deci = abs(deci)
                sign = -1
            hd, f1 = divmod(deci, 1)
            mm, f2 = divmod(f1 * 60.0, 1)
            sf = f2 * 60.0
            fp = 10 ** pre
            if trunc:
                ss, _ = divmod(sf * fp, 1)
            else:
                ss = round(sf * fp, 0)
            ss = int(ss)
            if ss == 60 * fp:
                mm += 1
                ss = 0
            if mm == 60:
                hd += 1
                mm = 0
            hd = int(hd)
            mm = int(mm)
            if lower != None:
                if upper != None:
                    if upper_trim:
                        if hd == upper:
                            hd = lower
    else:
        if hd == 0:
            if mm == 0:
                if ss == 0:
                    sign = 1
    ss /= float(fp)
    return (
     sign, hd, mm, ss)


def sexa2deci(sign, hd, mm, ss, todeg=False):
    """Combine sexagesimal components into a decimal number.

    Parameters
    ----------
    sign : int
        Sign of the number: 1 for +ve, -1 for negative.
    hd : float
        The hour or degree like part.
    mm : float
        The minute or arc-minute like part.
    ss : float
        The second or arc-second like part.
    todeg : bool
        If True then convert to degrees, assuming that the input value
        is in hours. Default is False.

    Returns
    -------
    d : float
        The decimal equivalent of the sexagesimal number.

    Raises
    ------
    ValueError
        This exception is raised if `sign` is not -1 or 1.

    Notes
    -----
    The angle returned is::

      sign * (hd + mm / 60.0 + ss / 3600.0)

    In sexagesimal notation the sign applies to the whole quantity and
    not to each part separately. So the `sign` is asked separately, and
    applied to the whole quantity.

    If the sexagesimal quantity is in hours, then we frequently want to
    convert it into degrees. If the `todeg == True` then the given
    value is assumed to be in hours, and the returned value will be in
    degrees.

    Examples
    --------
    >>> d = sexa2deci(1,12,0,0.0)
    >>> d
    12.0
    >>> d = sexa2deci(1,12,0,0.0,todeg=True)
    >>> d
    180.0
    >>> x = sexa2deci(1,9,12.456,0.0)
    >>> assert round(x,4) == 9.2076
    >>> x  = sexa2deci(1,11,30,27.0)
    >>> assert round(x, 4) == 11.5075
    """
    divisors = [
     1.0, 60.0, 3600.0]
    d = 0.0
    if sign not in (-1, 1):
        raise ValueError('Sign has to be -1 or 1.')
    sexages = [sign, hd, mm, ss]
    for i, divis in zip(sexages[1:], divisors):
        d += i / divis

    d *= sexages[0]
    if todeg:
        d = h2d(d)
    return d


def fmt_angle(val, s1=' ', s2=' ', s3=' ', pre=3, trunc=False, lower=None, upper=None, b=False, upper_trim=False):
    """Return sexagesimal string of given angle in degrees or hours.

    Parameters
    ----------
    val : float
        The angle (in degrees or hours) that is to be converted into a
        sexagesimal string.
    s1 : str
        Character to be used between the first and second parts of the
        the sexagesimal representation.
    s2 : str
        Character to be used between the second and third parts of the
        the sexagesimal representation.
    s3 : str
        Character to be used after the third part of the sexagesimal
        representation.
    pre : int
        The final part of the sexagesimal number is rounded to these
        many decimal places. This can be negative.
    trunc : bool
        If True then the third part of the sexagesimal number is
        truncated to `pre` decimal places, instead of rounding.
    lower, upper : float
        If `lower` and `upper` are given then the given value is
        normalized into the this range before converting to sexagesimal
        string.
    b : bool
        This affect how the normalization is performed. See notes. This
        works exactly like that for the function `normalize()`.
    upper_trim : bool
        If `lower` and `upper` are given, then if the first part of the
        sexagesimal number equals `upper`, it is replaced with
        `lower`. For examples, "12 00 00" gets turned into "00 00
        00".

    See also
    --------
    normalize
    deci2sexa

    Examples
    --------
    >>> fmt_angle(12.348978659, pre=4, trunc=True)
    '+12 20 56.3231 '
    >>> fmt_angle(12.348978659, pre=5)
    '+12 20 56.32317 '
    >>> fmt_angle(12.348978659, s1='HH ', s2='MM ', s3='SS', pre=5)
    '+12HH 20MM 56.32317SS'

    >>> x = 23+59/60.0+59.99999/3600.0
    >>> fmt_angle(x)
    '+24 00 00.000 '
    >>> fmt_angle(x, lower=0, upper=24, upper_trim=True)
    '+00 00 00.000 '
    >>> fmt_angle(x, pre=5)
    '+23 59 59.99999 '
    >>> fmt_angle(-x, lower=0, upper=24, upper_trim=True)
    '+00 00 00.000 '
    >>> fmt_angle(-x)
    '-24 00 00.000 '

    """
    if lower == None or upper == None:
        n = val
    else:
        n = normalize(val, lower=lower, upper=upper, b=b)
    x = deci2sexa(n, pre=pre, trunc=trunc, lower=lower, upper=upper, upper_trim=upper_trim)
    p = '{3:0' + '{0}.{1}'.format(pre + 3, pre) + 'f}' + s3
    p = '{0}{1:02d}' + s1 + '{2:02d}' + s2 + p
    return (p.format)('-' if x[0] < 0 else '+', *x[1:])


def phmsdms(hmsdms):
    """Parse a string containing a sexageismal number.

    This can handle several types of delimiters and will process
    reasonably valid strings. See examples.

    Parameters
    ----------
    hmsdms : str
        String containing a sexagesimal number.

    Returns
    -------
    d : dict

        parts : a 3 element list of floats
            The three parts of the sexagesimal number that were
            identified.
        vals : 3 element list of floats
            The numerical values of the three parts of the sexagesimal
            number.
        sign : int
            Sign of the sexagesimal number; 1 for positive and -1 for
            negative.
        units : {"degrees", "hours"}
            The units of the sexagesimal number. This is infered from
            the characters present in the string. If it a pure number
            then units is "degrees".

    Examples
    --------
    >>> phmsdms("12")

    {'parts': [12.0, None, None],
     'sign': 1,
     'units': 'degrees',
     'vals': [12.0, 0.0, 0.0]}
    >>> phmsdms("12h")

    {'parts': [12.0, None, None],
     'sign': 1,
     'units': 'hours',
     'vals': [12.0, 0.0, 0.0]}
    >>> phmsdms("12d13m14.56")

    {'parts': [12.0, 13.0, 14.56],
     'sign': 1,
     'units': 'degrees',
     'vals': [12.0, 13.0, 14.56]}
    >>> phmsdms("12d13m14.56")

    {'parts': [12.0, 13.0, 14.56],
     'sign': 1,
     'units': 'degrees',
     'vals': [12.0, 13.0, 14.56]}
    >>> phmsdms("12d14.56ss")

    {'parts': [12.0, None, 14.56],
     'sign': 1,
     'units': 'degrees',
     'vals': [12.0, 0.0, 14.56]}
    >>> phmsdms("14.56ss")

    {'parts': [None, None, 14.56],
     'sign': 1,
     'units': 'degrees',
     'vals': [0.0, 0.0, 14.56]}

    >>> phmsdms("12h13m12.4s")

    {'parts': [12.0, 13.0, 12.4],
     'sign': 1,
     'units': 'hours',
     'vals': [12.0, 13.0, 12.4]}

    >>> phmsdms("12:13:12.4s")

    {'parts': [12.0, 13.0, 12.4],
     'sign': 1,
     'units': 'degrees',
     'vals': [12.0, 13.0, 12.4]}

    But `phmsdms("12:13mm:12.4s")` will not work.

    """
    units = None
    sign = None
    pattern1 = re.compile('([-+]?[0-9]*\\.?[0-9]+[^0-9\\-+]*)')
    pattern2 = re.compile('([-+]?[0-9]*\\.?[0-9]+)')
    hmsdms = hmsdms.lower()
    hdlist = pattern1.findall(hmsdms)
    parts = [
     None, None, None]

    def _fill_right_not_none():
        rp = reversed(parts)
        for i, j in enumerate(rp):
            if j is not None:
                break

        if i == 0:
            raise ValueError('Invalid string.')
        else:
            if i == 1:
                parts[2] = v
            elif i == 2:
                if parts[0] is None:
                    parts[0] = v
                else:
                    parts[1] = v

    for valun in hdlist:
        try:
            v = float(valun)
            _fill_right_not_none()
        except ValueError:
            if 'hh' in valun or 'h' in valun:
                m = pattern2.search(valun)
                parts[0] = float(valun[m.start():m.end()])
                units = 'hours'
            else:
                if 'dd' in valun or 'd' in valun:
                    m = pattern2.search(valun)
                    parts[0] = float(valun[m.start():m.end()])
                    units = 'degrees'
                else:
                    if 'mm' in valun or 'm' in valun:
                        m = pattern2.search(valun)
                        parts[1] = float(valun[m.start():m.end()])
                    else:
                        if 'ss' in valun or 's' in valun:
                            m = pattern2.search(valun)
                            parts[2] = float(valun[m.start():m.end()])
                        if "'" in valun:
                            m = pattern2.search(valun)
                            parts[1] = float(valun[m.start():m.end()])
                    if '"' in valun:
                        m = pattern2.search(valun)
                        parts[2] = float(valun[m.start():m.end()])
                if ':' in valun:
                    v = valun.replace(':', '')
                    v = float(v)
                    _fill_right_not_none()

        if not units:
            units = 'degrees'

    for i in parts:
        if i:
            if i < 0.0:
                if sign is None:
                    sign = -1
                else:
                    raise ValueError('Only one number can be negative.')

    if sign is None:
        sign = 1
    vals = [abs(i) if i is not None else 0.0 for i in parts]
    return dict(sign=sign, units=units, vals=vals, parts=parts)


def sep(a1, b1, a2, b2):
    """Angular spearation between two points on a unit sphere.

    This will be an angle between [0, π] radians.

    Parameters
    ----------
    a1, b1 : float
        Longitude-like and latitude-like angles defining the first
        point. Both are in radians.

    a2, b2 : float
        Longitude-like and latitude-like angles defining the second
        point. Both are in radians.

    Notes
    -----
    The great cicle angular separation of the second point from the
    first is returned as an angle in radians. the return value is
    always in the range [0, π].

    Results agree with those from SLALIB routine sla_dsep. See
    _test_with_slalib().

    Examples
    --------
    >>> r2d(sep(0, 0, 0, d2r(90.0)))
    90.0
    >>> r2d(sep(0, d2r(45.0), 0, d2r(90.0)))
    45.00000000000001
    >>> r2d(sep(0, d2r(-45.0), 0, d2r(90.0)))
    135.0

    >>> r2d(sep(0, d2r(-90.0), 0, d2r(90.0)))
    180.0
    >>> r2d(sep(d2r(45.0), d2r(-90.0), d2r(45.0), d2r(90.0)))
    180.0
    >>> r2d(sep(0, 0, d2r(90.0), 0))
    90.0

    >>> r2d(sep(0, d2r(45.0), d2r(90.0), d2r(45.0)))
    60.00000000000001
    >>> import math
    >>> 90.0 * math.cos(d2r(45.0))  # Distance along latitude circle.
    63.63961030678928
    """
    tol = 1e-15
    v = CartesianVector()
    v.from_s(1.0, a1, b1)
    v2 = CartesianVector()
    v2.from_s(1.0, a2, b2)
    d = v.dot(v2)
    c = v.cross(v2).mod
    res = math.atan2(c, d)
    if abs(res) < tol:
        return 0.0
    else:
        return res


def bear(a1, b1, a2, b2):
    """Find bearing/position angle between two points on a unit sphere.

    Parameters
    ----------
    a1, b1 : float
        Longitude-like and latitude-like angles defining the first
        point. Both are in radians.

    a2, b2 : float
        Longitude-like and latitude-like angles defining the second
        point. Both are in radians.

    Notes
    -----
    Position angle of the second point with respect to the first
    is returned in radians. Position angle is calculated clockwise
    and counter-clockwise from the direction towards the North
    pole. It is between [0 and π] if the second point is in the
    eastern hemisphere w.r.t the first, and between (0, -π) if
    the second point is in the western hemisphere w.r.t the first.

    .. warning::

        If the first point is at the pole then bearing is undefined and
        0 is returned.

    Results agree with those from SLALIB rountine sla_dbear. See
    _test_with_slalib().

    Examples
    --------
    >>> angles.bear(0, 0, 0, -angles.d2r(90.0))
    3.141592653589793
    >>> angles.bear(0, -angles.d2r(90.0), 0, 0)
    0.0
    >>> angles.bear(0, -angles.d2r(45.0), 0, 0)
    0.0
    >>> angles.bear(0, -angles.d2r(89.678), 0, 0)
    0.0

    >>> r2d(bear(angles.d2r(45.0), angles.d2r(45.0),
        angles.d2r(60.0), angles.d2r(45.0)))
    84.68152816060062
    >>> r2d(bear(angles.d2r(45.0), angles.d2r(45.0),
        angles.d2r(46.0), angles.d2r(45.0)))
    89.64644212193384

    >>> r2d(bear(angles.d2r(45.0), angles.d2r(45.0),
        angles.d2r(44.0), angles.d2r(45.0)))
    -89.64644212193421

    """
    tol = 1e-15
    v1 = CartesianVector()
    v1.from_s(1.0, a1, b1)
    v2 = CartesianVector()
    v2.from_s(1.0, a2, b2)
    v0 = CartesianVector()
    v0.from_s(r=1.0, alpha=0.0, delta=(d2r(90.0)))
    if abs(v1.cross(v0).mod) < tol:
        warnings.warn('First point is on the pole. Bearing undefined.')
        return 0.0
    else:
        v12 = v1.cross(v2)
        v10 = v1.cross(v0)
        dot = v12.dot(v10)
        cross = v12.cross(v10).mod
        x = math.atan2(cross, dot)
        if v12.z < 0:
            x = -x
        if abs(x) < tol:
            return 0.0
        return x


class Angle(object):
    __doc__ = 'A class for representing angles, including string formatting.\n\n    This is the basic Angle object. The angle is initialized to the\n    given value. Default is 0 radians. This class will accept any\n    reasonably well formatted sexagesimal string representation, in\n    addition to numerical values.\n\n    The value of the angle in different units are available as\n    attributes. The angle object can be converted to a sexagesimal\n    string, which can be customized using other attributes.\n\n    Parameters\n    ----------\n    r : float\n        Angle in radians.\n    d : degrees\n        Angle in degrees.\n    h : float\n        Angle in hours.\n    mm : float\n        The second part, i.e., minutes, of a sexagesimal number.\n    ss : float\n        The third part, i.e., seconds, of a sexagesimal number.\n    sg : str\n        A string containing a sexagesimal number.\n\n    Atttributes\n    -----------\n    r\n    d\n    h\n    arcs\n    ounit\n    pre : float\n        The last part of the sexagesimal string is rounded to these\n        many decimal points. This can be negative.\n    trunc : bool\n        If True, then the last part of the sexagesimal string is\n        truncated to `pre` decimal places, instead of rounding.\n    s1 : str\n        Separator between first and second parts of sexagesimal string.\n    s2 : str\n        Separator between second and third parts of sexagesimal string.\n    s1 : str\n        Separator after the third part of sexagesimal string.\n\n    Notes\n    -----\n    The output string representation depends on `ounit`, `pre` and\n    `trunc` attributes.\n\n    The `ounit` attribute determines the unit. It can be "radians",\n    "degrees" or "hours". For "radians", the string representation is\n    just the number itself.\n\n    The attribute `pre` determines the number of decimal places in the\n    last part of the sexagesimal representation. This can be\n    negative. If `trunc` is true then the number is truncated to `pre`\n    places, else it is rounded.\n\n    The "repr", say using repr() function, of an angle object returns\n    the value in radians.\n\n    See also\n    --------\n    phmsdms\n    sexa2deci\n    deci2sexa\n    normalize\n\n    Examples\n    --------\n    >>> a = Angle(sg="12h34m16.592849219")\n    >>> print a.r, a.d, a.h, a.arcs\n    3.29115230606 188.569136872 12.5712757914 678848.892738\n    >>> print a.ounit\n    hours\n    >>> print a\n    +12 34 16.593\n    >>> print a.pre, a.trunc\n    3 False\n    >>> a.pre = 4\n    >>> print a\n    +12 34 16.5928\n    >>> a.pre = 3\n    >>> a.trunc = True\n    >>> print a\n    +12 34 16.592\n\n    >>> a.ounit = "degrees"\n    >>> print a\n    +188 34 08.8927\n    >>> a.ounit = "radians"\n    >>> print a\n    3.29115230606\n\n    >>> a.ounit = "degrees"\n    >>> a.s1 = "DD "\n    >>> a.s2 = "MM "\n    >>> a.s3 = "SS"\n    >>> print a\n    +188DD 34MM 08.892SS\n\n    Unicode characters can be used. But this will cause problems when\n    converting to string in Python 2.x, i.e., `print a` will raise\n    UnicodeEncodeError.\n\n    >>> a.s1 = u"° "\n    >>> print unicode(a)\n    +12° 34MM 16.593SS\n\n    The default unit is inferred from the input values.\n\n    >>> a = Angle("35d24m34.5")\n    >>> print a\n    +35 24 34.500\n    >>> print a\n    +35 24 34.500\n    >>> a = Angle("35:24:34.5")\n    >>> print a\n    +35 24 34.500\n    >>> a = Angle("35h24m34.5")\n    >>> print a\n    +35 24 34.500\n    >>> a.ounit\n    \'hours\'\n\n    Angle objects can be added to and subtracted from each other.\n\n    >>> a = Angle(h=12.5)\n    >>> b = Angle(h=13.0)\n    >>> c = a - b\n    >>> c.h\n    -0.5000000000000011\n    >>> c = a + b\n    >>> c.h\n    25.5\n\n    '
    _units = ('radians', 'degrees', 'hours')
    _keyws = ('r', 'd', 'h', 'mm', 'ss', 'sg')
    _raw = 0.0
    _iunit = 0
    _ounit = 'radians'
    pre = 3
    trunc = False
    s1 = ' '
    s2 = ' '
    s3 = ' '

    def __init__(self, sg=None, **kwargs):
        if sg != None:
            kwargs['sg'] = str(sg)
        x = ((True if i in self._keyws else False) for i in kwargs)
        if not all(x):
            raise TypeError('Only {0} are allowed.'.format(self._keyws))
        if 'sg' in kwargs:
            x = phmsdms(kwargs['sg'])
            if x['units'] not in self._units:
                raise ValueError('Unknow units: {0}'.format(x['units']))
            self._iunit = self._units.index(x['units'])
            if self._iunit == 1:
                self._setnorm(d2r(sexa2deci(x['sign'], *x['vals'])))
            else:
                if self._iunit == 2:
                    self._setnorm(h2r(sexa2deci(x['sign'], *x['vals'])))
            if len(kwargs) != 1:
                warnings.warn('Only sg = {0} used.'.format(kwargs['sg']))
        else:
            if 'r' in kwargs:
                self._iunit = 0
                self._setnorm(kwargs['r'])
                if len(kwargs) != 1:
                    warnings.warn('Only r = {0} used.'.format(kwargs['r']))
            else:
                if 'd' in kwargs:
                    self._iunit = 1
                    self._setnorm(d2r(sexa2deci(1, kwargs['d'], kwargs.get('mm', 0.0), kwargs.get('ss', 0.0))))
                    if 'h' in kwargs:
                        warnings.warn('h not used.')
                else:
                    if 'h' in kwargs:
                        self._iunit = 2
                        self._setnorm(h2r(sexa2deci(1, kwargs['h'], kwargs.get('mm', 0.0), kwargs.get('ss', 0.0))))
            self._ounit = self._units[self._iunit]

    def _getnorm(self):
        return self._raw

    def _setnorm(self, val):
        self._raw = val

    def __getr(self):
        return self._getnorm()

    def __setr(self, val):
        self._setnorm(val)

    r = property(_Angle__getr, _Angle__setr, doc='Angle in radians.')

    def __getd(self):
        return r2d(self._getnorm())

    def __setd(self, val):
        self._setnorm(d2r(val))

    d = property(_Angle__getd, _Angle__setd, doc='Angle in degrees.')

    def __geth(self):
        return r2h(self._getnorm())

    def __seth(self, val):
        self._setnorm(h2r(val))

    h = property(_Angle__geth, _Angle__seth, doc='Angle in hours.')

    def __getarcs(self):
        return r2arcs(self._getnorm())

    def __setarcs(self, val):
        self._setnorm(arcs2r(val))

    arcs = property(_Angle__getarcs, _Angle__setarcs, doc='Angle in arcseconds.')

    def __getounit(self):
        return self._ounit

    def __setounit(self, val):
        if val not in self._units:
            raise ValueError('Unit can only be {0}'.format(self._units))
        self._ounit = val

    ounit = property(_Angle__getounit, _Angle__setounit, doc='String output unit.')

    def __repr__(self):
        return str(self.r)

    def __str__(self):
        if self.ounit == 'radians':
            return str(self.r)
        else:
            if self.ounit == 'degrees':
                return fmt_angle((self.d), s1=(self.s1), s2=(self.s2), s3=(self.s3),
                  pre=(self.pre),
                  trunc=(self.trunc))
            if self.ounit == 'hours':
                return fmt_angle((self.h), s1=(self.s1), s2=(self.s2), s3=(self.s3),
                  pre=(self.pre),
                  trunc=(self.trunc))

    def __add__(self, other):
        if not isinstance(other, Angle):
            raise ValueError('Addition needs to Angle objects.')
        return Angle(r=(self.r + other.r))

    def __sub__(self, other):
        if not isinstance(other, Angle):
            raise ValueError('Subtraction needs two Angle objects.')
        return Angle(r=(self.r - other.r))


class AlphaAngle(Angle):
    __doc__ = 'Angle for longitudinal angles such as Right Ascension.\n\n    AlphaAngle is a subclass of Angle that can be used to represent\n    longitudinal angles such as Right Ascension, azimuth and longitude.\n\n    In AlphaAngle the attribute `ounit` is always "hours" and\n    formatting is always as an HMS sexagesimal string.\n\n    The angle is normalized to [0, 24) hours.\n\n    This takes the same parameters as the `Angle` class, and has the\n    same attributes as the `Angle` class. The attribute `ounit` is\n    read-only. Additonal attributes are given below.\n\n    Attributes\n    ----------\n    hms : tuple (int, int, int, float)\n        Sexagesimal, HMS, parts of the angle as tuple: first item is\n        sign, second is hours, third is minutes and the fourth is\n        seconds. Sign is 1 for positive and -1 for negative. The values\n        are affected by `pre` and `trunc`.\n    sign : int\n        Sign of the angle. 1 for positive and -1 for negative. Sign\n        applies to the whole angle and not to any single part.\n    hh : int\n        The hours part of `hms`, between [0,23]\n    mm : int\n        The minutes part of `hms`, between [0, 59]\n    ss : float\n        The seconds part of `hms`.\n\n    Notes\n    -----\n    The `pre` and `trunc` properties will affect both the string\n    representation as well as the sexagesimal parts. The angle is\n    normalized into [0, 24) hours in such a way that 25 hours become 1\n    hours and -1 hours become 23 hours.\n\n    See also\n    --------\n    Angle (for common attributes)\n\n    Examples\n    --------\n    >>> a = AlphaAngle(d=180.5)\n    >>> print a\n    +12HH 02MM 00.000SS\n    >>> a = AlphaAngle(h=12.0)\n    >>> print a\n    +12HH 00MM 00.000SS\n    >>> a = AlphaAngle(h=-12.0)\n\n    The attribute `ounit` is read-only.\n\n    >>> a.ounit\n    "hours"\n    >>> print a\n    +12HH 00MM 00.000SS\n\n    If no keyword is provided then the input is taken to a sexagesimal\n    string and the units will be determined from it. The numerical\n    value of the angle in radians, hours, degrees and arc-seconds can\n    be extracted from appropriate attributes.\n\n    >>> a = angles.AlphaAngle("12h14m23.4s")\n    >>> print a\n    +12HH 14MM 23.400SS\n    >>> print a.r, a.d, a.h, a.arcs\n    3.20438087343 183.5975 12.2398333333 660951.0\n\n    The `hms` attribute contains the sexagesimal represenation. These\n    are also accessible as `a.sign`, a.hh`, `a.mm` and `a.ss`. The\n    `pre` and `trunc` attributes are taken into account while\n    generating the `hms` attribute.\n\n    >>> a.hms\n    (1, 12, 0, 0.0)\n    >>> a = AlphaAngle(h=12.54678345)\n    >>> a.hms\n    (1, 12, 32, 48.42)\n    >>> a.sign, a.hh, a.mm, a.ss\n    (1, 12, 32, 48.42)\n    >>> print a\n    +12HH 32MM 48.420SS\n    >>> a.pre = 5\n    >>> a.hms\n    (1, 12, 32, 48.42042)\n    >>> print a\n    +12HH 32MM 48.42042SS\n\n    Separators can be changed.\n\n    >>> a.s1 = " : "\n    >>> a.s2 = " : "\n    >>> a.s3 = ""\n    >>> print a\n    +12 : 32 : 48.420\n\n    Angles are properly normalized.\n\n    >>> a = AlphaAngle(h=25.0)\n    >>> print a\n    +01HH 00MM 00.000SS\n    >>> a = AlphaAngle(h=-1.0)\n    >>> print a\n    +23HH 00MM 00.000SS\n\n    The sexagesimal parts are properly converted into their respective\n    ranges.\n\n    >>> a.hh = 23\n    >>> a.mm = 59\n    >>> a.ss = 59.99999\n    >>> a.hms\n    (1, 0, 0, 0.0)\n    >>> print a\n    +00HH 00MM 00.000SS\n    >>> a.pre = 5\n    >>> a.hms\n    (1, 23, 59, 59.99999)\n    >>> print a\n    +23HH 59MM 59.99999SS\n\n    Angles can be added to and subtracted from each other.\n\n    >>> a = AlphaAngle(h=12.0)\n    >>> b = AlphaAngle(h=13.0)\n    >>> c = a - b\n    >>> c.h\n    -1.0000000000000007\n    >>> c = a + b\n    >>> c.h\n    25.0\n\n    '

    def __init__(self, sg=None, **kwargs):
        (Angle.__init__)(self, sg, **kwargs)
        self._AlphaAngle__ounit = 'hours'
        self.s1 = 'HH '
        self.s2 = 'MM '
        self.s3 = 'SS'

    def _setnorm(self, val):
        self._raw = r2r(val)

    def __getounit(self):
        return self._AlphaAngle__ounit

    ounit = property(fget=_AlphaAngle__getounit, doc='Formatting unit: always hours for RA.')

    def __gethms(self):
        return deci2sexa((self.h), pre=(self.pre), trunc=(self.trunc), lower=0,
          upper=24,
          upper_trim=True)

    def __sethms(self, val):
        if len(val) != 4:
            raise ValueError('HMS must be of the form [sign, HH, MM, SS.ss..]')
        if val[0] not in (-1, 1):
            raise ValueError('Sign has to be -1 or 1.')
        self.h = sexa2deci(*val)

    hms = property(_AlphaAngle__gethms, _AlphaAngle__sethms, doc='HMS tuple.')

    def __getsign(self):
        return self.hms[0]

    def __setsign(self, sign):
        if sign not in (-1, 1):
            raise ValueError('Sign has to be -1 or 1.')
        self.h *= sign

    sign = property(_AlphaAngle__getsign, _AlphaAngle__setsign, doc='Sign of HMS angle.')

    def __gethh(self):
        return self.hms[1]

    def __sethh(self, val):
        if type(val) != type(1):
            raise ValueError('HH takes only integers.')
        x = self.hms
        self.h = sexa2deci(x[0], val, x[2], x[3])

    hh = property(_AlphaAngle__gethh, _AlphaAngle__sethh, doc='HH of HMS angle.')

    def __getmm(self):
        return self.hms[2]

    def __setmm(self, val):
        if type(val) != type(1):
            raise ValueError('MM takes integers only.')
        x = self.hms
        self.h = sexa2deci(x[0], x[1], val, x[3])

    mm = property(_AlphaAngle__getmm, _AlphaAngle__setmm, doc='MM of HMS angle.')

    def __getss(self):
        return self.hms[3]

    def __setss(self, val):
        x = self.hms
        self.h = sexa2deci(x[0], x[1], x[2], val)

    ss = property(_AlphaAngle__getss, _AlphaAngle__setss, doc='SS of HMS angle.')

    def __str__(self):
        return fmt_angle((self.h), s1=(self.s1), s2=(self.s2), s3=(self.s3), pre=(self.pre),
          trunc=(self.trunc),
          lower=0,
          upper=24,
          upper_trim=True)

    def __add__(self, other):
        """Adds any type of angle to this."""
        if not isinstance(other, Angle):
            raise ValueError('Addition needs two Angle objects.')
        return AlphaAngle(r=(self.r + other.r))

    def __sub__(self, other):
        """Subtracts any type of angle from this."""
        if not isinstance(other, Angle):
            raise ValueError('Subtraction needs two Angle objects.')
        return AlphaAngle(r=(self.r - other.r))


class DeltaAngle(Angle):
    __doc__ = 'Angle for latitudinal angles such as Declination.\n\n    DeltaAngle is a subclass of Angle for latitudinal angles such as\n    Declination, elevation and latitude.\n\n    In DeltaAngle the attribute `ounit` is always "degrees" and\n    formatting is always as a DMS sexagesimal string.\n\n    The angle is normalized to the range [-90, 90] degrees.\n\n    This takes the same parameters as the `Angle` class, and has the\n    same attributes as the `Angle` class. The attribute `ounit` is\n    read-only. Additonal attributes are given below.\n\n    Attributes\n    ----------\n    dms : tuple (int, int, int, float)\n        Sexagesimal, DMS, parts of the angle as tuple: first item is\n        sign, second is degrees, third is arc-minutes and the fourth is\n        arc-seconds. Sign is 1 for positive and -1 for negative. The\n        `pre` and `trunc` attributes affect the value of `dms`.\n    sign : int\n        Sign of the angle. 1 for positive and -1 for negative. Sign\n        applies to the whole angle and not to any single part.\n    dd : int\n        The degrees part of `dms`, between [-90, 90]\n    mm : int\n        The arc-minutes part of `dms`, between [0, 59]\n    ss : float\n        The arc-seconds part of `dms`.\n\n    Notes\n    -----\n    The `pre` and `trunc` properties will affect both the string\n    representation as well as the sexagesimal parts. The angle is\n    normalized between [-90, 90], in such a way that -91 becomes -89\n    and 91 becomes 89.\n\n    See also\n    --------\n    Angle (for other attributes)\n\n    Examples\n    --------\n    >>> a = DeltaAngle(d=-45.0)\n    >>> print a\n    -45DD 00MM 00.000SS\n    >>> a = DeltaAngle(d=180.0)\n    >>> print a\n    +00DD 00MM 00.000SS\n    >>> a = DeltaAngle(h=12.0)\n    >>> print a\n    +00DD 00MM 00.000SS\n    >>> a = DeltaAngle(sg="91d")\n    >>> print a\n    +89DD 00MM 00.000SS\n\n    Attribute `ounit` is always "degrees".\n\n    >>> a.ounit\n    \'degrees\'\n\n    If no keyword is provided then the input is taken to a sexagesimal\n    string and the units will be determined from it.  The numerical\n    value of the angle in radians, hours, degrees and arc-seconds can\n    be extracted from appropriate attributes.\n\n    >>> a = DeltaAngle("12d23m14.2s")\n    >>> print a\n    +12DD 23MM 14.200SS\n    >>> print a.r, a.d, a.h, a.arcs\n    0.216198782581 12.3872777778 0.825818518519 44594.2\n\n    The `dms` attribute contains the sexagesimal represenation. These\n    are also accessible as `a.sign`, a.dd`, `a.mm` and `a.ss`. The\n    `pre` and `trunc` attributes are taken into account.\n\n    >>> a = DeltaAngle(d=12.1987546)\n    >>> a.dms\n    (1, 12, 11, 55.517)\n    >>> a.pre = 5\n    >>> a.dms\n    (1, 12, 11, 55.51656)\n    >>> a.dd, a.mm, a.ss\n    (12, 11, 55.51656)\n    >>> a.pre = 0\n    >>> a.dms\n    (1, 12, 11, 56.0)\n\n    The separators can be changed.\n\n    >>> a = DeltaAngle(d=12.3459876)\n    >>> a.s1 = " : "\n    >>> a.s2 = " : "\n    >>> a.s3 = ""\n    >>> print a\n    +12 : 20 : 45.555\n\n    Angles are properly normalized.\n\n    >>> a = DeltaAngle(d=-91.0)\n    >>> print a\n    -89DD 00MM 00.000SS\n    >>> a = DeltaAngle(d=91.0)\n    >>> print a\n    +89DD 00MM 00.000SS\n\n    The sexagesimal parts are properly normalized into their respective\n    ranges.\n\n    >>> a.dd = 89\n    >>> a.mm = 59\n    >>> a.ss = 59.9999\n    >>> print a\n    +90DD 00MM 00.000SS\n    >>> a.pre = 5\n    >>> print a\n    +89DD 59MM 59.99990SS\n    >>> a.dd = 89\n    >>> a.mm = 60\n    >>> a.ss = 60\n    >>> print a\n    +89DD 59MM 00.000SS\n\n    Angles can be added to and subtracted from each other.\n\n    >>> a = DeltaAngle(d=12.0)\n    >>> b = DeltaAngle(d=13.0)\n    >>> c = a - b\n    >>> c.d\n    -0.9999999999999998\n    >>> c = a + b\n    >>> c.d\n    25.000000000000004\n    >>> print c\n    +25DD 00MM 00.000SS\n    >>> c = a - b\n    >>> print c\n    -01DD 00MM 00.000SS\n\n    '

    def __init__(self, sg=None, **kwargs):
        (Angle.__init__)(self, sg, **kwargs)
        self._DeltaAngle__ounit = 'degrees'
        self.s1 = 'DD '
        self.s2 = 'MM '
        self.s3 = 'SS'

    def _setnorm(self, val):
        self._raw = normalize(val, lower=(-90), upper=90, b=True)

    def __getounit(self):
        return self._DeltaAngle__ounit

    ounit = property(fget=_DeltaAngle__getounit, doc='Formatting unit: always degrees for Dec.')

    def __getdms(self):
        return deci2sexa((self.d), pre=(self.pre), trunc=(self.trunc))

    def __setdms(self, val):
        if len(val) != 4:
            raise ValueError('DMS must be of the form [sign, DD, MM, SS.ss..]')
        if val[0] not in (-1, 1):
            raise ValueError('Sign has to be -1 or 1.')
        self.d = sexa2deci(*val)

    dms = property(_DeltaAngle__getdms, doc='DMS tuple.')

    def __getsign(self):
        return self.dms[0]

    def __setsign(self, sign):
        if sign not in (-1, 1):
            raise ValueError('Sign has to be -1 or 1')
        self.d *= sign

    sign = property(_DeltaAngle__getsign, _DeltaAngle__setsign, doc='Sign of DMS angle.')

    def __getdd(self):
        return self.dms[1]

    def __setdd(self, val):
        if type(val) != type(1):
            raise ValueError('DD takes only integers.')
        x = self.dms
        self.d = sexa2deci(x[0], val, x[2], x[3])

    dd = property(_DeltaAngle__getdd, _DeltaAngle__setdd, doc='DD of DMS angle.')

    def __getmm(self):
        return self.dms[2]

    def __setmm(self, val):
        if type(val) != type(1):
            raise ValueError('MM takes only integers.')
        x = self.dms
        self.d = sexa2deci(x[0], x[1], val, x[3])

    mm = property(_DeltaAngle__getmm, _DeltaAngle__setmm, doc='MM of DMS angle.')

    def __getss(self):
        return self.dms[3]

    def __setss(self, val):
        x = self.dms
        self.d = sexa2deci(x[0], x[1], x[2], val)

    ss = property(_DeltaAngle__getss, _DeltaAngle__setss, doc='SS of DMS angle.')

    def __unicode__(self):
        return fmt_angle((self.d), s1=(self.s1), s2=(self.s2), s3=(self.s3), pre=(self.pre),
          trunc=(self.trunc),
          lower=(-90),
          upper=90,
          b=True)

    def __str__(self):
        return fmt_angle((self.d), s1=(self.s1), s2=(self.s2), s3=(self.s3), pre=(self.pre),
          trunc=(self.trunc),
          lower=(-90),
          upper=90,
          b=True)

    def __add__(self, other):
        """Adds any type of angle to this."""
        if not isinstance(other, Angle):
            raise ValueError('Addition needs two Angle objects.')
        return DeltaAngle(r=(self.r + other.r))

    def __sub__(self, other):
        """Subtracts any type of angle from this."""
        if not isinstance(other, Angle):
            raise ValueError('Subtraction needs two Angle objects.')
        return DeltaAngle(r=(self.r - other.r))


class CartesianVector(object):
    __doc__ = 'A 3D Cartesian vector.\n\n    An instance of this is added to an AngularPosition object, so that\n    vector methods can be used for calculating bearings and\n    separations.\n\n    Methods\n    -------\n    dot\n    cross\n    mod\n    from_s\n\n    '

    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def dot(self, v):
        return self.x * v.x + self.y * v.y + self.z * v.z

    def cross(self, v):
        """Cross product of two vectors.

        Parameters
        ----------
        v : CartesianVector
            The vector to take cross product with.

        Returns
        -------
        v : CartesianVector
            Cross product of this vector and the given vector.

        """
        n = self.__class__()
        n.x = self.y * v.z - self.z * v.y
        n.y = -(self.x * v.z - self.z * v.x)
        n.z = self.x * v.y - self.y * v.x
        return n

    @property
    def mod(self):
        """Modulus of vector."""
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def from_s(self, r=1.0, alpha=0.0, delta=0.0):
        """Construct Cartesian vector from spherical coordinates.

        alpha and delta must be in radians.
        """
        self.x = r * math.cos(delta) * math.cos(alpha)
        self.y = r * math.cos(delta) * math.sin(alpha)
        self.z = r * math.sin(delta)

    def __repr__(self):
        return str(self.x, self.y, self.z)

    def __str__(self):
        self.___repr__()


class AngularPosition(object):
    __doc__ = 'Class for representing a point on a unit sphere, say (RA, DEC).\n\n    AngularPosition can be used to work with points on a sphere. This\n    object stores two attributes `alpha` and `delta` that represent the\n    longitudinal and latitudinal angles, repectively. The former is of\n    type `AlphaAngle` and the latter is of type `DeltaAngle`.\n\n    The string representation of AngularPosition is constructed using\n    both alpha and delta.\n\n    Difference between two AngularPosition gives the separation between\n    them in radians.\n\n    The separation between two angular positions can also be obtained\n    by calling the method `sep`.\n\n    The bearing between two points can be obtained using the `bear`\n    method.\n\n    Parameters\n    ----------\n    alpha : float, str\n        The longitudinal angle. If value is a float then it is taken to\n        be the angle in hours. If value is str then it is treated as a\n        sexagesimal number and the units are determined from\n        it. Default is 0.0.\n\n    delta : float, str\n        The latitudinal angle. If value is a float then it is taken to be\n        the angle in degrees. If value is str then it is treated as a\n        sexagesimal number and the units are determined from\n        it. Default is 0.0.\n\n    Attributes\n    ----------\n    alpha : AlphaAngle\n        The longitudinal angle.\n    delta : DeltaAngle\n        The lattudinal angle.\n    dlim : str\n        Delimiter to use between `alpha` and `delta` angles in string\n        representation.\n\n    Methods\n    -------\n    sep : return great circle separation in radians.\n    bear : return bearing/position angle in radians.\n\n    See also\n    --------\n    Angle\n    AlphaAngle\n    DeltaAngle\n\n    Examples\n    --------\n    >>> pos1 = AngularPosition(alpha=12.0, delta=90.0)\n    >>> pos2 = AngularPosition(alpha=12.0, delta=0.0)\n    >>> angles.r2d(pos2.bear(pos1))\n    0.0\n    >>> angles.r2d(pos1.bear(pos2))\n    0.0\n    >>> angles.r2d(pos1.sep(pos2))\n    90.0\n    >>> pos1.alpha.h = 0.0\n    >>> pos2.alpha.h = 0.0\n    >>> angles.r2d(pos1.sep(pos2))\n    90.0\n    >>> angles.r2d(pos2.bear(pos1))\n    0.0\n    >>> angles.r2d(pos1.bear(pos2))\n    0.0\n\n    >>> pos2.delta.d = -90\n    >>> angles.r2d(pos1.bear(pos2))\n    0.0\n    >>> angles.r2d(pos1.sep(pos2))\n    180.0\n\n    >>> print pos1\n    +00HH 00MM 00.000SS +90DD 00MM 00.000SS\n    >>> print pos2\n    +00HH 00MM 00.000SS +00DD 00MM 00.000SS\n    >>> pos1.dlim = " | "\n    >>> print pos1\n    +00HH 00MM 00.000SS | +90DD 00MM 00.000SS\n\n    '
    dlim = ' '

    def __init__(self, alpha=0.0, delta=0.0):
        if type(alpha) == type(' '):
            self._alpha = AlphaAngle(sg=alpha)
        else:
            self._alpha = AlphaAngle(h=alpha)
        if type(delta) == type(' '):
            self._delta = DeltaAngle(sg=delta)
        else:
            self._delta = DeltaAngle(d=delta)

    def __getalpha(self):
        return self._alpha

    def __setalpha(self, a):
        if not isinstance(a, AlphaAngle):
            raise TypeError('alpha must be of type AlphaAngle.')
        else:
            self._alpha = a

    alpha = property(fget=_AngularPosition__getalpha, fset=_AngularPosition__setalpha, doc='Longitudinal angle (AlphaAngle).')

    def __getdelta(self):
        return self._delta

    def __setdelta(self, a):
        if not isinstance(a, DeltaAngle):
            raise TypeError('delta must be of type DeltaAngle.')
        else:
            self._delta = a

    delta = property(fget=_AngularPosition__getdelta, fset=_AngularPosition__setdelta, doc='Latitudinal angle (DeltaAngle).')

    def sep(self, p):
        """Angular spearation between objects in radians.

        Parameters
        ----------
        p : AngularPosition
            The object to which the separation from the current object
            is to be calculated.

        Notes
        -----
        This method calls the function sep(). See its docstring for
        details.

        See also
        --------
        sep

        """
        return sep(self.alpha.r, self.delta.r, p.alpha.r, p.delta.r)

    def bear(self, p):
        """Find position angle between objects, in radians.

        Parameters
        ----------
        p : AngularPosition
            The object to which bearing must be determined.

        Notes
        -----
        This method calls the function bear(). See its docstring for
        details.

        See also
        --------
        bear

        """
        return bear(self.alpha.r, self.delta.r, p.alpha.r, p.delta.r)

    def __str__(self):
        return self.dlim.join([self.alpha.__str__(),
         self.delta.__str__()])

    def __repr__(self):
        return str(dict(alpha=(self.alpha.h), delta=(self.delta.d)))

    def __sub__(self, other):
        if type(other) != type(self):
            raise TypeError('Subtraction needs an AngularPosition object.')
        return self.sep(other)


def _test_with_slalib():
    try:
        from pyslalib import slalib
    except ImportError:
        print('Tests not run on this machine.')
        print('PySLALIB is needed to run tests on this machine.')
        print('When run the results are identical to those from SLALIB.')
        exit(1)

    import random, math
    alpha = [random.uniform(0, 2 * math.pi) for i in range(100)]
    delta = [random.uniform(-math.pi / 2, math.pi / 2) for i in range(100)]
    alpha1 = [random.uniform(0, 2 * math.pi) for i in range(100)]
    delta1 = [random.uniform(-math.pi / 2, math.pi / 2) for i in range(100)]
    s = [slalib.sla_dsep(alpha[i], delta[i], alpha1[i], delta1[i]) for i in range(100)]
    pos1 = [AngularPosition() for i in range(100)]
    pos2 = [AngularPosition() for i in range(100)]
    for i in range(100):
        pos1[i].alpha.r = alpha[i]
        pos1[i].delta.r = delta[i]
        pos2[i].alpha.r = alpha1[i]
        pos2[i].delta.r = delta1[i]

    s1 = [pos1[i].sep(pos2[i]) for i in range(100)]
    d = [i - j for i, j in zip(s, s1)]
    if not abs(min(d)) <= 1e-08:
        raise AssertionError
    else:
        if not abs(max(d)) <= 1e-08:
            raise AssertionError
        else:
            s = [slalib.sla_dbear(alpha[i], delta[i], alpha1[i], delta1[i]) for i in range(100)]
            s1 = [pos1[i].bear(pos2[i]) for i in range(100)]
            d = [i - j for i, j in zip(s, s1)]
            assert abs(min(d)) <= 1e-08
        assert abs(max(d)) <= 1e-08


if __name__ == '__main__':
    _test_with_slalib()
    print('Tests ran succesfully.')