# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expy_python\latex.py
# Compiled at: 2019-04-17 08:48:30
# Size of source mod 2**32: 12481 bytes
"""3.to_latex-------------------------------------------------------------------------"""
begin1 = '\\begin{align}\n\t'
begin2 = '&='
newln = '\\\\\n\t\t&='
end1 = '\\mathrm{'
end2 = '}\\\\\n\t\\label{'
end3 = '}\n\\end{align}'

def print_latex(text):
    latex = text.replace('\t', '').split('\n')
    h = len(latex)
    for i in range(len(latex)):
        t = latex[i]
        print(str(i + 1) + '>  ' + t)
        if not 'begin' in t:
            'end' in t or plt.figure(figsize=(1, 0.5))
            if '&=' in t:
                t = t.replace('&=', '').replace('\\\\', '')
                plt.text(0, 1, ('\t\t=  $' + t + '$'), size='25', va='center', alpha=0.9)
            else:
                plt.text(0, 1, ('$' + t + '$'), size='25', va='center', alpha=0.9)
            plt.axis('off')
            plt.show()


def to_latex(s='%%', answer=0, x='%%', rm='%%', p=0, label=''):
    tex = begin1 + x + begin2 + s + newln + str(answer) + end1 + rm + end2 + label + end3
    print('')
    plt.show()
    if p != 0:
        print_latex(tex)
        return tex
    copy(tex)
    return tex


def align_latex(unit=[], label='', p=0, s=''):
    tex = ''
    for i in range(len(unit)):
        if i != 0:
            tex += '='
        tex += sym.latex(unit[i])

    begin = '\\begin{align}\n\t'
    end = '\n\t\\label{' + label + '}' + '\n\t' + '\\end{align}'
    tex = begin + tex + s + end
    if p != 0:
        print_latex(tex)
        return tex
    copy(tex)
    return tex


def align_asta_latex(unit=[], p=0):
    tex = ''
    for i in range(len(unit)):
        if i != 0:
            tex += '\n\t&='
        tex += sym.latex(unit[i])
        if i != 0:
            tex += '\\\\'

    tex = '\\begin{align*}\n\t' + tex + '\n\t' + '\\end{align*}'
    if p != 0:
        print_latex(tex)
        return tex
    copy(tex)
    return tex


def func_to_latex(func, sym_all=[], val_all=[], rm_all=None, sym_ans='%%', dig_ans=3, rm_ans='%%', p=0):
    if type(sym_ans) is not str:
        sym_ans = sym.latex(sym_ans)

    def func_sym_to_val(func, sym_all, val_all, rm_all):
        if rm_all is None:
            rm_all = [
             ''] * len(sym_all)
        sym_str = []
        for i in sym_all:
            sym_str.append(sym.Symbol('%' + sym.latex(i) + '%'))

        func_str = ep.subs(func, sym_all, sym_str)
        func_str = sym.latex(func_str)
        for i, j in zip(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], ['0%', '1%', '2%', '3%', '4%', '5%', '6%', '7%', '8%', '9%']):
            func_str = func_str.replace(i, j)

        func_str = func_str.replace('%%', '\\times ')
        for i in range(len(sym_all)):
            func_str = func_str.replace(str(sym.latex(sym_str[i])), str(round(val_all[i], 3)) + '\\mathrm{' + rm_all[i] + '}')

        func_str = func_str.replace('%', '')
        print(6, func_str)
        return func_str

    def func_to_ans(func, sym_all, val_all, dig_ans, rm_ans):
        ans = ep.subs(func, sym_all, val_all)
        ans = np.round(float(ans), int(dig_ans + dig_ans))
        ans = str(ans) + rm_ans
        return ans

    def func_to_rslt(func, sym_all, val_all, dig_ans, rm_ans):
        ans = ep.subs(func, sym_all, val_all)
        ans = ep.to_sgnf_fig(float(ans), dig_ans) + rm_ans
        return ans

    latex_text = ep.align_asta_latex([
     sym_ans, func,
     func_sym_to_val(func, sym_all, val_all, rm_all),
     func_to_ans(func, sym_all, val_all, dig_ans, rm_ans),
     func_to_rslt(func, sym_all, val_all, dig_ans, rm_ans)], 0)
    if p != 0:
        print_latex(latex_text)
        return latex_text
    copy(latex_text)
    return latex_text


def frac_to_latex(denom, numer, answer=0, x='%%', rm='%%', p=0, label=''):
    return to_latex('\\frac{' + denom + '}{' + numer + '}', answer, x, rm, p, label)


def mean_to_latex(data, x='%%', rm='%%', p=0, label=''):
    denom = ''
    for i in range(len(data)):
        if i != 0:
            denom = denom + '+'
        denom += str(data[i]) + rm

    return frac_to_latex(denom, str(len(data)), np.mean(data), x, rm, p, label)


def uncrt_to_latex(data, x='%%', rm='%%', p=0, label=''):
    N = len(data)
    m = np.mean(data)
    u = uncrt(data)
    s = '\\sqrt{\\frac{1}{' + str(N) + '\\cdot' + str(N - 1) + '}\\sum_{i=1}^' + str(N) + '(' + x + '_i-' + str(m) + ')^2}'
    return to_latex(s, uncrt(data), 'Δ' + x, rm, p, label)


def mean_sq_to_latex(data, x='%%', rm='%%', p=0, label=''):
    denom = ''
    for i in range(len(data)):
        if i != 0:
            denom = denom + '+'
        denom += '(' + str(data[i]) + ')^{2}'

    return to_latex('\\sqrt{' + denom + '}', mean_sq(data), x, rm, p, label)


def syn_uncrt_to_latex(func=sym.Symbol('f'), uncrt_sym=[], uncrt_all=[], sym_all=[
 sym.Symbol('f')], uncrt_unit_all=[
 0], rm_all=[], x='%%', rm='%%', p=0, label=''):
    ans, partial_all, all_sym_to_val, uncrt_unit_all = syn_uncrt(func, uncrt_sym, uncrt_all, sym_all, uncrt_unit_all, rm_all, 1)
    print([partial_all, '<<<>>>', all_sym_to_val, '<<<>>>', uncrt_unit_all])
    func1 = ''
    func2 = ''
    func3 = ''
    func4 = ''
    for i in range(len(uncrt_all)):
        if i != 0:
            func1 = func1 + '+'
            func2 = func2 + '+'
            func3 = func3 + '+'
            func4 = func4 + '+'
        diff_denom = sym.Symbol('\\partial ' + x)
        diff_numor = sym.Symbol('\\partial ' + str(uncrt_sym[i]))
        func1 = func1 + '(' + sym.latex(diff_denom / diff_numor) + ')^{2}' + '\\Delta ' + str(uncrt_sym[i]) + '^2'
        func2 = func2 + partial_all[i]
        func3 = func3 + all_sym_to_val[i]
        func4 = func4 + '(' + str(uncrt_unit_all[i]) + ')^{2}'
    else:
        func1 = '\\sqrt{' + func1 + '}'
        func2 = '\\sqrt{' + func2 + '}'
        func3 = '\\sqrt{' + func3 + '}'
        func4 = '\\sqrt{' + func4 + '}'

    return to_latex(func1 + '\n\t&=' + func2 + '\n\t&=' + func3 + '\n\t&=' + func4, ans, '\\Delta ' + x, rm, p, label)


def syn_to_latex(func, sym_all=[], val_all=[], uncrt_all=[], rm_all=[], sym_ans='%%', dig_ans=3, rm_ans='%%', p=0):
    if type(sym_ans) is not str:
        sym_ans = sym.latex(sym_ans)

    def func_sym_to_val(func, sym_all, val_all, rm_all):
        if rm_all is None:
            rm_all = [
             ''] * len(sym_all)
        sym_str = []
        for i in sym_all:
            sym_str.append(sym.Symbol('%' + sym.latex(i) + '%'))

        func_str = ep.subs(func, sym_all, sym_str)
        func_str = sym.latex(func_str)
        for i, j in zip(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], ['0%', '1%', '2%', '3%', '4%', '5%', '6%', '7%', '8%', '9%']):
            func_str = func_str.replace(i, j)

        func_str = func_str.replace('%%', '\\times ')
        for i in range(len(sym_all)):
            func_str = func_str.replace(str(sym.latex(sym_str[i])), str(round(val_all[i], 3)) + '\\mathrm{' + rm_all[i] + '}')

        func_str = func_str.replace('%', '')
        print(6, func_str)
        return func_str

    def func_to_ans(funct, sym_all, val_all, dig_ans):
        ans = ep.subs(func, sym_all, val_all)
        ans = ep.subs(ans, sym_all, val_all)
        ans = np.round(float(ans), int(dig_ans + dig_ans))
        return ans

    def func_to_uncrt(func, sym_all, val_all, dig_ans, rm_ans):
        ans = ep.subs(func, sym_all, val_all)
        print(ans)
        ans = np.round(float(ans), int(dig_ans + dig_ans))
        ans = str(ans)
        ans = ans + rm_ans
        return ans

    def func_to_rslt(func, sym_all, val_all, dig_ans, rm_ans):
        ans = ep.subs(func, sym_all, val_all)
        ans = ep.to_sgnf_fig(float(ans), dig_ans) + rm_ans
        return ans

    func_todiff = 0
    func_diffed = 0
    todiff = []
    diffed = []
    sym_uncrt = []
    for s in sym_all:
        todiff.append(sym.Symbol('\\partial ' + sym_ans) / sym.Symbol('\\partial ' + sym.latex(s)))
        diffed.append(diff(func, s))
        sym_uncrt.append(sym.Symbol('Δ' + sym.latex(s)))
        func_todiff = func_todiff + sym.Symbol('\\partial ' + sym_ans) ** 2 / sym.Symbol('\\partial ' + sym.latex(s)) ** 2 * sym.Symbol('Δ' + sym.latex(s)) ** 2
        func_diffed = func_diffed + diff(func, s) ** 2 * sym.Symbol('Δ' + sym.latex(s)) ** 2

    syms = to_list(sym_all) + sym_uncrt
    syms.append(sym.Symbol(sym_ans))
    vals = to_list(val_all) + to_list(uncrt_all)
    vals.append(float(func_to_ans(func, sym_all, val_all, dig_ans)))
    rms = rm_all + rm_all
    rms.append(rm_ans)
    func_todiff = sym.Symbol(sym_ans) * sqrt(func_todiff)
    func_diffed = sym.Symbol(sym_ans) * sqrt(func_diffed)
    latex_text = ep.align_asta_latex([
     'Δ' + sym_ans,
     func_todiff,
     func_diffed,
     func_sym_to_val(func_diffed, syms, vals, rms),
     func_to_uncrt(func_diffed, syms, vals, dig_ans, rm_ans),
     func_to_rslt(func_diffed, syms, vals, dig_ans, rm_ans)], 0)
    if p != 0:
        print_latex(latex_text)
        return latex_text
    copy(latex_text)
    return latex_text


def weighted_mean_to_latex(mean_all, uncrt_all, x='%%', rm='%%', p=0, label=''):
    denom = ''
    numer = ''
    for i in range(len(mean_all)):
        denom += '\\frac{' + str(mean_all[i]) + '}{(' + str(uncrt_all[i]) + ')^2}'
        numer += '\\frac{1}{(' + str(uncrt_all[i]) + ')^2}'
        if i != len(mean_all) - 1:
            denom += '+'
            numer += '+'

    return frac_to_latex(denom, numer, weighted_mean(mean_all, uncrt_all)[0], x, rm, p, label)


def weighted_uncrt_to_latex(mean_all, uncrt_all, x='%%', rm='%%', p=0, label=''):
    numer = '\\sqrt{'
    for i in range(len(mean_all)):
        numer += '\\frac{1}{(' + str(uncrt_all[i]) + ')^2}'
        if i != len(mean_all) - 1:
            numer += '+'
        if i == len(mean_all) - 1:
            numer += '}'

    return frac_to_latex('1', numer, weighted_mean(mean_all, uncrt_all)[1], x, rm, p, label)


def df_to_latex(df, label='%%%%', c=None, i=False, p=0):
    txt_bgn = '\\begin{table}[htb]\\label{' + label + '}\n\t\\centering\n\t\\caption{' + label + '}\n'
    txt_end = '\t\\end{table}\n'
    latex = df.to_latex(index=i, columns=c, escape=False)
    if p != 0:
        print(txt_bgn + latex + txt_end)
    else:
        copy(txt_bgn + latex + txt_end)


def alnm():
    txt = paste()
    s = ''
    pi = ''
    for i in txt:
        if not pi.isalnum():
            if i.isalnum():
                s = s + '$' + i
            elif pi.isalnum():
                if not i.isalnum():
                    s = s + i + '$'
                else:
                    s = isinstance(i, unicode) or s
                if i == ' ':
                    s = s
                if i == '．':
                    s = s
                if i == '，':
                    s = s
                if i == '。':
                    s = s + '.'
                if i == '、':
                    s = s + ','
            else:
                s = s + i
            pi = i