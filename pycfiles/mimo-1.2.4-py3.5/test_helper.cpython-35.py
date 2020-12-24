# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mimo/test_helper.py
# Compiled at: 2016-10-13 12:43:28
# Size of source mod 2**32: 955 bytes
import asyncio
from .io.input import Input
from .io.output import Output
from .io.io_set import IOSet

class TestHelper:

    def __init__(self, stream, timeout=5):
        ins = [Input(in_) for in_ in stream.ins]
        outs = [Output(out) for out in stream.outs]
        self.sinks = [Input(out) for out in stream.outs]
        for out, sink in zip(outs, self.sinks):
            out.pipe(sink)

        self.ins = IOSet(ins)
        self.outs = IOSet(outs)
        self.stream = stream
        self._timeout = timeout
        self._loop = asyncio.get_event_loop()

    def run(self, ins={}):
        for key, value in ins.items():
            self.ins[key]._queue.extend(value)
            self.ins[key].close()

        task = self._loop.create_task(self.stream.run(self.ins, self.outs))
        self._loop.run_until_complete(asyncio.wait_for(task, self._timeout, loop=self._loop))
        return {sink.name:list(sink._queue) for sink in self.sinks}