# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/macroeco/models/_distributions_docstrings.py
# Compiled at: 2015-10-07 18:42:13
docheaders = {'methods': '\nMethods\n-------\n', 'parameters': '\nParameters\n---------\n', 
   'notes': '\nNotes\n-----\n', 
   'examples': '\nExamples\n--------\n'}
_doc_rvs = 'rvs(%(shapes)s, loc=0, scale=1, size=1)\n    Random variates.\n'
_doc_pdf = 'pdf(x, %(shapes)s, loc=0, scale=1)\n    Probability density function.\n'
_doc_logpdf = 'logpdf(x, %(shapes)s, loc=0, scale=1)\n    Log of the probability density function.\n'
_doc_pmf = 'pmf(x, %(shapes)s, loc=0, scale=1)\n    Probability mass function.\n'
_doc_logpmf = 'logpmf(x, %(shapes)s, loc=0, scale=1)\n    Log of the probability mass function.\n'
_doc_cdf = 'cdf(x, %(shapes)s, loc=0, scale=1)\n    Cumulative density function.\n'
_doc_logcdf = 'logcdf(x, %(shapes)s, loc=0, scale=1)\n    Log of the cumulative density function.\n'
_doc_sf = 'sf(x, %(shapes)s, loc=0, scale=1)\n    Survival function (1-cdf --- sometimes more accurate).\n'
_doc_logsf = 'logsf(x, %(shapes)s, loc=0, scale=1)\n    Log of the survival function.\n'
_doc_ppf = 'ppf(q, %(shapes)s, loc=0, scale=1)\n    Percent point function (inverse of cdf --- percentiles).\n'
_doc_isf = 'isf(q, %(shapes)s, loc=0, scale=1)\n    Inverse survival function (inverse of sf).\n'
_doc_moment = 'moment(n, %(shapes)s, loc=0, scale=1)\n    Non-central moment of order n\n'
_doc_stats = "stats(%(shapes)s, loc=0, scale=1, moments='mv')\n    Mean('m'), variance('v'), skew('s'), and/or kurtosis('k').\n"
_doc_entropy = 'entropy(%(shapes)s, loc=0, scale=1)\n    (Differential) entropy of the RV.\n'
_doc_fit = 'fit(data, %(shapes)s, loc=0, scale=1)\n    Parameter estimates for generic data.\n'
_doc_expect = 'expect(func, %(shapes)s, loc=0, scale=1, lb=None, ub=None, conditional=False, **kwds)\n    Expected value of a function (of one argument) with respect to the distribution.\n'
_doc_expect_discrete = 'expect(func, %(shapes)s, loc=0, lb=None, ub=None, conditional=False)\n    Expected value of a function (of one argument) with respect to the distribution.\n'
_doc_median = 'median(%(shapes)s, loc=0, scale=1)\n    Median of the distribution.\n'
_doc_mean = 'mean(%(shapes)s, loc=0, scale=1)\n    Mean of the distribution.\n'
_doc_var = 'var(%(shapes)s, loc=0, scale=1)\n    Variance of the distribution.\n'
_doc_std = 'std(%(shapes)s, loc=0, scale=1)\n    Standard deviation of the distribution.\n'
_doc_interval = 'interval(alpha, %(shapes)s, loc=0, scale=1)\n    Endpoints of the range that contains alpha percent of the distribution\n'
_doc_allmethods = ('').join([docheaders['methods'], _doc_rvs, _doc_pdf,
 _doc_logpdf, _doc_cdf, _doc_logcdf, _doc_sf,
 _doc_logsf, _doc_ppf, _doc_isf, _doc_moment,
 _doc_stats, _doc_entropy, _doc_fit,
 _doc_expect, _doc_median,
 _doc_mean, _doc_var, _doc_std, _doc_interval])
_doc_default_callparams = "\nParameters\n----------\nx : array_like\n    quantiles\nq : array_like\n    lower or upper tail probability\n%(shapes)s : array_like\n    shape parameters\nloc : array_like, optional\n    location parameter (default=0)\nscale : array_like, optional\n    scale parameter (default=1)\nsize : int or tuple of ints, optional\n    shape of random variates (default computed from input arguments )\nmoments : str, optional\n    composed of letters ['mvsk'] specifying which moments to compute where\n    'm' = mean, 'v' = variance, 's' = (Fisher's) skew and\n    'k' = (Fisher's) kurtosis. (default='mv')\n"
_doc_default_longsummary = 'Continuous random variables are defined from a standard form and may\nrequire some shape parameters to complete its specification.  Any\noptional keyword parameters can be passed to the methods of the RV\nobject as given below:\n'
_doc_default_frozen_note = '\nAlternatively, the object may be called (as a function) to fix the shape,\nlocation, and scale parameters returning a "frozen" continuous RV object:\n\nrv = %(name)s(%(shapes)s, loc=0, scale=1)\n    - Frozen RV object with the same methods but holding the given shape,\n      location, and scale fixed.\n'
_doc_default_example = "Examples\n--------\n>>> from scipy.stats import %(name)s\n>>> import matplotlib.pyplot as plt\n>>> fig, ax = plt.subplots(1, 1)\n\nCalculate a few first moments:\n\n%(set_vals_stmt)s\n>>> mean, var, skew, kurt = %(name)s.stats(%(shapes)s, moments='mvsk')\n\nDisplay the probability density function (``pdf``):\n\n>>> x = np.linspace(%(name)s.ppf(0.01, %(shapes)s),\n...               %(name)s.ppf(0.99, %(shapes)s), 100)\n>>> ax.plot(x, %(name)s.pdf(x, %(shapes)s),\n...          'r-', lw=5, alpha=0.6, label='%(name)s pdf')\n\nAlternatively, freeze the distribution and display the frozen pdf:\n\n>>> rv = %(name)s(%(shapes)s)\n>>> ax.plot(x, rv.pdf(x), 'k-', lw=2, label='frozen pdf')\n\nCheck accuracy of ``cdf`` and ``ppf``:\n\n>>> vals = %(name)s.ppf([0.001, 0.5, 0.999], %(shapes)s)\n>>> np.allclose([0.001, 0.5, 0.999], %(name)s.cdf(vals, %(shapes)s))\nTrue\n\nGenerate random numbers:\n\n>>> r = %(name)s.rvs(%(shapes)s, size=1000)\n\nAnd compare the histogram:\n\n>>> ax.hist(r, normed=True, histtype='stepfilled', alpha=0.2)\n>>> ax.legend(loc='best', frameon=False)\n>>> plt.show()\n"
_doc_default = ('').join([_doc_default_longsummary,
 _doc_allmethods,
 _doc_default_callparams,
 _doc_default_frozen_note,
 _doc_default_example])
_doc_default_before_notes = ('').join([_doc_default_longsummary,
 _doc_allmethods,
 _doc_default_callparams,
 _doc_default_frozen_note])
docdict = {'rvs': _doc_rvs, 
   'pdf': _doc_pdf, 
   'logpdf': _doc_logpdf, 
   'cdf': _doc_cdf, 
   'logcdf': _doc_logcdf, 
   'sf': _doc_sf, 
   'logsf': _doc_logsf, 
   'ppf': _doc_ppf, 
   'isf': _doc_isf, 
   'stats': _doc_stats, 
   'entropy': _doc_entropy, 
   'fit': _doc_fit, 
   'moment': _doc_moment, 
   'expect': _doc_expect, 
   'interval': _doc_interval, 
   'mean': _doc_mean, 
   'std': _doc_std, 
   'var': _doc_var, 
   'median': _doc_median, 
   'allmethods': _doc_allmethods, 
   'callparams': _doc_default_callparams, 
   'longsummary': _doc_default_longsummary, 
   'frozennote': _doc_default_frozen_note, 
   'example': _doc_default_example, 
   'default': _doc_default, 
   'before_notes': _doc_default_before_notes}
docdict_discrete = docdict.copy()
docdict_discrete['pmf'] = _doc_pmf
docdict_discrete['logpmf'] = _doc_logpmf
docdict_discrete['expect'] = _doc_expect_discrete
_doc_disc_methods = ['rvs', 'pmf', 'logpmf', 'cdf', 'logcdf', 'sf', 'logsf',
 'ppf', 'isf', 'stats', 'entropy', 'expect', 'median',
 'mean', 'var', 'std', 'interval']
for obj in _doc_disc_methods:
    docdict_discrete[obj] = docdict_discrete[obj].replace(', scale=1', '')

docdict_discrete.pop('pdf')
docdict_discrete.pop('logpdf')
_doc_allmethods = ('').join([ docdict_discrete[obj] for obj in _doc_disc_methods ])
docdict_discrete['allmethods'] = docheaders['methods'] + _doc_allmethods
docdict_discrete['longsummary'] = _doc_default_longsummary.replace('Continuous', 'Discrete')
_doc_default_frozen_note = '\nAlternatively, the object may be called (as a function) to fix the shape and\nlocation parameters returning a "frozen" discrete RV object:\n\nrv = %(name)s(%(shapes)s, loc=0)\n    - Frozen RV object with the same methods but holding the given shape and\n      location fixed.\n'
docdict_discrete['frozennote'] = _doc_default_frozen_note
_doc_default_discrete_example = "Examples\n--------\n>>> from scipy.stats import %(name)s\n>>> import matplotlib.pyplot as plt\n>>> fig, ax = plt.subplots(1, 1)\n\nCalculate a few first moments:\n\n%(set_vals_stmt)s\n>>> mean, var, skew, kurt = %(name)s.stats(%(shapes)s, moments='mvsk')\n\nDisplay the probability mass function (``pmf``):\n\n>>> x = np.arange(%(name)s.ppf(0.01, %(shapes)s),\n...               %(name)s.ppf(0.99, %(shapes)s))\n>>> ax.plot(x, %(name)s.pmf(x, %(shapes)s), 'bo', ms=8, label='%(name)s pmf')\n>>> ax.vlines(x, 0, %(name)s.pmf(x, %(shapes)s), colors='b', lw=5, alpha=0.5)\n\nAlternatively, freeze the distribution and display the frozen ``pmf``:\n\n>>> rv = %(name)s(%(shapes)s)\n>>> ax.vlines(x, 0, rv.pmf(x), colors='k', linestyles='-', lw=1, \n...         label='frozen pmf')\n>>> ax.legend(loc='best', frameon=False)\n>>> plt.show()\n\nCheck accuracy of ``cdf`` and ``ppf``:\n\n>>> prob = %(name)s.cdf(x, %(shapes)s)\n>>> np.allclose(x, %(name)s.ppf(prob, %(shapes)s))\nTrue\n\nGenerate random numbers:\n\n>>> r = %(name)s.rvs(%(shapes)s, size=1000)\n"
docdict_discrete['example'] = _doc_default_discrete_example
_doc_default_before_notes = ('').join([docdict_discrete['longsummary'],
 docdict_discrete['allmethods'],
 docdict_discrete['callparams'],
 docdict_discrete['frozennote']])
docdict_discrete['before_notes'] = _doc_default_before_notes
_doc_default_disc = ('').join([docdict_discrete['longsummary'],
 docdict_discrete['allmethods'],
 docdict_discrete['frozennote'],
 docdict_discrete['example']])
docdict_discrete['default'] = _doc_default_disc