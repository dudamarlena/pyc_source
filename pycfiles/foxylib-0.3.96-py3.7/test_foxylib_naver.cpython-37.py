# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/socialmedia/naver/tests/test_foxylib_naver.py
# Compiled at: 2020-01-15 23:57:40
# Size of source mod 2**32: 2392 bytes
import logging
from unittest import TestCase
import pytest, requests
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.socialmedia.naver.foxylib_naver import FoxylibNaver
from foxylib.tools.url.url_tool import URLTool

class TestFoxylibNaver(TestCase):

    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    @pytest.mark.skip(reason='one time thing for auth token')
    def test_01(self):
        redirect_url = 'http://www.way2gosu.com/api/member/oauth2c'
        client_id = FoxylibNaver.client_id()
        url = URLTool.append_query2url('https://nid.naver.com/oauth2.0/authorize', {'response_type':'code', 
         'client_id':client_id, 
         'redirect_uri':redirect_url})
        requests.get(url)

    @pytest.mark.skip(reason="can't make it work yet")
    def test_02(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)
        token = FoxylibNaver.foxytrixy_auth_token()
        clubid = '29510017'
        url = 'https://openapi.naver.com/v1/cafe/' + clubid + '/members'
        j_data = {'nickname': 'foxytrixy'}
        headers = {'Content-Type':'application/json', 
         'Authorization':'Bearer {}'.format(token)}
        response = requests.post(url, json=j_data, headers=headers)
        logger.debug({'response':response,  'response.json()':response.json()})
        self.assertTrue(response.ok)