# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/pyjama/bootstrap.py
# Compiled at: 2012-01-11 12:12:18
"""
Created on Oct 14, 2011

@author: maemo
"""
from optparse import OptionParser
import logging
from pyjama.common import version
version.getInstance().submitRevision('$Revision: 4 $')
LEVELS = {'debug': logging.DEBUG, 'info': logging.INFO, 
   'warning': logging.WARNING, 
   'error': logging.ERROR, 
   'critical': logging.CRITICAL}

def showGui():
    from pyjama.gui.hildon.pyjamaGui import pyjamaGui
    gui = pyjamaGui()
    gui.run()


def noGui(output=None):
    from pyjama.core import facade
    facade.pyjama().generate(output)


def run():
    versionManager = version.getInstance()
    usage = '%prog '
    str_version = '%prog ' + versionManager.getVersion() + '(' + versionManager.getRevision() + ')'
    parser = OptionParser(usage=usage, version=str_version)
    parser.add_option('-o', '--output', action='store', dest='output', default='.', help='output location')
    parser.add_option('-g', '--gui', action='store_true', dest='gui', default=False, help='show the gui')
    parser.add_option('-l', '--log', action='store', type='string', dest='level_name', help='log level')
    (options, args) = parser.parse_args()
    level = LEVELS.get(options.level_name, logging.NOTSET)
    logging.basicConfig(level=level)
    if options.gui:
        showGui()
    else:
        noGui(options.output)


if __name__ == '__main__':
    run()