# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python2.7/site-packages/grakopp/codegen/cpp.py
# Compiled at: 2014-08-01 21:55:59
from __future__ import absolute_import, division, print_function, unicode_literals
from grako.util import indent, trim, timestamp, ustr, urepr, compress_seq
from grako.exceptions import CodegenError
from grako.model import Node
from grako.codegen.cgbase import ModelRenderer, CodeGenerator

def cpp_repr(str):
    return b'R"(' + urepr(str)[1:-1] + b')"'


class CppCodeGenerator(CodeGenerator):

    def _find_renderer_class(self, item):
        if not isinstance(item, Node):
            return
        else:
            name = item.__class__.__name__
            renderer = globals().get(name, None)
            if not renderer or not issubclass(renderer, Base):
                raise CodegenError(b'Renderer for %s not found' % name)
            return renderer


def codegen(model):
    return CppCodeGenerator().render(model)


class Base(ModelRenderer):

    def defines(self):
        return []


class Void(Base):
    template = b';'


class Fail(Base):
    template = b'return _fail();'


class Comment(Base):
    template = b'\n        /* {comment} */\n\n        '


class EOF(Base):
    template = b'ast << _check_eof(); RETURN_IF_EXC(ast);'


class _Decorator(Base):

    def defines(self):
        return self.get_renderer(self.node.exp).defines()

    template = b'{exp}'


class Group(_Decorator):
    template = b'                ast << _group([this] () {{\n                    AstPtr ast = std::make_shared<Ast>();\n                {exp:1::}\n                    return ast;\n                }}); RETURN_IF_EXC(ast);               '


class Token(Base):

    def render_fields(self, fields):
        fields.update(token=cpp_repr(self.node.token))

    template = b'ast << _token({token}); RETURN_IF_EXC(ast);'


class Pattern(Base):

    def render_fields(self, fields):
        raw_repr = cpp_repr(self.node.pattern).replace(b'\\\\', b'\\')
        fields.update(pattern=raw_repr)

    template = b'ast << _pattern({pattern}); RETURN_IF_EXC(ast);'


class Lookahead(_Decorator):
    template = b'                ast << _if([this] () {{\n                    AstPtr ast = std::make_shared<Ast>();\n                {exp:1::}\n                    return ast;\n                }}); RETURN_IF_EXC(ast);                '


class NegativeLookahead(_Decorator):
    template = b'                ast << _ifnot([this] () {{\n                    AstPtr ast = std::make_shared<Ast>();\n                {exp:1::}\n                    return ast;\n                }}); RETURN_IF_EXC(ast);                '


class Sequence(Base):

    def defines(self):
        return [ d for s in self.node.sequence for d in s.defines() ]

    def render_fields(self, fields):
        fields.update(seq=(b'\n').join(self.rend(s) for s in self.node.sequence))

    template = b'\n                {seq}                '


class Choice(Base):

    def defines(self):
        return [ d for o in self.node.options for d in o.defines() ]

    def render_fields(self, fields):
        template = trim(self.option_template)
        options = [ template.format(option=indent(self.rend(o))) for o in self.node.options
                  ]
        options = (b'\n').join(o for o in options)
        firstset = (b' ').join(f[0] for f in sorted(self.node.firstset) if f)
        if firstset:
            error = b'expecting one of: ' + firstset
        else:
            error = b'no available options'
        fields.update(n=self.counter(), options=indent(options), error=cpp_repr(error))

    def render(self, **fields):
        if len(self.node.options) == 1:
            return self.rend(self.options[0], **fields)
        else:
            return super(Choice, self).render(**fields)

    option_template = b'                       ast << _option(success, [this] () {{\n                           AstPtr ast = std::make_shared<Ast>();\n                       {option}\n                           return ast;\n                       }}); if (success) return ast;                      '
    template = b'                ast << _choice([this] () {{\n                    AstPtr ast = std::make_shared<Ast>();\n                    bool success = false;\n                {options}\n                    return _error<FailedParse>({error});\n                }}); RETURN_IF_EXC(ast);               '


class Closure(_Decorator):

    def render_fields(self, fields):
        fields.update(n=self.counter())

    def render(self, **fields):
        if {
         ()} in self.node.exp.firstset:
            raise CodegenError(b'may repeat empty sequence')
        return b'\n' + super(Closure, self).render(**fields)

    template = b'                ast << _closure([this] () {{\n                    AstPtr ast = std::make_shared<Ast>();\n                {exp:1::}\n                    return ast;\n                }}); RETURN_IF_EXC(ast);                '


class PositiveClosure(Closure):

    def render_fields(self, fields):
        fields.update(n=self.counter())

    template = b'\n                ast << _positive_closure([this] () {{\n                    AstPtr ast = std::make_shared<Ast>();\n                {exp:1::}\n                    return ast;\n                }}); RETURN_IF_EXC(ast);                '


class Optional(_Decorator):
    template = b'                ast << _optional([this] () {{\n                    AstPtr ast = std::make_shared<Ast>();\n                {exp:1::}\n                    return ast;\n                }}); RETURN_IF_EXC(ast);               '


class Cut(Base):
    template = b'ast << _cut();'


class Named(_Decorator):

    def defines(self):
        return [
         (
          self.node.name, False)] + super(Named, self).defines()

    def render_fields(self, fields):
        fields.update(n=self.counter(), name=self.node.name)

    template = b'\n                (*ast)["{name}"] << [this] () {{\n                    AstPtr ast = std::make_shared<Ast>();\n                {exp:1::}\n                    return ast;\n                }}(); RETURN_IF_EXC(ast);                '


class NamedList(Named):

    def defines(self):
        return [
         (
          self.name, True)] + super(Named, self).defines()

    template = b'\n                (*ast)["{name}"] << [this] () {{\n                    AstPtr ast = std::make_shared<Ast>();\n                {exp:1::}\n                    return ast;\n                }}(); RETURN_IF_EXC(ast);                '


class Override(Named):

    def defines(self):
        return []


class OverrideList(NamedList):

    def defines(self):
        return []


class Special(Base):
    pass


class RuleRef(Base):
    template = b'ast << _{name}_(); RETURN_IF_EXC(ast);'


class RuleInclude(_Decorator):

    def render_fields(self, fields):
        super(RuleInclude, self).render_fields(fields)
        fields.update(exp=self.rend(self.node.rule.exp))

    template = b'\n                {exp}\n                '


class Rule(_Decorator):

    def render_fields(self, fields):
        self.reset_counter()
        params = kwparams = b''
        if self.node.params:
            params = (b', ').join(repr(ustr(self.rend(p))) for p in self.node.params)
        if self.node.kwparams:
            kwparams = (b', ').join(b'%s=%s' % (k, ustr(self.rend(v))) for k, v in self.kwparams)
        if params and kwparams:
            params = params + b', ' + kwparams
        elif kwparams:
            params = kwparams
        fields.update(params=params)
        defines = compress_seq(self.defines())
        sdefs = [ d for d, l in defines if not l ]
        ldefs = [ d for d, l in defines if l ]
        sdefs = set(sdefs)
        ldefs = set(ldefs) - sdefs
        if not (sdefs or ldefs):
            sdefines = b'AstPtr ast = std::make_shared<Ast>();'
        else:
            sdefines = b'AstPtr ast = std::make_shared<Ast>\n    (AstMap({\n        '
            elements = [ b'{ "%s" , AST_DEFAULT }' % d for d in sdefs ]
            elements += [ b'{ "%s" , AST_FORCELIST }' % d for d in ldefs ]
            sdefines += (b',\n        ').join(elements)
            sdefines += b'\n    }));'
        fields.update(defines=sdefines)

    template = b'\n                AstPtr {classname}Parser::_{name}_()\n                {{\n                    AstPtr ast = std::make_shared<Ast>();\n                    ast << _call("{name}", &Semantics::_{name}_, [this] () {{\n                {defines:2::}\n                {exp:2::}\n                        return ast;\n                    }}); RETURN_IF_EXC(ast);\n                    return ast;\n                }}\n                '


class BasedRule(Rule):

    def defines(self):
        return self.rhs.defines()

    def render_fields(self, fields):
        super(BasedRule, self).render_fields(fields)
        fields.update(exp=self.rhs)


class Grammar(Base):

    def render_fields(self, fields):
        abstract_template = trim(self.abstract_rule_template)
        abstract_rules = [ abstract_template.format(parsername=fields[b'name'], classname=fields[b'name'], name=rule.name) for rule in self.node.rules
                         ]
        abstract_rules = (b'\n').join(abstract_rules)
        if self.node.whitespace is not None:
            whitespace = b'set_whitespace(' + cpp_repr(self.node.whitespace) + b');'
        else:
            whitespace = b'// use default whitespace setting'
        if self.node.nameguard is not None:
            nameguard = b'true' if self.node.nameguard else b'false'
            nameguard = b'set_nameguard(' + nameguard + b');'
        else:
            nameguard = b'// use default nameguard setting'
        rules = (b'\n').join([ self.get_renderer(rule).render(classname=fields[b'name']) for rule in self.node.rules ])
        findruleitems = (b'\n').join([ b'{ "%s", &%sParser::_%s_ },' % (rule.name, fields[b'name'], rule.name) for rule in self.node.rules
                                     ])
        version = str(tuple(int(n) for n in str(timestamp()).split(b'.')))
        fields.update(rules=rules, findruleitems=indent(findruleitems), abstract_rules=abstract_rules, version=version, whitespace=whitespace, nameguard=nameguard)
        return

    abstract_rule_template = b'\n            AstPtr {classname}Semantics::_{name}_ (AstPtr& ast)\n            {{\n                return ast;\n            }}\n            '
    template = b'                /* -*- coding: utf-8 -*-\n                   CAVEAT UTILITOR\n\n                   This file was automatically generated by Grako++.\n                   https://pypi.python.org/pypi/grakopp/\n\n                   Any changes you make to it will be overwritten the next time\n                   the file is generated.\n                */\n                #include "_{name}.hpp"\n\n                // version__ = {version}\n\n                {abstract_rules}\n\n                {name}Parser::{name}Parser({name}Parser::Semantics* semantics)\n                  : Parser<{name}Parser::Semantics>(semantics)\n                {{\n                  {whitespace}\n                  {nameguard}\n                }}\n\n                {name}Parser::rule_method_t {name}Parser::find_rule(const std::string& name)\n                {{\n                  std::map<std::string, rule_method_t> map({{\n                {findruleitems}\n                  }});\n                  auto el = map.find(name);\n                  if (el != map.end())\n                    return el->second;\n                  return 0;\n                }}\n\n                {rules}\n\n                #ifdef GRAKOPP_MAIN\n                #include <grakopp/ast-io.hpp>\n\n                int\n                main(int argc, char *argv[])\n                {{\n                    std::ios_base::sync_with_stdio(false);\n\n                    int result = 0;\n                    std::list<std::string> args(argv + 1, argv + argc);\n                    bool validate = false;\n                    std::string validate_file;\n\n                    if (args.front() == "--test")\n                    {{\n                        args.pop_front();\n                        validate = true;\n                        validate_file = args.front();\n                        args.pop_front();\n                    }}\n\n                    BufferPtr buf = std::make_shared<Buffer>();\n                    {name}Parser parser;\n\n                    buf->from_file(args.front());\n                    args.pop_front();\n                    parser.set_buffer(buf);\n\n                    try\n                    {{\n                        std::string startrule(args.front());\n                        args.pop_front();\n                        {name}Parser::rule_method_t rule = parser.find_rule(startrule);\n                        AstPtr ast = (parser.*rule)();\n                        std::cout << *ast << "\\n";\n                        AstException *exc = ast->as_exception();\n                        if (exc)\n                            exc->_exc->_throw();\n\n                        if (validate)\n                        {{\n                            std::ifstream file;\n                            file.open(validate_file);\n                            AstPtr validate_ast = std::make_shared<Ast>();\n                            file >> std::noskipws >> std::ws >> validate_ast;\n                            if (ast != validate_ast)\n                                result = 1;\n                        }}\n\n                    }}\n                    catch(FailedParseBase& exc)\n                    {{\n                        std::cerr << "ERROR: " << exc << "\\n";\n                    }}\n                    catch (const std::invalid_argument& exc)\n                    {{\n                        std::cerr << "ERROR: parsing test file: " << exc.what() << "\\n";\n                        result = 2;\n                    }}\n\n                    return result;\n                }}\n                #endif /* GRAKOPP_MAIN */\n               '