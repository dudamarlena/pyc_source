# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/uploadr/test.py
# Compiled at: 2010-10-15 15:13:04
import shelve
from configobj import ConfigObj
__author__ = 'elek'
__date__ = '$Oct 15, 2010 8:37:28 PM$'
if __name__ == '__main__':
    d = shelve.open('/tmp/uploadr.history')
    with open('/tmp/flickr.photos', 'w') as (f):
        n = ConfigObj()
        for (k, v) in d.iteritems():
            if k.startswith('/home'):
                img = k[k.rfind('/') + 1:]
                n[img] = v

        n.write(f)