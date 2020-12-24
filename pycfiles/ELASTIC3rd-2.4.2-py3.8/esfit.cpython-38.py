# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\elastic3rd\post\esfit.py
# Compiled at: 2020-01-13 11:07:44
# Size of source mod 2**32: 5553 bytes
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np, math

def esfit_2nd(x, y):
    coef, pcov = curve_fit(esfun_2nd, x, y)
    return (coef, pcov)


def esfun_2nd(x, c2):
    y = c2 * x ** 2
    return y


def esfit_3rd(x, y):
    coef, pcov = curve_fit(esfun_3rd, x, y)
    return (coef, pcov)


def esfun_3rd(x, c2, c3):
    y = c2 * x ** 2 + c3 * x ** 3
    return y


def esfit(x, y, flag_se='e', flag_ord=3):
    flag_se = flag_se.lower()
    if flag_se == 'e':
        coef, pcov = eval('curve_fit(esfun_energy_' + str(flag_ord) + ', x, y)')
    else:
        if flag_se == 's':
            pass
    return (
     coef, pcov)


def esfun_energy_3(x, c2, c3):
    y = c2 * x ** 2 + c3 * x ** 3
    return y


def esfun_energy_2(x, c2, c3):
    y = c2 * x + c3 * x ** 2
    return y


def esfun_energy_1(x, c2, c3):
    y = c2 + c3 * x
    return y


def esfun_energy_4(x, c2, c3, c4):
    y = c2 * x ** 2 + c3 * x ** 3 + c4 * x ** 4
    return y


def esfun_energy_5(x, c2, c3, c4, c5):
    y = c2 * x ** 2 + c3 * x ** 3 + c4 * x ** 4 + c5 * x ** 5
    return y


def esfun_energy_6(x, c2, c3, c4, c5, c6):
    y = c2 * x ** 2 + c3 * x ** 3 + c4 * x ** 4 + c5 * x ** 5 + c6 * x ** 6
    return y


def esfun_energy_7(x, c2, c3, c4, c5, c6, c7):
    y = c2 * x ** 2 + c3 * x ** 3 + c4 * x ** 4 + c5 * x ** 5 + c6 * x ** 6 + c7 * x ** 7
    return y


def esfun_energy_8(x, c2, c3, c4, c5, c6, c7, c8):
    y = c2 * x ** 2 + c3 * x ** 3 + c4 * x ** 4 + c5 * x ** 5 + c6 * x ** 6 + c7 * x ** 7 + c8 * x ** 8
    return y


def esfun_energy_9(x, c2, c3, c4, c5, c6, c7, c8, c9):
    y = c2 * x ** 2 + c3 * x ** 3 + c4 * x ** 4 + c5 * x ** 5 + c6 * x ** 6 + c7 * x ** 7 + c8 * x ** 8 + c9 * x ** 9
    return y


def yfitfun(x, c, flag_se='e', flag_ord=3):
    if flag_ord == 4:
        c2, c3, c4 = c
    else:
        if flag_ord == 5:
            c2, c3, c4, c5 = c
        else:
            if flag_ord == 6:
                c2, c3, c4, c5, c6 = c
            else:
                c2, c3 = c
    flag_se = flag_se.lower()
    if flag_se == 'e':
        if flag_ord == 1:
            yfit = esfun_energy_1(x, c2, c3)
        else:
            if flag_ord == 2:
                yfit = esfun_energy_2(x, c2, c3)
            else:
                if flag_ord == 3:
                    yfit = esfun_energy_3(x, c2, c3)
                else:
                    if flag_ord == 4:
                        yfit = esfun_energy_4(x, c2, c3, c4)
                    else:
                        if flag_ord == 5:
                            yfit = esfun_energy_5(x, c2, c3, c4, c5)
                        else:
                            if flag_ord == 6:
                                yfit = esfun_energy_6(x, c2, c3, c4, c5, c6)
                            else:
                                if flag_ord == 7:
                                    yfit = esfun_energy_7(x, c2, c3, c4, c5, c6, c7)
                                else:
                                    if flag_ord == 8:
                                        yfit = esfun_energy_6(x, c2, c3, c4, c5, c6, c7, c8)
                                    else:
                                        if flag_ord == 9:
                                            yfit = esfun_energy_7(x, c2, c3, c4, c5, c6, c7, c8, c9)
    else:
        if flag_se == 's':
            pass
        return yfit


def esplot(x, y, coef, V0, flag_se='e', flag_ord=3):
    eVpmol2GPa = 160.21719175
    n = 100
    xmin = np.amin(x)
    xmax = np.amax(x)
    xfit = np.linspace(xmin, xmax, n)
    if flag_se == 'e':
        yfit = V0 / eVpmol2GPa * yfitfun(xfit, coef, flag_se, flag_ord)
    else:
        if flag_se == 's':
            pass
    plotori = plt.plot(x, y, '*', label='original data')
    plotfit = plt.plot(xfit, yfit, 'r', label='fitting')
    plt.show()


def multiesplot(s, e, coef, flag_se, flag_ord, V0):
    m, n = e.shape
    n_d = int((m - 1) / 2)
    for i in range(0, n):
        coefi = coef[i, :]
        print(coefi)
        ei = e[:, i] - e[n_d][i]
        if flag_ord > 2:
            s2 = s
            e2 = ei
        else:
            s2 = s
            s2[n_d] = 1
            if flag_ord == 1:
                e2 = ei / s2 / s2
                s2 = np.delete(s2, n_d)
                e2 = np.delete(e2, n_d)
            else:
                if flag_ord == 2:
                    e2 = ei / s2
                    s2[n_d] = 0
        esplot(s2, e2, coefi, V0, flag_se, flag_ord)