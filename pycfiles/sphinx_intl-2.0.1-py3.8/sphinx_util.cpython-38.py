# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: _build/bdist.macosx-10.15-x86_64/egg/sphinx_intl/sphinx_util.py
# Compiled at: 2020-04-19 02:09:17
# Size of source mod 2**32: 579 bytes
from typing import Iterator, List

class Tags(object):

    def __init__(self, tags: List[str]=None) -> None:
        self.tags = dict.fromkeys(tags or [], True)

    def has(self, tag: str) -> bool:
        return tag in self.tags

    __contains__ = has

    def __iter__(self) -> Iterator[str]:
        return iter(self.tags)

    def add(self, tag: str) -> None:
        self.tags[tag] = True

    def remove(self, tag: str) -> None:
        self.tags.pop(tag, None)