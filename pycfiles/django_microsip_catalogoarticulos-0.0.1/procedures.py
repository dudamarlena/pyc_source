# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SIC2-U\Documents\GitHub\django-microsip-base\django_microsip_base\apps\plugins\django_microsip_catalogoarticulos\django_microsip_catalogoarticulos\custom_db\procedures.py
# Compiled at: 2014-10-15 12:19:38
procedures = {}
procedures['SIC_ARTICULOS_CATALOGO'] = "\n    CREATE OR ALTER PROCEDURE SIC_ARTICULOS_CATALOGO\n    as\n    begin\n     if (not exists(\n        select 1 from RDB$RELATION_FIELDS rf\n        where rf.RDB$RELATION_NAME = 'ARTICULOS' and rf.RDB$FIELD_NAME = 'SIC_IMAGEN_URL')) then\n        execute statement 'ALTER TABLE ARTICULOS ADD SIC_IMAGEN_URL VARCHAR(100)';\n\tend  \n    "