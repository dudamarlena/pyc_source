# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/python_inquirer/prompts/common.py
# Compiled at: 2019-08-16 00:20:51
# Size of source mod 2**32: 3000 bytes
"""
common prompt functionality
"""
import sys
from prompt_tool_kit.validation import Validator, ValidationError
from prompt_tool_kit.styles import style_from_dict
from prompt_tool_kit.token import Token
from prompt_tool_kit.mouse_events import MouseEventTypes
PY3 = sys.version_info[0] >= 3
if PY3:
    basestring = str

def if_mousedown(handler):

    def handle_if_mouse_down(cli, mouse_event):
        if mouse_event.event_type == MouseEventTypes.MOUSE_DOWN:
            return handler(cli, mouse_event)
        else:
            return NotImplemented

    return handle_if_mouse_down


def setup_validator(kwargs):
    validate_prompt = kwargs.pop('validate', None)
    if validate_prompt:
        if issubclass(validate_prompt, Validator):
            kwargs['validator'] = validate_prompt()
        else:
            if callable(validate_prompt):

                class _InputValidator(Validator):

                    def validate(self, document):
                        verdict = validate_prompt(document.text)
                        if isinstance(verdict, basestring):
                            raise ValidationError(message=verdict,
                              cursor_position=(len(document.text)))
                        elif verdict is not True:
                            raise ValidationError(message='invalid input',
                              cursor_position=(len(document.text)))

                kwargs['validator'] = _InputValidator()
        return kwargs['validator']


def setup_simple_validator(kwargs):
    validate = kwargs.pop('validate', None)
    if validate is None:

        def _always(answer):
            return True

        return _always
    else:
        if not callable(validate):
            raise ValueError('Here a simple validate function is expected, no class')

        def _validator(answer):
            verdict = validate(answer)
            if isinstance(verdict, basestring):
                raise ValidationError(message=verdict)
            elif verdict is not True:
                raise ValidationError(message='invalid input')

        return _validator


default_style = style_from_dict({Token.Separator: '#6C6C6C', 
 Token.QuestionMark: '#5F819D', 
 Token.Selected: '', 
 Token.Pointer: '#FF9D00 bold', 
 Token.Instruction: '', 
 Token.Answer: '#FF9D00 bold', 
 Token.Question: 'bold'})