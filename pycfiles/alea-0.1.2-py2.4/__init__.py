# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-ppc/egg/alea/__init__.py
# Compiled at: 2007-08-03 20:58:41
""" Random generators for games

This library provides implementations for random generators as found
in non-computer games.

Currently implemented:

* ``alea.die`` implements polyhedral dice with any set of faces, and
  allows rolling arbitrary sets of dice and optionally totalling
  numeric results

* ``alea.table`` implements look-up tables that can be associated with
  random generators to have random table entries generated directly.
"""
__version__ = '0.1.2'
__date__ = '2007-08-04'
__author_name__ = 'Ben Finney'
__author_email__ = 'ben+python@benfinney.id.au'
__author__ = '%s <%s>' % (__author_name__, __author_email__)
__copyright__ = 'Copyright © %s %s' % (__date__.split('-')[0], __author_name__)
__license__ = 'GPL'
__url__ = 'http://cheeseshop.python.org/pypi/alea/'