# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bika/health/content/ethnicity.py
# Compiled at: 2015-11-03 03:53:19
from zope.interface import implements
from Products.Archetypes import atapi
from Products.Archetypes.public import BaseContent
from bika.health.interfaces import IEthnicity
from bika.lims.content.bikaschema import BikaSchema
from bika.health import config
schema = BikaSchema.copy() + atapi.Schema(())
schema['description'].widget.visible = True
schema['description'].schemata = 'default'

class Ethnicity(BaseContent):
    implements(IEthnicity)
    schema = schema


atapi.registerType(Ethnicity, config.PROJECTNAME)