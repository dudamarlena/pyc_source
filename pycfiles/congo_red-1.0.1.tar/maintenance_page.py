# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/mardochee.macxis/Projects/Python/portfoliopy/portfolio/component/views/maintenance_page.py
# Compiled at: 2015-06-20 05:08:18
__doc__ = '\nMaintenance Page\n'
from portfolio import Portfolio

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
        template = 'Portfolio/MaintenancePage/index.html'

    class Maintenance(Portfolio):

        @classmethod
        def register(cls, app, **kwargs):
            super(cls, cls).register(app, **kwargs)
            if cls.get_config('MAINTENANCE_ON'):

                @app.before_request
                def on_maintenance():
                    return (
                     cls.render(layout=template), 503)

    return Maintenance


MaintenanceV = maintenance_page()