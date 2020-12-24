# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/mesonbuild/modules/check.py
# Compiled at: 2018-11-24 17:59:05
# Size of source mod 2**32: 9721 bytes
import re
from mesonbuild.modules import ExtensionModule, ModuleReturnValue
from mesonbuild import mesonlib
from mesonbuild import mlog
from mesonbuild.interpreter import ConfigurationDataHolder, extract_required_kwarg
from mesonbuild.interpreterbase import FeatureNew, FeatureNewKwargs, InterpreterException, check_stringlist, noKwargs, noPosargs, permittedKwargs
from lark import Lark, Token, Tree
BASE_KWARGS = {
 'variable',
 'required',
 'args'}
c_declaration_grammar = '\ndeclaration: IDENTIFIER -> declaration_name\n    | actual_declaration\n\n?actual_declaration: type declarator\n    | declaration LPAREN (parameter_list)? RPAREN\n    | declaration LSQUARE constant_expression RSQUARE\n\ntype: type_qualifier? type_specifier* IDENTIFIER type_qualifier? pointer?\n\ntype_specifier: STRUCT | UNION | ENUM | SIGNED | UNSIGNED\n\n?pointer: STAR type_qualifier* pointer?\n\n?constant_expression: IDENTIFIER | (NUMBER)+\n\nparameter_list: parameter\n    | parameter_list COMMA ELLIPSIS\n    | parameter_list COMMA parameter\n\nparameter: type parameter_declarator\n    | parameter LPAREN (parameter_list)? RPAREN\n    | parameter LSQUARE STATIC? constant_expression RSQUARE\n\nparameter_declarator: IDENTIFIER? -> parameter_name\n    | LPAREN parameter_declarator RPAREN\n    | pointer parameter_declarator\n    | parameter_declarator LPAREN (parameter_list)? RPAREN\n\ndeclarator: IDENTIFIER -> declaration_name\n    | LPAREN declarator RPAREN\n    | pointer declarator\n    | declarator LPAREN (parameter_list)? RPAREN\n\n?type_qualifier: CONST | VOLATILE\n\nCONST: "const"\nENUM: "enum"\nSIGNED: "signed"\nSTATIC: "static"\nSTRUCT: "struct"\nUNION: "union"\nUNSIGNED: "unsigned"\nVOLATILE: "volatile"\nIDENTIFIER: /[a-zA-Z_]\\w*/\nLPAREN: "("\nRPAREN: ")"\nLSQUARE: "["\nRSQUARE: "]"\nCOMMA: ","\nELLIPSIS: "..."\nSTAR: "*"\n\n%import common.LETTER\n%import common.NUMBER\n%import common.WS\n%ignore WS\n'

def c_check_prototype(tree, pkg, name):
    check = rewrite_declaration(tree, '(*_)') + ' = &(' + name + ');'
    return '\n'.join([
     '#include <%s>' % pkg,
     'void __check(void) {',
     check,
     '}'])


declaration_parsers = {'c':Lark(c_declaration_grammar, start='declaration'), 
 'cpp':Lark(c_declaration_grammar, start='declaration')}
prototype_checkers = {'c':c_check_prototype, 
 'cpp':c_check_prototype}

def extract_declaration_name(tree):
    if isinstance(tree, Token):
        return
    if tree.data == 'declaration_name':
        return str(tree.children[0])
    for c in tree.children:
        name = extract_declaration_name(c)
        if name:
            return name


def rewrite_declaration(tree, name):

    def tokenize(tree):
        if isinstance(tree, Token):
            return [
             str(tree)]
        if tree.data == 'declaration_name':
            return [
             name]
        if tree.data == 'parameter_name':
            return []
        tokens = []
        for c in tree.children:
            tokens += tokenize(c)

        return tokens

    tokens = tokenize(tree)
    out = ' '
    for tok in tokens:
        if len(tok) == 0:
            continue
        if not out[(-1)] in ',':
            if out[(-1)].isalnum():
                if tok[0].isalnum() or tok[0] in '*':
                    out += ' '
            out += tok

    return out.strip()


def is_lone_identifier(tree):
    return isinstance(tree, Tree) and tree.data == 'declaration_name'


class CheckModule(ExtensionModule):

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.options = {}

    def _compiler(self, state):
        language = self.options.get('language', None)
        compiler = state.compilers.get(language, None)
        if compiler:
            return (
             language, compiler)
        return next(iter(state.compilers.items()))

    def _checklog(self, which, what, ok):
        status = mlog.green('YES') if ok else mlog.red('NO')
        mlog.log('Checking that', which, mlog.bold(what, True), 'exists:', status)

    def _compile_args(self, compiler, state, kwargs):
        args = []
        opts = state.environment.coredata.compiler_options
        args += compiler.get_option_compile_args(opts)
        args += compiler.get_option_link_args(opts)
        args += mesonlib.stringlistify(self.options.get('args', []))
        args += mesonlib.stringlistify(kwargs.get('args', []))
        return args

    def _config(self, state):
        return self.options.setdefault('config', ConfigurationDataHolder(state.subproject))

    def _set_config_var(self, state, status, name, kwargs):
        config = self._config(state)
        varname = kwargs.get('variable', 'HAVE_' + re.sub('\\W', '_', name.upper()))
        if status:
            config.set_method(args=[varname, 1], kwargs={})

    @FeatureNew('check.symbol', '0.48.0')
    @permittedKwargs({'libraries'} | BASE_KWARGS)
    def symbol(self, state, args, kwargs):
        if len(args) != 1:
            raise InterpreterException('symbol takes exactly one argument.')
        else:
            check_stringlist(args)
            disabled, required, _ = extract_required_kwarg(kwargs, state.subproject)
            if disabled:
                return ModuleReturnValue(False, [False])
            name = args[0]
            lang, compiler = self._compiler(state)
            args = self._compile_args(compiler, state, kwargs)
            args += ('-l' + lib for lib in mesonlib.stringlistify(kwargs.get('libraries', [])))
            ok = compiler.has_function(name, '', state.environment, args, None)
            self._checklog('symbol', name, ok)
            self._set_config_var(state, ok, name, kwargs)
            if not ok:
                if required:
                    raise InterpreterException('{} symbol {} required but not found.'.format(lang, name))
        return ModuleReturnValue(ok, [ok])

    @FeatureNew('check.declaration', '0.48.0')
    @permittedKwargs(BASE_KWARGS)
    def declaration(self, state, args, kwargs):
        if len(args) != 2:
            raise InterpreterException('declaration takes exactly two arguments.')
        else:
            check_stringlist(args)
            disabled, required, _ = extract_required_kwarg(kwargs, state.subproject)
            if disabled:
                return ModuleReturnValue(False, [False])
            lang, compiler = self._compiler(state)
            parser = declaration_parsers.get(lang)
            if not parser:
                raise InterpreterException('no declaration parser for language %s' % lang)
            compiler_args = self._compile_args(compiler, state, kwargs)
            compiler_args += compiler.get_werror_args()
            pkg = args[0]
            decl = args[1]
            tree = parser.parse(decl)
            name = extract_declaration_name(tree)
            proto = rewrite_declaration(tree, name)
            check_prototype = not is_lone_identifier(tree)
            if check_prototype:
                checker = prototype_checkers.get(lang)
                if not checker:
                    raise InterpreterException('no checker program for language %s' % lang)
                prog = checker(tree, pkg, name)
                ok = compiler.compiles(prog, state.environment, compiler_args, None)
                status = mlog.green('YES') if ok else mlog.red('NO')
                mlog.log('Checking that', mlog.bold(name, True), 'has prototype', mlog.bold(proto, True), ':', status)
            else:
                ok = compiler.has_header_symbol(pkg, name, '', state.environment, compiler_args, None)
                self._checklog('declaration for', name, ok)
            self._set_config_var(state, ok, name, kwargs)
            if not ok:
                if required:
                    raise InterpreterException('{} declaration {} required but not found.'.format(lang, name))
        return ModuleReturnValue(ok, [ok])

    @FeatureNew('check.header', '0.48.0')
    @permittedKwargs(BASE_KWARGS)
    def header(self, state, args, kwargs):
        if len(args) != 1:
            raise InterpreterException('declaration takes exactly one argument.')
        else:
            check_stringlist(args)
            disabled, required, _ = extract_required_kwarg(kwargs, state.subproject)
            if disabled:
                return ModuleReturnValue(False, [False])
            name = args[0]
            lang, compiler = self._compiler(state)
            args = self._compile_args(compiler, state, kwargs)
            ok = compiler.has_header(name, '', state.environment, args, None)
            self._checklog('header', name, ok)
            self._set_config_var(state, ok, name, kwargs)
            if not ok:
                if required:
                    raise InterpreterException('{} header {} required but not found.'.format(lang, name))
        return ModuleReturnValue(ok, [ok])

    @FeatureNew('check.setup', '0.48.0')
    @permittedKwargs({'language', 'args', 'config'})
    @noPosargs
    def setup(self, state, args, kwargs):
        self.options.update(kwargs)
        return ModuleReturnValue(None, [])

    @FeatureNew('check.config', '0.48.0')
    @noKwargs
    @noPosargs
    def config(self, state, args, kwargs):
        config_data = self._config(state)
        return ModuleReturnValue(config_data, [config_data])


def initialize(*args, **kwargs):
    return CheckModule(*args, **kwargs)