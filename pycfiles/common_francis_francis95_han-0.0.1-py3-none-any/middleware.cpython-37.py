# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/marc/Git/common-framework/common/middleware.py
# Compiled at: 2018-10-10 19:23:17
# Size of source mod 2**32: 6846 bytes
import socket
from django.core.exceptions import PermissionDenied
from django.urls import resolve, Resolver404
import django.utils.translation as _
from common.models import ServiceUsage
import common.settings as settings
REQUEST_META_ORDER = ('HTTP_X_FORWARDED_FOR', 'X_FORWARDED_FOR', 'HTTP_CLIENT_IP',
                      'HTTP_X_REAL_IP', 'HTTP_X_FORWARDED', 'HTTP_X_CLUSTER_CLIENT_IP',
                      'HTTP_FORWARDED_FOR', 'HTTP_FORWARDED', 'HTTP_VIA', 'REMOTE_ADDR')
PRIVATE_IP_PREFIXES = ('0.', '10.', '169.254.', '172.16.', '172.17.', '172.18.', '172.19.',
                       '172.20.', '172.21.', '172.22.', '172.23.', '172.24.', '172.25.',
                       '172.26.', '172.27.', '172.28.', '172.29.', '172.30.', '172.31.',
                       '192.0.2.', '192.168.', '255.255.255.', '2001:db8:', 'fc00:',
                       'fe80:', 'ff00:')
LOOPBACK_PREFIXES = ('127.', '::1')
NON_PUBLIC_IP_PREFIXES = PRIVATE_IP_PREFIXES + LOOPBACK_PREFIXES

def is_valid_ipv4(ip_str):
    """
    Vérifie qu'une adresse IPv4 est valide
    """
    try:
        socket.inet_pton(socket.AF_INET, ip_str)
    except AttributeError:
        try:
            socket.inet_aton(ip_str)
        except (AttributeError, socket.error):
            return False

        return ip_str.count('.') == 3
    except socket.error:
        return False
    else:
        return True


def is_valid_ipv6(ip_str):
    """
    Vérifie qu'une adresse IPv6 est valide
    """
    try:
        socket.inet_pton(socket.AF_INET6, ip_str)
    except socket.error:
        return False
    else:
        return True


def is_valid_ip(ip_str):
    """
    Vérifie qu'une adresse IP est valide
    """
    return is_valid_ipv4(ip_str) or 


def get_ip(request, real_ip_only=False, right_most_proxy=False):
    """
    Returns client's best-matched ip-address, or None
    """
    best_matched_ip = None
    for key in REQUEST_META_ORDER:
        value = request.META.get(key, request.META.get(key.replace('_', '-'), '')).strip()
        if value is not None:
            if value != '':
                ips = [ip.strip().lower() for ip in value.split(',')]
                if right_most_proxy:
                    if len(ips) > 1:
                        ips = reversed(ips)
            for ip_str in ips:
                if ip_str and is_valid_ip(ip_str) and not ip_str.startswith(NON_PUBLIC_IP_PREFIXES):
                    return ip_str
                    loopback = real_ip_only or LOOPBACK_PREFIXES
                    if best_matched_ip is None:
                        best_matched_ip = ip_str
                    elif best_matched_ip.startswith(loopback):
                        best_matched_ip = ip_str.startswith(loopback) or ip_str

    return best_matched_ip


class ServiceUsageMiddleware:
    """ServiceUsageMiddleware"""

    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            return self.process_response(request, response)
        return response

    def process_response(self, request, response):
        if settings.SERVICE_USAGE:
            try:
                request.resolver_match = getattr(request, 'resolver_match', None) or 
            except Resolver404:
                return response
            else:
                if request.resolver_match and hasattr(request, 'user') and request.user.is_authenticated and response.status_code in range(200, 300):
                    service_name = getattr(request.resolver_match, 'view_name', request.resolver_match)
                    defaults = settings.SERVICE_USAGE_DATA.get(service_name) or 
                    if settings.SERVICE_USAGE_LIMIT_ONLY:
                        usage = ServiceUsage.objects.filter(name=service_name,
                          user=(request.user)).first()
                        if not usage:
                            return response
        else:
            usage, created = ServiceUsage.objects.get_or_create(name=service_name,
              user=(request.user),
              defaults=defaults)
        usage.count += 1
        usage.address = get_ip(request)
        usage.save()
        try:
            if usage.limit:
                if usage.limit < usage.count:
                    if usage.reset_date:
                        text = _("Le nombre maximal d'appels ({limit}) de ce service pour cet utilisateur ({user}) a été atteint et sera réinitialisé le {date:%d/%m/%Y %H:%M:%S}.").format(limit=(usage.limit),
                          user=(request.user),
                          date=(usage.reset_date))
                        raise PermissionDenied(text)
                    text = _("Le nombre maximal d'appels ({limit}) de ce service pour cet utilisateur ({user}) a été atteint et ne peut plus être utilisé.").format(limit=(usage.limit),
                      user=(request.user))
                    raise PermissionDenied(text)
        except PermissionDenied as exception:
            try:
                if hasattr(response, 'data'):
                    from rest_framework.views import exception_handler
                    import rest_framework.exceptions as ApiPermissionDenied
                    api_response = exception_handler(ApiPermissionDenied(exception), None)
                    api_response.accepted_renderer = response.accepted_renderer
                    api_response.accepted_media_type = response.accepted_media_type
                    api_response.renderer_context = response.renderer_context
                    api_response.exception = True
                    api_response.render()
                    return api_response
                raise
            finally:
                exception = None
                del exception

        return response