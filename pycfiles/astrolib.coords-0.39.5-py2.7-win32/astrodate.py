# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\astrolib\coords\astrodate.py
# Compiled at: 2014-01-13 11:58:06
"""
For more information about astronomical date specifications,
consult a reference source such as
`this page <http://tycho.usno.navy.mil/systime.html>`_
provided by the US Naval Observatory.

Constants and formulae in this module were taken from the
`times.h` include file of the `tpm` package by Jeff Percival,
to ensure compatibility.

"""
import types, datetime
B1950 = 2433282.42345905
J2000 = 2451545.0
CB = 36524.21987817305
CJ = 36525.0
MJD_0 = 2400000.5

def jyear2jd(jyear):
    """
    Parameters
    ----------
    jyear : float
        Decimal Julian year.

    Returns
    -------
    value : float
        Julian date.
    
    """
    return J2000 + (jyear - 2000.0) * (CJ / 100.0)


def jd2jyear(jd):
    """
    Parameters
    ----------
    jd : float
        Julian date.

    Returns
    -------
    value : float
        Decimal Julian year.

    """
    return 2000.0 + (jd - J2000) * (100.0 / CJ)


def byear2jd(byear):
    """
    Parameters
    ----------
    byear : float
        Decimal Besselian year.

    Returns
    -------
    value : float
        Julian date.

    """
    return B1950 + (byear - 1950.0) * (CB / 100.0)


def utc2jd(utc):
    """
    Convert UTC to Julian date.
    
    Conversion translated from TPM modules `utcnow.c` and
    `gcal2j.c`, which notes that the algorithm to convert
    from a gregorian proleptic calendar date onto a julian
    day number is taken from The Explanatory Supplement to
    the Astronomical Almanac (1992), section 12.92, equation
    12.92-1, page 604.

    Parameters
    ----------
    utc : :py:class:`datetime.datetime` object
        UTC (Universal Civil Time).

    Returns
    -------
    value : float
        Julian date to the nearest second.
    
    """
    y = float(utc.year)
    m = float(utc.month)
    d = float(utc.day)
    hr = utc.hour
    min = utc.minute
    sec = utc.second
    mterm = int((m - 14) / 12)
    aterm = int(1461 * (y + 4800 + mterm) / 4)
    bterm = int(367 * (m - 2 - 12 * mterm) / 12)
    cterm = int(3 * int((y + 4900 + mterm) / 100) / 4)
    j = aterm + bterm - cterm + d
    j -= 32075
    j -= 0.5
    jd = j + (hr + (min + sec / 60.0) / 60.0) / 24.0
    return jd


def AstroDate(datespec=None):
    """
    AstroDate can be used as a class for managing astronomical
    date specifications (despite the fact that it was implemented
    as a factory function) that returns either a BesselDate or a
    JulianDate, depending on the properties of the datespec.

    AstroDate was originally conceived as a Helper class for the
    Position function for use with pytpm functionality, but also as a
    generally useful class for managing astronomical date specifications.

    The philosophy is the same as Position: to enable the user to specify
    the date once and for all, and access it in a variety of styles.

    .. todo::
        #. Add math functions! Addition, subtraction.
        #. Is there a need to support other date specifications?
           eg FITS-style dates?

    Parameters
    ----------
    datespec : string, float, integer, :py:class:`datetime.datetime`, or `None`

    Returns
    -------
    value : `~astrolib.coords.astrodate.JulianDate` or `~astrolib.coords.astrodate.BesselDate`
        Date specification as entered by the user. Permissible specifications include:
            * Julian year
                * 'J1997', 'J1997.325', 1997.325
                * Return a JulianDate
            * Besselian year
                * 'B1950','B1958.432'
                * Return a BesselDate
            * Julian date
                * 'JD2437241.81', '2437241.81', 2437241.81
                * Return a JulianDate
            * Modified Julian date
                * 'MJD37241.31'
                * Return a JulianDate
            * :py:class:`datetime.datetime` object
                * Assume input time is UTC
                * Return a JulianDate
            * `None`
                * Return the current time as a JulianDate

    Raises
    ------
    ValueError
        Raises an exception if the date specification is a
        string, but begins with a letter that is not
        'B','J','JD', or 'MJD' (case insensitive).

    """
    if datespec is None:
        return JulianDate(datetime.datetime.utcnow())
    else:
        try:
            dstring = datespec.upper()
            if dstring.startswith('B'):
                return BesselDate(datespec)
            if dstring.startswith('JD') or dstring.startswith('MJD') or dstring.startswith('J'):
                return JulianDate(datespec)
            if dstring[0].isalpha():
                raise ValueError, 'Invalid system specification: must be B, J, JD, or MJD'
            else:
                return JulianDate(datespec)
        except AttributeError:
            return JulianDate(datespec)

        return


class JulianDate:
    """
    Attributes
    ----------
    year : float
        Decimal Julian year.

    jd : float
        Julian date.

    mjd : float
        Modified Julian Date

    datespec
        Date specification as entered by the user

    """

    def __init__(self, datespec):
        self.datespec = datespec
        if isinstance(datespec, datetime.datetime):
            self.jd = utc2jd(datespec)
            self.mjd = self.jd - MJD_0
            self.year = jd2jyear(self.jd)
        elif type(datespec) is types.StringType:
            if datespec.upper().startswith('JD'):
                self.jd = float(datespec[2:])
                self.mjd = self.jd - MJD_0
                self.year = jd2jyear(self.jd)
            elif datespec.upper().startswith('MJD'):
                self.mjd = float(datespec[3:])
                self.jd = self.mjd + MJD_0
                self.year = jd2jyear(self.jd)
            elif datespec.upper().startswith('J'):
                self.year = float(datespec[1:])
                self.jd = jyear2jd(self.year)
                self.mjd = self.jd - MJD_0
            elif not datespec[0].isalpha():
                datespec = float(datespec)
                if datespec < 10000:
                    self.year = float(datespec)
                    self.jd = jyear2jd(self.year)
                    self.mjd = self.jd - MJD_0
                else:
                    self.jd = float(datespec)
                    self.mjd = self.jd + MJD_0
                    self.year = jd2jyear(self.jd)
            else:
                print 'help, we are confused'
        elif datespec < 10000:
            self.year = float(datespec)
            self.jd = jyear2jd(self.year)
            self.mjd = self.jd - MJD_0
        else:
            self.jd = datespec
            self.mjd = self.jd + MJD_0
            self.year = jd2jyear(self.jd)

    def __repr__(self):
        return str(self.datespec)

    def __equals__(self, other):
        """All comparisons will be done based on `jd` attribute."""
        return self.jd == other.jd

    def __lt__(self, other):
        return self.jd < other.jd

    def __gt__(self, other):
        return self.jd > other.jd

    def __le__(self, other):
        return self.jd <= other.jd

    def __ge__(self, other):
        return self.jd >= other.jd

    def byear(self):
        """
        Return Besselian year based on previously calculated
        julian date.

        Returns
        -------
        ans : float
            Decimal Besselian year.

        """
        ans = 1950.0 + (x - B1950) * (100.0 / CB)
        return ans


class BesselDate:
    """
    Attributes
    ----------
    year : float
        Decimal Besselian year

    jd : float
        Julian date

    mjd : float
        Modified Julian Date

    datespec
        Date specification as entered by the user

    """

    def __init__(self, datespec):
        self.datespec = datespec
        try:
            self.year = float(datespec)
        except ValueError:
            self.year = float(datespec[1:])

        self.jd = byear2jd(self.year)
        self.mjd = self.jd - MJD_0

    def __equals__(self, other):
        """All comparisons will be done based on `jd` attribute."""
        return self.jd == other.jd

    def __lt__(self, other):
        return self.jd < other.jd

    def __gt__(self, other):
        return self.jd > other.jd

    def __le__(self, other):
        return self.jd <= other.jd

    def __ge__(self, other):
        return self.jd >= other.jd

    def jyear(self):
        """
        Return the julian year using the already-converted
        julian date.

        Returns
        -------
        ans : float
            Decimal Julian year

        """
        ans = jd2jyear(self.jd)
        return ans