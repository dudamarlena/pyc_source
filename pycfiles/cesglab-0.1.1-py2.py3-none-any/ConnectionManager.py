# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.6/dist-packages/pymycraaawler/ConnectionManager.py
# Compiled at: 2011-12-08 21:26:16
__doc__ = ' \n     Copyright 2011 Cesar Valiente Gordo\n \n     This file is part of MSWL - Development and Tools WebCrawler exercise.\n\n    This file is free software: you can redistribute it and/or modify\n    it under the terms of the GNU General Public License as published by\n    the Free Software Foundation, either version 3 of the License, or\n    (at your option) any later version.\n\n    This file is distributed in the hope that it will be useful,\n    but WITHOUT ANY WARRANTY; without even the implied warranty of\n    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n    GNU General Public License for more details.\n\n    You should have received a copy of the GNU General Public License\n    along with this file.  If not, see <http://www.gnu.org/licenses/>.\n'
from Settings import Settings
import urllib2
from urlparse import urlparse

class ConnectionManager:
    """ Created on 05/11/2011
    
    @author: Cesar Valiente Gordo
    @mail: cesar.valiente@gmail.com
    
    This class has all methods to use in the connection with servers and urls """
    _TIMEOUT = 5

    def readRemoteUrl(self, url):
        """This function reads the website passed by parameter and sets the 
        rawCode parameter with the html code in brute """
        _opener = urllib2.build_opener()
        _opener.addheaders = [(Settings.USER_AGENT_TAG, Settings.USER_AGENT_CONTENT)]
        try:
            rawCode = _opener.open(url, None, self._TIMEOUT).read()
            return rawCode
        except BaseException:
            return
        except Exception:
            return

        return

    def parseUrl(self, url):
        """ Parses the complete url and returns itself parsed """
        urlComponents = urlparse(url)
        return urlComponents

    def getHostName(self, url):
        """ Parses the complete url and returns the hostName """
        urlComponents = self.parseUrl(url)
        return urlComponents.netloc