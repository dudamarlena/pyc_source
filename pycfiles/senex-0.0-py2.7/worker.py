# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/senex/worker.py
# Compiled at: 2016-05-02 10:35:12
"""This module contains some multithreading worker and queue logic plus the
functionality -- related to OLD installation -- that the worther thread
initiates.

The worker installs the OLD. Having a worker perform these tasks in a separate
thread from that processing the HTTP request allows us to immediately respond
to the user.

The worker can only run a callable that is a global in :mod:`senex.worker` and
which takes keyword arguments. Example usage::

    from worker import worker_q
    worker_q.put({
        'id': generate_salt(),
        'func': 'install_old',
        'args': {'env_dir': u'env-old'}
    })

Cf. http://www.chrismoos.com/2009/03/04/pylons-worker-threads.

"""
import Queue, threading, logging, time
from uuid import uuid4
import transaction
from .models import DBSession, SenexState
from installold import install
log = logging.getLogger(__name__)
worker_q = Queue.Queue(1)

class WorkerThread(threading.Thread):
    """Define the worker.

    """

    def run(self):
        while True:
            msg = worker_q.get()
            try:
                globals()[msg.get('func')](**msg.get('args'))
            except Exception as e:
                log.warn('Unable to process in worker thread: %s' % e)

            worker_q.task_done()


def start_worker():
    """TODO: Called in :mod:`onlinelinguisticdatabase.config.environment.py`.
    """
    worker = WorkerThread()
    worker.setDaemon(True)
    worker.start()


def mock_install(params):
    print 'In mock install with these params ...'
    print params
    time.sleep(10)
    print 'mock install slept for 10 seconds'
    time.sleep(10)
    print 'mock install slept for 20 seconds'
    time.sleep(10)
    print 'mock install slept for 30 seconds'


def install_old(**kwargs):
    """Install the OLD and its dependencies.

    """
    print 'install old in worker!'
    print kwargs
    try:
        try:
            mock_install(kwargs)
        except SystemExit as e:
            print 'CAUGHT SYSTEM EXIT in worker!!!! with this error:'
            print e
        except:
            print 'Caught OTHER ERROR'

    finally:
        installation_not_in_progress()


def installation_not_in_progress():
    senex_state = DBSession.query(SenexState).order_by(SenexState.id.desc()).first()
    senex_state.installation_in_progress = False
    DBSession.add(senex_state)
    transaction.commit()