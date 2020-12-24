# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/constant2-project/constant2/pkg/superjson/pkg/dateutil/tz/tz.py
# Compiled at: 2018-12-19 11:16:59
"""
This module offers timezone implementations subclassing the abstract
:py:`datetime.tzinfo` type. There are classes to handle tzfile format files
(usually are in :file:`/etc/localtime`, :file:`/usr/share/zoneinfo`, etc), TZ
environment string (in all known formats), given ranges (with help from
relative deltas), local machine timezone, fixed offset timezone, and UTC
timezone.
"""
import datetime, struct, time, sys, os, bisect
from ..pkg.six import string_types
from ._common import tzname_in_python2, _tzinfo, _total_seconds
from ._common import tzrangebase, enfold
from ._common import _validate_fromutc_inputs
try:
    from .win import tzwin, tzwinlocal
except ImportError:
    tzwin = tzwinlocal = None

ZERO = datetime.timedelta(0)
EPOCH = datetime.datetime.utcfromtimestamp(0)
EPOCHORDINAL = EPOCH.toordinal()

class tzutc(datetime.tzinfo):
    """
    This is a tzinfo object that represents the UTC time zone.
    """

    def utcoffset(self, dt):
        return ZERO

    def dst(self, dt):
        return ZERO

    @tzname_in_python2
    def tzname(self, dt):
        return 'UTC'

    def is_ambiguous(self, dt):
        """
        Whether or not the "wall time" of a given datetime is ambiguous in this
        zone.

        :param dt:
            A :py:class:`datetime.datetime`, naive or time zone aware.

        :return:
            Returns ``True`` if ambiguous, ``False`` otherwise.

        .. versionadded:: 2.6.0
        """
        return False

    @_validate_fromutc_inputs
    def fromutc(self, dt):
        """
        Fast track version of fromutc() returns the original ``dt`` object for
        any valid :py:class:`datetime.datetime` object.
        """
        return dt

    def __eq__(self, other):
        if not isinstance(other, (tzutc, tzoffset)):
            return NotImplemented
        return isinstance(other, tzutc) or isinstance(other, tzoffset) and other._offset == ZERO

    __hash__ = None

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return '%s()' % self.__class__.__name__

    __reduce__ = object.__reduce__


class tzoffset(datetime.tzinfo):
    """
    A simple class for representing a fixed offset from UTC.

    :param name:
        The timezone name, to be returned when ``tzname()`` is called.

    :param offset:
        The time zone offset in seconds, or (since version 2.6.0, represented
        as a :py:class:`datetime.timedelta` object.
    """

    def __init__(self, name, offset):
        self._name = name
        try:
            offset = _total_seconds(offset)
        except (TypeError, AttributeError):
            pass

        self._offset = datetime.timedelta(seconds=offset)

    def utcoffset(self, dt):
        return self._offset

    def dst(self, dt):
        return ZERO

    @tzname_in_python2
    def tzname(self, dt):
        return self._name

    @_validate_fromutc_inputs
    def fromutc(self, dt):
        return dt + self._offset

    def is_ambiguous(self, dt):
        """
        Whether or not the "wall time" of a given datetime is ambiguous in this
        zone.

        :param dt:
            A :py:class:`datetime.datetime`, naive or time zone aware.

        :return:
            Returns ``True`` if ambiguous, ``False`` otherwise.

        .. versionadded:: 2.6.0
        """
        return False

    def __eq__(self, other):
        if not isinstance(other, tzoffset):
            return NotImplemented
        return self._offset == other._offset

    __hash__ = None

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return '%s(%s, %s)' % (self.__class__.__name__,
         repr(self._name),
         int(_total_seconds(self._offset)))

    __reduce__ = object.__reduce__


class tzlocal(_tzinfo):
    """
    A :class:`tzinfo` subclass built around the ``time`` timezone functions.
    """

    def __init__(self):
        super(tzlocal, self).__init__()
        self._std_offset = datetime.timedelta(seconds=-time.timezone)
        if time.daylight:
            self._dst_offset = datetime.timedelta(seconds=-time.altzone)
        else:
            self._dst_offset = self._std_offset
        self._dst_saved = self._dst_offset - self._std_offset
        self._hasdst = bool(self._dst_saved)

    def utcoffset(self, dt):
        if dt is None and self._hasdst:
            return
        else:
            if self._isdst(dt):
                return self._dst_offset
            else:
                return self._std_offset

            return

    def dst(self, dt):
        if dt is None and self._hasdst:
            return
        else:
            if self._isdst(dt):
                return self._dst_offset - self._std_offset
            else:
                return ZERO

            return

    @tzname_in_python2
    def tzname(self, dt):
        return time.tzname[self._isdst(dt)]

    def is_ambiguous(self, dt):
        """
        Whether or not the "wall time" of a given datetime is ambiguous in this
        zone.

        :param dt:
            A :py:class:`datetime.datetime`, naive or time zone aware.

        :return:
            Returns ``True`` if ambiguous, ``False`` otherwise.

        .. versionadded:: 2.6.0
        """
        naive_dst = self._naive_is_dst(dt)
        return not naive_dst and naive_dst != self._naive_is_dst(dt - self._dst_saved)

    def _naive_is_dst(self, dt):
        timestamp = _datetime_to_timestamp(dt)
        return time.localtime(timestamp + time.timezone).tm_isdst

    def _isdst(self, dt, fold_naive=True):
        if not self._hasdst:
            return False
        else:
            dstval = self._naive_is_dst(dt)
            fold = getattr(dt, 'fold', None)
            if self.is_ambiguous(dt):
                if fold is not None:
                    return not self._fold(dt)
                else:
                    return True

            return dstval

    def __eq__(self, other):
        if not isinstance(other, tzlocal):
            return NotImplemented
        return self._std_offset == other._std_offset and self._dst_offset == other._dst_offset

    __hash__ = None

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return '%s()' % self.__class__.__name__

    __reduce__ = object.__reduce__


class _ttinfo(object):
    __slots__ = [
     'offset', 'delta', 'isdst', 'abbr',
     'isstd', 'isgmt', 'dstoffset']

    def __init__(self):
        for attr in self.__slots__:
            setattr(self, attr, None)

        return

    def __repr__(self):
        l = []
        for attr in self.__slots__:
            value = getattr(self, attr)
            if value is not None:
                l.append('%s=%s' % (attr, repr(value)))

        return '%s(%s)' % (self.__class__.__name__, (', ').join(l))

    def __eq__(self, other):
        if not isinstance(other, _ttinfo):
            return NotImplemented
        return self.offset == other.offset and self.delta == other.delta and self.isdst == other.isdst and self.abbr == other.abbr and self.isstd == other.isstd and self.isgmt == other.isgmt and self.dstoffset == other.dstoffset

    __hash__ = None

    def __ne__(self, other):
        return not self == other

    def __getstate__(self):
        state = {}
        for name in self.__slots__:
            state[name] = getattr(self, name, None)

        return state

    def __setstate__(self, state):
        for name in self.__slots__:
            if name in state:
                setattr(self, name, state[name])


class _tzfile(object):
    """
    Lightweight class for holding the relevant transition and time zone
    information read from binary tzfiles.
    """
    attrs = [
     'trans_list', 'trans_list_utc', 'trans_idx', 'ttinfo_list',
     'ttinfo_std', 'ttinfo_dst', 'ttinfo_before', 'ttinfo_first']

    def __init__(self, **kwargs):
        for attr in self.attrs:
            setattr(self, attr, kwargs.get(attr, None))

        return


class tzfile(_tzinfo):
    """
    This is a ``tzinfo`` subclass thant allows one to use the ``tzfile(5)``
    format timezone files to extract current and historical zone information.

    :param fileobj:
        This can be an opened file stream or a file name that the time zone
        information can be read from.

    :param filename:
        This is an optional parameter specifying the source of the time zone
        information in the event that ``fileobj`` is a file object. If omitted
        and ``fileobj`` is a file stream, this parameter will be set either to
        ``fileobj``'s ``name`` attribute or to ``repr(fileobj)``.

    See `Sources for Time Zone and Daylight Saving Time Data
    <http://www.twinsun.com/tz/tz-link.htm>`_ for more information. Time zone
    files can be compiled from the `IANA Time Zone database files
    <https://www.iana.org/time-zones>`_ with the `zic time zone compiler
    <https://www.freebsd.org/cgi/man.cgi?query=zic&sektion=8>`_
    """

    def __init__(self, fileobj, filename=None):
        super(tzfile, self).__init__()
        file_opened_here = False
        if isinstance(fileobj, string_types):
            self._filename = fileobj
            fileobj = open(fileobj, 'rb')
            file_opened_here = True
        elif filename is not None:
            self._filename = filename
        elif hasattr(fileobj, 'name'):
            self._filename = fileobj.name
        else:
            self._filename = repr(fileobj)
        if fileobj is not None:
            if not file_opened_here:
                fileobj = _ContextWrapper(fileobj)
            with fileobj as (file_stream):
                tzobj = self._read_tzfile(file_stream)
            self._set_tzdata(tzobj)
        return

    def _set_tzdata(self, tzobj):
        """ Set the time zone data of this object from a _tzfile object """
        for attr in _tzfile.attrs:
            setattr(self, '_' + attr, getattr(tzobj, attr))

    def _read_tzfile(self, fileobj):
        out = _tzfile()
        if fileobj.read(4).decode() != 'TZif':
            raise ValueError('magic not found')
        fileobj.read(16)
        ttisgmtcnt, ttisstdcnt, leapcnt, timecnt, typecnt, charcnt = struct.unpack('>6l', fileobj.read(24))
        if timecnt:
            out.trans_list_utc = list(struct.unpack('>%dl' % timecnt, fileobj.read(timecnt * 4)))
        else:
            out.trans_list_utc = []
        if timecnt:
            out.trans_idx = struct.unpack('>%dB' % timecnt, fileobj.read(timecnt))
        else:
            out.trans_idx = []
        ttinfo = []
        for i in range(typecnt):
            ttinfo.append(struct.unpack('>lbb', fileobj.read(6)))

        abbr = fileobj.read(charcnt).decode()
        if leapcnt:
            fileobj.seek(leapcnt * 8, os.SEEK_CUR)
        if ttisstdcnt:
            isstd = struct.unpack('>%db' % ttisstdcnt, fileobj.read(ttisstdcnt))
        if ttisgmtcnt:
            isgmt = struct.unpack('>%db' % ttisgmtcnt, fileobj.read(ttisgmtcnt))
        out.ttinfo_list = []
        for i in range(typecnt):
            gmtoff, isdst, abbrind = ttinfo[i]
            gmtoff = 60 * ((gmtoff + 30) // 60)
            tti = _ttinfo()
            tti.offset = gmtoff
            tti.dstoffset = datetime.timedelta(0)
            tti.delta = datetime.timedelta(seconds=gmtoff)
            tti.isdst = isdst
            tti.abbr = abbr[abbrind:abbr.find('\x00', abbrind)]
            tti.isstd = ttisstdcnt > i and isstd[i] != 0
            tti.isgmt = ttisgmtcnt > i and isgmt[i] != 0
            out.ttinfo_list.append(tti)

        out.trans_idx = [ out.ttinfo_list[idx] for idx in out.trans_idx ]
        out.ttinfo_std = None
        out.ttinfo_dst = None
        out.ttinfo_before = None
        if out.ttinfo_list:
            if not out.trans_list_utc:
                out.ttinfo_std = out.ttinfo_first = out.ttinfo_list[0]
            else:
                for i in range(timecnt - 1, -1, -1):
                    tti = out.trans_idx[i]
                    if not out.ttinfo_std and not tti.isdst:
                        out.ttinfo_std = tti
                    elif not out.ttinfo_dst and tti.isdst:
                        out.ttinfo_dst = tti
                    if out.ttinfo_std and out.ttinfo_dst:
                        break
                else:
                    if out.ttinfo_dst and not out.ttinfo_std:
                        out.ttinfo_std = out.ttinfo_dst
                    for tti in out.ttinfo_list:
                        if not tti.isdst:
                            out.ttinfo_before = tti
                            break
                    else:
                        out.ttinfo_before = out.ttinfo_list[0]

        laststdoffset = None
        out.trans_list = []
        for i, tti in enumerate(out.trans_idx):
            if not tti.isdst:
                offset = tti.offset
                laststdoffset = offset
            else:
                if laststdoffset is not None:
                    tti.dstoffset = tti.offset - laststdoffset
                    out.trans_idx[i] = tti
                offset = laststdoffset or 0
            out.trans_list.append(out.trans_list_utc[i] + offset)

        laststdoffset = None
        for i in reversed(range(len(out.trans_idx))):
            tti = out.trans_idx[i]
            if tti.isdst:
                if not (tti.dstoffset or laststdoffset is None):
                    tti.dstoffset = tti.offset - laststdoffset
            else:
                laststdoffset = tti.offset
            if not isinstance(tti.dstoffset, datetime.timedelta):
                tti.dstoffset = datetime.timedelta(seconds=tti.dstoffset)
            out.trans_idx[i] = tti

        out.trans_idx = tuple(out.trans_idx)
        out.trans_list = tuple(out.trans_list)
        out.trans_list_utc = tuple(out.trans_list_utc)
        return out

    def _find_last_transition(self, dt, in_utc=False):
        if not self._trans_list:
            return None
        else:
            timestamp = _datetime_to_timestamp(dt)
            trans_list = self._trans_list_utc if in_utc else self._trans_list
            idx = bisect.bisect_right(trans_list, timestamp)
            return idx - 1

    def _get_ttinfo(self, idx):
        if idx is None or idx + 1 >= len(self._trans_list):
            return self._ttinfo_std
        else:
            if idx < 0:
                return self._ttinfo_before
            return self._trans_idx[idx]

    def _find_ttinfo(self, dt):
        idx = self._resolve_ambiguous_time(dt)
        return self._get_ttinfo(idx)

    def fromutc(self, dt):
        """
        The ``tzfile`` implementation of :py:func:`datetime.tzinfo.fromutc`.

        :param dt:
            A :py:class:`datetime.datetime` object.

        :raises TypeError:
            Raised if ``dt`` is not a :py:class:`datetime.datetime` object.

        :raises ValueError:
            Raised if this is called with a ``dt`` which does not have this
            ``tzinfo`` attached.

        :return:
            Returns a :py:class:`datetime.datetime` object representing the
            wall time in ``self``'s time zone.
        """
        if not isinstance(dt, datetime.datetime):
            raise TypeError('fromutc() requires a datetime argument')
        if dt.tzinfo is not self:
            raise ValueError('dt.tzinfo is not self')
        idx = self._find_last_transition(dt, in_utc=True)
        tti = self._get_ttinfo(idx)
        dt_out = dt + datetime.timedelta(seconds=tti.offset)
        fold = self.is_ambiguous(dt_out, idx=idx)
        return enfold(dt_out, fold=int(fold))

    def is_ambiguous(self, dt, idx=None):
        """
        Whether or not the "wall time" of a given datetime is ambiguous in this
        zone.

        :param dt:
            A :py:class:`datetime.datetime`, naive or time zone aware.

        :return:
            Returns ``True`` if ambiguous, ``False`` otherwise.

        .. versionadded:: 2.6.0
        """
        if idx is None:
            idx = self._find_last_transition(dt)
        timestamp = _datetime_to_timestamp(dt)
        tti = self._get_ttinfo(idx)
        if idx is None or idx <= 0:
            return False
        od = self._get_ttinfo(idx - 1).offset - tti.offset
        tt = self._trans_list[idx]
        return timestamp < tt + od

    def _resolve_ambiguous_time(self, dt):
        idx = self._find_last_transition(dt)
        _fold = self._fold(dt)
        if idx is None or idx == 0:
            return idx
        idx_offset = int(not _fold and self.is_ambiguous(dt, idx))
        return idx - idx_offset

    def utcoffset(self, dt):
        if dt is None:
            return
        else:
            if not self._ttinfo_std:
                return ZERO
            return self._find_ttinfo(dt).delta

    def dst(self, dt):
        if dt is None:
            return
        else:
            if not self._ttinfo_dst:
                return ZERO
            tti = self._find_ttinfo(dt)
            if not tti.isdst:
                return ZERO
            return tti.dstoffset

    @tzname_in_python2
    def tzname(self, dt):
        if not self._ttinfo_std or dt is None:
            return
        return self._find_ttinfo(dt).abbr

    def __eq__(self, other):
        if not isinstance(other, tzfile):
            return NotImplemented
        return self._trans_list == other._trans_list and self._trans_idx == other._trans_idx and self._ttinfo_list == other._ttinfo_list

    __hash__ = None

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, repr(self._filename))

    def __reduce__(self):
        return self.__reduce_ex__(None)

    def __reduce_ex__(self, protocol):
        return (
         self.__class__, (None, self._filename), self.__dict__)


class tzrange(tzrangebase):
    """
    The ``tzrange`` object is a time zone specified by a set of offsets and
    abbreviations, equivalent to the way the ``TZ`` variable can be specified
    in POSIX-like systems, but using Python delta objects to specify DST
    start, end and offsets.

    :param stdabbr:
        The abbreviation for standard time (e.g. ``'EST'``).

    :param stdoffset:
        An integer or :class:`datetime.timedelta` object or equivalent
        specifying the base offset from UTC.

        If unspecified, +00:00 is used.

    :param dstabbr:
        The abbreviation for DST / "Summer" time (e.g. ``'EDT'``).

        If specified, with no other DST information, DST is assumed to occur
        and the default behavior or ``dstoffset``, ``start`` and ``end`` is
        used. If unspecified and no other DST information is specified, it
        is assumed that this zone has no DST.

        If this is unspecified and other DST information is *is* specified,
        DST occurs in the zone but the time zone abbreviation is left
        unchanged.

    :param dstoffset:
        A an integer or :class:`datetime.timedelta` object or equivalent
        specifying the UTC offset during DST. If unspecified and any other DST
        information is specified, it is assumed to be the STD offset +1 hour.

    :param start:
        A :class:`relativedelta.relativedelta` object or equivalent specifying
        the time and time of year that daylight savings time starts. To specify,
        for example, that DST starts at 2AM on the 2nd Sunday in March, pass:

            ``relativedelta(hours=2, month=3, day=1, weekday=SU(+2))``

        If unspecified and any other DST information is specified, the default
        value is 2 AM on the first Sunday in April.

    :param end:
        A :class:`relativedelta.relativedelta` object or equivalent representing
        the time and time of year that daylight savings time ends, with the
        same specification method as in ``start``. One note is that this should
        point to the first time in the *standard* zone, so if a transition
        occurs at 2AM in the DST zone and the clocks are set back 1 hour to 1AM,
        set the `hours` parameter to +1.

    **Examples:**

    .. testsetup:: tzrange

        from dateutil.tz import tzrange, tzstr

    .. doctest:: tzrange

        >>> tzstr('EST5EDT') == tzrange("EST", -18000, "EDT")
        True

        >>> from dateutil.relativedelta import *
        >>> range1 = tzrange("EST", -18000, "EDT")
        >>> range2 = tzrange("EST", -18000, "EDT", -14400,
        ...                  relativedelta(hours=+2, month=4, day=1,
        ...                                weekday=SU(+1)),
        ...                  relativedelta(hours=+1, month=10, day=31,
        ...                                weekday=SU(-1)))
        >>> tzstr('EST5EDT') == range1 == range2
        True

    """

    def __init__(self, stdabbr, stdoffset=None, dstabbr=None, dstoffset=None, start=None, end=None):
        global relativedelta
        from dateutil import relativedelta
        self._std_abbr = stdabbr
        self._dst_abbr = dstabbr
        try:
            stdoffset = _total_seconds(stdoffset)
        except (TypeError, AttributeError):
            pass

        try:
            dstoffset = _total_seconds(dstoffset)
        except (TypeError, AttributeError):
            pass

        if stdoffset is not None:
            self._std_offset = datetime.timedelta(seconds=stdoffset)
        else:
            self._std_offset = ZERO
        if dstoffset is not None:
            self._dst_offset = datetime.timedelta(seconds=dstoffset)
        elif dstabbr and stdoffset is not None:
            self._dst_offset = self._std_offset + datetime.timedelta(hours=+1)
        else:
            self._dst_offset = ZERO
        if dstabbr and start is None:
            self._start_delta = relativedelta.relativedelta(hours=+2, month=4, day=1, weekday=relativedelta.SU(+1))
        else:
            self._start_delta = start
        if dstabbr and end is None:
            self._end_delta = relativedelta.relativedelta(hours=+1, month=10, day=31, weekday=relativedelta.SU(-1))
        else:
            self._end_delta = end
        self._dst_base_offset_ = self._dst_offset - self._std_offset
        self.hasdst = bool(self._start_delta)
        return

    def transitions(self, year):
        """
        For a given year, get the DST on and off transition times, expressed
        always on the standard time side. For zones with no transitions, this
        function returns ``None``.

        :param year:
            The year whose transitions you would like to query.

        :return:
            Returns a :class:`tuple` of :class:`datetime.datetime` objects,
            ``(dston, dstoff)`` for zones with an annual DST transition, or
            ``None`` for fixed offset zones.
        """
        if not self.hasdst:
            return None
        else:
            base_year = datetime.datetime(year, 1, 1)
            start = base_year + self._start_delta
            end = base_year + self._end_delta
            return (
             start, end)

    def __eq__(self, other):
        if not isinstance(other, tzrange):
            return NotImplemented
        return self._std_abbr == other._std_abbr and self._dst_abbr == other._dst_abbr and self._std_offset == other._std_offset and self._dst_offset == other._dst_offset and self._start_delta == other._start_delta and self._end_delta == other._end_delta

    @property
    def _dst_base_offset(self):
        return self._dst_base_offset_


class tzstr(tzrange):
    """
    ``tzstr`` objects are time zone objects specified by a time-zone string as
    it would be passed to a ``TZ`` variable on POSIX-style systems (see
    the `GNU C Library: TZ Variable`_ for more details).

    There is one notable exception, which is that POSIX-style time zones use an
    inverted offset format, so normally ``GMT+3`` would be parsed as an offset
    3 hours *behind* GMT. The ``tzstr`` time zone object will parse this as an
    offset 3 hours *ahead* of GMT. If you would like to maintain the POSIX
    behavior, pass a ``True`` value to ``posix_offset``.

    The :class:`tzrange` object provides the same functionality, but is
    specified using :class:`relativedelta.relativedelta` objects. rather than
    strings.

    :param s:
        A time zone string in ``TZ`` variable format. This can be a
        :class:`bytes` (2.x: :class:`str`), :class:`str` (2.x: :class:`unicode`)
        or a stream emitting unicode characters (e.g. :class:`StringIO`).

    :param posix_offset:
        Optional. If set to ``True``, interpret strings such as ``GMT+3`` or
        ``UTC+3`` as being 3 hours *behind* UTC rather than ahead, per the
        POSIX standard.

    .. _`GNU C Library: TZ Variable`:
        https://www.gnu.org/software/libc/manual/html_node/TZ-Variable.html
    """

    def __init__(self, s, posix_offset=False):
        global parser
        from dateutil import parser
        self._s = s
        res = parser._parsetz(s)
        if res is None:
            raise ValueError('unknown string format')
        if res.stdabbr in ('GMT', 'UTC') and not posix_offset:
            res.stdoffset *= -1
        tzrange.__init__(self, res.stdabbr, res.stdoffset, res.dstabbr, res.dstoffset, start=False, end=False)
        if not res.dstabbr:
            self._start_delta = None
            self._end_delta = None
        else:
            self._start_delta = self._delta(res.start)
            if self._start_delta:
                self._end_delta = self._delta(res.end, isend=1)
        self.hasdst = bool(self._start_delta)
        return

    def _delta(self, x, isend=0):
        from dateutil import relativedelta
        kwargs = {}
        if x.month is not None:
            kwargs['month'] = x.month
            if x.weekday is not None:
                kwargs['weekday'] = relativedelta.weekday(x.weekday, x.week)
                if x.week > 0:
                    kwargs['day'] = 1
                else:
                    kwargs['day'] = 31
            elif x.day:
                kwargs['day'] = x.day
        elif x.yday is not None:
            kwargs['yearday'] = x.yday
        elif x.jyday is not None:
            kwargs['nlyearday'] = x.jyday
        if not kwargs:
            if not isend:
                kwargs['month'] = 4
                kwargs['day'] = 1
                kwargs['weekday'] = relativedelta.SU(+1)
            else:
                kwargs['month'] = 10
                kwargs['day'] = 31
                kwargs['weekday'] = relativedelta.SU(-1)
        if x.time is not None:
            kwargs['seconds'] = x.time
        else:
            kwargs['seconds'] = 7200
        if isend:
            delta = self._dst_offset - self._std_offset
            kwargs['seconds'] -= delta.seconds + delta.days * 86400
        return relativedelta.relativedelta(**kwargs)

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, repr(self._s))


class _tzicalvtzcomp(object):

    def __init__(self, tzoffsetfrom, tzoffsetto, isdst, tzname=None, rrule=None):
        self.tzoffsetfrom = datetime.timedelta(seconds=tzoffsetfrom)
        self.tzoffsetto = datetime.timedelta(seconds=tzoffsetto)
        self.tzoffsetdiff = self.tzoffsetto - self.tzoffsetfrom
        self.isdst = isdst
        self.tzname = tzname
        self.rrule = rrule


class _tzicalvtz(_tzinfo):

    def __init__(self, tzid, comps=[]):
        super(_tzicalvtz, self).__init__()
        self._tzid = tzid
        self._comps = comps
        self._cachedate = []
        self._cachecomp = []

    def _find_comp(self, dt):
        if len(self._comps) == 1:
            return self._comps[0]
        else:
            dt = dt.replace(tzinfo=None)
            try:
                return self._cachecomp[self._cachedate.index((dt, self._fold(dt)))]
            except ValueError:
                pass

            lastcompdt = None
            lastcomp = None
            for comp in self._comps:
                compdt = self._find_compdt(comp, dt)
                if compdt and (not lastcompdt or lastcompdt < compdt):
                    lastcompdt = compdt
                    lastcomp = comp

            if not lastcomp:
                for comp in self._comps:
                    if not comp.isdst:
                        lastcomp = comp
                        break
                else:
                    lastcomp = comp[0]

            self._cachedate.insert(0, (dt, self._fold(dt)))
            self._cachecomp.insert(0, lastcomp)
            if len(self._cachedate) > 10:
                self._cachedate.pop()
                self._cachecomp.pop()
            return lastcomp

    def _find_compdt(self, comp, dt):
        if comp.tzoffsetdiff < ZERO and self._fold(dt):
            dt -= comp.tzoffsetdiff
        compdt = comp.rrule.before(dt, inc=True)
        return compdt

    def utcoffset(self, dt):
        if dt is None:
            return
        else:
            return self._find_comp(dt).tzoffsetto

    def dst(self, dt):
        comp = self._find_comp(dt)
        if comp.isdst:
            return comp.tzoffsetdiff
        else:
            return ZERO

    @tzname_in_python2
    def tzname(self, dt):
        return self._find_comp(dt).tzname

    def __repr__(self):
        return '<tzicalvtz %s>' % repr(self._tzid)

    __reduce__ = object.__reduce__


class tzical(object):
    """
    This object is designed to parse an iCalendar-style ``VTIMEZONE`` structure
    as set out in `RFC 2445`_ Section 4.6.5 into one or more `tzinfo` objects.

    :param `fileobj`:
        A file or stream in iCalendar format, which should be UTF-8 encoded
        with CRLF endings.

    .. _`RFC 2445`: https://www.ietf.org/rfc/rfc2445.txt
    """

    def __init__(self, fileobj):
        global rrule
        from dateutil import rrule
        if isinstance(fileobj, string_types):
            self._s = fileobj
            fileobj = open(fileobj, 'r')
        else:
            self._s = getattr(fileobj, 'name', repr(fileobj))
            fileobj = _ContextWrapper(fileobj)
        self._vtz = {}
        with fileobj as (fobj):
            self._parse_rfc(fobj.read())

    def keys(self):
        """
        Retrieves the available time zones as a list.
        """
        return list(self._vtz.keys())

    def get(self, tzid=None):
        """
        Retrieve a :py:class:`datetime.tzinfo` object by its ``tzid``.

        :param tzid:
            If there is exactly one time zone available, omitting ``tzid``
            or passing :py:const:`None` value returns it. Otherwise a valid
            key (which can be retrieved from :func:`keys`) is required.

        :raises ValueError:
            Raised if ``tzid`` is not specified but there are either more
            or fewer than 1 zone defined.

        :returns:
            Returns either a :py:class:`datetime.tzinfo` object representing
            the relevant time zone or :py:const:`None` if the ``tzid`` was
            not found.
        """
        if tzid is None:
            if len(self._vtz) == 0:
                raise ValueError('no timezones defined')
            elif len(self._vtz) > 1:
                raise ValueError('more than one timezone available')
            tzid = next(iter(self._vtz))
        return self._vtz.get(tzid)

    def _parse_offset(self, s):
        s = s.strip()
        if not s:
            raise ValueError('empty offset')
        if s[0] in ('+', '-'):
            signal = (
             -1, +1)[(s[0] == '+')]
            s = s[1:]
        else:
            signal = +1
        if len(s) == 4:
            return (int(s[:2]) * 3600 + int(s[2:]) * 60) * signal
        if len(s) == 6:
            return (int(s[:2]) * 3600 + int(s[2:4]) * 60 + int(s[4:])) * signal
        raise ValueError('invalid offset: ' + s)

    def _parse_rfc(self, s):
        lines = s.splitlines()
        if not lines:
            raise ValueError('empty string')
        i = 0
        while i < len(lines):
            line = lines[i].rstrip()
            if not line:
                del lines[i]
            elif i > 0 and line[0] == ' ':
                lines[(i - 1)] += line[1:]
                del lines[i]
            else:
                i += 1

        tzid = None
        comps = []
        invtz = False
        comptype = None
        for line in lines:
            if not line:
                continue
            name, value = line.split(':', 1)
            parms = name.split(';')
            if not parms:
                raise ValueError('empty property name')
            name = parms[0].upper()
            parms = parms[1:]
            if invtz:
                if name == 'BEGIN':
                    if value in ('STANDARD', 'DAYLIGHT'):
                        pass
                    else:
                        raise ValueError('unknown component: ' + value)
                    comptype = value
                    founddtstart = False
                    tzoffsetfrom = None
                    tzoffsetto = None
                    rrulelines = []
                    tzname = None
                elif name == 'END':
                    if value == 'VTIMEZONE':
                        if comptype:
                            raise ValueError('component not closed: ' + comptype)
                        if not tzid:
                            raise ValueError('mandatory TZID not found')
                        if not comps:
                            raise ValueError('at least one component is needed')
                        self._vtz[tzid] = _tzicalvtz(tzid, comps)
                        invtz = False
                    elif value == comptype:
                        if not founddtstart:
                            raise ValueError('mandatory DTSTART not found')
                        if tzoffsetfrom is None:
                            raise ValueError('mandatory TZOFFSETFROM not found')
                        if tzoffsetto is None:
                            raise ValueError('mandatory TZOFFSETFROM not found')
                        rr = None
                        if rrulelines:
                            rr = rrule.rrulestr(('\n').join(rrulelines), compatible=True, ignoretz=True, cache=True)
                        comp = _tzicalvtzcomp(tzoffsetfrom, tzoffsetto, comptype == 'DAYLIGHT', tzname, rr)
                        comps.append(comp)
                        comptype = None
                    else:
                        raise ValueError('invalid component end: ' + value)
                elif comptype:
                    if name == 'DTSTART':
                        rrulelines.append(line)
                        founddtstart = True
                    elif name in ('RRULE', 'RDATE', 'EXRULE', 'EXDATE'):
                        rrulelines.append(line)
                    elif name == 'TZOFFSETFROM':
                        if parms:
                            raise ValueError('unsupported %s parm: %s ' % (name, parms[0]))
                        tzoffsetfrom = self._parse_offset(value)
                    elif name == 'TZOFFSETTO':
                        if parms:
                            raise ValueError('unsupported TZOFFSETTO parm: ' + parms[0])
                        tzoffsetto = self._parse_offset(value)
                    elif name == 'TZNAME':
                        if parms:
                            raise ValueError('unsupported TZNAME parm: ' + parms[0])
                        tzname = value
                    elif name == 'COMMENT':
                        pass
                    else:
                        raise ValueError('unsupported property: ' + name)
                elif name == 'TZID':
                    if parms:
                        raise ValueError('unsupported TZID parm: ' + parms[0])
                    tzid = value
                elif name in ('TZURL', 'LAST-MODIFIED', 'COMMENT'):
                    pass
                else:
                    raise ValueError('unsupported property: ' + name)
            elif name == 'BEGIN' and value == 'VTIMEZONE':
                tzid = None
                comps = []
                invtz = True

        return

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, repr(self._s))


if sys.platform != 'win32':
    TZFILES = [
     '/etc/localtime', 'localtime']
    TZPATHS = ['/usr/share/zoneinfo',
     '/usr/lib/zoneinfo',
     '/usr/share/lib/zoneinfo',
     '/etc/zoneinfo']
else:
    TZFILES = []
    TZPATHS = []

def gettz(name=None):
    tz = None
    if not name:
        try:
            name = os.environ['TZ']
        except KeyError:
            pass

    if name is None or name == ':':
        for filepath in TZFILES:
            if not os.path.isabs(filepath):
                filename = filepath
                for path in TZPATHS:
                    filepath = os.path.join(path, filename)
                    if os.path.isfile(filepath):
                        break
                else:
                    continue

            if os.path.isfile(filepath):
                try:
                    tz = tzfile(filepath)
                    break
                except (IOError, OSError, ValueError):
                    pass

        else:
            tz = tzlocal()

    else:
        if name.startswith(':'):
            name = name[:-1]
        if os.path.isabs(name):
            if os.path.isfile(name):
                tz = tzfile(name)
            else:
                tz = None
        else:
            for path in TZPATHS:
                filepath = os.path.join(path, name)
                if not os.path.isfile(filepath):
                    filepath = filepath.replace(' ', '_')
                    if not os.path.isfile(filepath):
                        continue
                try:
                    tz = tzfile(filepath)
                    break
                except (IOError, OSError, ValueError):
                    pass

            else:
                tz = None
                if tzwin is not None:
                    try:
                        tz = tzwin(name)
                    except WindowsError:
                        tz = None

                if not tz:
                    from dateutil.zoneinfo import get_zonefile_instance
                    tz = get_zonefile_instance().get(name)

            if not tz:
                for c in name:
                    if c in '0123456789':
                        try:
                            tz = tzstr(name)
                        except ValueError:
                            pass

                        break
                else:
                    if name in ('GMT', 'UTC'):
                        tz = tzutc()
                    elif name in time.tzname:
                        tz = tzlocal()
    return tz


def datetime_exists(dt, tz=None):
    """
    Given a datetime and a time zone, determine whether or not a given datetime
    would fall in a gap.

    :param dt:
        A :class:`datetime.datetime` (whose time zone will be ignored if ``tz``
        is provided.)

    :param tz:
        A :class:`datetime.tzinfo` with support for the ``fold`` attribute. If
        ``None`` or not provided, the datetime's own time zone will be used.

    :return:
        Returns a boolean value whether or not the "wall time" exists in ``tz``.
    """
    if tz is None:
        if dt.tzinfo is None:
            raise ValueError('Datetime is naive and no time zone provided.')
        tz = dt.tzinfo
    dt = dt.replace(tzinfo=None)
    dt_rt = dt.replace(tzinfo=tz).astimezone(tzutc()).astimezone(tz)
    dt_rt = dt_rt.replace(tzinfo=None)
    return dt == dt_rt


def datetime_ambiguous(dt, tz=None):
    """
    Given a datetime and a time zone, determine whether or not a given datetime
    is ambiguous (i.e if there are two times differentiated only by their DST
    status).

    :param dt:
        A :class:`datetime.datetime` (whose time zone will be ignored if ``tz``
        is provided.)

    :param tz:
        A :class:`datetime.tzinfo` with support for the ``fold`` attribute. If
        ``None`` or not provided, the datetime's own time zone will be used.

    :return:
        Returns a boolean value whether or not the "wall time" is ambiguous in
        ``tz``.

    .. versionadded:: 2.6.0
    """
    if tz is None:
        if dt.tzinfo is None:
            raise ValueError('Datetime is naive and no time zone provided.')
        tz = dt.tzinfo
    is_ambiguous_fn = getattr(tz, 'is_ambiguous', None)
    if is_ambiguous_fn is not None:
        try:
            return tz.is_ambiguous(dt)
        except:
            pass

    dt = dt.replace(tzinfo=tz)
    wall_0 = enfold(dt, fold=0)
    wall_1 = enfold(dt, fold=1)
    same_offset = wall_0.utcoffset() == wall_1.utcoffset()
    same_dst = wall_0.dst() == wall_1.dst()
    return not (same_offset and same_dst)


def _datetime_to_timestamp(dt):
    """
    Convert a :class:`datetime.datetime` object to an epoch timestamp in seconds
    since January 1, 1970, ignoring the time zone.
    """
    return _total_seconds(dt.replace(tzinfo=None) - EPOCH)


class _ContextWrapper(object):
    """
    Class for wrapping contexts so that they are passed through in a
    with statement.
    """

    def __init__(self, context):
        self.context = context

    def __enter__(self):
        return self.context

    def __exit__(*args, **kwargs):
        pass