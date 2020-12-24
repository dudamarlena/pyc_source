# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/pynfold/version.py
# Compiled at: 2018-05-17 06:58:54
from __future__ import absolute_import, division, print_function
_version_major = 0
_version_minor = 1
_version_micro = ''
_version_extra = 'dev'
_ver = [
 _version_major, _version_minor]
if _version_micro:
    _ver.append(_version_micro)
if _version_extra:
    _ver.append(_version_extra)
__version__ = ('.').join(map(str, _ver))
CLASSIFIERS = [
 'Development Status :: 3 - Alpha',
 'Environment :: Console',
 'Intended Audience :: Science/Research',
 'License :: OSI Approved :: MIT License',
 'Operating System :: OS Independent',
 'Programming Language :: Python',
 'Topic :: Scientific/Engineering']
description = 'pynFold: implementation of various solutions to unfoldngand the inverse problem '
long_description = '\n\nPynFold\n========\npynFold (pronounced pen-fold) is a pythonic implementation of (eventually)\nmany of the RooUnfold ROOT Unfolding Framework aiming to compare unfolding\nmethods with those provided outisde of high energy physics and to increase\nto robustness of a flexible re-usable codebase.\n\nThe fbu algorithm implemented here is the fully basian unfolding method\nbased code developed by Clement Helsens, Davide Gerbaudo, and Francesco Rubbo\n\nUnfolding relates to the problem of estimating probability distributions\nin cases where no parametric form is available,\nand where the data are subject to additional random fluctuations due\nto limited resolution.\nThe same mathematics can be found under the general heading of\ninverse problems, and is also called deconvolution or unsmearing.\n\nThis type of equation is also known as the Fredholm integral of the first kind.\nThe Kernel K, acts as a smoothing matrix in the forward detector and\nwe can interpret its elements as a matrix of probabilites,\nstrictly positive between 0 and one.\nInverting the matrix (if possible) resutls in strictly non-probabilistic terms\nthat, instead of smothing, add large high frequency components due to\narbitrarily small fluctuations.\nThe goal of unfolding is to impose some knowledge about the smoothness of this\nmatrix onto the inversion to suppress such high frequency elements.\n\nThis project is currently under development.\nIf you would like to be involved please contact vincent.croft at cern.ch.\n\nLicense\n=======\n``pynfold`` is licensed under the terms of the MIT license. See the file\n"LICENSE" for information on the history of this software, terms & conditions\nfor usage, and a DISCLAIMER OF ALL WARRANTIES.\n\nAll trademarks referenced herein are property of their respective holders.\n\nCopyright (c) 2018--, Vincent Alexander Croft,\nNew York University Department of Physics and DIANA-HEP\n'
NAME = 'pynfold'
MAINTAINER = 'Vince Croft'
MAINTAINER_EMAIL = 'vincecroft@gmail.com'
DESCRIPTION = description
LONG_DESCRIPTION = long_description
URL = 'http://github.com/vincecr0ft/pynFold'
DOWNLOAD_URL = ''
LICENSE = 'MIT'
AUTHOR = 'Vince Croft'
AUTHOR_EMAIL = 'vincecroft@gmail.com'
PLATFORMS = 'OS Independent'
MAJOR = _version_major
MINOR = _version_minor
MICRO = _version_micro
VERSION = __version__
REQUIRES = ['numpy', 'matplotlib', 'pymc', 'scipy']