# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/util/decorator_utils.py
# Compiled at: 2018-06-15 01:22:48
# Size of source mod 2**32: 3588 bytes
"""Utility functions for writing decorators (which modify docstrings)."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import sys

def get_qualified_name(function):
    if hasattr(function, '__qualname__'):
        return function.__qualname__
    if hasattr(function, 'im_class'):
        return function.im_class.__name__ + '.' + function.__name__
    return function.__name__


def _normalize_docstring(docstring):
    """Normalizes the docstring.

  Replaces tabs with spaces, removes leading and trailing blanks lines, and
  removes any indentation.

  Copied from PEP-257:
  https://www.python.org/dev/peps/pep-0257/#handling-docstring-indentation

  Args:
    docstring: the docstring to normalize

  Returns:
    The normalized docstring
  """
    if not docstring:
        return ''
    lines = docstring.expandtabs().splitlines()
    indent = sys.maxsize
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
            continue

    trimmed = [
     lines[0].strip()]
    if indent < sys.maxsize:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())

    while trimmed and not trimmed[(-1)]:
        trimmed.pop()

    while trimmed and not trimmed[0]:
        trimmed.pop(0)

    return '\n'.join(trimmed)


def add_notice_to_docstring(doc, instructions, no_doc_str, suffix_str, notice):
    """Adds a deprecation notice to a docstring."""
    if not doc:
        lines = [
         no_doc_str]
    else:
        lines = _normalize_docstring(doc).splitlines()
        lines[0] += ' ' + suffix_str
    notice = [''] + notice + [instructions]
    if len(lines) > 1:
        if lines[1].strip():
            notice.append('')
        lines[1:1] = notice
    else:
        lines += notice
    return '\n'.join(lines)


def validate_callable(func, decorator_name):
    if not hasattr(func, '__call__'):
        raise ValueError('%s is not a function. If this is a property, make sure @property appears before @%s in your source code:\n\n@property\n@%s\ndef method(...)' % (
         func, decorator_name, decorator_name))


class classproperty(object):
    __doc__ = "Class property decorator.\n\n  Example usage:\n\n  class MyClass(object):\n\n    @classproperty\n    def value(cls):\n      return '123'\n\n  > print MyClass.value\n  123\n  "

    def __init__(self, func):
        self._func = func

    def __get__(self, owner_self, owner_cls):
        return self._func(owner_cls)