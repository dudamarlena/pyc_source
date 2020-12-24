# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/dbmanagr/__init__.py
# Compiled at: 2015-10-11 07:17:06
__drivers__ = []
KIND_VALUE = 'value'
KIND_FOREIGN_KEY = 'foreign-key'
KIND_FOREIGN_VALUE = 'foreign-value'
IMAGE_VALUE = 'images/value.png'
IMAGE_FOREIGN_KEY = 'images/foreign-key.png'
IMAGE_FOREIGN_VALUE = 'images/foreign-value.png'
OPTION_URI_SINGLE_ROW_FORMAT = '%s%s/?%s'
OPTION_URI_MULTIPLE_ROWS_FORMAT = '%s%s?%s'
OPERATORS = {'=': lambda c, v: c.__eq__(v), 
   '!=': lambda c, v: c.__ne__(v), 
   '~': lambda c, v: c.like(v), 
   '*': lambda c, v: c.like(v), 
   '>': lambda c, v: c.__gt__(v), 
   '>=': lambda c, v: c.__ge__(v), 
   '<=': lambda c, v: c.__le__(v), 
   '<': lambda c, v: c.__lt__(v), 
   'in': lambda c, v: c.in_(v), 
   ':': lambda c, v: c.in_(v)}