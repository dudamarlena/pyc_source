# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gazest/controllers/robots.py
# Compiled at: 2007-10-17 12:11:25
import logging
from gazest.lib.base import *
from pprint import pprint
from paste.deploy.converters import asbool
log = logging.getLogger(__name__)

class RobotsController(BaseController):
    __module__ = __name__

    def index(self):
        response.headers['Content-Type'] = 'text/plain'
        if asbool(config['staging']):
            return 'User-agent: * \nDisallow: /\n'
        else:
            return render('/robots.mako')