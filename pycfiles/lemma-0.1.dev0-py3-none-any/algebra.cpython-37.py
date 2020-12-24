# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jovyan/lemma/lemma/algebra.hy
# Compiled at: 2020-04-12 00:57:52
# Size of source mod 2**32: 2254 bytes
import hy.macros
from hy.core.language import first, is_none, name, rest, take_nth
from hy import HyExpression, HySymbol
hy.macros.require('hy.contrib.walk', None, assignments=[['let', 'let']], prefix='')
hy.macros.require('lemma.core', None, assignments='ALL', prefix='le')
from functools import partial
import math
from lemma.lang import gen_latex, gen_hy, latex_enclose_arg, hyx_validate_even_bindingsXexclamation_markX
hy.macros.require('lemma.core', None, assignments='ALL', prefix='lemma.core')
import lemma.lang
hy.macros.require('hy.contrib.walk', None, assignments='ALL', prefix='hy.contrib.walk')
import lemma.lang
_hyx_letXUffffX13 = {}
_hyx_letXUffffX13['-latex-val\uffff12'] = '\\pi'
PI = lemma.lang.LeConstant(_hyx_letXUffffX13['-latex-val\uffff12'] if (isinstance(_hyx_letXUffffX13['-latex-val\uffff12'], lemma.lang.LatexString) and is_none(None)) else (lemma.lang.LatexString(_hyx_letXUffffX13['-latex-val\uffff12'], 0 if is_none(None) else None)), math.pi)
PI.name = name(HySymbol('PI'))
if not is_none(None):
    PI.__doc__ = None
    _hy_anon_var_1 = None
else:
    _hy_anon_var_1 = None

def _hy_anon_var_2(numerator, denominator):
    import lemma.lang
    hy.macros.require('lemma.core', None, assignments='ALL', prefix='lemma.core')
    numerator = lemma.lang.gen_latex(numerator)
    denominator = lemma.lang.gen_latex(denominator)
    hy.macros.require('hy.contrib.walk', None, assignments='ALL', prefix='hy.contrib.walk')
    import lemma.lang
    _hyx_letXUffffX15 = {}
    _hyx_letXUffffX15['-latex-val\uffff14'] = '\\frac{' + numerator + '}{' + denominator + '}'
    if isinstance(_hyx_letXUffffX15['-latex-val\uffff14'], lemma.lang.LatexString):
        if is_none(10):
            return _hyx_letXUffffX15['-latex-val\uffff14']
    return lemma.lang.LatexString(_hyx_letXUffffX15['-latex-val\uffff14'], 0 if is_none(10) else 10)


def _hy_anon_var_3(numerator, denominator):
    import lemma.lang, lemma.core
    numerator = lemma.lang.gen_hy(numerator)
    denominator = lemma.lang.gen_hy(denominator)
    return lemma.core.resolve_hy_code({'numerator':numerator, 
     'denominator':denominator}, HyExpression([] + [HySymbol('do')] + [
     HyExpression([] + [HySymbol('/')] + [HySymbol('numerator')] + [HySymbol('denominator')])]))


frac = lemma.lang.LeOperator(_hy_anon_var_2, _hy_anon_var_3)
if not is_none(None):
    frac.__doc__ = None
    _hy_anon_var_4 = None
else:
    _hy_anon_var_4 = None
frac.name = name(HySymbol('frac'))

def _hy_anon_var_5(value, exponent):
    import lemma.lang
    hy.macros.require('lemma.core', None, assignments='ALL', prefix='lemma.core')
    value = lemma.lang.gen_latex(value)
    exponent = lemma.lang.gen_latex(exponent)
    hy.macros.require('hy.contrib.walk', None, assignments='ALL', prefix='hy.contrib.walk')
    import lemma.lang
    _hyx_letXUffffX17 = {}
    _hyx_letXUffffX17['-latex-val\uffff16'] = f"{latex_enclose_arg(10, value)}^{exponent}"
    if isinstance(_hyx_letXUffffX17['-latex-val\uffff16'], lemma.lang.LatexString):
        if is_none(5):
            return _hyx_letXUffffX17['-latex-val\uffff16']
    return lemma.lang.LatexString(_hyx_letXUffffX17['-latex-val\uffff16'], 0 if is_none(5) else 5)


def _hy_anon_var_6(value, exponent):
    import lemma.lang, lemma.core
    value = lemma.lang.gen_hy(value)
    exponent = lemma.lang.gen_hy(exponent)
    return lemma.core.resolve_hy_code({'value':value, 
     'exponent':exponent}, HyExpression([] + [HySymbol('do')] + [
     HyExpression([] + [HySymbol('**')] + [HySymbol('value')] + [HySymbol('exponent')])]))


exp = lemma.lang.LeOperator(_hy_anon_var_5, _hy_anon_var_6)
if not is_none(None):
    exp.__doc__ = None
    _hy_anon_var_7 = None
else:
    _hy_anon_var_7 = None
exp.name = name(HySymbol('exp'))

def _hy_anon_var_8(value):
    import lemma.lang
    hy.macros.require('lemma.core', None, assignments='ALL', prefix='lemma.core')
    value = lemma.lang.gen_latex(value)
    hy.macros.require('hy.contrib.walk', None, assignments='ALL', prefix='hy.contrib.walk')
    import lemma.lang
    _hyx_letXUffffX19 = {}
    _hyx_letXUffffX19['-latex-val\uffff18'] = f"|{value}|"
    if isinstance(_hyx_letXUffffX19['-latex-val\uffff18'], lemma.lang.LatexString):
        if is_none(10):
            return _hyx_letXUffffX19['-latex-val\uffff18']
    return lemma.lang.LatexString(_hyx_letXUffffX19['-latex-val\uffff18'], 0 if is_none(10) else 10)


def _hy_anon_var_9(value):
    import lemma.lang, lemma.core
    value = lemma.lang.gen_hy(value)
    return lemma.core.resolve_hy_code({'value': value}, HyExpression([] + [HySymbol('do')] + [
     HyExpression([] + [HySymbol('len')] + [HySymbol('value')])]))


length = lemma.lang.LeOperator(_hy_anon_var_8, _hy_anon_var_9)
if not is_none(None):
    length.__doc__ = None
    _hy_anon_var_10 = None
else:
    _hy_anon_var_10 = None
length.name = name(HySymbol('length'))

def _hy_anon_var_11(*args):
    import lemma.lang
    hy.macros.require('lemma.core', None, assignments='ALL', prefix='lemma.core')
    args = list(map(lemma.lang.gen_latex, args))
    hy.macros.require('hy.contrib.walk', None, assignments='ALL', prefix='hy.contrib.walk')
    import lemma.lang
    _hyx_letXUffffX21 = {}
    _hyx_letXUffffX21['-latex-val\uffff20'] = ' + '.join(map(partial(latex_enclose_arg, 100), args))
    if isinstance(_hyx_letXUffffX21['-latex-val\uffff20'], lemma.lang.LatexString):
        if is_none(100):
            return _hyx_letXUffffX21['-latex-val\uffff20']
    return lemma.lang.LatexString(_hyx_letXUffffX21['-latex-val\uffff20'], 0 if is_none(100) else 100)


def _hy_anon_var_12(*args):
    import lemma.lang, lemma.core
    args = list(map(lemma.lang.gen_hy, args))
    return lemma.core.resolve_hy_code({'args': args}, HyExpression([] + [HySymbol('do')] + [
     HyExpression([] + [HySymbol('+')] + [HyExpression([] + [HySymbol('unpack-iterable')] + [HySymbol('args')])])]))


add = lemma.lang.LeOperator(_hy_anon_var_11, _hy_anon_var_12)
if not is_none(None):
    add.__doc__ = None
    _hy_anon_var_13 = None
else:
    _hy_anon_var_13 = None
add.name = name(HySymbol('add'))

def _hy_anon_var_14(*args):
    import lemma.lang
    hy.macros.require('lemma.core', None, assignments='ALL', prefix='lemma.core')
    args = list(map(lemma.lang.gen_latex, args))
    hy.macros.require('hy.contrib.walk', None, assignments='ALL', prefix='hy.contrib.walk')
    import lemma.lang
    _hyx_letXUffffX23 = {}
    _hyx_letXUffffX23['-latex-val\uffff22'] = ' - '.join(map(partial(latex_enclose_arg, 100), args)) if len(args) > 1 else f"-{first(args)}"
    if isinstance(_hyx_letXUffffX23['-latex-val\uffff22'], lemma.lang.LatexString):
        if is_none(100):
            return _hyx_letXUffffX23['-latex-val\uffff22']
    return lemma.lang.LatexString(_hyx_letXUffffX23['-latex-val\uffff22'], 0 if is_none(100) else 100)


def _hy_anon_var_15(*args):
    import lemma.lang, lemma.core
    args = list(map(lemma.lang.gen_hy, args))
    return lemma.core.resolve_hy_code({'args': args}, HyExpression([] + [HySymbol('do')] + [
     HyExpression([] + [HySymbol('hy.core.shadow.-')] + [HyExpression([] + [HySymbol('unpack-iterable')] + [HySymbol('args')])])]))


subtract = lemma.lang.LeOperator(_hy_anon_var_14, _hy_anon_var_15)
if not is_none(None):
    subtract.__doc__ = None
    _hy_anon_var_16 = None
else:
    _hy_anon_var_16 = None
subtract.name = name(HySymbol('subtract'))

def _hy_anon_var_17(*args):
    import lemma.lang
    hy.macros.require('lemma.core', None, assignments='ALL', prefix='lemma.core')
    args = list(map(lemma.lang.gen_latex, args))
    hy.macros.require('hy.contrib.walk', None, assignments='ALL', prefix='hy.contrib.walk')
    import lemma.lang
    _hyx_letXUffffX25 = {}
    _hyx_letXUffffX25['-latex-val\uffff24'] = ' \\times '.join(map(partial(latex_enclose_arg, 50), args))
    if isinstance(_hyx_letXUffffX25['-latex-val\uffff24'], lemma.lang.LatexString):
        if is_none(50):
            return _hyx_letXUffffX25['-latex-val\uffff24']
    return lemma.lang.LatexString(_hyx_letXUffffX25['-latex-val\uffff24'], 0 if is_none(50) else 50)


def _hy_anon_var_18(*args):
    import lemma.lang, lemma.core
    args = list(map(lemma.lang.gen_hy, args))
    return lemma.core.resolve_hy_code({'args': args}, HyExpression([] + [HySymbol('do')] + [
     HyExpression([] + [HySymbol('*')] + [HyExpression([] + [HySymbol('unpack-iterable')] + [HySymbol('args')])])]))


multiply = lemma.lang.LeOperator(_hy_anon_var_17, _hy_anon_var_18)
if not is_none(None):
    multiply.__doc__ = None
    _hy_anon_var_19 = None
else:
    _hy_anon_var_19 = None
multiply.name = name(HySymbol('multiply'))

def _hy_anon_var_20(bindings, body):
    hy.macros.require('hy.contrib.walk', None, assignments='ALL', prefix='hy.contrib.walk')
    import lemma.lang
    _hyx_letXUffffX27 = {}
    hyx_validate_even_bindingsXexclamation_markX('set-sum', bindings)
    _hyx_letXUffffX28 = {}
    _hyx_letXUffffX28['identifiers'] = map(gen_latex, take_nth(2, bindings))
    _hyx_letXUffffX28['values'] = map(gen_latex, take_nth(2, rest(bindings)))
    _hyx_letXUffffX28['latex-bindings'] = ', '.join(map(lambda ident, val: f"{ident} \\in {val}", _hyx_letXUffffX28['identifiers'], _hyx_letXUffffX28['values']))
    _hyx_letXUffffX27['-latex-val\uffff26'] = '\\sum_{' + _hyx_letXUffffX28['latex-bindings'] + '} ' + gen_latex(body)
    if isinstance(_hyx_letXUffffX27['-latex-val\uffff26'], lemma.lang.LatexString):
        if is_none(500):
            return _hyx_letXUffffX27['-latex-val\uffff26']
    return lemma.lang.LatexString(_hyx_letXUffffX27['-latex-val\uffff26'], 0 if is_none(500) else 500)


def _hy_anon_var_21(bindings, body):
    hyx_validate_even_bindingsXexclamation_markX('set-sum', bindings)
    return HyExpression([] + [HySymbol('sum')] + [HyExpression([] + [HySymbol('lfor')] + list(map(gen_hy, bindings) or []) + [gen_hy(body)])])


set_sum = lemma.lang.LeOperator(_hy_anon_var_20, _hy_anon_var_21)
if not is_none(None):
    set_sum.__doc__ = None
    _hy_anon_var_22 = None
else:
    _hy_anon_var_22 = None
set_sum.name = name(HySymbol('set-sum'))