# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/python_inquirer/prompts/list.py
# Compiled at: 2019-08-16 00:20:51
# Size of source mod 2**32: 6321 bytes
"""
`list` type question
"""
from __future__ import print_function
from __future__ import unicode_literals
import sys
from prompt_tool_kit.application import Application
from prompt_tool_kit.key_binding.manager import KeyBindingManager
from prompt_tool_kit.keys import Keys
from prompt_tool_kit.layout.containers import Window
from prompt_tool_kit.filters import IsDone
from prompt_tool_kit.layout.controls import TokenListControl
from prompt_tool_kit.layout.containers import ConditionalContainer, ScrollOffsets, HSplit
from prompt_tool_kit.layout.dimension import LayoutDimension as D
from prompt_tool_kit.token import Token
from .. import PromptParameterException
from ..separator import Separator
from .common import if_mousedown, default_style
PY3 = sys.version_info[0] >= 3
if PY3:
    basestring = str

class InquirerControl(TokenListControl):

    def __init__(self, choices, **kwargs):
        self.selected_option_index = 0
        self.answered = False
        self.choices = choices
        self._init_choices(choices)
        (super(InquirerControl, self).__init__)((self._get_choice_tokens), **kwargs)

    def _init_choices(self, choices, default=None):
        self.choices = []
        searching_first_choice = True
        for i, c in enumerate(choices):
            if isinstance(c, Separator):
                self.choices.append((c, None, None))
            else:
                if isinstance(c, basestring):
                    self.choices.append((c, c, None))
                else:
                    name = c.get('name')
                    value = c.get('value', name)
                    disabled = c.get('disabled', None)
                    self.choices.append((name, value, disabled))
                if searching_first_choice:
                    self.selected_option_index = i
                    searching_first_choice = False

    @property
    def choice_count(self):
        return len(self.choices)

    def _get_choice_tokens(self, cli):
        tokens = []
        T = Token

        def append(index, choice):
            selected = index == self.selected_option_index

            @if_mousedown
            def select_item(cli, mouse_event):
                self.selected_option_index = index
                self.answered = True
                cli.set_return_value(self.get_selection()[0])

            tokens.append((T.Pointer if selected else T,
             ' ❯ ' if selected else '   '))
            if selected:
                tokens.append((Token.SetCursorPosition, ''))
            else:
                if choice[2]:
                    tokens.append((T.Selected if selected else T,
                     '- %s (%s)' % (choice[0], choice[2])))
                else:
                    try:
                        tokens.append((T.Selected if selected else T, str(choice[0]),
                         select_item))
                    except:
                        tokens.append((T.Selected if selected else T, choice[0],
                         select_item))

            tokens.append((T, '\n'))

        for i, choice in enumerate(self.choices):
            append(i, choice)

        tokens.pop()
        return tokens

    def get_selection(self):
        return self.choices[self.selected_option_index]


def question(message, **kwargs):
    if 'choices' not in kwargs:
        raise PromptParameterException('choices')
    choices = kwargs.pop('choices', None)
    default = kwargs.pop('default', 0)
    qmark = kwargs.pop('qmark', '?')
    style = kwargs.pop('style', default_style)
    ic = InquirerControl(choices)

    def get_prompt_tokens(cli):
        tokens = []
        tokens.append((Token.QuestionMark, qmark))
        tokens.append((Token.Question, ' %s ' % message))
        if ic.answered:
            tokens.append((Token.Answer, ' ' + ic.get_selection()[0]))
        else:
            tokens.append((Token.Instruction, ' (Use arrow keys)'))
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

    @manager.registry.add_binding((Keys.Down), eager=True)
    def move_cursor_down(event):

        def _next():
            ic.selected_option_index = (ic.selected_option_index + 1) % ic.choice_count

        _next()
        while isinstance(ic.choices[ic.selected_option_index][0], Separator) or ic.choices[ic.selected_option_index][2]:
            _next()

    @manager.registry.add_binding((Keys.Up), eager=True)
    def move_cursor_up(event):

        def _prev():
            ic.selected_option_index = (ic.selected_option_index - 1) % ic.choice_count

        _prev()
        while isinstance(ic.choices[ic.selected_option_index][0], Separator) or ic.choices[ic.selected_option_index][2]:
            _prev()

    @manager.registry.add_binding((Keys.Enter), eager=True)
    def set_answer(event):
        ic.answered = True
        event.cli.set_return_value(ic.get_selection()[1])

    return Application(layout=layout,
      key_bindings_registry=(manager.registry),
      mouse_support=True,
      style=style)