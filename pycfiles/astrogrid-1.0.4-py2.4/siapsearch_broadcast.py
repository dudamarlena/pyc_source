# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-9.6.0-i386/egg/astrogrid/examples/siapsearch_broadcast.py
# Compiled at: 2007-06-17 11:28:16
import sys
from astrogrid import acr
from astrogrid import MySpace
idir = '#siap/' + sys.argv[1]
print 'Reading images from %s' % idir
m = MySpace()
for filename in [ f[2] for f in m.ls(idir) if f[2][-4:] == 'fits' ]:
    print 'Loading %s' % filename
    acr.plastic.broadcast(idir + '/' + filename, 'Aladin')