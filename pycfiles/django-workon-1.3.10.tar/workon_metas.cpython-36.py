# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/workon/templatetags/workon_metas.py
# Compiled at: 2018-08-13 08:59:58
# Size of source mod 2**32: 3375 bytes
import re
from django import template
__all__ = [
 'lazy_register']

def lazy_register(register):

    def _setup_metas_dict(parser):
        try:
            parser._metas
        except AttributeError:
            parser._metas = {}

    class DefineMetaNode(template.Node):

        def __init__(self, name, nodelist, args):
            self.name = name
            self.nodelist = nodelist
            self.args = args

        def render(self, context):
            return ''

    @register.tag(name='meta')
    def do_meta(parser, token):
        try:
            args = token.split_contents()
            tag_name, meta_name, args = args[0], args[1], args[2:]
        except IndexError as e:
            raise template.TemplateSyntaxError("'%s' tag requires at least one argument (macro name)" % token.contents.split()[0])

        r_valid_arg_name = re.compile('^[a-zA-Z0-9_]+$')
        for arg in args:
            if not r_valid_arg_name.match(arg):
                raise template.TemplateSyntaxError("Argument '%s' to macro '%s' contains illegal characters. Only alphanumeric characters and '_' are allowed." % (arg, macro_name))

        nodelist = parser.parse(('endmeta', ))
        parser.delete_first_token()
        _setup_metas_dict(parser)
        if meta_name not in parser._metas:
            parser._metas[meta_name] = DefineMetaNode(meta_name, nodelist, args)
        return parser._metas[meta_name]

    class UseMetaNode(template.Node):

        def __init__(self, meta, filter_expressions, truncate=None):
            self.nodelist = meta.nodelist
            self.args = meta.args
            self.filter_expressions = filter_expressions
            self.truncate = truncate

        def render(self, context):
            for arg, fe in [(self.args[i], self.filter_expressions[i]) for i in range(len(self.args))]:
                context[arg] = fe.resolve(context)

            return self.nodelist.render(context).strip()

    class NoopNode(template.Node):

        def render(self, context):
            return ''

    @register.tag(name='usemeta')
    def do_usemeta(parser, token, truncate=None):
        try:
            args = token.split_contents()
            tag_name, meta_name, values = args[0], args[1], args[2:]
        except IndexError as e:
            raise template.TemplateSyntaxError("'%s' tag requires at least one argument (macro name)" % token.contents.split()[0])

        try:
            meta = parser._metas[meta_name]
        except (AttributeError, KeyError):
            return NoopNode()
        else:
            if len(values) != len(meta.args):
                raise template.TemplateSyntaxError("Macro '%s' was declared with %d parameters and used with %d parameter" % (
                 meta_name,
                 len(meta.args),
                 len(values)))
            filter_expressions = []
            for val in values:
                if val[0] == "'" or val[0] == '"':
                    if val[0] != val[(-1)]:
                        raise template.TemplateSyntaxError('Non-terminated string argument: %s' % val[1:])
                filter_expressions.append(FilterExpression(val, parser))

            return UseMetaNode(meta, filter_expressions, truncate)