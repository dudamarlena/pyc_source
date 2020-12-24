# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/opentracing_utils/libs/_requests.py
# Compiled at: 2019-02-13 08:31:21
# Size of source mod 2**32: 3648 bytes
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
import logging, re, urllib.parse as parse
try:
    import requests
except ImportError:
    pass
else:
    __requests_http_send = requests.adapters.HTTPAdapter.send
import opentracing
from opentracing import Format
from opentracing.ext import tags as ot_tags
from opentracing_utils.decorators import trace
from opentracing_utils.span import get_span_from_kwargs
from opentracing_utils.common import sanitize_url
OPERATION_NAME_PREFIX = 'http_send'
logger = logging.getLogger(__name__)

def trace_requests(default_tags=None, set_error_tag=True, mask_url_query=True, mask_url_path=False, ignore_url_patterns=None):
    """Patch requests library with OpenTracing support.

    :param default_tags: Default span tags to included with every outgoing request.
    :type default_tags: dict

    :param set_error_tag: Set error tag to span if request is not ok.
    :type set_error_tag: bool

    :param mask_url_query: Mask URL query args.
    :type mask_url_query: bool

    :param mask_url_path: Mask URL path.
    :type mask_url_path: bool

    :param ignore_url_patterns: Ignore tracing for any URL's that match entries in this list
    :type ignore_url_patterns: list
    """

    def skip_span_matcher(http_adapter_obj, request, **kwargs):
        if ignore_url_patterns is None:
            return False
        if any(re.match(p, request.url) for p in ignore_url_patterns):
            return True
        return False

    @trace(pass_span=True, tags=default_tags, skip_span=skip_span_matcher)
    def requests_send_wrapper(self, request, **kwargs):
        if ignore_url_patterns is not None and any(re.match(pattern, request.url) for pattern in ignore_url_patterns):
            return __requests_http_send(self, request, **kwargs)
        else:
            op_name = '{}_{}'.format(OPERATION_NAME_PREFIX, request.method.lower())
            k, request_span = get_span_from_kwargs(inspect_stack=False, **kwargs)
            kwargs.pop(k, None)
            components = parse.urlsplit(request.url)
            if request_span:
                request_span.set_operation_name(op_name).set_tag(ot_tags.COMPONENT, 'requests').set_tag(ot_tags.PEER_HOSTNAME, components.hostname).set_tag(ot_tags.HTTP_URL, sanitize_url(request.url, mask_url_query=mask_url_query, mask_url_path=mask_url_path)).set_tag(ot_tags.HTTP_METHOD, request.method).set_tag(ot_tags.SPAN_KIND, ot_tags.SPAN_KIND_RPC_CLIENT).set_tag('timeout', kwargs.get('timeout'))
                try:
                    carrier = {}
                    opentracing.tracer.inject(request_span.context, Format.HTTP_HEADERS, carrier)
                    request.headers.update(carrier)
                except opentracing.UnsupportedFormatException:
                    logger.error('Failed to inject span context in request!')

                resp = __requests_http_send(self, request, **kwargs)
                request_span.set_tag(ot_tags.HTTP_STATUS_CODE, resp.status_code)
                if set_error_tag and not resp.ok:
                    request_span.set_tag('error', True)
                return resp
            logger.warn('Failed to extract span during initiating request!')
            return __requests_http_send(self, request, **kwargs)

    requests.adapters.HTTPAdapter.send = requests_send_wrapper