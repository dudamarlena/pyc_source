# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/osiot/python/post.py
# Compiled at: 2014-02-18 02:32:20
import urllib, urllib2

def post(url, data):
    req = urllib2.Request(url)
    data = urllib.urlencode(data)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    response = opener.open(req, data)
    return response.read()


def main():
    posturl = 'http://b.phodal.com/athome/1/'
    data = {'temperature': 19, 'sensors1': 22, 'sensors2': 7.5, 'led1': 1}
    print post(posturl, data)


if __name__ == '__main__':
    main()