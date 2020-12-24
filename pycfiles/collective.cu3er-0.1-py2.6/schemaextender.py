# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/cu3er/schemaextender.py
# Compiled at: 2010-05-22 18:32:52
from zope.component import adapts
from zope.interface import implements
from zope.i18nmessageid import MessageFactory
from Products.ATContentTypes.interface import IATContentType
from Products.Archetypes.public import BooleanField, BooleanWidget, IntegerField, IntegerWidget, TextField, TextAreaWidget
from archetypes.schemaextender.interfaces import ISchemaExtender, IBrowserLayerAwareExtender
from archetypes.schemaextender.field import ExtensionField
from collective.cu3er.interfaces import ICU3ERSpecific
_ = MessageFactory('collective.cu3er')

class CU3ERBooleanField(ExtensionField, BooleanField):
    """A custom boolean field."""
    pass


class CU3ERIntegerField(ExtensionField, IntegerField):
    """A custom integer field."""
    pass


class CU3ERTextField(ExtensionField, TextField):
    """A custom text field."""
    pass


class CU3ERContentTypeExtender(object):
    adapts(IATContentType)
    implements(ISchemaExtender, IBrowserLayerAwareExtender)
    layer = ICU3ERSpecific
    _fields = [
     CU3ERBooleanField('cu3er_enabled', languageIndependent=True, schemata='CU3ER', widget=BooleanWidget(description=_('desc_cu3er_enabled', default='Switch CU3ER on and off.'), label=_('label_cu3er_enabled', default='Enable CU3ER.'))),
     CU3ERIntegerField('cu3er_height', default='300', languageIndependent=True, schemata='CU3ER', validators='isInt', widget=IntegerWidget(description=_('descr_cu3er_height', 'The height of the flash object in px.'), label=_('label_cu3er_height', default='Height'))),
     CU3ERIntegerField('cu3er_width', default='600', languageIndependent=True, schemata='CU3ER', validators='isInt', widget=IntegerWidget(description=_('descr_cu3er_width', 'The width of the flash object in px.'), label=_('label_cu3er_width', default='Width'))),
     CU3ERTextField('cu3er_config', languageIndependent=True, schemata='CU3ER', type='text/xml', widget=TextAreaWidget(description=_('desc_cu3er_config', default='Add your custom XML config here. This must be valid xml. See <a href="http://www.progressivered.com/cu3er/docs/" target="_blank">http://www.progressivered.com/cu3er/docs/</a> for further information. See <a href="++resource++collective.cu3er.config-sample.xml" target="_blank">this XML file</a> for a sample configuration.'), label=_('label_cu3er_config', default='CU3ER config.'), rows=20))]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self._fields