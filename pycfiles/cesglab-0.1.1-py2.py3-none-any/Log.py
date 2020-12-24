# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.6/dist-packages/pymycraaawler/Log.py
# Compiled at: 2011-12-08 21:26:16
__doc__ = ' \n     Copyright 2011 Cesar Valiente Gordo\n \n     This file is part of MSWL - Development and Tools WebCrawler exercise.\n\n    This file is free software: you can redistribute it and/or modify\n    it under the terms of the GNU General Public License as published by\n    the Free Software Foundation, either version 3 of the License, or\n    (at your option) any later version.\n\n    This file is distributed in the hope that it will be useful,\n    but WITHOUT ANY WARRANTY; without even the implied warranty of\n    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n    GNU General Public License for more details.\n\n    You should have received a copy of the GNU General Public License\n    along with this file.  If not, see <http://www.gnu.org/licenses/>.\n'

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