# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/feed2twitter/tinyurl.py
# Compiled at: 2008-05-16 15:46:22
import urllib

def tiny(url):
    try:
        data = urllib.urlencode(dict(url=url, source='RSS2Twit'))
        encodedurl = 'http://www.tinyurl.com/api-create.php?' + data
        instream = urllib.urlopen(encodedurl)
        ret = instream.read()
        instream.close()
        if len(ret) == 0:
            return url
        return ret
    except IOError, e:
        raise 'urllib error.'