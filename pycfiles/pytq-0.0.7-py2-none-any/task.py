# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/pytq-project/pytq/task.py
# Compiled at: 2017-11-29 22:49:56
import six, attr
try:
    from .pkg.attrs_mate import AttrsClass
except:
    from pytq.pkg.attrs_mate import AttrsClass

def none_or_is_callable(instance, attribute, value):
    """
    Can be None or callable.
    """
    if value is not None and not callable(value):
        raise TypeError('callback must be a callable, got %s' % type(value).__name__)
    return


@attr.s
class Task(AttrsClass):
    """
    Task is the core concept for task queue application.

    :param id: str or int, fingerprint of input_data.
    :param input_data: input data of the task.
    :param nth_counter: its the nth task in the entire queue.
    :param left_counter: there's nth task left for the entire batch job.
    :param output_data: after processing, the output data you got, could
        includes anything, such as, raw data, status, errors.
    :param pre_process: a callable function for single task, will be called
        before the process function been called.
    :param post_process: a callable function for single task, will be called
        after the process function been called.
    """
    id = attr.ib()
    input_data = attr.ib()
    nth_counter = attr.ib(default=None)
    left_counter = attr.ib(default=None)
    output_data = attr.ib(default=None)
    pre_process = attr.ib(default=None, validator=none_or_is_callable)
    post_process = attr.ib(default=None, validator=none_or_is_callable)

    def _pre_process(self):
        self.pre_process(self)

    def _post_process(self):
        self.post_process(self)

    def progress_msg(self):
        """
        Generate progress message.
        """
        if self.nth_counter is None:
            msg = 'Process: InputData(%r) ...' % self.input_data
            return msg
        else:
            if self.left_counter is None:
                msg = 'Process %sth: InputData(%r) ...' % (
                 self.nth_counter, self.input_data)
            else:
                msg = 'Process %sth: InputData(%r); %s left ...' % (
                 self.nth_counter, self.input_data, self.left_counter)
            return msg