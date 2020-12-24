# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Apps/Compose/PipeBuild.py
# Compiled at: 2008-10-19 12:19:52
import Axon
from Axon.Ipc import producerFinished, shutdownMicroprocess

class PipeBuild(Axon.Component.component):
    """This component takes messages instructing it to add/remove entities from
    a pipeline, and outputs the messages needed to update a topology viewer, and
    also a full enumeration of the pipeline

    Accepts:
        ("ADD", id_, name, data, afterid)
           Add item to pipeline, with id_, name, and data, immediately after the
           element with id 'afterid'. Or on the end if afterid == None.
        ("DEL", id_)
           Remove item from the pipeline with id_

    Emits:
        Topology msgs:
           ("DEL", "ALL")
           ("ADD", "NODE", ...)
           ("ADD", "LINK", ...)
           ("DEL", "NODE", ...)
           ("DEL", "LINK", ...)

        Pipeline enumeration messages:
           ("PIPELINE", [ <pipeline data items> ])

    """

    def __init__(self):
        super(PipeBuild, self).__init__()
        self.pipeline = []

    def main(self):
        done = False
        self.send(('DEL', 'ALL'), 'outbox')
        while not done:
            while self.dataReady('inbox'):
                command = self.recv('inbox')
                self.updatePipeline(command)

            while self.dataReady('control'):
                msg = self.recv('control')
                if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                    self.send(msg, 'signal')

            if not done:
                self.pause()
            yield 1

    def updatePipeline(self, cmd):
        if cmd[0] == 'ADD':
            self.do_addComponent(id_=cmd[1], name=cmd[2], data=cmd[3], afterid=cmd[4])
        if cmd[0] == 'DEL':
            self.do_delComponent(id_=cmd[1])
        self.outputPipeline()

    def do_addComponent(self, id_, name, data, afterid=None):
        msg = (
         'ADD', 'NODE', id_, name, 'randompos', 'component')
        self.send(msg, 'outbox')
        index = len(self.pipeline)
        if afterid != None:
            for c in self.pipeline:
                if c['id'] == afterid:
                    index = self.pipeline.index(c) + 1

        self.pipeline.insert(index, {'id': id_, 'data': data})
        if index < len(self.pipeline) - 1:
            msg = ('DEL', 'LINK', self.pipeline[(index - 1)]['id'], self.pipeline[(index + 1)]['id'])
            self.send(msg, 'outbox')
            msg = (
             'ADD', 'LINK', id_, self.pipeline[(index + 1)]['id'])
            self.send(msg, 'outbox')
        if index > 0:
            msg = ('ADD', 'LINK', self.pipeline[(index - 1)]['id'], id_)
            self.send(msg, 'outbox')
        return

    def do_delComponent(self, id_):
        self.send(('DEL', 'NODE', id_), 'outbox')
        index = -1
        for c in self.pipeline:
            if c['id'] == id_:
                index = self.pipeline.index(c)

        if index != -1:
            del self.pipeline[index]
            if index > 0 and index < len(self.pipeline):
                msg = (
                 'ADD', 'LINK', self.pipeline[(index - 1)]['id'], self.pipeline[index]['id'])
                self.send(msg, 'outbox')

    def outputPipeline(self):
        self.send(('PIPELINE', [ c['data'] for c in self.pipeline ]), 'outbox')