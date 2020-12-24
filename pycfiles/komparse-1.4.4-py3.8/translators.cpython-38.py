# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\komparse\translators.py
# Compiled at: 2020-03-07 08:14:04
# Size of source mod 2**32: 3489 bytes
from .ast import Ast

class TokenType(object):

    def __init__(self, token_type, id=''):
        self._token_type = token_type
        self._id = id

    def translate(self, grammar, token_stream):
        if not token_stream.has_next():
            return
        token = token_stream.peek()
        if self._token_type in token.types:
            token_stream.advance()
            return [Ast(self._token_type, token.value, self._id)]
        return


class Rule(object):

    def __init__(self, name, id=''):
        self._name = name
        self._id = id

    def translate(self, grammar, token_stream):
        translator = grammar.get_rule(self._name)
        nodes = translator.translate(grammar, token_stream)
        if nodes is not None:
            ast = Ast((self._name), id=(self._id))
            for node in nodes:
                ast.add_child(node)
            else:
                trans = grammar.get_ast_transform(self._name)
                if trans:
                    ast = trans(ast)
                    ast.id = self._id
                if self._name == grammar.get_root_rule():
                    ast.set_attr('root', 'true')
                return [
                 ast]

        return


class Sequence(object):

    def __init__(self, *elements):
        self._elements = elements

    def translate(self, grammar, token_stream):
        ret = []
        token_stream.open_transaction()
        for element in self._elements:
            nodes = element.translate(grammar, token_stream)
            if nodes is None:
                token_stream.undo()
                return None
            ret += nodes
        else:
            token_stream.commit()
            return ret


class OneOf(object):

    def __init__(self, *choices):
        self._choices = choices

    def translate(self, grammar, token_stream):
        token_stream.open_transaction()
        for choice in self._choices:
            nodes = choice.translate(grammar, token_stream)
            if nodes is not None:
                token_stream.commit()
                return nodes
        else:
            token_stream.undo()


class Optional(object):

    def __init__(self, translator):
        self._translator = translator

    def translate(self, grammar, token_stream):
        return self._translator.translate(grammar, token_stream) or []


class Many(object):

    def __init__(self, translator):
        self._translator = translator

    def translate--- This code section failed: ---

 L.  88         0  BUILD_LIST_0          0 
                2  STORE_FAST               'ret'

 L.  90         4  LOAD_FAST                'self'
                6  LOAD_ATTR                _translator
                8  LOAD_METHOD              translate
               10  LOAD_FAST                'grammar'
               12  LOAD_FAST                'token_stream'
               14  CALL_METHOD_2         2  ''
               16  STORE_FAST               'nodes'

 L.  91        18  LOAD_FAST                'nodes'
               20  LOAD_CONST               None
               22  COMPARE_OP               is-not
               24  POP_JUMP_IF_FALSE    40  'to 40'

 L.  92        26  LOAD_FAST                'ret'
               28  LOAD_FAST                'nodes'
               30  INPLACE_ADD      
               32  STORE_FAST               'ret'
               34  JUMP_BACK             4  'to 4'

 L.  94        36  BREAK_LOOP           40  'to 40'
               38  JUMP_BACK             4  'to 4'
             40_0  COME_FROM            24  '24'

 L.  95        40  LOAD_FAST                'ret'
               42  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 42


class OneOrMore(object):

    def __init__(self, translator):
        self._translator = translator

    def translate(self, grammar, token_stream):
        ret = []
        nodes = self._translator.translate(grammar, token_stream)
        if nodes is None:
            return
        else:
            ret += nodes
            while True:
                while True:
                    nodes = self._translator.translate(grammar, token_stream)
                    if nodes is not None:
                        ret += nodes

                break

        return ret