# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/snipsskills/utils/wizard.py
# Compiled at: 2017-09-06 12:21:23


class Wizard(object):

    def __init__(self):
        self._questions = list()

    def __len__(self):
        return len(self._questions)

    def __getitem__(self, position):
        return self._questions[position]

    def add_question(self, text, description, input_function, input_validation, default_value=None):
        question = Question(text=text, description=description, input_function=input_function, input_validation=input_validation, default_value=default_value)
        self._questions.append(question)

    def run(self):
        return [ question.answer() for question in self._questions ]


class Question(object):

    def __init__(self, text, description, input_function, input_validation, default_value=None):
        self.text = text
        self.description = description
        self.input_function = input_function
        self.input_validation = input_validation
        self.default_value = default_value

    def answer(self):
        if len(self.description) > 0:
            print self.description
        result = (self.default_value or self.input_function)(self.text) if 1 else self.input_function(self.text, self.default_value)
        while not self.input_validation(result):
            result = (self.default_value or self.input_function)(self.text) if 1 else self.input_function(self.text, self.default_val)

        return result