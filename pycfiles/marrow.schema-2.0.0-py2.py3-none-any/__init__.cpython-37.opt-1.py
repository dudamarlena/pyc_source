# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/schema/__init__.py
# Compiled at: 2018-12-02 18:40:17
# Size of source mod 2**32: 204 bytes
from .release import version as __version__
from .meta import Element
from .declarative import Container, DataAttribute, Attribute, CallbackAttribute
from .exc import Concern
from .util import Attributes