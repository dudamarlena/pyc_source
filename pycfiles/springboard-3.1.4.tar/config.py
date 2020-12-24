# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/universalcore/springboard/springboard/config.py
# Compiled at: 2015-11-17 11:55:31


def includeme(config):
    config.include('springboard.auth')
    config.include('pyramid_celery')
    config.add_static_view('static', 'springboard:static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('category', '/category/{uuid}/')
    config.add_route('page', '/page/{uuid}/')
    config.add_route('search', '/search/')
    config.add_route('locale', '/locale/')
    config.add_route('locale_change', '/locale/change/')
    config.add_route('locale_matched', '/locale/{language}/')
    config.add_route('health', '/health/')
    config.add_route('flat_page', '/{slug}/')
    config.add_route('api_notify', '/api/notify/', request_method='POST')
    config.scan('.views')
    config.scan('.events')