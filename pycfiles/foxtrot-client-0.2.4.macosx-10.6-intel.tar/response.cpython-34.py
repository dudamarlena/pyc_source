# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/yasyf/.virtualenvs/foxtrot-api-client/lib/python3.4/site-packages/foxtrot/response.py
# Compiled at: 2015-05-24 07:16:55
# Size of source mod 2**32: 2777 bytes
import abc, time
from .errors import APIResponseError, APITimeoutError

class FoxtrotResponse(object, metaclass=abc.ABCMeta):

    def __init__(self, endpoint, resp, api_instance):
        self.endpoint = endpoint
        self.resp = resp
        self.api_instance = api_instance

    @abc.abstractmethod
    def is_complete(self):
        """True if the server is finished processing your request."""
        raise NotImplementedError()

    @abc.abstractmethod
    def poll(self):
        """Queries the server for the status of your request, returning a FoxtrotResponse object."""
        raise NotImplementedError()

    @abc.abstractmethod
    def get_result(self):
        """Returns the result from the server, if the server is finished processing your request."""
        raise NotImplementedError()

    def poll_and_block(self, interval=1, timeout=60):
        """Blocks until the server is finished processing your request, up to a timeout limit."""
        count = 0
        instance = self
        while not instance.is_complete():
            instance = instance.poll()
            time.sleep(interval)
            count += interval
            if count >= timeout:
                raise APITimeoutError(count)
                continue

        return instance

    @staticmethod
    def response_for(endpoint, resp, api_instance):
        if resp['status'] == 'pending':
            return PendingRespose(endpoint, resp, api_instance)
        else:
            if resp['status'] == 'success':
                return SuccessResponse(endpoint, resp, api_instance)
            return ErrorResponse(endpoint, resp, api_instance)


class ErrorResponse(FoxtrotResponse):

    def __init__(self, endpoint, resp, api_instance):
        super(ErrorResponse, self).__init__(endpoint, resp, api_instance)
        self.message = resp.get('message')
        self.exception = APIResponseError(self.message)
        raise self.exception

    def is_complete(self):
        return True

    def poll(self):
        raise self.exception

    def get_result(self):
        pass

    def __repr__(self):
        return 'ErrorResponse ({})'.format(self.message)


class PendingRespose(FoxtrotResponse):

    def __init__(self, endpoint, resp, api_instance):
        super(PendingRespose, self).__init__(endpoint, resp, api_instance)
        self.txid = resp['txid']

    def is_complete(self):
        return False

    def poll(self):
        return self.api_instance.poll(self.txid)

    def get_result(self):
        pass

    def __repr__(self):
        return 'PendingRespose ({})'.format(self.txid)


class SuccessResponse(FoxtrotResponse):

    def __init__(self, endpoint, resp, api_instance):
        super(SuccessResponse, self).__init__(endpoint, resp, api_instance)
        self.txid = resp['txid']
        self._SuccessResponse__data = resp['response']

    def is_complete(self):
        return True

    def poll(self):
        return self

    def get_result(self):
        return self._SuccessResponse__data

    def __repr__(self):
        return 'SuccessResponse ({})'.format(self.txid)