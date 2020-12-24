# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/alteraparser/parser.py
# Compiled at: 2015-12-30 04:57:43
# Size of source mod 2**32: 2728 bytes
from alteraparser.ast import AST, TextNode
from alteraparser.io.string_input import StringInput
from alteraparser.syntaxgraph.match_finder import MatchFinder

class ParseError(RuntimeError):
    pass


class Parser(object):

    def __init__(self, grammar):
        self._Parser__grammar = grammar
        self._Parser__debug = False

    def debug_mode(self, debug=True):
        self._Parser__debug = debug
        return self

    def parse(self, input_stream):
        finder = MatchFinder(input_stream).debug_mode(self._Parser__debug)
        self._Parser__grammar.get_dock_vertex().walk(finder)
        if not finder.stopped:
            return self._Parser__create_ast(finder.path)
        raise ParseError(self._Parser__get_unparsed_text(finder.path))

    def parse_string(self, code_str):
        return self.parse(StringInput(code_str))

    def parse_file(self, file_path):
        f = open(file_path, 'r')
        code_lines = f.readlines()
        f.close()
        code = ''.join(code_lines)
        return self.parse_string(code)

    def __create_ast(self, path):
        root = None
        stack = []
        text = ''
        for vertex, ch in path:
            if vertex.is_group_start():
                if text and stack:
                    parent = stack[(-1)]
                    parent.add_child(TextNode(text))
                text = ''
                node = AST(vertex.name, vertex.id)
                stack.append(node)
                if self._Parser__debug and vertex.name:
                    print('PUSH -> {}'.format(vertex.name))
                    print(self._Parser__stack_to_string(stack))
            elif vertex.is_group_end():
                node = stack.pop()
                if self._Parser__debug and vertex.name:
                    print('POP <- {}'.format(vertex.name))
                    print(self._Parser__stack_to_string(stack))
                    print("TEXT: '{}'".format(text))
                node.add_child(TextNode(text))
                text = ''
                id_ = node.id
                transformed_node = vertex.transform_ast_fn(node)
                transformed_node.id = id_
                if stack:
                    parent = stack[(-1)]
                    if not vertex.ignore:
                        parent.add_child(transformed_node)
                else:
                    root = transformed_node
            if ch is not None:
                text += ch
                continue

        return root

    @staticmethod
    def __get_unparsed_text(path):
        return ''.join([ch for _, ch in path if ch is not None])

    @staticmethod
    def __stack_to_string(stack):
        res = [node.name for node in stack if node.name]
        res = '[' + ','.join(res) + ']'
        return res