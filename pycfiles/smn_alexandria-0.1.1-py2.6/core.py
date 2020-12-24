# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/alexandria/dsl/core.py
# Compiled at: 2011-04-12 08:10:56
from validators import always_true
from exceptions import InvalidInputException
from utils import msg, coroutine
from contextlib import contextmanager
from generator_tools.copygenerators import copy_generator
import types, logging
from logging.handlers import TimedRotatingFileHandler
import copy

class MenuSystem(object):

    def __init__(self, *items):
        self.stack = list(items)
        self.__iter_index = 0

    def clone(self, **kwargs):
        """
        Clone self, always return a clone instead of self when chaining
        methods, otherwise you'll get lots of confusing behaviour because
        vars are passed by reference
        """
        clone = self.__class__.__new__(self.__class__)
        clone.__iter_index = self.__iter_index
        clone.stack = map(copy_generator, self.stack)
        return clone

    def append(self, *items):
        """
        Clone the stack and append *items to it. Appended items need to be
        coroutines.
        """
        self.stack.extend(list(items))
        clone = self.clone()
        return clone

    def __iter__(self):
        return self

    def get_current_index(self):
        return self.__iter_index

    def fast_forward(self, index):
        """
        Fast forward to the given index in the stack.
        
        TODO:   how will we go about this when menu's become tree structures 
                instead of linear paths?
        """
        self.__iter_index = index

    def repeat_current_item(self):
        """
        Repeat the current item, decrements the counter by one & calls 
        next() to repeat the current item.
        """
        self.fast_forward(self.__iter_index - 1)
        return self.next()

    def next_after(self, index):
        """
        Short hand for returning the next item in the stack
        """
        self.fast_forward(index)
        return self.next()

    def next(self):
        """
        Proceed to the next coroutine in the stack
        """
        if self.__iter_index > len(self.stack):
            raise StopIteration
        if self.__iter_index == len(self.stack):
            next_item = None
        else:
            next_item = copy_generator(self.stack[self.__iter_index])
        self.__iter_index += 1
        return (self.__iter_index, next_item)


def prompt(text, validator=always_true, save_as=None, options=(), parse=False):
    """
    Prompt the user with a question, possibly multiple choice. 
    Read the answer, validate it and store it in the session store.
    """
    save_as = save_as or text
    while True:
        (ms, session) = yield
        question = msg(text, options)
        if parse:
            question = question % session
        yield (
         question, False)
        answer = yield
        validated_answer = validator(answer, options)
        session[save_as] = validated_answer
        yield validated_answer


def end(text):
    """
    Sign-off the user with the given text. Ends the session
    """
    while True:
        (ms, session) = yield
        yield (
         text, True)


def case(*cases):
    """Returns the first prompt for which the test function returns True"""
    while True:
        (ms, session) = yield
        for (test, prompt) in cases:
            if test(ms, session):
                prompt = copy_generator(prompt)
                prompt.next()
                question = prompt.send((ms, session))
                yield question
                answer = yield
                prompt.next()
                validated_answer = prompt.send(answer)
                yield validated_answer

        yield (
         False, False)


def pick_first_unanswered(*prompts):
    """Returns the first prompt for which the storage doesn't have an
    answer stored yet."""
    cloned_prompts = map(copy_generator, prompts)
    while True:
        (ms, session) = yield
        while cloned_prompts:
            prompt = cloned_prompts.pop()
            prompt.next()
            (question, end_of_session) = prompt.send((ms, session))
            if not any([ question.startswith(key) for key in session ]):
                yield (
                 question, end_of_session)
                answer = yield
                prompt.next()
                validated_answer = prompt.send(answer)
                yield validated_answer
            else:
                logging.debug('already handled question %s' % question)

        yield (
         False, False)


def question(text, options):
    """
    Having python generate prompts & cases for us on the fly. We should probably
    look at ways of doing more of this or making it possible through the DSL.
    
    Example:

        MenuSystem(
            *question('Can traditional medicine cure HIV/AIDS?', {
                'no': 'Correct! Press 1 to continue.',
                'yes': 'Incorrect! Please check your answer and press 1 to continue'
            })
        )

    Is the same as:

        MenuSystem(
            prompt(_('Can traditional medicine cure HIV/AIDS?'), {
                'options': ('yes','no'),
                'validator': pick_one
            }),
            case(
                (
                    lambda (ms, session): session['Can traditional medicine cure HIV/AIDS?'] == ['1']),
                    prompt('Correct! Press 1 to continue.')
                ),
                (
                    lambda (ms, session): session['Can traditional medicine cure HIV/AIDS?'] != ['1']),
                    prompt('Incorrect! Please check your answer and press 1 to continue.')
                ),
            )
        )

    """

    def check_answer(question, answer):

        def _checker(ms, session):
            return session[question] == answer

        return _checker

    stack_list = []
    question_text = msg(text, options.keys())
    stack_list.append(prompt(text, options=options.keys()))
    case_list = []
    for (option, answer) in options.items():
        case_list.append((
         check_answer(text, option), prompt(answer)))

    stack_list.append(case(*case_list))
    return stack_list