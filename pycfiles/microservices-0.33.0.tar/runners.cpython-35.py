# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/viator/coding/code/microservices/microservices/queues/runners.py
# Compiled at: 2017-03-07 09:44:21
# Size of source mod 2**32: 719 bytes


def gevent_run(app, monkey_patch=True, start=True, debug=False, **kwargs):
    """Run your app in gevent.spawn, run simple loop if start == True

    :param app: queues.Microservice instance
    :param monkey_patch: boolean, use gevent.monkey.patch_all() for patching standard modules, default: True
    :param start: boolean, if True, server will be start (simple loop)
    :param kwargs: other params for WSGIServer(**kwargs)
    :return: server
    """
    if monkey_patch:
        from gevent import monkey
        monkey.patch_all()
    import gevent
    gevent.spawn(app.run, debug=debug, **kwargs)
    if start:
        while not app.stopped:
            gevent.sleep(0.1)