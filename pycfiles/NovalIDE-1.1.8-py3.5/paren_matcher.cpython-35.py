# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/plugins/paren_matcher.py
# Compiled at: 2019-08-16 02:55:35
# Size of source mod 2**32: 6676 bytes
import io, tokenize, noval.util.utils as utils
from noval import GetApp
import noval.iface as iface, noval.plugin as plugin
from noval.editor.code import CodeCtrl
_OPENERS = {')': '(', ']': '[', '}': '{'}
if utils.is_py2():
    from token import tok_name
    import collections

    class TokenInfo(collections.namedtuple('TokenInfo', 'type string start end line')):

        def __repr__(self):
            annotated_type = '%d (%s)' % (self.type, tok_name[self.type])
            return 'TokenInfo(type=%s, string=%r, start=%r, end=%r, line=%r)' % self._replace(type=annotated_type)

        @property
        def exact_type(self):
            if self.type == OP and self.string in EXACT_TOKEN_TYPES:
                return EXACT_TOKEN_TYPES[self.string]
            else:
                return self.type


    class TokenParser:

        def __init__(self, tokens):
            self.tokens = tokens

        def __call__(self, type, token, srow_scol, erow_ecol, line):
            srow, scol = srow_scol
            erow, ecol = erow_ecol
            self.tokens.append(TokenInfo(type, token, srow_scol, erow_ecol, line))


class ParenMatcher:

    def __init__(self, text):
        self.text = text
        self._update_scheduled = False

    def schedule_update(self):

        def perform_update():
            try:
                self.update_highlighting()
            finally:
                self._update_scheduled = False

        if not self._update_scheduled:
            self._update_scheduled = True
            self.text.after_idle(perform_update)

    def update_highlighting(self):
        self.text.tag_remove('surrounding_parens', '0.1', 'end')
        self.text.tag_remove('unclosed_expression', '0.1', 'end')
        if utils.profile_get_int('TextHighlightParentheses', True):
            self._update_highlighting_for_active_range()

    def _update_highlighting_for_active_range(self):
        start_index = '1.0'
        end_index = self.text.index('end')
        remaining = self._highlight_surrounding(start_index, end_index)
        self._highlight_unclosed(remaining, start_index, end_index)

    def _highlight_surrounding(self, start_index, end_index):
        open_index, close_index, remaining = self.find_surrounding(start_index, end_index)
        if None not in [open_index, close_index]:
            self.text.tag_add('surrounding_parens', open_index)
            self.text.tag_add('surrounding_parens', close_index)
        return remaining

    def _highlight_unclosed(self, remaining, start_index, end_index):
        if len(remaining) > 0:
            opener = remaining[0]
            open_index = '%d.%d' % (opener.start[0], opener.start[1])
            self.text.tag_add('unclosed_expression', open_index, end_index)

    def _get_paren_tokens(self, source):
        result = []
        try:
            tokens = []
            if utils.is_py2():
                tokenize.tokenize(io.BytesIO(source.encode('utf-8')).readline, TokenParser(tokens))
            elif utils.is_py3_plus():
                tokens = tokenize.tokenize(io.BytesIO(source.encode('utf-8')).readline)
            for token in tokens:
                if token.string != '' and token.string in '()[]{}':
                    result.append(token)

        except Exception as e:
            utils.get_logger().exception('')

        return result

    def find_surrounding(self, start_index, end_index):
        stack = []
        opener, closer = (None, None)
        open_index, close_index = (None, None)
        start_row, start_col = map(int, start_index.split('.'))
        source = self.text.get(start_index, end_index)
        source = '\n' * (start_row - 1) + ' ' * start_col + source
        for t in self._get_paren_tokens(source):
            if t.string == '' or t.string not in '()[]{}':
                pass
            else:
                if t.string in '([{':
                    stack.append(t)
                elif len(stack) > 0:
                    if stack[(-1)].string != _OPENERS[t.string]:
                        pass
                    elif not closer:
                        opener = stack.pop()
                        open_index = '%d.%d' % (opener.start[0], opener.start[1])
                        token_index = '%d.%d' % (t.start[0], t.start[1])
                        if self._is_insert_between_indices(open_index, token_index):
                            closer = t
                            close_index = token_index
                        else:
                            stack.pop()

        return (
         open_index, close_index, stack)

    def _is_insert_between_indices(self, index1, index2):
        return self.text.compare('insert', '>=', index1) and self.text.compare('insert-1c', '<=', index2)


class ShellParenMatcher(ParenMatcher):

    def _update_highlighting_for_active_range(self):
        index_parts = self.text.tag_prevrange('command', 'end')
        if index_parts:
            start_index, end_index = index_parts
            remaining = self._highlight_surrounding(start_index, end_index)
            self._highlight_unclosed(remaining, start_index, 'end')


def update_highlighting(event=None):
    text = event.widget
    if not hasattr(text, 'paren_matcher'):
        if isinstance(text, CodeCtrl):
            text.paren_matcher = ParenMatcher(text)
    else:
        return
    text.paren_matcher.schedule_update()


class ParenMatcherPluginLoader(plugin.Plugin):
    plugin.Implements(iface.CommonPluginI)

    def Load(self):
        wb = GetApp()
        wb.bind_class('CodeCtrl', '<<CursorMove>>', update_highlighting, True)
        wb.bind_class('CodeCtrl', '<<TextChange>>', update_highlighting, True)
        wb.bind('<<UpdateAppearance>>', update_highlighting, True)