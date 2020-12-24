# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/karas/training/extensions/log_report.py
# Compiled at: 2019-01-08 04:39:38
# Size of source mod 2**32: 4568 bytes
import json, os, shutil, six
from karas import compare_key
from karas import reporter
from karas.training import extension, utils
from karas.training.triggers.utils import get_trigger

class LogReport(extension.Extension):
    __doc__ = "Trainer extension to output the accumulated results to a log file.\n\n    This extension accumulates the observations of the trainer to\n    :class:`~chainer.DictSummary` at a regular interval specified by a supplied\n    trigger, and writes them into a log file in JSON format.\n\n    There are two triggers to handle this extension. One is the trigger to\n    invoke this extension, which is used to handle the timing of accumulating\n    the results. It is set to ``1, 'iteration'`` by default. The other is the\n    trigger to determine when to emit the result. When this trigger returns\n    True, this extension appends the summary of accumulated values to the list\n    of past summaries, and writes the list to the log file. Then, this\n    extension makes a new fresh summary object which is used until the next\n    time that the trigger fires.\n\n    It also adds some entries to each result dictionary.\n\n    - ``'epoch'`` and ``'iteration'`` are the epoch and iteration counts at the\n      output, respectively.\n    - ``'elapsed_time'`` is the elapsed time in seconds since the training\n      begins. The value is taken from :attr:`Trainer.elapsed_time`.\n\n    Args:\n        keys (iterable of strs): Keys of values to accumulate. If this is None,\n            all the values are accumulated and output to the log file.\n        trigger: Trigger that decides when to aggregate the result and output\n            the values. This is distinct from the trigger of this extension\n            itself. If it is a tuple in the form ``<int>, 'epoch'`` or\n            ``<int>, 'iteration'``, it is passed to :class:`IntervalTrigger`.\n        postprocess: Callback to postprocess the result dictionaries. Each\n            result dictionary is passed to this callback on the output. This\n            callback can modify the result dictionaries, which are used to\n            output to the log file.\n        log_name (str): Name of the log file under the output directory. It can\n            be a format string: the last result dictionary is passed for the\n            formatting. For example, users can use '{iteration}' to separate\n            the log files for different iterations. If the log name is None, it\n            does not output the log to any file.\n\n    "

    def __init__(self, keys=None, trigger=(1, 'epoch'), postprocess=None, log_name='log'):
        self._keys = keys
        self._trigger = get_trigger(trigger)
        self._postprocess = postprocess
        self._log_name = log_name
        self._log = []
        self._init_summary()

    def __call__(self, trainer):
        keys = self._keys
        observation = trainer.observation
        summary = self._summary
        if keys is None:
            summary.add(observation)
        else:
            for tag in observation.keys():
                for key in keys:
                    if compare_key(key, tag):
                        summary.add({key: observation[tag]})

        if not self._trigger(trainer):
            stats = self._summary.compute_mean()
            stats_cpu = {}
            for name, value in six.iteritems(stats):
                stats_cpu[name] = float(value)

            stats_cpu['epoch'] = trainer.epoch
            stats_cpu['iteration'] = trainer.iteration
            stats_cpu['elapsed_time'] = trainer.elapsed_time
            if self._postprocess is not None:
                self._postprocess(stats_cpu)
            self._log.append(stats_cpu)
            if self._log_name is not None:
                log_name = (self._log_name.format)(**stats_cpu)
                with utils.tempdir(prefix=log_name, dir=(trainer.out)) as (tempd):
                    path = os.path.join(tempd, 'log.json')
                    with open(path, 'w') as (f):
                        json.dump((self._log), f, indent=4)
                    new_path = os.path.join(trainer.out, log_name)
                    shutil.move(path, new_path)
            self._init_summary()

    @property
    def log(self):
        """The current list of observation dictionaries."""
        return self._log

    def _init_summary(self):
        self._summary = reporter.DictSummary()