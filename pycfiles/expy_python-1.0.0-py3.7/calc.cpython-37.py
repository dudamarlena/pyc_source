# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expy_python\calc.py
# Compiled at: 2019-04-17 08:47:02
# Size of source mod 2**32: 7787 bytes
"""1.解析-------------------------------------------------------------------------"""

def to_list(data):
    if type(data) is type(pd.Series([])):
        return data.values.tolist()
    if type(data) is type(pd.DataFrame([])):
        return data.values.tolist()
    if type(data) is type(np.array([])):
        return data.tolist()
    return data


def to_discrete(arr, method=lambda a, b: b - a, axis=0):
    if type(arr) is type(pd.DataFrame([])):
        if axis == 0:
            arr = arr.T

    def _to_discrete(arr, method=lambda a, b: b - a):
        arr_rslt = [np.NaN]
        for i in range(len(arr) - 1):
            arr_rslt.append(method(arr[i], arr[(i + 1)]))

        return arr_rslt

    arr_in = to_list(arr)
    func = lambda arr: _to_discrete(arr, method)
    return to_multi_d(func, arr_in, 1)


def to_multi_d(func, data, is_list, data2=None, is_none=None):
    data = to_list(data)

    def do(to_arr=0):
        if data is None:
            return is_none
        if to_arr == 0:
            if data2 is None:
                return func(data)
            return func(data, data2)
        if to_arr == 1:
            if data2 is None:
                return func([data])
            return func([data], [data2])

    def repeat():
        output = []
        for i in range(len(data)):
            if data2 is None:
                output.append(to_multi_d(func, data[i], is_list, is_none))
            else:
                output.append(to_multi_d(func, data[i], is_list, data2[i], is_none))

        return output

    if type(data) is not list:
        if is_list == 0:
            return do()
        if is_list == 1:
            return do(1)
        p('not ? but 0')
    elif type(data) is list:
        if is_list == 0:
            return repeat()
            if is_list == 1:
                if type(data[0]) is not list:
                    return do()
                if type(data[0]) is list:
                    return repeat()
        else:
            p('not ? but 1')
    else:
        return '??'


def mm_to_cm(a):
    func = lambda a: a / 10
    return to_multi_d(func, a, 0)


def cm_to_m(a):
    func = lambda a: a / 100
    return to_multi_d(func, a, 0)


def cm_to_mm(a):
    func = lambda a: a * 10
    return to_multi_d(func, a, 0)


def mean(a):
    func = lambda a: np.mean(a)
    return to_multi_d(func, a, 1)


def subs(func, sym, val):
    for i in range(len(val)):
        func = func.subs([(sym[i], val[i])])

    return func


def STDEV(data):

    def STDEV_unit(d):
        ave = np.sum(d) / len(d)
        siguma = 0
        for i in range(len(d)):
            siguma += math.pow(d[i] - ave, 2)

        if len(d) <= 1:
            return 0
        output = math.sqrt(siguma / (len(d) - 1))
        return output

    func = lambda d: STDEV_unit(d)
    return to_multi_d(func, data, 1)


def uncrt(data):

    def uncrt_unit(data):
        output = STDEV(data) / math.sqrt(len(data))
        return output

    func = lambda d: uncrt_unit(d)
    return to_multi_d(func, data, 1)


def rlt_uncrt(data):

    def rlt_uncrt_unit(data):
        return uncrt(data) / np.mean(data)

    func = lambda d: rlt_uncrt_unit(d)
    return to_multi_d(func, data, 1)


def cul(data, p=0):

    def cul_unit(data):
        mean = np.mean(data)
        uncrt = ep.uncrt(data)
        rslt = ep.rslt(mean, uncrt)
        rlt = ep.rlt_uncrt(data)
        df_cul = pd.DataFrame([uncrt, rslt, rlt], index=['uncrt', 'rslt', 'rlt/%'])
        df_cul = pd.Series(data).describe().append(df_cul)
        if p == 1:
            display(df_cul.T)
        return df_cul.T

    unit = lambda d: cul_unit(d)
    return to_multi_d(unit, data, 1)


def mean_sq(data):

    def mean_sq_unit(data1, data2):
        import math
        synth = math.sqrt(math.pow(data1, 2) + math.pow(data2, 2))
        return synth

    func = lambda d1, d2: mean_sq_unit(d1, d2)
    synth = data[0]
    for i in range(1, len(data)):
        synth = to_multi_d(func, synth, 0, data[i])

    return synth


def syn_uncrt(func=sym.Symbol('f'), uncrt_sym=[], uncrt_all=[], sym_all=[
 sym.Symbol('f')], val_all=[
 0], rm_all=[], arr=0):

    def sym_to_val_to_latex(func, sym_all=[], val_all=[], rm_all=[]):
        sym_str = []
        if rm_all == []:
            rm_all = [
             ''] * len(sym_all)
        for i in sym_all:
            sym_str.append(sym.Symbol('[]' + str(i) + '[]'))

        func_str = subs(func, sym_all, sym_str)
        func_str = sym.latex(func_str)
        for i in range(len(sym_all)):
            func_str = func_str.replace(str(sym.latex(sym_str[i])), '(' + str(round(val_all[i], 3)) + '\\mathrm{' + rm_all[i] + '}' + ')')

        return func_str

    def syn_uncrt_unit(uncrt_all=[], val_all=[0]):
        syn = 0
        partial_all = []
        all_sym_to_val = []
        uncrt_unit_all = []

        def uncrt_to_unit_uncrt(u, sym):
            df_dsym = diff(func, sym)
            for i in range(len(sym_all)):
                df_dsym = df_dsym.subs([(sym_all[i], val_all[i])])

            return u * float(df_dsym)

        for i in range(len(uncrt_all)):
            unit_uncrt = 0
            unit_uncrt_sym = sym.Symbol('\\Delta ' + str(uncrt_sym[i])) ** 2
            unit_parcial = unit_uncrt_sym
            if uncrt_sym[i] is None:
                syn = mean_sq([syn, uncrt_all[i]])
                unit_uncrt = uncrt_all[i]
            else:
                unit_uncrt = uncrt_to_unit_uncrt(uncrt_all[i], uncrt_sym[i])
                unit_parcial = diff(func, uncrt_sym[i]) ** 2
                unit_sym_to_val = sym_to_val_to_latex(unit_parcial, sym_all, val_all, rm_all) + '(' + str(uncrt_all[i]) + ')^{2}'
                unit_parcial = sym.latex(unit_parcial) + sym.latex(unit_uncrt_sym)
                syn = mean_sq([syn, unit_uncrt])
            partial_all.append(unit_parcial)
            uncrt_unit_all.append(unit_uncrt)
            all_sym_to_val.append(unit_sym_to_val)

        if arr == 0:
            return syn
        return [
         syn,
         partial_all,
         all_sym_to_val,
         uncrt_unit_all]

    unit = lambda u, v: syn_uncrt_unit(u, v)
    return to_multi_d(unit, uncrt_all, 1, val_all)


def weighted_mean(mean_all, uncrt_all):

    def weighted_uncrt_unit(mean_all, uncrt_all):
        numer1 = mean_all / np.square(uncrt_all)
        denom1 = 1 / np.square(uncrt_all)
        mean = np.sum(numer1) / np.sum(denom1)
        denom2 = 1 / np.square(uncrt_all)
        uncrt = 1 / np.sqrt(np.sum(denom2))
        return (mean, uncrt)

    func = lambda m, u: weighted_uncrt_unit(m, u)
    return to_multi_d(func, mean_all, 1, uncrt_all)