# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/typhoonae/channel/channel_service_stub.py
# Compiled at: 2010-12-12 04:36:57
"""TyphoonAE's stub version of the Channel API."""
from google.appengine.api import apiproxy_stub
from google.appengine.api.channel import channel_service_pb
from google.appengine.runtime import apiproxy_errors
import httplib, logging, random, time
WEEKDAY_ABBR = [
 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
MONTHNAME = [None, 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def rfc1123_date(ts=None):
    """Return an RFC 1123 format date string.

  Required for use in HTTP Date headers per the HTTP 1.1 spec. 'Fri, 10 Nov
  2000 16:21:09 GMT'.
  """
    if ts is None:
        ts = time.time()
    (year, month, day, hh, mm, ss, wd, y, z) = time.gmtime(ts)
    return '%s, %02d %3s %4d %02d:%02d:%02d GMT' % (WEEKDAY_ABBR[wd],
     day, MONTHNAME[month],
     year,
     hh, mm, ss)


class ChannelServiceStub(apiproxy_stub.APIProxyStub):
    """Channel service stub.

  Using a publish/subscribe service.
  """

    def __init__(self, address, log=logging.info, service_name='channel'):
        """Initializes the Channel API proxy stub.

    Args:
      address: The address of our Channel service.
      log: A logger, used for dependency injection.
      service_name: Service name expected for all calls.
    """
        apiproxy_stub.APIProxyStub.__init__(self, service_name)
        self._address = address
        self._log = log

    def _Dynamic_CreateChannel(self, request, response):
        """Implementation of channel.get_channel.

    Args:
      request: A ChannelServiceRequest.
      response: A ChannelServiceResponse
    """
        application_key = request.application_key()
        if not application_key:
            raise apiproxy_errors.ApplicationError(channel_service_pb.ChannelServiceError.INVALID_CHANNEL_KEY)
        response.set_client_id(application_key)

    def _Dynamic_SendChannelMessage(self, request, response):
        """Implementation of channel.send_message.

    Queues a message to be retrieved by the client when it polls.

    Args:
      request: A SendMessageRequest.
      response: A VoidProto.
    """
        application_key = request.application_key()
        if not request.message():
            raise apiproxy_errors.ApplicationError(channel_service_pb.ChannelServiceError.BAD_MESSAGE)
        conn = httplib.HTTPConnection(self._address)
        headers = {'Content-Type': 'text/plain', 'Last-Modified': rfc1123_date()}
        conn.request('POST', '/_ah/publish?id=%s' % application_key, request.message(), headers)
        conn.close()