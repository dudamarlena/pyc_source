# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/qt/work/pyside/pyside-setup/pyside2_install/py2.7-qt5.14.2-64bit-release/lib/python2.7/site-packages/shiboken2/files.dir/shibokensupport/signature/parser.py
# Compiled at: 2020-03-30 06:40:47
from __future__ import print_function, absolute_import
import sys, re, warnings, types, keyword, functools
from shibokensupport.signature.mapping import type_map, update_mapping, namespace, typing, _NotCalled, ResultVariable, ArrayLikeVariable
from shibokensupport.signature.lib.tool import SimpleNamespace, build_brace_pattern
_DEBUG = False
LIST_KEYWORDS = False

def dprint(*args, **kw):
    if _DEBUG:
        import pprint
        for arg in args:
            pprint.pprint(arg)
            sys.stdout.flush()


_cache = {}

def _parse_arglist(argstr):
    key = '_parse_arglist'
    if key not in _cache:
        regex = build_brace_pattern(level=3, separators=',')
        _cache[key] = re.compile(regex, flags=re.VERBOSE)
    split = _cache[key].split
    return [ x.strip() for x in split(argstr) if x.strip() not in ('', ',') ]


def _parse_line(line):
    line_re = '\n        ((?P<multi> ([0-9]+)) : )?    # the optional multi-index\n        (?P<funcname> \\w+(\\.\\w+)*)    # the function name\n        \\( (?P<arglist> .*?) \\)       # the argument list\n        ( -> (?P<returntype> .*) )?   # the optional return type\n        $\n        '
    ret = SimpleNamespace(**re.match(line_re, line, re.VERBOSE).groupdict())
    argstr = ret.arglist.replace('->', '.deref.')
    arglist = _parse_arglist(argstr)
    args = []
    for arg in arglist:
        name, ann = arg.split(':')
        if name in keyword.kwlist:
            if LIST_KEYWORDS:
                print('KEYWORD', ret)
            name = name + '_'
        if '=' in ann:
            ann, default = ann.split('=', 1)
            tup = (name, ann, default)
        else:
            tup = (
             name, ann)
        args.append(tup)

    ret.arglist = args
    multi = ret.multi
    if multi is not None:
        ret.multi = int(multi)
    funcname = ret.funcname
    parts = funcname.split('.')
    if parts[(-1)] in keyword.kwlist:
        ret.funcname = funcname + '_'
    return vars(ret)


def make_good_value(thing, valtype):
    try:
        if thing.endswith('()'):
            thing = ('Default("{}")').format(thing[:-2])
        else:
            ret = eval(thing, namespace)
            if valtype and repr(ret).startswith('<'):
                thing = ('Instance("{}")').format(thing)
        return eval(thing, namespace)
    except Exception:
        pass


def try_to_guess(thing, valtype):
    if '.' not in thing and '(' not in thing:
        text = ('{}.{}').format(valtype, thing)
        ret = make_good_value(text, valtype)
        if ret is not None:
            return ret
    typewords = valtype.split('.')
    valwords = thing.split('.')
    braceless = valwords[0]
    if '(' in braceless:
        braceless = braceless[:braceless.index('(')]
    for idx, w in enumerate(typewords):
        if w == braceless:
            text = ('.').join(typewords[:idx] + valwords)
            ret = make_good_value(text, valtype)
            if ret is not None:
                return ret

    return


def _resolve_value(thing, valtype, line):
    if thing in ('0', 'None') and valtype:
        if valtype.startswith('PySide2.') or valtype.startswith('typing.'):
            return
        map = type_map[valtype]
        name = map.__name__ if hasattr(map, '__name__') else str(map)
        thing = ('zero({})').format(name)
    if thing in type_map:
        return type_map[thing]
    else:
        res = make_good_value(thing, valtype)
        if res is not None:
            type_map[thing] = res
            return res
        res = try_to_guess(thing, valtype) if valtype else None
        if res is not None:
            type_map[thing] = res
            return res
        warnings.warn(('pyside_type_init:\n\n        UNRECOGNIZED:   {!r}\n        OFFENDING LINE: {!r}\n        ').format(thing, line), RuntimeWarning)
        return thing


def _resolve_arraytype(thing, line):
    search = re.search('\\[(\\d*)\\]$', thing)
    thing = thing[:search.start()]
    if thing.endswith(']'):
        thing = _resolve_arraytype(thing, line)
    if search.group(1):
        nelem = int(search.group(1))
        thing = (', ').join([thing] * nelem)
        thing = 'Tuple[' + thing + ']'
    else:
        thing = 'QList[' + thing + ']'
    return thing


def to_string(thing):
    if isinstance(thing, str):
        return thing
    if hasattr(thing, '__name__'):
        dot = '.' in str(thing)
        if dot:
            return thing.__module__ + '.' + thing.__name__
        return thing.__name__
    return str(thing)


matrix_pattern = 'PySide2.QtGui.QGenericMatrix'

def handle_matrix(arg):
    n, m, typstr = tuple(map(lambda x: x.strip(), arg.split(',')))
    assert typstr == 'float'
    result = ('PySide2.QtGui.QMatrix{n}x{m}').format(**locals())
    return eval(result, namespace)


debugging_aid = '\nfrom inspect import currentframe\n\ndef lno(level):\n    lineno = currentframe().f_back.f_lineno\n    spaces = level * "  "\n    return "{lineno}{spaces}".format(**locals())\n'

def _resolve_type(thing, line, level, var_handler):
    if thing in type_map:
        return type_map[thing]
    else:
        if '[' in thing:
            if re.search('\\[\\d*\\]$', thing):
                thing = _resolve_arraytype(thing, line)
            contr, thing = re.match('(.*?)\\[(.*?)\\]$', thing).groups()
            if contr == matrix_pattern:
                return handle_matrix(thing)
            contr = var_handler(_resolve_type(contr, line, level + 1, var_handler))
            if isinstance(contr, _NotCalled):
                raise SystemError('Container types must exist:', repr(contr))
            contr = to_string(contr)
            pieces = []
            for part in _parse_arglist(thing):
                part = var_handler(_resolve_type(part, line, level + 1, var_handler))
                if isinstance(part, _NotCalled):
                    part = repr(part)
                pieces.append(to_string(part))

            thing = (', ').join(pieces)
            result = ('{contr}[{thing}]').format(**locals())
            return eval(result, namespace)
        return _resolve_value(thing, None, line)


def _handle_generic(obj, repl):
    """
    Assign repl if obj is an ArrayLikeVariable

    This is a neat trick. Example:

        obj                     repl        result
        ----------------------  --------    ---------
        ArrayLikeVariable       List        List
        ArrayLikeVariable(str)  List        List[str]
        ArrayLikeVariable       Sequence    Sequence
        ArrayLikeVariable(str)  Sequence    Sequence[str]
    """
    if isinstance(obj, ArrayLikeVariable):
        return repl[obj.type]
    if isinstance(obj, type) and issubclass(obj, ArrayLikeVariable):
        return repl
    return obj


def handle_argvar(obj):
    """
    Decide how array-like variables are resolved in arguments

    Currently, the best approximation is types.Sequence.
    We want to change that to types.Iterable in the near future.
    """
    return _handle_generic(obj, typing.Sequence)


def handle_retvar(obj):
    """
    Decide how array-like variables are resolved in results

    This will probably stay typing.List forever.
    """
    return _handle_generic(obj, typing.List)


def calculate_props(line):
    parsed = SimpleNamespace(**_parse_line(line.strip()))
    arglist = parsed.arglist
    annotations = {}
    _defaults = []
    for idx, tup in enumerate(arglist):
        name, ann = tup[:2]
        if ann == '...':
            name = '*args' if name.startswith('arg_') else '*' + name
            ann = 'nullptr'
            tup = (name, ann)
            arglist[idx] = tup
        annotations[name] = _resolve_type(ann, line, 0, handle_argvar)
        if len(tup) == 3:
            default = _resolve_value(tup[2], ann, line)
            _defaults.append(default)

    defaults = tuple(_defaults)
    returntype = parsed.returntype
    if returntype is not None:
        annotations['return'] = _resolve_type(returntype, line, 0, handle_retvar)
    props = SimpleNamespace()
    props.defaults = defaults
    props.kwdefaults = {}
    props.annotations = annotations
    props.varnames = varnames = tuple(tup[0] for tup in arglist)
    funcname = parsed.funcname
    props.fullname = funcname
    shortname = funcname[funcname.rindex('.') + 1:]
    props.name = shortname
    props.multi = parsed.multi
    fix_variables(props, line)
    return vars(props)


def fix_variables(props, line):
    annos = props.annotations
    if not any(isinstance(ann, (ResultVariable, ArrayLikeVariable)) for ann in annos.values()):
        return
    else:
        retvar = annos.get('return', None)
        if retvar and isinstance(retvar, (ResultVariable, ArrayLikeVariable)):
            annos['return'] = retvar = typing.List[retvar.type]
        fullname = props.fullname
        varnames = list(props.varnames)
        defaults = list(props.defaults)
        diff = len(varnames) - len(defaults)
        safe_annos = annos.copy()
        retvars = [retvar] if retvar else []
        deletions = []
        for idx, name in enumerate(varnames):
            ann = safe_annos[name]
            if isinstance(ann, ArrayLikeVariable):
                ann = typing.Sequence[ann.type]
                annos[name] = ann
            if not isinstance(ann, ResultVariable):
                continue
            retvars.append(ann.type)
            deletions.append(idx)
            del annos[name]

        for idx in reversed(deletions):
            del varnames[idx]
            if idx >= diff:
                del defaults[idx - diff]
            else:
                diff -= 1

        if retvars:
            rvs = []
            retvars = list((handle_retvar(rv) if isinstance(rv, ArrayLikeVariable) else rv) for rv in retvars)
            if len(retvars) == 1:
                returntype = retvars[0]
            else:
                typestr = ('typing.Tuple[{}]').format((', ').join(map(to_string, retvars)))
                returntype = eval(typestr, namespace)
            props.annotations['return'] = returntype
        props.varnames = tuple(varnames)
        props.defaults = tuple(defaults)
        return


def fixup_multilines(lines):
    """
    Multilines can collapse when certain distinctions between C++ types
    vanish after mapping to Python.
    This function fixes this by re-computing multiline-ness.
    """
    res = []
    multi_lines = []
    for line in lines:
        multi = re.match('([0-9]+):', line)
        if multi:
            idx, rest = int(multi.group(1)), line[multi.end():]
            multi_lines.append(rest)
            if idx > 0:
                continue
            multi_lines = sorted(set(multi_lines))
            nmulti = len(multi_lines)
            if nmulti > 1:
                for idx, line in enumerate(multi_lines):
                    res.append(('{}:{}').format(nmulti - idx - 1, line))

            else:
                res.append(multi_lines[0])
            multi_lines = []
        else:
            res.append(line)

    return res


def pyside_type_init(type_key, sig_strings):
    dprint()
    dprint(("Initialization of type key '{}'").format(type_key))
    update_mapping()
    lines = fixup_multilines(sig_strings)
    ret = {}
    multi_props = []
    for line in lines:
        props = calculate_props(line)
        shortname = props['name']
        multi = props['multi']
        if multi is None:
            ret[shortname] = props
            dprint(props)
        else:
            multi_props.append(props)
            if multi > 0:
                continue
            fullname = props.pop('fullname')
            multi_props = {'multi': multi_props, 'fullname': fullname}
            ret[shortname] = multi_props
            dprint(multi_props)
            multi_props = []

    return ret