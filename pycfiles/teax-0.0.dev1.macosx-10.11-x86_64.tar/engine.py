# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maciejczyzewski/teax/repository/teax/system/engine.py
# Compiled at: 2016-02-02 21:49:18
from teax.messages import T_UNKNOWN_ADAPTER_NAME

class EngineObject:
    """
    Reference interface for adapter classes;
    inheritance is not necessary.
    """
    parseable_extensions = set()

    def __init__(self, filename):
        self.filename = filename

    def start(self):
        raise NotImplementedError

    @classmethod
    def match(cls, filename, points=0):
        return points


class EngineFacade:
    adapters = {}

    def __init__(self):
        pass

    def analyze(self, filename):
        engines = {}
        for name, adapter in self.adapters.iteritems():
            engines[name] = adapter.match(filename)

        return engines

    def provide(self, filename, name):
        try:
            adapter_cls = self.adapters[name]
        except KeyError:
            tty.error(T_UNKNOWN_ADAPTER_NAME % name)

        adapter = adapter_cls(filename)
        adapter.start()
        return adapter

    @classmethod
    def register(cls, adapter):
        cls.adapters[adapter.__name__] = adapter