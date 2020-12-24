# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Workspace/shcs_cli/shcs_cli/client.py
# Compiled at: 2016-09-11 11:02:52
import json, requests, re
from myterm.parser import VerbParser

class Error(Exception):

    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __str__(self):
        return '[%s] %s' % (self.code, self.msg)


class Client:

    def __init__(self, url=None, user=None, password=None, **kwargs):
        self._url = url
        self._user = user
        self._password = password
        if self._url[(-1)] != '/':
            self._url = self._url + '/'

    def _login(self, s):
        s.post(self._url + 'ws/login', data=json.dumps({'username': self._user, 
           'password': self._password}))

    def post(self, url, login=False, **kwargs):
        url = self._url + url
        s = requests.Session()
        if login:
            self._login(s)
        if 'data' not in kwargs:
            res = s.post(url, data=json.dumps(kwargs))
        else:
            res = s.post(url, data=kwargs['data'])
        if res.status_code == 200:
            try:
                return json.loads(res.text)
            except:
                return res

        raise Error(res.status_code, re.sub('<.*?>', '', res.text))

    def get(self, url, login=False):
        url = self._url + url
        s = requests.Session()
        if login:
            self._login(s)
        res = s.get(url)
        if res.status_code == 200:
            try:
                return json.loads(res.text)
            except:
                return res

        raise Error(res.status_code, re.sub('<.*?>', '', res.text))


from functools import wraps

def manage_error(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except requests.exceptions.ConnectionError as e:
            VerbParser().error('your parameters are wrong or shcs not run, check your parameters')
        except Error as e:
            if e.code == 404:
                VerbParser().error('shcs not found action, check your parameters')
            elif e.code == 418:
                VerbParser().error('shcs does not understand your request, check your parameters')
            elif e.code == 500:
                VerbParser().error('shcs has a problem, connect your admin')
            else:
                VerbParser().error(e)
        except Exception as e:
            raise e

    return decorated_function