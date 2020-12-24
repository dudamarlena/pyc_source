# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/idapload/test/mock_locustfile.py
# Compiled at: 2020-04-13 02:37:12
# Size of source mod 2**32: 1224 bytes
import os, random, time
from contextlib import contextmanager
MOCK_LOUCSTFILE_CONTENT = '\n"""This is a mock locust file for unit testing"""\n\nfrom locust import HttpLocust, TaskSet, task, between\n\n\ndef index(l):\n    l.client.get("/")\n\ndef stats(l):\n    l.client.get("/stats/requests")\n\n\nclass UserTasks(TaskSet):\n    # one can specify tasks like this\n    tasks = [index, stats]\n\n\nclass LocustSubclass(HttpLocust):\n    host = "http://127.0.0.1:8089"\n    wait_time = between(2, 5)\n    task_set = UserTasks\n\n\nclass NotLocustSubclass():\n    host = "http://localhost:8000"\n\n'

class MockedLocustfile:
    __slots__ = [
     'filename', 'directory', 'file_path']


@contextmanager
def mock_locustfile(filename_prefix='mock_locustfile', content=MOCK_LOUCSTFILE_CONTENT):
    mocked = MockedLocustfile()
    mocked.directory = os.path.dirname(os.path.abspath(__file__))
    mocked.filename = '%s_%s_%i.py' % (
     filename_prefix,
     str(time.time()).replace('.', '_'),
     random.randint(0, 100000))
    mocked.file_path = os.path.join(mocked.directory, mocked.filename)
    with open(mocked.file_path, 'w') as (file):
        file.write(content)
    yield mocked
    os.remove(mocked.file_path)