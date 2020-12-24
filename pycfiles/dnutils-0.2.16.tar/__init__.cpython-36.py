# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/code/dnutils/python3.5/dnutils/__init__.py
# Compiled at: 2019-05-17 08:53:57
# Size of source mod 2**32: 882 bytes
import os, sys
try:
    from . import _version
except ImportError:
    path, _ = os.path.split(__file__)
    print(path)
    sys.path.append(os.path.join(path, '..', '..'))
    import _version

from _version import __version__
__version__ = _version.__version__
__author__ = 'Daniel Nyga'
from .debug import out, stop, trace, stoptrace
from .tools import ifnone, ifnot, allnone, allnot, edict, idxif, first, last, LinearScale
from .signals import add_handler, rm_handler, enable_ctrlc
from .threads import Lock, RLock, Condition, Event, Semaphore, BoundedSemaphore, Barrier, Relay, Thread, SuspendableThread, sleep, waitabout, Timer
from .logs import loggers, newlogger, getlogger, DEBUG, INFO, WARNING, ERROR, CRITICAL, expose, inspect, active_exposures, exposure, set_exposure_dir
from .console import ProgressBar, StatusMsg, bf
enable_ctrlc()