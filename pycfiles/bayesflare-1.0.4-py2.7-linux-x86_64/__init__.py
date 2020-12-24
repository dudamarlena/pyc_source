# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bayesflare/__init__.py
# Compiled at: 2017-04-26 11:11:14
"""
BayesFlare
==========

Provides:
   1. A number of pythonic means for handling lightcurve data from the Kepler spacecraft
   2. A set of functions for conducting analysis of the lightcurve data to find flaring events

Using the documentation
-----------------------

Documentation for pyFlare is available in the form of docstrings, and this compiled reference
guide. Further information on the methods used are covered in the paper (Pitkin et al, 2014).

The examples in the docstrings assume that `BayesFlare` has been imported as `pf`

   >>> import bayesflare as pf

Code snippets are indicated by three greater-than signs

   >>> x = 2 + 3

in common with standard usage in Python documentation.

A docstring can be read using the python interpretter's built-in function ``help``

   >>> help(pf.plot)

"""
from __future__ import absolute_import
from .data.data import Loader, Lightcurve
from .models import Model, Flare, Transit, Expdecay, Impulse, Gaussian, Step, ModelCurve
from .finder.find import SigmaThresholdMethod, OddsRatioDetector
from .noise.noise import estimate_noise_ps, estimate_noise_tv, make_noise_lightcurve, addNoise, highpass_filter_lightcurve, savitzky_golay, running_median
from .stats import *
from .stats.bayes import Bayes, ParameterEstimationGrid
from .misc.misc import nextpow2, mkdir
from .inject.inject import inject_model
from .simulate.simulate import SimLightcurve, simulate_single