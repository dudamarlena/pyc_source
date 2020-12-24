# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc7229.py
# Compiled at: 2019-10-17 01:03:15
from pyasn1.type import univ
id_pkix = univ.ObjectIdentifier('1.3.6.1.5.5.7')
id_TEST = id_pkix + (13, )
id_TEST_certPolicyOne = id_TEST + (1, )
id_TEST_certPolicyTwo = id_TEST + (2, )
id_TEST_certPolicyThree = id_TEST + (3, )
id_TEST_certPolicyFour = id_TEST + (4, )
id_TEST_certPolicyFive = id_TEST + (5, )
id_TEST_certPolicySix = id_TEST + (6, )
id_TEST_certPolicySeven = id_TEST + (7, )
id_TEST_certPolicyEight = id_TEST + (8, )