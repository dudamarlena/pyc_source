# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dpl1_main/testing_app/forms.py
# Compiled at: 2014-02-25 09:38:37
from django import forms
from django.core.exceptions import ValidationError

class CustomForm(forms.Form):
    """Validates the entire page
    """

    def clean(self):
        """Checks if an answer was given to all the questions on the page

        :return: :raise ValidationError: if condition not satisfied
        """
        if set(self.fields.keys()).issubset(self.changed_data):
            return self.cleaned_data
        raise ValidationError('All questions have to be answered', code='invalid')


def create_form_for_questions(questions):
    """Creates a dynamic form instance, given the questions in a page

    :param questions: django.db.models.QuerySet of testing_app.models.Question
    :return: django.forms.Form instance
    """
    bases = (
     CustomForm,)
    attributes = {}
    if questions.count() == 0:
        attributes['submittable'] = False
        return type('EmptyDynamicForm', bases, attributes)
    for question in questions.all():
        if question.answer_set.count() == 0:
            continue
        choices = []
        for answer in question.answer_set.all():
            choices.append((answer.id, answer.text))

        if question.multiple_answers is True:
            form_type = forms.MultipleChoiceField
            widget = forms.CheckboxSelectMultiple
        else:
            widget = forms.RadioSelect
            form_type = forms.ChoiceField
        attributes[question.as_form_id()] = form_type(widget=widget, choices=choices, label=question.text)

    attributes['submittable'] = True
    form = type('DynamicPageForm', bases, attributes)
    return form