# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/comet/authenticate.py
# Compiled at: 2017-04-23 10:30:41
from __future__ import print_function
import requests, json, time
from pprint import pprint
USERNAME = ''
PASSWORD = ''

class AuthenticationException(Exception):
    pass


class Authenticator(object):
    base_uri = None
    token = None
    HEADER = {'content-type': 'application/json'}
    verify = False

    def __init__(self, uri=None):
        Authenticator.base_uri = uri

    @classmethod
    def set_auth_base_uri(cls, uri):
        cls.base_uri = uri

    @classmethod
    def logon(cls, username, password):
        ret = False
        if not cls.token:
            if cls.base_uri:
                authuri = '%s/login/' % cls.base_uri
                data = {'username': username, 'password': password}
                r = requests.post(authuri, data=json.dumps(data), headers=cls.HEADER, verify=cls.verify)
                try:
                    cls.token = r.json()['key']
                except:
                    ret = False

                ret = cls.token
        else:
            ret = cls.token
        return ret

    @classmethod
    def logoff(cls):
        ret = True
        if cls.token:
            if cls.base_uri:
                authuri = '%s/logout/' % cls.base_uri
                header = cls.HEADER
                header['Authorization'] = 'Token %s' % cls.token
                r = requests.post(authuri, headers=header, verify=cls.verify)
                cls.token = None
            else:
                ret = False
        return ret

    @classmethod
    def status(cls):
        ret = False
        if cls.token:
            ret = True
        return ret


def hop_get(url, headers=None):
    r = requests.get(url, headers=headers)
    ret = None
    if r.status_code == 200:
        ret = r.json()
    elif r.status_code == 202:
        finished = False
        newurl = r.headers['Location']
        while not finished:
            ret = requests.get(newurl, headers=headers).json()
            if 'status' not in ret:
                finished = True
            else:
                time.sleep(1)

    elif r.status_code == 401:
        ret = {'error': 'Not Authenticated'}
    return ret


def main():
    url = 'http://localhost:8080/rest-auth'
    auth = Authenticator(url)
    user = USERNAME
    password = PASSWORD
    print(auth.status())
    print(auth.logon(user, password))
    print(auth.status())
    print(auth.logoff())
    print(auth.status())
    print(auth.logoff())


def test_get_cluster_list():
    token = ''
    print('\nTEST 1: Get without logon')
    print('-' * 80)
    authheader = {'content-type': 'application/json', 'Authorization': 'Token %s' % token}
    geturl = 'http://localhost:8080/v1/cluster/'
    r = requests.get(geturl, headers=authheader)
    pprint(r.json())
    print('\nTEST 2: Auth and then get cluster list')
    print('-' * 80)
    authurl = 'http://localhost:8080/rest-auth'
    auth = Authenticator(authurl)
    user = USERNAME
    password = PASSWORD
    token = auth.logon(user, password)
    authheader = {'content-type': 'application/json', 'Authorization': 'Token %s' % token}
    geturl = 'http://localhost:8080/v1/cluster/'
    r = hop_get(geturl, headers=authheader)
    pprint(r)
    print("\nTEST 3: Get cluster 'OSG'")
    print('-' * 80)
    geturl1 = '%s%s' % (geturl, 'osg/')
    r1 = hop_get(geturl1, headers=authheader)
    pprint(r1)
    print('\nTEST 4: logoff and get cluster list again')
    print('-' * 80)
    auth.logoff()
    authheader = {'content-type': 'application/json', 'Authorization': 'Token %s' % token}
    geturl = 'http://localhost:8080/v1/cluster/'
    r = requests.get(geturl, headers=authheader)
    pprint(r.json())


if __name__ == '__main__':
    test_get_cluster_list()