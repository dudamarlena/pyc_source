# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/mougeon/bootstrap.py
# Compiled at: 2012-03-07 16:35:35
"""
Created on 01 March 2012 04:19:29

@author: maemo
"""
from mougeon.core import facade
from optparse import OptionParser
import logging
from mougeon.common import version
version.getInstance().submitRevision('$Revision: 30 $')
LEVELS = {'debug': logging.DEBUG, 'info': logging.INFO, 
   'warning': logging.WARNING, 
   'error': logging.ERROR, 
   'critical': logging.CRITICAL}

def showGui():
    from mougeon.gui.hildon.mougeonGui import mougeonGui
    gui = mougeonGui()
    gui.run()


def noGui():
    pass


def run():
    versionManager = version.getInstance()
    usage = '%prog '
    str_version = '%prog ' + versionManager.getVersion() + '(' + versionManager.getRevision() + ')'
    parser = OptionParser(usage=usage, version=str_version)
    parser.add_option('-g', '--gui', action='store_true', dest='gui', default=False, help='show the gui')
    parser.add_option('-l', '--log', action='store', type='string', dest='level_name', help='log level')
    (options, args) = parser.parse_args()
    level = LEVELS.get(options.level_name, logging.WARNING)
    logging.basicConfig(level=level)
    if options.gui:
        showGui()
    else:
        noGui()


if __name__ == '__main__':
    run()