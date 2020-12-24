# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/restin/controllers/data.py
# Compiled at: 2007-05-04 19:49:10
from restin.lib.base import *

class DataController(restler.BaseController(restin_model)):
    __module__ = __name__

    def __init__(self):
        route = request.environ['routes.route']
        route_info = request.environ['pylons.routes_dict']
        application_id = route_info['application_id']
        app = self._get_entity_or_404(restin_model.Application, application_id)
        self._model = app.model
        entity_name = route_info['entity_name']
        collection_name = '%ss' % entity_name
        route.member_name = entity_name
        route.collection_name = collection_name
        route.parent_resource = dict(member_name='application', collection_name='applications')
        super(DataController, self).__init__()