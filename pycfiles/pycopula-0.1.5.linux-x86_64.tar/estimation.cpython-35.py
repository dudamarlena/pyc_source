# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/pycopula/estimation.py
# Compiled at: 2018-11-08 17:34:28
# Size of source mod 2**32: 9245 bytes
import numpy as np
from scipy.optimize import minimize, minimize_scalar

def cmle(log_lh, theta_start=0, theta_bounds=None, optimize_method='Nelder-Mead', bounded_optimize_method='SLSQP', is_scalar=False):
    """
        Computes the CMLE on a specified log-likelihood function.
        
        Parameters
        ----------
        log_lh : Function
                The log-likelihood.
        theta_start : float
                Initial value of theta in optimization algorithm.
        theta_bounds : couple
                Allowed values of theta.
        optimize_method : str
                The optimization method used in SciPy minimization when no theta_bounds was specified.
        bounded_optimize_method : str
                The optimization method used in SciPy minimization under constraints
                
        Returns
        -------
        OptimizeResult
                The optimization result returned from SciPy.
        """
    if is_scalar:
        if theta_bounds == None:
            return minimize_scalar(log_lh, method=optimize_method)
        return minimize_scalar(log_lh, bounds=theta_bounds, method='bounded', options={'maxiter': 200})
    if theta_bounds == None:
        return minimize(log_lh, theta_start, method=optimize_method)
    return minimize(log_lh, theta_start, method=bounded_optimize_method, bounds=[theta_bounds], options={'maxiter': 200})


def mle(copula, X, marginals, hyper_param, hyper_param_start=None, hyper_param_bounds=None, theta_start=[0], theta_bounds=None, optimize_method='Nelder-Mead', bounded_optimize_method='SLSQP'):
    """
        Computes the MLE on specified data.
        
        Parameters
        ----------
        copula : Copula
                The copula.
        X : numpy array (of size n * copula dimension)
                The data to fit.
        marginals : numpy array
                The marginals distributions. Use scipy.stats distributions or equivalent that requires pdf and cdf functions according to rv_continuous class from scipy.stat.
        hyper_param : numpy array
                The hyper-parameters for each marginal distribution. Use None when the hyper-parameter is unknow and must be estimated.
        hyper_param_start : numpy array
                The start value of hyper-parameters during optimization. Must be same dimension of hyper_param.
        hyper_param_bounds : numpy array
                Allowed values for each hyper-parameter.
        theta_start : numpy array
                Initial value of theta in optimization algorithm.
        theta_bounds : couple
                Allowed values of theta.
        optimize_method : str
                The optimization method used in SciPy minimization when no theta_bounds was specified.
        bounded_optimize_method : str
                The optimization method used in SciPy minimization under constraints.
                
        Returns
        -------
        optimizeResult : OptimizeResult
                The optimization result returned from SciPy.
        estimatedHyperParams : numpy array
                The estimated hyper-parameters.
        """
    hyperParams = np.asarray(hyper_param)
    hyperOptimizeParams = np.copy([dic.copy() for dic in hyperParams])
    hyperStart = np.asarray(hyper_param_start)
    n, d = X.shape
    thetaOffset = len(theta_start)
    start_vector = np.repeat(0, d + thetaOffset)
    start_vector[0:thetaOffset] = theta_start
    if hyper_param_start == None:
        start_vector[thetaOffset:] = [1.0 for i in range(d)]
    optiVector = []
    idx = 1
    for k in range(len(hyperParams)):
        for key in hyperParams[k]:
            optiVector.append(hyperParams[k][key])
            if hyper_param_start != None and hyperParams[k][key] != None:
                start_vector[idx] = hyperStart[k][key]
                idx += 1

    def log_likelihood(x):
        lh = 0
        idx = 1
        for k in range(len(hyperParams)):
            for key in hyperParams[k]:
                if hyperParams[k][key] == None:
                    hyperOptimizeParams[k][key] = x[idx]
                    idx += 1

        marginCDF = [marginals[j].cdf(np.transpose(X)[j], **hyperOptimizeParams[j]) for j in range(d)]
        marginCDF = np.transpose(marginCDF)
        if thetaOffset == 1:
            lh += sum([np.log(copula.pdf_param(marginCDF[i], x[0])) for i in range(n)])
        else:
            lh += sum([np.log(copula.pdf_param(marginCDF[i], x[0:thetaOffset])) for i in range(n)])
        print('OK')
        lh += sum([sum(np.log(marginals[j].pdf(np.transpose(X)[j], **hyperOptimizeParams[j]))) for j in range(d)])
        return lh

    optimizeResult = None
    if hyper_param_bounds == None:
        if theta_bounds == None:
            optimizeResult = minimize(lambda x: -log_likelihood(x), start_vector, method=optimize_method)
        else:
            optiBounds = np.vstack((np.array([theta_bounds]), np.tile(np.array([None, None]), [d, 1])))
            optimizeResult = minimize(lambda x: -log_likelihood(x), start_vector, method=bounded_optimize_method, bounds=optiBounds)
    else:
        if theta_bounds == None:
            optiBounds = np.vstack((np.array([None, None]), np.tile(np.array([None, None]), [d, 1])))
            optimizeResult = minimize(lambda x: -log_likelihood(x), start_vector, method=bounded_optimize_method, bounds=optiBounds)
        else:
            optiBounds = np.vstack((np.array([theta_bounds]), hyper_param_bounds))
            optimizeResult = minimize(lambda x: -log_likelihood(x), start_vector, method=bounded_optimize_method, bounds=optiBounds)
    estimatedHyperParams = hyperParams
    idx = 1
    for k in range(len(hyperParams)):
        for key in hyperParams[k]:
            if estimatedHyperParams[k][key] == None:
                estimatedHyperParams[k][key] = optimizeResult['x'][idx]
                idx += 1

    return (
     optimizeResult, estimatedHyperParams)


def ifm(copula, X, marginals, hyper_param, hyper_param_start=None, hyper_param_bounds=None, theta_start=0, theta_bounds=None, optimize_method='Nelder-Mead', bounded_optimize_method='SLSQP'):
    """
        Computes the IFM estimation on specified data.
        
        Parameters
        ----------
        copula : Copula
                The copula.
        X : numpy array (of size n * copula dimension)
                The data to fit.
        marginals : numpy array
                The marginals distributions. Use scipy.stats distributions or equivalent that requires pdf and cdf functions according to rv_continuous class from scipy.stat.
        hyper_param : numpy array
                The hyper-parameters for each marginal distribution. Use None when the hyper-parameter is unknow and must be estimated.
        hyper_param_start : numpy array
                The start value of hyper-parameters during optimization. Must be same dimension of hyper_param.
        hyper_param_bounds : numpy array
                Allowed values for each hyper-parameter.
        theta_start : float
                Initial value of theta in optimization algorithm.
        theta_bounds : couple
                Allowed values of theta.
        optimize_method : str
                The optimization method used in SciPy minimization when no theta_bounds was specified.
        bounded_optimize_method : str
                The optimization method used in SciPy minimization under constraints
                
        Returns
        -------
        optimizeResult : OptimizeResult
                The optimization result returned from SciPy.
        estimatedHyperParams : numpy array
                The estimated hyper-parameters
        """
    hyperParams = np.asarray(hyper_param)
    hyperOptimizeParams = np.copy([dic.copy() for dic in hyperParams])
    hyperStart = np.asarray(hyper_param_start)
    n, d = X.shape
    hyperEstimated = np.copy(hyperParams)
    pobs = np.zeros((d, n))
    for j in range(d):
        if hyper_param_start == None:
            start = [
             1.0]
        else:
            start = []
            for key in hyperParams[j]:
                if hyperParams[j][key] == None:
                    start.append(hyperStart[j][key])

        def uni_log_likelihood(x):
            idx = 0
            for key in hyperParams[j]:
                if hyperParams[j][key] == None:
                    hyperOptimizeParams[j][key] = x[idx]
                    idx += 1

            return sum(np.log(marginals[j].pdf(np.transpose(X)[j], **hyperOptimizeParams[j])))

        if hyper_param_bounds[j] == None:
            optiRes = minimize(lambda x: -uni_log_likelihood(x), start, method=optimize_method)['x']
        else:
            optiRes = minimize(lambda x: -uni_log_likelihood(x), start, method=bounded_optimize_method, bounds=[hyper_param_bounds[j]])['x']
        idx = 0
        for key in hyperEstimated[j]:
            if hyperEstimated[j][key] == None:
                hyperEstimated[j][key] = optiRes[idx]
                idx += 1

        pobs[j] = marginals[j].cdf(np.transpose(X)[j], **hyperEstimated[j])

    pobs = np.transpose(pobs)
    optimizeResult = None

    def log_likelihood(x):
        return sum([np.log(copula.pdf_param(pobs[i], x)) for i in range(n)])

    if theta_bounds == None:
        optimizeResult = minimize(lambda x: -log_likelihood(x), theta_start, method=optimize_method)
    else:
        optimizeResult = minimize(lambda x: -log_likelihood(x), theta_start, method=bounded_optimize_method, bounds=[theta_bounds])
    return (optimizeResult, hyperEstimated)