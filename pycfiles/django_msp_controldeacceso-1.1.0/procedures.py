# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\django_msp_controldeacceso\django_msp_controldeacceso\custom_db\procedures.py
# Compiled at: 2016-02-15 12:30:53
procedures = {}
procedures['SIC_CLIENTES_ACCESO'] = "\n    CREATE OR ALTER PROCEDURE SIC_CLIENTES_ACCESO\n    as\n    begin\n     if (not exists(\n        select 1 from RDB$RELATION_FIELDS rf\n        where rf.RDB$RELATION_NAME = 'CLIENTES' and rf.RDB$FIELD_NAME = 'SIC_IMAGEN_URL')) then\n        execute statement 'ALTER TABLE CLIENTES ADD SIC_IMAGEN_URL VARCHAR(100)';\n\tend  \n    "