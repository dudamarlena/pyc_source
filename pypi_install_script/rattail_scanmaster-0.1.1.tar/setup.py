#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2014 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU Affero General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option)
#  any later version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for
#  more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################


import sys
import os.path
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))
execfile(os.path.join(here, u'rattail_scanmaster', u'_version.py'))
with open(os.path.join(here, u'README.rst'), u'rt') as f:
    README = f.read().decode(u'utf_8')


requires = [
    #
    # Version numbers within comments below have specific meanings.
    # Basically the 'low' value is a "soft low," and 'high' a "soft high."
    # In other words:
    #
    # If either a 'low' or 'high' value exists, the primary point to be
    # made about the value is that it represents the most current (stable)
    # version available for the package (assuming typical public access
    # methods) whenever this project was started and/or documented.
    # Therefore:
    #
    # If a 'low' version is present, you should know that attempts to use
    # versions of the package significantly older than the 'low' version
    # may not yield happy results.  (A "hard" high limit may or may not be
    # indicated by a true version requirement.)
    #
    # Similarly, if a 'high' version is present, and especially if this
    # project has laid dormant for a while, you may need to refactor a bit
    # when attempting to support a more recent version of the package.  (A
    # "hard" low limit should be indicated by a true version requirement
    # when a 'high' version is present.)
    #
    # In any case, developers and other users are encouraged to play
    # outside the lines with regard to these soft limits.  If bugs are
    # encountered then they should be filed as such.
    #
    # package                           # low                   high

    u'rattail',                         #                       0.3.27
    ]


setup(
    name = u"rattail_scanmaster",
    version = __version__,
    author = u"Lance Edgar",
    author_email = u"lance@edbob.org",
    url = u"http://rattailproject.org/",
    license = u"GNU GPL v3",
    description = u"Retail Software Framework",
    long_description = README,

    classifiers = [
        u'Development Status :: 3 - Alpha',
        u'Environment :: Console',
        u'Environment :: Win32 (MS Windows)',
        u'Intended Audience :: Developers',
        u'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        u'Natural Language :: English',
        u'Operating System :: OS Independent',
        u'Programming Language :: Python',
        u'Programming Language :: Python :: 2.6',
        u'Programming Language :: Python :: 2.7',
        u'Topic :: Office/Business',
        u'Topic :: Software Development :: Libraries :: Python Modules',
        ],

    install_requires = requires,
    tests_require = requires + [u'nose', u'coverage', u'fixture', u'mock'],
    test_suite = u'nose.collector',
    packages = find_packages(exclude=[u'tests.*', u'tests']),
    )
