# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kelvin.liu/Code/OSS/kforce/tests/unit/test_aws_facts.py
# Compiled at: 2018-02-17 06:37:50
# Size of source mod 2**32: 244 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os
from unittest import TestCase
from kforce.aws_facts import get_vpc_facts
from moto import mock_ec2

@mock_ec2
class TestAwsFacts(TestCase):

    def setUp(self):
        pass

    def test_check_rt_internet_facing(self):
        pass