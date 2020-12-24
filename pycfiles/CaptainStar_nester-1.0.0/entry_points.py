# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cptsoul/entry_points.py
# Compiled at: 2013-10-07 08:06:28
import logging
from argparse import ArgumentParser
from cptsoul.common import CptCommon

def configLogging():
    fmt = '%(levelname)s - %(funcName)s: %(message)s'
    level = logging.DEBUG
    if CptCommon.cmdline.verbose <= 3:
        level = [
         logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG][CptCommon.cmdline.verbose]
    logging.basicConfig(level=level, format=fmt)


def cptsoul():
    parser = ArgumentParser(prog='cptsoul')
    parser.add_argument('-v', '--verbose', action='count', dest='verbose', help='Set verbose mode', default=0)
    parser.add_argument('-t', action='store_true', dest='tray', help='Start in tray')
    parser.add_argument('-d', action='store_true', dest='debug', help='Start with debug window')
    CptCommon.cmdline = parser.parse_args()
    from twisted.internet import gtk2reactor
    gtk2reactor.install()
    from twisted.internet import reactor
    from cptsoul.config import createConfigFile
    from cptsoul.manager import Manager
    configLogging()
    CptCommon.config = createConfigFile()
    manager = Manager()
    manager()
    reactor.run()