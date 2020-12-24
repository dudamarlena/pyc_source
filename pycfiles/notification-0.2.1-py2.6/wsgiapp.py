# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/notification/wsgiapp.py
# Compiled at: 2009-02-23 05:30:01


def filter_factory(global_conf, **local_conf):
    from notification.service import NotificationService
    return _filter_factory(NotificationService, global_conf, local_conf)


def filter_factory_mako(global_conf, **local_conf):
    from notification.mako.service import NotificationService
    return _filter_factory(NotificationService, global_conf, local_conf)


def _filter_factory(service_factory, global_conf, local_conf):
    notification_service = service_factory(**local_conf)

    def filter(app):
        return NotificationServiceApp(app, notification_service)

    return filter


class NotificationServiceApp(object):

    def __init__(self, app, service):
        self.app = app
        self.service = service

    def __call__(self, environ, start_response):
        environ['service.NotificationService'] = self.service
        return self.app(environ, start_response)