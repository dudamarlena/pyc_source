# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pygp/__init__.py
# Compiled at: 2013-04-10 06:45:39
__doc__ = '\nPython package for Gaussian process regression in python\n========================================================\n\ndemo_gpr.py explains how to perform basic regression tasks.\ndemo_gpr_robust.py shows how to apply EP for robust Gaussian process regression.\n\ngpr.py Basic gp regression package\ngpr_ep.py GP regression with EP likelihood models\n\ncovar: covariance functions\n'
import pkgutil
__all__ = []
for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    __all__.append(module_name)
    loader.find_module(module_name).load_module(module_name)

del loader
del module_name
del is_pkg