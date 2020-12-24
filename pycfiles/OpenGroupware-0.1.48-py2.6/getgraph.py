# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/task/getgraph.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *

class GetGraph(Command):
    __domain__ = 'task'
    __operation__ = 'get-graph'
    root = None

    def __init__(self):
        Command.__init__(self)

    def _chase_root(self, task):
        if task.parent_id:
            query = self._ctx.db_session().query(Task).filter(Task.object_id == task.parent_id)
            query = query.enable_eagerloads(False)
            parent = query.all()
            if parent:
                return self._chase_root(parent[0])
            return task
        else:
            return task

    def _get_children(self, object_id):
        db = self._ctx.db_session()
        query = db.query(Task.object_id).filter(Task.parent_id == object_id)
        query = query.enable_eagerloads(False)
        return [ x[0] for x in query.all() ]

    def _get_graph(self, object_id):
        graph = {}
        children = self._get_children(object_id)
        for child in children:
            graph[str(child)] = self._get_graph(child)

        return graph

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        self.object_id = params.get('id', None)
        self.obj = params.get('object', None)
        return

    def run(self):
        db = self._ctx.db_session()
        if self.object_id:
            self.obj = self._ctx.run_command('task::get', id=[self._object_id])
        if not self.obj:
            raise COILSException(404, 'No task available to command task::get-graph')
        root = self._chase_root(self.obj)
        self.set_result({str(root.object_id): self._get_graph(root.object_id)})