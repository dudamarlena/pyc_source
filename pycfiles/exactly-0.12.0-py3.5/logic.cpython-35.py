# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/definitions/logic.py
# Compiled at: 2020-01-31 11:01:50
# Size of source mod 2**32: 553 bytes
from exactly_lib.util.logic_types import Quantifier
NOT_OPERATOR_NAME = '!'
AND_OPERATOR_NAME = '&&'
OR_OPERATOR_NAME = '||'
FALSE = 'false'
TRUE = 'true'
BOOLEANS = {False: FALSE, 
 True: TRUE}
BOOLEANS_STRINGS = {item[1]:item[0] for item in BOOLEANS.items()}
CONSTANT_MATCHER = 'constant'
ALL_QUANTIFIER_ARGUMENT = 'every'
EXISTS_QUANTIFIER_ARGUMENT = 'any'
QUANTIFICATION_SEPARATOR_ARGUMENT = ':'
QUANTIFIER_ARGUMENTS = {Quantifier.ALL: ALL_QUANTIFIER_ARGUMENT, 
 Quantifier.EXISTS: EXISTS_QUANTIFIER_ARGUMENT}