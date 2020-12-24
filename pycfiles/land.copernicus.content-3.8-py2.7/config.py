# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/land/copernicus/content/config.py
# Compiled at: 2018-01-16 07:51:31
""" Config module
"""
import os, logging
from zope.i18nmessageid.message import MessageFactory
EEAMessageFactory = MessageFactory('eea')
product_globals = globals()
PROJECTNAME = 'land.copernicus.content'
logger = logging.getLogger(PROJECTNAME)
PACKAGE_NAME = 'land.copernicus.content'
PACKAGE_DESCRIPTION = 'Custom Content-Types for Land Copernicus'
PACKAGE_URL = 'http://github.com/eea/land.copernicus.content'
ADD_PERMISSION = 'land.copernicus.content: Add presentation'
IFRAME_WIDTH = '920'
IFRAME_HEIGHT = '450'

def ENVPATH(name, default=None):
    """ GET path from os env
    """
    path = os.environ.get(name)
    if not path and default is None:
        raise EnvironmentError(('{} needs to be defined!').format(name))
    else:
        return path or default
    return


ENV_DL_SRC_PATH = ENVPATH('LAND_DOWNLOADS_SRC_PATH')
ENV_DL_DST_PATH = ENVPATH('LAND_DOWNLOADS_DST_PATH')
ENV_DL_STATIC_PATH = ENVPATH('LAND_DOWNLOADS_STATIC_PATH', '/land-files/')
ENV_HOST_USERS_STATS = ENVPATH('LAND_HOST_USERS_STATS', 'land.copernicus.eu')