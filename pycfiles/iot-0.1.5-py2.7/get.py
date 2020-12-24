# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/osiot/python/get.py
# Compiled at: 2014-02-18 02:32:20
import json, urllib2, serial, time
url = 'http://b.phodal.com/athome/1'
while 1:
    try:
        date = urllib2.urlopen(url)
        result = json.load(date)
        status = result[0]['led1']
        print status
    except urllib2.URLError:
        print 'Bad URL or timeout'