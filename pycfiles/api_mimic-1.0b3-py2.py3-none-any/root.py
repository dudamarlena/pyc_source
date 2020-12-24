# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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