# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/colin/Projects/pyqode.core/pyqode/core/api/syntax_highlighter.py
# Compiled at: 2016-12-29 05:31:31
# Size of source mod 2**32: 13286 bytes
"""
This module contains the syntax highlighter API.
"""
import logging, sys, time, weakref
from pygments.styles import get_style_by_name, get_all_styles
from pygments.token import Token, Punctuation
from pygments.util import ClassNotFound
from pyqode.core.api.mode import Mode
from pyqode.core.api.utils import drift_color
from pyqode.qt import QtGui, QtCore, QtWidgets

def _logger():
    return logging.getLogger(__name__)


PYGMENTS_STYLES = sorted(set(list(get_all_styles()) + ['darcula', 'qt']))
COLOR_SCHEME_KEYS = {'background': None, 
 'highlight': None, 
 'normal': Token.Text, 
 'keyword': Token.Keyword, 
 'namespace': Token.Keyword.Namespace, 
 'type': Token.Keyword.Type, 
 'keyword_reserved': Token.Keyword.Reserved, 
 'builtin': Token.Name.Builtin, 
 'definition': Token.Name.Class, 
 'comment': Token.Comment, 
 'string': Token.Literal.String, 
 'docstring': Token.Literal.String.Doc, 
 'number': Token.Number, 
 'instance': Token.Name.Variable, 
 'whitespace': Token.Text.Whitespace, 
 'tag': Token.Name.Tag, 
 'self': Token.Name.Builtin.Pseudo, 
 'decorator': Token.Name.Decorator, 
 'punctuation': Punctuation, 
 'constant': Token.Name.Constant, 
 'function': Token.Name.Function, 
 'operator': Token.Operator, 
 'operator_word': Token.Operator.Word}

class ColorScheme(object):
    __doc__ = '\n    Translates a pygments style into a dictionary of colors associated with a\n    style key.\n\n    See :attr:`pyqode.core.api.syntax_highligter.COLOR_SCHEM_KEYS` for the\n    available keys.\n\n    '

    @property
    def name(self):
        """
        Name of the color scheme, this is usually the name of the associated
        pygments style.
        """
        return self._name

    @property
    def background(self):
        """
        Gets the background color.
        :return:
        """
        return self.formats['background'].background().color()

    @property
    def highlight(self):
        """
        Gets the highlight color.
        :return:
        """
        return self.formats['highlight'].background().color()

    def __init__(self, style):
        """
        :param style: name of the pygments style to load
        """
        self._name = style
        self._brushes = {}
        self.formats = {}
        try:
            style = get_style_by_name(style)
        except ClassNotFound:
            if style == 'darcula':
                from pyqode.core.styles.darcula import DarculaStyle
                style = DarculaStyle
            else:
                from pyqode.core.styles.qt import QtStyle
                style = QtStyle

        self._load_formats_from_style(style)

    def _load_formats_from_style(self, style):
        self.formats['background'] = self._get_format_from_color(style.background_color)
        self.formats['highlight'] = self._get_format_from_color(style.highlight_color)
        for key, token in COLOR_SCHEME_KEYS.items():
            if token and key:
                self.formats[key] = self._get_format_from_style(token, style)

    def _get_format_from_color(self, color):
        fmt = QtGui.QTextCharFormat()
        fmt.setBackground(self._get_brush(color))
        return fmt

    def _get_format_from_style(self, token, style):
        """ Returns a QTextCharFormat for token by reading a Pygments style.
        """
        result = QtGui.QTextCharFormat()
        items = list(style.style_for_token(token).items())
        for key, value in items:
            if value is None and key == 'color':
                value = drift_color(self.background, 1000).name()
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
                                result.setFontItalic(value)
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

        if token in [Token.Literal.String, Token.Literal.String.Doc,
         Token.Comment]:
            result.setObjectType(result.UserObject)
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
        """ Returns a QColor built from a Pygments color string. """
        color = str(color).replace('#', '')
        qcolor = QtGui.QColor()
        qcolor.setRgb(int(color[:2], base=16), int(color[2:4], base=16), int(color[4:6], base=16))
        return qcolor


class SyntaxHighlighter(QtGui.QSyntaxHighlighter, Mode):
    __doc__ = '\n    Abstract base class for syntax highlighter modes.\n\n    It fills up the document with our custom block data (fold levels,\n    triggers,...).\n\n    It **does not do any syntax highlighting**, that task is left to\n    sublasses such as :class:`pyqode.core.modes.PygmentsSyntaxHighlighter`.\n\n    Subclasses **must** override the\n    :meth:`pyqode.core.api.SyntaxHighlighter.highlight_block` method to\n    apply custom highlighting.\n\n    .. note:: Since version 2.1 and for performance reasons, we store all\n        our data in the block user state as a bit-mask. You should always\n        use :class:`pyqode.core.api.TextBlockHelper` to retrieve or modify\n        those data.\n    '
    block_highlight_started = QtCore.Signal(object, object)
    block_highlight_finished = QtCore.Signal(object, object)

    @property
    def formats(self):
        """
        Returns the color shcme formats dict.
        """
        return self._color_scheme.formats

    @property
    def color_scheme(self):
        """
        Gets/Sets the color scheme of the syntax highlighter, this will trigger
        a rehighlight automatically.
        """
        return self._color_scheme

    @color_scheme.setter
    def color_scheme(self, color_scheme):
        if isinstance(color_scheme, str):
            color_scheme = ColorScheme(color_scheme)
        if color_scheme.name != self._color_scheme.name:
            self._color_scheme = color_scheme
            self.refresh_editor(color_scheme)
            self.rehighlight()

    def refresh_editor(self, color_scheme):
        """
        Refresh editor settings (background and highlight colors) when color
        scheme changed.

        :param color_scheme: new color scheme.
        """
        self.editor.background = color_scheme.background
        self.editor.foreground = color_scheme.formats['normal'].foreground().color()
        self.editor.whitespaces_foreground = color_scheme.formats['whitespace'].foreground().color()
        try:
            mode = self.editor.modes.get('CaretLineHighlighterMode')
        except KeyError:
            pass
        else:
            mode.background = color_scheme.highlight
            mode.refresh()
        try:
            mode = self.editor.panels.get('FoldingPanel')
        except KeyError:
            pass
        else:
            mode.refresh_decorations(force=True)
        self.editor._reset_stylesheet()

    def __init__(self, parent, color_scheme=None):
        """
        :param parent: parent document (QTextDocument)
        :param color_scheme: color scheme to use.
        """
        QtGui.QSyntaxHighlighter.__init__(self, parent)
        Mode.__init__(self)
        if not color_scheme:
            color_scheme = ColorScheme('qt')
        self._color_scheme = color_scheme
        self._spaces_ptrn = QtCore.QRegExp('[ \\t]+')
        self.fold_detector = None
        self.WHITESPACES = QtCore.QRegExp('\\s+')

    def on_state_changed(self, state):
        if self._on_close:
            return
        if state:
            self.setDocument(self.editor.document())
        else:
            self.setDocument(None)

    def _highlight_whitespaces(self, text):
        index = self.WHITESPACES.indexIn(text, 0)
        while index >= 0:
            index = self.WHITESPACES.pos(0)
            length = len(self.WHITESPACES.cap(0))
            self.setFormat(index, length, self.formats['whitespace'])
            index = self.WHITESPACES.indexIn(text, index + length)

    @staticmethod
    def _find_prev_non_blank_block(current_block):
        previous_block = current_block.previous() if current_block.blockNumber() else None
        while previous_block and previous_block.blockNumber() and previous_block.text().strip() == '':
            previous_block = previous_block.previous()

        return previous_block

    def highlightBlock(self, text):
        """
        Highlights a block of text. Please do not override, this method.
        Instead you should implement
        :func:`pyqode.core.api.SyntaxHighlighter.highlight_block`.

        :param text: text to highlight.
        """
        if not self.enabled:
            return
        current_block = self.currentBlock()
        previous_block = self._find_prev_non_blank_block(current_block)
        if self.editor:
            self.highlight_block(text, current_block)
            if self.editor.show_whitespaces:
                self._highlight_whitespaces(text)
            if self.fold_detector is not None:
                self.fold_detector._editor = weakref.ref(self.editor)
                self.fold_detector.process_block(current_block, previous_block, text)

    def highlight_block(self, text, block):
        """
        Abstract method. Override this to apply syntax highlighting.

        :param text: Line of text to highlight.
        :param block: current block
        """
        raise NotImplementedError()

    def rehighlight(self):
        """
        Rehighlight the entire document, may be slow.
        """
        start = time.time()
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        try:
            super(SyntaxHighlighter, self).rehighlight()
        except RuntimeError:
            pass

        QtWidgets.QApplication.restoreOverrideCursor()
        end = time.time()
        _logger().debug('rehighlight duration: %fs' % (end - start))

    def on_install(self, editor):
        super(SyntaxHighlighter, self).on_install(editor)
        self.refresh_editor(self.color_scheme)
        self.document().setParent(editor)
        self.setParent(editor)

    def clone_settings(self, original):
        self._color_scheme = original.color_scheme


class TextBlockUserData(QtGui.QTextBlockUserData):
    __doc__ = '\n    Custom text block user data, mainly used to store checker messages and\n    markers.\n    '

    def __init__(self):
        super(TextBlockUserData, self).__init__()
        self.messages = []
        self.markers = []