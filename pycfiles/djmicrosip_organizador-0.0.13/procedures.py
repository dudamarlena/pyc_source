# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SIC2-U\Documents\GitHub\django-microsip-base\django_microsip_base\django_microsip_base\apps\plugins\djmicrosip_organizador\djmicrosip_organizador\custom_db\procedures.py
# Compiled at: 2015-02-07 15:36:52
procedures = {}
procedures['SIC_ARTICULOS_ORGANIZADOR'] = "\n    CREATE OR ALTER PROCEDURE SIC_ARTICULOS_ORGANIZADOR\n    as\n    begin\n     if (not exists(\n        select 1 from RDB$RELATION_FIELDS rf\n        where rf.RDB$RELATION_NAME = 'ARTICULOS' and rf.RDB$FIELD_NAME = 'SIC_CARPETA_ID')) then\n        execute statement 'ALTER TABLE ARTICULOS ADD SIC_CARPETA_ID ENTERO_ID';\n     \n\tend  \n    "