# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/lune/phase.py
# Compiled at: 2020-05-07 04:25:50
# Size of source mod 2**32: 22871 bytes
"""From a date given in parameter,
the algorithm returns dates for :
- the new moon;
- the first quarter;
- the full moon;
- last quarter

Author : Keller Stéphane.
Teacher of Mathematics, Physics, Chemistry, informatics and Digital science and technology.
Agricultural High School Louis Pasteur - Marmilhat.  B.P. 116 - 63 370 Lempdes
stephane.keller@yahoo.com
https://github.com/KELLERStephane/KELLER-Stephane-Tests2maths

Usage :
>>> from moons import phase
>>> phase.lunar_phase(day, month, year)
"""
from math import cos, sin, radians
import datetime, calendar
__all__ = [
 'angle', 'jj2date', 'calcul_Ci', 'lunar_phase', 'between_dates']

def angle(alpha):
    """Input: any alpha angle in degrees.
Output: the angle such that 0 <= alpha < 360"""
    n = 1
    alpha2 = alpha
    while alpha <= 0:
        alpha = alpha2 + n * 360
        n += 1

    n = 1
    alpha2 = alpha
    while alpha > 360:
        alpha -= n * 360
        n += 1

    return alpha


def jj2date(JJ):
    """Input: one day Julian of the ephemerides.
Output: the date in the form (day, month, year)"""
    JJ += 0.5
    Z = int(JJ)
    F = JJ - Z
    if Z < 2299161:
        A = Z
    else:
        alpha = int((Z - 1867216.25) / 36524.25)
        A = Z + 1 + alpha - int(alpha / 4)
    B = A + 1524
    C = int((B - 122.1) / 365.25)
    D = int(365.25 * C)
    E = int((B - D) / 30.6001)
    JD = B - D - int(30.6001 * E) + F
    J = int(JD)
    if E < 13.5:
        M = E - 1
    else:
        M = E - 13
    if M > 2.5:
        A = C - 4716
    else:
        A = C - 4715
    return '%02d/%02d/%04d' % (J, M, A)


def calcul_Ci(k, T):
    r"""Input: the coefficients k and T ;
    (T is the time in Julian centuries since the epoch 2000.0).
Output: the list of the 1st group of the 14 corrections of the \☻
periodic terms for the new moon."""
    A1 = 299.77 + 0.107408 * k - 0.009173 * T ** 2
    A2 = 251.88 + 0.016321 * k
    A3 = 251.83 + 26.651886 * k
    A4 = 349.42 + 36.412478 * k
    A5 = 84.66 + 18.206239 * k
    A6 = 141.74 + 53.303771 * k
    A7 = 207.14 + 2.453732 * k
    A8 = 154.84 + 7.30686 * k
    A9 = 34.52 + 27.261239 * k
    A10 = 207.19 + 0.121824 * k
    A11 = 291.34 + 1.844379 * k
    A12 = 161.72 + 24.198154 * k
    A13 = 239.56 + 25.513099 * k
    A14 = 331.55 + 3.592518 * k
    li_A = [A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11, A12, A13, A14]
    C1 = 0.000325 * sin(radians(A1))
    C2 = 0.000165 * sin(radians(A2))
    C3 = 0.000164 * sin(radians(A3))
    C4 = 0.000126 * sin(radians(A4))
    C5 = 0.00011 * sin(radians(A5))
    C6 = 6.2e-05 * sin(radians(A6))
    C7 = 6e-05 * sin(radians(A7))
    C8 = 5.6e-05 * sin(radians(A8))
    C9 = 4.7e-05 * sin(radians(A9))
    C10 = 4.2e-05 * sin(radians(A10))
    C11 = 4e-05 * sin(radians(A11))
    C12 = 3.7e-05 * sin(radians(A12))
    C13 = 3.5e-05 * sin(radians(A13))
    C14 = 2.3e-05 * sin(radians(A14))
    li_C = [C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12, C13, C14]
    SOM_C = sum(li_C)
    return (
     li_C, SOM_C)


def lunar_phase(day, month, year):
    """Input: a date in the format (day, month, year).
    Output: the list of the four dates corresponding respectively to :
    - the new moon;
    - the first quarter;
    - the full moon;
    - the last quarter
    in the form Julian day and in the form (day, month, year)."""
    delta = (datetime.date(year, month, day) - datetime.date(year, 1, 1)).days
    nb_days_year = (datetime.date(year, 12, 31) - datetime.date(year, 1, 1)).days + 1
    li_JDE, li_date = [], []
    year_plus_month = year + delta / nb_days_year
    j = 12.3685 * (year_plus_month - 2000)
    k = round(j)
    T = k / 1236.85
    E = 1 - 0.002516 * T - 7.4e-06 * T ** 2
    JDE = 2451550.09765 + 29.530588853 * k + 0.0001337 * T ** 2 - 1.5e-07 * T ** 3 + 7.3e-10 * T ** 4
    M = 2.5534 + 29.1053567 * k - 1.4e-06 * T ** 2 - 1.1e-07 * T ** 3
    M_prime = 201.5643 + 385.81693528 * k + 0.0107438 * T ** 2 + 1.239e-05 * T ** 3 - 5.8e-08 * T ** 4
    F = 160.7108 + 390.67050274 * k - 0.0016341 * T ** 2 - 2.27e-06 * T ** 3 + 1.1e-08 * T ** 4
    OMEGA = 124.7746 - 1.5637558 * k + 0.0020691 * T ** 2 + 2.15e-06 * T ** 3
    li_C, SOM_C = calcul_Ci(k, T)
    NM1 = -0.4072 * sin(radians(M_prime))
    NM2 = 0.17241 * E * sin(radians(M))
    NM3 = 0.01608 * sin(radians(2 * M_prime))
    NM4 = 0.01039 * sin(radians(2 * F))
    NM5 = 0.00739 * E * sin(radians(M_prime - M))
    NM6 = -0.00514 * E * sin(radians(M_prime + M))
    NM7 = -0.00208 * E ** 2 * sin(radians(2 * M))
    NM8 = -0.00111 * sin(radians(M_prime - 2 * F))
    NM9 = -0.00057 * sin(radians(M_prime + 2 * F))
    NM10 = 0.00056 * E * sin(radians(2 * M_prime + M))
    NM11 = -0.00042 * sin(radians(3 * M_prime))
    NM12 = 0.00042 * E * sin(radians(M + 2 * F))
    NM13 = 0.00038 * E * sin(radians(M - 2 * F))
    NM14 = -0.00024 * E * sin(radians(2 * M_prime - M))
    NM15 = -0.00017 * sin(radians(OMEGA))
    NM16 = -7e-05 * sin(radians(M_prime + 2 * M))
    NM17 = 4e-05 * sin(radians(2 * M_prime - 2 * F))
    NM18 = 4e-05 * sin(radians(3 * M))
    NM19 = 3e-05 * sin(radians(M_prime + M - 2 * F))
    NM20 = 3e-05 * sin(radians(2 * M_prime + 2 * F))
    NM21 = 3e-05 * sin(radians(M_prime + M + 2 * F))
    NM22 = 3e-05 * sin(radians(M_prime - M + 2 * F))
    NM23 = -2e-05 * sin(radians(M_prime - M - 2 * F))
    NM24 = -2e-05 * sin(radians(3 * M_prime + M))
    NM25 = 2e-05 * sin(radians(4 * M_prime))
    li_NM = [NM1, NM2, NM3, NM4, NM5, NM6, NM7, NM8, NM9, NM10, NM11, NM12,
     NM13, NM14, NM15, NM16, NM17, NM18, NM19, NM20, NM21, NM22, NM23,
     NM24, NM25]
    SOM_NM = sum(li_NM)
    JDE_NM = JDE + SOM_NM + SOM_C
    li_JDE += [JDE_NM]
    li_date += [jj2date(JDE_NM)]
    k += 0.25
    T = k / 1236.85
    E = 1 - 0.002516 * T - 7.4e-06 * T ** 2
    JDE = 2451550.09765 + 29.530588853 * k + 0.0001337 * T ** 2 - 1.5e-07 * T ** 3 + 7.3e-10 * T ** 4
    M = 2.5534 + 29.1053567 * k - 1.4e-06 * T ** 2 - 1.1e-07 * T ** 3
    M_prime = 201.5643 + 385.81693528 * k + 0.0107438 * T ** 2 + 1.239e-05 * T ** 3 - 5.8e-08 * T ** 4
    F = 160.7108 + 390.67050274 * k - 0.0016341 * T ** 2 - 2.27e-06 * T ** 3 + 1.1e-08 * T ** 4
    OMEGA = 124.7746 - 1.5637558 * k + 0.0020691 * T ** 2 + 2.15e-06 * T ** 3
    W = 0.00306 - 0.00038 * E * cos(radians(M)) + 0.00026 * cos(radians(M_prime)) - 2e-05 * cos(radians(M_prime - M)) + 2e-05 * cos(radians(M_prime + M)) + 2e-05 * cos(radians(2 * F))
    li_C, SOM_C = calcul_Ci(k, T)
    li_C, SOM_C = calcul_Ci(k, T)
    FQ1 = -0.62801 * sin(radians(M_prime))
    FQ2 = 0.17172 * E * sin(radians(M))
    FQ3 = -0.01183 * E * sin(radians(M_prime + M))
    FQ4 = 0.00862 * sin(radians(2 * M_prime))
    FQ5 = 0.00804 * sin(radians(2 * F))
    FQ6 = 0.00454 * E * sin(radians(M_prime - M))
    FQ7 = 0.00204 * E ** 2 * sin(radians(2 * M))
    FQ8 = -0.0018 * sin(radians(M_prime - 2 * F))
    FQ9 = -0.0007 * sin(radians(M_prime + 2 * F))
    FQ10 = -0.0004 * sin(radians(3 * M_prime))
    FQ11 = -0.00034 * E * sin(radians(2 * M_prime - M))
    FQ12 = 0.00032 * E * sin(radians(M + 2 * F))
    FQ13 = 0.00032 * E * sin(radians(M - 2 * F))
    FQ14 = -0.00028 * E ** 2 * sin(radians(M_prime + 2 * M))
    FQ15 = 0.00027 * E * sin(radians(2 * M_prime + M))
    FQ16 = -0.00017 * sin(radians(OMEGA))
    FQ17 = -5e-05 * sin(radians(M_prime - M - 2 * F))
    FQ18 = 4e-05 * sin(radians(2 * M_prime + 2 * F))
    FQ19 = -4e-05 * sin(radians(M_prime + M + 2 * F))
    FQ20 = 4e-05 * sin(radians(M_prime - 2 * M))
    FQ21 = 3e-05 * sin(radians(M_prime + M - 2 * F))
    FQ22 = 3e-05 * sin(radians(3 * M))
    FQ23 = 2e-05 * sin(radians(2 * M_prime - 2 * F))
    FQ24 = 2e-05 * sin(radians(M_prime - M + 2 * F))
    FQ25 = -2e-05 * sin(radians(3 * M_prime + M))
    li_FQ = [FQ1, FQ2, FQ3, FQ4, FQ5, FQ6, FQ7, FQ8, FQ9, FQ10, FQ11, FQ12, FQ13,
     FQ14, FQ15, FQ16, FQ17, FQ18, FQ19, FQ20, FQ21, FQ22, FQ23, FQ24, FQ25]
    SOM_FQ = sum(li_FQ)
    JDE_FQ = JDE + SOM_FQ + SOM_C + W
    li_JDE += [JDE_FQ]
    li_date += [jj2date(JDE_FQ)]
    k += 0.25
    T = k / 1236.85
    E = 1 - 0.002516 * T - 7.4e-06 * T ** 2
    JDE = 2451550.09765 + 29.530588853 * k + 0.0001337 * T ** 2 - 1.5e-07 * T ** 3 + 7.3e-10 * T ** 4
    M = 2.5534 + 29.1053567 * k - 1.4e-06 * T ** 2 - 1.1e-07 * T ** 3
    M_prime = 201.5643 + 385.81693528 * k + 0.0107438 * T ** 2 + 1.239e-05 * T ** 3 - 5.8e-08 * T ** 4
    F = 160.7108 + 390.67050274 * k - 0.0016341 * T ** 2 - 2.27e-06 * T ** 3 + 1.1e-08 * T ** 4
    OMEGA = 124.7746 - 1.5637558 * k + 0.0020691 * T ** 2 + 2.15e-06 * T ** 3
    li_C, SOM_C = calcul_Ci(k, T)
    FM1 = -0.40614 * sin(radians(M_prime))
    FM2 = 0.17302 * E * sin(radians(M))
    FM3 = 0.01614 * sin(radians(2 * M_prime))
    FM4 = 0.01043 * sin(radians(2 * F))
    FM5 = 0.00734 * E * sin(radians(M_prime - M))
    FM6 = -0.00515 * E * sin(radians(M_prime + M))
    FM7 = -0.00209 * E ** 2 * sin(radians(2 * M))
    FM8 = -0.00111 * sin(radians(M_prime - 2 * F))
    FM9 = -0.00057 * sin(radians(M_prime + 2 * F))
    FM10 = 0.00056 * E * sin(radians(2 * M_prime + M))
    FM11 = -0.00042 * sin(radians(3 * M_prime))
    FM12 = 0.00042 * E * sin(radians(M + 2 * F))
    FM13 = 0.00038 * E * sin(radians(M - 2 * F))
    FM14 = -0.00024 * E * sin(radians(2 * M_prime - M))
    FM15 = -0.00017 * sin(radians(OMEGA))
    FM16 = -7e-05 * sin(radians(M_prime + 2 * M))
    FM17 = 4e-05 * sin(radians(2 * M_prime - 2 * F))
    FM18 = 4e-05 * sin(radians(3 * M))
    FM19 = 3e-05 * sin(radians(M_prime + M - 2 * F))
    FM20 = 3e-05 * sin(radians(2 * M_prime + 2 * F))
    FM21 = 3e-05 * sin(radians(M_prime + M + 2 * F))
    FM22 = 3e-05 * sin(radians(M_prime - M + 2 * F))
    FM23 = -2e-05 * sin(radians(M_prime - M - 2 * F))
    FM24 = -2e-05 * sin(radians(3 * M_prime + M))
    FM25 = 2e-05 * sin(radians(4 * M_prime))
    li_FM = [FM1, FM2, FM3, FM4, FM5, FM6, FM7, FM8, FM9, FM10, FM11, FM12,
     FM13, FM14, FM15, FM16, FM17, FM18, FM19, FM20, FM21, FM22, FM23, FM24,
     FM25]
    SOM_FM = sum(li_FM)
    JDE_FM = JDE + SOM_FM + SOM_C
    li_JDE += [JDE_FM]
    li_date += [jj2date(JDE_FM)]
    k += 0.25
    T = k / 1236.85
    E = 1 - 0.002516 * T - 7.4e-06 * T ** 2
    JDE = 2451550.09765 + 29.530588853 * k + 0.0001337 * T ** 2 - 1.5e-07 * T ** 3 + 7.3e-10 * T ** 4
    M = 2.5534 + 29.1053567 * k - 1.4e-06 * T ** 2 - 1.1e-07 * T ** 3
    M_prime = 201.5643 + 385.81693528 * k + 0.0107438 * T ** 2 + 1.239e-05 * T ** 3 - 5.8e-08 * T ** 4
    F = 160.7108 + 390.67050274 * k - 0.0016341 * T ** 2 - 2.27e-06 * T ** 3 + 1.1e-08 * T ** 4
    OMEGA = 124.7746 - 1.5637558 * k + 0.0020691 * T ** 2 + 2.15e-06 * T ** 3
    W = 0.00306 - 0.00038 * E * cos(radians(M)) + 0.00026 * cos(radians(M_prime)) - 2e-05 * cos(radians(M_prime - M)) + 2e-05 * cos(radians(M_prime + M)) + 2e-05 * cos(radians(2 * F))
    li_C, SOM_C = calcul_Ci(k, T)
    li_C, SOM_C = calcul_Ci(k, T)
    LQ1 = -0.62801 * sin(radians(M_prime))
    LQ2 = 0.17172 * E * sin(radians(M))
    LQ3 = -0.01183 * E * sin(radians(M_prime + M))
    LQ4 = 0.00862 * sin(radians(2 * M_prime))
    LQ5 = 0.00804 * sin(radians(2 * F))
    LQ6 = 0.00454 * E * sin(radians(M_prime - M))
    LQ7 = 0.00204 * E ** 2 * sin(radians(2 * M))
    LQ8 = -0.0018 * sin(radians(M_prime - 2 * F))
    LQ9 = -0.0007 * sin(radians(M_prime + 2 * F))
    LQ10 = -0.0004 * sin(radians(3 * M_prime))
    LQ11 = -0.00034 * E * sin(radians(2 * M_prime - M))
    LQ12 = 0.00032 * E * sin(radians(M + 2 * F))
    LQ13 = 0.00032 * E * sin(radians(M - 2 * F))
    LQ14 = -0.00028 * E ** 2 * sin(radians(M_prime + 2 * M))
    LQ15 = 0.00027 * E * sin(radians(2 * M_prime + M))
    LQ16 = -0.00017 * sin(radians(OMEGA))
    LQ17 = -5e-05 * sin(radians(M_prime - M - 2 * F))
    LQ18 = 4e-05 * sin(radians(2 * M_prime + 2 * F))
    LQ19 = -4e-05 * sin(radians(M_prime + M + 2 * F))
    LQ20 = 4e-05 * sin(radians(M_prime - 2 * M))
    LQ21 = 3e-05 * sin(radians(M_prime + M - 2 * F))
    LQ22 = 3e-05 * sin(radians(3 * M))
    LQ23 = 2e-05 * sin(radians(2 * M_prime - 2 * F))
    LQ24 = 2e-05 * sin(radians(M_prime - M + 2 * F))
    LQ25 = -2e-05 * sin(radians(3 * M_prime + M))
    li_LQ = [LQ1, LQ2, LQ3, LQ4, LQ5, LQ6, LQ7, LQ8, LQ9, LQ10, LQ11,
     LQ12, LQ13, LQ14, LQ15, LQ16, LQ17, LQ18, LQ19, LQ20, LQ21, LQ22,
     LQ23, LQ24, LQ25]
    SOM_LQ = sum(li_LQ)
    JDE_LQ = JDE + SOM_LQ + SOM_C - W
    li_JDE += [JDE_LQ]
    li_date += [jj2date(JDE_LQ)]
    return (
     li_JDE, li_date)


def between_dates(periode, d_NM, d_FQ, d_FM, d_LQ):
    """Input: dates periode (any date),
    d_NM (date of the new moon),
    d_FQ (date or the first quarter),
    d_FM (date ouf the full moon),
    d_LQ (date of the last quarter) in the form 'DD/MM/YYYY'.
    Output: the number of the image corresponding to visibility of the moon on this date and if necessary, the particular state, of the moon on this date."""
    day, month, year = periode.split('/')
    d = datetime.date(int(year), int(month), int(day))
    day_NM, month_NM, year_NM = d_NM.split('/')
    d_NM = datetime.date(int(year_NM), int(month_NM), int(day_NM))
    day_FQ, month_FQ, year_FQ = d_FQ.split('/')
    d_FQ = datetime.date(int(year_FQ), int(month_FQ), int(day_FQ))
    day_FM, month_FM, year_FM = d_FM.split('/')
    d_FM = datetime.date(int(year_FM), int(month_FM), int(day_FM))
    day_LQ, month_LQ, year_LQ = d_LQ.split('/')
    d_LQ = datetime.date(int(year_LQ), int(month_LQ), int(day_LQ))
    if (d - d_NM).days == 0:
        return ('0.png', 'Nouvelle lune')
    if (d - d_FQ).days == 0:
        return ('8.png', 'Premier quartier')
    if (d - d_FM).days == 0:
        return ('15.png', 'Pleine lune')
    if (d - d_LQ).days == 0:
        return ('22.png', 'Dernier quartier')
    if 0 < (d - d_NM).days:
        if (d_FQ - d).days > 0:
            return (
             str((d - d_NM).days) + '.png', '')
    if 0 < (d - d_FQ).days:
        if (d_FM - d).days > 0:
            return (
             str((d - d_FQ).days + 8) + '.png', '')
    if 0 < (d - d_FM).days:
        if (d_LQ - d).days > 0:
            return (
             str((d - d_FM).days + 15) + '.png', '')
    return (
     str((d - d_LQ).days + 51) + '.png', '')


if __name__ == '__main__':
    print('The date display is in the form DD/MM/YYYY    then JJ (Julian day)')
    print('\nExample with the date May 24, 1969')
    day, month, year = (24, 5, 1969)
    periode = str(day) + '/' + str(month) + '/' + str(year)
    (JDE_NM, JDE_FQ, JDE_FM, JDE_LQ), (d_NM, d_FQ, d_FM, d_LQ) = lunar_phase(day, month, year)
    print('Date  =', str(day), '/', str(month) + '/' + str(year))
    print('Date of the new moon =', d_NM, '\n', JDE_NM)
    print('Date of the first quarter =', d_FQ, '\n', JDE_FQ)
    print('Date of the full moon =', d_FM, '\n', JDE_FM)
    print('Date of the last quarter =', d_LQ, '\n', JDE_LQ)
    print("\nExample with today's date")
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    periode = str(day) + '/' + str(month) + '/' + str(year)
    (JDE_NM, JDE_FQ, JDE_FM, JDE_LQ), (d_NM, d_FQ, d_FM, d_LQ) = lunar_phase(day, month, year)
    print('Date  =', str(day), '/', str(month) + '/' + str(year))
    print('Date of the new moon =', d_NM, '\n', JDE_NM)
    print('Date of the first quarter =', d_FQ, '\n', JDE_FQ)
    print('Date of the full moon =', d_FM, '\n', JDE_FM)
    print('Date of the last quarter =', d_LQ, '\n', JDE_LQ)