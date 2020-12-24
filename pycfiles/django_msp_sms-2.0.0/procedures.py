# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\django_msp_sms\django_msp_sms\modulos\preferencias\procedures.py
# Compiled at: 2015-10-19 12:15:01
procedures = {}
procedures['SIC_SMS_CLIENTE_AT'] = "\n    CREATE OR ALTER PROCEDURE SIC_SMS_CLIENTE_AT\n    as\n    BEGIN\n        if (not exists(\n        select 1 from RDB$RELATION_FIELDS rf\n        where rf.RDB$RELATION_NAME = 'CLIENTES' and rf.RDB$FIELD_NAME = 'SIC_SMS_NOENVIAR')) then\n            execute statement 'ALTER TABLE CLIENTES ADD SIC_SMS_NOENVIAR SMALLINT';\n    END  \n    "