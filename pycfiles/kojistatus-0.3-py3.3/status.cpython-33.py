# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kojistatus/status.py
# Compiled at: 2017-01-27 08:21:42
# Size of source mod 2**32: 1170 bytes
import re, requests
RE_ID = re.compile('<td>(\\d+)</td>', re.ASCII)
RE_STATUS = re.compile('<img class="stateimg" src="/koji-static/images/\\w+.png" title="(\\w+)" alt="\\w+"/>', re.ASCII)

def status(username=None, *, kojiurl=None, session=None):
    """
    For given username, return the last builds with status information.
    Returns an iterable of 2-tuples, sorted descending.

    Only the first page with maximum 50 results is fetched.
    """
    kojiurl = kojiurl or 'https://koji.fedoraproject.org/'
    session = session or requests.Session()
    url = '{}koji/tasks'.format(kojiurl)
    params = {'state': 'all', 
     'view': 'toplevel'}
    if username:
        params['owner'] = username
    response = session.get(url, params=params)
    response.raise_for_status()
    return _parse(response.text)


def _parse(html):
    """
    Parses the given HTML source using regular expressions (I know :P)
    Returns status information for status()
    """
    ids = RE_ID.findall(html)
    statuses = RE_STATUS.findall(html)
    for idx, status in enumerate(statuses):
        yield (
         int(ids[idx]), status)