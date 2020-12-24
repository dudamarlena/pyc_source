# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/python_inquirer/prompts/confirm.py
# Compiled at: 2019-08-16 00:20:51
# Size of source mod 2**32: 2631 bytes
"""
confirm type question
"""
from __future__ import print_function, unicode_literals
from prompt_tool_kit.application import Application
from prompt_tool_kit.key_binding.manager import KeyBindingManager
from prompt_tool_kit.keys import Keys
from prompt_tool_kit.layout.containers import Window, HSplit
from prompt_tool_kit.layout.controls import TokenListControl
from prompt_tool_kit.layout.dimension import LayoutDimension as D
from prompt_tool_kit.token import Token
from prompt_tool_kit.shortcuts import create_prompt_application
from prompt_tool_kit.styles import style_from_dict

def question(message, **kwargs):
    default = kwargs.pop('default', True)
    style = kwargs.pop('style', style_from_dict({Token.QuestionMark: '#5F819D', 
     Token.Instruction: '', 
     Token.Answer: '#FF9D00 bold', 
     Token.Question: 'bold'}))
    status = {'answer': None}
    qmark = kwargs.pop('qmark', '?')

    def get_prompt_tokens(cli):
        tokens = []
        tokens.append((Token.QuestionMark, qmark))
        tokens.append((Token.Question, ' %s ' % message))
        if isinstance(status['answer'], bool):
            tokens.append((Token.Answer, ' Yes' if status['answer'] else ' No'))
        else:
            if default:
                instruction = ' (Y/n)'
            else:
                instruction = ' (y/N)'
            tokens.append((Token.Instruction, instruction))
        return tokens

    manager = KeyBindingManager.for_prompt()

    @manager.registry.add_binding((Keys.ControlQ), eager=True)
    @manager.registry.add_binding((Keys.ControlC), eager=True)
    def _(event):
        raise KeyboardInterrupt()

    @manager.registry.add_binding('n')
    @manager.registry.add_binding('N')
    def key_n(event):
        status['answer'] = False
        event.cli.set_return_value(False)

    @manager.registry.add_binding('y')
    @manager.registry.add_binding('Y')
    def key_y(event):
        status['answer'] = True
        event.cli.set_return_value(True)

    @manager.registry.add_binding((Keys.Enter), eager=True)
    def set_answer(event):
        status['answer'] = default
        event.cli.set_return_value(default)

    return create_prompt_application(get_prompt_tokens=get_prompt_tokens,
      key_bindings_registry=(manager.registry),
      mouse_support=False,
      style=style,
      erase_when_done=False)