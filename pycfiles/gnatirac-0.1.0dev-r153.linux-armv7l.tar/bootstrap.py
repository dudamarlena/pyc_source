# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/gnatirac/bootstrap.py
# Compiled at: 2011-12-29 07:58:32
"""
Created on Oct 14, 2011

@author: maemo
"""
from gnatirac.core import gnatirac
from optparse import OptionParser
import logging
from gnatirac.common import version
version.getInstance().submitRevision('$Revision: 4 $')
LEVELS = {'debug': logging.DEBUG, 'info': logging.INFO, 
   'warning': logging.WARNING, 
   'error': logging.ERROR, 
   'critical': logging.CRITICAL}

def showGui():
    from gnatirac.gui.hildon.gnatiracGui import gnatiracGui
    gui = gnatiracGui()
    gui.run()


def run():
    versionManager = version.getInstance()
    usage = '%prog '
    str_version = '%prog ' + versionManager.getVersion() + '(' + versionManager.getRevision() + ')'
    parser = OptionParser(usage=usage, version=str_version)
    parser.add_option('-l', '--log', action='store', type='string', dest='level_name', help='log level')
    (options, args) = parser.parse_args()
    level = LEVELS.get(options.level_name, logging.NOTSET)
    logging.basicConfig(level=level)
    showGui()


if __name__ == '__main__':
    run()