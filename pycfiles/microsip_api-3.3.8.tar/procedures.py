# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\djmicrosip_apps\django-microsip-api\microsip_api\apps\commun\articulos\articulos\alertas\procedures.py
# Compiled at: 2019-09-09 14:21:49
procedures = {}
procedures['SIC_ALERTA_ARTICULO_AT'] = "\n    CREATE OR ALTER PROCEDURE SIC_ALERTA_ARTICULO_AT\n    as\n    BEGIN\n        if (not exists(\n        select 1 from RDB$RELATION_FIELDS rf\n        where rf.RDB$RELATION_NAME = 'ARTICULOS' and rf.RDB$FIELD_NAME = 'SIC_ALERTA_UNIDADES')) then\n            execute statement 'ALTER TABLE ARTICULOS ADD SIC_ALERTA_UNIDADES INTEGER DEFAULT 0';\n\n        if (not exists(\n        select 1 from RDB$RELATION_FIELDS rf\n        where rf.RDB$RELATION_NAME = 'ARTICULOS' and rf.RDB$FIELD_NAME = 'SIC_ALERTA_UNIDAD_MEDIDA')) then\n            execute statement 'ALTER TABLE ARTICULOS ADD SIC_ALERTA_UNIDAD_MEDIDA VARCHAR(20)';\n    END  \n    "