# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cbayes/__init__.py
# Compiled at: 2018-01-21 23:52:53
# Size of source mod 2**32: 751 bytes
"""
Consistent Bayesian formulation and solution for posing 
and solving stochastic inverse problems.

sample :mod:`cbayes.sample` provides data structures to store sets 
of samples and formulate inverse problems.

solve :mod:`cbayes.solve` provides various methods for solving the 
stochastic inverse problem, including accept/reject, MCMC (to add), 
and surrogate posteriors (to add).

postProcess :mod:`cbayes.postProcess` provides several plotting utilities, 
sorting tools, metrics, and other functionality once the posterior is computed.

distributions :mod:`cbayes.distributions` provides methods for handling 
parameteric distributions
"""
__all__ = [
 'sample', 'distributions', 'solve']