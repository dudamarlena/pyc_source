# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expy\tex.py
# Compiled at: 2019-10-15 05:21:34
# Size of source mod 2**32: 28601 bytes
import math, numpy as np, sympy as sym, pandas as pd
from sympy import sqrt, sin, cos, tan, exp, log, diff
from pyperclip import copy
from pyperclip import paste
from IPython.display import display, Math, Latex, Image, Markdown, HTML
from .base import to_list
from .calc import weighted_mean, uncrt
from .disp import digitnum, sgnf, roundup, effective_digit, to_sf, df_sf, rslt_ans, rslt_ans_array, rslt_ans_align
from .var import *

def newpage():
    display(Latex('\\newpage'))


def tiny():
    display(Latex('\\tiny'))


def norm():
    display(Latex('\\normalsize'))


def md(text=''):
    display(Md(text))


def caption(text=''):
    display(Caption(text))


def figure(filepath, cap=''):
    display(Image(filepath), Caption(cap))


def table(data, cap='', text=None, index=None, is_sf=False, is_tiny=False):
    rslt = pd.DataFrame(data, index=(index if index else [''] * len(list(data.values())[0]))) if type(data) is type({}) else data
    if is_sf:
        rslt = df_sf(rslt)
    if text:
        display(Caption(text)) if type(text) == type('') else md('以上より, 以下の表を得る')
    if cap:
        display(Caption(cap))
    if is_tiny:
        tiny()
    display(rslt)
    if is_tiny:
        norm()


def freehand(text='', line=12):
    for i in range(line):
        display(Markdown('<p style="page-break-after: always;">&nbsp;</p>'))

    display(Caption(text))


class Md:

    def __init__(self, s):
        self.s = s

    def _repr_html_(self):
        return '%s' % self.s

    def _repr_latex_(self):
        return '\n %s \n' % self.s


class Caption:

    def __init__(self, s=''):
        self.s = s

    def _repr_html_(self):
        return '<center> %s </center>' % self.s

    def _repr_latex_(self):
        return '\\begin{center}\n %s \n\\end{center}' % self.s


def align_asta_latex(unit=[], cp=True, ipynb=True):
    tex = ''
    for i in range(len(unit)):
        if unit[i]:
            if i != 0:
                tex += '\n\t&='
            tex += sym.latex(unit[i])
            if i != 0:
                tex += '\\\\'

    tex = '\\begin{align*}\n\t' + tex + '\n\t' + '\\end{align*}'
    if cp:
        copy(tex)
    if ipynb:
        return Latex(tex)
    return tex


def to_latex(s='x^2+ y^2', ans=0, x='z', rm='', dig=3, cp=True, ipynb=True, label=''):
    return align_asta_latex(['%s' % x, '%s' % s, '%s\\mathrm{%s}' % (to_sf(ans, dig * 2), rm),
     '%s\\mathrm{%s}' % (to_sf(ans, dig), rm)], cp, ipynb)


def frac(denom, numer, ans=0, x='z', rm='', dig=3, cp=True, ipynb=True, label=''):
    return to_latex('{\\tiny \\frac{%s}{%s}}' % (denom, numer), ans, x, rm, dig, cp, ipynb, label)


def weighted(mean_all, uncrt_all, x='z', rm='', dig=3, cp=True, ipynb=True, label=''):

    def tex_weighted_mean(mean_all, uncrt_all, x='z', rm='', cp=True, ipynb=True, label=''):
        denom = ''
        numer = ''
        for i in range(len(mean_all)):
            denom += '\\frac{%s}{(%s)^2}' % (to_sf(mean_all[i], dig), to_sf(uncrt_all[i], dig))
            numer += '\\frac{1}{(%s)^2}' % to_sf(uncrt_all[i], dig)
            if i != len(mean_all) - 1:
                denom += '+'
                numer += '+'

        return frac(denom, numer, weighted_mean(mean_all, uncrt_all)[0], x, rm, dig)

    def tex_weighted_uncrt(mean_all, uncrt_all, x='z', rm='', cp=True, ipynb=True, label=''):
        numer = '\\sqrt{'
        for i in range(len(mean_all)):
            numer += '\\frac{1}{(%s)^2}' % to_sf(uncrt_all[i], dig)
            if i != len(mean_all) - 1:
                numer += '+'
            if i == len(mean_all) - 1:
                numer += '}'

        return frac('1', numer, weighted_mean(mean_all, uncrt_all)[1], x, rm, dig)

    display(tex_weighted_mean(mean_all, uncrt_all, x, rm, cp, ipynb, label))
    display(tex_weighted_uncrt(mean_all, uncrt_all, '\\Delta ' + x, rm, cp, ipynb, label))
    md('よって $%s$ は以下のようになる.' % x)
    rslt_ans_align(weighted_mean(mean_all, uncrt_all)[0], weighted_mean(mean_all, uncrt_all)[1], x, rm, dig)


def dollar(arr):
    if type(arr) != type(''):
        return [' $%s$ ' % v for v in arr]
    return ' $%s$ ' % arr


def mark_number(text):
    rslt = text
    for i, j in zip([str(i) for i in range(10)], ['%{}%'.format(i) for i in range(10)]):
        rslt = rslt.replace(i, j)

    return rslt


class Var:

    def __init__(self, var=sym.Symbol('x')):
        self.var = var
        self.val = 0
        self.dig = 3
        self.rm = ''
        self.array = np.array([0])
        self.err = 1
        self.todiff = None
        self.diffed = None

    def set_var(self, var=None, val=None, rm=None, dig=None):
        if val is not None:
            self.set_array(val)
        if var:
            self.var = var
        if rm:
            self.rm = str(rm)
        if dig:
            self.dig = int(dig)

    def set_array(self, val):
        self.array = np.array(val)
        if self.array.size == 1:
            self.val = val
            self.err = 0
            self.dig = effective_digit(self.val)
        else:
            self.val = np.mean(val)
            self.err = np.std(val) / np.sqrt(len(val) - 1)
            self.dig = effective_digit(self.array[0])

    def set_diff(self, ans_obj, function):
        self.todiff = sym.Symbol('(\\frac{{ \\partial {} }}{{ \\partial {} }})^2'.format(sym.latex(ans_obj.var), sym.latex(self.var)))
        self.diffed = sym.diff(function, self.var) ** 2

    def subs_str(self, func):
        return func.subs(self.var, '%' + sym.latex(self.var) + '%')

    def subs_ans(self, func):
        return func.subs(self.var, self.val)

    def subs_val(self, func):
        return func.subs(self.var, '%s\\mathrm{%s}' % (round(self.val, self.dig), self.rm))

    def tex(self):
        return '%s' % sym.latex(self.var)

    def d_tex(self):
        return '\\Delta{%s}' % sym.latex(self.var)

    def tex_name(self, err=True, rm=True):
        text = '%s\\pm %s' % (self.tex(), self.d_tex()) if err else self.tex()
        return '%s(%s)%s' % ('(' if rm else '', text, '/\\mathrm{%s}' % self.rm if rm else '')

    def df(self, df_name='', name=''):
        data = {'%s' % name: self.array}
        df = pd.DataFrame(data, index=([''] * len(self.array)))
        return df.T

    def latex_mean(self, max=10, cp=True, ipynb=True):
        denom = ''
        N = self.array.size
        for i in range(N):
            if i != 0:
                denom = denom + '+'
            if i >= max:
                denom = denom + '..'
                break
            denom += '%s \\mathrm{%s}' % (to_sf(self.array[i], self.dig), self.rm)

        display(frac(denom, (str(N)), (np.mean(self.array)), (self.tex()), (self.rm), cp=True, ipynb=True))

    def latex_err(self, cp=True, ipynb=True):
        N = self.array.size
        m = to_sf(np.mean(self.array), self.dig)
        s = '\\sqrt{\\frac{1}{%s\\cdot%s}\\sum_{i=1}^%s(%s_i-%s)^2}' % (N, N - 1, N, self.tex(), m)
        display(to_latex(s, (uncrt(self.array)), (self.d_tex()), (self.rm), (self.dig), cp=True, ipynb=True))

    def latex(self, max=10, cp=True, ipynb=True):
        if self.err:
            self.latex_mean(max, cp, ipynb)
            self.latex_err(cp, ipynb)
            rslt_ans_align(self.val, self.err, self.tex_name(rm=False), self.rm, self.dig)


class Eq:

    def __init__(self, leq, req, ans_sym=None, label='', **kwargs):
        self.label = label
        self.func, self.todiff, self.diffed = [None] * 3
        self.subs_str, self.subs_val, self.subs_ans = [None] * 3
        self.func_val, self.func_ans, self.func_rslt = [None] * 3
        self.syn_val, self.syn_ans, self.syn_rslt = [None] * 3
        self.eq = sym.Eq(leq, req)
        self.vars = {}
        self.ans = None
        self.ans_val = 0
        self.err_val = 0
        if ans_sym:
            self.set_func(self.vars[ans_sym].var)
        else:
            if leq in self.vars:
                self.set_func(self.vars[leq].var)

    def set_var(self, obj):
        self.vars[obj.var] = obj

    def set_err(self, var, err):
        self.vars[var].err = err

    def set_func(self, ans_sym=None):
        if ans_sym:
            self.ans = self.vars[ans_sym]
        elif self.ans:
            self.func = sym.solve(self.eq, self.ans.var)[0]
        else:
            print("please set ans_var_object as 'eq_obj.set_ans( var_obj )'")

    def set_ans(self, obj):
        self.set_func(obj.var)
        self.ans = obj

    def set_eq(self, leq, req):
        self.eq = sym.Eq(leq, req)
        self.set_func()

    def set_obj(self, var=None, val=None, rm='', dig=3, ans=False):
        obj = Var()
        obj.set_var(var, val, rm, dig)
        self.set_var(obj)
        if val is None or ans:
            self.set_func(obj.var)

    def set_err(self, var, err):
        self.vars[var].err = err

    def not_setting_obj(self):
        return [v for v in self.eq.atoms(sym.Symbol) if v not in self.vars]

    def status(self):
        for v in self.not_setting_obj():
            print('{0} is not setting. please run "f.set_obj({0})"'.format(v))

        display(pd.DataFrame({' $%s$ ' % sym.latex(var):[obj.val, '$\\mathrm{%s}$' % obj.rm, obj.dig, var == self.ans.var] for var, obj in self.vars.items()}, index=[
         'val', 'rm', 'dig', 'is ans']).T)

    def set_tex(self, err=False):
        if self.ans is None:
            [self.set_obj(var, None) for var in self.not_setting_obj()]
        self.subs_str = self.func
        for var, obj in self.vars.items():
            self.subs_str = obj.subs_str(self.subs_str)

        self.subs_ans = self.func
        for var, obj in self.vars.items():
            self.subs_ans = obj.subs_ans(self.subs_ans)

        self.ans_val = float(self.subs_ans)
        self.func_val = sym.latex(self.subs_str)
        self.func_val = mark_number(self.func_val)
        for var, obj in self.vars.items():
            txt = str(to_sf(float(obj.val), int(obj.dig))) + '\\mathrm{' + obj.rm + '}'
            self.func_val = self.func_val.replace('%{}%'.format(mark_number(obj.tex())), '%({})%'.format(txt))

        self.func_val = self.func_val.replace(' ', '').replace('%%', '\\times ').replace('%', '')
        self.func_ans = '%s\\mathrm{%s}' % (to_sf(self.ans_val, self.ans.dig * 2), self.ans.rm)
        self.func_rslt = '%s\\mathrm{%s}' % (to_sf((self.ans_val), (1 if err else self.ans.dig), up=True), self.ans.rm)

    def set_syn(self):
        for i, (var, obj) in enumerate(self.vars.items()):
            obj.set_diff(self.ans, self.func)
            diff_new = [Delta_(var) ** 2 * obj.todiff, Delta_(var) ** 2 * obj.diffed]
            if var is self.ans.var:
                continue
            if float(obj.err) <= 0:
                continue
            if self.todiff is None or self.diffed is None:
                self.todiff, self.diffed = diff_new
            else:
                self.todiff, self.diffed = [
                 self.todiff + diff_new[0], self.diffed + diff_new[1]]

        self.todiff = self.ans.var * sqrt(self.todiff)
        self.diffed = self.ans.var * sqrt(self.diffed)
        past_eq = self.eq
        past_func = self.func.copy()
        past_vars = self.vars.copy()
        past_ans = self.ans
        past_rslt = self.ans_val
        self.set_eq(Delta_(past_ans.var), self.diffed)
        self.set_obj((Delta_(past_ans.var)), None, (past_ans.rm), (past_ans.dig), ans=1)
        for var, obj in past_vars.items():
            obj.set_diff(self.ans, self.func)
            self.set_obj(Delta_(var), obj.err, obj.rm, obj.dig)

        self.set_obj((past_ans.var), past_rslt, (past_ans.rm), (past_ans.dig), ans=0)
        self.set_tex(err=True)
        self.syn_val = self.func_val
        self.syn_ans = self.func_ans
        self.syn_rslt = self.func_rslt
        self.err_val = self.ans_val
        self.eq = past_eq
        self.func = past_func
        self.vars = past_vars
        self.ans = past_ans
        self.ans_val = past_rslt

    def ans_align(self):
        rslt_ans_align(self.ans_val, self.err_val, self.ans.tex_name(rm=False), self.ans.rm, self.ans.dig)

    def latex(self, cp=True, ipynb=True):
        self.set_tex()
        latex_text = align_asta_latex([
         self.ans.var, self.func,
         self.func_val,
         self.func_ans,
         self.func_rslt], cp, ipynb)
        if ipynb:
            display(latex_text)
        else:
            return latex_text

    def syn(self, cp=True, ipynb=True, sub_val=True):
        self.set_syn()
        latex_text = align_asta_latex([
         self.ans.d_tex(), sym.latex(self.todiff),
         sym.latex(self.diffed),
         self.syn_val if sub_val else None,
         self.syn_ans,
         self.syn_rslt], cp, ipynb)
        if ipynb:
            display(latex_text)
        else:
            return latex_text


class F:

    def __init__(self, leq, req, ans_sym=None, label='', **kwargs):
        self.leq = leq
        self.req = req
        self.ans_sym = ans_sym
        self.label = label
        self.obj = Eq(self.leq, self.req, self.ans_sym, self.label)
        self.objs = []
        self.eq = self.obj.eq

    def set_obj(self, var=None, val=None, rm='', dig=None, ans=False):
        self.obj.set_obj(var, val, rm, dig, ans)

    def set_err(self, var, err):
        self.obj.set_err(var, err)

    def set(self, var=None, val=None, rm='', dig=None, ans=False, err=None):
        self.obj.set_obj(var, val, rm, dig, ans)
        if err:
            self.obj.set_err(var, err)

    def status(self):
        [obj.status() for obj in self.objs]

    def save(self):
        self.obj.set_tex()
        self.objs.append(self.obj)
        self.obj = Eq(self.leq, self.req, self.ans_sym, self.label)

    def get_var(self, var=None):
        if var:
            return self.objs[(-1)].vars[var]
        return self.objs[(-1)].ans

    def get_ans_val(self):
        return [obj.ans_val for obj in self.objs]

    def get_ans_err(self):
        return [obj.err_val for obj in self.objs]

    def get_var_val(self, var):
        return [obj.vars[var].val for obj in self.objs]

    def get_var_err(self, var):
        return [obj.vars[var].err for obj in self.objs]

    def get_var_arr(self, var):
        return [obj.vars[var].array for obj in self.objs]

    def get_rslt_ans(self):
        return rslt_ans_array(self.get_ans_val(), self.get_ans_err(), self.get_var().rm, self.get_var().dig)

    def get_rslt_var(self, var):
        return rslt_ans_array(self.get_var_val(var), self.get_var_err(var), self.get_var(var).rm, self.get_var(var).dig)

    def get_vars(self, var, num=None):
        if type(num) == type(0):
            return [
             self.objs[num].vars[var]]
        if type(num) == type([]):
            return [self.objs[i].vars[var] for i in num]
        if num is None:
            return [obj.vars[var] for obj in self.objs]

    def get(self, var=None, num=None, ans=False, err=False):
        if var:
            vals = self.get_rslt_var(var) if ans else self.get_var_err(var) if err else self.get_var_val(var)
        else:
            vals = self.get_rslt_ans() if ans else self.get_ans_err() if err else self.get_ans_val()
        if type(num) == type(0):
            return vals[num]
        if type(num) == type([]):
            return [vals[n] for n in num]
        return vals

    def latex(self, num=None):
        self.tex_ans(num)

    def tex_num(self, n, arr):
        if arr is None:
            return True
        if n == arr or n in np.array(arr):
            return True
        return False

    def tex_var(self, var, num=None):
        [obj.latex() for obj in self.get_vars(var, num)]

    def tex_ans(self, num=None):
        [obj.latex(ipynb=(self.tex_num(i, num))) for i, obj in enumerate(self.objs)]

    def tex(self, var=None, num=None):
        if self.objs == []:
            self.save()
        elif var:
            self.tex_var(var, num) if var != self.objs[(-1)].ans.var else self.tex_ans(num)
        else:
            self.tex_ans(var if var == 0 else num)

    def syn(self, num=None, sub=True):
        [obj.syn(ipynb=(self.tex_num(i, num)), sub_val=sub) for i, obj in enumerate(self.objs)]

    def df(self, var=None, cap='', index=None, name='', text=False, ans=True, err=False, ipynb=True):
        ans = self.objs[0].ans
        vals = self.get(var, num=None, ans=ans, err=err)
        if type(index) == type({}):
            dict = {key:['$%s$' % v for v in val] for key, val in index.items()}
        else:
            dict = {'回数': ['%s回目' % (i + 1) for i in range(len(vals))]} if index else {}
        if var:
            dict.update({'測定結果$%s$' % ('/\\mathrm{%s}' % ans.rm if ans.rm else ''): [[' $%s$' % to_sf(v) for v in arr] for arr in self.get_var_arr(var)]})
        else:
            dict.update({'$%s%s%s$' % (name, ans.var, '/\\mathrm{%s}' % ans.rm if ans.rm else ''): dollar(vals)})
            if text:
                md(text) if type(text) == type('') else md('全項目の計算結果を下表にまとめた.単位は $\\mathrm{%s}$ である.' % self.get_var().rm)
            if ipynb:
                display(Caption(cap), pd.DataFrame(dict, index=([''] * len(vals))))
            else:
                return pd.DataFrame(dict, index=([''] * len(vals)))

    def md(self, name=None, err=True, text=None):
        if text:
            md(text)
        else:
            md('以上より, %s $%s$ を求めると, 次のようになる.' % (name if name else '', self.get_var().tex_name(rm=False)))

    def auto(self, f_num=0):
        vars_str = ''
        for i, var in enumerate(self.vars.keys()):
            if i == 0:
                vars_str = sym.latex(var)
            else:
                vars_str += ', ' + sym.latex(var)

        md('{}{}を代入して{}を求めると, 次のようになる.'.format([
         '式({})に'.format(f_num) if f_num else ''][0], vars_str, sym.latex(self.ans.var)))

    def mkdf(self, cap='全項目の計算結果', index=None, ref=''):
        md('全項目の計算結果を下表にまとめた.単位は $\\mathrm{%s}$ である.' % self.objs[0].ans.rm)
        if index:
            pass
        data = {}
        for i, obj in enumerate(self.objs):
            data['%s回目' % (i + 1)] = '($%s\\pm %s$)/$\\mathrm{%s}$' % (
             to_sf(obj.ans_val, 3), to_sf((obj.err_val), 1, up=1), obj.ans.rm)

        caption(cap)
        display(pd.DataFrame(data, index=['']))


from sympy import symbols as ss
from sympy import sqrt, sin, cos, tan, exp, log, diff

def sub(var, any):
    return ss('%s_{%s}' % (sym.latex(var), sym.latex(any)))


def sup(var, any):
    return ss('%s^{%s}' % (sym.latex(var), sym.latex(any)))


def sub_0(var):
    return sub(var, 0)


def sub_1(var):
    return sub(var, 1)


def sub_2(var):
    return sub(var, 2)


def sub_i(var):
    return sub(var, i_)


def sub_k(var):
    return sub(var, k_)


def sub_m(var):
    return sub(var, m_)


def sub_n(var):
    return sub(var, n_)


def sub_t(var):
    return sub(var, t_)


def _dash(var):
    return ss("%s'" % sym.latex(var))


def Delta_(var):
    return ss('\\Delta{%s}' % sym.latex(var))


def delta_(var):
    return ss('d%s' % sym.latex(var))


def partial_(var):
    return ss('\\partial{%s}' % sym.latex(var))


def bar_(var):
    return ss('\\bar{%s}' % sym.latex(var))


def frac_(up, down):
    return ss('\\frac{%s}{%s}' % (Delta_(up), Delta_(down)))


def diff_(up, down):
    return ss('\\frac{d%s}{d%s}' % (sym.latex(up), sym.latex(down)))


def part_(up, down):
    return ss('\\frac{%s}{%s}' % (partial_(up), partial_(down)))


def para_(var, any):
    return ss('%s(%s)' % (var, any))