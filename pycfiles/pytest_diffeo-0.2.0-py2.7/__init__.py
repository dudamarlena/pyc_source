# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pytest_diffeo/__init__.py
# Compiled at: 2016-04-08 13:51:41
"""Support code for py.test tests.

This module includes support code that defines common command-line options
and provides other common infrastructure for tests.

-----

This software is released under an MIT/X11 open source license.

Copyright 2012-2014 Diffeo, Inc.

"""
from __future__ import absolute_import
from pytest_diffeo.args import pytest_addoption, pytest_configure, pytest_runtest_setup, pytest_runtest_teardown, third_dir, external_data, redis_address, ingest_v2, elastic_address
from pytest_diffeo.namespace import make_namespace_string, namespace_string