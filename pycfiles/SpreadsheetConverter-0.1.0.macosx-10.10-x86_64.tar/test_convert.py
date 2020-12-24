# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/yugo/.virtualenvs/ssc/lib/python2.7/site-packages/tests/test_convert.py
# Compiled at: 2015-09-14 12:51:54
from __future__ import absolute_import
from __future__ import unicode_literals
import pytest
from spreadsheetconverter import Converter, YamlConfig
from spreadsheetconverter.exceptions import TargetFieldDoesNotExistError, ForeignkeyTargetDataDoesNotExistError

def test_convert():
    Converter(YamlConfig.get_config(b'dummy1.yaml')).run()
    Converter(YamlConfig.get_config(b'dummy2.yaml')).run()


def test_nothing_field_convert_error():
    with pytest.raises(TargetFieldDoesNotExistError):
        Converter(YamlConfig.get_config(b'nothing_field.yaml')).run()


def test_nothing_foreignkey_convert_error():
    with pytest.raises(ForeignkeyTargetDataDoesNotExistError):
        Converter(YamlConfig.get_config(b'nothing_foreignkey.yaml')).run()