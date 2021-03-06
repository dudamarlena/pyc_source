# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/musixmatch/__init__.py
# Compiled at: 2011-07-29 04:58:23
import os
__author__ = 'Luca De Vitis <luca@monkeython.com>'
__version__ = '0.9'
__copyright__ = '2011, %s ' % __author__
__license__ = '\n   Copyright (C) %s\n\n      This program is free software: you can redistribute it and/or modify\n      it under the terms of the GNU General Public License as published by\n      the Free Software Foundation, either version 3 of the License, or\n      (at your option) any later version.\n\n      This program is distributed in the hope that it will be useful,\n      but WITHOUT ANY WARRANTY; without even the implied warranty of\n      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n      GNU General Public License for more details.\n\n      You should have received a copy of the GNU General Public License\n      along with this program.  If not, see <http://www.gnu.org/licenses/>.\n' % __copyright__
__doc__ = '\n:abstract: Python interface to Musixmatch API\n:version: %s\n:author: %s\n:organization: Monkeython\n:contact: http://www.monkeython.com\n:copyright: %s\n' % (__version__, __author__, __license__)
__docformat__ = 'restructuredtext en'
__classifiers__ = [
 'Development Status :: 4 - Beta',
 'Intended Audience :: Developers',
 'License :: OSI Approved :: GNU General Public License (GPL)',
 'Operating System :: OS Independent',
 'Topic :: Internet :: WWW/HTTP',
 'Topic :: Software Development :: Libraries']
__all__ = [
 'ws', 'api', 'base',
 'artist', 'track', 'lyrics', 'subtitle', 'album']
apikey = os.environ.get('musixmatch_apikey', None)
format = os.environ.get('musixmatch_format', 'json')