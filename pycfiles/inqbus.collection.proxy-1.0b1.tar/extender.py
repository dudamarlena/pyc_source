# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/max/development/checkouts/inqbus.collection.proxy/inqbus/collection/proxy/content/extender.py
# Compiled at: 2011-06-06 08:02:23
from zope.component import adapts
from zope.interface import implements
from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.field import ExtensionField
from Products.Archetypes.Field import BooleanField
from Products.Archetypes.Widget import BooleanWidget
from Products.ATContentTypes.interface import IATTopic

class BooleanProxyField(ExtensionField, BooleanField):
    """A trivial field."""
    pass


class ProxyExtender(object):
    implements(ISchemaExtender)
    adapts(IATTopic)
    fields = [
     BooleanProxyField('boolean_proxy_field', schemata='settings', widget=BooleanWidget(label='enable proxy', description='Allow Plone Collections to proxy the content to not switch the context. The proxied content is shown directly in the context of the collection. If the user klick on a collectionitem, only the url change but neither the navigation nor the breadcrums are modified.'))]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields