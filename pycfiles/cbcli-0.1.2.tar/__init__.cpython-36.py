# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cbayes/__init__.py
# Compiled at: 2018-01-21 23:52:53
# Size of source mod 2**32: 751 bytes
__doc__ = '\nConsistent Bayesian formulation and solution for posing \nand solving stochastic inverse problems.\n\nsample :mod:`cbayes.sample` provides data structures to store sets \nof samples and formulate inverse problems.\n\nsolve :mod:`cbayes.solve` provides various methods for solving the \nstochastic inverse problem, including accept/reject, MCMC (to add), \nand surrogate posteriors (to add).\n\npostProcess :mod:`cbayes.postProcess` provides several plotting utilities, \nsorting tools, metrics, and other functionality once the posterior is computed.\n\ndistributions :mod:`cbayes.distributions` provides methods for handling \nparameteric distributions\n'
__all__ = ['sample', 'distributions', 'solve']