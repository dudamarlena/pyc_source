# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/colin/Projects/pyqode.core/pyqode/core/modes/pygments_sh.py
# Compiled at: 2016-12-29 05:31:31
# Size of source mod 2**32: 14333 bytes
"""
This module contains Syntax Highlighting mode and the QSyntaxHighlighter based
on pygments.

.. note: This code is taken and adapted from the IPython project.
"""
import logging, mimetypes, sys
from pygments.formatters.html import HtmlFormatter
from pygments.lexer import Error, RegexLexer, Text, _TokenType
from pygments.lexers import get_lexer_for_filename, get_lexer_for_mimetype
from pygments.lexers.agile import PythonLexer
from pygments.lexers.compiled import CLexer, CppLexer
from pygments.lexers.dotnet import CSharpLexer
from pygments.lexers.special import TextLexer
from pygments.styles import get_style_by_name, get_all_styles
from pygments.token import Whitespace, Comment, Token
from pygments.util import ClassNotFound
from pyqode.qt import QtGui
from pyqode.qt.QtCore import QRegExp
from pyqode.core.api.syntax_highlighter import SyntaxHighlighter, ColorScheme, TextBlockUserData

def _logger():
    """ Returns the module's logger """
    return logging.getLogger(__name__)


PYGMENTS_STYLES = sorted(list(get_all_styles()))
if hasattr(sys, 'frozen'):
    PYGMENTS_STYLES += ['darcula', 'qt']

def get_tokens_unprocessed(self, text, stack=('root', )):
    """ Split ``text`` into (tokentype, text) pairs.

        Monkeypatched to store the final stack on the object itself.
    """
    pos = 0
    tokendefs = self._tokens
    if hasattr(self, '_saved_state_stack'):
        statestack = list(self._saved_state_stack)
    else:
        statestack = list(stack)
    statetokens = tokendefs[statestack[(-1)]]
    while True:
        for rexmatch, action, new_state in statetokens:
            m = rexmatch(text, pos)
            if m:
                if action is not None:
                    if type(action) is _TokenType:
                        yield (
                         pos, action, m.group())
                    else:
                        for item in action(self, m):
                            yield item

                    pos = m.end()
                    if new_state is not None:
                        if isinstance(new_state, tuple):
                            for state in new_state:
                                if state == '#pop':
                                    statestack.pop()
                                else:
                                    if state == '#push':
                                        statestack.append(statestack[(-1)])
                                    else:
                                        statestack.append(state)

                        else:
                            if isinstance(new_state, int):
                                del statestack[new_state:]
                            else:
                                if new_state == '#push':
                                    statestack.append(statestack[(-1)])
                                elif not False:
                                    raise AssertionError('wrong state def: %r' % new_state)
                                statetokens = tokendefs[statestack[(-1)]]
                            break
        else:
            try:
                if text[pos] == '\n':
                    pos += 1
                    statestack = ['root']
                    statetokens = tokendefs['root']
                    yield (pos, Text, '\n')
                    continue
                yield (
                 pos, Error, text[pos])
                pos += 1
            except IndexError:
                break

    self._saved_state_stack = list(statestack)


RegexLexer.get_tokens_unprocessed = get_tokens_unprocessed

def replace_pattern(tokens, new_pattern):
    """ Given a RegexLexer token dictionary 'tokens', replace all patterns that
        match the token specified in 'new_pattern' with 'new_pattern'.
    """
    for state in tokens.values():
        for index, pattern in enumerate(state):
            if isinstance(pattern, tuple) and pattern[1] == new_pattern[1]:
                state[index] = new_pattern


COMMENT_START = (
 '/\\*', Comment.Multiline, 'comment')
COMMENT_STATE = [('[^*/]', Comment.Multiline),
 (
  '/\\*', Comment.Multiline, '#push'),
 (
  '\\*/', Comment.Multiline, '#pop'),
 (
  '[*/]', Comment.Multiline)]
replace_pattern(CLexer.tokens, COMMENT_START)
replace_pattern(CppLexer.tokens, COMMENT_START)
CLexer.tokens['comment'] = COMMENT_STATE
CppLexer.tokens['comment'] = COMMENT_STATE
CSharpLexer.tokens['comment'] = COMMENT_STATE

class PygmentsSH(SyntaxHighlighter):
    __doc__ = ' Highlights code using the pygments parser.\n\n    This mode enable syntax highlighting using the pygments library. This is a\n    generic syntax highlighter, it is slower than a native highlighter and\n    does not do any code folding detection. Use it as a fallback for languages\n    that do not have a native highlighter available. Check the other pyqode\n    namespace packages to see what other languages are available (at the time\n    of writing, only python has specialised support).\n\n    .. warning:: There are some issues with multi-line comments, they are not\n                 properly highlighted until a full re-highlight is triggered.\n                 The text is automatically re-highlighted on save.\n    '
    DESCRIPTION = 'Apply syntax highlighting to the editor using pygments'

    @property
    def pygments_style(self):
        """
        Gets/Sets the pygments style
        """
        return self.color_scheme.name

    @pygments_style.setter
    def pygments_style(self, value):
        self._pygments_style = value
        self._update_style()
        self.color_scheme = ColorScheme(value)

    def __init__(self, document, lexer=None, color_scheme=None):
        super(PygmentsSH, self).__init__(document, color_scheme=color_scheme)
        self._pygments_style = self.color_scheme.name
        self._style = None
        self._formatter = HtmlFormatter(nowrap=True)
        self._lexer = lexer if lexer else PythonLexer()
        self._brushes = {}
        self._formats = {}
        self._init_style()
        self._prev_block = None

    def _init_style(self):
        """ Init pygments style """
        self._update_style()

    def on_install(self, editor):
        """
        :type editor: pyqode.code.api.CodeEdit
        """
        self._clear_caches()
        self._update_style()
        super(PygmentsSH, self).on_install(editor)

    def set_mime_type(self, mime_type):
        """
        Update the highlighter lexer based on a mime type.

        :param mime_type: mime type of the new lexer to setup.
        """
        try:
            self.set_lexer_from_mime_type(mime_type)
        except ClassNotFound:
            _logger().exception('failed to get lexer from mimetype')
            self._lexer = TextLexer()
            return False
        except ImportError:
            _logger().warning('failed to get lexer from mimetype (%s)' % mime_type)
            self._lexer = TextLexer()
            return False
        else:
            return True

    def set_lexer_from_filename(self, filename):
        """
        Change the lexer based on the filename (actually only the extension is
        needed)

        :param filename: Filename or extension
        """
        self._lexer = None
        if filename.endswith('~'):
            filename = filename[0:len(filename) - 1]
        try:
            self._lexer = get_lexer_for_filename(filename)
        except (ClassNotFound, ImportError):
            print('class not found for url', filename)
            try:
                m = mimetypes.guess_type(filename)
                print(m)
                self._lexer = get_lexer_for_mimetype(m[0])
            except (ClassNotFound, IndexError, ImportError):
                self._lexer = get_lexer_for_mimetype('text/plain')

        if self._lexer is None:
            _logger().warning('failed to get lexer from filename: %s, using plain text instead...', filename)
            self._lexer = TextLexer()

    def set_lexer_from_mime_type(self, mime, **options):
        """
        Sets the pygments lexer from mime type.

        :param mime: mime type
        :param options: optional addtional options.
        """
        self._lexer = get_lexer_for_mimetype(mime, **options)
        _logger().debug('lexer for mimetype (%s): %r', mime, self._lexer)

    def highlight_block(self, text, block):
        """
        Highlights the block using a pygments lexer.

        :param text: text of the block to highlith
        :param block: block to highlight
        """
        if self.color_scheme.name != self._pygments_style:
            self._pygments_style = self.color_scheme.name
            self._update_style()
        original_text = text
        if self.editor and self._lexer and self.enabled:
            if block.blockNumber():
                prev_data = self._prev_block.userData()
                if prev_data:
                    if hasattr(prev_data, 'syntax_stack'):
                        pass
                self._lexer._saved_state_stack = prev_data.syntax_stack
        else:
            if hasattr(self._lexer, '_saved_state_stack'):
                del self._lexer._saved_state_stack
            index = 0
            usd = block.userData()
            if usd is None:
                usd = TextBlockUserData()
                block.setUserData(usd)
            tokens = list(self._lexer.get_tokens(text))
            for token, text in tokens:
                length = len(text)
                fmt = self._get_format(token)
                if token in [Token.Literal.String, Token.Literal.String.Doc,
                 Token.Comment]:
                    fmt.setObjectType(fmt.UserObject)
                self.setFormat(index, length, fmt)
                index += length

            if hasattr(self._lexer, '_saved_state_stack'):
                setattr(usd, 'syntax_stack', self._lexer._saved_state_stack)
                del self._lexer._saved_state_stack
            text = original_text
            expression = QRegExp('\\s+')
            index = expression.indexIn(text, 0)
            while index >= 0:
                index = expression.pos(0)
                length = len(expression.cap(0))
                self.setFormat(index, length, self._get_format(Whitespace))
                index = expression.indexIn(text, index + length)

            self._prev_block = block

    def _update_style(self):
        """ Sets the style to the specified Pygments style.
        """
        try:
            self._style = get_style_by_name(self._pygments_style)
        except ClassNotFound:
            if self._pygments_style == 'qt':
                from pyqode.core.styles import QtStyle
                self._style = QtStyle
            else:
                if self._pygments_style == 'darcula':
                    from pyqode.core.styles import DarculaStyle
                    self._style = DarculaStyle
                else:
                    self._style = get_style_by_name('default')
                    self._pygments_style = 'default'

        self._clear_caches()

    def _clear_caches(self):
        """ Clear caches for brushes and formats.
        """
        self._brushes.clear()
        self._formats.clear()

    def _get_format(self, token):
        """ Returns a QTextCharFormat for token or None.
        """
        if token == Whitespace:
            return self.editor.whitespaces_foreground
        if token in self._formats:
            return self._formats[token]
        result = self._get_format_from_style(token, self._style)
        self._formats[token] = result
        return result

    def _get_format_from_style(self, token, style):
        """ Returns a QTextCharFormat for token by reading a Pygments style.
        """
        result = QtGui.QTextCharFormat()
        try:
            style = style.style_for_token(token)
        except KeyError:
            style = style.style_for_token(Text)

        for key, value in list(style.items()):
            if value:
                if key == 'color':
                    result.setForeground(self._get_brush(value))
                else:
                    if key == 'bgcolor':
                        result.setBackground(self._get_brush(value))
                    else:
                        if key == 'bold':
                            result.setFontWeight(QtGui.QFont.Bold)
                        else:
                            if key == 'italic':
                                result.setFontItalic(True)
                            else:
                                if key == 'underline':
                                    result.setUnderlineStyle(QtGui.QTextCharFormat.SingleUnderline)
                                else:
                                    if key == 'sans':
                                        result.setFontStyleHint(QtGui.QFont.SansSerif)
                                    else:
                                        if key == 'roman':
                                            result.setFontStyleHint(QtGui.QFont.Times)
                                        elif key == 'mono':
                                            result.setFontStyleHint(QtGui.QFont.TypeWriter)

        return result

    def _get_brush(self, color):
        """ Returns a brush for the color.
        """
        result = self._brushes.get(color)
        if result is None:
            qcolor = self._get_color(color)
            result = QtGui.QBrush(qcolor)
            self._brushes[color] = result
        return result

    @staticmethod
    def _get_color(color):
        """ Returns a QColor built from a Pygments color string.
        """
        color = str(color).replace('#', '')
        qcolor = QtGui.QColor()
        qcolor.setRgb(int(color[:2], base=16), int(color[2:4], base=16), int(color[4:6], base=16))
        return qcolor