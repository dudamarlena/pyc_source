# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/py2opencl/convert.py
# Compiled at: 2014-11-11 10:50:58
"""
convert simple Python lambda to OpenCL

currently relies upon 
"""
import ast, inspect
from . import ast2xml
import xml.etree.ElementTree as ET, re, numpy as np
USING_BEIGNET = False
npchar_to_typ = {'b': 'char', 'h': 'short', 
   'i': 'int', 
   'l': 'long', 
   'B': 'uchar', 
   'H': 'ushort', 
   'I': 'uint', 
   'L': 'ulong', 
   'e': 'half', 
   'f': 'float', 
   'd': 'double'}
typ_to_npchar = dict((v, k) for k, v in npchar_to_typ.items())
nptyp_to_cl = {np.dtype('float16'): 'half', np.dtype('float32'): 'float', 
   np.dtype('float64'): 'double', 
   np.dtype('uint8'): 'uchar', 
   np.dtype('int16'): 'short', 
   np.dtype('int32'): 'int', 
   np.dtype('int64'): 'long'}
cltyp_to_np = dict((v, k) for k, v in nptyp_to_cl.items())

def verify_apply(func, argtypes):
    """
    verify_apply( func, argtypes )

    verify that function accepts arg types given
    returns return-type of function
    """
    matching_ret = None
    for t in func.types:
        args, ret = t.split('->')
        assert len(argtypes) == len(args)
        for atyp, ch in zip(argtypes, args):
            if atyp is None:
                continue
            if npchar_to_typ.get(ch) == atyp:
                matching_ret = npchar_to_typ[ret]
                break

        if matching_ret:
            return matching_ret

    if set(argtypes) != set([None]):
        raise TypeError("unfunc %s didn't match provided types -- %s not found among types %s" % (
         func.__name__, argtypes, func.types))
    return


def special_funcs(modname, funcname, symbol_lookup, args):
    if not modname and funcname == 'int':
        return ('convert_int_rtz', 'int')
    else:
        if not modname and funcname == 'float':
            return ('convert_float', 'float')
        import importlib
        try:
            mod = importlib.import_module(modname)
        except ImportError:
            mod = importlib.import_module('.' + modname, package='py2opencl')

        try:
            func = mod.__getattribute__(funcname)
            argtypes = [ symbol_lookup(a)[1] for a, _ in args ]
            return (
             funcname, verify_apply(func, argtypes))
        except AttributeError:
            return (
             funcname, None)

        return


def conv_subscr(el, symbol_lookup, declarations):
    """
    special case: tuple subscripts (ie, x[i,j]) are 
    """
    sub, = el.findall('./value')
    name = sub.get('_name')
    if name == 'Name':
        return conv(sub, symbol_lookup, declarations)
    if name == 'Tuple':
        l = [ conv(x, symbol_lookup, declarations) for x in sub.findall('./elts/_list_element') ]
        args = (',').join(a for a, _ in l)
        if len(l) == 2:
            return ('FLATTEN2( %s )' % args, 'int')
        if len(l) == 3:
            return ('FLATTEN3( %s )' % args, 'int')
        raise ValueError("can't flatten %d arguments" % len(l))


def conv(el, symbol_lookup, declarations=None):
    """
    returns <openCL-C string representation>, <openCL type>
    """

    def is_float(s):
        if s.startswith('float'):
            return s
        raise ValueError('%s is not float' % s)

    def is_int(s):
        if s.startswith('int') or s.startswith('uint'):
            return s
        raise ValueError('%s is not int' % s)

    _conv = lambda el: conv(el, symbol_lookup, declarations)
    _conv_subscr = lambda el: conv_subscr(el, symbol_lookup, declarations)

    def cpow(left_el, right_el):
        (lval, ltyp), (rval, rtyp) = _conv(left_el), _conv(right_el)
        assert None in (ltyp, rtyp) or ltyp == rtyp, 'pow requires types match; got %s, %s' % (ltyp, rtyp)
        return ('pow( %s, %s )' % (lval, rval), ltyp or rtyp)

    def cnumeric(s):
        try:
            return (str(int(s)), symbol_lookup(s)[1])
        except ValueError:
            return (
             s, None)

        return

    def conv_cmp(s):
        try:
            return ({'Eq': '==', 'NotEq': '!=', 'Lt': '<', 'LtE': '<=', 'Gt': '>', 'GtE': '>='}[s], None)
        except KeyError:
            raise ValueError("comparitor not supported: '%s'" % str(s))

        return

    name = el.get('_name')
    if name == 'Name':
        iden = el.get('id')
        if iden == 'True' or iden == 'False':
            return (iden.lower(), 'bool')
        _, typ, nom = symbol_lookup(iden)
        return (
         nom, typ)
    else:
        if name == 'Num':
            return cnumeric(el.get('n'))
        if name == 'BoolOp':
            op, = el.findall('./op')
            operands = [ _conv(x)[0] for x in el.findall('./values/_list_element') ]
            return (
             '(%s)' % {'And': ' && ', 'Or': ' || '}[op.get('_name')].join(operands), 'bool')
        if name == 'UnaryOp':
            operand, = el.findall('./operand')
            operand, typ = _conv(operand)
            op, = el.findall('./op')
            return (
             {'Invert': '~' + operand, 'Not': '!' + operand, 
                'UAdd': operand, 
                'USub': '-' + operand}[op.get('_name')], typ)
        if name == 'BinOp':
            op, = el.findall('./op')
            right, = el.findall('./right')
            left, = el.findall('./left')
            if op.get('_name') == 'Pow':
                return cpow(left, right)
            cop = {'Add': '+', 'Sub': '-', 'Mult': '*', 'Div': '/', 'Mod': '%', 'LShift': '<<', 
               'RShift': '>>', 'BitOr': '|', 'BitXor': '^', 
               'BitAnd': '&', 'FloorDiv': '/'}[op.get('_name')]
            (lval, ltyp), (rval, rtyp) = _conv(left), _conv(right)
            typ = rtyp or ltyp
            return (
             '(%s %s %s)' % (lval, cop, rval), typ)
        if name == 'If':
            test, = el.findall('./test')
            body, = el.findall('./body')
            l = [ _conv(x) for x in body.findall('./_list_element') ]
            body = (';\n').join(a for a, b in l)
            ret = 'if( %s ) {\n%s\n}' % (_conv(test)[0], body)
            if el.findall('./orelse'):
                orelse, = el.findall('./orelse')
                l = [ _conv(x) for x in orelse.findall('./_list_element') ]
                orelse = (';\n').join(a for a, _ in l)
                ret += ' else { %s }' % orelse
            return (ret, None)
        if name == 'IfExp':
            test, = el.findall('./test')
            iftrue, = el.findall('./body')
            iffalse, = el.findall('./orelse')
            (lval, ltyp), (rval, rtyp) = _conv(iftrue), _conv(iffalse)
            typ = ltyp or rtyp
            return (
             '(%s ? %s : %s)' % (_conv(test)[0], lval, rval), typ)
        if name == 'Compare':
            ops, = el.findall('./ops')
            ops = [ conv_cmp(op.get('_name')) for op in ops.findall('./_list_element') ]
            left, = el.findall('./left')
            operands, = el.findall('./comparators')
            operands = [left] + sorted((item for item in operands.findall('_list_element')), key=lambda x: (
             int(x.get('lineno')), int(x.get('col_offset'))))
            operands = [ _conv(item) for item in operands ]
            assert len(operands) == len(ops) + 1
            l = []
            for i in range(len(operands) - 1):
                l.append('(%s %s %s)' % (operands[i][0], ops[i][0], operands[(i + 1)][0]))

            return ('(' + (' && ').join(l) + ')', 'bool')
        if name == 'Call':
            funcname, = el.findall('./func')
            module = funcname.findall('./value')
            if module:
                module, = module
                module = module.get('id')
            funcname = funcname.get('attr') or funcname.get('id')
            args = map(_conv, el.findall('./args/_list_element'))
            funcname, typ = special_funcs(module, funcname, symbol_lookup, args)
            if isinstance(funcname, basestring):
                return (
                 '%s( %s )' % (funcname, (', ').join(a for a, t in args)), typ)
            return (
             funcname((', ').join(a for a, t in args)), typ)
        if name == 'Assign':
            target, = el.findall('./targets/_list_element')
            target, ttyp = _conv(target)
            operand, = el.findall('./value')
            operand, otyp = _conv(operand)
            assert symbol_lookup
            target_name = re.match('(\\w+)\\[?', target).group(1)
            decl, styp, nom = symbol_lookup(target_name)
            typ = styp or ttyp or otyp
            if decl:
                declarations[target_name] = typ
            return (
             '%s = %s;' % (target, operand), typ)
        if name == 'Subscript':
            name, = el.findall('./value')
            subscr, = el.findall('./slice')
            val, typ = _conv(name)
            sval, styp = _conv_subscr(subscr)
            return (
             '%s[ %s ]' % (val, sval), typ)
        if name == 'Index':
            val, = el.findall('./value')
            return _conv(val)
        if name == 'Expr':
            return ('', None)
        return ('', None)


import xml.dom.minidom

def pprint(s):
    if not isinstance(s, basestring):
        s = ET.tostring(s)
    return xml.dom.minidom.parseString(s).toprettyxml()


def function_to_kernel(lmb, types, shape, bindings=None, return_type=None):
    """
    NOTE: method to convery python lambda to an OpenCL kernel; delegates conversion
    of proper function to `full_function_to_kernel`

    @types -- numpy types
    """
    src = ast.parse(inspect.getsource(lmb).lstrip())
    root = ET.fromstring(ast2xml.ast2xml().convert(src))
    if not root.findall(".//*[@_name='Lambda']"):
        return full_function_to_kernel(lmb, types, shape, bindings, return_type=return_type)
    else:
        func, = root.findall(".//*[@_name='Lambda']")
        args = func.findall('args/args/_list_element[@id]')
        argnames = [ a.get('id') for a in args ]
        assert argnames
        declarations = dict(zip(argnames, types)) if types else {}

        def symbol_lookup(s):
            target_name = None
            if s in declarations:
                return (True, nptyp_to_cl[declarations[s]], s + '[gid]')
            else:
                target_name = re.match('(\\w+)\\[?', s).group(1)
                if target_name != s:
                    return symbol_lookup(target_name)
                return (False, None, s)

        body, = func.findall('./body')
        kernel_body, result_typ = conv(body, symbol_lookup=symbol_lookup, declarations=declarations)
        numpy_typ = cltyp_to_np[result_typ]
        sigs = [ '__global const %s *%s' % (nptyp_to_cl[typ], aname) for typ, aname in zip(types, argnames) ] if types else [ '__global const float *%s' % aname for aname in argnames ]
        sigs.append('__global %s *res_g' % result_typ)
        sigs = (', ').join(sigs)
        kernel = '\n\nkernel void sum( %(sigs)s ) {\n  size_t gid = get_global_id(0);\n  res_g[gid] = %(body)s;\n}' % {'sigs': sigs, 'body': kernel_body}
        kernel = '\n#pragma OPENCL EXTENSION cl_khr_fp64 : enable\n\n\n' + kernel
        if bindings is None:
            kernel = '/* NOTE: without numpy bindings, some types might be incorrectly annotated as None */' + kernel
        return (argnames, kernel, result_typ)


def full_function_to_kernel(f, types, shape, bindings=None, return_type=None):
    src = ast.parse(inspect.getsource(f).lstrip())
    root = ET.fromstring(ast2xml.ast2xml().convert(src))
    func, = root.findall(".//*[@_name='FunctionDef']")
    argnames = [ x.get('id') for x in func.findall("./args[@_name='arguments']/args/_list_element[@_name='Name']")
               ]
    headers = ''
    assert len(argnames) > 1
    if len(shape) == 1:
        id_getters = 'size_t gid = get_global_id(0);'
        idx_names = {argnames.pop(0): 'gid'}
        results_name = argnames.pop(0)
    elif len(shape) == 2:
        id_getters = '\nsize_t gid_x = get_global_id(0);\nsize_t gid_y = get_global_id(1);\n'
        headers = '\n#define XDIM %d\n#define YDIM %d\n#define TOTSIZE (XDIM * YDIM)\n#define FLATTEN2( i, j ) (TOTSIZE + ((j * XDIM) + i)) %% TOTSIZE\n' % shape
        idx_names = {argnames.pop(0): 'gid_x', argnames.pop(0): 'gid_y'}
        results_name = argnames.pop(0)
    elif len(shape) == 3:
        id_getters = '\nsize_t gid_x = get_global_id(0);\nsize_t gid_y = get_global_id(1);\nsize_t gid_z = get_global_id(2);\n'
        headers = '\n#define XDIM %d\n#define YDIM %d\n#define ZDIM %d\n#define TOTSIZE (XDIM * YDIM * ZDIM)\n#define FLATTEN3( i, j, k ) ((TOTSIZE + (i * ZDIM) + (j * (XDIM * ZDIM)) + k) %% TOTSIZE)\n' % shape
        idx_names = {argnames.pop(0): 'gid_x', argnames.pop(0): 'gid_y', 
           argnames.pop(0): 'gid_z'}
        results_name = argnames.pop(0)
    argname_to_type = dict((nom, nptyp_to_cl[ntyp]) for nom, ntyp in zip(argnames, types)) if types else dict((a, None) for a in argnames)
    declarations = {}

    def symbol_lookup(s):
        if s in idx_names:
            return (False, None, idx_names[s])
        else:
            if s == results_name or s == 'res_g':
                return (True, return_type, 'res_g')
            if argname_to_type:
                if s in argname_to_type:
                    return (False, argname_to_type[s], s)
            if bindings:
                if s in bindings:
                    return (False, type(bindings[s]), str(bindings[s]))
            return (
             True, declarations.get(s), s)

    funcbod, = func.findall('./body')
    assignments = [ conv(el, symbol_lookup=symbol_lookup, declarations=declarations) for el in funcbod.getchildren() ]
    assignments = [ a for a, b in assignments ]
    body, = func.findall('./body')
    _, typ = conv(body, symbol_lookup=symbol_lookup, declarations=declarations)
    result_typ = declarations['res_g']
    del declarations['res_g']
    sigs = [ '__global const %s *%s' % (nptyp_to_cl[ntyp], aname) for ntyp, aname in zip(types, argnames) ] if types else [ '__global const float *%s' % aname for aname in argnames ]
    sigs.append('__global %s *res_g' % result_typ)
    input_sig = (', ').join(sigs)
    decl = ('\n').join('%s %s;' % (typ, nom) for nom, typ in declarations.items())
    kernel = headers + '\n\n__kernel void sum( %(sig)s ) {\n  %(getters)s\n  %(decl)s\n  %(body)s\n}' % {'getters': id_getters, 'decl': decl, 'sig': input_sig, 'body': ('\n  ').join(assignments)}
    kernel = '\n#pragma OPENCL EXTENSION cl_khr_fp64 : enable\n\n' + kernel
    if bindings is None:
        kernel = '/* NOTE: without numpy bindings, some types might be incorrectly annotated as None */' + kernel
    return (argnames, kernel, result_typ)