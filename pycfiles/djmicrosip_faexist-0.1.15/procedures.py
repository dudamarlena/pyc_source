# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Jesus\Documents\GitHub\django-microsip-base\django_microsip_base\django_microsip_base\apps\plugins\djmicrosip_faexist\djmicrosip_faexist\procedures.py
# Compiled at: 2015-01-22 18:49:01
procedures = {}
procedures['SIC_FAEXIST_ARTICULO_AT'] = "\n    CREATE OR ALTER PROCEDURE SIC_FAEXIST_ARTICULO_AT\n    as\n    BEGIN\n        if (not exists(\n        select 1 from RDB$RELATION_FIELDS rf\n        where rf.RDB$RELATION_NAME = 'ARTICULOS' and rf.RDB$FIELD_NAME = 'SIC_FAEXIST_IGNORAR')) then\n            execute statement 'ALTER TABLE ARTICULOS ADD SIC_FAEXIST_IGNORAR SMALLINT';\n    END  \n    "