# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\djmicrosip_polizasautomaticas\djmicrosip_polizasautomaticas\custom_db\contabilidad\procedures.py
# Compiled at: 2015-10-24 14:40:32
sql_procedures = {}
sql_procedures['SIC_CONTABILIDAD_POLIZASAUTO'] = "\n    CREATE OR ALTER PROCEDURE SIC_CONTABILIDAD_POLIZASAUTO\n    as\n    begin\n     if (not exists(\n        select 1 from RDB$RELATION_FIELDS rf\n        where rf.RDB$RELATION_NAME = 'DOCTOS_CO' and rf.RDB$FIELD_NAME = 'SIC_POLIZASAUTO_REF')) then\n\t\tbegin\n        \texecute statement 'ALTER TABLE DOCTOS_CO ADD SIC_POLIZASAUTO_REF NOMBRE_CORTO';\n\t\tend\n\tend"