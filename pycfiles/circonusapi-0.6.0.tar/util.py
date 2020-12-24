# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/circonus/util.py
# Compiled at: 2015-01-30 15:28:02
__doc__ = '\n\ncirconus.util\n~~~~~~~~~~~~~\n\nUtility functions that other modules depend upon.\n\n'
from calendar import timegm
from posixpath import sep as pathsep
from colour import Color

def datetime_to_int(dt):
    """Convert date and time to seconds since the epoch.

    :param datetime.datetime dt: The date and time to convert.
    :rtype: :py:class:`int`

    ``dt`` is expected to have been created for the UTC date and time, e.g., with
    :py:meth:`datetime.datetime.utcnow`.  It is converted to seconds since the epoch with
    :py:func:`calendar.timegm` to respect UTC.

    """
    return int(timegm(dt.timetuple()))


def get_check_id_from_cid(cid):
    """Get a check id integer from ``cid``.

    :param str cid: The check id.
    :rtype: :py:class:`int`

    """
    return int(cid.strip(pathsep).rpartition(pathsep)[(-1)])


def get_resource_from_cid(cid):
    """Get the resource name from ``cid``.

    :param str cid: The check id.
    :rtype: :py:class:`str`

    """
    return cid.strip(pathsep).split(pathsep)[0]


def colors(items):
    """Create a generator which returns colors for each item in ``items``.

    :param list items: The list to generate colors for.
    :rtype: generator(`colour.Color <https://pypi.python.org/pypi/colour>`_)

    """
    if len(items) < 2:
        c = (c for c in (Color('red'),))
    else:
        color_from = Color('red')
        color_to = Color('green')
        c = color_from.range_to(color_to, len(items))
    return c