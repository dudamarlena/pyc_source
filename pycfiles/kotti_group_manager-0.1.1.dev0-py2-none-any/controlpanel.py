# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/workspace/src/kotti_group_manager/kotti_group_manager/controlpanel.py
# Compiled at: 2018-09-19 15:48:59
import colander, deform
from kotti.views.form import ObjectType, CommaSeparatedListWidget
from kotti.fanstatic import tagit
from kotti_controlpanel.util import add_settings
from kotti_controlpanel.util import get_setting
from kotti_group_manager import _

@colander.deferred
def deferred_tag_it_widget(node, kw):
    tagit.need()
    all_tags = get_setting('domains', default=[])
    if not all_tags:
        all_tags = []
    available_tags = [ tag.encode('utf-8') for tag in all_tags ]
    widget = CommaSeparatedListWidget(template='tag_it', available_tags=available_tags)
    return widget


class GroupRulesSchema(colander.MappingSchema):
    email_domain_as_group = colander.SchemaNode(colander.Boolean(), description=_('Check the box above to enable this feature'), widget=deform.widget.CheckboxWidget(), title='Allow groups to be created from email domain', default=False)
    domains = colander.SchemaNode(ObjectType(), title=_('Black listed Domains'), widget=deferred_tag_it_widget, missing=[])
    group_as_content = colander.SchemaNode(colander.Boolean(), description='Check the box above to enable this feature', widget=deform.widget.CheckboxWidget(), title='Create a page for each group created', default=False)


GroupRulesControlPanel = {'name': 'kotti_group_rules', 
   'title': _('Group Rules'), 
   'description': _('Set rules for group members'), 
   'success_message': _('Successfully saved settings.'), 
   'schema_factory': GroupRulesSchema}