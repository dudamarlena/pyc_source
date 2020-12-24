# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/wizard_builder/mocks.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 2056 bytes
__doc__ = '\nmocks are fake models, used in place of actual models when rendering forms\n'
from . import fields

class MockPage(object):
    pk = None
    id = None

    def __init__(self, data):
        try:
            self.section = data[0].get('section', 1)
        except BaseException:
            self.section = 1

        self.mock_questions = self._create_questions(data)

    def _create_questions(self, data):
        questions = []
        for question_data in data:
            question = MockQuestion(question_data)
            questions.append(question)

        return questions


class MockQuestion(object):

    def __init__(self, data):
        self.pk = self.id = data.get('id')
        self.text = data.get('question_text')
        self.descriptive_text = data.get('descriptive_text')
        self.section = data.get('section')
        self.position = data.get('position', 0)
        self.serialized = self.data = data
        self.choices = [MockChoice(choice_data) for choice_data in data.get('choices', [])]

    @property
    def type(self):
        try:
            return self.data.get('type').lower()
        except BaseException:
            return ''

    @property
    def field_id(self):
        return 'question_' + str(self.id)

    @property
    def choices_data_array(self):
        return [choice.data for choice in self.choices]

    @property
    def choices_pk_text_array(self):
        return [(choice.pk, choice.text) for choice in self.choices]

    def make_field(self):
        field_generator = getattr(fields.QuestionField, self.type, fields.QuestionField.singlelinetext)
        return field_generator(self)


class MockChoice(object):

    def __init__(self, data):
        self.pk = self.id = data.get('pk')
        self.text = data.get('text')
        self.position = data.get('position', 0)
        self.data = data