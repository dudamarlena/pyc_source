# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alex/mgxrace/django-warmama/warmama/decorators.py
# Compiled at: 2015-05-17 01:56:10
# Size of source mod 2**32: 3721 bytes
import logging, traceback
from django.conf import settings
from django.core import exceptions as djexceptions
from django.http import JsonResponse
from functools import wraps
from ipware.ip import get_ip
from ipware.utils import is_valid_ipv4, is_valid_ipv6
from warmama import exceptions as wmexceptions
logger = logging.getLogger(__name__)

def exception_response(data):
    """Decorator factory to return JSON response on exception

    Args:
        data (dict): Default JSON data to return.
    """

    def decorator(func):

        @wraps(func)
        def wrapped(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except wmexceptions.WarmamaException as e:
                logger.info('WarmamaException: %s', e)
                return JsonResponse(data, status=e.status)
            except djexceptions.ObjectDoesNotExist as e:
                logger.info('DoesNotExist: %s', e)
                return JsonResponse(data, status=403)
            except Exception as e:
                logger.error('Unexpected exception: %s', e)
                logger.error('Traceback: %s', traceback.format_exc())
                return JsonResponse(data, status=500)

            return result

        return wrapped

    return decorator


def request_ip(func):
    """View function decorator to add ipv4 and ipv6 arguments

    Calculates the ip address from the request and passes it to the function
    as named arguments `ipv4` and `ipv6`. Accepts private ip addresses if
    `DEBUG` is `True`.
    """

    @wraps(func)
    def wrapped(request, *args, **kwargs):
        ipv4, ipv6 = kwargs.get('ipv4', ''), kwargs.get('ipv6', '')
        if ipv4 or ipv6:
            kwargs['ipv4'] = ipv4
            kwargs['ipv6'] = ipv6
            return func(request, *args, **kwargs)
        real_ip = not settings.DEBUG
        ipaddr = get_ip(request, real_ip_only=real_ip)
        if not ipaddr:
            raise wmexceptions.BadRequest('Couldnt read IP address for request')
        if is_valid_ipv4(ipaddr):
            kwargs['ipv4'], kwargs['ipv6'] = ipaddr, ''
        else:
            if is_valid_ipv6(ipaddr):
                kwargs['ipv4'], kwargs['ipv6'] = '', ipaddr
            else:
                raise wmexceptions.BadRequest('Couldnt read IP address for request')
        return func(request, *args, **kwargs)

    return wrapped


def clean_post_args(form):
    """Factory for view function decorators to Form validate POST arguments

    Uses the `form` to validate `request.POST` data and passes it as a argument
    to the wrapped function.
    """

    def decorator(func):

        @wraps(func)
        def wrapped(request, *args, **kwargs):
            if kwargs.get('POST', None):
                return func(request, *args, **kwargs)
            formdata = form(request.POST)
            if not formdata.is_valid():
                logger.info('Invalid form data: %s', formdata.errors)
                raise wmexceptions.BadRequest('Invalid arguments: {0}'.format(formdata.errors))
            kwargs['POST'] = formdata.cleaned_data
            return func(request, *args, **kwargs)

        return wrapped

    return decorator


def log_args(logger):
    """Factor for decorator to log function calls/arguments with level DEBUG"""

    def decorator(func):

        @wraps(func)
        def wrapped(*args, **kwargs):
            logger.debug('args: %s', args)
            logger.debug('kwargs: %s', kwargs)
            return func(*args, **kwargs)

        return wrapped

    return decorator