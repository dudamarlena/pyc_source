# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/odin/utils/progbar.py
# Compiled at: 2019-02-05 10:38:34
# Size of source mod 2**32: 17934 bytes
from __future__ import print_function, division, absolute_import
import sys, time, inspect
from numbers import Number
from datetime import datetime
from contextlib import contextmanager
from collections import OrderedDict, defaultdict
import numpy as np
from odin.visual.bashplot import print_bar, print_confusion
try:
    from tqdm import __version__ as tqdm_version
    tqdm_version = int(tqdm_version.split('.')[0])
    if tqdm_version < 4:
        raise ImportError
    from tqdm import tqdm as _tqdm
    from tqdm._utils import _environ_cols_wrapper
except ImportError:
    sys.stderr.write('[ERROR] Cannot import `tqdm` version >= 4.\n')
    exit()

try:
    import colorama
    colorama.init()
    from colorama import Fore as _Fore
    _RED = _Fore.RED
    _YELLOW = _Fore.YELLOW
    _CYAN = _Fore.CYAN
    _MAGENTA = _Fore.MAGENTA
    _RESET = _Fore.RESET
except ImportError:
    _RED, _YELLOW, _CYAN, _MAGENTA, _RESET = ('', '', '', '', '')

_NUMBERS_CH = {ord('0'): 0, 
 ord('1'): 1, 
 ord('2'): 2, 
 ord('3'): 3, 
 ord('4'): 4, 
 ord('5'): 5, 
 ord('6'): 6, 
 ord('7'): 7, 
 ord('8'): 8, 
 ord('9'): 9}
_LAST_UPDATED_PROG = [
 None]

def add_notification(msg):
    msg = _CYAN + '[%s]Notification:' % datetime.now().strftime('%d/%b-%H:%M:%S') + _RESET + msg + ''
    _tqdm.write(msg)


class _FuncWrap(object):

    def __init__(self, func, default_func=lambda x: x):
        super(_FuncWrap, self).__init__()
        if func is None:
            func = default_func
        elif not inspect.isfunction(func):
            raise AssertionError('Invalid function object of type: %s' % str(type(func)))
        self.func = func

    def __call__(self, *args, **kwargs):
        return (self.func)(*args, **kwargs)

    def __getstate__(self):
        import dill
        return dill.dumps(self.func)

    def __setstate__(self, states):
        import dill
        self.func = dill.loads(states)


def _default_dict_list_creator():
    return defaultdict(list)


class Progbar(object):
    __doc__ = ' Comprehensive review of any progress, this object is\n  fully pickle-able, and can be used for storing history,\n  summaries and report of the progress as well.\n\n  Parameters\n  ----------\n  target: int\n      total number of steps expected\n\n  interval: float\n      Minimum progress display update interval, in seconds.\n\n  keep: bool\n      whether to keep the progress bar when the epoch finished\n\n  print_report: bool\n      print updated report along with the progress bar for each update\n\n  print_summary: bool\n      print epoch summary after each epoch\n\n  count_func: call-able\n      a function takes the returned batch and return an integer for upating\n      progress.\n\n  report_func: call-able\n      a function takes the returned batch and a collection of pair\n      (key, value) for constructing the report.\n\n  progress_func : call-able\n      for post-processing the return value during processing into\n      a number representing addition in the progress\n\n  name: str or None\n      specific name for the progress bar\n\n  Examples\n  --------\n  >>> import numpy as np\n  >>> from odin.utils import Progbar\n  >>> x = list(range(10))\n  >>> for i in Progbar(target=x):\n  ...     pass\n\n  Note\n  ----\n  Some special case:\n      * any report key contain "confusionmatrix" will be printed out using\n      `print_confusion`\n      * any report key\n  '
    FP = sys.stderr

    def __init__(self, target, interval=0.08, keep=False, print_progress=True, print_report=True, print_summary=False, count_func=None, report_func=None, progress_func=None, name=None):
        self._Progbar__pb = None
        if isinstance(target, Number):
            self.target = int(target)
            self._Progbar__iter_obj = None
        else:
            if hasattr(target, '__len__'):
                self.target = len(target)
                self._Progbar__iter_obj = target
            else:
                raise ValueError('Unsupport for `target` type: %s' % str(target.__class__))
        self._seen_so_far = defaultdict(int)
        n = len(str(self.target))
        self._counter_fmt = '(%%%dd/%%%dd)' % (n, n)
        if name is None:
            name = 'Progress-%s' % datetime.utcnow()
        self._name = name
        self._Progbar__interval = float(interval)
        self._Progbar__keep = keep
        self.print_progress = bool(print_progress)
        self.print_report = bool(print_report)
        self.print_summary = bool(print_summary)
        self._report = OrderedDict()
        self._last_report = None
        self._last_print_time = None
        self._epoch_summarizer_func = {}
        self._epoch_hist = defaultdict(_default_dict_list_creator)
        self._epoch_summary = defaultdict(dict)
        self._epoch_idx = 0
        self._epoch_start_time = None
        if self._Progbar__iter_obj is None:
            if count_func is not None or report_func is not None:
                raise RuntimeError('`count_func` and `report_func` can only be used when `target` is an iterator with specific length.')
        self._Progbar__count_func = _FuncWrap(func=count_func, default_func=(lambda x: len(x)))
        self._Progbar__report_func = _FuncWrap(func=report_func, default_func=(lambda x: None))
        self._progress_func = _FuncWrap(func=progress_func, default_func=(lambda x: x))
        self._labels = None

    def __getitem__(self, key):
        return self._report.__getitem__(key)

    def __setitem__(self, key, val):
        self._epoch_hist[self.epoch_idx][key].append(val)
        return self._report.__setitem__(key, val)

    def __delitem__(self, key):
        return self._report.__delitem__(key)

    def __iter__(self):
        if self._Progbar__iter_obj is None:
            raise RuntimeError('This Progbar cannot be iterated, the set `target` must be iterable.')
        for X in self._Progbar__iter_obj:
            count = self._Progbar__count_func(X)
            report = self._Progbar__report_func(X)
            if report is not None:
                for key, val in report:
                    self[key] = val

            self.add(int(count))
            yield X

        del self._Progbar__iter_obj
        del self._Progbar__count_func
        del self._Progbar__report_func

    @property
    def epoch_idx(self):
        return self._epoch_idx

    @property
    def nb_epoch(self):
        return self._epoch_idx + 1

    @property
    def name(self):
        return self._name

    @property
    def labels(self):
        """ Special labels for printing the confusion matrix. """
        return self._labels

    @property
    def history(self):
        """ Return
    dictonary:
      {epoch_id : {tensor_name0: [batch_return1, batch_return2, ...],
                   tensor_name1: [batch_return1, batch_return2, ...],
                   ...},
       1 : {tensor_name0: [batch_return1, batch_return2, ...],
                  tensor_name1: [batch_return1, batch_return2, ...],
                  ...},
       ... }

    Example
    -------
    >>> for epoch_id, results in task.history.items():
    >>>   for tensor_name, values in results.items():
    >>>     print(tensor_name, len(values))
    """
        return self._epoch_hist

    def get_report(self, epoch=-1, key=None):
        if epoch < 0:
            epoch = self.nb_epoch + epoch - 1
        if key is None:
            return self._epoch_hist[epoch]
        else:
            return self._epoch_hist[epoch][key]

    def set_summarizer(self, key, fn):
        """ Epoch summarizer is a function, searching in the
    report for given key, and summarize all the stored values
    of each epoch into a readable format

    i.e. the input arguments is a list of stored epoch report,
    the output is a string.
    """
        if not hasattr(fn, '__call__'):
            raise ValueError('`fn` must be call-able.')
        key = str(key)
        self._epoch_summarizer_func[key] = _FuncWrap(func=fn, default_func=None)
        return self

    def set_name(self, name):
        self._name = str(name)
        return self

    def set_labels(self, labels):
        if labels is not None:
            self._labels = tuple([str(l) for l in labels])
        return self

    def _formatted_report(self, report_dict, margin='', inc_name=True):
        """ Convert a dictionary of key -> value to well formatted string."""
        if inc_name:
            text = _MAGENTA + '\t%s' % self.name + _RESET + '\n'
        else:
            text = ''
        report_dict = sorted((report_dict.items()), key=(lambda x: str(x[0])))
        for i, (key, value) in enumerate(report_dict):
            key = margin + str(key).replace('\n', ' ')
            if 'confusionmatrix' in key.lower() or 'confusion_matrix' in key.lower() or 'confusion-matrix' in key.lower() or 'confusion matrix' in key.lower():
                value = print_confusion(value, labels=(self.labels), inc_stats=True)
            else:
                value = str(value)
            if '\n' in value:
                text += _YELLOW + key + _RESET + ':\n'
                for line in value.split('\n'):
                    text += margin + ' ' + line + '\n'

            else:
                text += _YELLOW + key + _RESET + ': ' + value + '\n'

        return text[:-1]

    @property
    def progress_bar(self):
        if self._Progbar__pb is None:
            it = range(self.target)
            self._Progbar__pb = _tqdm(iterable=it, desc=('Epoch%s' % str(self.epoch_idx)),
              leave=(self._Progbar__keep),
              total=(self.target),
              file=(Progbar.FP),
              unit='obj',
              mininterval=(self._Progbar__interval),
              maxinterval=10,
              miniters=0,
              position=0)
            self._Progbar__pb.clear()
            self._epoch_start_time = time.time()
        return self._Progbar__pb

    @property
    def seen_so_far(self):
        return self._seen_so_far[self.epoch_idx]

    def _generate_epoch_summary(self, epoch, inc_name=False, inc_counter=True):
        seen_so_far = self._seen_so_far[epoch]
        if seen_so_far == 0:
            return ''
        else:
            if inc_name:
                s = _MAGENTA + '%s' % self.name + _RESET
            else:
                s = ''
            if seen_so_far == self.target:
                speed = 1.0 / self._epoch_summary[epoch]['__avg_time__']
                elapsed = self._epoch_summary[epoch]['__total_time__']
            else:
                avg_time = (time.time() - self._epoch_start_time) / self.seen_so_far if self.progress_bar.avg_time is None else self.progress_bar.avg_time
                speed = 1.0 / avg_time
                elapsed = time.time() - self._epoch_start_time
            if inc_counter:
                frac = seen_so_far / self.target
                counter_epoch = self._counter_fmt % (seen_so_far, self.target)
                percentage = '%6.2f%%%s ' % (frac * 100, counter_epoch)
            else:
                percentage = ''
            s += _RED + ' Epoch %d ' % epoch + _RESET + '%.4f(s) %s%.4f(obj/s)' % (
             elapsed, percentage, speed)
            summary = dict(self._epoch_summary[epoch])
            if len(summary) > 2:
                summary.pop('__total_time__', None)
                summary.pop('__avg_time__', None)
                s += '\n' + self._formatted_report(summary, margin='   ', inc_name=False)
            return s

    @property
    def summary(self):
        s = _MAGENTA + 'Report "%s"    TotalEpoch: %d\n' % (self.name, self.nb_epoch) + _RESET
        s += '\n'.join([self._generate_epoch_summary(i) for i in range(self.nb_epoch)])
        return s[:-1]

    def add_notification(self, msg):
        msg = _CYAN + '[%s][%s]Notification:' % (datetime.now().strftime('%d/%b-%H:%M:%S'), _MAGENTA + self.name + _CYAN) + _RESET + msg
        _tqdm.write(msg)
        return self

    def _new_epoch(self):
        if self._Progbar__pb is None:
            return
        else:
            if self._last_report is None:
                nlines = 0
            else:
                nlines = len(self._last_report.split('\n'))
            if self._Progbar__keep:
                self._Progbar__pb.moveto(nlines)
            else:
                for i in range(nlines):
                    Progbar.FP.write('\r')
                    console_width = _environ_cols_wrapper()(Progbar.FP)
                    Progbar.FP.write(' ' * (79 if console_width is None else console_width))
                    Progbar.FP.write('\r')
                    self._Progbar__pb.moveto(1)

                self._Progbar__pb.moveto(-(nlines * 2))
            self._Progbar__pb.close()
            for key, values in self._epoch_hist[self._epoch_idx].items():
                values = [v for v in values]
                if key in self._epoch_summarizer_func:
                    self._epoch_summary[self._epoch_idx][key] = self._epoch_summarizer_func[key](values)
                else:
                    if isinstance(values[0], Number):
                        self._epoch_summary[self._epoch_idx][key] = np.mean(values)
                    else:
                        if isinstance(values[0], np.ndarray):
                            self._epoch_summary[self._epoch_idx][key] = sum(v for v in values)

            total_time = time.time() - self._epoch_start_time
            self._epoch_summary[self._epoch_idx]['__total_time__'] = total_time
            avg_time = self._Progbar__pb.avg_time
            if avg_time is None:
                avg_time = total_time / self.target
            self._epoch_summary[self._epoch_idx]['__avg_time__'] = avg_time
            self._Progbar__pb = None
            self._last_report = None
            self._last_print_time = None
            self._epoch_start_time = None
            self._epoch_idx += 1
            return self

    @contextmanager
    def safe_progress(self):
        """ This context manager will automatically call `pause` if the
    progress unfinished, hence, it doesn't mesh up the screen. """
        yield
        if 0 < self.seen_so_far < self.target:
            self.pause()

    def pause(self):
        """ Call `pause` if progress is running, hasn't finish, and
    you want to print something else on the scree.
    """
        if self._last_report is not None:
            nlines = len(self._last_report.split('\n'))
            self._Progbar__pb.moveto(-nlines)
            for i in range(nlines):
                Progbar.FP.write('\r')
                console_width = _environ_cols_wrapper()(Progbar.FP)
                Progbar.FP.write(' ' * (79 if console_width is None else console_width))
                Progbar.FP.write('\r')
                self._Progbar__pb.moveto(1)

        else:
            nlines = 0
        if self._Progbar__pb is not None:
            self._Progbar__pb.clear()
            self._Progbar__pb.moveto(-nlines)
        self._last_report = None
        return self

    def add(self, n=1):
        """ You need to call pause if """
        n = self._progress_func(n)
        if not isinstance(n, Number):
            raise RuntimeError('Progress return an object, but not given `progress_func` for post-processing')
        if n <= 0:
            return self
        else:
            fp = Progbar.FP
            seen_so_far = min(self._seen_so_far[self.epoch_idx] + n, self.target)
            self._seen_so_far[self.epoch_idx] = seen_so_far
            if _LAST_UPDATED_PROG[0] is None:
                _LAST_UPDATED_PROG[0] = self
            else:
                if _LAST_UPDATED_PROG[0] != self:
                    _LAST_UPDATED_PROG[0].pause()
                    _LAST_UPDATED_PROG[0] = self
                if self.print_report:
                    curr_time = time.time()
                    if self._last_print_time is None or time.time() - self._last_print_time > self._Progbar__interval or seen_so_far >= self.target:
                        self._last_print_time = curr_time
                        if self._last_report is not None:
                            nlines = len(self._last_report.split('\n'))
                            self.progress_bar.moveto(-nlines)
                        report = self._formatted_report(self._report)
                        if self._last_report is not None:
                            for i, l in enumerate(self._last_report.split('\n')):
                                fp.write('\r')
                                fp.write(' ' * len(l))
                                fp.write('\r')
                                self.progress_bar.moveto(1)

                            self.progress_bar.clear()
                            self.progress_bar.moveto(-i - 1)
                        fp.write(report)
                        fp.flush()
                        self._last_report = report
                        self.progress_bar.moveto(1)
                if self.print_progress:
                    self.progress_bar.update(n=n)
                else:
                    self.progress_bar
            if seen_so_far >= self.target:
                self._new_epoch()
                if self.print_summary:
                    _tqdm.write(self._generate_epoch_summary((self.epoch_idx - 1), inc_name=True,
                      inc_counter=False))
            return self