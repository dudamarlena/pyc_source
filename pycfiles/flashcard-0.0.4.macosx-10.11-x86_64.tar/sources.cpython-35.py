# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sotetsuk/.pyenv/versions/3.5.1/lib/python3.5/site-packages/flashcard/sources.py
# Compiled at: 2016-05-13 01:20:48
# Size of source mod 2**32: 2082 bytes
import re, requests
from urllib.parse import urlparse
from typing import Tuple
from flashcard.property import Flashcard

def fetch_google_spreadsheet(url: str, fmt='tsv') -> Flashcard:
    """ Obtain flashcard data from Google Speradsheet

    :param url:
    :param fmt:
    :return:
    """
    assert url.startswith('https://docs.google.com/spreadsheets/'), 'URL should start with https://docs.google.com/spreadsheets/'
    if not fmt == 'tsv':
        assert fmt == 'csv'
    delimiter = ''
    if fmt == 'tsv':
        delimiter = '\t'
    if fmt == 'csv':
        delimiter = ','
    _id, gid = _parse_google_spreadsheet(url)
    downloadable_url = _generate_downloadable_url(_id, gid, fmt)
    r = requests.get(downloadable_url)
    r.encoding = 'utf-8'
    ret = []
    for row in r.text.split('\n'):
        ret.append([e.strip('\r').strip() for e in row.split(delimiter)])

    return ret


def _parse_google_spreadsheet(url: str) -> Tuple[(str, str)]:
    """ Parse id and gid from url of Google Spreadsheet

    :param url:
    :return:
    """
    o = urlparse(url)
    path = o.path
    fragment = o.fragment
    _id = None
    r = re.compile('/spreadsheets/d/')
    _id = r.sub('', path)
    r = re.compile('edit.*')
    _id = r.sub('', _id)
    _id = _id.strip('/')
    gid = None
    if 'gid' in fragment:
        r = re.compile('gid=[0-9]*')
        gid = r.match(fragment).group().lstrip('gid=')
    return (_id, gid)


def _generate_downloadable_url(_id: str, gid: str, fmt='tsv') -> str:
    """

    :param _id:
    :param gid:
    :return:
    """
    assert _id is not None and _id != '', 'id is not set'
    url = 'https://docs.google.com/spreadsheets/d/{}/export?'.format(_id)
    if gid is None or gid == '':
        gid = '0'
    url += 'gid={}&format={}'.format(gid, fmt)
    return url