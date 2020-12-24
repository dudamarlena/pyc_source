# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kursywalut/handlers/generic_handler.py
# Compiled at: 2018-12-20 11:59:26
# Size of source mod 2**32: 1558 bytes
"""Generic handler module.

It consists of GenericHandler() class, which is ihnerited by MoneyPlHandler()
class from kursywalut.handlers.moneypl_handler module. In the future, it could
be used by another handlers used to request currency data from various
websites.

"""
import logging, requests
from ..funcs.string_operations import _to_unicode
logger = logging.getLogger(__name__)

class GenericHandler(object):
    __doc__ = 'GenericHandler class.\n\n    This is main handler class. All other handlers should inherit from it.\n\n    Attributes:\n        site_mapping (dict): A dict containing website mapping.\n        page_list (list): A list of string containing responses from websites.\n        page (str): data retrieved from website.\n        url (str): URL to retrieve data from.\n\n    '

    def __init__(self, url):
        """Initialization method."""
        self.site_mapping = None
        self.page_list = None
        self.page = None
        self.url = url
        self.download_time = None
        self.parse_time = None

    def get_webpage(self):
        """get_webpage method.

        Send the request from self.site_mapping list.

        """
        logger.debug('Data retrieving...')
        try:
            page = requests.get(self.url)
            logger.debug('Done.')
            self.page = page.content
        except requests.exceptions.RequestException as error:
            msg = _to_unicode('Błąd pobrania danych ze strony {}!'.format(self.url))
            logger.error(msg + ': ' + str(error))