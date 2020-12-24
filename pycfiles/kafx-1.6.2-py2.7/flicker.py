# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\kafx\flicker.py
# Compiled at: 2012-05-18 23:22:26
import json, urllib2
url = 'http://api.flickr.com/services/rest/?format=json&method=flickr.people.getPublicPhotos&user_id=57176197@N02&api_key=126d9428fa129b7cf7c614b7c9af0325&per_page=500&extras=url_l'
udata = urllib2.urlopen(url)
data = udata.read()
if data[:14] == 'jsonFlickrApi(':
    data = data[14:]
    data = data[:-1]
o = json.loads(data)
for f in o['photos']['photo']:
    u = f['url_l']
    fn = u.rsplit('/', 1)[(-1)]
    print 'downloading %s to %s' % (u, fn)
    img = open(fn, 'wb')
    img.write(urllib2.urlopen(u, fn).read())
    img.close()