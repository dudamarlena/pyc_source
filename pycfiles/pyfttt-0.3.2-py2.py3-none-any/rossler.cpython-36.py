# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/data/rossler.py
# Compiled at: 2018-08-30 11:37:18
# Size of source mod 2**32: 1587 bytes
__doc__ = '\nO. E. Rössler, Phys. Lett. 57A, 397 (1976).\n\ndx/dt = -z - y\ndy/dt = x + ay\ndz/dt = b + z( x - c )\n\n'
import numpy as np, pandas as pd

def get_data(var, a=0.2, b=0.2, c=5.7, dt=0.01, initial_values=[
 0.001, 0.001, 0.001], iterations=5000):
    """
    Get a simple univariate time series data.

    :param var: the dataset field name to extract
    :return: numpy array
    """
    return get_dataframe(a, b, c, dt, initial_values, iterations)[var].values


def get_dataframe(a=0.2, b=0.2, c=5.7, dt=0.01, initial_values=[
 0.001, 0.001, 0.001], iterations=5000):
    """
    Return a dataframe with the multivariate Rössler Map time series (x, y, z).

    :param a: Equation coefficient. Default value: 0.2
    :param b: Equation coefficient. Default value: 0.2
    :param c: Equation coefficient. Default value: 5.7
    :param dt: Time differential for continuous time integration. Default value: 0.01
    :param initial_values: numpy array with the initial values of x,y and z. Default: [0.001, 0.001, 0.001]
    :param iterations: number of iterations. Default: 5000
    :return: Panda dataframe with the x, y and z values
    """
    x = [
     initial_values[0]]
    y = [initial_values[1]]
    z = [initial_values[2]]
    for t in np.arange(0, iterations):
        dxdt = -(y[t] + z[t])
        dydt = x[t] + a * y[t]
        dzdt = b + z[t] * x[t] - z[t] * c
        x.append(x[t] + dt * dxdt)
        y.append(y[t] + dt * dydt)
        z.append(z[t] + dt * dzdt)

    return pd.DataFrame({'x':x,  'y':y,  'z':z})