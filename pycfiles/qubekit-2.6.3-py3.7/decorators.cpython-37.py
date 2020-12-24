# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/QUBEKit/utils/decorators.py
# Compiled at: 2019-09-23 09:51:08
# Size of source mod 2**32: 8113 bytes
from QUBEKit.utils.helpers import pretty_print, unpickle, COLOURS
from datetime import datetime
from functools import wraps, partial
import logging, os
from time import time

def timer_func(orig_func):
    """
    Prints the runtime of a function when applied as a decorator (@timer_func).
    Currently only used for debugging.
    """

    @wraps(orig_func)
    def wrapper(*args, **kwargs):
        t1 = time()
        result = orig_func(*args, **kwargs)
        t2 = time() - t1
        print(f"{orig_func.__qualname__} ran in: {t2} seconds.")
        return result

    return wrapper


def timer_logger(orig_func):
    """
    Logs the various timings of a function in a dated and numbered file.
    Writes the start time, function / method qualname and docstring when function / method starts.
    Then outputs the runtime and time when function / method finishes.
    """

    @wraps(orig_func)
    def wrapper(*args, **kwargs):
        if len(args) >= 1 and hasattr(args[0], 'molecule'):
            if getattr(args[0].molecule, 'home') is None:
                return orig_func(*args, **kwargs)
            log_file_path = os.path.join(args[0].molecule.home, 'QUBEKit_log.txt')
        else:
            if not os.path.exists('../QUBEKit_log.txt'):
                return orig_func(*args, **kwargs)
            log_file_path = '../QUBEKit_log.txt'
        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        t1 = time()
        with open(log_file_path, 'a+') as (log_file):
            log_file.write(f"{orig_func.__qualname__} began at {start_time}.\n\n    ")
            log_file.write(f"Docstring for {orig_func.__qualname__}:\n    {orig_func.__doc__}\n\n")
            time_taken = time() - t1
            mins, secs = divmod(time_taken, 60)
            hours, mins = divmod(mins, 60)
            secs, remain = str(float(secs)).split('.')
            time_taken = f"{int(hours):02d}h:{int(mins):02d}m:{int(secs):02d}s.{remain[:5]}"
            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_file.write(f"{orig_func.__qualname__} finished in {time_taken} at {end_time}.\n\n")
            log_file.write(f"{'--------------------------------------------------'}\n\n")
        return orig_func(*args, **kwargs)

    return wrapper


def for_all_methods(decorator):
    """
    Applies a decorator to all methods of a class (includes sub-classes and init; it is literally all callables).
    This class decorator is applied using '@for_all_methods(timer_func)' for example.
    """

    @wraps(decorator)
    def decorate(cls):
        for attr in cls.__dict__:
            if callable(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))

        return cls

    return decorate


def logger_format(log_file):
    """
    Creates logging object to be returned.
    Contains proper formatting and locations for logging exceptions.
    This isn't a decorator itself but is only used by exception_logger so it makes sense for it to be here.
    """
    logger = logging.getLogger('Exception Logger')
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(log_file)
    fmt = '\n\n%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


def exception_logger(func):
    """
    Decorator which logs exceptions to QUBEKit_log.txt file if one occurs.
    Do not apply this decorator to a function / method unless a log file will exist in the working dir;
    doing so will just raise the exception as normal.

    On any Exception, the Ligand class objects which are taken from the pickle file are printed to the log file,
    then the full stack trace is printed to the log file as well.

    Currently, only Execute.run is decorated like this, as it will always have a log file.
    Decorating other functions this way is possible and won't break anything, but it is pointless.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BaseException as exc:
            try:
                home = getattr(args[0].molecule, 'home', None)
                state = getattr(args[0].molecule, 'state', None)
                if home is None or state is None:
                    raise
                mol = unpickle()[state]
                if getattr(args[0].molecule, 'verbose'):
                    pretty_print(mol, to_file=True, finished=False)
                log_file = os.path.join(home, 'QUBEKit_log.txt')
                logger = logger_format(log_file)
                logger.exception(f"\nAn exception occurred with: {func.__qualname__}\n")
                print(f"{COLOURS.red}\n\nAn exception occurred with: {func.__qualname__}{COLOURS.end}\nException: {exc}\nView the log file for details.")
                if isinstance(exc, SystemExit) or isinstance(exc, KeyboardInterrupt):
                    raise
                if len(args) >= 1:
                    if hasattr(args[0], 'molecule'):
                        if not hasattr(args[0].molecule, 'bulk_run'):
                            raise
                        if args[0].molecule.bulk_run is None:
                            raise
            finally:
                exc = None
                del exc

    return wrapper


class ExceptionLogger:
    __doc__ = 'Alternate implementation of exception logger functions above'

    def __init__(self, func):
        self.func = func
        self.log_file = None

    def __get__(self, instance, owner):
        """Allows decoration of functions and methods"""
        return partial(self.__call__, instance)

    def __call__(self, *args, **kwargs):
        try:
            return (self.func)(*args, **kwargs)
        except Exception as exc:
            try:
                home = getattr(args[0].molecule, 'home', None)
                state = getattr(args[0].molecule, 'state', None)
                if home is None or state is None:
                    raise
                mol = unpickle()[state]
                pretty_print(mol, to_file=True, finished=False)
                self.log_file = os.path.join(home, 'QUBEKit_log.txt')
                logger = self.logger_format()
                logger.exception(f"\nAn exception occurred with: {self.func.__qualname__}\n")
                print(f"\n\nAn exception occurred with: {self.func.__qualname__}\nException: {exc}\nView the log file for details.".upper())
                if len(args) >= 1:
                    if hasattr(args[0], 'molecule'):
                        if not hasattr(args[0].molecule, 'bulk_run'):
                            raise
                        if args[0].molecule.bulk_run is None:
                            raise
            finally:
                exc = None
                del exc

    def logger_format(self):
        logger = logging.getLogger('Exception Logger')
        logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler(self.log_file)
        fmt = '\n\n%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(fmt)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger