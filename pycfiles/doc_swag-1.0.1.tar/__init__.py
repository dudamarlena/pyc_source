# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-dgUSur/flasgger/flasgger/__init__.py
# Compiled at: 2017-06-27 07:41:04
__version__ = '0.5.14'
__author__ = 'Bruno Rocha'
__email__ = 'rochacbruno@gmail.com'
from jsonschema import ValidationError
from .base import Swagger, NO_SANITIZER, BR_SANITIZER, MK_SANITIZER
from .utils import swag_from, validate