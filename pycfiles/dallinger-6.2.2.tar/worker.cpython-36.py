# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/Dallinger/Dallinger/dallinger_scripts/worker.py
# Compiled at: 2020-04-27 20:27:30
# Size of source mod 2**32: 1379 bytes
"""Heroku web worker."""
listen = ['high', 'default', 'low']

def main():
    import gevent.monkey
    gevent.monkey.patch_all()
    from gevent.queue import LifoQueue
    import os
    from redis import BlockingConnectionPool, StrictRedis
    from rq import Queue, Connection
    from dallinger.heroku.rq_gevent_worker import GeventWorker as Worker
    from dallinger.config import initialize_experiment_package
    initialize_experiment_package(os.getcwd())
    import logging
    logging.basicConfig(format='%(asctime)s %(message)s', level=(logging.DEBUG))
    redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
    redis_pool = BlockingConnectionPool.from_url(redis_url, queue_class=LifoQueue)
    redis_conn = StrictRedis(connection_pool=redis_pool)
    with Connection(redis_conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()


if __name__ == '__main__':
    main()