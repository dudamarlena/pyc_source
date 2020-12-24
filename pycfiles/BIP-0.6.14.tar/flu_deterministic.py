# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: flu_deterministic.py
# Compiled at: 2010-03-18 08:29:37
"""
Parameter estimation and series forcasting based on simulated data with moving window.
Deterministic model
"""
from BIP.Bayes.Melding import FitModel
from scipy.integrate import odeint
import scipy.stats as st, numpy as np
beta = 1
tau = 0.2
tf = 36
y0 = [0.999, 0.001, 0.0]

def model(theta):
    beta = theta[0]

    def sir(y, t):
        """ODE model"""
        (S, I, R) = y
        return [-beta * I * S,
         beta * I * S - tau * I,
         tau * I]

    y = odeint(sir, inits, np.arange(0, tf, 1))
    return y


F = FitModel(300, model, y0, tf, ['beta'], ['S', 'I', 'R'], wl=36, nw=1, verbose=False, burnin=100)
F.set_priors(tdists=[st.norm], tpars=[(1.1, 0.2)], tlims=[(0.5, 1.5)], pdists=[
 st.uniform] * 3, ppars=[(0, 0.1), (0, 0.1), (0.8, 0.2)], plims=[(0, 1)] * 3)
d = model([1.0])
noise = st.norm(0, 0.01).rvs(36)
dt = {'I': d[:, 1] + noise}
F.run(dt, 'MCMC', likvar=0.01, pool=True, monitor=[])