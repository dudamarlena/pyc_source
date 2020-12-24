# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../py010parser/c_parser.py
# Compiled at: 2020-01-05 09:41:10
import re
from .ply import yacc
from . import c_ast
from .c_lexer import CLexer
from .plyparser import PLYParser, Coord, ParseError
from .ast_transforms import fix_switch_cases

class CParser(PLYParser):

    def __init__(self, lex_optimize=True, lextab='lextab', yacc_optimize=True, yacctab='yacctab', yacc_debug=False):
        """ Create a new CParser.

            Some arguments for controlling the debug/optimization
            level of the parser are provided. The defaults are
            tuned for release/performance mode.
            The simple rules for using them are:
            *) When tweaking CParser/CLexer, set these to False
            *) When releasing a stable parser, set to True

            lex_optimize:
                Set to False when you're modifying the lexer.
                Otherwise, changes in the lexer won't be used, if
                some lextab.py file exists.
                When releasing with a stable lexer, set to True
                to save the re-generation of the lexer table on
                each run.

            lextab:
                Points to the lex table that's used for optimized
                mode. Only if you're modifying the lexer and want
                some tests to avoid re-generating the table, make
                this point to a local lex table file (that's been
                earlier generated with lex_optimize=True)

            yacc_optimize:
                Set to False when you're modifying the parser.
                Otherwise, changes in the parser won't be used, if
                some parsetab.py file exists.
                When releasing with a stable parser, set to True
                to save the re-generation of the parser table on
                each run.

            yacctab:
                Points to the yacc table that's used for optimized
                mode. Only if you're modifying the parser, make
                this point to a local yacc table file

            yacc_debug:
                Generate a parser.out file that explains how yacc
                built the parsing table from the grammar.
        """
        self.clex = CLexer(error_func=self._lex_error_func, on_lbrace_func=self._lex_on_lbrace_func, on_rbrace_func=self._lex_on_rbrace_func, type_lookup_func=self._lex_type_lookup_func)
        self.clex.build(optimize=lex_optimize, lextab=lextab)
        self.tokens = self.clex.tokens
        rules_with_opt = [
         'abstract_declarator',
         'assignment_expression',
         'declaration_list',
         'declaration_specifiers',
         'designation',
         'expression',
         'identifier_list',
         'init_declarator_list',
         'parameter_type_list',
         'specifier_qualifier_list',
         'block_item_list',
         'type_qualifier_list',
         'struct_declarator_list',
         'metadata010',
         'enum_type']
        for rule in rules_with_opt:
            self._create_opt_rule(rule)

        self.cparser = yacc.yacc(module=self, start='external_block_item_list_or_empty', debug=yacc_debug, optimize=yacc_optimize, tabmodule=yacctab)
        self._scope_stack = [
         dict()]
        self._structs_with_params = {}
        self._last_yielded_token = None
        self._in_typedef_stack = [
         False]
        self._struct_level = 0
        self._in_enum = False
        return

    def parse(self, text, filename='', debuglevel=0, predefine_types=True, keep_scopes=False):
        """ Parses C code and returns an AST.

            text:
                A string containing the C source code

            filename:
                Name of the file being parsed (for meaningful
                error messages)

            debuglevel:
                Debug level to yacc
        """
        if not keep_scopes:
            self._scope_stack = [
             dict()]
            self._structs_with_params = {}
        predefined_ext = []
        if predefine_types:
            predefined_ext = self._define_010_typedefs().ext
        self.clex.filename = filename
        self.clex.reset_lineno()
        self._last_yielded_token = None
        res = self.cparser.parse(input=text, lexer=self.clex, debug=debuglevel)
        res.ext = predefined_ext + res.ext
        return res

    def _define_010_typedefs(self):
        typedefs = '\n        typedef unsigned int UINT;\n        typedef char byte;\n        typedef char CHAR;\n        typedef byte BYTE;\n        typedef unsigned char uchar;\n        typedef uchar ubyte;\n        typedef uchar UCHAR;\n        typedef ubyte UBYTE;\n        typedef short int16;\n        typedef short SHORT;\n        typedef short INT16;\n        typedef unsigned int16 uint16;\n        typedef unsigned short ushort;\n        typedef ushort wchar_t;\n        typedef ushort USHORT;\n        typedef uint16 UINT16;\n        typedef ushort WORD;\n        typedef int int32;\n        typedef int INT;\n        typedef int INT32;\n        typedef long LONG;\n        typedef unsigned int uint;\n        typedef uint uint32;\n        typedef unsigned long ulong;\n        typedef uint UINT;\n        typedef uint UINT32;\n        typedef ulong ULONG;\n        typedef uint DWORD;\n        typedef long long int64;\n        typedef int64 quad;\n        typedef int64 QUAD;\n        typedef int64 INT64;\n        typedef int64 __int64;\n        typedef unsigned int64 uint64;\n        typedef uint64 uquad;\n        typedef uint64 UQUAD;\n        typedef uint64 UINT64;\n        typedef uint64 QWORD;\n        typedef uint64 __uint64;\n        typedef float FLOAT;\n        typedef double DOUBLE;\n        typedef float hfloat;\n        typedef hfloat HFLOAT;\n\n        typedef struct tagDOSTIME {\n            WORD second  : 5;  \n            WORD minute : 6;    \n            WORD hour    : 5;   \n        } DOSTIME;\n\n        typedef struct tagDOSDATE {\n            WORD day  : 5;  \n            WORD month : 4;    \n            WORD year    : 7;   \n        } DOSDATE;\n\n        typedef struct _FILETIME {\n          DWORD dwLowDateTime;\n          DWORD dwHighDateTime;\n        } FILETIME;\n\n        typedef uint64 OLETIME;\n        typedef long time_t;\n        '
        self.clex.filename = '010_typedefs.h'
        self.clex.reset_lineno()
        return self.cparser.parse(input=typedefs, lexer=self.clex, debug=0)

    def _push_scope(self):
        self._in_typedef_stack.append(False)
        self._scope_stack.append(dict())

    def _pop_scope(self):
        assert len(self._scope_stack) > 1
        self._in_typedef_stack.pop()
        self._scope_stack.pop()

    def _add_typedef_name(self, name, coord):
        """ Add a new typedef name (ie a TYPEID) to the current scope
        """
        if not self._scope_stack[(-1)].get(name, True):
            self._parse_error('Typedef %r previously declared as non-typedef in this scope' % name, coord)
        self._scope_stack[(-1)][name] = True

    def _add_identifier(self, name, coord):
        """ Add a new object, function, or enum member name (ie an ID) to the
            current scope
        """
        if self._scope_stack[(-1)].get(name, False):
            self._parse_error('Non-typedef %r previously declared as typedef in this scope' % name, coord)
        self._scope_stack[(-1)][name] = False

    def _is_type_in_scope(self, name):
        """ Is *name* a typedef-name in the current scope?
        """
        for scope in reversed(self._scope_stack):
            in_scope = scope.get(name)
            if in_scope is not None:
                return in_scope

        return False

    def _lex_error_func(self, msg, line, column):
        self._parse_error(msg, self._coord(line, column))

    def _lex_on_lbrace_func(self):
        self._push_scope()

    def _lex_on_rbrace_func(self):
        self._pop_scope()

    def _lex_type_lookup_func(self, name):
        """ Looks up types that were previously defined with
            typedef.
            Passed to the lexer for recognizing identifiers that
            are types.
        """
        is_type = self._is_type_in_scope(name)
        return is_type

    def _get_yacc_lookahead_token(self):
        """ We need access to yacc's lookahead token in certain cases.
            This is the last token yacc requested from the lexer, so we
            ask the lexer.
        """
        return self.clex.last_token

    def _type_modify_decl(self, decl, modifier):
        """ Tacks a type modifier on a declarator, and returns
            the modified declarator.

            Note: the declarator and modifier may be modified
        """
        modifier_head = modifier
        modifier_tail = modifier
        while modifier_tail.type:
            modifier_tail = modifier_tail.type

        if isinstance(decl, c_ast.TypeDecl):
            modifier_tail.type = decl
            return modifier
        else:
            decl_tail = decl
            while not isinstance(decl_tail.type, c_ast.TypeDecl):
                decl_tail = decl_tail.type

            modifier_tail.type = decl_tail.type
            decl_tail.type = modifier_head
            return decl

    def _fix_decl_name_type(self, decl, typename):
        """ Fixes a declaration. Modifies decl.
        """
        type = decl
        while not isinstance(type, c_ast.TypeDecl):
            type = type.type

        decl.name = type.declname
        type.quals = decl.quals
        for tn in typename:
            if not isinstance(tn, c_ast.IdentifierType):
                if len(typename) > 1:
                    self._parse_error('Invalid multiple types specified', tn.coord)
                else:
                    type.type = tn
                    return decl

        if not typename:
            if not isinstance(decl.type, c_ast.FuncDecl):
                self._parse_error('Missing type in declaration', decl.coord)
            type.type = c_ast.IdentifierType([
             'int'], coord=decl.coord)
        else:
            type.type = c_ast.IdentifierType([ name for id in typename for name in id.names ], coord=typename[0].coord)
        return decl

    def _add_declaration_specifier(self, declspec, newspec, kind):
        """ Declaration specifiers are represented by a dictionary
            with the entries:
            * qual: a list of type qualifiers
            * storage: a list of storage type qualifiers
            * type: a list of type specifiers
            * function: a list of function specifiers

            This method is given a declaration specifier, and a
            new specifier of a given kind.
            Returns the declaration specifier, with the new
            specifier incorporated.
        """
        spec = declspec or dict(qual=[], storage=[], type=[], function=[])
        spec[kind].insert(0, newspec)
        return spec

    def _build_declarations(self, spec, decls, typedef_namespace=False, metadata=None):
        """ Builds a list of declarations all sharing the given specifiers.
            If typedef_namespace is true, each declared name is added
            to the "typedef namespace", which also includes objects,
            functions, and enum constants.
        """
        is_typedef = 'typedef' in spec['storage']
        declarations = []
        if decls[0].get('bitsize') is not None:
            pass
        else:
            if decls[0]['decl'] is None:
                if len(spec['type']) < 2 or len(spec['type'][(-1)].names) != 1 or not self._is_type_in_scope(spec['type'][(-1)].names[0]):
                    coord = '?'
                    for t in spec['type']:
                        if hasattr(t, 'coord'):
                            coord = t.coord
                            break

                    self._parse_error('Invalid declaration', coord)
                decls[0]['decl'] = c_ast.TypeDecl(declname=spec['type'][(-1)].names[0], type=None, quals=None, coord=spec['type'][(-1)].coord)
                del spec['type'][-1]
            else:
                if not isinstance(decls[0]['decl'], (
                 c_ast.Struct, c_ast.Union, c_ast.IdentifierType)):
                    decls_0_tail = decls[0]['decl']
                    while not isinstance(decls_0_tail, c_ast.TypeDecl):
                        decls_0_tail = decls_0_tail.type

                    if decls_0_tail.declname is None:
                        decls_0_tail.declname = spec['type'][(-1)].names[0]
                        del spec['type'][-1]
                for decl in decls:
                    assert decl['decl'] is not None
                    if is_typedef:
                        declaration = c_ast.Typedef(name=None, quals=spec['qual'], storage=spec['storage'], type=decl['decl'], coord=decl['decl'].coord)
                    else:
                        declaration = c_ast.Decl(name=None, quals=spec['qual'], storage=spec['storage'], funcspec=spec['function'], type=decl['decl'], init=decl.get('init'), bitsize=decl.get('bitsize'), coord=decl['decl'].coord)
                    if isinstance(declaration.type, (
                     c_ast.Struct, c_ast.Union, c_ast.IdentifierType)):
                        fixed_decl = declaration
                    else:
                        fixed_decl = self._fix_decl_name_type(declaration, spec['type'])
                    decld_type = ''
                    try:
                        decld_type = (' ').join(fixed_decl.type.type.type.names)
                    except Exception as e:
                        pass

                    if typedef_namespace:
                        if is_typedef:
                            self._add_typedef_name(fixed_decl.name, fixed_decl.coord)
                        else:
                            self._add_identifier(fixed_decl.name, fixed_decl.coord)
                    declarations.append(fixed_decl)

            if is_typedef and isinstance(spec['type'][0], c_ast.Struct) and (spec['type'][0].args is not None or spec['type'][0].name in self._structs_with_params):
                decld_name = declarations[0].type.declname
                self._structs_with_params[decld_name] = True
            for declaration in declarations:
                declaration.metadata = metadata

        return declarations

    def _build_function_definition(self, spec, decl, param_decls, body):
        """ Builds a function definition.
        """
        assert 'typedef' not in spec['storage']
        declaration = self._build_declarations(spec=spec, decls=[
         dict(decl=decl, init=None)], typedef_namespace=True)[0]
        return c_ast.FuncDef(decl=declaration, param_decls=param_decls, body=body, coord=decl.coord)

    def _select_struct_union_class(self, token):
        """ Given a token (either STRUCT or UNION), selects the
            appropriate AST class.
        """
        if token == 'struct':
            return c_ast.Struct
        else:
            return c_ast.Union

    precedence = (
     ('left', 'LOR'),
     ('left', 'LAND'),
     ('left', 'OR'),
     ('left', 'XOR'),
     ('left', 'AND'),
     ('left', 'EQ', 'NE'),
     ('left', 'GT', 'GE', 'LT', 'LE'),
     ('left', 'RSHIFT', 'LSHIFT'),
     ('left', 'PLUS', 'MINUS'),
     ('left', 'TIMES', 'DIVIDE', 'MOD'))

    def p_external_block_item_list_or_empty(self, p):
        """ external_block_item_list_or_empty   : external_block_item_list
                                                | empty
        """
        if p[1] is None:
            p[0] = c_ast.FileAST([])
        else:
            p[0] = c_ast.FileAST(p[1])
        return

    def p_external_block_item_list(self, p):
        """ external_block_item_list    : external_block_item
                                        | external_block_item_list external_block_item
        """
        p[0] = p[1] if len(p) == 2 or p[2] == [None] else p[1] + p[2]
        return

    def p_external_block_item(self, p):
        """ external_block_item : statement
                                | declaration
                                | external_declaration
        """
        self._in_typedef_stack[-1] = False
        p[0] = p[1] if isinstance(p[1], list) else [p[1]]

    def p_external_declaration_1(self, p):
        """ external_declaration    : function_definition
        """
        p[0] = [
         p[1]]

    def p_external_declaration_2(self, p):
        """ external_declaration    : declaration
        """
        p[0] = p[1]

    def p_external_declaration_3(self, p):
        """ external_declaration    : pp_directive
        """
        p[0] = p[1]

    def p_external_declaration_4(self, p):
        """ external_declaration    : SEMI
        """
        p[0] = None
        return

    def p_pp_directive(self, p):
        """ pp_directive  : PPHASH
        """
        self._parse_error('Directives not supported yet', self._coord(p.lineno(1)))

    def p_function_definition(self, p):
        """ function_definition : declaration_specifiers declarator declaration_list_opt compound_statement
        """
        spec = p[1]
        p[0] = self._build_function_definition(spec=spec, decl=p[2], param_decls=p[3], body=p[4])

    def p_statement(self, p):
        """ statement   : labeled_statement
                        | expression_statement
                        | compound_statement
                        | selection_statement
                        | iteration_statement
                        | jump_statement
        """
        p[0] = p[1]

    def p_decl_body_1(self, p):
        """ decl_body : declaration_specifiers init_declarator_list_opt
        """
        spec = p[1]
        if p[2] is None:
            ty = spec['type']
            s_u_or_e = (c_ast.Struct, c_ast.Union, c_ast.Enum)
            if len(ty) == 1 and isinstance(ty[0], s_u_or_e):
                decls = [
                 c_ast.Decl(name=None, quals=spec['qual'], storage=spec['storage'], funcspec=spec['function'], type=ty[0], init=None, bitsize=None, coord=ty[0].coord)]
            else:
                decls = self._build_declarations(spec=spec, decls=[
                 dict(decl=None, init=None)], typedef_namespace=True)
        else:
            decls = self._build_declarations(spec=spec, decls=p[2], typedef_namespace=True)
        p[0] = decls
        return

    def p_decl_body_2(self, p):
        """ decl_body : declaration_specifiers declarator COLON constant_expression
        """
        spec = p[1]
        if len(p) > 3:
            info = {'decl': p[2], 'bitsize': p[4]}
        else:
            info = {'decl': c_ast.TypeDecl(None, None, None), 'bitsize': p[2]}
        decls = self._build_declarations(spec=spec, decls=[
         info], typedef_namespace=True)
        p[0] = decls[0]
        return

    def p_declaration(self, p):
        """ declaration : decl_body metadata010_opt SEMI
        """
        metadata = p[2]
        if type(p[1]) is list:
            for decl in p[1]:
                decl.metadata = metadata

        p[0] = p[1]

    def p_declaration_list(self, p):
        """ declaration_list    : declaration
                                | declaration_list declaration
        """
        p[0] = p[1] if len(p) == 2 else p[1] + p[2]

    def p_declaration_specifiers_1(self, p):
        """ declaration_specifiers  : type_qualifier declaration_specifiers_opt
        """
        p[0] = self._add_declaration_specifier(p[2], p[1], 'qual')

    def p_declaration_specifiers_2(self, p):
        """ declaration_specifiers  : type_specifier declaration_specifiers_opt
        """
        p[0] = self._add_declaration_specifier(p[2], p[1], 'type')

    def p_declaration_specifiers_3(self, p):
        """ declaration_specifiers  : storage_class_specifier declaration_specifiers_opt
        """
        p[0] = self._add_declaration_specifier(p[2], p[1], 'storage')

    def p_declaration_specifiers_4(self, p):
        """ declaration_specifiers  : function_specifier declaration_specifiers_opt
        """
        p[0] = self._add_declaration_specifier(p[2], p[1], 'function')

    def p_storage_class_specifier(self, p):
        """ storage_class_specifier : AUTO
                                    | TYPEDEF
        """
        if p[1] == 'typedef':
            self._in_typedef_stack[-1] = True
        p[0] = p[1]

    def p_function_specifier(self, p):
        """ function_specifier  : INLINE
        """
        p[0] = p[1]

    def p_type_specifier_1(self, p):
        """ type_specifier  : VOID
                            | _BOOL
                            | CHAR
                            | SHORT
                            | INT
                            | LONG
                            | FLOAT
                            | DOUBLE
                            | STRING
                            | WSTRING
                            | _COMPLEX
                            | SIGNED
                            | UNSIGNED
        """
        p[0] = c_ast.IdentifierType([p[1]], coord=self._coord(p.lineno(1)))

    def p_type_specifier_2(self, p):
        """ type_specifier  : typedef_name
                            | enum_specifier
                            | struct_or_union_specifier
        """
        if not self._in_typedef_stack[(-1)] and (isinstance(p[1], c_ast.IdentifierType) and p[1].names[0] in self._structs_with_params and self._get_yacc_lookahead_token().type == 'ID' or isinstance(p[1], c_ast.Struct) and p[1].name in self._structs_with_params and self._get_yacc_lookahead_token().type == 'ID'):
            self.clex.insert_token('STRUCT_CALL')
        p[0] = p[1]

    def p_type_qualifier(self, p):
        """ type_qualifier  : CONST
                            | RESTRICT
                            | LOCAL
        """
        p[0] = p[1]

    def p_init_declarator_list_1(self, p):
        """ init_declarator_list    : init_declarator
                                    | init_declarator_list COMMA init_declarator
        """
        p[0] = p[1] + [p[3]] if len(p) == 4 else [p[1]]

    def p_init_declarator_list_2(self, p):
        """ init_declarator_list    : EQUALS initializer
        """
        p[0] = [
         dict(decl=None, init=p[2])]
        return

    def p_init_declarator_list_3(self, p):
        """ init_declarator_list    : abstract_declarator
        """
        p[0] = [
         dict(decl=p[1], init=None)]
        return

    def p_init_declarator(self, p):
        """ init_declarator : declarator
                            | declarator EQUALS initializer
        """
        p[0] = dict(decl=p[1], init=p[3] if len(p) > 2 else None)
        return

    def p_specifier_qualifier_list_1(self, p):
        """ specifier_qualifier_list    : type_qualifier specifier_qualifier_list_opt
        """
        p[0] = self._add_declaration_specifier(p[2], p[1], 'qual')

    def p_specifier_qualifier_list_2(self, p):
        """ specifier_qualifier_list    : type_specifier specifier_qualifier_list_opt
        """
        p[0] = self._add_declaration_specifier(p[2], p[1], 'type')

    def p_struct_or_union_specifier_1(self, p):
        """ struct_or_union_specifier   : struct_or_union ID
                                        | struct_or_union TYPEID
        """
        klass = self._select_struct_union_class(p[1])
        p[0] = klass(name=p[2], decls=None, coord=self._coord(p.lineno(2)))
        self._struct_level -= 1
        self._add_typedef_name(p[2], self._coord(p.lineno(1)))
        return

    def p_struct_or_union_specifier_2(self, p):
        """ struct_or_union_specifier : struct_or_union brace_open struct_item_list brace_close """
        klass = self._select_struct_union_class(p[1])
        p[0] = klass(name=None, decls=p[3], coord=self._coord(p.lineno(2)))
        self._struct_level -= 1
        return

    def p_struct_or_union_specifier_3(self, p):
        """ struct_or_union_specifier   : struct_or_union ID brace_open struct_item_list brace_close
                                        | struct_or_union TYPEID brace_open struct_item_list brace_close
        """
        klass = self._select_struct_union_class(p[1])
        p[0] = klass(name=p[2], decls=p[4], coord=self._coord(p.lineno(2)))
        self._add_typedef_name(p[2], self._coord(p.lineno(1)))
        self._struct_level -= 1

    def p_struct_or_union_specifier_4(self, p):
        """ struct_or_union_specifier   : struct_or_union ID LPAREN parameter_type_list RPAREN brace_open struct_item_list brace_close
                                        | struct_or_union TYPEID LPAREN parameter_type_list RPAREN brace_open struct_item_list brace_close
        """
        klass = self._select_struct_union_class(p[1])
        p[0] = klass(name=p[2], decls=p[7], coord=self._coord(p.lineno(2)), args=p[4])
        self._add_typedef_name(p[2], self._coord(p.lineno(1)))
        self._structs_with_params[p[2]] = True
        self._struct_level -= 1

    def p_struct_or_union_specifier_5(self, p):
        """ struct_or_union_specifier : struct_or_union LPAREN parameter_type_list RPAREN brace_open struct_item_list brace_close """
        klass = self._select_struct_union_class(p[1])
        p[0] = klass(name=None, decls=p[6], coord=self._coord(p.lineno(2)), args=p[3])
        self._struct_level -= 1
        return

    def p_struct_or_union(self, p):
        """ struct_or_union : STRUCT
                            | UNION
        """
        self._struct_level += 1
        p[0] = p[1]

    def p_struct_item_list(self, p):
        """ struct_item_list     : struct_item
                                 | struct_item_list struct_item
        """
        p[0] = p[1] if len(p) == 2 else p[1] + p[2]

    def p_struct_item_list2(self, p):
        """ struct_item_list     : 
        """
        p[0] = []

    def p_struct_item(self, p):
        """ struct_item    : block_item
                           | struct_declaration
        """
        p[0] = p[1]

    def p_struct_declaration_1(self, p):
        """ struct_declaration : specifier_qualifier_list struct_declarator_list_opt metadata010_opt SEMI
        """
        spec = p[1]
        assert 'typedef' not in spec['storage']
        metadata = p[3]
        if p[2] is not None:
            decls = self._build_declarations(spec=spec, decls=p[2], metadata=metadata)
        elif len(spec['type']) == 1:
            node = spec['type'][0]
            if isinstance(node, c_ast.Node):
                decl_type = node
            else:
                decl_type = c_ast.IdentifierType(node)
            decls = self._build_declarations(spec=spec, decls=[
             dict(decl=decl_type)])
        else:
            decls = self._build_declarations(spec=spec, decls=[
             dict(decl=None, init=None)])
        p[0] = decls
        return

    def p_struct_declaration_2(self, p):
        """ struct_declaration : specifier_qualifier_list abstract_declarator SEMI
        """
        p[0] = self._build_declarations(spec=p[1], decls=[
         dict(decl=p[2], init=None)])
        return

    def p_struct_declaration_3(self, p):
        """ struct_declaration : block_item
        """
        p[0] = p[1]

    def p_struct_declarator_list(self, p):
        """ struct_declarator_list  : struct_declarator
                                    | struct_declarator_list COMMA struct_declarator
        """
        p[0] = p[1] + [p[3]] if len(p) == 4 else [p[1]]

    def p_struct_declarator_1(self, p):
        """ struct_declarator : declarator
                              | init_declarator
        """
        if type(p[1]) is dict:
            p[0] = p[1]
        else:
            p[0] = {'decl': p[1], 'bitsize': None}
        return

    def p_struct_declarator_2(self, p):
        """ struct_declarator : declarator COLON constant_expression
                              | COLON constant_expression
        """
        if len(p) > 3:
            p[0] = {'decl': p[1], 'bitsize': p[3]}
        else:
            p[0] = {'decl': c_ast.TypeDecl(None, None, None), 'bitsize': p[2]}
        return

    def p_enum_specifier_1(self, p):
        """ enum_specifier  : ENUM ID
                            | ENUM TYPEID
        """
        p[0] = c_ast.Enum(p[2], None, self._coord(p.lineno(1)))
        return

    def p_enum_specifier_2(self, p):
        """ enum_specifier  : ENUM enum_type_opt brace_open enumerator_list brace_close
        """
        p[0] = c_ast.Enum(None, p[4], self._coord(p.lineno(1)), p[2])
        return

    def p_enum_specifier_3(self, p):
        """ enum_specifier  : ENUM enum_type ID brace_open enumerator_list brace_close
                            | ENUM enum_type TYPEID brace_open enumerator_list brace_close
                            | ENUM TYPEID brace_open enumerator_list brace_close
                            | ENUM ID brace_open enumerator_list brace_close
        """
        if len(p) == 6:
            p[0] = c_ast.Enum(p[2], p[4], self._coord(p.lineno(1)), None)
        else:
            p[0] = c_ast.Enum(p[3], p[5], self._coord(p.lineno(1)), p[2])
        self._add_typedef_name(p[0].name, self._coord(p.lineno(1)))
        return

    def p_enum_type(self, p):
        """ enum_type   : LT type_specifier GT
        """
        p[0] = p[2]

    def p_enumerator_list(self, p):
        """ enumerator_list : enumerator
                            | enumerator_list COMMA
                            | enumerator_list COMMA enumerator
        """
        if len(p) == 2:
            p[0] = c_ast.EnumeratorList([p[1]], p[1].coord)
        elif len(p) == 3:
            p[0] = p[1]
        else:
            p[1].enumerators.append(p[3])
            p[0] = p[1]

    def p_enumerator(self, p):
        """ enumerator  : ID
                        | ID EQUALS constant_expression
        """
        if len(p) == 2:
            enumerator = c_ast.Enumerator(p[1], None, self._coord(p.lineno(1)))
        else:
            enumerator = c_ast.Enumerator(p[1], p[3], self._coord(p.lineno(1)))
        self._add_identifier(enumerator.name, enumerator.coord)
        p[0] = enumerator
        return

    def p_declarator_1(self, p):
        """ declarator  : direct_declarator
        """
        p[0] = p[1]

    def p_declarator_2(self, p):
        """ declarator  : pointer direct_declarator
        """
        p[0] = self._type_modify_decl(p[2], p[1])

    def p_declarator_3(self, p):
        """ declarator : byref direct_declarator
        """
        p[0] = self._type_modify_decl(p[2], p[1])

    def p_declarator_4(self, p):
        """ declarator  : pointer TYPEID
        """
        decl = c_ast.TypeDecl(declname=p[2], type=None, quals=None, coord=self._coord(p.lineno(2)))
        p[0] = self._type_modify_decl(decl, p[1])
        return

    def p_direct_declarator_1(self, p):
        """ direct_declarator   : ID
        """
        p[0] = c_ast.TypeDecl(declname=p[1], type=None, quals=None, coord=self._coord(p.lineno(1)))
        return

    def p_direct_declarator_2(self, p):
        """ direct_declarator   : LPAREN declarator RPAREN
        """
        p[0] = p[2]

    def p_direct_declarator_3(self, p):
        """ direct_declarator   : direct_declarator LBRACKET type_qualifier_list_opt assignment_expression_opt RBRACKET
        """
        arr = c_ast.ArrayDecl(type=None, dim=p[4], dim_quals=p[3] if p[3] != None else [], coord=p[1].coord)
        p[0] = self._type_modify_decl(decl=p[1], modifier=arr)
        return

    def p_direct_declarator_5(self, p):
        """ direct_declarator   : direct_declarator LBRACKET type_qualifier_list_opt TIMES RBRACKET
        """
        arr = c_ast.ArrayDecl(type=None, dim=c_ast.ID(p[4], self._coord(p.lineno(4))), dim_quals=p[3] if p[3] != None else [], coord=p[1].coord)
        p[0] = self._type_modify_decl(decl=p[1], modifier=arr)
        return

    def p_direct_declarator_6(self, p):
        """ direct_declarator   : direct_declarator LPAREN RPAREN
                                | direct_declarator LPAREN parameter_type_list RPAREN
                                | direct_declarator LPAREN identifier_list_opt RPAREN
        """
        if len(p) == 4:
            p[3] = None
        func = c_ast.FuncDecl(args=p[3], type=None, coord=p[1].coord)
        if self._get_yacc_lookahead_token().type == 'LBRACE':
            if func.args is not None:
                for param in func.args.params:
                    if isinstance(param, c_ast.EllipsisParam):
                        break
                    self._add_identifier(param.name, param.coord)

        p[0] = self._type_modify_decl(decl=p[1], modifier=func)
        return

    def p_direct_declarator_7(self, p):
        """ direct_declarator   : direct_declarator STRUCT_CALL LPAREN argument_expression_list RPAREN
        """
        p[0] = c_ast.StructCallTypeDecl(declname=p[1].declname, quals=None, type=p[1], coord=self._coord(p.lineno(1)), args=p[4])
        return

    def p_pointer(self, p):
        """ pointer : TIMES type_qualifier_list_opt
                    | TIMES type_qualifier_list_opt pointer
        """
        coord = self._coord(p.lineno(1))
        p[0] = c_ast.PtrDecl(quals=p[2] or [], type=p[3] if len(p) > 3 else None, coord=coord)
        return

    def p_byref(self, p):
        """ byref : AND type_qualifier_list_opt
        """
        coord = self._coord(p.lineno(1))
        p[0] = c_ast.ByRefDecl(quals=p[2] or [], type=p[3] if len(p) > 3 else None, coord=coord)
        return

    def p_type_qualifier_list(self, p):
        """ type_qualifier_list : type_qualifier
                                | type_qualifier_list type_qualifier
        """
        p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]

    def p_parameter_type_list(self, p):
        """ parameter_type_list : parameter_list
                                | parameter_list COMMA ELLIPSIS
        """
        if len(p) > 2:
            p[1].params.append(c_ast.EllipsisParam(self._coord(p.lineno(3))))
        p[0] = p[1]

    def p_parameter_list(self, p):
        """ parameter_list  : parameter_declaration
                            | parameter_list COMMA parameter_declaration
        """
        if len(p) == 2:
            p[0] = c_ast.ParamList([p[1]], p[1].coord)
        else:
            p[1].params.append(p[3])
            p[0] = p[1]

    def p_parameter_declaration_1(self, p):
        """ parameter_declaration   : declaration_specifiers declarator
        """
        spec = p[1]
        if not spec['type']:
            spec['type'] = [c_ast.IdentifierType(['int'], coord=self._coord(p.lineno(1)))]
        p[0] = self._build_declarations(spec=spec, decls=[
         dict(decl=p[2])])[0]

    def p_parameter_declaration_2(self, p):
        """ parameter_declaration   : declaration_specifiers abstract_declarator_opt
        """
        spec = p[1]
        if not spec['type']:
            spec['type'] = [c_ast.IdentifierType(['int'], coord=self._coord(p.lineno(1)))]
        if len(spec['type']) > 1 and len(spec['type'][(-1)].names) == 1 and self._is_type_in_scope(spec['type'][(-1)].names[0]):
            decl = self._build_declarations(spec=spec, decls=[
             dict(decl=p[2], init=None)])[0]
        else:
            decl = c_ast.Typename(quals=spec['qual'], type=p[2] or c_ast.TypeDecl(None, None, None), coord=self._coord(p.lineno(2)))
            typename = spec['type']
            decl = self._fix_decl_name_type(decl, typename)
        p[0] = decl
        return

    def p_parameter_declaration_3(self, p):
        """ parameter_declaration   : identifier declarator
        """
        id_ = p[1]
        spec = self._add_declaration_specifier(None, id_, 'type')
        decl = self._build_declarations(spec=spec, decls=[
         dict(decl=p[2], init=None)])[0]
        p[0] = decl
        return

    def p_identifier_list(self, p):
        """ identifier_list : identifier
                            | identifier_list COMMA identifier
        """
        if len(p) == 2:
            p[0] = c_ast.ParamList([p[1]], p[1].coord)
        else:
            p[1].params.append(p[3])
            p[0] = p[1]

    def p_initializer_1(self, p):
        """ initializer : assignment_expression
        """
        p[0] = p[1]

    def p_initializer_2(self, p):
        """ initializer : brace_open initializer_list brace_close
                        | brace_open initializer_list COMMA brace_close
        """
        p[0] = p[2]

    def p_initializer_list(self, p):
        """ initializer_list    : designation_opt initializer
                                | initializer_list COMMA designation_opt initializer
        """
        if len(p) == 3:
            init = p[2] if p[1] is None else c_ast.NamedInitializer(p[1], p[2])
            p[0] = c_ast.InitList([init], p[2].coord)
        else:
            init = p[4] if p[3] is None else c_ast.NamedInitializer(p[3], p[4])
            p[1].exprs.append(init)
            p[0] = p[1]
        return

    def p_designation(self, p):
        """ designation : designator_list EQUALS
        """
        p[0] = p[1]

    def p_designator_list(self, p):
        """ designator_list : designator
                            | designator_list designator
        """
        p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]

    def p_designator(self, p):
        """ designator  : LBRACKET constant_expression RBRACKET
                        | PERIOD identifier
        """
        p[0] = p[2]

    def p_type_name(self, p):
        """ type_name   : specifier_qualifier_list abstract_declarator_opt
        """
        typename = c_ast.Typename(quals=p[1]['qual'], type=p[2] or c_ast.TypeDecl(None, None, None), coord=self._coord(p.lineno(2)))
        p[0] = self._fix_decl_name_type(typename, p[1]['type'])
        return

    def p_abstract_declarator_1(self, p):
        """ abstract_declarator     : pointer
        """
        dummytype = c_ast.TypeDecl(None, None, None)
        p[0] = self._type_modify_decl(decl=dummytype, modifier=p[1])
        return

    def p_abstract_declarator_2(self, p):
        """ abstract_declarator     : pointer direct_abstract_declarator
        """
        p[0] = self._type_modify_decl(p[2], p[1])

    def p_abstract_declarator_3(self, p):
        """ abstract_declarator     : direct_abstract_declarator
        """
        p[0] = p[1]

    def p_direct_abstract_declarator_1(self, p):
        """ direct_abstract_declarator  : LPAREN abstract_declarator RPAREN """
        p[0] = p[2]

    def p_direct_abstract_declarator_2(self, p):
        """ direct_abstract_declarator  : direct_abstract_declarator LBRACKET assignment_expression_opt RBRACKET
        """
        arr = c_ast.ArrayDecl(type=None, dim=p[3], dim_quals=[], coord=p[1].coord)
        p[0] = self._type_modify_decl(decl=p[1], modifier=arr)
        return

    def p_direct_abstract_declarator_3(self, p):
        """ direct_abstract_declarator  : LBRACKET assignment_expression_opt RBRACKET
        """
        p[0] = c_ast.ArrayDecl(type=c_ast.TypeDecl(None, None, None), dim=p[2], dim_quals=[], coord=self._coord(p.lineno(1)))
        return

    def p_direct_abstract_declarator_4(self, p):
        """ direct_abstract_declarator  : direct_abstract_declarator LBRACKET TIMES RBRACKET
        """
        arr = c_ast.ArrayDecl(type=None, dim=c_ast.ID(p[3], self._coord(p.lineno(3))), dim_quals=[], coord=p[1].coord)
        p[0] = self._type_modify_decl(decl=p[1], modifier=arr)
        return

    def p_direct_abstract_declarator_5(self, p):
        """ direct_abstract_declarator  : LBRACKET TIMES RBRACKET
        """
        p[0] = c_ast.ArrayDecl(type=c_ast.TypeDecl(None, None, None), dim=c_ast.ID(p[3], self._coord(p.lineno(3))), dim_quals=[], coord=self._coord(p.lineno(1)))
        return

    def p_direct_abstract_declarator_6(self, p):
        """ direct_abstract_declarator  : direct_abstract_declarator LPAREN parameter_type_list_opt RPAREN
        """
        func = c_ast.FuncDecl(args=p[3], type=None, coord=p[1].coord)
        p[0] = self._type_modify_decl(decl=p[1], modifier=func)
        return

    def p_direct_abstract_declarator_7(self, p):
        """ direct_abstract_declarator  : LPAREN parameter_type_list_opt RPAREN
        """
        p[0] = c_ast.FuncDecl(args=p[2], type=c_ast.TypeDecl(None, None, None), coord=self._coord(p.lineno(1)))
        return

    def p_block_item(self, p):
        """ block_item  : declaration
                        | statement
        """
        p[0] = p[1] if isinstance(p[1], list) else [p[1]]

    def p_block_item_list(self, p):
        """ block_item_list : block_item
                            | block_item_list block_item
        """
        p[0] = p[1] if len(p) == 2 or p[2] == [None] else p[1] + p[2]
        return

    def p_metadata010(self, p):
        """ metadata010  : METADATA010
        """
        meta = c_ast.Metadata010(p[1])
        p[0] = meta

    def p_compound_statement_1(self, p):
        """ compound_statement : brace_open block_item_list_opt brace_close """
        p[0] = c_ast.Compound(block_items=p[2], coord=self._coord(p.lineno(1)))

    def p_labeled_statement_1(self, p):
        """ labeled_statement : ID COLON statement """
        p[0] = c_ast.Label(p[1], p[3], self._coord(p.lineno(1)))

    def p_labeled_statement_2(self, p):
        """ labeled_statement : CASE constant_expression COLON block_item """
        p[0] = c_ast.Case(p[2], [p[4]], self._coord(p.lineno(1)))

    def p_labeled_statement_3(self, p):
        """ labeled_statement : DEFAULT COLON block_item """
        p[0] = c_ast.Default([p[3]], self._coord(p.lineno(1)))

    def p_selection_statement_1(self, p):
        """ selection_statement : IF LPAREN expression RPAREN statement
                                | IF LPAREN expression RPAREN declaration """
        p[0] = c_ast.If(p[3], p[5], None, self._coord(p.lineno(1)))
        return

    def p_selection_statement_2(self, p):
        """ selection_statement : IF LPAREN expression RPAREN statement ELSE statement
                                | IF LPAREN expression RPAREN statement ELSE declaration
                                | IF LPAREN expression RPAREN declaration ELSE statement
                                | IF LPAREN expression RPAREN declaration ELSE declaration
        """
        p[0] = c_ast.If(p[3], p[5], p[7], self._coord(p.lineno(1)))

    def p_selection_statement_3(self, p):
        """ selection_statement : SWITCH LPAREN expression RPAREN statement """
        p[0] = fix_switch_cases(c_ast.Switch(p[3], p[5], self._coord(p.lineno(1))))

    def p_iteration_statement_1(self, p):
        """ iteration_statement : WHILE LPAREN expression RPAREN statement
                                | WHILE LPAREN expression RPAREN declaration """
        p[0] = c_ast.While(p[3], p[5], self._coord(p.lineno(1)))

    def p_iteration_statement_2(self, p):
        """ iteration_statement : DO statement WHILE LPAREN expression RPAREN SEMI
                                | DO declaration WHILE LPAREN expression RPAREN SEMI """
        p[0] = c_ast.DoWhile(p[5], p[2], self._coord(p.lineno(1)))

    def p_iteration_statement_3(self, p):
        """ iteration_statement : FOR LPAREN expression_opt SEMI expression_opt SEMI expression_opt RPAREN statement
                                | FOR LPAREN expression_opt SEMI expression_opt SEMI expression_opt RPAREN declaration
        """
        p[0] = c_ast.For(p[3], p[5], p[7], p[9], self._coord(p.lineno(1)))

    def p_iteration_statement_4(self, p):
        """ iteration_statement : FOR LPAREN declaration expression_opt SEMI expression_opt RPAREN statement
                                | FOR LPAREN declaration expression_opt SEMI expression_opt RPAREN declaration """
        p[0] = c_ast.For(c_ast.DeclList(p[3], self._coord(p.lineno(1))), p[4], p[6], p[8], self._coord(p.lineno(1)))

    def p_jump_statement_1(self, p):
        """ jump_statement  : BREAK SEMI """
        p[0] = c_ast.Break(self._coord(p.lineno(1)))

    def p_jump_statement_2(self, p):
        """ jump_statement  : CONTINUE SEMI """
        p[0] = c_ast.Continue(self._coord(p.lineno(1)))

    def p_jump_statement_3(self, p):
        """ jump_statement  : RETURN expression SEMI
                            | RETURN SEMI
        """
        p[0] = c_ast.Return(p[2] if len(p) == 4 else None, self._coord(p.lineno(1)))
        return

    def p_expression_statement(self, p):
        """ expression_statement : expression_opt SEMI """
        if p[1] is None:
            p[0] = c_ast.EmptyStatement(self._coord(p.lineno(1)))
        else:
            p[0] = p[1]
        return

    def p_expression(self, p):
        """ expression  : assignment_expression
                        | expression COMMA assignment_expression
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            if not isinstance(p[1], c_ast.ExprList):
                p[1] = c_ast.ExprList([p[1]], p[1].coord)
            p[1].exprs.append(p[3])
            p[0] = p[1]

    def p_typedef_name(self, p):
        """ typedef_name : TYPEID """
        p[0] = c_ast.IdentifierType([p[1]], coord=self._coord(p.lineno(1)))

    def p_assignment_expression(self, p):
        """ assignment_expression   : conditional_expression
                                    | unary_expression assignment_operator assignment_expression
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = c_ast.Assignment(p[2], p[1], p[3], p[1].coord)

    def p_assignment_operator(self, p):
        """ assignment_operator : EQUALS
                                | XOREQUAL
                                | TIMESEQUAL
                                | DIVEQUAL
                                | MODEQUAL
                                | PLUSEQUAL
                                | MINUSEQUAL
                                | LSHIFTEQUAL
                                | RSHIFTEQUAL
                                | ANDEQUAL
                                | OREQUAL
        """
        p[0] = p[1]

    def p_constant_expression(self, p):
        """ constant_expression : conditional_expression """
        p[0] = p[1]

    def p_conditional_expression(self, p):
        """ conditional_expression  : binary_expression
                                    | binary_expression CONDOP expression COLON conditional_expression
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = c_ast.TernaryOp(p[1], p[3], p[5], p[1].coord)

    def p_binary_expression(self, p):
        """ binary_expression   : cast_expression
                                | binary_expression TIMES binary_expression
                                | binary_expression DIVIDE binary_expression
                                | binary_expression MOD binary_expression
                                | binary_expression PLUS binary_expression
                                | binary_expression MINUS binary_expression
                                | binary_expression RSHIFT binary_expression
                                | binary_expression LSHIFT binary_expression
                                | binary_expression LT binary_expression
                                | binary_expression LE binary_expression
                                | binary_expression GE binary_expression
                                | binary_expression GT binary_expression
                                | binary_expression EQ binary_expression
                                | binary_expression NE binary_expression
                                | binary_expression AND binary_expression
                                | binary_expression OR binary_expression
                                | binary_expression XOR binary_expression
                                | binary_expression LAND binary_expression
                                | binary_expression LOR binary_expression
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = c_ast.BinaryOp(p[2], p[1], p[3], p[1].coord)

    def p_cast_expression_1(self, p):
        """ cast_expression : unary_expression """
        p[0] = p[1]

    def p_cast_expression_2(self, p):
        """ cast_expression : LPAREN type_name RPAREN cast_expression """
        p[0] = c_ast.Cast(p[2], p[4], self._coord(p.lineno(1)))

    def p_unary_expression_1(self, p):
        """ unary_expression    : postfix_expression """
        p[0] = p[1]

    def p_unary_expression_2(self, p):
        """ unary_expression    : PLUSPLUS unary_expression
                                | MINUSMINUS unary_expression
                                | unary_operator cast_expression
        """
        p[0] = c_ast.UnaryOp(p[1], p[2], p[2].coord)

    def p_unary_expression_3(self, p):
        """ unary_expression    : SIZEOF unary_expression
                                | SIZEOF LPAREN type_name RPAREN
                                | EXISTS unary_expression
                                | EXISTS LPAREN type_name RPAREN
                                | FUNCTION_EXISTS unary_expression
                                | FUNCTION_EXISTS LPAREN type_name RPAREN
                                | PARENTOF unary_expression
                                | PARENTOF LPAREN type_name RPAREN
                                | STARTOF unary_expression
                                | STARTOF LPAREN type_name RPAREN
        """
        p[0] = c_ast.UnaryOp(p[1], p[2] if len(p) == 3 else p[3], self._coord(p.lineno(1)))

    def p_unary_operator(self, p):
        """ unary_operator  : AND
                            | TIMES
                            | PLUS
                            | MINUS
                            | NOT
                            | LNOT
        """
        p[0] = p[1]

    def p_postfix_expression_1(self, p):
        """ postfix_expression  : primary_expression """
        p[0] = p[1]

    def p_postfix_expression_2(self, p):
        """ postfix_expression  : postfix_expression LBRACKET expression RBRACKET """
        p[0] = c_ast.ArrayRef(p[1], p[3], p[1].coord)

    def p_postfix_expression_3(self, p):
        """ postfix_expression  : postfix_expression LPAREN argument_expression_list RPAREN
                                | postfix_expression LPAREN RPAREN
        """
        p[0] = c_ast.FuncCall(p[1], p[3] if len(p) == 5 else None, p[1].coord)
        return

    def p_postfix_expression_4(self, p):
        """ postfix_expression  : postfix_expression PERIOD ID
                                | postfix_expression PERIOD TYPEID
                                | postfix_expression ARROW ID
                                | postfix_expression ARROW TYPEID
        """
        field = c_ast.ID(p[3], self._coord(p.lineno(3)))
        p[0] = c_ast.StructRef(p[1], p[2], field, p[1].coord)

    def p_postfix_expression_5(self, p):
        """ postfix_expression  : postfix_expression PLUSPLUS
                                | postfix_expression MINUSMINUS
        """
        p[0] = c_ast.UnaryOp('p' + p[2], p[1], p[1].coord)

    def p_postfix_expression_6(self, p):
        """ postfix_expression  : LPAREN type_name RPAREN brace_open initializer_list brace_close
                                | LPAREN type_name RPAREN brace_open initializer_list COMMA brace_close
        """
        p[0] = c_ast.CompoundLiteral(p[2], p[5])

    def p_primary_expression_1(self, p):
        """ primary_expression  : identifier """
        p[0] = p[1]

    def p_primary_expression_2(self, p):
        """ primary_expression  : constant """
        p[0] = p[1]

    def p_primary_expression_3(self, p):
        """ primary_expression  : unified_string_literal
                                | unified_wstring_literal
        """
        p[0] = p[1]

    def p_primary_expression_4(self, p):
        """ primary_expression  : LPAREN expression RPAREN """
        p[0] = p[2]

    def p_argument_expression_list(self, p):
        """ argument_expression_list    : assignment_expression
                                        | argument_expression_list COMMA assignment_expression
        """
        if len(p) == 2:
            p[0] = c_ast.ExprList([p[1]], p[1].coord)
        else:
            p[1].exprs.append(p[3])
            p[0] = p[1]

    def p_identifier(self, p):
        """ identifier  : ID """
        p[0] = c_ast.ID(p[1], self._coord(p.lineno(1)))

    def p_constant_1(self, p):
        """ constant    : INT_CONST_DEC
                        | INT_CONST_OCT
                        | INT_CONST_HEX
        """
        p[0] = c_ast.Constant('int', p[1], self._coord(p.lineno(1)))

    def p_constant_2(self, p):
        """ constant    : FLOAT_CONST
                        | HEX_FLOAT_CONST
        """
        p[0] = c_ast.Constant('float', p[1], self._coord(p.lineno(1)))

    def p_constant_3(self, p):
        """ constant    : CHAR_CONST
                        | WCHAR_CONST
        """
        p[0] = c_ast.Constant('char', p[1], self._coord(p.lineno(1)))

    def p_unified_string_literal(self, p):
        """ unified_string_literal  : STRING_LITERAL
                                    | unified_string_literal STRING_LITERAL
        """
        if len(p) == 2:
            p[0] = c_ast.Constant('string', p[1], self._coord(p.lineno(1)))
        else:
            p[1].value = p[1].value[:-1] + p[2][1:]
            p[0] = p[1]

    def p_unified_wstring_literal(self, p):
        """ unified_wstring_literal : WSTRING_LITERAL
                                    | unified_wstring_literal WSTRING_LITERAL
        """
        if len(p) == 2:
            p[0] = c_ast.Constant('string', p[1], self._coord(p.lineno(1)))
        else:
            p[1].value = p[1].value.rstrip()[:-1] + p[2][2:]
            p[0] = p[1]

    def p_brace_open(self, p):
        """ brace_open  :   LBRACE
        """
        p[0] = p[1]

    def p_brace_close(self, p):
        """ brace_close :   RBRACE
        """
        p[0] = p[1]

    def p_empty(self, p):
        """empty : """
        p[0] = None
        return

    def p_error(self, p):
        if p:
            self._parse_error('before: %s' % p.value, self._coord(lineno=p.lineno, column=self.clex.find_tok_column(p)))
        else:
            self._parse_error('At end of input', '')


if __name__ == '__main__':
    import pprint, time, sys