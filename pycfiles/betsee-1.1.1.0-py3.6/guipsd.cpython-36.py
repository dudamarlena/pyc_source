# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/lib/pyside2/guipsd.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 2393 bytes
"""
Low-level :mod:`PySide2` facilities.
"""
import PySide2
from betse.util.io.log import logs
from betse.util.type.decorator.decmemo import func_cached
from betse.util.type.numeric import versions
from betse.util.type.types import type_check
from betsee.lib.pyside2.cache.guipsdcache import CachePolicy
VERSION = PySide2.__version__

@type_check
def init(cache_policy: CachePolicy) -> None:
    """
    Initialize :mod:`PySide2`.

    Specifically, this function:

    * Contextually caches all :mod:`PySide2`-based submodules required at
      runtime by this GUI.
    * Initializes PySide2-based multithreading facilities.

    Parameters
    ----------
    cache_policy : CachePolicy
        Type of :mod:`PySide2`-based submodule caching to be performed.
    """
    from betsee.lib.pyside2.cache import guipsdcache
    from betsee.util.thread import guithread
    logs.log_info('Initializing PySide2 %s...', VERSION)
    guipsdcache.init(cache_policy=cache_policy)
    guithread.init()


@func_cached
def is_version_5_6_or_older() -> bool:
    """
    ``True`` only if the currently installed version of :mod:`PySide2` targets
    the Qt 5.6 (LTS) line of stable releases or older (e.g., Qt 5.5.0, Qt
    5.6.1).

    Versions of :mod:`PySide2` targetting such obsolete releases are well-known
    to suffer a medley of critical defects, including:

    * The entire :mod:`pyside2uic` package, which converts working
      XML-formatted user interface (UIC) files into broken pure-Python modules.
      Naturally, this is bad.
    """
    return versions.is_less_than(VERSION, '5.7.0')