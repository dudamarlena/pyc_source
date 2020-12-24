# -*- coding: utf-8 -*-
"""Distribute 'namedtupledefs', patched *collections.namedtuple* with default values.
This package contains the syntax release *Python3*, for *Python2* refer to *namedtupledefs2*.
"""
from __future__ import absolute_import
from __future__ import print_function

import os
import sys

import setuptools


__author__ = 'Arno-Can Uestuensoez'
__author_email__ = 'acue_sf2@sourceforge.net'
__license__ = "Artistic-License-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (C) 2019 Arno-Can Uestuensoez" \
                " @Ingenieurbuero Arno-Can Uestuensoez"
__uuid__ = "19683f50-48f2-4e1e-953f-640455e97340"

__vers__ = [0, 1, 21,]
__version__ = "%02d.%02d.%03d"%(__vers__[0],__vers__[1],__vers__[2],)


# required for various interfaces, thus just do it
_mypath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(_mypath))


_name = 'namedtupledefs'
__pkgname__ = 'namedtupledefs'
_version = "%d.%d.%d" % (__vers__[0], __vers__[1], __vers__[2],)


#
# see setup.py for remaining parameters
#
setuptools.setup(
    author=__author__,
    author_email=__author_email__,
    description="Extended 'namedtuple' by default values.",
    download_url="https://sourceforge.net/projects/namedtupledefs/files/",
    license=__license__,
    long_description=os.path.join(os.path.dirname(__file__), 'README.md'),
    name=_name,
    packages=["namedtupledefs"],
    url='https://sourceforge.net/projects/namedtupledefs/',
    version=_version,
    zip_safe=False,
)

sys.exit(0)

