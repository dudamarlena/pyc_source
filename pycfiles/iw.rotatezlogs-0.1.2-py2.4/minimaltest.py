# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/rotatezlogs/ftests/minimaltest.py
# Compiled at: 2008-07-29 13:25:24
"""Testing rotatezlogs

Configure a <rotatelogfile> handler in the <logger access> section of
your Zope instance, then run this script. See the main README.txt of
this packege for configuration hints.

Assuming your instance listens in http://localhost:8080, otherwise
change ZOPE_HOME_URL below.

$Id: minimaltest.py 5742 2006-06-05 19:13:43Z glenfant $
"""
import urllib2
ZOPE_HOME_URL = 'http://localhost:8080/'
SHOW_DOT_EVERY = 50
print 'Refresh the view of your log directory while running this script.'
print 'Hit Ctrl+C to stop.'
print 'Will show one dot every', SHOW_DOT_EVERY, 'queries.'
i = 0
while 1:
    fh = urllib2.urlopen(ZOPE_HOME_URL)
    dummy = fh.read()
    fh.close()
    i += 1
    if i == SHOW_DOT_EVERY:
        i = 0
        print '.',