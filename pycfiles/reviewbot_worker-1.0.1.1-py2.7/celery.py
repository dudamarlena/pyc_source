# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/reviewbot/celery.py
# Compiled at: 2018-07-31 04:26:56
from __future__ import absolute_import, unicode_literals
import logging, pkg_resources
from celery import Celery
from kombu import Exchange, Queue
from reviewbot.config import init as init_config
from reviewbot.repositories import repositories, init_repositories
celery = None

def create_queues():
    """Create the celery queues.

    Returns:
        list of kombu.Queue:
        The queues that this worker will listen to.
    """
    default_exchange = Exchange(b'celery', type=b'direct')
    queues = [
     Queue(b'celery', default_exchange, routing_key=b'celery')]
    for ep in pkg_resources.iter_entry_points(group=b'reviewbot.tools'):
        tool_class = ep.load()
        tool = tool_class()
        queue_name = b'%s.%s' % (ep.name, tool_class.version)
        if tool.check_dependencies():
            if tool.working_directory_required:
                for repo_name in repositories:
                    repo_queue_name = b'%s.%s' % (queue_name, repo_name)
                    queues.append(Queue(repo_queue_name, Exchange(repo_queue_name, type=b'direct'), routing_key=repo_queue_name))

            else:
                queues.append(Queue(queue_name, Exchange(queue_name, type=b'direct'), routing_key=queue_name))
        else:
            logging.warning(b'%s dependency check failed.', ep.name)

    return queues


def main():
    global celery
    init_config()
    init_repositories()
    celery = Celery(b'reviewbot.celery', include=[b'reviewbot.tasks'])
    celery.conf.CELERY_ACCEPT_CONTENT = [b'json']
    celery.conf.CELERY_QUEUES = create_queues()
    celery.start()


if __name__ == b'__main__':
    main()