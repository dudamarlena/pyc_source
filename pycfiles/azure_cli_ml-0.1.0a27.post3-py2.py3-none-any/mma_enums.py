# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: F:\GitCode\trangevi-azurecli\azure\cli\command_modules\ml\_mma\models\mma_enums.py
# Compiled at: 2017-09-20 13:50:34
from enum import Enum

class SkuName(Enum):
    s1 = 'S1'
    s2 = 'S2'
    s3 = 'S3'
    dev_test = 'DevTest'