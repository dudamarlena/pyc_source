# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/refaction/config/routing.py
# Compiled at: 2008-09-16 07:11:09
"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/

Copyright (C) 2008 Emanuel Calso <egcalso [at] gmail.com>

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

"""
from pylons import config
from routes import Mapper

def make_map():
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'], always_scan=config['debug'])
    map.connect('error/:action/:id', controller='error')
    map.connect('/login', controller='template', action='login')
    map.connect('/logout', controller='template', action='logout')
    map.connect('/restricted', controller='template', action='restricted')
    map.connect('/', controller='template', action='index')
    map.connect(':controller/:action/:id')
    map.connect('*url', controller='template', action='view')
    return map