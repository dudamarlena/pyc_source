# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dalou/www/LECHTI/LECHTI/workon/utils/ip_address.py
# Compiled at: 2018-01-12 04:53:00
# Size of source mod 2**32: 973 bytes
PRIVATE_IPS_PREFIX = ('10.', '172.', '192.')
__all__ = [
 'get_ip_address_from_request', 'get_ip_address']

def get_ip_address_from_request(request):
    """get the client ip from the request
    """
    remote_address = request.META.get('REMOTE_ADDR')
    ip = remote_address
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        proxies = x_forwarded_for.split(',')
        while len(proxies) > 0 and proxies[0].startswith(PRIVATE_IPS_PREFIX):
            proxies.pop(0)

        if len(proxies) > 0:
            ip = proxies[0]
    return ip


get_ip_address = get_ip_address_from_request