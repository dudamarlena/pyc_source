# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\aggregate\__init__.py
# Compiled at: 2020-01-11 21:20:43
# Size of source mod 2**32: 1485 bytes
__docformat__ = 'restructuredtext'
__author__ = 'Stephen J. Mildenhall'
__copyright__ = 'Copyright 2018-2019, Convex Risk LLC'
__license__ = 'BSD 3-Clause New License'
__version__ = '0.7.6'
__email__ = 'steve@convexrisk.com'
__status__ = 'alpha'
from .param import hack_make_lines_from_csv
from .underwriter import Underwriter
from .port import Portfolio
from .distr import Frequency, Severity, Aggregate, CarefulInverse
from .spectral import Distortion
from .utils import get_fmts, tidy_agg_program, ft, ift, sln_fit, sgamma_fit, estimate_agg_percentile, axiter_factory, AxisManager, lognorm_lev, html_title, sensible_jump, suptitle_and_tight, insurability_triangle, read_log, MomentAggregator, MomentWrangler, xsden_to_meancv, frequency_examples, Answer, log_test, subsets
from .parser import UnderwritingLexer, UnderwritingParser
__doc__ = '\naggregate - a powerful aggregate loss modeling library for Python\n==================================================================\n\n**aggregate** is a Python package providing fast, accurate, and expressive data\nstructures designed to make working with probability distributions\neasy and intuitive. Its primary aim is to be an educational tool, allowing\nexperimentation with complex, **real world** distributions. It has applications in\ninsurance, risk management, actuarial science and related areas.\n\n\n'