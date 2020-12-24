# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/layout/prompt.py
# Compiled at: 2019-08-15 23:53:38
# Size of source mod 2**32: 3238 bytes
from __future__ import unicode_literals
from six import text_type
from prompt_tool_kit.enums import IncrementalSearchDirection, SEARCH_BUFFER
from prompt_tool_kit.token import Token
from .utils import token_list_len
from .processors import Processor, Transformation
__all__ = ('DefaultPrompt', )

class DefaultPrompt(Processor):
    """DefaultPrompt"""

    def __init__(self, get_tokens):
        assert callable(get_tokens)
        self.get_tokens = get_tokens

    @classmethod
    def from_message(cls, message='> '):
        """
        Create a default prompt with a static message text.
        """
        assert isinstance(message, text_type)

        def get_message_tokens(cli):
            return [
             (
              Token.Prompt, message)]

        return cls(get_message_tokens)

    def apply_transformation(self, cli, document, lineno, source_to_display, tokens):
        if cli.is_searching:
            before = _get_isearch_tokens(cli)
        else:
            if cli.input_processor.arg is not None:
                before = _get_arg_tokens(cli)
            else:
                before = self.get_tokens(cli)
        shift_position = token_list_len(before)
        if lineno != 0:
            before = [
             (
              Token.Prompt, ' ' * shift_position)]
        return Transformation(tokens=(before + tokens),
          source_to_display=(lambda i: i + shift_position),
          display_to_source=(lambda i: i - shift_position))

    def has_focus(self, cli):
        return cli.is_searching


def _get_isearch_tokens(cli):

    def before():
        if cli.search_state.direction == IncrementalSearchDirection.BACKWARD:
            text = 'reverse-i-search'
        else:
            text = 'i-search'
        return [
         (
          Token.Prompt.Search, '(%s)`' % text)]

    def text():
        return [
         (
          Token.Prompt.Search.Text, cli.buffers[SEARCH_BUFFER].text)]

    def after():
        return [
         (
          Token.Prompt.Search, '`: ')]

    return before() + text() + after()


def _get_arg_tokens(cli):
    """
    Tokens for the arg-prompt.
    """
    arg = cli.input_processor.arg
    return [
     (
      Token.Prompt.Arg, '(arg: '),
     (
      Token.Prompt.Arg.Text, str(arg)),
     (
      Token.Prompt.Arg, ') ')]