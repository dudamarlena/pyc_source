# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jwql/tests/test_api_views.py
# Compiled at: 2019-08-26 11:08:03
# Size of source mod 2**32: 3284 bytes
"""Tests for the ``api_views`` module in the ``jwql`` web application.

Authors
-------

    - Matthew Bourque

Use
---

    These tests can be run via the command line (omit the -s to
    suppress verbose output to stdout):

    ::

        pytest -s test_api_views.py
"""
import http, json, os
from urllib import request, error
import pytest
from jwql.utils.utils import get_base_url
from jwql.utils.constants import JWST_INSTRUMENT_NAMES
ON_JENKINS = '/home/jenkins' in os.path.expanduser('~')
try:
    url = request.urlopen('http://127.0.0.1:8000')
    LOCAL_SERVER = True
except error.URLError:
    LOCAL_SERVER = False

urls = []
urls.append('api/proposals/')
for instrument in JWST_INSTRUMENT_NAMES:
    urls.append('api/{}/proposals/'.format(instrument))
    urls.append('api/{}/preview_images/'.format(instrument))
    urls.append('api/{}/thumbnails/'.format(instrument))

proposals = [
 '86700',
 '98012',
 '93025',
 '00308',
 '308',
 '96213']
for proposal in proposals:
    urls.append('api/{}/filenames/'.format(proposal))
    urls.append('api/{}/preview_images/'.format(proposal))
    urls.append('api/{}/thumbnails/'.format(proposal))

rootnames = [
 'jw86600007001_02101_00001_guider2',
 'jw98012001001_02102_00001_mirimage',
 'jw93025001001_02102_00001_nrca2',
 'jw00308001001_02103_00001_nis',
 'jw96213001001_02101_00001_nrs1']
for rootname in rootnames:
    urls.append('api/{}/filenames/'.format(rootname))
    urls.append('api/{}/preview_images/'.format(rootname))
    urls.append('api/{}/thumbnails/'.format(rootname))

@pytest.mark.parametrize('url', urls)
def test_api_views(url):
    """Test to see if the given ``url`` returns a populated JSON object

    Parameters
    ----------
    url : str
        The url to the api view of interest (e.g.
        ``http://127.0.0.1:8000/api/86700/filenames/'``).
    """
    if not ON_JENKINS:
        base_url = get_base_url()
    else:
        base_url = 'https://dljwql.stsci.edu'
    if base_url == 'http://127.0.0.1:8000':
        if not LOCAL_SERVER:
            pytest.skip('Local server not running')
    url = '{}/{}'.format(base_url, url)
    data_type = url.split('/')[(-2)]
    try:
        url = request.urlopen(url)
    except error.HTTPError as e:
        if e.code == 502:
            pytest.skip('Dev server problem')
        raise e

    try:
        data = json.loads(url.read().decode())
        assert len(data[data_type]) > 0
    except http.client.IncompleteRead as e:
        data = e.partial
        if not len(data) > 0:
            raise AssertionError