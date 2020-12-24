# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/db/query_templates.py
# Compiled at: 2016-10-28 17:38:14
from .queries import mysql as mysql_templates
from .queries import postgres as postgres_templates
from .queries import sqlite as sqlite_templates
from .queries import mssql as mssql_templates
query_templates = {'mysql': mysql_templates, 
   'postgres': postgres_templates, 
   'redshift': postgres_templates, 
   'sqlite': sqlite_templates, 
   'mssql': mssql_templates}