# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Mardix/Dropbox/Projects/Python/harambe/harambe/contrib/views/maintenance_page.py
# Compiled at: 2017-02-26 06:59:25
from harambe import Harambe
from harambe.contrib.app_option import AppOption
__options__ = {}

class Main(Harambe):
    NS = 'MaintenancePage'
    app_option = AppOption(__name__)

    @classmethod
    def _register(cls, app, **kwargs):
        template = __options__.get('template', 'maintenance_page/Main/index.jade')
        super(cls, cls)._register(app, **kwargs)
        cls.app_option.init({'status': False, 
           'exclude': []}, 'Maintenance Page Option')

        @app.before_request
        def on_maintenance():
            if cls.app_option.get('status') is True:
                return (cls.render(_layout=template), 503)