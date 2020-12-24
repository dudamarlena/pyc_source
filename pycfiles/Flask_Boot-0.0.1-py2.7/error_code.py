# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/flask_boot/project/application/exception/error_code.py
# Compiled at: 2018-08-07 11:02:04
from __future__ import unicode_literals
DEV_METHOD_VALID = 40
DEV_CLASS_EXTENDS_ERR = 30
DEV_EXCEPTION_UNDEFINED_ERROR = 10
DATABASE_UNKNOWN_ERROR = 200
INVALID_ARGS = 1361
CODE_MSG = {DEV_CLASS_EXTENDS_ERR: b'抽象类<{class_name}> 必须先继承才能使用。', 
   DEV_METHOD_VALID: b'函数写法不符合要求。{msg}', 
   DEV_EXCEPTION_UNDEFINED_ERROR: b'异常码未定义', 
   DATABASE_UNKNOWN_ERROR: b'数据库未知错误', 
   INVALID_ARGS: b'请求参数不合法'}