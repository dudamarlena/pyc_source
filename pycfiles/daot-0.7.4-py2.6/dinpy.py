# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dao\dinpy\dinpy.py
# Compiled at: 2011-11-10 02:08:10
"""dao grammar embeded in python list display by operator grammar"""
__all__ = [
 'dinpy', 'preparse', 'eval', 'solve',
 '_', 'v', 'var', 'put',
 'iff', 'let', 'letr', 'case', 'els', 'on', 'block', 'label',
 'do', 'loop', 'each', 'when', 'exit', 'next',
 'catch', 'throw', 'protect',
 'fun', 'macro', 'at']
from dao.pysyntax import *
from dao.dinpy import dexpr
from dao.dinpy.dexpr import _VarSymbol, _DummyVarSymbol
from dao.term import Var, DummyVar, CommandCall, conslist as L, vars, dummies
from dao import builtin
from dao import special
from dao.special import set as assign
from dao.builtins.matcher import some, any, may
from dao.builtins.terminal import eoi
from dao.builtins.container import pytuple, head_list, list_tail, items, first, left
from dao.builtins.term import pycall, py_apply
from dao.builtins.term import getvalue, getvalue_default, is_
from dao.builtins.arith import ne_p
from dao.solve import eval as dao_eval, solve, tag_loop_label, to_sexpression
from dao.solve import set_run_mode, noninteractive, DaoUncaughtThrow
from dao.solve import interactive_parser, interactive_tagger, interactive_solver

def eval(code):
    code = preparse(code)
    code = tag_loop_label(code)
    return dao_eval(code)


class DaoCodeFormater:

    def __init__(self, indent_width=2):
        self.indent = 0
        self.indent_width = indent_width
        self.text = ''
        self.row = 0
        self.column = 0

    def indent(self):
        self.indent += self.indent_width

    def unindent(self):
        self.indent -= self.indent_width

    def pprint(self, code):
        try:
            code____pprint___ = code.___pprint___
        except:
            if isinstance(code, list) or isinstance(code, tuple):
                for x in code:
                    self.text += self.pprint(x)

            else:
                self.text += repr(code)

        code____pprint___(self)


class Dinpy(object):

    def __init__(self):
        self.code = []

    def __setattr__(self, attr, value):
        if attr == 'version':
            self._version = tuple(int(x) for x in value.split('.'))
            self.code = []
            return self
        else:
            return object.__setattr__(self, attr, value)

    def __getitem__(self, code):
        set_run_mode(noninteractive)
        if isinstance(code, tuple):
            self.code += list(code)
        else:
            self.code += [code]
        return self

    def preprocess(self):
        return special.begin(*tag_loop_label(preparse(self.code)))

    def solve(self):
        result = solve(self.preprocess())
        self.code = []
        return result

    def eval(self):
        result = dao_eval(self.preprocess())
        self.code = []
        return result

    def pprint(self, formater=None):
        if formater is None:
            formater = DaoCodeFormater()
        formater.text += 'dao.version = %s' % self.version
        return formater.pprint(self.code)


dinpy = Dinpy()

def solve(exp):
    code = interactive_parser().parse(exp)
    code = interactive_tagger().tag_loop_label(code)
    code = to_sexpression(code)
    return interactive_solver().solve(code)


def my_single_var(name, klass):

    class VForm(object):

        def __init__(self, name=name, grammar=None):
            self.__form_name__ = 'v'
            self.__form_grammar__ = None
            return

        def __getattr__(self, var):
            return my_varcache(var, klass)

    return lead(VForm)


_my_varcache = {}

def my_varcache(name, klass=Var):
    return _my_varcache.setdefault(klass, {}).setdefault(name, klass(name))


def _vars(text):
    return [ _my_varcache(x.strip()) for x in text.split(',') ]


vv = my_single_var('vv', Var)
__ = my_single_var('__', DummyVar)

def single_symbol(name, klass):

    class VForm(object):

        def __init__(self, name=name, grammar=None):
            self.__form_name__ = 'v'
            self.__form_grammar__ = None
            return

        def __getattr__(self, name):
            return klass(name)

    return lead(VForm)


from dao.dinpy.dexpr import varcache
v = single_symbol('v', _VarSymbol)
_ = single_symbol('_', _DummyVarSymbol)

class SymbolForm(object):

    def __init__(self, name=None, grammar=None):
        self.__form_name__ = 'var'
        self.__form_grammar__ = None
        self.__symbols__ = []
        return

    def __getattr__(self, name):
        self.__symbols__.append(_VarSymbol(name))
        return self

    def __len__(self):
        return len(self.__symbols__)

    def __iter__(self):
        return iter(self.__symbols__)


var = lead(SymbolForm)

@builtin.function('getvar')
def getvar(name, klass=Var):
    return varcache(name, klass)


put = element('put', (getattr(__._) + assign(vv.x, getvar(__._)))[1:] % vv.x * vv.vars + lshift(vv.value) + eoi + pycall(special.set_list, vv.vars, pycall(preparse, vv.value)))

@builtin.function('make_begin')
def make_begin(body):
    return special.begin(*preparse(body))


do = element('do', getitem_to_list(vv.body) + eoi + make_begin(vv.body))
(_do, _of, _at, _loop, _always) = words('do, of, at, loop, always')

def get_let_vars(binary, klass):
    if not isinstance(binary.y, _VarSymbol):
        raise DinpySyntaxError()
    if isinstance(binary.x, _VarSymbol):
        return (binary.x, binary.y)
    if isinstance(binary.x, klass):
        return get_let_vars(binary.x, klass) + (binary.y,)
    raise DinpySyntaxError()


@builtin.function('make_let')
def make_let(args, body, function):
    bindings = []
    for b in args:
        if not isinstance(b, dexpr._lshift):
            raise DinpySyntaxError()
        vars, value = b.x, preparse(b.y)
        if isinstance(vars, _VarSymbol):
            bindings.append((preparse(vars), value))
        elif isinstance(vars, dexpr._lshift):
            vars = get_let_vars(vars, dexpr._lshift)
            i = len(vars) - 1
            v2 = varcache(vars[i].name)
            bindings.append((v2, value))
            while i > 0:
                v1 = varcache(vars[(i - 1)].name)
                bindings.append((v1, v2))
                v2 = v1
                i -= 1

        elif isinstance(vars, dexpr._div):
            bindings += [ (varcache(v.name), value) for (v, value) in zip(get_let_vars(vars, dexpr._div), value)
                        ]
        else:
            raise DinpySyntaxError()

    body = preparse(body)
    if isinstance(body, tuple):
        return function(bindings, *body)
    else:
        return function(bindings, body)


def let_grammar(function):
    return call(vv.bindings) + _do + getitem(vv.body) + eoi + make_let(vv.bindings, vv.body, function)


let = element('let', let_grammar(special.let))
letr = element('letr', let_grammar(special.letr))

@builtin.function('make_iff')
def make_iff(test, clause, clauses, els_clause):
    els_clause = preparse(els_clause) if not isinstance(els_clause, Var) else None
    test = preparse(test[0])
    clause = preparse(clause)
    clauses1 = [ (preparse(t), preparse(c)) for (t, c) in clauses ]
    return special.iff([(test, clause)] + clauses1, els_clause)


(_then, _elsif, _els) = words('then, elsif, els')
(_test, _test2, _body) = dummies('_test, _test2, _body')
iff = element('iff', call(vv.test) + _do + getitem(vv.clause) + any(_elsif + call(_test) + _do + getitem(_body) + is_(_test2, first(_test)), (_test2, _body), vv.clauses) + may(_els + getitem(vv.els_clause)) + eoi + make_iff(vv.test, vv.clause, vv.clauses, vv.els_clause))

class CASE_ELS:
    pass


CASE_ELS = CASE_ELS()

@builtin.function('make_case')
def make_case(test, cases):
    case_dict = {}
    for (case, clause) in cases:
        case = preparse(case)
        if case is CASE_ELS:
            els_clause = preparse(clause) if clause is not None else None
        else:
            clause = preparse(clause)
            for x in case:
                case_dict[x] = clause

    return special.CaseForm(preparse(test[0]), case_dict, els_clause)


of_fun = attr_call('of')
case = element('case', call(vv.test) + (some(of_fun(__.values) + getitem_to_list(__.clause), (__.values, __.clause), vv.clauses) + may(_els + getitem_to_list(vv.els)) + eoi + make_case(vv.test, list_tail(vv.clauses, pytuple(CASE_ELS, getvalue_default(vv.els))))))
els = CASE_ELS

@builtin.function('make_loop')
def make_loop(body):
    return special.LoopForm(preparse(body))


@builtin.function('make_loop_times')
def make_loop_times(body, times):
    return special.LoopTimesForm(preparse(times[0]), preparse(body))


@builtin.function('make_loop_when')
def make_loop_when(body, test):
    return special.LoopWhenForm(preparse(body), preparse(test[0]))


@builtin.function('make_loop_until')
def make_loop_until(body, test):
    return special.LoopUntilForm(preparse(body), preparse(test[0]))


when_fun = attr_call('when')
until_fun = attr_call('until')
loop = element('loop', call(vv.times) + getitem_to_list(vv.body) + eoi + make_loop_times(vv.body, getvalue_default(vv.times)) | getitem_to_list(vv.body) + (eoi + make_loop(vv.body) | (when_fun(vv.test) + eoi + make_loop_when(vv.body, vv.test) | until_fun(vv.test) + eoi + make_loop_until(vv.body, vv.test))))

@builtin.function('make_when_loop')
def make_when_loop(test, body):
    return special.WhenLoopForm(preparse(test[0]), preparse(body))


when = element('when', call(vv.test) + _loop + getitem_to_list(vv.body) + eoi + make_when_loop(vv.test, vv.body))

@builtin.function('make_each1')
def make_each(vars, iterators, body):

    def tran_iterator(iterator):
        if isinstance(iterator, slice):
            start = preparse(iterator.start)
            stop = preparse(iterator.stop)
            step = preparse(iterator.step)
            iterator = range(start, stop, 1 if step is None else step)
        else:
            iterator = preparse(iterator)
        return iterator

    if len(vars) == 0:
        raise DinpySyntaxError()
    for x in vars:
        if not isinstance(x, _VarSymbol):
            raise DinpySyntaxError()

    vars = preparse(vars)
    if len(vars) == 1:
        if len(iterators) != 1:
            raise DinpySyntaxError()
        if not isinstance(iterators[0], slice) and len(iterators[0]) != 1:
            raise DinpySyntaxError()
        iterator = tran_iterator(iterators[0])
        return special.EachForm(vars[0], iterator, preparse(body))
    else:
        if len(iterators) == 1:
            return special.EachForm(vars, iterators[0], preparse(body))
        else:
            iterators1 = []
            for iterator in iterators:
                if isinstance(iterator, slice):
                    start = preparse(iterator.start)
                    stop = preparse(iterator.stop)
                    step = preparse(iterator.step)
                    iterators1.append(range(start, stop, 1 if step is None else step))
                else:
                    iterators1.append(preparse(iterator))

            return special.EachForm(vars, zip(*iterators1), preparse(body))
        return


each = element('each', call(vv.vars) + some(getitem(__.iterator), __.iterator, vv.iterators) + _loop + getitem_to_list(vv.body) + eoi + make_each(vv.vars, vv.iterators, vv.body))

@builtin.function('make_exit')
def make_exit(type, level, label, value):
    type = None if isinstance(type, Var) else type
    level = 0 if isinstance(level, Var) else level
    label = None if isinstance(label, Var) else label
    return special.exit(preparse(value), type, level, label)


exit = element('exit', (may(div(vv.type)) + may(mul(vv.level)) | may(getattr(vv.label))) + may(rshift(vv.value)) + eoi + make_exit(vv.type, vv.level, vv.label, getvalue_default(vv.value)))

@builtin.function('make_next')
def make_next(type, level, label):
    type = None if isinstance(type, Var) else type
    level = 0 if isinstance(level, Var) else level
    label = None if isinstance(label, Var) else label
    return special.next(type, level, label)


next = element('next', (may(div(vv.type)) + may(mul(vv.level)) | may(getattr(vv.label))) + eoi + make_next(vv.type, vv.level, vv.label))

@builtin.function('set_loop_label')
def set_loop_label(label, body):
    body = preparse(body)
    if not isinstance(body, special.RepeatForm):
        raise DinpySyntaxError()
    body.label = label
    return body


label = element('label', getattr(vv.name) + mod(vv.body) + eoi + set_loop_label(vv.name, vv.body))

@builtin.function('make_block')
def make_block(name, body):
    body = tuple(preparse(x) for x in body)
    return special.block(name, *body)


block = element('block', getattr(vv.name) + getitem_to_list(vv.body) + eoi + make_block(vv.name, vv.body))

@builtin.function('make_catch')
def make_catch(tag, body):
    if len(tag) != 1:
        raise DinpySyntaxError()
    return special.catch(preparse(tag[0]), *preparse(body))


catch = element('catch', call(vv.tag) + _do + getitem_to_list(vv.body) + eoi + make_catch(vv.tag, vv.body))

@builtin.function('make_throw')
def make_throw(tag, form):
    if len(tag) != 1:
        raise DinpySyntaxError()
    if len(form) != 1:
        form = special.begin(*preparse(form))
    else:
        form = preparse(form[0])
    return special.throw(preparse(tag[0]), form)


throw = element('throw', call(vv.tag) + _do + getitem_to_list(vv.form) + eoi + make_throw(vv.tag, vv.form))

@builtin.function('make_protect')
def make_protect(form, cleanup):
    if len(form) != 1:
        form = special.begin(*preparse(form))
    else:
        form = preparse(form[0])
    return special.unwind_protect(form, *preparse(cleanup))


protect = element('protect', getitem_to_list(vv.form) + _always + getitem_to_list(vv.cleanup) + eoi + make_protect(vv.form, vv.cleanup))

@builtin.function('make_pycall')
def make_pycall(args):
    args = tuple(preparse(x) for x in args)
    return pycall(args[0], args[1:])


py = element('py', getattr(vv.func) + assign(vv.func, getvar(vv.func)) + eoi + pycall(vv.func, vv.args) | ~call(vv.args) + eoi + make_pycall(vv.args))

@builtin.function('make_on_form')
def make_on_form(form, body):
    form = preparse(form)
    body = tuple(preparse(x) for x in body)
    return special.OnForm(form, *body)


on = element('on', call(vv.form) + _do + getitem(vv.body) + eoi + pycall(special.OnForm, vv.form, vv.body))

class AtForm:

    def __init__(self, clauses):
        self.clauses = clauses

    def __eq__(self, other):
        return self.clauses == other.clauses

    def __repr__(self):
        return 'AtForm(%s)' % repr(self.clauses)


@builtin.function('make_AtForm')
def make_AtForm(args_bodies):
    return AtForm(preparse(args_bodies))


at = element('at', some(may(call(__.args)) + assign(__.args, getvalue_default(__.args)) + some(getitem_to_list(__.body), __.body, __.bodies), (__.args, __.bodies), vv.args_bodies) + eoi + make_AtForm(vv.args_bodies))
from dao.builtins.rule import replace_def, remove, append_def, insert_def, abolish, retractall, retract

@builtin.function('make_fun1')
def make_fun1(name, rules, klass):
    fun = varcache(name)
    if len(rules) == 0:
        return replace_def(fun, (), [[]], klass)
    if len(rules) == 1:
        return replace_def(fun, preparse(rules[0][0]), preparse(rules[0][1]), klass)
    replaces = []
    for (head, bodies) in rules:
        head = preparse(head)
        bodies = preparse(bodies)
        replaces.append(replace_def(fun, head, bodies, klass))

    return special.begin(*replaces)


@builtin.function('make_fun2')
def make_fun2(name, args, body, klass):
    fun = varcache(name)
    head = args
    body = preparse(body)
    if isinstance(body, AtForm):
        body = body.clauses
        if len(body) > 1:
            raise DinpySyntaxError()
        if body[0][0] is not None:
            raise DinpySyntaxError()
        return append_def(fun, head, body[0][1], klass)
    else:
        return append_def(fun, head, [body], klass)
        return


@builtin.function('make_fun3')
def make_fun3(name, args, body, klass):
    fun = varcache(name)
    head = args
    body = preparse(body)
    if isinstance(body, AtForm):
        body = body.clauses
        if len(body) > 1:
            raise DinpySyntaxError()
        if body[0][0] is not None:
            raise DinpySyntaxError()
        return insert_def(fun, head, body[0][1], klass)
    else:
        return insert_def(fun, head, [body], klass)
        return


@builtin.function('make_fun4')
def make_fun4(name, rules, klass):
    fun = varcache(name)
    rules = preparse(rules)
    if isinstance(rules, AtForm):
        rules1 = []
        for (head, bodies) in rules.clauses:
            if head is None:
                head = ()
            for body in bodies:
                rules1.append((head,) + tuple(body))

        return assign(fun, klass(*rules1))
    else:
        if isinstance(rules, list):
            return assign(fun, klass(((), rules)))
        raise DinpySyntaxError()
        return


@builtin.function('make_fun5')
def make_fun5(name, rules, klass):
    fun = varcache(name)
    rules = preparse(rules)
    if isinstance(rules, AtForm):
        clauses = [ (head if head is not None else (), bodies) for (head, bodies) in rules.clauses ]
        return special.begin(*[ append_def(fun, head, bodies, klass) for (head, bodies) in clauses
                              ])
    else:
        if isinstance(rules, list):
            return append_def(fun, head, [rules], klass)
        raise DinpySyntaxError()
        return


@builtin.function('make_fun6')
def make_fun6(name, rules, klass):
    fun = varcache(name)
    rules = preparse(rules)
    if isinstance(rules, AtForm):
        clauses = [ (head if head is not None else (), bodies) for (head, bodies) in rules.clauses ]
        return special.begin(*[ insert_def(fun, head, bodies, klass) for (head, bodies) in clauses
                              ])
    else:
        if isinstance(rules, list):
            return insert_def(fun, head, [rules], klass)
        raise DinpySyntaxError()
        return


@builtin.function('make_fun7')
def make_fun7(clauses, klass):
    rules = []
    for (head, bodies) in clauses:
        for body in bodies:
            body = preparse(body)
            rules.append((preparse(head),) + tuple(body))

    return klass(*rules)


@builtin.function('make_fun8')
def make_fun8(name, args, klass):
    fun = varcache(name)
    args = preparse(args)
    return remove(fun, args, klass)


def fun_macro_grammar(klass1, klass2):
    return getattr(vv.name) + any(~call(__.args) + assign(__.args, getvalue_default(__.args, ())) + some(getitem_to_list(__.body), __.body, __.bodies), (__.args, __.bodies), vv.rules) + eoi + make_fun1(vv.name, vv.rules, klass2) | getattr(vv.name) + call(vv.args) + ge(vv.body) + eoi + make_fun2(vv.name, vv.args, vv.body, klass2) | getattr(vv.name) + call(vv.args) + le(vv.body) + eoi + make_fun3(vv.name, vv.args, vv.body, klass2) | getattr(vv.name) + eq(vv.rules) + eoi + make_fun4(vv.name, vv.rules, klass1) | getattr(vv.name) + ge(vv.rules) + eoi + make_fun5(vv.name, vv.rules, klass2) | getattr(vv.name) + le(vv.rules) + eoi + make_fun6(vv.name, vv.rules, klass2) | some(may(call(__.args)) + assign(__.args, getvalue_default(__.args, ())) + some(getitem_to_list(__.body), __.body, __.bodies), (__.args, __.bodies), vv.rules) + eoi + make_fun7(vv.rules, klass1) | getattr(vv.name) + neg + div(vv.arity) + eoi + pycall(abolish, getvar(vv.name), vv.arity) | getattr(vv.name) + call(vv.args) + neg + eoi + make_fun8(vv.name, vv.args, klass2)


fun = element('fun', fun_macro_grammar(special.FunctionForm, special.UserFunction))
macro = element('macro', fun_macro_grammar(special.FunctionForm, special.UserMacro))