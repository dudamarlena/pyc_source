# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\requests_model\myRequests.py
# Compiled at: 2019-10-23 22:38:43
# Size of source mod 2**32: 3166 bytes
import requests, re
from retrying import retry

class MyRequest:

    def __init__(self):
        self.result_content = None
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}

    @retry(stop_max_attempt_number=3)
    def get_response(self, url):
        try:
            response = requests.get(url, headers=(self.headers), timeout=30)
            if response.status_code == 200:
                return response
        except Exception as err:
            return ''

    def get_response_cookies(self, url, cookies):
        try:
            response = requests.get(url, headers=(self.headers), timeout=30, cookies=cookies)
            if response.status_code == 200:
                return response
        except Exception as err:
            return ''

    @retry(stop_max_attempt_number=3)
    def get_resText(self, url):
        try:
            response = requests.get(url, headers=(self.headers), timeout=30)
            if response.status_code == 200:
                return response.text
        except Exception as err:
            return ''

    @retry(stop_max_attempt_number=3)
    def get_resText_cookies(self, url, cookies):
        try:
            response = requests.get(url, headers=(self.headers), timeout=30, cookies=cookies)
            if response.status_code == 200:
                return response.text
        except Exception as err:
            return ''

    @retry(stop_max_attempt_number=3)
    def get_resText_post(self, url):
        try:
            response = requests.post(url, headers=(self.headers), timeout=30)
            if response.status_code == 200:
                return response.text
        except Exception as err:
            return ''

    @retry(stop_max_attempt_number=3)
    def get_resText_post_cookies(self, url, cookies):
        try:
            response = requests.post(url, headers=(self.headers), timeout=30, cookies=cookies)
            if response.status_code == 200:
                return response.text
        except Exception as err:
            return ''

    @retry(stop_max_attempt_number=3)
    def post_resText_cookies(self, url, headers, json, cookies):
        try:
            response = requests.post(url, headers=headers, data=json, timeout=30, cookies=cookies)
            if response.status_code == 200:
                return response.text
        except Exception as err:
            return ''

    @retry(stop_max_attempt_number=3)
    def parse_reg_info(self, html_message, reg_expre):
        try:
            pattern_messageInfo = re.compile('{reg_expre}'.format(reg_expre=reg_expre))
            self.result_content = pattern_messageInfo.findall(html_message)
            return self.result_content
        except Exception as err:
            return ''

    def get_cookie(self, url):
        session = requests.Session()
        req = session.get(url, headers=(self.headers))
        Cookie = dict(session.cookies)
        return Cookie