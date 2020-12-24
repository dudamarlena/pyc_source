# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/karas/training/extensions/lr_observer.py
# Compiled at: 2019-01-08 08:42:29
# Size of source mod 2**32: 462 bytes
from karas.training import extension

class LrObserver(extension.Extension):

    def initialize(self, trainer):
        self(trainer)

    def __call__(self, trainer):
        reporter = trainer.reporter
        optimizers = trainer.updater.get_optimizers()
        for key, optimizer in optimizers.items():
            lr = optimizer.param_groups[0]['lr']
            with reporter.scope('scalar'):
                reporter.report({'{}/lr'.format(key): lr})