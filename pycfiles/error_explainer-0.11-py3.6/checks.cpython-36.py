# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/error_explainer/checks.py
# Compiled at: 2020-04-25 13:41:41
# Size of source mod 2**32: 11053 bytes
"""
Different checks for finding possible errors.
"""
import re, tokenize
from typing import Tuple, List, Optional
from error_explainer.colon_statements import *
from tokenize import TokenInfo
from error_explainer import utils
import enum, parso

class IndentationErrorType(enum.Enum):
    __doc__ = '\n    Enum for types of indentation errors.\n    '
    HIGHER_LEVEL_WITHOUT_START = 1
    DOES_NOT_MATCH_OUTER = 2
    NEW_INDENT_AT_EOF = 3
    NO_NEW_INDENT = 4


class BracketErrorType(enum.Enum):
    __doc__ = '\n    Enum for bracket miss match errors\n    '
    NORMAL_SQUARE = 1
    NORMAL_CURLY = 2
    CURLY_SQUARE = 3


def check_missing_brackets(error_node: parso.python.tree.PythonErrorNode) -> Tuple[(int, int, int)]:
    """
    Check if there are any missing brackets in the code of the given PythonErrorNode.
    :param error_node: parso.python.tree.PythonErrorNode
    :return: List in the shape of [brackets_normal, brackets_square, brackets_curly] where each
    value is 0 if there are no missing brackets of that type and positive or negative depending on if there were more
    opening or closing brackets.
    """
    error_code = error_node.get_code()
    error_code = error_code.strip()
    return utils.count_brackets(error_code)


def check_print_missing_brackets(error_node: parso.python.tree.PythonErrorNode) -> bool:
    """
    Check for python 2 style print usage (without brackets)
    :param error_node: parso.python.tree.PythonErrorNode
    :return: True/False
    """
    error_code = error_node.get_code()
    error_code = error_code.strip()
    if error_code == 'print':
        return True
    else:
        return False


def check_missing_colon(error_node: parso.python.tree.PythonErrorNode) -> Optional[str]:
    """
    Uses colon_statements to determine if there is a missing
    colon after a statement that should be followed by one.
    :param error_node: parso.python.tree.PythonErrorNode
    :return: the statement missing a colon or None if no colon error found
    """
    error_code = error_node.get_code()
    error_code = error_code.strip()
    for statement in colon_statements:
        if statement in error_code:
            if ':' not in error_code:
                return statement


def check_invalid_function_def(error_node: parso.python.tree.PythonErrorNode) -> bool:
    """
    Check if the error node is only the string "def"
    :param error_node: parso.python.tree.PythonErrorNode
    :return: True/False
    """
    error_code = error_node.get_code()
    error_code = error_code.strip()
    return 'def' in error_code


def check_missing_function_def_parts(line: str) -> Optional[str]:
    """
    Check if the line is a proper function definition.
    :param line: line to check
    :return: None if proper definition, given line if error found.
    """
    tokens = utils.tokenize_line(line)
    line = line.strip()
    if len(tokens) < 5:
        return line
    if not utils.is_correct_variable_name(tokens[1].string) or tokens[2].string != '(' or tokens[(-2)].string != ')':
        return line


def check_invalid_function_name(tokens: List[TokenInfo]) -> Optional[str]:
    """
    Check if there is a correct function name used in the function definition.
    :param tokens: tokens to check
    :return: None if no error found otherwise a string representing what type of error was found
    """
    if len(tokens) > 1:
        if tokens[1].string == '=':
            return '='
    if len(tokens) >= 6:
        should_be_variable_name = tokens[1]
        if should_be_variable_name.type == tokenize.NAME:
            if utils.is_correct_variable_name(should_be_variable_name.string):
                return
        return should_be_variable_name.string


def check_miss_matched_bracket_type(path: str) -> Optional[BracketErrorType]:
    """
    Check for miss matched brackets
    :param path: path to file
    :return: Type of miss match or None if there is none
    """
    file_as_string = utils.read_file(path)
    brackets_count = utils.count_brackets(file_as_string)
    normal_brackets_are_even = brackets_count[0] % 2 == 0
    square_brackets_are_even = brackets_count[1] % 2 == 0
    curly_brackets_are_even = brackets_count[2] % 2 == 0
    if not normal_brackets_are_even:
        if not square_brackets_are_even:
            return BracketErrorType.NORMAL_SQUARE
    if not normal_brackets_are_even:
        if not curly_brackets_are_even:
            return BracketErrorType.NORMAL_CURLY
    if not curly_brackets_are_even:
        if not square_brackets_are_even:
            return BracketErrorType.CURLY_SQUARE


def check_invalid_indentation(path: str) -> Tuple[(int, str, str, IndentationErrorType)]:
    """
    Check if the file contains any indentation errors.
    :param path: Path to file
    :return: Tuple[line number: int,
                    error line: str,
                    previous start of indentation block line: str,
                    IndentationErrorType]
    """
    level_stack = [
     0]
    statement_lines = [None]

    def is_correct_indent_level(line_to_check):
        if utils.is_only_comment_line(line_to_check):
            return True
        else:
            if len(line_to_check.strip()) == 0:
                return True
            return utils.count_leading_spaces(line_to_check) == level_stack[0]

    def is_lower_indentation(line_to_check):
        return utils.count_leading_spaces(line_to_check) < level_stack[0]

    def get_next_non_comment_line(all_lines, from_line):
        for l in all_lines[from_line:]:
            if not utils.is_only_comment_line(l):
                return l

    lines = utils.read_lines(path)
    if utils.is_colon_statement_line(lines[(len(lines) - 1)]):
        return (
         len(lines),
         lines[(len(lines) - 1)].rstrip(),
         lines[(len(lines) - 1)].rstrip(),
         IndentationErrorType.NEW_INDENT_AT_EOF)
    for i, line in enumerate(lines):
        space_count = utils.count_leading_spaces(line)
        if is_correct_indent_level(line):
            if utils.is_colon_statement_line(line):
                statement_lines.insert(0, line)
                try:
                    next_non_comment_line = get_next_non_comment_line(lines, i + 1)
                    next_indentation_level = utils.count_leading_spaces(next_non_comment_line)
                    if next_indentation_level <= level_stack[0]:
                        return (
                         i,
                         next_non_comment_line.rstrip(),
                         statement_lines[0].rstrip(),
                         IndentationErrorType.NO_NEW_INDENT)
                    level_stack.insert(0, next_indentation_level)
                except IndexError:
                    return (i + 1,
                     line.rstrip(),
                     statement_lines[0].rstrip(),
                     IndentationErrorType.NEW_INDENT_AT_EOF)

        else:
            if is_lower_indentation(line):
                if space_count in level_stack:
                    index = level_stack.index(space_count) + 1
                    del level_stack[0:index - 1]
                    del statement_lines[0:index - 1]
                else:
                    return (i + 1,
                     line.rstrip(),
                     statement_lines[0].rstrip(),
                     IndentationErrorType.DOES_NOT_MATCH_OUTER)
            else:
                return (i + 1,
                 line.rstrip(),
                 '',
                 IndentationErrorType.HIGHER_LEVEL_WITHOUT_START)


def check_invalid_assignment_expr(root_node: parso.python.tree.Module) -> Optional[List[parso.python.tree.ExprStmt]]:
    """
    Check for errors in tree constructed by parso
    :param root_node: parso.python.tree.Module root node for tree
    :return: List of parso.python.tree.ExprStmt nodes for every bad statement found or None if none were found
    """
    expr_nodes = utils.find_nodes_of_type(root_node, parso.python.tree.ExprStmt)
    bad_exprs = []
    for expr in expr_nodes:
        code = expr.get_code().strip()
        if not utils.is_correct_assignment_signature(code):
            bad_exprs.append(expr)

    if len(bad_exprs) != 0:
        return bad_exprs


def check_coma_used_instead_of_period(root_node: parso.python.tree.Module) -> Optional[List[parso.python.tree.ExprStmt]]:
    expr_nodes = utils.find_nodes_of_type(root_node, parso.python.tree.ExprStmt)
    bad_exprs = []
    for expr in expr_nodes:
        code = expr.get_code().strip()
        if utils.is_bad_coma_usage(code):
            bad_exprs.append(expr)

    if len(bad_exprs) != 0:
        return bad_exprs


def check_quote_error(root_node: parso.python.tree.Module) -> Optional[List[parso.python.tree.PythonErrorLeaf]]:
    """
    Check if there are any parso.python.tree.PythonErrorLeaf nodes in the tree and if they contain a quote symbol
    (if yes this should be a quotation error)
    :param root_node: parso.python.tree.Module root node for tree
    :return: List of parso.python.tree.PythonErrorLeaf nodes for every quote error found or None if none were found
    """
    leaf_error_nodes = utils.find_nodes_of_type(root_node, parso.python.tree.PythonErrorLeaf)
    leaf_error_nodes = [leaf for leaf in leaf_error_nodes if leaf.get_code().strip() == "'" or leaf.get_code().strip() == '"' or leaf.get_code().strip() == "'''" or leaf.get_code().strip() == '"""']
    if len(leaf_error_nodes) > 0:
        return leaf_error_nodes
    else:
        return


def check_docstring_quote_error(root_node: parso.python.tree.Module) -> Optional[parso.python.tree.PythonErrorLeaf]:
    double_pattern = re.compile('(\\"{3}).*(\\"{2}|\\")')
    single_pattern = re.compile("('{3}).*('{2}|')")
    leaf_error_nodes = utils.find_nodes_of_type(root_node, parso.python.tree.PythonErrorLeaf)
    for leaf in leaf_error_nodes:
        code = leaf.get_code().strip().replace('\n', '')
        code = code.replace('\t', '')
        if double_pattern.match(code) or single_pattern.match(code):
            return leaf