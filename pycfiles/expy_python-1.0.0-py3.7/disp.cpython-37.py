# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expy_python\disp.py
# Compiled at: 2019-04-17 08:48:44
# Size of source mod 2**32: 1668 bytes
"""2.表示-------------------------------------------------------------------------"""

def roundup(x, dig):
    func = lambda x: math.ceil(x * 10 ** dig) / 10 ** dig
    return to_multi_d(func, x, 0)


def rounder(x, dig):
    func = lambda x: round(x, dig)
    return to_multi_d(func, x, 0)


def digitnum(x):

    def digitnum_unit(x):
        y = abs(x) + abs(x) * 1e-13
        if y >= 1:
            return math.floor(math.log10(y))
        if 1 > y > 0:
            return -math.floor(math.log10(1 / y) + 1)
        if y == 0:
            return 0

    func = lambda x: digitnum_unit(x)
    return to_multi_d(func, x, is_list=0)


def to_sgnf_fig(n_in, num_sgnf):
    dig = ep.digitnum(n_in)
    n_rslt = n_in * 10 ** (-dig)
    n_rslt = np.round(n_rslt, num_sgnf - 1)
    rslt = str(n_rslt) + '\\times 10^{' + str(dig) + '}'
    return rslt


def sgnf(n_in, num_sgnf):
    dig = ep.digitnum(n_in)
    n_rslt = n_in * 10 ** (-dig)
    print(1, n_rslt)
    n_rslt = np.round(n_rslt, num_sgnf - 1)
    print(2, n_rslt)
    n_rslt = n_rslt * 10 ** dig
    print(3, n_rslt)
    return n_rslt


def rslt(mean, uncrt):

    def roundup(x, dig):
        return math.ceil(x * 10 ** dig) / 10 ** dig

    def rslt_unit(mean, uncrt):
        dig = -digitnum(uncrt)
        return str(rounder(mean, dig)) + '±' + str(roundup(uncrt, dig))

    func = lambda m, u: rslt_unit(m, u)
    return to_multi_d(func, mean, 0, uncrt)


def rslt_polyfit(x, y, dig=3):
    a, b = np.polyfit(x, y, 1)
    return 'y=' + str(round(a, dig)) + 'x+' + str(round(b, dig))


def rslt_polyfit_plot(x, y):
    a, b = np.polyfit(x, y, 1)
    y = []
    for i in x:
        y.append(i * a + b)

    plt.plot(x, y, '^--')