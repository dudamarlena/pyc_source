# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stas/workspace/partners/flask_restframework/flask_restframework/__init__.py
# Compiled at: 2017-07-14 09:16:04
# Size of source mod 2**32: 499 bytes
"""

Serializer API
===================

.. automodule:: flask_restframework.serializer.base_serializer
    :members:

.. automodule:: flask_restframework.queryset_wrapper
    :members:

.. automodule:: flask_restframework.model_wrapper
    :members:

"""
__author__ = 'stas'
__version__ = '0.0.34'
from flask_restframework.serializer import BaseSerializer
from flask_restframework.serializer.model_serializer import ModelSerializer
from flask_restframework.queryset_wrapper import QuerysetWrapper