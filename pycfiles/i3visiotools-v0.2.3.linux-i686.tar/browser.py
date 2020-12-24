# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/i3visiotools/browser.py
# Compiled at: 2014-12-25 06:48:18
import mechanize, cookielib, logging, random

class Browser:
    """ 
                Utility used to code a Browser.
        """

    def __init__(self):
        """ 
                        Recovering an instance of a new Browser.
                """
        self.br = mechanize.Browser()
        self.cj = cookielib.LWPCookieJar()
        self.br.set_cookiejar(self.cj)
        self.br.set_handle_equiv(True)
        self.br.set_handle_gzip(False)
        self.br.set_handle_redirect(True)
        self.br.set_handle_referer(False)
        self.br.set_handle_robots(False)
        self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        self.userAgents = self._getUserAgents()
        self.proxies = self._getProxies()

    def _getUserAgents(self):
        """ 
                        This method will be overwritten. Check for more user agents: 
                                http://www.useragentstring.com/pages/useragentstring.php
                        [TO-DO]
                                Recovers the list of User agents from a file. One User-Agent per line.
                        
                """
        return [
         'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0']

    def _getProxies(self):
        """ 
                        Recovers the list of proxies from a file. Structure is as follows:
                                <protocol>;<url:port>;[<user>;<password>;]
                        Example:
                        This method will be overwritten.
                """
        return []

    def recoverURL(self, url):
        """ 
                        Public method to recover a resource.
                                url
                                Platform
                        
                        Returns:
                                Returns a resource that has to be read, for instance, with html = self.br.read()
                """
        logger = logging.getLogger('i3visiotools')
        self.setUserAgent()
        if '.onion' in url:
            try:
                pass
            except:
                pass

            url = url.replace('.onion', '.tor2web.org')
        logger.debug('Retrieving the resource: ' + url)
        recurso = self.br.open(url)
        logger.debug('Reading html code from: ' + url)
        html = recurso.read()
        return html

    def setNewPassword(self, url, username, password):
        """ 
                        Public method to manually set the credentials for a url in the browser.
                """
        self.br.add_password(url, username, password)

    def setProxy(self, protocol, proxy, username=None, password=None):
        """ 
                        Public method to set a proxy for the browser.
                """
        self.br.set_proxies({protocol: proxy})
        if username:
            self.br.add_proxy_password(username, password)

    def setUserAgent(self, uA=None):
        """
                        This method will be called whenever a new query will be executed. 
                        
                        :param uA:      Any User Agent that was needed to be inserted. This parameter is optional.
                        
                        :return:        Returns True if a User Agent was inserted and False if no User Agent could be inserted.
                """
        logger = logging.getLogger('i3visiotools')
        if not uA:
            if self.userAgents:
                logger = logging.debug('Selecting a new random User Agent.')
                uA = random.choice(self.userAgents)
            else:
                logger = logging.debug('No user agent was inserted.')
                return False
        self.br.addheaders = [
         (
          'User-agent', uA)]
        return True