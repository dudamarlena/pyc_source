# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/karas/training/extensions/tensorboard.py
# Compiled at: 2019-01-08 04:51:58
# Size of source mod 2**32: 2035 bytes
import tensorboardX as tbx
from karas import compare_key
from karas.training import extension

class TensorBoard(extension.Extension):
    __doc__ = 'Trainer extension to print the accumulated results.\n\n    This extension uses the log accumulated by a :class:`LogReport` extension\n    to print specified entries of the log in a human-readable format.\n\n    Args:\n        entries (list of str): List of keys of observations to print.\n        log_report (str or LogReport): Log report to accumulate the\n            observations. This is either the name of a LogReport extensions\n            registered to the trainer, or a LogReport instance to use\n            internally.\n        out: Stream to print the bar. Standard output is used by default.\n\n    '

    def __init__(self, keys=None, out='logdir'):
        self._keys = keys
        self._out = out

    def initialize(self, trainer):
        self._writer = tbx.SummaryWriter(log_dir=(self._out))

    def __call__(self, trainer):
        observation = trainer.observation
        epoch = trainer.epoch
        iteration = trainer.iteration
        for tag, value in observation.items():
            step = epoch if 'test' in tag else iteration
            haskey = False
            if self._keys is not None:
                for key in self._keys:
                    if compare_key(key, tag):
                        haskey = True
                        break

                if not haskey:
                    continue
            if 'scalar' in tag:
                self._writer.add_scalar(tag, value, global_step=step)
            else:
                if 'images' in tag:
                    self._writer.add_image(tag, (value.cpu().numpy()), global_step=step)

    def finalize(self):
        self._writer.close()

    def __getstate__(self):
        state = {}
        state['_keys'] = self._keys
        state['_out'] = self._out
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self._writer = tbx.SummaryWriter(log_dir=(self._out))