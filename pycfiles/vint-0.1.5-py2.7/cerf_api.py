# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vint/cerf_api.py
# Compiled at: 2013-05-01 20:06:06
from __future__ import unicode_literals
import logging, json
from urlparse import urljoin
import requests
__author__ = b'tchen'
logger = logging.getLogger(__name__)
DEFAULT_HOSTNAME = b'http://exam.tchen.me'

class Request(object):
    hostname = b''
    api_path = b'/'

    def __init__(self, authcode):
        from misc import config
        self.authcode = authcode
        self.api_base = self.hostname + self.api_path
        if config:
            try:
                self.hostname = config.get(b'global', b'host')
            except:
                pass

    def retrieve(self, id):
        url = urljoin(self.api_base, str(id)) + b'/'
        try:
            r = requests.get(url, data={b'authcode': self.authcode})
            return json.loads(r.text)
        except:
            return {}

    def delete(self, id):
        url = urljoin(self.api_base, str(id)) + b'/'
        try:
            r = requests.delete(url, data={b'authcode': self.authcode})
            if r.status_code == requests.codes.no_content:
                return True
            return False
        except:
            return False


class Cerf(object):

    def __init__(self, id, authcode, hostname=DEFAULT_HOSTNAME):
        from misc import config
        self.id = id
        self.authcode = authcode
        self.hostname = hostname
        if config:
            try:
                self.hostname = config.get(b'global', b'host')
                print b'Host name is: %s' % self.hostname
            except:
                pass

        self.interview = Interview(authcode, id)
        self.exam = Exam(authcode)
        self.answer = Answer(authcode)


class Interview(Request):
    hostname = DEFAULT_HOSTNAME
    api_path = b'/api/interviews/'

    def __init__(self, authcode, id):
        super(Interview, self).__init__(authcode)
        self.id = id

    def update(self, action, id=None, authcode=None):
        id = id or self.id
        authcode = authcode or self.authcode
        url = urljoin(self.api_base, str(id)) + b'/'
        try:
            r = requests.put(url, data={b'authcode': authcode, b'action': action})
            return json.loads(r.text)
        except:
            return {}

    def start(self, id=None, authcode=None):
        return self.update(b'start', id, authcode)

    def finish(self, id=None, authcode=None):
        return self.update(b'finish', id, authcode)

    def reset(self, id=None, authcode=None):
        return self.update(b'reset', id, authcode)


class Exam(Request):
    hostname = DEFAULT_HOSTNAME
    api_path = b'/api/exams/'


class Answer(Request):
    hostname = DEFAULT_HOSTNAME
    api_path = b'/api/answers/'

    def create(self, data):
        headers = {b'Content-type': b'application/json', b'Accept': b'*/*'}
        try:
            r = requests.post(self.api_base + b'?authcode=%s' % self.authcode, data=json.dumps(data), headers=headers)
            if r.status_code != requests.codes.created:
                return {}
            return json.loads(r.text)
        except Exception:
            return {}