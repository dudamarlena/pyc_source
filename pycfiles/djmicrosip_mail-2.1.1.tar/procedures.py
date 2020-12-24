# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\djmicrosip_apps\djmicrosip_mail\djmicrosip_mail\modulos\herramientas\procedures.py
# Compiled at: 2019-12-02 13:48:11
procedures = {}
procedures['SIC_MAIL_CLIENTE_AT'] = "\n    CREATE OR ALTER PROCEDURE SIC_MAIL_CLIENTE_AT\n    as\n    BEGIN\n        if (not exists(\n        select 1 from RDB$RELATION_FIELDS rf\n        where rf.RDB$RELATION_NAME = 'CLIENTES' and rf.RDB$FIELD_NAME = 'SIC_MAIL_NOENVIAR')) then\n            execute statement 'ALTER TABLE CLIENTES ADD SIC_MAIL_NOENVIAR SMALLINT';\n    END\n    "