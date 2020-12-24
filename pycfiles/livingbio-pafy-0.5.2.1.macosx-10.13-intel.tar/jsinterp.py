# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/davidchen/repos/django-video-composer/venv/lib/python2.7/site-packages/pafy/jsinterp.py
# Compiled at: 2017-12-12 20:44:10
from __future__ import unicode_literals
import json, operator, re, sys, traceback

class ExtractorError(Exception):
    """Error during info extraction."""

    def __init__(self, msg, tb=None, expected=False, cause=None, video_id=None):
        """ tb, if given, is the original traceback (so that it can be printed out).
        If expected is set, this is a normal error message and most likely not a bug in youtube-dl.
        """
        if video_id is not None:
            msg = video_id + b': ' + msg
        if cause:
            msg += b' (caused by %r)' % cause
        super(ExtractorError, self).__init__(msg)
        self.traceback = tb
        self.exc_info = sys.exc_info()
        self.cause = cause
        self.video_id = video_id
        return

    def format_traceback(self):
        if self.traceback is None:
            return
        else:
            return (b'').join(traceback.format_tb(self.traceback))


_OPERATORS = [
 (
  b'|', operator.or_),
 (
  b'^', operator.xor),
 (
  b'&', operator.and_),
 (
  b'>>', operator.rshift),
 (
  b'<<', operator.lshift),
 (
  b'-', operator.sub),
 (
  b'+', operator.add),
 (
  b'%', operator.mod),
 (
  b'/', operator.truediv),
 (
  b'*', operator.mul)]
_ASSIGN_OPERATORS = [ (op + b'=', opfunc) for op, opfunc in _OPERATORS ]
_ASSIGN_OPERATORS.append((b'=', lambda cur, right: right))
_NAME_RE = b'[a-zA-Z_$][a-zA-Z_$0-9]*'

class JSInterpreter(object):

    def __init__(self, code, objects=None):
        if objects is None:
            objects = {}
        self.code = code
        self._functions = {}
        self._objects = objects
        return

    def interpret_statement(self, stmt, local_vars, allow_recursion=100):
        if allow_recursion < 0:
            raise ExtractorError(b'Recursion limit reached')
        should_abort = False
        stmt = stmt.lstrip()
        stmt_m = re.match(b'var\\s', stmt)
        if stmt_m:
            expr = stmt[len(stmt_m.group(0)):]
        else:
            return_m = re.match(b'return(?:\\s+|$)', stmt)
            if return_m:
                expr = stmt[len(return_m.group(0)):]
                should_abort = True
            else:
                expr = stmt
        v = self.interpret_expression(expr, local_vars, allow_recursion)
        return (v, should_abort)

    def interpret_expression(self, expr, local_vars, allow_recursion):
        expr = expr.strip()
        if expr == b'':
            return
        else:
            if expr.startswith(b'('):
                parens_count = 0
                for m in re.finditer(b'[()]', expr):
                    if m.group(0) == b'(':
                        parens_count += 1
                    else:
                        parens_count -= 1
                        if parens_count == 0:
                            sub_expr = expr[1:m.start()]
                            sub_result = self.interpret_expression(sub_expr, local_vars, allow_recursion)
                            remaining_expr = expr[m.end():].strip()
                            if not remaining_expr:
                                return sub_result
                            expr = json.dumps(sub_result) + remaining_expr
                            break
                else:
                    raise ExtractorError(b'Premature end of parens in %r' % expr)

            for op, opfunc in _ASSIGN_OPERATORS:
                m = re.match(b'(?x)\n                (?P<out>%s)(?:\\[(?P<index>[^\\]]+?)\\])?\n                \\s*%s\n                (?P<expr>.*)$' % (_NAME_RE, re.escape(op)), expr)
                if not m:
                    continue
                right_val = self.interpret_expression(m.group(b'expr'), local_vars, allow_recursion - 1)
                if m.groupdict().get(b'index'):
                    lvar = local_vars[m.group(b'out')]
                    idx = self.interpret_expression(m.group(b'index'), local_vars, allow_recursion)
                    assert isinstance(idx, int)
                    cur = lvar[idx]
                    val = opfunc(cur, right_val)
                    lvar[idx] = val
                    return val
                cur = local_vars.get(m.group(b'out'))
                val = opfunc(cur, right_val)
                local_vars[m.group(b'out')] = val
                return val

            if expr.isdigit():
                return int(expr)
            var_m = re.match(b'(?!if|return|true|false)(?P<name>%s)$' % _NAME_RE, expr)
            if var_m:
                return local_vars[var_m.group(b'name')]
            try:
                return json.loads(expr)
            except ValueError:
                pass

            m = re.match(b'(?P<var>%s)\\.(?P<member>[^(]+)(?:\\(+(?P<args>[^()]*)\\))?$' % _NAME_RE, expr)
            if m:
                variable = m.group(b'var')
                member = m.group(b'member')
                arg_str = m.group(b'args')
                if variable in local_vars:
                    obj = local_vars[variable]
                else:
                    if variable not in self._objects:
                        self._objects[variable] = self.extract_object(variable)
                    obj = self._objects[variable]
                if arg_str is None:
                    if member == b'length':
                        return len(obj)
                    return obj[member]
                assert expr.endswith(b')')
                if arg_str == b'':
                    argvals = tuple()
                else:
                    argvals = tuple([ self.interpret_expression(v, local_vars, allow_recursion) for v in arg_str.split(b',')
                                    ])
                if member == b'split':
                    assert argvals == ('', )
                    return list(obj)
                if member == b'join':
                    assert len(argvals) == 1
                    return argvals[0].join(obj)
                if member == b'reverse':
                    assert len(argvals) == 0
                    obj.reverse()
                    return obj
                if member == b'slice':
                    assert len(argvals) == 1
                    return obj[argvals[0]:]
                if member == b'splice':
                    assert isinstance(obj, list)
                    index, howMany = argvals
                    res = []
                    for i in range(index, min(index + howMany, len(obj))):
                        res.append(obj.pop(index))

                    return res
                return obj[member](argvals)
            m = re.match(b'(?P<in>%s)\\[(?P<idx>.+)\\]$' % _NAME_RE, expr)
            if m:
                val = local_vars[m.group(b'in')]
                idx = self.interpret_expression(m.group(b'idx'), local_vars, allow_recursion - 1)
                return val[idx]
            for op, opfunc in _OPERATORS:
                m = re.match(b'(?P<x>.+?)%s(?P<y>.+)' % re.escape(op), expr)
                if not m:
                    continue
                x, abort = self.interpret_statement(m.group(b'x'), local_vars, allow_recursion - 1)
                if abort:
                    raise ExtractorError(b'Premature left-side return of %s in %r' % (op, expr))
                y, abort = self.interpret_statement(m.group(b'y'), local_vars, allow_recursion - 1)
                if abort:
                    raise ExtractorError(b'Premature right-side return of %s in %r' % (op, expr))
                return opfunc(x, y)

            m = re.match(b'^(?P<func>%s)\\((?P<args>[a-zA-Z0-9_$,]+)\\)$' % _NAME_RE, expr)
            if m:
                fname = m.group(b'func')
                argvals = tuple([ int(v) if v.isdigit() else local_vars[v] for v in m.group(b'args').split(b',')
                                ])
                if fname not in self._functions:
                    self._functions[fname] = self.extract_function(fname)
                return self._functions[fname](argvals)
            raise ExtractorError(b'Unsupported JS expression %r' % expr)
            return

    def extract_object(self, objname):
        obj = {}
        obj_m = re.search(b'(?:var\\s+)?%s\\s*=\\s*\\{' % re.escape(objname) + b'\\s*(?P<fields>([a-zA-Z$0-9]+\\s*:\\s*function\\(.*?\\)\\s*\\{.*?\\}(?:,\\s*)?)*)' + b'\\}\\s*;', self.code)
        fields = obj_m.group(b'fields')
        fields_m = re.finditer(b'(?P<key>[a-zA-Z$0-9]+)\\s*:\\s*function\\((?P<args>[a-z,]+)\\){(?P<code>[^}]+)}', fields)
        for f in fields_m:
            argnames = f.group(b'args').split(b',')
            obj[f.group(b'key')] = self.build_function(argnames, f.group(b'code'))

        return obj

    def extract_function(self, funcname):
        func_m = re.search(b'(?x)\n                (?:function\\s+%s|[{;,]\\s*%s\\s*=\\s*function|var\\s+%s\\s*=\\s*function)\\s*\n                \\((?P<args>[^)]*)\\)\\s*\n                \\{(?P<code>[^}]+)\\}' % (
         re.escape(funcname), re.escape(funcname), re.escape(funcname)), self.code)
        if func_m is None:
            raise ExtractorError(b'Could not find JS function %r' % funcname)
        argnames = func_m.group(b'args').split(b',')
        return self.build_function(argnames, func_m.group(b'code'))

    def call_function(self, funcname, *args):
        f = self.extract_function(funcname)
        return f(args)

    def build_function(self, argnames, code):

        def resf(args):
            local_vars = dict(zip(argnames, args))
            for stmt in code.split(b';'):
                res, abort = self.interpret_statement(stmt, local_vars)
                if abort:
                    break

            return res

        return resf