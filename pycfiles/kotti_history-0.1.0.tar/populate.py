# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/oshane/Workspace/osoobe/packages/kotti/src/kotti_history/kotti_history/populate.py
# Compiled at: 2017-01-06 12:40:45
import colander, deform
from kotti import get_settings
from kotti_controlpanel.util import add_settings
from kotti_controlpanel.util import get_setting
from kotti_history import _, controlpanel_id
from kotti.views.edit.actions import content_type_factories

def available_content_types():
    try:
        all_types = get_settings()['kotti.available_types']
        return [ (f.type_info.name, f.type_info.title) for f in all_types
               ]
    except TypeError as e:
        return []


def build_widget():
    return deform.widget.CheckboxChoiceWidget(values=available_content_types(), inline=True)


class HistorySchema(colander.MappingSchema):
    track_contenttypes = colander.SchemaNode(colander.Set(), widget=build_widget(), validator=colander.Length(min=1))


HistoryControlPanel = {'name': controlpanel_id, 
   'title': _('History Controlpanel'), 
   'description': _('Settings for Site History'), 
   'success_message': _('Successfully saved history settings.'), 
   'schema_factory': HistorySchema, 
   'template': 'kotti_controlpanel:templates/cpanel.pt', 
   'bind': {'track_contenttypes': {'widget': build_widget}}}

def populate():
    add_settings(HistoryControlPanel, links=[])