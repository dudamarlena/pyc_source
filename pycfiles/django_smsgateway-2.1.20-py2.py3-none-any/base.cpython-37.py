# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tim/unleashed/django-smsgateway/smsgateway/backends/base.py
# Compiled at: 2019-04-19 04:31:39
# Size of source mod 2**32: 6083 bytes
from __future__ import absolute_import
from datetime import datetime
from logging import getLogger
from re import sub
from six import iteritems
from six.moves.urllib.request import urlopen
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from smsgateway.enums import DIRECTION_OUTBOUND
from smsgateway.models import SMS
from smsgateway.sms import SMSRequest
from smsgateway.utils import is_pre_django2
if is_pre_django2():
    from django.core.urlresolvers import get_callable
else:
    from django.urls import get_callable
logger = getLogger(__name__)
try:
    all_hooks = settings.SMSGATEWAY_HOOK
except:
    raise ImproperlyConfigured('No SMSGATEWAY_HOOK defined.')

class SMSBackend(object):

    def send(self, sms_request, account_dict):
        """
        Send an SMS message to one or more recipients, and create entries in the
        SMS table for each successful attempt.
        """
        capacity = self.get_url_capacity()
        sender = '[{}]'.format(self.get_slug()) if not sms_request.signature else sms_request.signature
        reference = self.get_send_reference(sms_request)
        all_succeeded = True
        requests = []
        while len(sms_request.to) > 0:
            requests.append(SMSRequest((sms_request.to[:capacity]),
              (sms_request.msg),
              (sms_request.signature),
              reliable=(sms_request.reliable),
              reference=reference))
            del sms_request.to[:capacity]

        for request in requests:
            url = self.get_send_url(request, account_dict)
            result = ''
            if url is not None:
                try:
                    sock = urlopen(url)
                    result = sock.read()
                    sock.close()
                except:
                    return False

                if not self.validate_send_result(result):
                    all_succeeded = False
            else:
                for dest in request.to:
                    SMS.objects.create(sender=sender,
                      content=(sms_request.msg),
                      to=dest,
                      backend=(self.get_slug()),
                      direction=DIRECTION_OUTBOUND,
                      gateway_ref=(self.get_gateway_ref(reference, result)))

        return all_succeeded

    def get_send_url(self, sms_request, account_dict):
        """
        Returns the url to call to send text messages.
        """
        raise NotImplementedError

    def validate_send_result(self, result):
        """
        Returns whether sending an sms was successful.
        """
        raise NotImplementedError

    def handle_incoming(self, request, reply_using=None):
        """
        Django view to receive incoming SMSes
        """
        raise NotImplementedError

    def get_url_capacity(self):
        """
        Returns the number of text messages one call to the url can handle at once.
        """
        raise NotImplementedError

    def get_slug(self):
        """
        A unique short identifier for the SMS gateway provider.
        """
        raise NotImplementedError

    def get_send_reference(self, sms_request):
        """
        Generate a reference for the send sms
        """
        return datetime.now().strftime('%Y%m%d%H%M%S') + ''.join(sms_request.to[:1])

    def get_gateway_ref(self, reference, result=None):
        """
        Retrieve the gateway_ref, defaults to `reference`
        """
        return reference

    def _find_callable(self, content, hooks):
        """
        Parse the content of an sms according, and try to match it with a callable function defined in the settings.

        This function calls itself to dig through the hooks, because they can have an arbitrary depth.

        :param str content: the content of the sms to parse
        :param dict hooks: the hooks to match
        :returns str or None: the name of the function to call, or None if no function was matched
        """
        matched = False
        for keyword, hook in iteritems(hooks):
            if content.startswith(keyword + ' ') or content == keyword:
                matched = True
                break

        if not matched:
            if '*' in hooks:
                hook = hooks['*']
                matched = True
        if matched:
            remaining_content = content.split(' ', 1)[1] if ' ' in content else ''
            if isinstance(hook, dict):
                return self._find_callable(remaining_content, hook)
            return hook

    def process_incoming(self, request, sms):
        """
        Process an incoming SMS message and call the correct hook.

        :param Request request: the request we're handling. Passed to the handler
        :param SMS sms: the sms we're processing
        :returns: the result of the callable function, or None if nothing was called
        """
        sms.save()
        content = sms.content.upper().strip()
        content = sub('\\s+', ' ', content)
        callable_name = self._find_callable(content, all_hooks)
        if not callable_name:
            if hasattr(settings, 'SMSGATEWAY_FALLBACK_HOOK'):
                callable_name = settings.SMSGATEWAY_FALLBACK_HOOK
        else:
            return callable_name or None
        callable_function = get_callable(callable_name)
        return callable_function(request, sms)