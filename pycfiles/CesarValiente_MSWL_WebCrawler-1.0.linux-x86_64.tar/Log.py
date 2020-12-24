# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.6/dist-packages/pymycraaawler/Log.py
# Compiled at: 2011-12-08 21:26:16
""" 
     Copyright 2011 Cesar Valiente Gordo
 
     This file is part of MSWL - Development and Tools WebCrawler exercise.

    This file is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This file is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this file.  If not, see <http://www.gnu.org/licenses/>.
"""

class Log:
    """ Created on 04/12/2011
    
    @author: Cesar Valiente Gordo
    @mail: cesar.valiente@gmail.com
    
    This class is used to print log traces  """
    _DEBUG = True
    _CLASS_NAME = False

    def d(self, className, message):
        """ Print a log trace if the DEBUG flag is true """
        if self._DEBUG:
            if self._CLASS_NAME:
                print str(className) + '\t' + str(message)
            else:
                print str(message)