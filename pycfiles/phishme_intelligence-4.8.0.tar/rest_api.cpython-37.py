# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robert.mcmahon@phishme.com/development2/ise-python-libraries/intelligence/phishme_intelligence/core/rest_api.py
# Compiled at: 2020-05-04 10:30:57
# Size of source mod 2**32: 7301 bytes
from __future__ import unicode_literals, absolute_import
import logging, re, sys, time, requests
from . import metadata
USER_AGENT_BASE = 'PhishMe Intelligence'

class RestApi(object):
    __doc__ = '\n\n    '

    def __init__(self, config, product):
        """
        Initialize a RestApi object

        :param ConfigParser config: ConfigParser object
        :param str product: Name of section (integration) instantiating this object (or pm_api)
        """
        self.config = config
        self.product = product
        self.logger = logging.getLogger(__name__)
        self.version = metadata.__version__

    def connect_to_api(self, verb, url, auth=None, data=None, headers=None, params=None, proxies=None):
        """
        Method to send request the PhishMe Intelligence API and get back response

        :param str verb: Type of HTTP method (GET or POST)
        :param str url: HTTP URL to use for PhishMe Intelligence API connection
        :param tuple auth: (optional) Tuple for HTTP Basic Authentication credentials to use for PhishMe Intelligence API connection
        :param data: (optional) Dictionary or tuple values to send in body of request to PhishMe Intelligence API
        :type data: dict or tuple
        :param dict headers: (optional) HTTP headers to send with request to PhishMe Intelligence API
        :param dict params: (optional) Dictionary of query string data to send to PhishMe Intelligence API
        :param dict proxies: (optional) Dictionary of protocol and URL of proxy to use for PhishMe Intelligence API connection
        :return: Tuple of status code returned from PhishMe Intelligence API connection and JSON returned from PhishMe Intelligence API request
        :rtype: (int, str)
        """
        if self.config.getboolean('local_proxy', 'use'):
            sanitized_proxy = re.sub(pattern='https://(.*)@', repl='https://', string=(self.config.get('local_proxy', 'https')))
            sanitized_proxy = re.sub(pattern='http://(.*)@', repl='http://', string=sanitized_proxy)
            sanitized_proxy = re.sub(pattern='(.*)@', repl='', string=sanitized_proxy)
            self.logger.info('Using proxy: ' + sanitized_proxy)
        elif self.config.has_option(self.product, 'ssl_verify'):
            if self.config.getboolean(self.product, 'ssl_verify'):
                verify_value = True
            else:
                requests.packages.urllib3.disable_warnings()
                verify_value = False
            max_retries = self.config.getint('pm_api', 'max_retries')
            if headers is None:
                headers = {}
            if self.product == 'pm_api':
                headers['User-Agent'] = self._build_user_agent()
        elif self.product.startswith('custom_search_'):
            headers['User-Agent'] = self._build_user_agent(custom_product=(self.product))
        else:
            headers['User-Agent'] = USER_AGENT_BASE
        for attempt in range(max_retries):
            try:
                if verb == 'GET':
                    response = requests.get(url=url, auth=auth, data=data, headers=headers, params=params, proxies=proxies, verify=verify_value)
                else:
                    if verb == 'POST':
                        response = requests.post(url=url, auth=auth, data=data, headers=headers, params=params, proxies=proxies, verify=verify_value)
                    else:
                        if not str(response.status_code).startswith('2'):
                            self.logger.warning('API call has failed: HTTP Status: ' + str(response.status_code) + ' URL: ' + str(url) + ' Data: ' + str(data) + ' Headers: ' + str(headers) + ' Parameters: ' + str(params) + ' Proxies: ' + str(proxies) + ' Verify: ' + str(verify_value) + ' Content: ' + str(response.content))
                            continue
                return (response.status_code, response.content.decode('utf-8'))
            except requests.exceptions.RequestException as exception:
                try:
                    self.logger.error(exception)
                    time.sleep(60)
                finally:
                    exception = None
                    del exception

        else:
            self.logger.error('An error occurred. Tried to complete request ' + str(max_retries) + ' times and all failed.')
            sys.exit(1)

    def _build_user_agent(self, custom_product=None):
        """
        Create a custom user agent for communicating with the PhishMe Intelligence API.

        :param str custom_product: suser agent for custom product (if applicable)
        :return: The custom user agent
        :rtype: str
        """
        custom_user_agent = USER_AGENT_BASE
        active_integrations = []
        if custom_product is not None:
            custom_product = custom_product.replace('custom_search_', '')
            active_integrations.append(custom_product)
        else:
            for section in self.config.sections():
                if section.startswith('integration_') and self.config.getboolean(section, 'use'):
                    section = section.replace('integration_', '')
                    active_integrations.append(section)

        custom_user_agent += '/' + self.version + ' (' + ', '.join(active_integrations) + ')'
        return custom_user_agent