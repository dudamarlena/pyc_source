# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/coverage/coverage/templite.py
# Compiled at: 2019-07-30 18:47:10
# Size of source mod 2**32: 6868 bytes
"""A simple Python template renderer, for a nano-subset of Django syntax."""
import re
from coverage.backward import set

class CodeBuilder(object):
    __doc__ = 'Build source code conveniently.'

    def __init__(self, indent=0):
        self.code = []
        self.indent_amount = indent

    def add_line(self, line):
        """Add a line of source to the code.

        Don't include indentations or newlines.

        """
        self.code.append(' ' * self.indent_amount)
        self.code.append(line)
        self.code.append('\n')

    def add_section(self):
        """Add a section, a sub-CodeBuilder."""
        sect = CodeBuilder(self.indent_amount)
        self.code.append(sect)
        return sect

    def indent(self):
        """Increase the current indent for following lines."""
        self.indent_amount += 4

    def dedent(self):
        """Decrease the current indent for following lines."""
        self.indent_amount -= 4

    def __str__(self):
        return ''.join([str(c) for c in self.code])

    def get_function(self, fn_name):
        """Compile the code, and return the function `fn_name`."""
        assert self.indent_amount == 0
        g = {}
        code_text = str(self)
        exec(code_text, g)
        return g[fn_name]


class Templite(object):
    __doc__ = 'A simple template renderer, for a nano-subset of Django syntax.\n\n    Supported constructs are extended variable access::\n\n        {{var.modifer.modifier|filter|filter}}\n\n    loops::\n\n        {% for var in list %}...{% endfor %}\n\n    and ifs::\n\n        {% if var %}...{% endif %}\n\n    Comments are within curly-hash markers::\n\n        {# This will be ignored #}\n\n    Construct a Templite with the template text, then use `render` against a\n    dictionary context to create a finished string.\n\n    '

    def __init__(self, text, *contexts):
        """Construct a Templite with the given `text`.

        `contexts` are dictionaries of values to use for future renderings.
        These are good for filters and global values.

        """
        self.text = text
        self.context = {}
        for context in contexts:
            self.context.update(context)

        code = CodeBuilder()
        code.add_line('def render(ctx, dot):')
        code.indent()
        vars_code = code.add_section()
        self.all_vars = set()
        self.loop_vars = set()
        code.add_line('result = []')
        code.add_line('a = result.append')
        code.add_line('e = result.extend')
        code.add_line('s = str')
        buffered = []

        def flush_output():
            if len(buffered) == 1:
                code.add_line('a(%s)' % buffered[0])
            else:
                if len(buffered) > 1:
                    code.add_line('e([%s])' % ','.join(buffered))
            del buffered[:]

        toks = re.split('(?s)({{.*?}}|{%.*?%}|{#.*?#})', text)
        ops_stack = []
        for tok in toks:
            if tok.startswith('{{'):
                buffered.append('s(%s)' % self.expr_code(tok[2:-2].strip()))
            else:
                if tok.startswith('{#'):
                    continue
                else:
                    if tok.startswith('{%'):
                        flush_output()
                        words = tok[2:-2].strip().split()
                        if words[0] == 'if':
                            assert len(words) == 2
                            ops_stack.append('if')
                            code.add_line('if %s:' % self.expr_code(words[1]))
                            code.indent()
                        else:
                            if words[0] == 'for':
                                assert len(words) == 4 and words[2] == 'in'
                                ops_stack.append('for')
                                self.loop_vars.add(words[1])
                                code.add_line('for c_%s in %s:' % (
                                 words[1],
                                 self.expr_code(words[3])))
                                code.indent()
                            else:
                                if words[0].startswith('end'):
                                    end_what = words[0][3:]
                                    if ops_stack[(-1)] != end_what:
                                        raise SyntaxError('Mismatched end tag: %r' % end_what)
                                    ops_stack.pop()
                                    code.dedent()
                                else:
                                    raise SyntaxError("Don't understand tag: %r" % words[0])
                    else:
                        if tok:
                            buffered.append('%r' % tok)

        flush_output()
        for var_name in self.all_vars - self.loop_vars:
            vars_code.add_line('c_%s = ctx[%r]' % (var_name, var_name))

        if ops_stack:
            raise SyntaxError('Unmatched action tag: %r' % ops_stack[(-1)])
        code.add_line("return ''.join(result)")
        code.dedent()
        self.render_function = code.get_function('render')

    def expr_code(self, expr):
        """Generate a Python expression for `expr`."""
        if '|' in expr:
            pipes = expr.split('|')
            code = self.expr_code(pipes[0])
            for func in pipes[1:]:
                self.all_vars.add(func)
                code = 'c_%s(%s)' % (func, code)

        else:
            if '.' in expr:
                dots = expr.split('.')
                code = self.expr_code(dots[0])
                args = [repr(d) for d in dots[1:]]
                code = 'dot(%s, %s)' % (code, ', '.join(args))
            else:
                self.all_vars.add(expr)
                code = 'c_%s' % expr
        return code

    def render(self, context=None):
        """Render this template by applying it to `context`.

        `context` is a dictionary of values to use in this rendering.

        """
        ctx = dict(self.context)
        if context:
            ctx.update(context)
        return self.render_function(ctx, self.do_dots)

    def do_dots(self, value, *dots):
        """Evaluate dotted expressions at runtime."""
        for dot in dots:
            try:
                value = getattr(value, dot)
            except AttributeError:
                value = value[dot]

            if hasattr(value, '__call__'):
                value = value()

        return value