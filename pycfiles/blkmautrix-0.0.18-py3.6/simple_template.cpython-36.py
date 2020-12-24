# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mautrix/util/simple_template.py
# Compiled at: 2019-11-21 01:01:47
# Size of source mod 2**32: 1495 bytes
from typing import Optional, Type, Generic, TypeVar
T = TypeVar('T')

class SimpleTemplate(Generic[T]):
    _template: str
    _keyword: str
    _prefix: str
    _suffix: str
    _type: Type[T]

    def __init__(self, template: str, keyword: str, prefix: str='', suffix: str='', type: Type[T]=str) -> None:
        self._template = template
        self._keyword = keyword
        index = self._template.find('{%s}' % keyword)
        length = len(keyword) + 2
        self._prefix = prefix + self._template[:index]
        self._suffix = self._template[index + length:] + suffix
        self._type = type

    def format(self, arg: T) -> str:
        return (self._template.format)(**{self._keyword: arg})

    def format_full(self, arg: T) -> str:
        return f"{self._prefix}{arg}{self._suffix}"

    def parse(self, val: str) -> Optional[T]:
        prefix_ok = val[:len(self._prefix)] == self._prefix
        has_suffix = len(self._suffix) > 0
        suffix_ok = not has_suffix or val[-len(self._suffix):] == self._suffix
        if prefix_ok:
            if suffix_ok:
                start = len(self._prefix)
                end = -len(self._suffix) if has_suffix else len(val)
                return self._type(val[start:end])