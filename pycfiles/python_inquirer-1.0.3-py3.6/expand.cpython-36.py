# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/python_inquirer/prompts/expand.py
# Compiled at: 2019-08-16 00:20:51
# Size of source mod 2**32: 6662 bytes
"""
`expand` type question
"""
from __future__ import print_function, unicode_literals
import sys
from prompt_tool_kit.application import Application
from prompt_tool_kit.key_binding.manager import KeyBindingManager
from prompt_tool_kit.keys import Keys
from prompt_tool_kit.layout.containers import Window
from prompt_tool_kit.filters import IsDone
from prompt_tool_kit.layout.controls import TokenListControl
from prompt_tool_kit.layout.containers import ConditionalContainer, HSplit
from prompt_tool_kit.layout.dimension import LayoutDimension as D
from prompt_tool_kit.token import Token
from .. import PromptParameterException
from ..separator import Separator
from .common import default_style
from .common import if_mousedown
PY3 = sys.version_info[0] >= 3
if PY3:
    basestring = str

class InquirerControl(TokenListControl):

    def __init__(self, choices, default=None, **kwargs):
        self.pointer_index = 0
        self.answered = False
        self._init_choices(choices, default)
        self._help_active = False
        (super(InquirerControl, self).__init__)((self._get_choice_tokens), **kwargs)

    def _init_choices(self, choices, default=None):
        self.choices = []
        for i, c in enumerate(choices):
            if isinstance(c, Separator):
                self.choices.append(c)
            elif isinstance(c, basestring):
                self.choices.append((key, c, c))
            else:
                key = c.get('key')
                name = c.get('name')
                value = c.get('value', name)
                self.choices.append([key, name, value])

        self.choices.append(['h', 'Help, list all options', '__HELP__'])
        for i, choice in enumerate(self.choices):
            if isinstance(choice, list):
                key = choice[0]
                default = default or 'h'
                if default == key:
                    self.pointer_index = i
                    choice[0] = key.upper()

    @property
    def choice_count(self):
        return len(self.choices)

    def _get_choice_tokens(self, cli):
        tokens = []
        T = Token

        def _append(index, line):
            if isinstance(line, Separator):
                tokens.append((T.Separator, '   %s\n' % line))
            else:
                key = line[0]
                line = line[1]
                pointed_at = index == self.pointer_index

                @if_mousedown
                def select_item(cli, mouse_event):
                    self.pointer_index = index

                if pointed_at:
                    tokens.append((T.Selected, '  %s) %s' % (key, line),
                     select_item))
                else:
                    tokens.append((T, '  %s) %s' % (key, line),
                     select_item))
                tokens.append((T, '\n'))

        if self._help_active:
            for i, choice in enumerate(self.choices):
                _append(i, choice)

            tokens.append((T,
             '  Answer: %s' % self.choices[self.pointer_index][0]))
        else:
            tokens.append((T.Pointer, '>> '))
            tokens.append((T, self.choices[self.pointer_index][1]))
        return tokens

    def get_selected_value(self):
        return self.choices[self.pointer_index][2]


def question(message, **kwargs):
    if 'choices' not in kwargs:
        raise PromptParameterException('choices')
    choices = kwargs.pop('choices', None)
    default = kwargs.pop('default', None)
    qmark = kwargs.pop('qmark', '?')
    style = kwargs.pop('style', default_style)
    ic = InquirerControl(choices, default)

    def get_prompt_tokens(cli):
        tokens = []
        T = Token
        tokens.append((T.QuestionMark, qmark))
        tokens.append((T.Question, ' %s ' % message))
        if not ic.answered:
            tokens.append((T.Instruction,
             ' (%s)' % ''.join([k[0] for k in ic.choices if not isinstance(k, Separator)])))
        else:
            tokens.append((T.Answer, ' %s' % ic.get_selected_value()))
        return tokens

    layout = HSplit([
     Window(height=(D.exact(1)), content=(TokenListControl(get_prompt_tokens))),
     ConditionalContainer((Window(ic)),
       filter=(~IsDone()))])
    manager = KeyBindingManager.for_prompt()

    @manager.registry.add_binding((Keys.ControlQ), eager=True)
    @manager.registry.add_binding((Keys.ControlC), eager=True)
    def _(event):
        raise KeyboardInterrupt()

    for i, c in enumerate(ic.choices):
        if not isinstance(c, Separator):

            def _reg_binding(i, keys):

                @manager.registry.add_binding(keys, eager=True)
                def select_choice(event):
                    ic.pointer_index = i

            if c[0] not in ('h', 'H'):
                _reg_binding(i, c[0])
                if c[0].isupper():
                    _reg_binding(i, c[0].lower())

    @manager.registry.add_binding('H', eager=True)
    @manager.registry.add_binding('h', eager=True)
    def help_choice(event):
        ic._help_active = True

    @manager.registry.add_binding((Keys.Enter), eager=True)
    def set_answer(event):
        selected_value = ic.get_selected_value()
        if selected_value == '__HELP__':
            ic._help_active = True
        else:
            ic.answered = True
            event.cli.set_return_value(selected_value)

    return Application(layout=layout,
      key_bindings_registry=(manager.registry),
      mouse_support=True,
      style=style)