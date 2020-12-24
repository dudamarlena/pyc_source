# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mongolia/constants.py
# Compiled at: 2017-02-10 15:15:18
# Size of source mod 2**32: 3201 bytes
"""
The MIT License (MIT)

Copyright (c) 2015 Zagaran, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

@author: Zags (Benjamin Zagorsky)
"""
from bson import ObjectId
from datetime import datetime
from past.builtins import basestring
ID_KEY = '_id'
INC = '$inc'
GT = '$gt'
SET = '$set'
TYPES_TO_CHECK = [
 basestring, int, float, list, dict]
REQUIRED = '__required__'
REQUIRED_STRING = '__required__string'
REQUIRED_INT = '__required__int'
REQUIRED_FLOAT = '__required__float'
REQUIRED_LIST = '__required__list'
REQUIRED_DICT = '__required__dict'
REQUIRED_DATETIME = '__required__datetime'
REQUIRED_OBJECTID = '__required__object_id'
REQUIRED_VALUES = [
 REQUIRED, REQUIRED_STRING, REQUIRED_INT, REQUIRED_FLOAT,
 REQUIRED_LIST, REQUIRED_DICT, REQUIRED_DATETIME, REQUIRED_OBJECTID]
REQUIRED_TYPES = {REQUIRED_STRING: basestring, 
 REQUIRED_INT: int, 
 REQUIRED_FLOAT: float, 
 REQUIRED_LIST: list, 
 REQUIRED_DICT: dict, 
 REQUIRED_DATETIME: datetime, 
 REQUIRED_OBJECTID: ObjectId}
UPDATE = '__update__'
CHILD_TEMPLATE = 'CHILD_TEMPLATE'
TEST_DATABASE_NAME = '__MONGOLIA_TEST_DATABASE__'