# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/postlund/pyatv_dev/pyatv/pyatv/net.py
# Compiled at: 2019-10-02 04:59:55
# Size of source mod 2**32: 2431 bytes
"""Methods used to make GET/POST requests."""
import logging, binascii
_LOGGER = logging.getLogger(__name__)
DEFAULT_TIMEOUT = 10.0

class HttpSession:
    __doc__ = 'This class simplifies GET/POST requests.'

    def __init__(self, client_session, base_url):
        """Initialize a new HttpSession."""
        self._session = client_session
        self.base_url = base_url

    async def get_data(self, path, headers=None, timeout=None):
        """Perform a GET request."""
        url = self.base_url + path
        _LOGGER.debug('GET URL: %s', url)
        resp = None
        try:
            try:
                resp = await self._session.get(url,
                  headers=headers, timeout=(DEFAULT_TIMEOUT if timeout is None else timeout))
                if resp.content_length is not None:
                    resp_data = await resp.read()
                else:
                    resp_data = None
                return (
                 resp_data, resp.status)
            except Exception as ex:
                if resp is not None:
                    resp.close()
                raise ex

        finally:
            if resp is not None:
                await resp.release()

    async def post_data(self, path, data=None, headers=None, timeout=None):
        """Perform a POST request."""
        url = self.base_url + path
        _LOGGER.debug('POST URL: %s', url)
        self._log_data(data, False)
        resp = None
        try:
            try:
                resp = await self._session.post(url,
                  headers=headers, data=data, timeout=(DEFAULT_TIMEOUT if timeout is None else timeout))
                if resp.content_length is not None:
                    resp_data = await resp.read()
                else:
                    resp_data = None
                self._log_data(resp_data, True)
                return (resp_data, resp.status)
            except Exception as ex:
                if resp is not None:
                    resp.close()
                raise ex

        finally:
            if resp is not None:
                await resp.release()

    @staticmethod
    def _log_data(data, is_recv):
        if data:
            if _LOGGER.isEnabledFor(logging.DEBUG):
                output = data[0:128]
                _LOGGER.debug('%s Data[%d]: %s%s', '<-' if is_recv else '->', len(data), binascii.hexlify(output), '...' if len(output) != len(data) else '')