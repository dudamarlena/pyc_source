# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fab_addon_geoalchemy/manager.py
# Compiled at: 2018-10-01 12:38:06
# Size of source mod 2**32: 1547 bytes
import logging
from flask_appbuilder.basemanager import BaseManager
from flask_babel import lazy_gettext as _
from flask import Blueprint, url_for
log = logging.getLogger(__name__)

class GeoAlchemyManager(BaseManager):

    def __init__(self, appbuilder):
        """
        Use the constructor to setup any config keys specific for your app.
        """
        super(GeoAlchemyManager, self).__init__(appbuilder)
        self.static_bp = Blueprint('fab_addon_geoalchemy', __name__, url_prefix='/static', template_folder='templates', static_folder='static/fab_addon_geoalchemy', static_url_path='/fab_addon_geoalchemy')
        self.addon_js = [('fab_addon_geoalchemy.static', 'js/leaflet.js'),
         ('fab_addon_geoalchemy.static', 'js/main.js')]
        self.addon_css = [('fab_addon_geoalchemy.static', 'css/leaflet.css'),
         ('fab_addon_geoalchemy.static', 'css/map.css')]
        log.info('Initializing GeoAlchemyManager')

    def register_views(self):
        """
        This method is called by AppBuilder when initializing,
        use it to add your views
        """
        pass

    def pre_process(self):
        log.info('Adding static blueprint for fab_addon_geoalchemy.')
        self.appbuilder.get_app.register_blueprint(self.static_bp)

    def post_process(self):
        pass