# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/tests/kyoka/domain/domain_validator_test.py
# Compiled at: 2016-09-17 04:18:17
from tests.base_unittest import BaseUnitTest
from kyoka.domain.base_domain import BaseDomain
from kyoka.domain.domain_validator import DomainValidator

class DomainValidatorTest(BaseUnitTest):

    def test_implementation_check(self):
        empty_domain = BaseDomain()
        validator = DomainValidator(empty_domain)
        status, msg = validator.implementation_check()
        self.false(status)
        self.include('generate_inital_state', msg)