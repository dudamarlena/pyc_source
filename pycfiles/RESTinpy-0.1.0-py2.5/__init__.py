# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/RESTinpy/__init__.py
# Compiled at: 2009-04-22 07:30:36
"""

A Python library to ease the publication of REST-style web services in Django applications, specially (but not exclusively) those using the Django Model framework.

Acknowledgement
===============

@summary: Python interface to SPARQL services FIXME
@authors: U{Diego Berrueta<http://berrueta.net>, Jana Álvarez, U{Sergio Fernández<http://www.wikier.org>}, U{Carlos Tejo Alonso<http://dayures.net>}
@organization: U{Foundation CTIC<http://www.fundacionctic.org/>}.
@license: U{GNU Lesser General Public License (LGPL), Version 3<href="http://www.gnu.org/licenses/lgpl-3.0.html">}
@requires: U{simplejson<http://cheeseshop.python.org/pypi/simplejson>} package.
@requires: U{mimeparse<http://code.google.com/p/mimeparse/>} package.
"""
__version__ = '0.1.0'
__authors__ = 'Diego Berrueta, Jana Álvarez, Sergio Fernández, Carlos Tejo Alonso'
__license__ = 'GNU Lesser General Public License (LGPL), Version 3'
__contact__ = 'rest-in-py-devel@lists.sourceforge.net'
__date__ = '2009-03-26'
__agent__ = 'RESTinpy %s (http://rest-in-py.sourceforge.net/)' % __version__
import sys, logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(pathname)s:%(lineno)s %(levelname)s: %(message)s', stream=sys.stdout)
logging.info('Logger configured for RESTinpy')