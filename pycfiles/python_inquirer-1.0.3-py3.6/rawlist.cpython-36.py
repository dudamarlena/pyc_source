# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/python_inquirer/prompts/rawlist.py
# Compiled at: 2019-08-16 00:19:35
# Size of source mod 2**32: 5461 bytes
"""
`rawlist` type question
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

    def __init__(self, choices, **kwargs):
        self.pointer_index = 0
        self.answered = False
        self._init_choices(choices)
        (super(InquirerControl, self).__init__)((self._get_choice_tokens), **kwargs)

    def _init_choices(self, choices):
        self.choices = []
        searching_first_choice = True
        key = 1
        for i, c in enumerate(choices):
            if isinstance(c, Separator):
                self.choices.append(c)
            else:
                if isinstance(c, basestring):
                    self.choices.append((key, c, c))
                    key += 1
                if searching_first_choice:
                    self.pointer_index = i
                    searching_first_choice = False

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
                    tokens.append((T.Selected, '  %d) %s' % (key, line),
                     select_item))
                else:
                    tokens.append((T, '  %d) %s' % (key, line),
                     select_item))
                tokens.append((T, '\n'))

        for i, choice in enumerate(self.choices):
            _append(i, choice)

        tokens.append((T, '  Answer: %d' % self.choices[self.pointer_index][0]))
        return tokens

    def get_selected_value(self):
        return self.choices[self.pointer_index][2]


def question(message, **kwargs):
    if 'choices' not in kwargs:
        raise PromptParameterException('choices')
    qmark = kwargs.pop('qmark', '?')
    choices = kwargs.pop('choices', None)
    if len(choices) > 9:
        raise ValueError('rawlist supports only a maximum of 9 choices!')
    style = kwargs.pop('style', default_style)
    ic = InquirerControl(choices)

    def get_prompt_tokens(cli):
        tokens = []
        T = Token
        tokens.append((T.QuestionMark, qmark))
        tokens.append((T.Question, ' %s ' % message))
        if ic.answered:
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

            _reg_binding(i, '%d' % c[0])

    @manager.registry.add_binding((Keys.Enter), eager=True)
    def set_answer(event):
        ic.answered = True
        event.cli.set_return_value(ic.get_selected_value())

    return Application(layout=layout,
      key_bindings_registry=(manager.registry),
      mouse_support=True,
      style=style)