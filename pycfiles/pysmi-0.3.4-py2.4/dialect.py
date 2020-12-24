# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysmi/parser/dialect.py
# Compiled at: 2018-12-29 12:21:47
smiV2 = {}
smiV1 = smiV2.copy()
smiV1.update(supportSmiV1Keywords=True, supportIndex=True)
smiV1Relaxed = smiV1.copy()
smiV1Relaxed.update(commaAtTheEndOfImport=True, commaAtTheEndOfSequence=True, mixOfCommasAndSpaces=True, uppercaseIdentifier=True, lowcaseIdentifier=True, curlyBracesAroundEnterpriseInTrap=True, noCells=True)