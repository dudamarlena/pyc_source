# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wenlincms/utils/device.py
# Compiled at: 2016-01-26 14:11:49
from __future__ import unicode_literals

def device_from_request(request):
    """
    Determine's the device name from the request by first looking for an
    overridding cookie, and if not found then matching the user agent.
    Used at both the template level for choosing the template to load and
    also at the cache level as a cache key prefix.
    """
    from wenlincms.conf import settings
    try:
        user_agent = request.META[b'HTTP_USER_AGENT'].lower()
    except KeyError:
        pass
    else:
        try:
            user_agent = user_agent.decode(b'utf-8')
        except AttributeError:
            pass

    for device, ua_strings in settings.DEVICE_USER_AGENTS:
        for ua_string in ua_strings:
            if ua_string.lower() in user_agent:
                return device

    return b''


def templates_for_device(request, templates):
    """
    Given a template name (or list of them), returns the template names
    as a list, with each name prefixed with the device directory
    inserted before it's associate default in the list.
    """
    from wenlincms.conf import settings
    if not isinstance(templates, (list, tuple)):
        templates = [
         templates]
    device = device_from_request(request)
    device_templates = []
    for template in templates:
        if device:
            device_templates.append(b'%s/%s' % (device, template))
        if settings.DEVICE_DEFAULT and settings.DEVICE_DEFAULT != device:
            default = b'%s/%s' % (settings.DEVICE_DEFAULT, template)
            device_templates.append(default)
        device_templates.append(template)

    return device_templates


def hostid_from_request(request):
    from mainsys.settings import ALLOWED_HOSTS
    domain = request.META[b'HTTP_HOST'].lower()
    hostid = 1
    if domain in ALLOWED_HOSTS:
        hostid = ALLOWED_HOSTS.index(domain) + 1
    return hostid


def templates_for_host(request, templates):
    if not isinstance(templates, (list, tuple)):
        templates = [
         templates]
    host = request.META[b'HTTP_HOST'].lower()
    host_templates = []
    for template in templates:
        try:
            from mainsys.settings import SUB_HOST
            if host in SUB_HOST:
                host_templates.append(b'%s/%s' % (SUB_HOST[host], template))
        except ImportError:
            pass

        host_templates.append(template)

    return host_templates