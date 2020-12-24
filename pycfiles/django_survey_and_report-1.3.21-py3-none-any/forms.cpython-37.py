# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/workspace/django-survey/survey/forms.py
# Compiled at: 2020-02-23 10:00:51
# Size of source mod 2**32: 10710 bytes
import logging, uuid
from django import forms
from django.conf import settings
from django.forms import models
from django.urls import reverse
from django.utils.text import slugify
from survey.models import Answer, Question, Response
from survey.signals import survey_completed
from survey.widgets import ImageSelectWidget
LOGGER = logging.getLogger(__name__)

class ResponseForm(models.ModelForm):
    FIELDS = {Question.TEXT: forms.CharField, 
     Question.SHORT_TEXT: forms.CharField, 
     Question.SELECT_MULTIPLE: forms.MultipleChoiceField, 
     Question.INTEGER: forms.IntegerField}
    WIDGETS = {Question.TEXT: forms.Textarea, 
     Question.SHORT_TEXT: forms.TextInput, 
     Question.RADIO: forms.RadioSelect, 
     Question.SELECT: forms.Select, 
     Question.SELECT_IMAGE: ImageSelectWidget, 
     Question.SELECT_MULTIPLE: forms.CheckboxSelectMultiple}

    class Meta:
        model = Response
        fields = ()

    def __init__(self, *args, **kwargs):
        self.survey = kwargs.pop('survey')
        self.user = kwargs.pop('user')
        try:
            self.step = int(kwargs.pop('step'))
        except KeyError:
            self.step = None

        (super(ResponseForm, self).__init__)(*args, **kwargs)
        self.uuid = uuid.uuid4().hex
        self.steps_count = len(self.survey.questions.all())
        self.response = False
        self.answers = False
        data = kwargs.get('data')
        for i, question in enumerate(self.survey.questions.all()):
            is_current_step = i != self.step and self.step is not None
            if self.survey.display_by_question:
                if is_current_step:
                    continue
            self.add_question(question, data)

        self._get_preexisting_response()
        if not self.survey.editable_answers:
            if self.response is not None:
                for name in self.fields.keys():
                    self.fields[name].widget.attrs['disabled'] = True

    def _get_preexisting_response(self):
        """ Recover a pre-existing response in database.

        The user must be logged. Will store the response retrieved in an attribute
        to avoid multiple db calls.

        :rtype: Response or None"""
        if self.response:
            return self.response
            self.response = self.user.is_authenticated or None
        else:
            try:
                self.response = Response.objects.prefetch_related('user', 'survey').get(user=(self.user),
                  survey=(self.survey))
            except Response.DoesNotExist:
                LOGGER.debug("No saved response for '%s' for user %s", self.survey, self.user)
                self.response = None

            return self.response

    def _get_preexisting_answers(self):
        """ Recover pre-existing answers in database.

        The user must be logged. A Response containing the Answer must exists.
        Will create an attribute containing the answers retrieved to avoid multiple
        db calls.

        :rtype: dict of Answer or None"""
        if self.answers:
            return self.answers
            response = self._get_preexisting_response()
            if response is None:
                self.answers = None
        else:
            try:
                answers = Answer.objects.filter(response=response).prefetch_related('question')
                self.answers = {answer.question.id:answer for answer in answers.all()}
            except Answer.DoesNotExist:
                self.answers = None

        return self.answers

    def _get_preexisting_answer(self, question):
        """ Recover a pre-existing answer in database.

        The user must be logged. A Response containing the Answer must exists.

        :param Question question: The question we want to recover in the
        response.
        :rtype: Answer or None"""
        answers = self._get_preexisting_answers()
        return answers.get(question.id, None)

    def get_question_initial--- This code section failed: ---

 L. 132         0  LOAD_CONST               None
                2  STORE_FAST               'initial'

 L. 133         4  LOAD_FAST                'self'
                6  LOAD_METHOD              _get_preexisting_answer
                8  LOAD_FAST                'question'
               10  CALL_METHOD_1         1  '1 positional argument'
               12  STORE_FAST               'answer'

 L. 134        14  LOAD_FAST                'answer'
               16  POP_JUMP_IF_FALSE   164  'to 164'

 L. 136        18  LOAD_FAST                'question'
               20  LOAD_ATTR                type
               22  LOAD_GLOBAL              Question
               24  LOAD_ATTR                SELECT_MULTIPLE
               26  COMPARE_OP               ==
               28  POP_JUMP_IF_FALSE   158  'to 158'

 L. 137        30  BUILD_LIST_0          0 
               32  STORE_FAST               'initial'

 L. 138        34  LOAD_FAST                'answer'
               36  LOAD_ATTR                body
               38  LOAD_STR                 '[]'
               40  COMPARE_OP               ==
               42  POP_JUMP_IF_FALSE    46  'to 46'

 L. 139        44  JUMP_ABSOLUTE       164  'to 164'
             46_0  COME_FROM            42  '42'

 L. 140        46  LOAD_STR                 '['
               48  LOAD_FAST                'answer'
               50  LOAD_ATTR                body
               52  COMPARE_OP               in
               54  POP_JUMP_IF_FALSE   140  'to 140'
               56  LOAD_STR                 ']'
               58  LOAD_FAST                'answer'
               60  LOAD_ATTR                body
               62  COMPARE_OP               in
               64  POP_JUMP_IF_FALSE   140  'to 140'

 L. 141        66  BUILD_LIST_0          0 
               68  STORE_FAST               'initial'

 L. 142        70  LOAD_FAST                'answer'
               72  LOAD_ATTR                body
               74  LOAD_CONST               1
               76  LOAD_CONST               -1
               78  BUILD_SLICE_2         2 
               80  BINARY_SUBSCR    
               82  LOAD_METHOD              strip
               84  CALL_METHOD_0         0  '0 positional arguments'
               86  STORE_FAST               'unformated_choices'

 L. 143        88  SETUP_LOOP          156  'to 156'
               90  LOAD_FAST                'unformated_choices'
               92  LOAD_METHOD              split
               94  LOAD_GLOBAL              settings
               96  LOAD_ATTR                CHOICES_SEPARATOR
               98  CALL_METHOD_1         1  '1 positional argument'
              100  GET_ITER         
              102  FOR_ITER            136  'to 136'
              104  STORE_FAST               'unformated_choice'

 L. 144       106  LOAD_FAST                'unformated_choice'
              108  LOAD_METHOD              split
              110  LOAD_STR                 "'"
              112  CALL_METHOD_1         1  '1 positional argument'
              114  LOAD_CONST               1
              116  BINARY_SUBSCR    
              118  STORE_FAST               'choice'

 L. 145       120  LOAD_FAST                'initial'
              122  LOAD_METHOD              append
              124  LOAD_GLOBAL              slugify
              126  LOAD_FAST                'choice'
              128  CALL_FUNCTION_1       1  '1 positional argument'
              130  CALL_METHOD_1         1  '1 positional argument'
              132  POP_TOP          
              134  JUMP_BACK           102  'to 102'
              136  POP_BLOCK        
              138  JUMP_ABSOLUTE       164  'to 164'
            140_0  COME_FROM            64  '64'
            140_1  COME_FROM            54  '54'

 L. 148       140  LOAD_FAST                'initial'
              142  LOAD_METHOD              append
              144  LOAD_GLOBAL              slugify
              146  LOAD_FAST                'answer'
              148  LOAD_ATTR                body
              150  CALL_FUNCTION_1       1  '1 positional argument'
              152  CALL_METHOD_1         1  '1 positional argument'
              154  POP_TOP          
            156_0  COME_FROM_LOOP       88  '88'
              156  JUMP_FORWARD        164  'to 164'
            158_0  COME_FROM            28  '28'

 L. 150       158  LOAD_FAST                'answer'
              160  LOAD_ATTR                body
              162  STORE_FAST               'initial'
            164_0  COME_FROM           156  '156'
            164_1  COME_FROM            16  '16'

 L. 151       164  LOAD_FAST                'data'
              166  POP_JUMP_IF_FALSE   184  'to 184'

 L. 154       168  LOAD_FAST                'data'
              170  LOAD_METHOD              get
              172  LOAD_STR                 'question_%d'
              174  LOAD_FAST                'question'
              176  LOAD_ATTR                pk
              178  BINARY_MODULO    
              180  CALL_METHOD_1         1  '1 positional argument'
              182  STORE_FAST               'initial'
            184_0  COME_FROM           166  '166'

 L. 155       184  LOAD_FAST                'initial'
              186  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 156_0

    def get_question_widget(self, question):
        """ Return the widget we should use for a question.

        :param Question question: The question
        :rtype: django.forms.widget or None """
        try:
            return self.WIDGETS[question.type]
        except KeyError:
            return

    @staticmethod
    def get_question_choices(question):
        """ Return the choices we should use for a question.

        :param Question question: The question
        :rtype: List of String or None """
        qchoices = None
        if question.type not in [Question.TEXT, Question.SHORT_TEXT, Question.INTEGER]:
            qchoices = question.get_choices()
            if question.type in [Question.SELECT, Question.SELECT_IMAGE]:
                qchoices = tuple([('', '-------------')]) + qchoices
        return qchoices

    def get_question_field(self, question, **kwargs):
        """ Return the field we should use in our form.

        :param Question question: The question
        :param **kwargs: A dict of parameter properly initialized in
            add_question.
        :rtype: django.forms.fields """
        try:
            return (self.FIELDS[question.type])(**kwargs)
        except KeyError:
            return (forms.ChoiceField)(**kwargs)

    def add_question(self, question, data):
        """ Add a question to the form.

        :param Question question: The question to add.
        :param dict data: The pre-existing values from a post request. """
        kwargs = {'label':question.text, 
         'required':question.required}
        initial = self.get_question_initial(question, data)
        if initial:
            kwargs['initial'] = initial
        else:
            choices = self.get_question_choices(question)
            if choices:
                kwargs['choices'] = choices
            widget = self.get_question_widget(question)
            if widget:
                kwargs['widget'] = widget
            field = (self.get_question_field)(question, **kwargs)
            if question.category:
                field.widget.attrs['category'] = question.category.name
            else:
                field.widget.attrs['category'] = ''
        self.fields['question_%d' % question.pk] = field

    def has_next_step(self):
        if self.survey.display_by_question:
            if self.step < self.steps_count - 1:
                return True
        return False

    def next_step_url(self):
        if self.has_next_step():
            context = {'id':self.survey.id, 
             'step':self.step + 1}
            return reverse('survey-detail-step', kwargs=context)

    def current_step_url(self):
        return reverse('survey-detail-step', kwargs={'id':self.survey.id,  'step':self.step})

    def save(self, commit=True):
        """ Save the response object """
        response = self._get_preexisting_response()
        if not self.survey.editable_answers:
            if response is not None:
                return
        if response is None:
            response = super(ResponseForm, self).save(commit=False)
        response.survey = self.survey
        response.interview_uuid = self.uuid
        if self.user.is_authenticated:
            response.user = self.user
        response.save()
        data = {'survey_id':response.survey.id, 
         'interview_uuid':response.interview_uuid,  'responses':[]}
        for field_name, field_value in list(self.cleaned_data.items()):
            if field_name.startswith('question_'):
                q_id = int(field_name.split('_')[1])
                question = Question.objects.get(pk=q_id)
                answer = self._get_preexisting_answer(question)
                if answer is None:
                    answer = Answer(question=question)
                if question.type == Question.SELECT_IMAGE:
                    value, img_src = field_value.split(':', 1)
                    LOGGER.debug('Question.SELECT_IMAGE not implemented, please use : %s and %s', value, img_src)
                answer.body = field_value
                data['responses'].append((answer.question.id, answer.body))
                LOGGER.debug('Creating answer for question %d of type %s : %s', q_id, answer.question.type, field_value)
                answer.response = response
                answer.save()

        survey_completed.send(sender=Response, instance=response, data=data)
        return response