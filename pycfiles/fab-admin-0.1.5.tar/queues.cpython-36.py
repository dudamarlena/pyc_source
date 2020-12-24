# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: e:\opt\private\cw1427\fab-admin\fab_admin\addon\queue\queues.py
# Compiled at: 2020-02-17 02:50:15
# Size of source mod 2**32: 1774 bytes
"""
Redis queue.
Created on 2020-02-17.
@desc: Redis queue views.
@app: fab_admin
"""
import logging
from app import appbuilder, rq
import requests
from fab_admin.models import MyUser
log = logging.getLogger(appbuilder.get_app.config['LOG_NAME'])

class JobExecuteException(Exception):
    __doc__ = "Customize exception for job execute. won't retry."


class JobExecuteRetryException(Exception):
    __doc__ = 'Customize exception for job execute. need retry.'


@rq.job(timeout=300, ttl=86400)
def schedule_requests_task(url, method, basic_auth, headers, **form):
    """do a task to raise request by the parameter url based on form."""
    try:
        res = requests.request(method, url, headers=headers, auth=basic_auth, data=form, verify=False, timeout=300)
        if res.status_code > 400:
            log.error('Failed schedule_requests_task job url={0} response={1}'.format(url, res.content))
            raise JobExecuteException('Failed schedule_requests_task job url={0} response={1}'.format(url, res.content))
        else:
            log.info('Successfully do schedule_requests_task job url={0} response={1}'.format(url, res.content))
    except Exception as e:
        log.error('Exception occrured  schedule_requests_task job url={0} response={1}'.format(url, e))
        raise JobExecuteException('Exception occrured  schedule_requests_task job url={0} response={1}'.format(url, e))


@rq.job(timeout=60, ttl=60)
def schedule_test_task(name):
    """do a test task to test flask-rq2 worker post fork."""
    u1 = appbuilder.get_session.query(MyUser).filter(MyUser.id == 1).one_or_none()
    log.debug(u1)
    log.debug('schedule_test_task invoked say hi to {0}'.format(name))