# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/typhoonae/taskqueue/tests/test_celery_taskqueue.py
# Compiled at: 2010-12-12 04:36:57
"""Unit tests for TyphoonAE's Task Queue implementation backed by Celery."""
from typhoonae.taskqueue import taskqueue_celery_stub
from typhoonae.taskqueue.tests import test_taskqueue
import google.appengine.api.apiproxy_stub, google.appengine.api.apiproxy_stub_map, os, time

class TaskQueueTestCase(test_taskqueue.TaskQueueTestCase):
    """Testing the typhoonae task queue."""

    def setUp(self):
        """Register typhoonae's task queue API proxy stub."""
        google.appengine.api.apiproxy_stub_map.apiproxy = google.appengine.api.apiproxy_stub_map.APIProxyStubMap()
        taskqueue = taskqueue_celery_stub.TaskQueueServiceStub(internal_address='127.0.0.1:8770', root_path=os.path.dirname(__file__))
        google.appengine.api.apiproxy_stub_map.apiproxy.RegisterStub('taskqueue', taskqueue)
        self.stub = google.appengine.api.apiproxy_stub_map.apiproxy.GetStub('taskqueue')
        google.appengine.api.apiproxy_stub_map.apiproxy.RegisterStub('urlfetch', test_taskqueue.DummyURLFetchServiceStub())
        self._os_environ = dict(os.environ)
        os.environ.clear()
        os.environ['SERVER_NAME'] = 'localhost'
        os.environ['SERVER_PORT'] = '8080'
        os.environ['TZ'] = 'UTC'
        time.tzset()