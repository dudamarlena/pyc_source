# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /app/squad_client/core/api.py
# Compiled at: 2020-02-21 08:51:47
# Size of source mod 2**32: 2324 bytes
import requests, logging, urllib, re
url_validator_regex = re.compile('^(?:http|ftp)s?://(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\\.)+(?:[A-Z]{2,6}\\.?|[A-Z0-9-]{2,}\\.?)|localhost|\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3})(?::\\d+)?(?:/?|[/?]\\S+)$', re.IGNORECASE)
logger = logging.getLogger('api')

class ApiException(requests.exceptions.RequestException):
    pass


class SquadApi:
    url = None
    token = None
    headers = None

    @staticmethod
    def configure(url, token=None):
        if url_validator_regex.match(url) is None:
            raise ApiException('Malformed url: "%s"' % url)
        if token:
            SquadApi.token = token
            SquadApi.headers = {'Authorization': 'token %s' % token}
        SquadApi.url = url if url[(-1)] is '/' else url + '/'
        logger.debug('SquadApi: url = "%s" and token = "%s"' % (SquadApi.url, 'yes' if SquadApi.token else 'no'))

    @staticmethod
    def get(endpoint, params={}):
        if endpoint.startswith('http'):
            parsed_url = urllib.parse.urlparse(endpoint)
            tmp_url = '%s://%s/' % (parsed_url.scheme, parsed_url.netloc)
            if SquadApi.url != tmp_url:
                raise ApiException('Given url (%s) is does not match pre-configured one!' % tmp_url)
            params.update(urllib.parse.parse_qs(parsed_url.query))
            endpoint = parsed_url.path
        url = '%s%s' % (SquadApi.url, endpoint if endpoint[0] is not '/' else endpoint[1:])
        logger.debug('GET %s (%s)' % (url, params))
        try:
            response = requests.get(url=url, params=params, headers=(SquadApi.headers))
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            try:
                raise ApiException('Http Error: %s' % e)
            finally:
                e = None
                del e

        except requests.exceptions.ConnectionError as e:
            try:
                raise ApiException('Error Connecting: %s' % e)
            finally:
                e = None
                del e

        except requests.exceptions.Timeout as e:
            try:
                raise ApiException('Timeout Error: %s' % e)
            finally:
                e = None
                del e

        except requests.exceptions.RequestException as e:
            try:
                raise ApiException('OOps: Something unexpected happened while requesting the API: %s' % e)
            finally:
                e = None
                del e

        return response