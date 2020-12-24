# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/bridgedb/geo.py
# Compiled at: 2015-11-05 10:40:17
__doc__ = '\nBoilerplate setup for GeoIP. GeoIP allows us to look up the country code\nassociated with an IP address. This is a "pure" python version which interacts\nwith the Maxmind GeoIP API (version 1). It requires, in Debian, the libgeoip-dev\nand geoip-database packages.\n'
import logging
from os.path import isfile
from ipaddr import IPv4Address, IPv6Address
GEOIP_DBFILE = '/usr/share/GeoIP/GeoIP.dat'
GEOIPv6_DBFILE = '/usr/share/GeoIP/GeoIPv6.dat'
try:
    if not (isfile(GEOIP_DBFILE) and isfile(GEOIPv6_DBFILE)):
        raise EnvironmentError('Could not find %r. On Debian-based systems, please install the geoip-database package.' % GEOIP_DBFILE)
    import pygeoip
    geoip = pygeoip.GeoIP(GEOIP_DBFILE, flags=pygeoip.MEMORY_CACHE)
    geoipv6 = pygeoip.GeoIP(GEOIPv6_DBFILE, flags=pygeoip.MEMORY_CACHE)
    logging.info('GeoIP databases loaded')
except Exception as err:
    logging.warn('Error while loading geoip module: %r' % err)
    geoip = None
    geoipv6 = None

def getCountryCode(ip):
    """Return the two-letter country code of a given IP address.

    :type ip: :class:`ipaddr.IPAddress`
    :param ip: An IPv4 OR IPv6 address.
    :rtype: ``None`` or str

    :returns: If the GeoIP databases are loaded, and the **ip** lookup is
        successful, then this returns a two-letter country code.  Otherwise,
        this returns ``None``.
    """
    addr = None
    version = None
    try:
        addr = ip.compressed
        version = ip.version
    except AttributeError as err:
        logging.warn('Wrong type passed to getCountryCode: %s' % str(err))
        return

    db = None
    if None in (geoip, geoipv6):
        logging.warn("GeoIP databases aren't loaded; can't look up country code")
        return
    else:
        if version == 4:
            db = geoip
        else:
            db = geoipv6
        countryCode = db.country_code_by_addr(addr)
        if countryCode:
            logging.debug('Looked up country code: %s' % countryCode)
            return countryCode
        logging.debug('Country code was not detected. IP: %s' % addr)
        return
        return