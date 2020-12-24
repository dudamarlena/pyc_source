# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/python_inquirer/prompts/input.py
# Compiled at: 2019-08-16 00:20:51
# Size of source mod 2**32: 1714 bytes
"""
`input` type question
"""
from __future__ import print_function, unicode_literals
import inspect
from prompt_tool_kit.token import Token
from prompt_tool_kit.shortcuts import create_prompt_application
from prompt_tool_kit.validation import Validator, ValidationError
from prompt_tool_kit.layout.lexers import SimpleLexer
from .common import default_style

def question(message, **kwargs):
    default = kwargs.pop('default', '')
    validate_prompt = kwargs.pop('validate', None)
    if validate_prompt:
        if inspect.isclass(validate_prompt):
            if issubclass(validate_prompt, Validator):
                kwargs['validator'] = validate_prompt()
        if callable(validate_prompt):

            class _InputValidator(Validator):

                def validate(self, document):
                    verdict = validate_prompt(document.text)
                    if not verdict == True:
                        if verdict == False:
                            verdict = 'invalid input'
                        raise ValidationError(message=verdict,
                          cursor_position=(len(document.text)))

            kwargs['validator'] = _InputValidator()
    kwargs['style'] = kwargs.pop('style', default_style)
    qmark = kwargs.pop('qmark', '?')

    def _get_prompt_tokens(cli):
        return [
         (
          Token.QuestionMark, qmark),
         (
          Token.Question, ' %s  ' % message)]

    return create_prompt_application(get_prompt_tokens=_get_prompt_tokens, 
     lexer=SimpleLexer(Token.Answer), 
     default=default, **kwargs)