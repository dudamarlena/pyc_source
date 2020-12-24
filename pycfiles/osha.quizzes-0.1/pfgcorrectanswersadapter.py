# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zupo/work/osha.quizzes/src/osha/quizzes/content/pfgcorrectanswersadapter.py
# Compiled at: 2012-10-18 11:02:24
"""Definition of the PFGCorrectAnswersAdapter content type"""
from AccessControl import ClassSecurityInfo
from osha.quizzes.config import PROJECTNAME
from osha.quizzes.interfaces import IPFGCorrectAnswersAdapter
from plone import api
from Products.Archetypes import atapi
from Products.ATContentTypes.content import schemata
from Products.CMFCore.permissions import View
from Products.PloneFormGen.content.actionAdapter import FormActionAdapter
from Products.PloneFormGen.content.actionAdapter import FormAdapterSchema
from zope.interface import implements
PFGCorrectAnswersAdapterSchema = FormAdapterSchema.copy() + atapi.Schema(())
PFGCorrectAnswersAdapterSchema['title'].storage = atapi.AnnotationStorage()
PFGCorrectAnswersAdapterSchema['description'].storage = atapi.AnnotationStorage()
schemata.finalizeATCTSchema(PFGCorrectAnswersAdapterSchema, moveDiscussion=False)

class PFGCorrectAnswersAdapter(FormActionAdapter):
    """Calculate the percentage of correct answers."""
    implements(IPFGCorrectAnswersAdapter)
    meta_type = 'PFGCorrectAnswersAdapter'
    schema = PFGCorrectAnswersAdapterSchema
    security = ClassSecurityInfo()
    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    security.declareProtected(View, 'onSuccess')

    def onSuccess(self, fields, REQUEST=None):
        """The essential method of a PloneFormGen Adapter."""
        max_points = 0
        points = 0
        for field in fields:
            if field.portal_type != 'FormSelectionField':
                continue
            max_points += 1
            if REQUEST.form.get(field.id) and field.correct_answer.strip() == REQUEST.form[field.id]:
                points += 1

        if max_points > 0:
            result = round(float(points) / float(max_points) * 100)
            api.portal.show_message(request=REQUEST, type='info', message='Your score is: %i%%' % result)


atapi.registerType(PFGCorrectAnswersAdapter, PROJECTNAME)