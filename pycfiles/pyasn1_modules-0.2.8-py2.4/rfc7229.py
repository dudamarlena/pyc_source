# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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