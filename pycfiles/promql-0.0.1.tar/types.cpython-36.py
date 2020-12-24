# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/filters/types.py
# Compiled at: 2019-08-15 23:53:38
# Size of source mod 2**32: 1515 bytes
from __future__ import unicode_literals
from six import with_metaclass
from collections import defaultdict
import weakref
__all__ = ('CLIFilter', 'SimpleFilter')
_instance_check_cache = defaultdict(weakref.WeakKeyDictionary)

class _FilterTypeMeta(type):

    def __instancecheck__(cls, instance):
        cache = _instance_check_cache[tuple(cls.arguments_list)]

        def get():
            if not hasattr(instance, 'test_args'):
                return False
            else:
                return (instance.test_args)(*cls.arguments_list)

        try:
            return cache[instance]
        except KeyError:
            result = get()
            cache[instance] = result
            return result


class _FilterType(with_metaclass(_FilterTypeMeta)):

    def __new__(cls):
        raise NotImplementedError('This class should not be initiated.')


class CLIFilter(_FilterType):
    """CLIFilter"""
    arguments_list = [
     'cli']


class SimpleFilter(_FilterType):
    """SimpleFilter"""
    arguments_list = []