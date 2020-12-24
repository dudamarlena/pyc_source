# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jovyan/lemma/lemma/lang.hy
# Compiled at: 2020-04-12 01:38:44
# Size of source mod 2**32: 10678 bytes
import hy.macros
from hy.core.language import comp, eval, first, is_empty, is_even, is_list, is_none, is_numeric, is_symbol, keyword, name, nth, partition, rest, second
from hy import HyExpression, HyKeyword, HySymbol
hy.macros.require('hy.contrib.walk', None, assignments=[['let', 'let']], prefix='')
from typing import Any, Union, Callable, Sequence, Mapping
from hy.models import HyObject, HySymbol, HyExpression, HyList
from hy.contrib.walk import postwalk
import hy.contrib.hy_repr as hy_repr
from lemma.exceptions import *

class LatexString(str):

    def __new__(cls, text: str, precedence: Union[(int, float)]):
        _hyx_letXUffffX1 = {}
        _hyx_letXUffffX1['str-obj'] = str.__new__(cls, text)
        _hyx_letXUffffX1['str-obj'].precedence = precedence
        return _hyx_letXUffffX1['str-obj']


class HyCode:

    def __init__(self, form, bindings):
        self.form = form
        self.bindings = bindings
        return None

    def run(self):
        return eval(self.form, self.bindings)


class LeSyntax:

    def __init__(self):
        self.name = str(hex(id(self)))
        return None

    def __repr__(self):
        return self.__class__.__name__ + '#' + str(self.name)


class LeConstant(LeSyntax):

    def __init__(self, latex_val, hy_val):
        super().__init__()
        self.latex_val = latex_val
        self.hy_val = hy_val
        return None

    def latex(self):
        return gen_latex(self)

    def hy(self):
        return gen_hy(self)

    def __call__(self):
        return eval(self.hy())


class LeIdentifier(LeConstant):

    def __init__(self, latex_val, hy_val):
        super().__init__(latex_val, hy_val)
        return None


class LeExpression(LeSyntax):

    def __init__(self, body):
        super().__init__()
        self.body = body
        return None

    def bind(self, bindings: Mapping[(str, Any)]):

        def _hy_anon_var_16(form):
            if isinstance(form, HySymbol):
                try:
                    _hy_anon_var_12 = eval(form, bindings)
                except NameError:
                    _hy_anon_var_12 = form

                _hy_anon_var_15 = _hy_anon_var_12
            else:
                if isinstance(form, LeIdentifier):
                    try:
                        _hy_anon_var_13 = eval(form.hy_val, bindings)
                    except NameError:
                        _hy_anon_var_13 = form

                    _hy_anon_var_14 = _hy_anon_var_13
                else:
                    _hy_anon_var_14 = form
                _hy_anon_var_15 = _hy_anon_var_14
            return _hy_anon_var_15

        return LeExpression(postwalk(_hy_anon_var_16, self.body))

    def latex(self):
        return gen_latex(self)

    def hy(self):
        return gen_hy(self)

    def __call__(self):
        return eval(self.hy())

    def __repr__(self):
        return 'LeExpression#' + hy_repr(self.body)


class LeOperator(LeSyntax):

    def __init__(self, latex_fn, hy_fn):
        super().__init__()
        self.latex_fn = latex_fn
        self.hy_fn = hy_fn
        return None

    def __call__(self, *args, **kwargs):
        return eval((self.hy_fn)(*args, **kwargs))


class LeFormula(LeOperator):

    def __init__(self, latex_fn, expr_fn, latex_name, arg_identifiers, arg_groups):
        _hyx_letXUffffX2 = {}
        _hyx_letXUffffX2['hy-fn'] = lambda *args, **kwargs: gen_hy(expr_fn(*args, **kwargs))
        super().__init__(latex_fn, _hyx_letXUffffX2['hy-fn'])
        self.body_latex = lambda *args, **kwargs: gen_latex(expr_fn(*args, **kwargs))
        self.expr_fn = expr_fn
        self.latex_name = latex_name
        self.arg_identifiers = arg_identifiers
        self.arg_groups = arg_groups
        return None

    def signature_latex(self):
        return formula_signature_latex(self.latex_name, self.arg_groups, self.arg_identifiers)

    def latex(self, *args, **kwargs):
        _hyx_letXUffffX3 = {}
        _hyx_letXUffffX3['body-latex'] = (self.body_latex)(*self.arg_identifiers) if (is_empty(args) and is_empty(kwargs)) else ((self.body_latex)(*args, **kwargs))
        return LatexString(self.signature_latex() + ' = ' + _hyx_letXUffffX3['body-latex'], 0)

    @property
    def op(self):
        LeOperator
        _hyx_letXUffffX4 = {}
        _hyx_letXUffffX4['operator'] = LeOperator(self.body_latex, self.hy_fn)
        _hyx_letXUffffX4['operator'].name = self.name + '.op'
        return _hyx_letXUffffX4['operator']


class LeEquation(LeSyntax):

    def __init__(self, expressions_fn, arg_identifiers):
        super().__init__()
        self.expressions_fn = expressions_fn
        self.arg_identifiers = arg_identifiers
        return None

    def latex(self, *args, **kwargs):
        _hyx_letXUffffX5 = {}
        _hyx_letXUffffX5['expressions'] = (self.expressions_fn)(*self.arg_identifiers) if (is_empty(args) and is_empty(kwargs)) else ((self.expressions_fn)(*args, **kwargs))
        _hyx_letXUffffX5['latexs'] = list(map(gen_latex, _hyx_letXUffffX5['expressions']))
        return '\\begin{aligned} ' + first(_hyx_letXUffffX5['latexs']) + ' &= ' + ' \\\\&= '.join(rest(_hyx_letXUffffX5['latexs'])) + '\\end{aligned}'

    def __call__(self, *args, **kwargs):
        _hyx_letXUffffX6 = {}
        _hyx_letXUffffX6['expressions'] = list((self.expressions_fn)(*args, **kwargs))
        _hyx_letXUffffX6['results'] = list(map(comp(eval, gen_hy), _hyx_letXUffffX6['expressions']))
        _hyx_letXUffffX6['first-result'] = first(_hyx_letXUffffX6['results'])
        for result, expression in zip(rest(_hyx_letXUffffX6['results']), rest(_hyx_letXUffffX6['expressions'])):
            if not result == _hyx_letXUffffX6['first-result']:
                raise LeEquationError('While evaluating ' + repr(self) + ' with arguments [' + ', '.join(list(map(str, args)) + list(map(lambda pair: '='.join(map(str, pair)), kwargs.items()))) + "]: result '" + str(result) + "' of " + repr(expression) + " did not equal result '" + str(_hyx_letXUffffX6['first-result']) + "' of " + repr(first(_hyx_letXUffffX6['expressions'])))
                _hy_anon_var_30 = None
            else:
                _hy_anon_var_30 = None

        return _hyx_letXUffffX6['first-result']


def make_identifier(symbol, latex=None):
    _hyx_letXUffffX7 = {}
    _hyx_letXUffffX7['identifier'] = LeIdentifier(LatexString(name(symbol) if is_none(latex) else latex, 0), symbol)
    _hyx_letXUffffX7['identifier'].name = name(symbol)
    return _hyx_letXUffffX7['identifier']


ARG_GROUP_KEYS = {
 HyKeyword('paren'), HyKeyword('super'), HyKeyword('sub')}

def formula_signature_latex(latex_name, arg_groups, arg_identifiers):
    arg_grouping_dict = {HyKeyword('sub'): [], HyKeyword('super'): [], HyKeyword('paren'): []}
    for arg, group in zip(arg_identifiers, arg_groups):
        arg_grouping_dict[group].append(gen_latex(arg))

    _hyx_letXUffffX8 = {}
    _hyx_letXUffffX8['sub-args'] = '' if is_empty(arg_grouping_dict[HyKeyword('sub')]) else '_{' + ','.join(arg_grouping_dict[HyKeyword('sub')]) + '}'
    _hyx_letXUffffX8['super-args'] = '' if is_empty(arg_grouping_dict[HyKeyword('super')]) else '^{' + ','.join(arg_grouping_dict[HyKeyword('super')]) + '}'
    _hyx_letXUffffX8['paren-args'] = '' if is_empty(arg_grouping_dict[HyKeyword('paren')]) else '\\left(' + ','.join(arg_grouping_dict[HyKeyword('paren')]) + '\\right)'
    return LatexString(latex_name + _hyx_letXUffffX8['sub-args'] + _hyx_letXUffffX8['super-args'] + _hyx_letXUffffX8['paren-args'], 0)


def hyx_validate_even_bindingsXexclamation_markX(caller, bindings):
    if not is_even(len(bindings)):
        raise LeSyntaxError(f"An even number of bindings must be supplied to {caller}.")
        _hy_anon_var_34 = None
    else:
        _hy_anon_var_34 = None
    return _hy_anon_var_34


def is_operator_application(form):
    if isinstance(form, HyExpression):
        if isinstance(first(form), LeOperator):
            _hy_anon_var_36 = True
        else:
            raise LeSyntaxError(f"Unrecognised LeOperator: {first(form)}")
            _hy_anon_var_36 = None
        _hy_anon_var_37 = _hy_anon_var_36
    else:
        _hy_anon_var_37 = False
    return _hy_anon_var_37


def is_tag_application(form):
    return isinstance(form, HyExpression) and first(form) == HySymbol('dispatch-tag-macro')


def is_listy(form):
    return is_list(form) or isinstance(form, HyList)


def latex_format_numeric(number):
    return str(number)


def latex_enclose_arg(max_precedence, arg_latex_string):
    if arg_latex_string.precedence >= max_precedence:
        return LatexString('\\left(' + arg_latex_string + '\\right)', 0)
    return arg_latex_string


def split_args(args):
    args = list(args)
    first_keyword_neg_index = 0
    while True:
        _hyx_letXUffffX9 = {}
        _hyx_letXUffffX9['next-index'] = first_keyword_neg_index - 2
        if abs(_hyx_letXUffffX9['next-index']) <= len(args) and isinstance(args[_hyx_letXUffffX9['next-index']], HyKeyword):
            first_keyword_neg_index = _hyx_letXUffffX9['next-index']
            _hy_anon_var_43 = None
        else:
            break
            _hy_anon_var_43 = None

    if first_keyword_neg_index == 0:
        _hy_anon_var_44 = {HyKeyword('args'): args, 
         HyKeyword('kwargs'): {}}
    else:
        hyx_Xdollar_signX = args
        hyx_Xdollar_signX = hyx_Xdollar_signX[first_keyword_neg_index:None:None]
        hyx_Xdollar_signX = partition(hyx_Xdollar_signX, 2)
        hyx_Xdollar_signX = map(lambda pair: [name(first(pair)), second(pair)], hyx_Xdollar_signX)
        hyx_Xdollar_signX = dict(hyx_Xdollar_signX)
        _hy_anon_var_44 = {HyKeyword('args'): list(args[0:first_keyword_neg_index:None]), 
         
         HyKeyword('kwargs'): hyx_Xdollar_signX}
    return _hy_anon_var_44


bare = LeOperator(lambda body: LatexString(gen_latex(body), 0), lambda body: gen_hy(body))
bare.name = 'bare'
parens = LeOperator(lambda body: LatexString('\\left(' + gen_latex(body) + '\\right)', 0), lambda body: gen_hy(body))
parens.name = 'parens'

def resolve_tag_operator(tagname):
    if tagname == 'p':
        _hy_anon_var_47 = parens
    else:
        if tagname == 'b':
            _hy_anon_var_46 = bare
        else:
            raise LeSyntaxError('Unrecognised tag operator for Lemma: ' + str(tagname))
            _hy_anon_var_46 = None
        _hy_anon_var_47 = _hy_anon_var_46
    return _hy_anon_var_47


def gen_latex(form):
    try:
        if isinstance(form, LeExpression):
            _hy_anon_var_55 = gen_latex(form.body)
        else:
            if is_tag_application(form):
                _hy_anon_var_54 = gen_latex(LeExpression(HyExpression([] + [resolve_tag_operator(nth(form, 1))] + [nth(form, 2)])))
            else:
                if is_operator_application(form):
                    _hyx_letXUffffX10 = {}
                    _hyx_letXUffffX10['args'] = split_args(rest(form))
                    _hy_anon_var_53 = (first(form).latex_fn)(*HyKeyword('args')(_hyx_letXUffffX10['args']), **HyKeyword('kwargs')(_hyx_letXUffffX10['args']))
                else:
                    if isinstance(form, LeConstant):
                        _hy_anon_var_52 = form.latex_val
                    else:
                        if is_numeric(form):
                            _hy_anon_var_51 = LatexString(latex_format_numeric(form), 0)
                        else:
                            if is_symbol(form):
                                _hy_anon_var_50 = LatexString(str(form), 0)
                            else:
                                if is_listy(form):
                                    _hy_anon_var_49 = LatexString('\\{' + ', '.join(map(gen_latex, form)) + '\\}', 0)
                                else:
                                    raise LeSyntaxError(f"Cannot interpret lemma form {hy_repr(form)}")
                                    _hy_anon_var_49 = None
                                _hy_anon_var_50 = _hy_anon_var_49
                            _hy_anon_var_51 = _hy_anon_var_50
                        _hy_anon_var_52 = _hy_anon_var_51
                    _hy_anon_var_53 = _hy_anon_var_52
                _hy_anon_var_54 = _hy_anon_var_53
            _hy_anon_var_55 = _hy_anon_var_54
        _hy_anon_var_56 = _hy_anon_var_55
    except Exception as ex:
        try:
            if not isinstance(ex, LeRuntimeError):
                raise isinstance(ex, LeSyntaxError) or LeRuntimeError(f"Error generating latex for lemma form: {hy_repr(form)}") from ex
                _hy_anon_var_57 = None
            else:
                raise
                _hy_anon_var_57 = None
            _hy_anon_var_56 = _hy_anon_var_57
        finally:
            ex = None
            del ex

    return _hy_anon_var_56


def gen_hy(form):
    try:
        if isinstance(form, LeExpression):
            _hy_anon_var_65 = gen_hy(form.body)
        else:
            if is_tag_application(form):
                _hy_anon_var_64 = gen_hy(LeExpression(HyExpression([] + [resolve_tag_operator(nth(form, 1))] + [nth(form, 2)])))
            else:
                if is_operator_application(form):
                    _hyx_letXUffffX11 = {}
                    _hyx_letXUffffX11['args'] = split_args(rest(form))
                    _hy_anon_var_63 = (first(form).hy_fn)(*HyKeyword('args')(_hyx_letXUffffX11['args']), **HyKeyword('kwargs')(_hyx_letXUffffX11['args']))
                else:
                    if isinstance(form, LeConstant):
                        _hy_anon_var_62 = form.hy_val
                    else:
                        if is_numeric(form):
                            _hy_anon_var_61 = form
                        else:
                            if is_symbol(form):
                                _hy_anon_var_60 = form
                            else:
                                if is_listy(form):
                                    _hy_anon_var_59 = list(map(gen_hy, form))
                                else:
                                    raise LeSyntaxError(f"Cannot interpret lemma form {hy_repr(form)}")
                                    _hy_anon_var_59 = None
                                _hy_anon_var_60 = _hy_anon_var_59
                            _hy_anon_var_61 = _hy_anon_var_60
                        _hy_anon_var_62 = _hy_anon_var_61
                    _hy_anon_var_63 = _hy_anon_var_62
                _hy_anon_var_64 = _hy_anon_var_63
            _hy_anon_var_65 = _hy_anon_var_64
        _hy_anon_var_66 = _hy_anon_var_65
    except Exception as ex:
        try:
            if not isinstance(ex, LeRuntimeError):
                raise isinstance(ex, LeSyntaxError) or LeRuntimeError(f"Error generating code for lemma form: {hy_repr(form)}") from ex
                _hy_anon_var_67 = None
            else:
                raise
                _hy_anon_var_67 = None
            _hy_anon_var_66 = _hy_anon_var_67
        finally:
            ex = None
            del ex

    return _hy_anon_var_66