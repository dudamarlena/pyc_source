# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/karas/training/triggers/interval_trigger.py
# Compiled at: 2019-01-07 04:13:42
# Size of source mod 2**32: 4036 bytes
import warnings

class IntervalTrigger(object):
    __doc__ = "Trigger based on a fixed interval.\n\n    This trigger accepts iterations divided by a given interval. There are two\n    ways to specify the interval: per iterations and epochs. `Iteration` means\n    the number of updates, while `epoch` means the number of sweeps over the\n    training dataset. Fractional values are allowed if the interval is a\n    number of epochs; the trigger uses the `iteration` and `epoch_detail`\n    attributes defined by the updater.\n\n    For the description of triggers, see :func:`~chainer.training.get_trigger`.\n\n    Args:\n        period (int or float): Length of the interval. Must be an integer if\n            unit is ``'iteration'``.\n        unit (str): Unit of the length specified by ``period``. It must be\n            either ``'iteration'`` or ``'epoch'``.\n\n    "

    def __init__(self, period, unit):
        self.period = period
        if not unit == 'epoch':
            if not unit == 'iteration':
                raise AssertionError
        self.unit = unit
        self._previous_iteration = 0
        self._previous_epoch_detail = 0.0
        self.count = 0

    def __call__(self, trainer):
        """Decides whether the extension should be called on this iteration.

        Args:
            trainer (Trainer): Trainer object that this trigger is associated
                with. The updater associated with this trainer is used to
                determine if the trigger should fire.

        Returns:
            bool: True if the corresponding extension should be invoked in this
            iteration.

        """
        if self.unit == 'epoch':
            epoch_detail = trainer.epoch_detail
            previous_epoch_detail = self._previous_epoch_detail
            if previous_epoch_detail < 0:
                previous_epoch_detail = trainer.previous_epoch_detail
            self.count = epoch_detail // self.period
            fire = previous_epoch_detail // self.period != epoch_detail // self.period
        else:
            iteration = trainer.iteration
            previous_iteration = self._previous_iteration
            if previous_iteration < 0:
                previous_iteration = iteration - 1
            fire = previous_iteration // self.period != iteration // self.period
        self._previous_iteration = trainer.iteration
        if hasattr(trainer, 'epoch_detail'):
            self._previous_epoch_detail = trainer.epoch_detail
        return fire

    def serialize(self, serializer):
        try:
            self._previous_iteration = serializer('previous_iteration', self._previous_iteration)
        except KeyError:
            warnings.warn('The previous value of iteration is not saved. IntervalTrigger guesses it using current iteration. If this trigger is not called at every iteration, it may not work correctly.')
            self._previous_iteration = -1

        try:
            self._previous_epoch_detail = serializer('previous_epoch_detail', self._previous_epoch_detail)
        except KeyError:
            warnings.warn('The previous value of epoch_detail is not saved. IntervalTrigger uses the value of trainer.updater.previous_epoch_detail. If this trigger is not called at every iteration, it may not work correctly.')
            self._previous_epoch_detail = -1.0

    def get_training_length(self):
        return (self.period, self.unit)