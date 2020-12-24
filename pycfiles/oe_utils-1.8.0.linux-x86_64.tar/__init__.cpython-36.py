# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/claeyswo/Envs/env_oe_utils/lib/python3.6/site-packages/oe_utils/__init__.py
# Compiled at: 2020-02-12 07:50:31
# Size of source mod 2**32: 1379 bytes
from collections import Sequence

def conditional_http_tween_factory(handler, registry):
    """Tween that adds ETag headers and enables conditional responses."""
    settings = registry.settings if hasattr(registry, 'settings') else {}
    not_cacheble_list = []
    if 'not.cachable.list' in settings:
        not_cacheble_list = settings.get('not.cachable.list').split()

    def conditional_http_tween(request):
        response = handler(request)
        if request.path not in not_cacheble_list:
            if response.last_modified is not None:
                response.conditional_response = True
            if response.etag is not None:
                response.conditional_response = True
            elif isinstance(response.app_iter, Sequence):
                if len(response.app_iter) == 1:
                    if response.body is not None:
                        response.conditional_response = True
                        response.md5_etag()
        return response

    return conditional_http_tween