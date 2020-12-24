# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/perf/statobject.py
# Compiled at: 2012-10-12 07:02:39
import pprint
from coils.net import PathObject

class StatObject(PathObject):

    def __init__(self, parent, name, **params):
        self.name = name
        PathObject.__init__(self, parent, **params)

    def is_public(self):
        return False

    def get_name(self):
        return self.name

    def do_GET(self):
        data = self.context.run_command('admin::get-performance-log', lname=self.name)
        data = pprint.pformat(data)
        self.request.simple_response(200, mimetype='text/plain', data=data)