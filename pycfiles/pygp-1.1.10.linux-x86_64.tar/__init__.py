# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pygp/__init__.py
# Compiled at: 2013-04-10 06:45:39
"""
Python package for Gaussian process regression in python
========================================================

demo_gpr.py explains how to perform basic regression tasks.
demo_gpr_robust.py shows how to apply EP for robust Gaussian process regression.

gpr.py Basic gp regression package
gpr_ep.py GP regression with EP likelihood models

covar: covariance functions
"""
import pkgutil
__all__ = []
for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    __all__.append(module_name)
    loader.find_module(module_name).load_module(module_name)

del loader
del module_name
del is_pkg