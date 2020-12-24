# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zupo/work/osha.quizzes/src/osha/quizzes/extender.py
# Compiled at: 2012-10-18 05:04:35
"""Extending existing Archetypes content types."""
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from Products.Archetypes.public import StringField
from Products.Archetypes.public import StringWidget
from Products.PloneFormGen.content.fields import FGSelectionField
from zope.component import adapts
from zope.interface import implements

class CorrectAnswerField(ExtensionField, StringField):
    """Field to specify the correct answer."""
    pass


class FGSelectionFieldExtender(object):
    adapts(FGSelectionField)
    implements(IOrderableSchemaExtender)
    fields = [
     CorrectAnswerField('correct_answer', widget=StringWidget(label='Correct answer'))]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        """Manipulate the order in which fields appear.

        @param schematas: Dictonary of schemata name -> field lists
        @return: Dictionary of reordered field lists per schemata.

        """
        new_schemata = schematas.copy()
        new_schemata['default'].remove('correct_answer')
        new_schemata['default'].insert(new_schemata['default'].index('fgVocabulary') + 1, 'correct_answer')
        return new_schemata

    def getFields(self):
        return self.fields