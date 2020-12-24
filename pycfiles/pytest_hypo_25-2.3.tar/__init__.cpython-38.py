# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\__init__.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 1582 bytes
"""Hypothesis is a library for writing unit tests which are parametrized by
some source of data.

It verifies your code against a wide range of input and minimizes any
failing examples it finds.
"""
import hypothesis._error_if_old
from hypothesis._settings import HealthCheck, Phase, Verbosity, settings
from hypothesis.control import assume, event, note, reject, target
from hypothesis.core import example, find, given, reproduce_failure, seed
from hypothesis.internal.entropy import register_random
from hypothesis.utils.conventions import infer
from hypothesis.version import __version__, __version_info__
__all__ = [
 'settings',
 'Verbosity',
 'HealthCheck',
 'Phase',
 'assume',
 'reject',
 'seed',
 'given',
 'reproduce_failure',
 'find',
 'example',
 'note',
 'event',
 'infer',
 'register_random',
 'target',
 '__version__',
 '__version_info__']