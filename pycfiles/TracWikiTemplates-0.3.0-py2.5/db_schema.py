# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/WikiTemplates/db_schema.py
# Compiled at: 2007-11-10 06:34:56
from trac.core import *
from trac.db_default import Table, Column, Index
version = 1
schema = [
 Table('templates', key=('name', 'version'))[(
  Column('name'),
  Column('version', type='int'),
  Column('time', type='int'),
  Column('author'),
  Column('ipnr'),
  Column('text'),
  Column('comment'),
  Column('readonly', type='int'),
  Index(['time']))]]