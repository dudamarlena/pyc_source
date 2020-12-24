# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/resolv/resolvers/dummy.py
# Compiled at: 2012-10-28 17:13:06
from resolv.shared import Task

class DummyTask(Task):
    result_type = 'dummy'
    name = 'Dummy Resolver'
    author = 'Sven Slootweg'
    author_url = 'http://cryto.net/~joepie91'

    def run(self):
        self.results = {'dummy': self.url}
        self.state = 'finished'
        return self