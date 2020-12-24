# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpQtLib/widgets/code.py
# Compiled at: 2020-01-16 21:52:29
# Size of source mod 2**32: 19730 bytes
"""
Module that contains code/script related widgets
"""
from __future__ import print_function, division, absolute_import
import re, sys, string
from Qt.QtCore import *
from Qt.QtWidgets import *
from Qt.QtGui import *
import tpDccLib as tp
from tpPyUtils import python, fileio, code, folder as folder_utils, path as path_utils

class PythonCompleter(QCompleter, object):

    def __init__(self):
        super(PythonCompleter, self).__init__()
        self._info = None
        self._file_path = None
        self._model_strings = list()
        self._reset_list = True
        self._string_model = QStringListModel(self._model_strings, self)
        self._refresh_completer = True
        self._sub_activated = False
        self._last_imports = None
        self._last_lines = None
        self._last_path = None
        self._current_defined_imports = None
        self._last_path_and_part = None
        self._current_sub_functions = None
        self._last_column = 0
        self.setCompletionMode(self.PopupCompletion)
        self.setCaseSensitivity(Qt.CaseInsensitive)
        self.setWrapAround(False)
        self.activated.connect(self._on_insert_completion)

    def setWidget(self, widget):
        super(PythonCompleter, self).setWidget(widget)
        self.setParent(widget)

    def keyPressEvent(self):
        pass

    def show_info_popup(self, info=None):
        self._info = QTextEdit()
        self._info.setEnabled(False)
        self._info.setWindowFlags(Qt.Popup)
        self._info.show()

    def get_imports(self, paths=None):
        imports = self._get_available_modules(paths=paths)
        imports.sort()
        return imports

    def get_sub_imports(self, path):
        """
        Returns namespace in a module
        :param path: str
        :return: str
        """
        defined = code.get_defined(path)
        defined.sort()
        return defined

    def clean_completer_list(self):
        self._string_model.setStringList([])

    def text_under_cursor(self):
        cursor = self.widget().textCursor()
        cursor.select(cursor.LineUnderCursor)
        return cursor.selectedText()

    def set_filepath(self, file_path):
        if not file_path:
            return
        self._file_path = file_path

    def handle_text(self, text):
        """
        Parses a single line of text
        :param text: str
        :return: bool
        """
        if not text:
            return False
        else:
            cursor = self.widget().textCursor()
            column = cursor.columnNumber() - 1
            if column < self._last_column:
                self._last_column = column
                return False
            self._last_column = column
            if column == 1:
                return False
            text = str(text)
            passed = self.handle_from_import(text, column)
            if passed:
                return True
            passed = self.handle_sub_import(text, column)
            if passed:
                return True
            passed = self.handle_import_load(text, column)
            if passed:
                return True
            return False

    def handle_import(self, text):
        m = re.search('(from|import)(?:\\s+?)(\\w*)', text)
        if m:
            pass

    def handle_sub_import(self, text, column):
        m = re.search('(from|import)(?:\\s+?)(\\w*.?\\w*)\\.(\\w*)$', text)
        if m:
            if column < m.end(2):
                return False
            from_module = m.group(2)
            module_path = code.get_package_path_from_name(from_module)
            last_part = m.group(3)
            if module_path:
                defined = self.get_imports(module_path)
                self._string_model.setStringList(defined)
                self.setCompletionPrefix(last_part)
                self.popup().setCurrentIndex(self.completionModel().index(0, 0))
                return True
        return False

    def handle_import_load(self, text, cursor):
        m = re.search('\\s*([a-zA-Z0-9._]+)\\.([a-zA-Z0-9_]*)$', text)
        column = cursor.columnNumber() - 1
        block_number = cursor.blockNumber()
        line_number = block_number + 1
        all_text = self.widget().toPlainText()
        scope_text = all_text[:cursor.position() - 1]
        if m:
            if m.group(2):
                scope_text = all_text[:cursor.position() - len(m.group(2)) + 1]
        if m:
            assignment = m.group(1)
            if column < m.end(1):
                return False
            sub_m = re.search('(from|import)\\s+(%s)' % assignment, text)
            if sub_m:
                return False
            path = None
            sub_part = None
            target = None
            text = self.widget().toPlainText()
            lines = fileio.get_text_lines(text)
            assign_map = code.get_ast_assignment(scope_text, line_number - 1, assignment)
            if assign_map:
                if assignment in assign_map:
                    target = assign_map[assignment]
                else:
                    split_assignment = assignment.split('.')
                    inc = 1
                    while assignment not in assign_map:
                        sub_assignment = string.join(split_assignment[:inc * -1], '.')
                        if sub_assignment in assign_map:
                            target = assign_map[sub_assignment]
                            break
                        inc += 1
                        if inc > len(split_assignment) - 1:
                            break

                    sub_part = string.join(split_assignment[inc:], '.')
            module_name = m.group(1)
            if target:
                if len(target) == 2:
                    if target[0] == 'import':
                        module_name = target[1]
                    if not target[0] == 'import':
                        module_name = target[0]
                        sub_part = target[1]
            if module_name:
                imports = None
                if lines == self.last_lines:
                    imports = self.last_imports
                if not imports:
                    imports = code.get_line_imports(lines)
                self._last_imports = imports
                self._last_lines = lines
                if module_name in imports:
                    path = imports[module_name]
                if module_name not in imports:
                    split_assignment = module_name.split('.')
                    last_part = split_assignment[(-1)]
                    if last_part in imports:
                        path = imports[last_part]
                if path:
                    if not sub_part:
                        test_text = ''
                        defined = None
                        if path == self.last_path:
                            defined = self.current_defined_imports
                        if len(m.groups()) > 0:
                            test_text = m.group(2)
                        if not defined:
                            if path_utils.is_dir(path):
                                defined = self.get_imports(path)
                                self._current_defined_imports = defined
                            if path_utils.is_file(path):
                                defined = self.get_sub_imports(path)
                        custom_defined = self.custom_import_load(assign_map, module_name)
                        if custom_defined:
                            defined = custom_defined
                        if not defined:
                            return False
                        self._string_model.setStringList(defined)
                        self.setCompletionPrefix(test_text)
                        self.setCaseSensitivity(Qt.CaseInsensitive)
                        self.popup().setCurrentIndex(self.completionModel().index(0, 0))
                        return True
                if path:
                    if sub_part:
                        sub_functions = None
                        if self.last_path_and_part:
                            if path == self.last_path_and_part[0]:
                                if sub_part == self.last_path_and_part[1]:
                                    sub_functions = self.current_sub_functions
                        if not sub_functions:
                            sub_functions = code.get_ast_class_sub_functions(path, sub_part)
                            if sub_functions:
                                self._current_sub_functions = sub_functions
                        self._last_path_and_part = [
                         path, sub_part]
                        if not sub_functions:
                            return False
                        test_text = ''
                        if len(m.groups()) > 0:
                            test_text = m.group(2)
                        self._string_model.setStringList(sub_functions)
                        self.setCompletionPrefix(test_text)
                        self.popup().setCurrentIndex(self.completionModel().index(0, 0))
                        return True
            module_name = m.group(1)
            if module_name:
                custom_defined = self.custom_import_load(assign_map, module_name)
                test_text = ''
                if len(m.groups()) > 0:
                    test_text = m.group(2)
                self._string_model.setStringList(custom_defined)
                self.setCompletionPrefix(test_text)
                self.popup().setCurrentIndex(self.completionModel().index(0, 0))
                return True
        return False

    def handle_from_import(self, text, column):
        m = re.search('(from)(?:\\s+?)(\\w*.?\\w*)(?:\\s+?)(import)(?:\\s+?)(\\w+)?$', text)
        if m:
            if column < m.end(3):
                return False
            else:
                from_module = m.group(2)
                module_path = code.get_package_path_from_name(from_module)
                last_part = m.group(4)
                if not last_part:
                    last_part = ''
                if module_path:
                    defined = self.get_imports(module_path)
                    self._string_model.setStringList(defined)
                    self.setCompletionPrefix(last_part)
                    self.popup().setCurrentIndex(self.completionModel().index(0, 0))
                    return True
        return False

    def custom_import_load(self, assign_map, moduel_name):
        pass

    def _get_available_modules(self, paths=None):
        imports = list()
        if not paths:
            paths = sys.path
        if paths:
            paths = python.force_list(paths)
        for path in paths:
            fix_path = path_utils.normalize_path(path)
            if not path.is_dir(fix_path):
                pass
            else:
                folders = folder_utils.get_folders(fix_path)
                for folder in folders:
                    folder_path = path_utils.join_path(fix_path, folder)
                    files = folder_utils.get_files_with_extension('py', folder_path, full_path=False)
                    if '__init__.py' in files:
                        imports.append(str(folder))

                python_files = folder_utils.get_files_with_extension('py', fix_path, full_path=False)
                for python_file in python_files:
                    if python_file.startswith('__'):
                        pass
                    else:
                        python_file_name = python_file.split('.')[0]
                        imports.append(str(python_file_name))

        if imports:
            imports = list(set(imports))
        return imports

    def _on_insert_completion(self, completion_string):
        widget = self.widget()
        cursor = widget.textCursor()
        if completion_string == self.completionPrefix():
            return
        extra = len(self.completionPrefix())
        cursor.movePosition(QTextCursor.Left, cursor.KeepAnchor, extra)
        cursor.removeSelectedText()
        cursor.insertText(completion_string)
        widget.setTextCursor(cursor)


def get_syntax_format(color=None, style=''):
    """
    Returns a QTextCharFormat with the given attributes.
    """
    _color = None
    if type(color) == str:
        _color = QColor()
        _color.setNamedColor(color)
    if type(color) == list:
        _color = QColor(*color)
    if color == 'green':
        _color = Qt.green
    _format = QTextCharFormat()
    if _color:
        _format.setForeground(_color)
    if 'bold' in style:
        _format.setFontWeight(QFont.Bold)
    if 'italic' in style:
        _format.setFontItalic(True)
    return _format


def syntax_styles(name):
    if name == 'keyword':
        if tp.is_maya():
            return get_syntax_format('green', 'bold')
        elif not tp.is_maya():
            return get_syntax_format([0, 150, 150], 'bold')
        else:
            if name == 'operator':
                if tp.is_maya():
                    return get_syntax_format('gray')
                else:
                    if not tp.is_maya():
                        return get_syntax_format('darkGray')
                    elif name == 'brace':
                        if tp.is_maya():
                            return get_syntax_format('lightGray')
                        if not tp.is_maya():
                            return get_syntax_format('darkGray')
                    else:
                        if name == 'defclass':
                            if tp.is_maya():
                                return get_syntax_format(None, 'bold')
                            if not tp.is_maya():
                                return get_syntax_format(None, 'bold')
                        if name == 'string':
                            if tp.is_maya():
                                return get_syntax_format([230, 230, 0])
                            else:
                                return tp.is_maya() or get_syntax_format('blue')
                    if name == 'string2':
                        if tp.is_maya():
                            return get_syntax_format([230, 230, 0])
                        else:
                            return tp.is_maya() or get_syntax_format('lightGreen')
            else:
                if name == 'comment':
                    if tp.is_maya():
                        return get_syntax_format('red')
                    if not tp.is_maya():
                        return get_syntax_format('red')
            if name == 'self':
                if tp.is_maya():
                    return get_syntax_format(None, 'italic')
                else:
                    return tp.is_maya() or get_syntax_format('black', 'italic')
        if name == 'bold':
            return get_syntax_format(None, 'bold')
    else:
        if name == 'numbers':
            if tp.is_maya():
                return get_syntax_format('cyan')
            if not tp.is_maya():
                return get_syntax_format('brown')


class PythonHighlighter(QSyntaxHighlighter):
    __doc__ = '\n    Syntax highlighter for the Python language.\n    '
    keywords = [
     'and', 'assert', 'break', 'class', 'continue', 'def',
     'del', 'elif', 'else', 'except', 'exec', 'finally',
     'for', 'from', 'global', 'if', 'import', 'in',
     'is', 'lambda', 'not', 'or', 'pass', 'print',
     'raise', 'return', 'try', 'while', 'yield',
     'None', 'True', 'False', 'process', 'show']
    if tp.is_maya():
        keywords += ['cmds', 'pm', 'mc', 'pymel']
    operators = [
     '=',
     '==', '!=', '<', '<=', '>', '>=',
     '\\+', '-', '\\*', '/', '//', '\\%', '\\*\\*',
     '\\+=', '-=', '\\*=', '/=', '\\%=',
     '\\^', '\\|', '\\&', '\\~', '>>', '<<']
    braces = [
     '\\{', '\\}', '\\(', '\\)', '\\[', '\\]']

    def __init__(self, document):
        super(PythonHighlighter, self).__init__(document)
        self.tri_single = (
         QRegExp("'''"), 1, syntax_styles('string2'))
        self.tri_double = (QRegExp('"""'), 2, syntax_styles('string2'))
        rules = []
        rules += [('\\b%s\\b' % w, 0, syntax_styles('keyword')) for w in PythonHighlighter.keywords]
        rules += [('%s' % o, 0, syntax_styles('operator')) for o in PythonHighlighter.operators]
        rules += [('%s' % b, 0, syntax_styles('brace')) for b in PythonHighlighter.braces]
        rules += [
         (
          '\\bself\\b', 0, syntax_styles('self')),
         (
          '"[^"\\\\]*(\\\\.[^"\\\\]*)*"', 0, syntax_styles('string')),
         (
          "'[^'\\\\]*(\\\\.[^'\\\\]*)*'", 0, syntax_styles('string')),
         (
          '#[^\\n]*', 0, syntax_styles('comment')),
         (
          '\\b[+-]?[0-9]+[lL]?\\b', 0, syntax_styles('numbers')),
         (
          '\\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\\b', 0, syntax_styles('numbers')),
         (
          '\\b[+-]?[0-9]+(?:\\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\\b', 0, syntax_styles('numbers'))]
        self.rules = [(QRegExp(pat), index, fmt) for pat, index, fmt in rules]

    def highlightBlock(self, text):
        """
        Apply syntax highlighting to the given block of text.
        """
        for expression, nth, format_value in self.rules:
            index = expression.indexIn(text, 0)
            while index >= 0:
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, format_value)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)
        in_multiline = (self.match_multiline)(text, *self.tri_single)
        if not in_multiline:
            in_multiline = (self.match_multiline)(text, *self.tri_double)

    def match_multiline(self, text, delimiter, in_state, style):
        """
        Do highlighting of multi-line strings. ``delimiter`` should be a
        ``QRegExp`` for triple-single-quotes or triple-double-quotes, and
        ``in_state`` should be a unique integer to represent the corresponding
        state changes when inside those strings. Returns True if we're still
        inside a multi-line string when this function is finished.
        """
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
        else:
            start = delimiter.indexIn(text)
            add = delimiter.matchedLength()
        while start >= 0:
            end = delimiter.indexIn(text, start + add)
            if end >= add:
                length = end - start + add + delimiter.matchedLength()
                self.setCurrentBlockState(0)
            else:
                self.setCurrentBlockState(in_state)
                length = len(text) - start + add
            self.setFormat(start, length, style)
            start = delimiter.indexIn(text, start + length)

        if self.currentBlockState() == in_state:
            return True
        else:
            return False