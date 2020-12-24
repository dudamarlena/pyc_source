# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mardochee.macxis/Projects/Python/flask-pilot/pylot/component/views/maintenance_page.py
# Compiled at: 2015-05-21 02:42:07
"""
Maintenance Page
"""
from pylot import Pylot

def maintenance_page(template=None):
    """
    Create the Maintenance view
    Must be instantiated

    import maintenance_view
    MaintenanceView = maintenance_view()

    :param view_template: The directory containing the view pages
    :return:
    """
    if not template:
        template = 'Pylot/MaintenancePage/index.html'

    class Maintenance(Pylot):

        @classmethod
        def register(cls, app, **kwargs):
            super(cls, cls).register(app, **kwargs)
            if cls.get_config__('MAINTENANCE_ON'):

                @app.before_request
                def on_maintenance():
                    return (cls.render(layout=template), 503)

    return Maintenance


MaintenanceV = maintenance_page()