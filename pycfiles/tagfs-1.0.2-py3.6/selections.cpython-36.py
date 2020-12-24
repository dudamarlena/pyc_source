# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tagfs/selections.py
# Compiled at: 2018-02-19 03:20:56
# Size of source mod 2**32: 2395 bytes
import ast
_OPS = {ast.Eq: '=', 
 ast.NotEq: '!=', 
 ast.Gt: '>', 
 ast.GtE: '>=', 
 ast.Lt: '<', 
 ast.LtE: '<=', 
 ast.Is: '=', 
 ast.IsNot: '!=', 
 ast.In: 'IN', 
 ast.NotIn: 'NI', 
 ast.And: 'AND', 
 ast.Or: 'OR', 
 ast.Not: '!'}
_NAMES = {'file':{'name':'files.name', 
  'path':'files.path', 
  'id':'files.id'}, 
 'tag':{'name':'tags.name', 
  'id':'tags.id'}}

def build(val):
    if isinstance(val, ast.BoolOp):
        return {'op':_OPS[type(val.op)],  'values':[build(i) for i in val.values]}
    else:
        if isinstance(val, ast.Compare):
            v = []
            p = val.left
            for op, val in zip(val.ops, val.comparators):
                op = type(op)
                if op is ast.In or op is ast.NotIn:
                    r = [build(i) for i in val.elts]
                else:
                    r = [
                     build(val)]
                v.append({'op':_OPS[op], 
                 'values':[
                  build(p)] + r})
                p = val

            if len(v) == 1:
                return v[0]
            else:
                return {'op':'AND', 
                 'values':v}
        else:
            if isinstance(val, ast.Attribute):
                return _NAMES[val.value.id][val.attr]
            if isinstance(val, ast.Str):
                return {'type':'str',  'value':val.s}
        if isinstance(val, ast.Num):
            return {'type':'number',  'value':val.n}
    raise ValueError('Unknown or invalid expression')


def compile_sel(v):
    if 'op' in v:
        op = v['op']
        if op == 'IN':
            a = compile_sel(v['values'][0])
            return '(%s)' % 'OR'.join('(%s=%s)' % (a, compile_sel(i)) for i in v['values'][1:])
        if op == 'NI':
            a = compile_sel(v['values'][0])
            return '(%s)' % 'AND'.join('(%s!=%s)' % (a, compile_sel(i)) for i in v['values'][1:])
        return '(%s)' % op.join(compile_sel(i) for i in v['values'])
    else:
        if 'type' in v:
            return repr(v['value'])
        return v


def compile_selection(sel: str):
    if sel.startswith('sel:'):
        sel = sel[4:]
    sel = compile(sel, '<selection>', 'eval', ast.PyCF_ONLY_AST, 1)
    if not isinstance(sel, ast.Expression):
        raise TypeError('Value must be expression')
    return compile_sel(build(sel.body))