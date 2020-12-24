# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icsemantic/langfallback/tests/helpers.py
# Compiled at: 2008-10-06 10:31:06
from Products.Archetypes import atapi
from Products.ATContentTypes.content.base import registerATCT
from Products.ATContentTypes.content.document import ATDocument
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.CMFCore.utils import getToolByName
from icsemantic.core.fieldproperty import ATFieldProperty, ATFieldMultilingualProperty
from icsemantic.langfallback import LangviewMessageFactory as _
from icsemantic.langfallback.config import PROJECTNAME
ATMockSchema = ATDocument.schema.copy() + atapi.Schema((atapi.StringField('textoMultilingue', required=False, searchable=True, storage=atapi.AnnotationStorage(), widget=atapi.StringWidget(label=_('Multilingual text'), description=_(''))),))
finalizeATCTSchema(ATMockSchema)

class ATMock(ATDocument):
    """ Describe a ATMock.
        ATMock es una clase de archetypes para hacer pruebas en los tests.
        No debe cargarse en una instalacion estandar del sistema.
    """
    __module__ = __name__
    portal_type = meta_type = archetype_name = 'ATMock'
    _at_rename_after_creation = True
    schema = ATMockSchema
    global_allow = True
    __implements__ = ATDocument.__implements__
    actions = ATDocument.actions
    multilingual_text = ATFieldProperty('textoMultilingue')
    multilingual_title = ATFieldMultilingualProperty('title')


registerATCT(ATMock, PROJECTNAME)