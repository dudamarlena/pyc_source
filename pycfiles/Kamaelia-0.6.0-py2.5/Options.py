# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Apps/Whiteboard/Options.py
# Compiled at: 2008-10-19 12:19:52
import sys, getopt, re

def parseOptions():
    (rhost, rport) = (None, None)
    serveport = None
    shortargs = ''
    longargs = ['serveport=', 'connectto=']
    (optlist, remargs) = getopt.getopt(sys.argv[1:], shortargs, longargs)
    for (o, a) in optlist:
        if o in ('-s', '--serveport'):
            serveport = int(a)
        elif o in ('-c', '--connectto'):
            (rhost, rport) = re.match('^([^:]+):([0-9]+)$', a).groups()
            rport = int(rport)

    return (
     rhost, rport, serveport)