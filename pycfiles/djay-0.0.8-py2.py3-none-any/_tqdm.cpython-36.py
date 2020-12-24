# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/tqdm/tqdm/_tqdm.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 51300 bytes
"""
Customisable progressbar decorator for iterators.
Includes a default (x)range iterator printing to stderr.

Usage:
  >>> from tqdm import trange[, tqdm]
  >>> for i in trange(10): #same as: for i in tqdm(xrange(10))
  ...     ...
"""
from __future__ import absolute_import
from __future__ import division
from ._utils import _supports_unicode, _environ_cols_wrapper, _range, _unich, _term_move_up, _unicode, WeakSet, _basestring, _OrderedDict, Comparable, RE_ANSI, _is_ascii, SimpleTextIOWrapper
from ._monitor import TMonitor
import sys
from numbers import Number
from time import time
from contextlib import contextmanager
import threading as th
from warnings import warn
__author__ = {'github.com/': ['noamraph', 'obiwanus', 'kmike', 'hadim',
                 'casperdcl', 'lrq3000']}
__all__ = ['tqdm', 'trange',
 'TqdmTypeError', 'TqdmKeyError', 'TqdmWarning',
 'TqdmExperimentalWarning', 'TqdmDeprecationWarning',
 'TqdmMonitorWarning']

class TqdmTypeError(TypeError):
    pass


class TqdmKeyError(KeyError):
    pass


class TqdmWarning(Warning):
    __doc__ = 'base class for all tqdm warnings.\n\n    Used for non-external-code-breaking errors, such as garbled printing.\n    '

    def __init__(self, msg, fp_write=None, *a, **k):
        if fp_write is not None:
            fp_write('\n' + self.__class__.__name__ + ': ' + str(msg).rstrip() + '\n')
        else:
            (super(TqdmWarning, self).__init__)(msg, *a, **k)


class TqdmExperimentalWarning(TqdmWarning, FutureWarning):
    __doc__ = 'beta feature, unstable API and behaviour'


class TqdmDeprecationWarning(TqdmWarning, DeprecationWarning):
    pass


class TqdmMonitorWarning(TqdmWarning, RuntimeWarning):
    __doc__ = 'tqdm monitor errors which do not affect external functionality'


class TqdmDefaultWriteLock(object):
    __doc__ = '\n    Provide a default write lock for thread and multiprocessing safety.\n    Works only on platforms supporting `fork` (so Windows is excluded).\n    You must initialise a `tqdm` or `TqdmDefaultWriteLock` instance\n    before forking in order for the write lock to work.\n    On Windows, you need to supply the lock from the parent to the children as\n    an argument to joblib or the parallelism lib you use.\n    '

    def __init__(self):
        self.create_mp_lock()
        self.create_th_lock()
        cls = type(self)
        self.locks = [lk for lk in [cls.mp_lock, cls.th_lock] if lk is not None]

    def acquire(self):
        for lock in self.locks:
            lock.acquire()

    def release(self):
        for lock in self.locks[::-1]:
            lock.release()

    def __enter__(self):
        self.acquire()

    def __exit__(self, *exc):
        self.release()

    @classmethod
    def create_mp_lock(cls):
        if not hasattr(cls, 'mp_lock'):
            try:
                from multiprocessing import RLock
                cls.mp_lock = RLock()
            except ImportError:
                cls.mp_lock = None
            except OSError:
                cls.mp_lock = None

    @classmethod
    def create_th_lock(cls):
        if not hasattr(cls, 'th_lock'):
            try:
                cls.th_lock = th.RLock()
            except OSError:
                cls.th_lock = None


TqdmDefaultWriteLock.create_th_lock()
ASCII_FMT = ' 123456789#'
UTF_FMT = ' ' + ''.join(map(_unich, range(9615, 9607, -1)))

class tqdm(Comparable):
    __doc__ = '\n    Decorate an iterable object, returning an iterator which acts exactly\n    like the original iterable, but prints a dynamically updating\n    progressbar every time a value is requested.\n    '
    monitor_interval = 10
    monitor = None

    @staticmethod
    def format_sizeof(num, suffix='', divisor=1000):
        """
        Formats a number (greater than unity) with SI Order of Magnitude
        prefixes.

        Parameters
        ----------
        num  : float
            Number ( >= 1) to format.
        suffix  : str, optional
            Post-postfix [default: ''].
        divisor  : float, optionl
            Divisor between prefixes [default: 1000].

        Returns
        -------
        out  : str
            Number with Order of Magnitude SI unit postfix.
        """
        for unit in ('', 'k', 'M', 'G', 'T', 'P', 'E', 'Z'):
            if abs(num) < 999.5:
                if abs(num) < 99.95:
                    if abs(num) < 9.995:
                        return '{0:1.2f}'.format(num) + unit + suffix
                    return '{0:2.1f}'.format(num) + unit + suffix
                else:
                    return '{0:3.0f}'.format(num) + unit + suffix
            num /= divisor

        return '{0:3.1f}Y'.format(num) + suffix

    @staticmethod
    def format_interval(t):
        """
        Formats a number of seconds as a clock time, [H:]MM:SS

        Parameters
        ----------
        t  : int
            Number of seconds.

        Returns
        -------
        out  : str
            [H:]MM:SS
        """
        mins, s = divmod(int(t), 60)
        h, m = divmod(mins, 60)
        if h:
            return '{0:d}:{1:02d}:{2:02d}'.format(h, m, s)
        else:
            return '{0:02d}:{1:02d}'.format(m, s)

    @staticmethod
    def format_num(n):
        """
        Intelligent scientific notation (.3g).

        Parameters
        ----------
        n  : int or float or Numeric
            A Number.

        Returns
        -------
        out  : str
            Formatted number.
        """
        f = '{0:.3g}'.format(n).replace('+0', '+').replace('-0', '-')
        n = str(n)
        if len(f) < len(n):
            return f
        else:
            return n

    @staticmethod
    def ema(x, mu=None, alpha=0.3):
        """
        Exponential moving average: smoothing to give progressively lower
        weights to older values.

        Parameters
        ----------
        x  : float
            New value to include in EMA.
        mu  : float, optional
            Previous EMA value.
        alpha  : float, optional
            Smoothing factor in range [0, 1], [default: 0.3].
            Increase to give more weight to recent values.
            Ranges from 0 (yields mu) to 1 (yields x).
        """
        if mu is None:
            return x
        else:
            return alpha * x + (1 - alpha) * mu

    @staticmethod
    def status_printer(file):
        """
        Manage the printing and in-place updating of a line of characters.
        Note that if the string is longer than a line, then in-place
        updating may not work (it will print a new line at each refresh).
        """
        fp = file
        fp_flush = getattr(fp, 'flush', lambda : None)

        def fp_write(s):
            fp.write(_unicode(s))
            fp_flush()

        last_len = [
         0]

        def print_status(s):
            len_s = len(s)
            fp_write('\r' + s + ' ' * max(last_len[0] - len_s, 0))
            last_len[0] = len_s

        return print_status

    @staticmethod
    def format_meter(n, total, elapsed, ncols=None, prefix='', ascii=False, unit='it', unit_scale=False, rate=None, bar_format=None, postfix=None, unit_divisor=1000, **extra_kwargs):
        """
        Return a string-based progress bar given some parameters

        Parameters
        ----------
        n  : int
            Number of finished iterations.
        total  : int
            The expected total number of iterations. If meaningless (), only
            basic progress statistics are displayed (no ETA).
        elapsed  : float
            Number of seconds passed since start.
        ncols  : int, optional
            The width of the entire output message. If specified,
            dynamically resizes the progress meter to stay within this bound
            [default: None]. The fallback meter width is 10 for the progress
            bar + no limit for the iterations counter and statistics. If 0,
            will not print any meter (only stats).
        prefix  : str, optional
            Prefix message (included in total width) [default: ''].
            Use as {desc} in bar_format string.
        ascii  : bool, optional or str, optional
            If not set, use unicode (smooth blocks) to fill the meter
            [default: False]. The fallback is to use ASCII characters
            " 123456789#".
        unit  : str, optional
            The iteration unit [default: 'it'].
        unit_scale  : bool or int or float, optional
            If 1 or True, the number of iterations will be printed with an
            appropriate SI metric prefix (k = 10^3, M = 10^6, etc.)
            [default: False]. If any other non-zero number, will scale
            `total` and `n`.
        rate  : float, optional
            Manual override for iteration rate.
            If [default: None], uses n/elapsed.
        bar_format  : str, optional
            Specify a custom bar string formatting. May impact performance.
            [default: '{l_bar}{bar}{r_bar}'], where
            l_bar='{desc}: {percentage:3.0f}%|' and
            r_bar='| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, '
              '{rate_fmt}{postfix}]'
            Possible vars: l_bar, bar, r_bar, n, n_fmt, total, total_fmt,
              percentage, rate, rate_fmt, rate_noinv, rate_noinv_fmt,
              rate_inv, rate_inv_fmt, elapsed, elapsed_s,
              remaining, remaining_s, desc, postfix, unit.
            Note that a trailing ": " is automatically removed after {desc}
            if the latter is empty.
        postfix  : *, optional
            Similar to `prefix`, but placed at the end
            (e.g. for additional stats).
            Note: postfix is usually a string (not a dict) for this method,
            and will if possible be set to postfix = ', ' + postfix.
            However other types are supported (#382).
        unit_divisor  : float, optional
            [default: 1000], ignored unless `unit_scale` is True.

        Returns
        -------
        out  : Formatted meter and stats, ready to display.
        """
        if total:
            if n > total:
                total = None
            else:
                if unit_scale:
                    if unit_scale not in (True, 1):
                        if total:
                            total *= unit_scale
                        n *= unit_scale
                        if rate:
                            rate *= unit_scale
                        unit_scale = False
                elapsed_str = tqdm.format_interval(elapsed)
                if rate is None:
                    if elapsed:
                        rate = n / elapsed
            inv_rate = 1 / rate if rate else None
            format_sizeof = tqdm.format_sizeof
            rate_noinv_fmt = ((format_sizeof(rate) if unit_scale else '{0:5.2f}'.format(rate)) if rate else '?') + unit + '/s'
            rate_inv_fmt = ((format_sizeof(inv_rate) if unit_scale else '{0:5.2f}'.format(inv_rate)) if inv_rate else '?') + 's/' + unit
            rate_fmt = rate_inv_fmt if (inv_rate and inv_rate > 1) else rate_noinv_fmt
            if unit_scale:
                n_fmt = format_sizeof(n, divisor=unit_divisor)
                total_fmt = format_sizeof(total, divisor=unit_divisor) if total is not None else '?'
            else:
                n_fmt = str(n)
                total_fmt = str(total) if total is not None else '?'
        else:
            try:
                postfix = ', ' + postfix if postfix else ''
            except TypeError:
                pass

            remaining = (total - n) / rate if (rate and total) else 0
            remaining_str = tqdm.format_interval(remaining) if rate else '?'
            if prefix:
                bool_prefix_colon_already = prefix[-2:] == ': '
                l_bar = prefix if bool_prefix_colon_already else prefix + ': '
            else:
                l_bar = ''
        r_bar = '| {0}/{1} [{2}<{3}, {4}{5}]'.format(n_fmt, total_fmt, elapsed_str, remaining_str, rate_fmt, postfix)
        format_dict = dict(n=n, 
         n_fmt=n_fmt, total=total, total_fmt=total_fmt, rate=inv_rate if (inv_rate and inv_rate > 1) else rate, 
         rate_fmt=rate_fmt, 
         rate_noinv=rate, rate_noinv_fmt=rate_noinv_fmt, 
         rate_inv=inv_rate, rate_inv_fmt=rate_inv_fmt, 
         elapsed=elapsed_str, 
         elapsed_s=elapsed, remaining=remaining_str, 
         remaining_s=remaining, l_bar=l_bar, 
         r_bar=r_bar, desc=prefix or '', 
         postfix=postfix, unit=unit, **extra_kwargs)
        if total:
            frac = n / total
            percentage = frac * 100
            l_bar += '{0:3.0f}%|'.format(percentage)
            if ncols == 0:
                return l_bar[:-1] + r_bar[1:]
            if bar_format:
                format_dict.update(l_bar=l_bar, percentage=percentage)
                if not prefix:
                    bar_format = bar_format.replace('{desc}: ', '')
                if '{bar}' in bar_format:
                    l_bar_user, r_bar_user = bar_format.split('{bar}')
                    l_bar = (l_bar_user.format)(**format_dict)
                    r_bar = (r_bar_user.format)(**format_dict)
                else:
                    return (bar_format.format)(**format_dict)
            if ncols:
                N_BARS = max(1, ncols - len(RE_ANSI.sub('', l_bar + r_bar)))
            else:
                N_BARS = 10
            if ascii is True:
                ascii = ASCII_FMT
            else:
                if ascii is False:
                    ascii = UTF_FMT
                nsyms = len(ascii) - 1
                bar_length, frac_bar_length = divmod(int(frac * N_BARS * nsyms), nsyms)
                bar = ascii[(-1)] * bar_length
                frac_bar = ascii[frac_bar_length]
                if bar_length < N_BARS:
                    full_bar = bar + frac_bar + ascii[0] * (N_BARS - bar_length - 1)
                else:
                    full_bar = bar + ascii[0] * (N_BARS - bar_length)
            return l_bar + full_bar + r_bar
        else:
            if bar_format:
                return (bar_format.format)(bar='?', **format_dict)
            return (prefix + ': ' if prefix else '') + '{0}{1} [{2}, {3}{4}]'.format(n_fmt, unit, elapsed_str, rate_fmt, postfix)

    def __new__(cls, *args, **kwargs):
        instance = object.__new__(cls)
        with cls.get_lock():
            if not hasattr(cls, '_instances'):
                cls._instances = WeakSet()
            cls._instances.add(instance)
            if cls.monitor_interval:
                if cls.monitor is None or not cls.monitor.report():
                    try:
                        cls.monitor = TMonitor(cls, cls.monitor_interval)
                    except Exception as e:
                        warn('tqdm:disabling monitor support (monitor_interval = 0) due to:\n' + str(e), TqdmMonitorWarning)
                        cls.monitor_interval = 0

        return instance

    @classmethod
    def _get_free_pos(cls, instance=None):
        """Skips specified instance."""
        positions = set(abs(inst.pos) for inst in cls._instances if inst is not instance if hasattr(inst, 'pos'))
        return min(set(range(len(positions) + 1)).difference(positions))

    @classmethod
    def _decr_instances(cls, instance):
        """
        Remove from list and reposition other bars
        so that newer bars won't overlap previous bars
        """
        with cls._lock:
            try:
                cls._instances.remove(instance)
            except KeyError:
                pass

            if not instance.gui:
                for inst in cls._instances:
                    if hasattr(inst, 'pos') and inst.pos > abs(instance.pos):
                        inst.pos -= 1

            if not cls._instances:
                if cls.monitor:
                    try:
                        cls.monitor.exit()
                        del cls.monitor
                    except AttributeError:
                        pass
                    else:
                        cls.monitor = None

    @classmethod
    def write(cls, s, file=None, end='\n', nolock=False):
        """Print a message via tqdm (without overlap with bars)."""
        fp = file if file is not None else sys.stdout
        with cls.external_write_mode(file=file, nolock=nolock):
            fp.write(s)
            fp.write(end)

    @classmethod
    @contextmanager
    def external_write_mode(cls, file=None, nolock=False):
        """
        Disable tqdm within context and refresh tqdm when exits.
        Useful when writing to standard output stream
        """
        fp = file if file is not None else sys.stdout
        if not nolock:
            cls.get_lock().acquire()
        inst_cleared = []
        for inst in getattr(cls, '_instances', []):
            if hasattr(inst, 'start_t') and (inst.fp == fp or all(f in (sys.stdout, sys.stderr) for f in (fp, inst.fp))):
                inst.clear(nolock=True)
                inst_cleared.append(inst)

        yield
        for inst in inst_cleared:
            inst.refresh(nolock=True)

        if not nolock:
            cls._lock.release()

    @classmethod
    def set_lock(cls, lock):
        """Set the global lock."""
        cls._lock = lock

    @classmethod
    def get_lock(cls):
        """Get the global lock. Construct it if it does not exist."""
        if not hasattr(cls, '_lock'):
            cls._lock = TqdmDefaultWriteLock()
        return cls._lock

    @classmethod
    def pandas(tclass, *targs, **tkwargs):
        """
        Registers the given `tqdm` class with
            pandas.core.
            ( frame.DataFrame
            | series.Series
            | groupby.DataFrameGroupBy
            | groupby.SeriesGroupBy
            ).progress_apply

        A new instance will be create every time `progress_apply` is called,
        and each instance will automatically close() upon completion.

        Parameters
        ----------
        targs, tkwargs  : arguments for the tqdm instance

        Examples
        --------
        >>> import pandas as pd
        >>> import numpy as np
        >>> from tqdm import tqdm, tqdm_gui
        >>>
        >>> df = pd.DataFrame(np.random.randint(0, 100, (100000, 6)))
        >>> tqdm.pandas(ncols=50)  # can use tqdm_gui, optional kwargs, etc
        >>> # Now you can use `progress_apply` instead of `apply`
        >>> df.groupby(0).progress_apply(lambda x: x**2)

        References
        ----------
        https://stackoverflow.com/questions/18603270/
        progress-indicator-during-pandas-operations-python
        """
        from pandas.core.frame import DataFrame
        from pandas.core.series import Series
        from pandas import Panel
        try:
            from pandas.core.window import _Rolling_and_Expanding
        except ImportError:
            _Rolling_and_Expanding = None

        try:
            from pandas.core.groupby.groupby import DataFrameGroupBy, SeriesGroupBy, GroupBy, PanelGroupBy
        except ImportError:
            from pandas.core.groupby import DataFrameGroupBy, SeriesGroupBy, GroupBy, PanelGroupBy

        deprecated_t = [
         tkwargs.pop('deprecated_t', None)]

        def inner_generator(df_function='apply'):

            def inner(df, func, *args, **kwargs):
                total = tkwargs.pop('total', getattr(df, 'ngroups', None))
                if total is None:
                    if df_function == 'applymap':
                        total = df.size
                    else:
                        if isinstance(df, Series):
                            total = len(df)
                        elif _Rolling_and_Expanding is None or not isinstance(df, _Rolling_and_Expanding):
                            axis = kwargs.get('axis', 0)
                            if axis == 'index':
                                axis = 0
                            else:
                                if axis == 'columns':
                                    axis = 1
                                total = df.size // df.shape[axis]
                else:
                    if deprecated_t[0] is not None:
                        t = deprecated_t[0]
                        deprecated_t[0] = None
                    else:
                        t = tclass(targs, total=total, **tkwargs)
                if len(args) > 0:
                    TqdmDeprecationWarning('Except func, normal arguments are intentionally not supported by `(DataFrame|Series|GroupBy).progress_apply`. Use keyword arguments instead.',
                      fp_write=(getattr(t.fp, 'write', sys.stderr.write)))

                def wrapper(*args, **kwargs):
                    t.update(n=(1 if not t.total or t.n < t.total else 0))
                    return func(*args, **kwargs)

                result = (getattr(df, df_function))(wrapper, **kwargs)
                t.close()
                return result

            return inner

        Series.progress_apply = inner_generator()
        SeriesGroupBy.progress_apply = inner_generator()
        Series.progress_map = inner_generator('map')
        SeriesGroupBy.progress_map = inner_generator('map')
        DataFrame.progress_apply = inner_generator()
        DataFrameGroupBy.progress_apply = inner_generator()
        DataFrame.progress_applymap = inner_generator('applymap')
        Panel.progress_apply = inner_generator()
        PanelGroupBy.progress_apply = inner_generator()
        GroupBy.progress_apply = inner_generator()
        GroupBy.progress_aggregate = inner_generator('aggregate')
        GroupBy.progress_transform = inner_generator('transform')
        if _Rolling_and_Expanding is not None:
            _Rolling_and_Expanding.progress_apply = inner_generator()

    def __init__(self, iterable=None, desc=None, total=None, leave=True, file=None, ncols=None, mininterval=0.1, maxinterval=10.0, miniters=None, ascii=None, disable=False, unit='it', unit_scale=False, dynamic_ncols=False, smoothing=0.3, bar_format=None, initial=0, position=None, postfix=None, unit_divisor=1000, write_bytes=None, gui=False, **kwargs):
        """
        Parameters
        ----------
        iterable  : iterable, optional
            Iterable to decorate with a progressbar.
            Leave blank to manually manage the updates.
        desc  : str, optional
            Prefix for the progressbar.
        total  : int, optional
            The number of expected iterations. If unspecified,
            len(iterable) is used if possible. If float("inf") or as a last
            resort, only basic progress statistics are displayed
            (no ETA, no progressbar).
            If `gui` is True and this parameter needs subsequent updating,
            specify an initial arbitrary large positive integer,
            e.g. int(9e9).
        leave  : bool, optional
            If [default: True], keeps all traces of the progressbar
            upon termination of iteration.
        file  : `io.TextIOWrapper` or `io.StringIO`, optional
            Specifies where to output the progress messages
            (default: sys.stderr). Uses `file.write(str)` and `file.flush()`
            methods.  For encoding, see `write_bytes`.
        ncols  : int, optional
            The width of the entire output message. If specified,
            dynamically resizes the progressbar to stay within this bound.
            If unspecified, attempts to use environment width. The
            fallback is a meter width of 10 and no limit for the counter and
            statistics. If 0, will not print any meter (only stats).
        mininterval  : float, optional
            Minimum progress display update interval [default: 0.1] seconds.
        maxinterval  : float, optional
            Maximum progress display update interval [default: 10] seconds.
            Automatically adjusts `miniters` to correspond to `mininterval`
            after long display update lag. Only works if `dynamic_miniters`
            or monitor thread is enabled.
        miniters  : int, optional
            Minimum progress display update interval, in iterations.
            If 0 and `dynamic_miniters`, will automatically adjust to equal
            `mininterval` (more CPU efficient, good for tight loops).
            If > 0, will skip display of specified number of iterations.
            Tweak this and `mininterval` to get very efficient loops.
            If your progress is erratic with both fast and slow iterations
            (network, skipping items, etc) you should set miniters=1.
        ascii  : bool or str, optional
            If unspecified or False, use unicode (smooth blocks) to fill
            the meter. The fallback is to use ASCII characters " 123456789#".
        disable  : bool, optional
            Whether to disable the entire progressbar wrapper
            [default: False]. If set to None, disable on non-TTY.
        unit  : str, optional
            String that will be used to define the unit of each iteration
            [default: it].
        unit_scale  : bool or int or float, optional
            If 1 or True, the number of iterations will be reduced/scaled
            automatically and a metric prefix following the
            International System of Units standard will be added
            (kilo, mega, etc.) [default: False]. If any other non-zero
            number, will scale `total` and `n`.
        dynamic_ncols  : bool, optional
            If set, constantly alters `ncols` to the environment (allowing
            for window resizes) [default: False].
        smoothing  : float, optional
            Exponential moving average smoothing factor for speed estimates
            (ignored in GUI mode). Ranges from 0 (average speed) to 1
            (current/instantaneous speed) [default: 0.3].
        bar_format  : str, optional
            Specify a custom bar string formatting. May impact performance.
            [default: '{l_bar}{bar}{r_bar}'], where
            l_bar='{desc}: {percentage:3.0f}%|' and
            r_bar='| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, '
              '{rate_fmt}{postfix}]'
            Possible vars: l_bar, bar, r_bar, n, n_fmt, total, total_fmt,
              percentage, rate, rate_fmt, rate_noinv, rate_noinv_fmt,
              rate_inv, rate_inv_fmt, elapsed, elapsed_s, remaining,
              remaining_s, desc, postfix, unit.
            Note that a trailing ": " is automatically removed after {desc}
            if the latter is empty.
        initial  : int, optional
            The initial counter value. Useful when restarting a progress
            bar [default: 0].
        position  : int, optional
            Specify the line offset to print this bar (starting from 0)
            Automatic if unspecified.
            Useful to manage multiple bars at once (eg, from threads).
        postfix  : dict or *, optional
            Specify additional stats to display at the end of the bar.
            Calls `set_postfix(**postfix)` if possible (dict).
        unit_divisor  : float, optional
            [default: 1000], ignored unless `unit_scale` is True.
        write_bytes  : bool, optional
            If (default: None) and `file` is unspecified,
            bytes will be written in Python 2. If `True` will also write
            bytes. In all other cases will default to unicode.
        gui  : bool, optional
            WARNING: internal parameter - do not use.
            Use tqdm_gui(...) instead. If set, will attempt to use
            matplotlib animations for a graphical output [default: False].

        Returns
        -------
        out  : decorated iterator.
        """
        if write_bytes is None:
            write_bytes = file is None and sys.version_info < (3, )
        else:
            if file is None:
                file = sys.stderr
            elif write_bytes:
                file = SimpleTextIOWrapper(file,
                  encoding=(getattr(file, 'encoding', None) or 'utf-8'))
            elif disable is None:
                if hasattr(file, 'isatty'):
                    if not file.isatty():
                        disable = True
                    else:
                        if total is None:
                            if iterable is not None:
                                try:
                                    total = len(iterable)
                                except (TypeError, AttributeError):
                                    total = None

                            else:
                                if total == float('inf'):
                                    total = None
                                if disable:
                                    self.iterable = iterable
                                    self.disable = disable
                                    with self._lock:
                                        self.pos = self._get_free_pos(self)
                                        self._instances.remove(self)
                                    self.n = initial
                                    self.total = total
                                    return
                            if kwargs:
                                self.disable = True
                                with self._lock:
                                    self.pos = self._get_free_pos(self)
                                    self._instances.remove(self)
                                from textwrap import dedent
                                raise TqdmDeprecationWarning((dedent('                       `nested` is deprecated and automated.\n                       Use `position` instead for manual control.\n                       ')), fp_write=(getattr(file, 'write', sys.stderr.write))) if 'nested' in kwargs else TqdmKeyError('Unknown argument(s): ' + str(kwargs))
                        else:
                            if ncols is None and file in (sys.stderr, sys.stdout) or dynamic_ncols:
                                if dynamic_ncols:
                                    dynamic_ncols = _environ_cols_wrapper()
                                    if dynamic_ncols:
                                        ncols = dynamic_ncols(file)
                                else:
                                    _dynamic_ncols = _environ_cols_wrapper()
                                    if _dynamic_ncols:
                                        ncols = _dynamic_ncols(file)
                            if miniters is None:
                                miniters = 0
                                dynamic_miniters = True
                            else:
                                dynamic_miniters = False
                        if mininterval is None:
                            mininterval = 0
                    if maxinterval is None:
                        maxinterval = 0
                else:
                    if ascii is None:
                        ascii = not _supports_unicode(file)
                    if bar_format:
                        if not (ascii is True or _is_ascii(ascii)):
                            bar_format = _unicode(bar_format)
            else:
                if smoothing is None:
                    smoothing = 0
                self.iterable = iterable
                self.desc = desc or ''
                self.total = total
                self.leave = leave
                self.fp = file
                self.ncols = ncols
                self.mininterval = mininterval
                self.maxinterval = maxinterval
                self.miniters = miniters
                self.dynamic_miniters = dynamic_miniters
                self.ascii = ascii
                self.disable = disable
                self.unit = unit
                self.unit_scale = unit_scale
                self.unit_divisor = unit_divisor
                self.gui = gui
                self.dynamic_ncols = dynamic_ncols
                self.smoothing = smoothing
                self.avg_time = None
                self._time = time
                self.bar_format = bar_format
                self.postfix = None
                if postfix:
                    try:
                        (self.set_postfix)(refresh=False, **postfix)
                    except TypeError:
                        self.postfix = postfix

            self.last_print_n = initial
            self.n = initial
            with self._lock:
                if position is None:
                    self.pos = self._get_free_pos(self)
                else:
                    self.pos = -position
            if not gui:
                self.sp = self.status_printer(self.fp)
                with self._lock:
                    self.display()
        self.last_print_t = self._time()
        self.start_t = self.last_print_t

    def __bool__(self):
        if self.total is not None:
            return self.total > 0
        else:
            if self.iterable is None:
                raise TypeError('bool() undefined when iterable == total == None')
            return bool(self.iterable)

    def __nonzero__(self):
        return self.__bool__()

    def __len__(self):
        if self.iterable is None:
            return self.total
        else:
            if hasattr(self.iterable, 'shape'):
                return self.iterable.shape[0]
            if hasattr(self.iterable, '__len__'):
                return len(self.iterable)
            return getattr(self, 'total', None)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
        return False

    def __del__(self):
        self.close()

    def __repr__(self):
        return (self.format_meter)(**self.format_dict)

    @property
    def _comparable(self):
        return abs(getattr(self, 'pos', 2147483648))

    def __hash__(self):
        return id(self)

    def __iter__(self):
        """Backward-compatibility to use: for x in tqdm(iterable)"""
        iterable = self.iterable
        if self.disable:
            for obj in iterable:
                yield obj

        else:
            mininterval = self.mininterval
            maxinterval = self.maxinterval
            miniters = self.miniters
            dynamic_miniters = self.dynamic_miniters
            last_print_t = self.last_print_t
            last_print_n = self.last_print_n
            n = self.n
            smoothing = self.smoothing
            avg_time = self.avg_time
            _time = self._time
            if not hasattr(self, 'sp'):
                from textwrap import dedent
                raise TqdmDeprecationWarning((dedent('                Please use `tqdm_gui(...)` instead of `tqdm(..., gui=True)`\n                ')),
                  fp_write=(getattr(self.fp, 'write', sys.stderr.write)))
            for obj in iterable:
                yield obj
                n += 1
                if n - last_print_n >= self.miniters:
                    miniters = self.miniters
                    delta_t = _time() - last_print_t
                    if delta_t >= mininterval:
                        cur_t = _time()
                        delta_it = n - last_print_n
                        if smoothing and delta_t and delta_it:
                            rate = delta_t / delta_it
                            avg_time = self.ema(rate, avg_time, smoothing)
                            self.avg_time = avg_time
                        self.n = n
                        with self._lock:
                            self.display()
                        if dynamic_miniters:
                            if maxinterval:
                                if delta_t >= maxinterval:
                                    if mininterval:
                                        miniters = delta_it * mininterval / delta_t
                                    else:
                                        miniters = delta_it * maxinterval / delta_t
                            else:
                                if smoothing:
                                    rate = delta_it
                                    if mininterval:
                                        if delta_t:
                                            rate *= mininterval / delta_t
                                    miniters = self.ema(rate, miniters, smoothing)
                                else:
                                    miniters = max(miniters, delta_it)
                        self.n = self.last_print_n = last_print_n = n
                        self.last_print_t = last_print_t = cur_t
                        self.miniters = miniters

            self.last_print_n = last_print_n
            self.n = n
            self.miniters = miniters
            self.close()

    def update(self, n=1):
        """
        Manually update the progress bar, useful for streams
        such as reading files.
        E.g.:
        >>> t = tqdm(total=filesize) # Initialise
        >>> for current_buffer in stream:
        ...    ...
        ...    t.update(len(current_buffer))
        >>> t.close()
        The last line is highly recommended, but possibly not necessary if
        `t.update()` will be called in such a way that `filesize` will be
        exactly reached and printed.

        Parameters
        ----------
        n  : int, optional
            Increment to add to the internal counter of iterations
            [default: 1].
        """
        if self.disable:
            return
        else:
            if n < 0:
                self.last_print_n += n
            self.n += n
            if self.n - self.last_print_n >= self.miniters:
                delta_t = self._time() - self.last_print_t
                if delta_t >= self.mininterval:
                    cur_t = self._time()
                    delta_it = self.n - self.last_print_n
                    if self.smoothing:
                        if delta_t:
                            if delta_it:
                                rate = delta_t / delta_it
                                self.avg_time = self.ema(rate, self.avg_time, self.smoothing)
                    if not hasattr(self, 'sp'):
                        from textwrap import dedent
                        raise TqdmDeprecationWarning((dedent('                    Please use `tqdm_gui(...)` instead of `tqdm(..., gui=True)`\n                    ')),
                          fp_write=(getattr(self.fp, 'write', sys.stderr.write)))
                    with self._lock:
                        self.display()
                    if self.dynamic_miniters:
                        if self.maxinterval:
                            if delta_t >= self.maxinterval:
                                if self.mininterval:
                                    self.miniters = delta_it * self.mininterval / delta_t
                                else:
                                    self.miniters = delta_it * self.maxinterval / delta_t
                        else:
                            if self.smoothing:
                                self.miniters = self.smoothing * delta_it * self.mininterval / delta_t if (self.mininterval and delta_t) else 1 + (1 - self.smoothing) * self.miniters
                            else:
                                self.miniters = max(self.miniters, delta_it)
                    self.last_print_n = self.n
                    self.last_print_t = cur_t

    def close(self):
        """Cleanup and (if leave=False) close the progressbar."""
        if self.disable:
            return
        else:
            self.disable = True
            pos = abs(self.pos)
            self._decr_instances(self)
            if not hasattr(self, 'sp'):
                return

            def fp_write(s):
                self.fp.write(_unicode(s))

            try:
                fp_write('')
            except ValueError as e:
                if 'closed' in str(e):
                    return
                raise

        with self._lock:
            if self.leave:
                if self.last_print_n < self.n:
                    self.avg_time = None
                    self.display(pos=pos)
                if not max([abs(getattr(i, 'pos', 0)) for i in self._instances] + [pos]):
                    fp_write('\n')
            else:
                self.display(msg='', pos=pos)
            if not pos:
                fp_write('\r')

    def clear(self, nolock=False):
        """Clear current bar display."""
        if self.disable:
            return
        else:
            if not nolock:
                self._lock.acquire()
            self.moveto(abs(self.pos))
            self.sp('')
            self.fp.write('\r')
            self.moveto(-abs(self.pos))
            if not nolock:
                self._lock.release()

    def refresh(self, nolock=False):
        """Force refresh the display of this bar."""
        if self.disable:
            return
        else:
            if not nolock:
                self._lock.acquire()
            self.display()
            if not nolock:
                self._lock.release()

    def unpause(self):
        """Restart tqdm timer from last print time."""
        cur_t = self._time()
        self.start_t += cur_t - self.last_print_t
        self.last_print_t = cur_t

    def reset(self, total=None):
        """
        Resets to 0 iterations for repeated use.

        Consider combining with `leave=True`.

        Parameters
        ----------
        total  : int, optional. Total to use for the new bar.
        """
        self.last_print_n = self.n = 0
        self.last_print_t = self.start_t = self._time()
        if total is not None:
            self.total = total
        self.refresh()

    def set_description(self, desc=None, refresh=True):
        """
        Set/modify description of the progress bar.

        Parameters
        ----------
        desc  : str, optional
        refresh  : bool, optional
            Forces refresh [default: True].
        """
        self.desc = desc + ': ' if desc else ''
        if refresh:
            self.refresh()

    def set_description_str(self, desc=None, refresh=True):
        """Set/modify description without ': ' appended."""
        self.desc = desc or ''
        if refresh:
            self.refresh()

    def set_postfix(self, ordered_dict=None, refresh=True, **kwargs):
        """
        Set/modify postfix (additional stats)
        with automatic formatting based on datatype.

        Parameters
        ----------
        ordered_dict  : dict or OrderedDict, optional
        refresh  : bool, optional
            Forces refresh [default: True].
        kwargs  : dict, optional
        """
        postfix = _OrderedDict([] if ordered_dict is None else ordered_dict)
        for key in sorted(kwargs.keys()):
            postfix[key] = kwargs[key]

        for key in postfix.keys():
            if isinstance(postfix[key], Number):
                postfix[key] = self.format_num(postfix[key])
            else:
                if not isinstance(postfix[key], _basestring):
                    postfix[key] = str(postfix[key])

        self.postfix = ', '.join(key + '=' + postfix[key].strip() for key in postfix.keys())
        if refresh:
            self.refresh()

    def set_postfix_str(self, s='', refresh=True):
        """
        Postfix without dictionary expansion, similar to prefix handling.
        """
        self.postfix = str(s)
        if refresh:
            self.refresh()

    def moveto(self, n):
        self.fp.write(_unicode('\n' * n + _term_move_up() * -n))
        self.fp.flush()

    @property
    def format_dict(self):
        """Public API for read-only member access."""
        return dict(n=(self.n),
          total=(self.total),
          elapsed=(self._time() - self.start_t if hasattr(self, 'start_t') else 0),
          ncols=(self.dynamic_ncols(self.fp) if self.dynamic_ncols else self.ncols),
          prefix=(self.desc),
          ascii=(self.ascii),
          unit=(self.unit),
          unit_scale=(self.unit_scale),
          rate=(1 / self.avg_time if self.avg_time else None),
          bar_format=(self.bar_format),
          postfix=(self.postfix),
          unit_divisor=(self.unit_divisor))

    def display(self, msg=None, pos=None):
        """
        Use `self.sp` to display `msg` in the specified `pos`.

        Consider overloading this function when inheriting to use e.g.:
        `self.some_frontend(**self.format_dict)` instead of `self.sp`.

        Parameters
        ----------
        msg  : str, optional. What to display (default: `repr(self)`).
        pos  : int, optional. Position to `moveto`
          (default: `abs(self.pos)`).
        """
        if pos is None:
            pos = abs(self.pos)
        else:
            if pos:
                self.moveto(pos)
            self.sp(self.__repr__() if msg is None else msg)
            if pos:
                self.moveto(-pos)


def trange(*args, **kwargs):
    """
    A shortcut for tqdm(xrange(*args), **kwargs).
    On Python3+ range is used instead of xrange.
    """
    return tqdm(_range(*args), **kwargs)