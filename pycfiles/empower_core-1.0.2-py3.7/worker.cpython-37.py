# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/empower_core/worker.py
# Compiled at: 2020-05-10 06:48:32
# Size of source mod 2**32: 1215 bytes
"""Worker."""
from empower_core.service import EService
EVERY = 2000

class EWorker(EService):
    __doc__ = 'Base worker class.'
    MODULES = []

    def __init__(self, context, **kwargs):
        (super().__init__)(context=context, **kwargs)

    def start(self):
        for module in self.MODULES:
            module.register_callbacks(self)

        super().start()

    def stop(self):
        for module in self.MODULES:
            module.unregister_callbacks(self)

        super().stop()