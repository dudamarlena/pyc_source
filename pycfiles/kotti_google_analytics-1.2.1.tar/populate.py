# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/workspace/kotti_google_analytics/kotti_google_analytics/populate.py
# Compiled at: 2017-06-09 02:59:49
import colander, deform
from kotti_controlpanel.util import add_settings
from kotti_controlpanel.util import get_setting
from kotti_google_analytics import _, controlpanel_id, AnalyticsDefault, CONTROL_PANEL_LINKS

class AnalyticsSchema(colander.MappingSchema):
    client_id = colander.SchemaNode(colander.String(), name='client_id', title=_('Client ID'))
    client_secret = colander.SchemaNode(colander.String(), name='client_secret', title=_('Client Secret'))
    identity = colander.SchemaNode(colander.String(), name='identity', title=_('Identity'))
    access_token = colander.SchemaNode(colander.String(), name='access_token', title=_('Access Token'), widget=deform.widget.HiddenWidget(), missing=True)
    refresh_token = colander.SchemaNode(colander.String(), name='refresh_token', title=_('Refresh Token'), widget=deform.widget.HiddenWidget(), missing=True)
    property_id = colander.SchemaNode(colander.String(), name='property_id', title=_('Account Property ID'), default=AnalyticsDefault.property_id)
    send_user_id = colander.SchemaNode(colander.Boolean(), name='send_user_id', title=_('Send User ID to Google Analytics'), label=_('Enabling this will allow Google Analytics to individual users'), default=AnalyticsDefault.send_user_id)


GAControlPanel = {'name': controlpanel_id, 
   'icon': 'kotti_google_analytics:static/analytics.png', 
   'title': _('Google Analytics Settings'), 
   'description': _('Settings for google_analytics'), 
   'success_message': _('Successfully saved google_analytics settings.'), 
   'schema_factory': AnalyticsSchema, 
   'template': 'kotti_google_analytics:templates/controlpanel.pt'}

def populate():
    add_settings(GAControlPanel, links=CONTROL_PANEL_LINKS)