# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/api_metadata/views/root.py
# Compiled at: 2018-04-27 06:39:21
from api_metadata import __version__
from . import MetadataAPIBaseView
API_DESCRIPTION = 'Metadata API, just query http://169.254.42.42/conf or http://169.254.42.42/conf?format=json to get info about yourself'

class RootView(MetadataAPIBaseView):
    route_base = '/'

    def index(self):
        return {'api': 'api-metadata', 
           'description': API_DESCRIPTION, 
           'version': __version__}