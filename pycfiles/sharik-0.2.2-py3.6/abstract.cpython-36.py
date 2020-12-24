# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sharik/abstract.py
# Compiled at: 2019-12-14 09:29:54
# Size of source mod 2**32: 304 bytes
from abc import ABC, abstractmethod
from pydantic.dataclasses import dataclass
from typing import Iterable, Tuple, Callable
ContentSupplier = Callable[([], bytes)]

@dataclass
class DataSource(ABC):

    @abstractmethod
    def provide_files(self) -> Iterable[Tuple[(str, ContentSupplier)]]:
        pass