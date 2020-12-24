# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/karas/training/extensions/progress_bar.py
# Compiled at: 2019-01-08 04:39:38
# Size of source mod 2**32: 4623 bytes
from __future__ import division
import datetime, os, sys, time
from karas.training import extension
from karas.training import utils

class ProgressBar(extension.Extension):
    __doc__ = "Trainer extension to print a progress bar and recent training status.\n\n    This extension prints a progress bar at every call. It watches the current\n    iteration and epoch to print the bar.\n\n    Args:\n        training_length (tuple): Length of whole training. It consists of an\n            integer and either ``'epoch'`` or ``'iteration'``. If this value is\n            omitted and the stop trigger of the trainer is\n            :class:`IntervalTrigger`, this extension uses its attributes to\n            determine the length of the training.\n        update_interval (int): Number of iterations to skip printing the\n            progress bar.\n        bar_length (int): Length of the progress bar in characters.\n        out: Stream to print the bar. Standard output is used by default.\n\n    "

    def __init__(self, training_length=None, update_interval=100, bar_length=50, out=sys.stdout):
        self._training_length = training_length
        self._status_template = None
        self._update_interval = update_interval
        self._bar_length = bar_length
        self._out = out
        self._recent_timing = []

    def __call__(self, trainer):
        training_length = self._training_length
        if training_length is None:
            t = trainer.stop_trigger
            training_length = t.get_training_length()
        stat_template = self._status_template
        if stat_template is None:
            stat_template = self._status_template = '{0.iteration:10} iter, {0.epoch} epoch / %s %ss\n' % training_length
        length, unit = training_length
        out = self._out
        iteration = trainer.iteration
        if iteration % self._update_interval == 0:
            epoch = trainer.epoch_detail
            recent_timing = self._recent_timing
            now = time.time()
            recent_timing.append((iteration, epoch, now))
            if os.name == 'nt':
                utils.erase_console(0, 0)
            else:
                out.write('\x1b[J')
            if unit == 'iteration':
                rate = iteration / length
            else:
                rate = epoch / length
            rate = min(rate, 1.0)
            bar_length = self._bar_length
            marks = '#' * int(rate * bar_length)
            out.write('     total [{}{}] {:6.2%}\n'.format(marks, '.' * (bar_length - len(marks)), rate))
            epoch_rate = epoch - int(epoch)
            marks = '#' * int(epoch_rate * bar_length)
            out.write('this epoch [{}{}] {:6.2%}\n'.format(marks, '.' * (bar_length - len(marks)), epoch_rate))
            status = stat_template.format(trainer.get_iterator('train'))
            out.write(status)
            old_t, old_e, old_sec = recent_timing[0]
            span = now - old_sec
            if span != 0:
                speed_t = (iteration - old_t) / span
                speed_e = (epoch - old_e) / span
            else:
                speed_t = float('inf')
                speed_e = float('inf')
            if unit == 'iteration':
                estimated_time = (length - iteration) / speed_t
            else:
                estimated_time = (length - epoch) / speed_e
            estimated_time = max(estimated_time, 0.0)
            out.write('{:10.5g} iters/sec. Estimated time to finish: {}.\n'.format(speed_t, datetime.timedelta(seconds=estimated_time)))
            if os.name == 'nt':
                utils.set_console_cursor_position(0, -4)
            else:
                out.write('\x1b[4A')
            if hasattr(out, 'flush'):
                out.flush()
            if len(recent_timing) > 100:
                del recent_timing[0]

    def finalize(self):
        out = self._out
        if os.name == 'nt':
            utils.erase_console(0, 0)
        else:
            out.write('\x1b[J')
        if hasattr(out, 'flush'):
            out.flush()

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['_out']
        return state

    def __setstate__(self, state):
        state['_out'] = sys.stdout
        self.__dict__.update(state)