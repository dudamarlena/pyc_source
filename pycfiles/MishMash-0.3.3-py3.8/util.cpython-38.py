# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mishmash/util.py
# Compiled at: 2020-03-01 00:33:55
# Size of source mod 2**32: 2950 bytes
import os, argparse
from urllib.parse import urlparse
from eyed3.utils import datePicker
NAME_PREFIXES = [
 'the ', 'los ', 'la ', 'el ']

def splitNameByPrefix(s):
    s_lower = s.lower()
    for prefix in NAME_PREFIXES:
        if s_lower.startswith(prefix):
            return (
             s[len(prefix):], s[0:len(prefix.rstrip())])
        return (
         s, None)


def sortByDate(things, prefer_recording_date=False):

    def _sortkey(a):
        return datePicker(a, prefer_recording_date=prefer_recording_date) or 0

    return sorted(things, key=_sortkey)


def normalizeCountry(country_str, target='iso3c'):
    """Return a normalized name/code for country in `country_str`.
    The input can be a code or name, the `target` determines output value.
    3 character ISO code is the default (iso3c), or 'iso2c'; otherwise then formal name is returned.

    Raises ``ValueError`` if the country is unrecognized.
    """
    from iso3166 import countries
    iso2 = 'iso2c'
    iso3 = 'iso3c'
    if country_str is None:
        return ''
    if country_str.lower() == 'united states':
        country_str += ' of america'
    try:
        cc = countries.get(country_str)
    except KeyError:
        raise ValueError(f"Country not found: {country_str}")
    else:
        if target == iso3:
            return cc.alpha3
        if target == iso2:
            return cc.alpha2
        return cc.name


def commonDirectoryPrefix(*args):
    return os.path.commonprefix(args).rpartition(os.path.sep)[0]


def mostCommonItem(lst):
    """Choose the most common item from the list, or the first item if all
    items are unique."""
    lst = [l for l in lst if l]
    if lst:
        return max((set(lst)), key=(lst.count))
    return


def safeDbUrl(db_url):
    """Obfuscates password from a database URL."""
    url = urlparse(db_url)
    if url.password:
        return db_url.replace(url.password, '****')
    return db_url


def addLibraryArguments(cli: argparse.ArgumentParser, nargs):
    """Add library options (-L/--library) with specific `nargs`."""
    from .orm import MAIN_LIB_NAME
    if nargs is not None:
        required = nargs in ('+', 1)
        if nargs not in ('?', 1):
            action, default, dest = 'append', [] if not required else [MAIN_LIB_NAME], 'libs'
        else:
            action, default, dest = 'store', None if required else MAIN_LIB_NAME, 'lib'
        cli.add_argument('-L', '--library', dest=dest, required=required, action=action,
          metavar='LIB_NAME',
          default=default,
          help='Specify a library.')