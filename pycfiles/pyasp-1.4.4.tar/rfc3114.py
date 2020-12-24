# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc3114.py
# Compiled at: 2020-01-09 12:20:13
from pyasn1.type import char
from pyasn1.type import namedval
from pyasn1.type import univ
from pyasn1_modules import rfc5755
id_smime = univ.ObjectIdentifier((1, 2, 840, 113549, 1, 9, 16))
id_tsp = id_smime + (7, )
id_tsp_TEST_Amoco = id_tsp + (1, )

class Amoco_SecurityClassification(univ.Integer):
    __module__ = __name__
    namedValues = namedval.NamedValues(('amoco-general', 6), ('amoco-confidential',
                                                              7), ('amoco-highly-confidential',
                                                                   8))


id_tsp_TEST_Caterpillar = id_tsp + (2, )

class Caterpillar_SecurityClassification(univ.Integer):
    __module__ = __name__
    namedValues = namedval.NamedValues(('caterpillar-public', 6), ('caterpillar-green',
                                                                   7), ('caterpillar-yellow',
                                                                        8), ('caterpillar-red',
                                                                             9))


id_tsp_TEST_Whirlpool = id_tsp + (3, )

class Whirlpool_SecurityClassification(univ.Integer):
    __module__ = __name__
    namedValues = namedval.NamedValues(('whirlpool-public', 6), ('whirlpool-internal',
                                                                 7), ('whirlpool-confidential',
                                                                      8))


id_tsp_TEST_Whirlpool_Categories = id_tsp + (4, )

class SecurityCategoryValues(univ.SequenceOf):
    __module__ = __name__
    componentType = char.UTF8String()


_securityCategoryMapUpdate = {id_tsp_TEST_Whirlpool_Categories: SecurityCategoryValues()}
rfc5755.securityCategoryMap.update(_securityCategoryMapUpdate)