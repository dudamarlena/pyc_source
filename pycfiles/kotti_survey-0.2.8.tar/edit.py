# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/workspace/kotti_survey/kotti_survey/views/edit.py
# Compiled at: 2016-06-17 05:39:38
"""
Created on 2016-06-15
:author: Oshane Bailey (b4.oshany@gmail.com)
"""
import colander
from kotti.views.form import AddFormView
from kotti.views.edit import ContentSchema
from kotti.views.form import EditFormView
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from pyramid.view import view_defaults
from deform.widget import RadioChoiceWidget
from kotti_survey import _
from kotti_survey.resources import Survey, Question, AnswerField

class SurveySchema(ContentSchema):
    title = colander.SchemaNode(colander.String(), title=_('Survey Title'))
    collect_user_info = colander.SchemaNode(colander.Boolean(), title=_('Restrict to login users'))
    redirect_url = colander.SchemaNode(colander.String(), title=_('Redirect URL:'), description='If no redirect url is given. Users will be redirect to the default result page.', missing=None)


class QuestionSchema(ContentSchema):
    title = colander.SchemaNode(colander.String(), title=_('Question'))
    question_type = colander.SchemaNode(colander.String(), title=_('Question Type'), validator=colander.OneOf(['radio', 'checkbox', 'text']), widget=RadioChoiceWidget(values=[
     [
      'radio', _('Single Choice')],
     [
      'checkbox', _('Multiple Choice')],
     [
      'text', _('Text')]]))


class AnswerSchema(ContentSchema):
    title = colander.SchemaNode(colander.String(), title=_('Answering Choice:'))


@view_config(name=Survey.type_info.add_view, permission='add', renderer='kotti:templates/edit/node.pt')
class SurveyAddForm(AddFormView):
    schema_factory = SurveySchema
    add = Survey
    item_type = _('Survey')


@view_config(name=Question.type_info.add_view, permission='add', renderer='kotti:templates/edit/node.pt')
class QuestionAddForm(AddFormView):
    schema_factory = QuestionSchema
    add = Question
    item_type = _('Question')


@view_config(name=AnswerField.type_info.add_view, permission='add', renderer='kotti:templates/edit/node.pt')
class AnswerAddForm(AddFormView):
    schema_factory = AnswerSchema
    add = AnswerField
    item_type = _('Answer')

    @property
    def success_url(self):
        return self.request.resource_url(self.context)

    def save_success(self, appstruct):
        prevanswers = self.context.children
        question_type = self.context.question_type
        if question_type == 'text':
            self.request.session.flash(('Cannot add answer to freetext question').format(self.context.title), 'error')
            raise HTTPFound(location=self.request.resource_url(self.context))
        elif question_type == 'radio' or question_type == 'checkbox':
            for prevanswer in prevanswers:
                if appstruct.get('title', '') == prevanswer.title:
                    self.request.session.flash(('Question already has this option').format(self.context.title), 'error')
                    raise HTTPFound(location=self.request.resource_url(self.context))

        super(AnswerAddForm, self).save_success(appstruct)


@view_config(name='edit', context=Survey, permission='edit', renderer='kotti:templates/edit/node.pt')
class SurveyEditForm(EditFormView):
    schema_factory = SurveySchema


@view_config(name='edit', context=Question, permission='edit', renderer='kotti:templates/edit/node.pt')
class QuestionEditForm(EditFormView):
    schema_factory = QuestionSchema


@view_config(name='edit', context=AnswerField, permission='edit', renderer='kotti:templates/edit/node.pt')
class AnswerEditForm(EditFormView):
    schema_factory = AnswerSchema