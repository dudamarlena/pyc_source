# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/flake8/flake8/processor.py
# Compiled at: 2019-07-30 18:47:04
# Size of source mod 2**32: 16020 bytes
"""Module containing our file processor that tokenizes a file for checks."""
import contextlib, logging, sys, tokenize
from typing import Any, Dict, List, Tuple
import flake8
from flake8 import defaults
from flake8 import exceptions
from flake8 import utils
LOG = logging.getLogger(__name__)
PyCF_ONLY_AST = 1024
NEWLINE = frozenset([tokenize.NL, tokenize.NEWLINE])
SKIP_TOKENS = frozenset([
 tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT])

class FileProcessor(object):
    __doc__ = 'Processes a file and holdes state.\n\n    This processes a file by generating tokens, logical and physical lines,\n    and AST trees. This also provides a way of passing state about the file\n    to checks expecting that state. Any public attribute on this object can\n    be requested by a plugin. The known public attributes are:\n\n    - :attr:`blank_before`\n    - :attr:`blank_lines`\n    - :attr:`checker_state`\n    - :attr:`indent_char`\n    - :attr:`indent_level`\n    - :attr:`line_number`\n    - :attr:`logical_line`\n    - :attr:`max_line_length`\n    - :attr:`max_doc_length`\n    - :attr:`multiline`\n    - :attr:`noqa`\n    - :attr:`previous_indent_level`\n    - :attr:`previous_logical`\n    - :attr:`previous_unindented_logical_line`\n    - :attr:`tokens`\n    - :attr:`file_tokens`\n    - :attr:`total_lines`\n    - :attr:`verbose`\n    '

    def __init__(self, filename, options, lines=None):
        """Initialice our file processor.

        :param str filename:
            Name of the file to process
        """
        self.options = options
        self.filename = filename
        self.lines = lines
        if lines is None:
            self.lines = self.read_lines()
        self.strip_utf_bom()
        self.blank_before = 0
        self.blank_lines = 0
        self._checker_states = {}
        self.checker_state = None
        self.hang_closing = options.hang_closing
        self.indent_char = None
        self.indent_level = 0
        self.line_number = 0
        self.logical_line = ''
        self.max_line_length = options.max_line_length
        self.max_doc_length = options.max_doc_length
        self.multiline = False
        self.noqa = False
        self.previous_indent_level = 0
        self.previous_logical = ''
        self.previous_unindented_logical_line = ''
        self.tokens = []
        self.total_lines = len(self.lines)
        self.verbose = options.verbose
        self.statistics = {'logical lines': 0}
        self._file_tokens = None

    @property
    def file_tokens(self):
        """Return the complete set of tokens for a file.

        Accessing this attribute *may* raise an InvalidSyntax exception.

        :raises: flake8.exceptions.InvalidSyntax
        """
        if self._file_tokens is None:
            line_iter = iter(self.lines)
            try:
                self._file_tokens = list(tokenize.generate_tokens(lambda : next(line_iter)))
            except tokenize.TokenError as exc:
                raise exceptions.InvalidSyntax(exception=exc)

        return self._file_tokens

    @contextlib.contextmanager
    def inside_multiline(self, line_number):
        """Context-manager to toggle the multiline attribute."""
        self.line_number = line_number
        self.multiline = True
        yield
        self.multiline = False

    def reset_blank_before(self):
        """Reset the blank_before attribute to zero."""
        self.blank_before = 0

    def delete_first_token(self):
        """Delete the first token in the list of tokens."""
        del self.tokens[0]

    def visited_new_blank_line(self):
        """Note that we visited a new blank line."""
        self.blank_lines += 1

    def update_state(self, mapping):
        """Update the indent level based on the logical line mapping."""
        start_row, start_col = mapping[0][1]
        start_line = self.lines[(start_row - 1)]
        self.indent_level = expand_indent(start_line[:start_col])
        if self.blank_before < self.blank_lines:
            self.blank_before = self.blank_lines

    def update_checker_state_for(self, plugin):
        """Update the checker_state attribute for the plugin."""
        if 'checker_state' in plugin['parameters']:
            self.checker_state = self._checker_states.setdefault(plugin['name'], {})

    def next_logical_line(self):
        """Record the previous logical line.

        This also resets the tokens list and the blank_lines count.
        """
        if self.logical_line:
            self.previous_indent_level = self.indent_level
            self.previous_logical = self.logical_line
            if not self.indent_level:
                self.previous_unindented_logical_line = self.logical_line
        self.blank_lines = 0
        self.tokens = []
        self.noqa = False

    def build_logical_line_tokens(self):
        """Build the mapping, comments, and logical line lists."""
        logical = []
        comments = []
        length = 0
        previous_row = previous_column = mapping = None
        for token_type, text, start, end, line in self.tokens:
            if token_type in SKIP_TOKENS:
                pass
            else:
                if not mapping:
                    mapping = [
                     (
                      0, start)]
            if token_type == tokenize.COMMENT:
                comments.append(text)
            else:
                if token_type == tokenize.STRING:
                    text = mutate_string(text)
                if previous_row:
                    start_row, start_column = start
                    if previous_row != start_row:
                        row_index = previous_row - 1
                        column_index = previous_column - 1
                        previous_text = self.lines[row_index][column_index]
                        if previous_text == ',' or previous_text not in '{[(' and text not in '}])':
                            text = ' ' + text
                    elif previous_column != start_column:
                        text = line[previous_column:start_column] + text
                logical.append(text)
                length += len(text)
                mapping.append((length, end))
                previous_row, previous_column = end

        return (
         comments, logical, mapping)

    def build_ast(self):
        """Build an abstract syntax tree from the list of lines."""
        return compile(''.join(self.lines), '', 'exec', PyCF_ONLY_AST)

    def build_logical_line(self):
        """Build a logical line from the current tokens list."""
        comments, logical, mapping_list = self.build_logical_line_tokens()
        joined_comments = ''.join(comments)
        self.logical_line = ''.join(logical)
        if defaults.NOQA_INLINE_REGEXP.search(joined_comments):
            self.noqa = True
        self.statistics['logical lines'] += 1
        return (joined_comments, self.logical_line, mapping_list)

    def split_line(self, token):
        """Split a physical line's line based on new-lines.

        This also auto-increments the line number for the caller.
        """
        for line in token[1].split('\n')[:-1]:
            yield line
            self.line_number += 1

    def keyword_arguments_for(self, parameters, arguments=None):
        """Generate the keyword arguments for a list of parameters."""
        if arguments is None:
            arguments = {}
        for param, required in parameters.items():
            if param in arguments:
                pass
            else:
                try:
                    arguments[param] = getattr(self, param)
                except AttributeError as exc:
                    if required:
                        LOG.exception(exc)
                        raise
                    else:
                        LOG.warning('Plugin requested optional parameter "%s" but this is not an available parameter.', param)

        return arguments

    def check_physical_error(self, error_code, line):
        """Update attributes based on error code and line."""
        if error_code == 'E101':
            self.indent_char = line[0]

    def generate_tokens(self):
        """Tokenize the file and yield the tokens.

        :raises flake8.exceptions.InvalidSyntax:
            If a :class:`tokenize.TokenError` is raised while generating
            tokens.
        """
        try:
            for token in tokenize.generate_tokens(self.next_line):
                if token[2][0] > self.total_lines:
                    break
                self.tokens.append(token)
                yield token

        except (tokenize.TokenError, SyntaxError) as exc:
            raise exceptions.InvalidSyntax(exception=exc)

    def line_for(self, line_number):
        """Retrieve the physical line at the specified line number."""
        adjusted_line_number = line_number - 1
        if 0 <= adjusted_line_number < len(self.lines):
            return self.lines[adjusted_line_number]

    def next_line(self):
        """Get the next line from the list."""
        if self.line_number >= self.total_lines:
            return ''
        else:
            line = self.lines[self.line_number]
            self.line_number += 1
            if self.indent_char is None:
                if line[:1] in defaults.WHITESPACE:
                    self.indent_char = line[0]
            return line

    def read_lines(self):
        """Read the lines for this file checker."""
        if self.filename is None or self.filename == '-':
            self.filename = self.options.stdin_display_name or 'stdin'
            lines = self.read_lines_from_stdin()
        else:
            lines = self.read_lines_from_filename()
        return lines

    def _readlines_py2(self):
        with open(self.filename, 'rU') as (fd):
            return fd.readlines()

    def _readlines_py3(self):
        try:
            with tokenize.open(self.filename) as (fd):
                return fd.readlines()
        except (SyntaxError, UnicodeError):
            with open((self.filename), encoding='latin-1') as (fd):
                return fd.readlines()

    def read_lines_from_filename(self):
        """Read the lines for a file."""
        if (2, 6) <= sys.version_info < (3, 0):
            readlines = self._readlines_py2
        else:
            if (3, 0) <= sys.version_info < (4, 0):
                readlines = self._readlines_py3
        return readlines()

    def read_lines_from_stdin(self):
        """Read the lines from standard in."""
        return utils.stdin_get_value().splitlines(True)

    def should_ignore_file(self):
        """Check if ``flake8: noqa`` is in the file to be ignored.

        :returns:
            True if a line matches :attr:`defaults.NOQA_FILE`,
            otherwise False
        :rtype:
            bool
        """
        if any(defaults.NOQA_FILE.match(line) for line in self.lines):
            return True
        else:
            if any(defaults.NOQA_FILE.search(line) for line in self.lines):
                LOG.warning('Detected `flake8: noqa` on line with code. To ignore an error on a line use `noqa` instead.')
                return False
            return False

    def strip_utf_bom(self):
        """Strip the UTF bom from the lines of the file."""
        if not self.lines:
            return
        else:
            first_byte = ord(self.lines[0][0])
            if first_byte not in (239, 65279):
                return
            if first_byte == 65279:
                self.lines[0] = self.lines[0][1:]
            elif self.lines[0][:3] == 'ï»¿':
                self.lines[0] = self.lines[0][3:]


def is_eol_token(token):
    """Check if the token is an end-of-line token."""
    return token[0] in NEWLINE or token[4][token[3][1]:].lstrip() == '\\\n'


def is_multiline_string(token):
    """Check if this is a multiline string."""
    return token[0] == tokenize.STRING and '\n' in token[1]


def token_is_newline(token):
    """Check if the token type is a newline token type."""
    return token[0] in NEWLINE


def count_parentheses(current_parentheses_count, token_text):
    """Count the number of parentheses."""
    if token_text in '([{':
        return current_parentheses_count + 1
    else:
        if token_text in '}])':
            return current_parentheses_count - 1
        return current_parentheses_count


def log_token(log, token):
    """Log a token to a provided logging object."""
    if token[2][0] == token[3][0]:
        pos = '[%s:%s]' % (token[2][1] or '', token[3][1])
    else:
        pos = 'l.%s' % token[3][0]
    log.log(flake8._EXTRA_VERBOSE, 'l.%s\t%s\t%s\t%r' % (
     token[2][0], pos, tokenize.tok_name[token[0]], token[1]))


def expand_indent(line):
    r"""Return the amount of indentation.

    Tabs are expanded to the next multiple of 8.

    >>> expand_indent('    ')
    4
    >>> expand_indent('\t')
    8
    >>> expand_indent('       \t')
    8
    >>> expand_indent('        \t')
    16
    """
    if '\t' not in line:
        return len(line) - len(line.lstrip())
    else:
        result = 0
        for char in line:
            if char == '\t':
                result = result // 8 * 8 + 8
            else:
                if char == ' ':
                    result += 1
                else:
                    break

        return result


def mutate_string(text):
    """Replace contents with 'xxx' to prevent syntax matching.

    >>> mute_string('"abc"')
    '"xxx"'
    >>> mute_string("'''abc'''")
    "'''xxx'''"
    >>> mute_string("r'abc'")
    "r'xxx'"
    """
    start = text.index(text[(-1)]) + 1
    end = len(text) - 1
    if text[-3:] in ('"""', "'''"):
        start += 2
        end -= 2
    return text[:start] + 'x' * (end - start) + text[end:]