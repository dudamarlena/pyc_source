# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\reporting.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 1754 bytes
import inspect
from hypothesis._settings import Verbosity, settings
from hypothesis.internal.compat import escape_unicode_characters
from hypothesis.utils.dynamicvariables import DynamicVariable

def silent(value):
    pass


def default(value):
    try:
        print(value)
    except UnicodeEncodeError:
        print(escape_unicode_characters(value))


reporter = DynamicVariable(default)

def current_reporter():
    return reporter.value


def with_reporter(new_reporter):
    return reporter.with_value(new_reporter)


def current_verbosity():
    return settings.default.verbosity


def to_text(textish):
    if inspect.isfunction(textish):
        textish = textish()
    if isinstance(textish, bytes):
        textish = textish.decode('utf-8')
    return textish


def verbose_report(text):
    if current_verbosity() >= Verbosity.verbose:
        base_report(text)


def debug_report(text):
    if current_verbosity() >= Verbosity.debug:
        base_report(text)


def report(text):
    if current_verbosity() >= Verbosity.normal:
        base_report(text)


def base_report(text):
    current_reporter()(to_text(text))