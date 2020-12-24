# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: e:\nmdev\src\branches\loyalty\evasion-web\evasion\web\config\routing.py
# Compiled at: 2010-05-19 07:23:06
"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
import logging
from pylons import config
from routes import Mapper
from routes.util import controller_scan

def get_log():
    return logging.getLogger('evasion.web.config.routing')


def directory_scanner():
    """
    Scan each of the controller paths and use the routes.util
    controller_scan() to recover from each path.
    
    This function uses the paths set up in config['pylons.paths']['controllers']
    by the load_environment step.
    
    """
    returned = []
    for directory in config['pylons.paths']['controllers']:
        rc = controller_scan(directory)
        returned.extend(rc)

    return returned


def make_map():
    """Create the default mapper instance that the evasion.web 
    modules will then add connections to.
    """
    map = Mapper(controller_scan=directory_scanner, directory=None, always_scan=config['debug'])
    map.minimization = False
    return map