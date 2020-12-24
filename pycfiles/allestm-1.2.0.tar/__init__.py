# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/mx/Dropbox (MIT)/Science/Code/allesfitter/allesfitter/__init__.py
# Compiled at: 2019-01-22 16:38:51
__doc__ = '\nCreated on Fri Oct  5 14:18:20 2018\n\n@author:\nMaximilian N. Günther\nMIT Kavli Institute for Astrophysics and Space Research, \nMassachusetts Institute of Technology,\n77 Massachusetts Avenue,\nCambridge, MA 02109, \nUSA\nEmail: maxgue@mit.edu\nWeb: www.mnguenther.com\n'
from __future__ import print_function, division, absolute_import
import seaborn as sns
sns.set(context='paper', style='ticks', palette='deep', font='sans-serif', font_scale=1.5, color_codes=True)
sns.set_style({'xtick.direction': 'in', 'ytick.direction': 'in'})
sns.set_context(rc={'lines.markeredgewidth': 1})
import os
from .mcmc import mcmc_fit
from .nested_sampling import ns_fit
from .general_output import get_labels
from .nested_sampling_output import get_ns_posterior_samples, ns_output
from .mcmc_output import get_mcmc_posterior_samples, mcmc_output
from .priors import transform_priors
from .priors.estimate_noise import estimate_noise
from .postprocessing.nested_sampling_compare_logZ import ns_plot_bayes_factors
from .postprocessing.plot_violins import ns_plot_violins, mcmc_plot_violins

def GUI():
    allesfitter_path = os.path.dirname(os.path.realpath(__file__))
    os.system('jupyter notebook "' + os.path.join(allesfitter_path, 'GUI.ipynb') + '"')


__version__ = '0.3.0'