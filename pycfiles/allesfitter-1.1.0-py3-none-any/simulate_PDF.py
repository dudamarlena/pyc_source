# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mx/Dropbox (MIT)/Science/Code/allesfitter/priors/simulate_PDF.py
# Compiled at: 2018-11-09 15:03:04
"""
Created on Tue Oct  2 10:54:58 2018

@author:
Dr. Maximilian N. Guenther
MIT Kavli Institute for Astrophysics and Space Research, 
Massachusetts Institute of Technology,
77 Massachusetts Avenue,
Cambridge, MA 02109, 
USA
Email: maxgue@mit.edu
Web: www.mnguenther.com
"""
import seaborn as sns
sns.set(context='paper', style='ticks', palette='deep', font='sans-serif', font_scale=1.5, color_codes=True)
sns.set_style({'xtick.direction': 'in', 'ytick.direction': 'in'})
sns.set_context(rc={'lines.markeredgewidth': 1})
import numpy as np, matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.stats import skewnorm
np.random.seed(42)

def simulate_PDF(median, lower_err, upper_err, size=1, plot=True):
    """
    Simulates a draw of posterior samples from a value and asymmetric errorbars
    by assuming the underlying distribution is a skewed normal distribution.
    
    Developed to estimate PDFs from literature exoplanet parameters that did not report their MCMC chains.
    
    Inputs:
    -------
    median : float
        the median value that was reported
    lower_err : float
        the lower errorbar that was reported
    upper_err : float
        the upper errorbar that was reported
    size : int
        the number of samples to be drawn
        
    Returns:
    --------
    samples : array of float
        the samples drawn from the simulated skrewed normal distribution
    """
    sigma, omega, alpha = calculate_skewed_normal_params(median, lower_err, upper_err)
    samples = skewnorm.rvs(alpha, loc=sigma, scale=omega, size=size)
    if plot == False:
        return samples
    else:
        lower_err = np.abs(lower_err)
        upper_err = np.abs(upper_err)
        x = np.arange(median - 4 * lower_err, median + 4 * upper_err, 0.01)
        fig = plt.figure()
        for i in range(3):
            plt.axvline([median - lower_err, median, median + upper_err][i], color='k', lw=2)

        plt.plot(x, skewnorm.pdf(x, alpha, loc=sigma, scale=omega), 'r-', lw=2)
        fit_percentiles = skewnorm.ppf([0.16, 0.5, 0.84], alpha, loc=sigma, scale=omega)
        for i in range(3):
            plt.axvline(fit_percentiles[i], color='r', ls='--', lw=2)

        plt.hist(samples, density=True, color='red', alpha=0.5)
        return (samples, fig)


def calculate_skewed_normal_params(median, lower_err, upper_err):
    """
    Fits a screwed normal distribution via its CDF to the [16,50,84]-percentiles
    
    Inputs:
    -------
    median : float
        the median value that was reported
    lower_err : float
        the lower errorbar that was reported
    upper_err : float
        the upper errorbar that was reported
    size : int
        the number of samples to be drawn
        
    Returns:
    --------
    sigma : float
        the mean of the fitted skewed normal distribution
    omega : float
        the std of the fitted skewed normal distribution
    alpha : float
        the skewness parameter
    """
    lower_err = np.abs(lower_err)
    upper_err = np.abs(upper_err)

    def fake_lnlike(p):
        sigma, omega, alpha = p
        eq1 = skewnorm.ppf(0.5, alpha, loc=sigma, scale=omega) - median
        eq2 = skewnorm.ppf(0.16, alpha, loc=sigma, scale=omega) - (median - lower_err)
        eq3 = skewnorm.ppf(0.84, alpha, loc=sigma, scale=omega) - (median + upper_err)
        fake_lnlike = np.log(eq1 ** 2 + eq2 ** 2 + eq3 ** 2)
        return fake_lnlike

    std = np.mean([lower_err, upper_err])
    initial_guess = (median, std, 0)
    sol = minimize(fake_lnlike, initial_guess, bounds=[(None, None), (0, None), (None, None)])
    sigma, omega, alpha = sol.x
    return (
     sigma, omega, alpha)


if __name__ == '__main__':
    median, lower_err, upper_err = (84.3, -2.0, 1.3)
    samples, fig = simulate_posterior_samples(median, lower_err, upper_err, size=1, plot=True)
    print np.percentile(samples, [16, 50, 84])