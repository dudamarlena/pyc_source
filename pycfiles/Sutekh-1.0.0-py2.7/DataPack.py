# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/io/DataPack.py
# Compiled at: 2019-12-11 16:37:58
"""Provide tools for locating and extracting data pack ZIP files."""
import datetime, json, urllib2, urlparse, socket
from sutekh.base.io.UrlOps import urlopen_with_timeout
DOC_URL = 'https://bitbucket.org/hodgestar/sutekh-datapack/raw/master/index.json'

def parse_datapack_date(sDate):
    """Parse a datapack's ISO format date entry into a datetime object."""
    return datetime.datetime.strptime(sDate, '%Y-%m-%dT%H:%M:%S.%f')


def find_all_data_packs(sTag, sDocUrl=DOC_URL, fErrorHandler=None):
    """Read the data pack index and return all datapacks listed for the
    given tag.

    Returns empty lists if no file could be found for the given tag.

    The index is a JSON file with the following structure:

    {
    "datapacks": [
        {
            "description": "Zip file of starter decks ...",
            "file": "Starters/Starters_SW_to_HttB_and_Others.zip",
            "sha256": "4f1867568127b12276efbe9bafa261f4ad86741ff09549a48f6...",
            "tag": "starters",
            "updated_at": "2014-07-04T18:54:31.802636"
        },
        ...
    ],
    "format": "sutekh-datapack",
    "format-version": "1.0"
    }
    """
    oFile = urlopen_with_timeout(sDocUrl, fErrorHandler)
    if not oFile:
        return (None, None, None)
    else:
        try:
            dIndex = json.load(oFile)
        except (urllib2.URLError, socket.timeout, ValueError) as oExp:
            if fErrorHandler:
                fErrorHandler(oExp)
                return (None, None, None)
            raise

        aZipUrls = []
        aHashes = []
        aDates = []
        for dPack in dIndex['datapacks']:
            if dPack.get('tag') != sTag:
                continue
            aZipUrls.append(urlparse.urljoin(sDocUrl, dPack['file']))
            aHashes.append(dPack['sha256'])
            oDate = parse_datapack_date(dPack['updated_at'])
            aDates.append(oDate.strftime('%Y-%m-%d'))

        return (aZipUrls, aDates, aHashes)


def find_data_pack(sTag, sDocUrl=DOC_URL, fErrorHandler=None):
    """Find a single data pack for a tag. Return url and hash, if appropriate.

    Return None if no match is found.

    See find_all_data_packs for details on the sutekh datapack format.

    If multiple datapack are found, return the last."""
    aZipUrls, _aSkip, aHashes = find_all_data_packs(sTag, sDocUrl=sDocUrl, fErrorHandler=fErrorHandler)
    if not aZipUrls:
        return (None, None)
    else:
        if not aHashes:
            return (
             aZipUrls[(-1)], None)
        return (
         aZipUrls[(-1)], aHashes[(-1)])