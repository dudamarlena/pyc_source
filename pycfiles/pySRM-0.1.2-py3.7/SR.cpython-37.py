# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/modules/SR.py
# Compiled at: 2020-04-29 04:11:15
# Size of source mod 2**32: 6575 bytes
import numpy as np
from matplotlib import pylab as plt
import pandas as pd
import scipy.optimize as lsq
from scipy.optimize import curve_fit
import scipy.stats as spst
from scipy import integrate
from scipy.integrate import quad
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sympy import *
from RegscorePy import *
df = pd.read_csv('Mg_Cp.csv', sep=',')
experiments = sorted(df.Ref.unique())
colors = plt.cm.rainbow(np.linspace(0, 1, len(experiments)))

def integrand(y):
    return y ** 4 * np.exp(y) / (np.exp(y) - 1) ** 2


def Debye_Cp(T, *param):
    Theta_D = param[0]
    Cp_debye = []
    for i in T:
        x = i / Theta_D
        Cp_debye.append(74.826 * x ** 3 * quad(integrand, 0, 1 / x)[0])

    return Cp_debye


def Einstein_Cp(T, *param):
    Theta_E = param[0]
    Cp_EM_final = []
    Cp_Einstein = 24.942 * (Theta_E / T) ** 2.0 * (np.exp(Theta_E / T) / (np.exp(Theta_E / T) - 1) ** 2.0)
    return Cp_Einstein


def bcm_Cp(T, *param):
    beta1 = param[0]
    beta2 = param[1]
    alpha = param[2]
    gamma = param[3]
    Cp_bcm = []
    for i in T:
        if i < alpha - gamma:
            Cp_bcm.append(beta1 * i)
        elif i > alpha + gamma:
            Cp_bcm.append(beta1 * i + beta2 * (i - alpha))
        else:
            Cp_bcm.append(beta1 * i + beta2 * (i - alpha + gamma) ** 2 / (4 * gamma))

    return Cp_bcm


def RW1995_Cp(T, *param):
    Theta_E = param[0]
    a = param[1]
    b = param[2]
    Cp_RW1995 = []
    Cp_RW1995 = Einstein_Cp(T, *param) + a * T + b * T ** 2
    return Cp_RW1995


def CS_Cp(T, *param):
    Theta_E = param[0]
    a = param[1]
    b = param[2]
    Cp_CS = []
    Cp_CS = Einstein_Cp(T, *param) + a * T + b * T ** 4
    return Cp_CS


def GEPM_Cp(T, *param):
    Theta_E = param[0]
    a = param[1]
    b = param[2]
    c = param[3]
    d = param[4]
    Cp_GEPM = []
    Cp_GEPM = Einstein_Cp(T, *param) + a * T + b * T ** 2 + c * T ** 3 + d * T ** 4
    return Cp_GEPM


def Cp_SR_Debye(T, *param):
    Cp_SR_D = []
    Parameter_Debye = []
    Parameter_Debye = param[0]
    Parameter_BCM = []
    Parameter_BCM.append(param[1])
    Parameter_BCM.append(param[2])
    Parameter_BCM.append(param[3])
    Parameter_BCM.append(param[4])
    Cp_SR_De = Debye_Cp(T, Parameter_Debye)
    Cp_SR_bc = bcm_Cp(T, *Parameter_BCM)
    for i in range(len(Cp_SR_De)):
        Cp_SR_D_i = Cp_SR_De[i] + Cp_SR_bc[i]
        Cp_SR_D.append(Cp_SR_D_i)

    return Cp_SR_D


def Cp_SR_Einstein(T, *param):
    Cp_SR_E = []
    Parameter_Einstein = []
    Parameter_Einstein = param[0]
    Parameter_BCM = []
    Parameter_BCM.append(param[1])
    Parameter_BCM.append(param[2])
    Parameter_BCM.append(param[3])
    Parameter_BCM.append(param[4])
    Cp_SR_Ei = Einstein_Cp(T, Parameter_Einstein)
    Cp_SR_bc = bcm_Cp(T, *Parameter_BCM)
    for i in range(len(Cp_SR_Ei)):
        Cp_SR_E_i = Cp_SR_Ei[i] + Cp_SR_bc[i]
        Cp_SR_E.append(Cp_SR_E_i)

    return Cp_SR_E


def AIC(logLik, nparm, k=2):
    return -2 * logLik + k * (nparm + 1)


def BIC(logLik, nobs, nparm, k=2):
    return -2 * logLik + k * np.log(nobs)


def RSE(RSS, nobs, nparm, k=2):
    return sqrt(RSS / (-2 * k - 2 - nobs))


new_df = df[(df.Temp > 5)]
func = RW1995_Cp
parmNames = ['ThetaE', 'a', 'b']
initialGuess = [236.882352, -0.001703, 1.8e-05]
nparm = len(initialGuess)
popt, pcov = curve_fit(func, new_df.Temp, new_df.Cp, initialGuess)
parmEsts = popt
fvec = func(new_df.Temp, *parmEsts) - new_df.Cp
RSS = np.sum(fvec ** 2)
dof = len(new_df) - nparm
nobs = len(new_df)
MSE = RSS / dof
RMSE = np.sqrt(abs(MSE))
cov = pcov
parmSE = np.diag(np.sqrt(abs(cov)))
tvals = parmEsts / parmSE
pvals = (1 - spst.t.cdf(np.abs(tvals), dof)) * 2
s2b = RSS / nobs
logLik = -nobs / 2 * np.log(2 * np.pi) - nobs / 2 * np.log(s2b) - 1 / (2 * s2b) * RSS
fit_df = pd.DataFrame(dict(Estimate=parmEsts, StdErr=parmSE, tval=tvals, pval=pvals))
fit_df.index = parmNames
print('Non-linear least squares')
print('Model: ' + func.__name__)
print('')
print(fit_df)
print()
print('Residual Standard Error: % 5.4f' % RMSE)
print('Df: %i' % dof)
print('AIC:', AIC(logLik, nparm))
print('BIC:', BIC(logLik, nobs, nparm))
print('RSE:', RSE(RSS, nobs, nparm))