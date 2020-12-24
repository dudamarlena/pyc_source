# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\Project\webapp\test\settings.py
# Compiled at: 2018-01-21 05:54:07
database = {'user': 'root', 
   'password': 'password', 
   'database': 'test', 
   'host': '127.0.0.1', 
   'port': '3306'}
app = ('views.index', 'views.admin')
middleware = ('middleware.PathAutoCompleter', )
debug = True