# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/plone/recipe/squid/iRedirector.py
# Compiled at: 2008-04-15 00:40:02
"""
/**********************************************************************
FILE     : $RCSfile$
PURPOSE  : squid redirector for icoya
NOTES    : uses redirector_class for custom rules
AUTHOR   : Simon Eisenmann
COPYRIGHT: (c) 2003-2007 by struktur AG
DATE     : 28JAN2003
REVISION : $Revision: 4359 $
VERSION  : $Id: iRedirector.py 4359 2007-06-15 07:19:12Z longsleep $ (Author: $Author: longsleep $)

struktur AG            Phone: +49 711 8966560
Kronenstr. 22A         Fax:   +49 711 89665610
70173 Stuttgart        email: info@struktur.de
GERMANY

http://www.struktur.de
http://www.strukturag.com

**********************************************************************/
 iRedirector.py -- a script for squid redirection.
 (a long-running process that uses unbuffered io; hence the -u flag in python)

 NOTE: use redirector_class to define the rules
       redirector_class can be automatically reloaded so you dont have to
       restart squid when the rules were changed.

"""
import sys, os, traceback
from thread import start_new_thread
cwd = os.getcwd()
if cwd not in sys.path:
    sys.path.insert(0, cwd)
import redirector_class
debug = 0
threaded = 1
logfile = '${location}/redirector.log'

class SquidRedirector:
    """ iRedirector main base class. """
    __module__ = __name__

    def __init__(self):
        pass

    def rewrite(self, line):
        if threaded:
            start_new_thread(rewrite, (line,), {})
        else:
            rewrite(line)

    def run(self):
        line = read()
        while line:
            maybe_reload_redirector_class()
            try:
                self.rewrite(line)
            except:
                exc = sys.exc_info()
                log(str(traceback.format_exception(exc[0], exc[1], exc[2])))
                raise

            line = read()


def maybe_reload_redirector_class():
    """ Helper for automatic reloading of the redirector class. """
    if redirector_class.reload_after == -1:
        return
    if redirector_class.reload_after > 0:
        redirector_class.reload_after = redirector_class.reload_after - 1
    else:
        reload(redirector_class)


def log(s):
    """ Loggin facility. """
    if not debug:
        return
    f = open(logfile, 'a')
    f.write(s + '\n')
    f.close()


def read():
    """ Returns one unbuffered line from squid. """
    try:
        return sys.stdin.readline()[:-1]
    except KeyboardInterrupt:
        return

    return


def write(s):
    """ Returns a single line to squid. """
    sys.stdout.write(s + '\n')
    sys.stdout.flush()


def rewrite(line):
    """ Splits up the line from squid and gives it to the redirector class. 
        This method can be called in a new thread so one redirector supports
        multiple redirections at the same time. This is a squid2.6 feature.
    """
    log('request : ' + line)
    line = line.split(' ')
    urlgroup = '-'
    if not threaded:
        (url, src_address, ident, method) = line[:4]
        if len(line) == 5:
            urlgroup = line[4]
    else:
        (index, url, src_address, ident, method) = line[:5]
        if len(line) == 6:
            urlgroup = line[5]
    new_url = redirector_class.rewrite(url, src_address)
    if not new_url:
        new_url = src_address = ident = method = ''
    if not threaded:
        response = (' ').join((new_url, src_address, ident, method, urlgroup))
    else:
        response = (' ').join((index, new_url, src_address, ident, method, urlgroup))
    write(response)
    log('response: ' + response)


if __name__ == '__main__':
    sr = SquidRedirector()
    sr.run()