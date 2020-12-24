# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/i3visiotools/darkfy/lib/config_darkfy.py
# Compiled at: 2014-12-25 06:48:18
import os, copy, i3visiotools.logger as logger, logging
from wrappers.torsearch import Torsearch
from wrappers.ahmia import Ahmia

def getAllDarkEngines():
    """ 
                Method that recovers ALL the list of <DarkEngine> classes to be processed....

                :return:        Returns a list [] of <DarkEngine> classes.
        """
    logger = logging.getLogger('darkfy')
    logger.debug('Recovering all the available <DarkEngine> classes.')
    listAll = []
    listAll.append(Ahmia())
    logger.debug('Returning a list of ' + str(len(listAll)) + ' <DarkEngine> classes.')
    return listAll