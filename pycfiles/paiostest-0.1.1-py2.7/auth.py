# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\paiostest\auth.py
# Compiled at: 2019-03-02 00:40:37
import json, urllib, urllib2
url = 'http://127.0.0.1:8888/'

def authen(name, secretId):
    values = {'name': name, 'secretId': secretId}
    data = urllib.urlencode(values)
    req = urllib2.Request(url + 'auth', data)
    response = urllib2.urlopen(req)
    print response.getcode()
    dict = response.read()
    print dict
    dict_info = json.loads(dict)
    print "dict_info['secretId']:", dict_info['secretId']
    G.secretId = dict_info['secretId']


class G:
    secretId = ''


def printMessage():
    print 'hi,welcome to authentication page!'


if __name__ == '__main__':
    printMessage()