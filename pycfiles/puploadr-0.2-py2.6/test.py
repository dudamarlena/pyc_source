# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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