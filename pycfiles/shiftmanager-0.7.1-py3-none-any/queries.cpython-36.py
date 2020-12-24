# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mikenawood/Code/shiftmanager/build/lib/shiftmanager/queries.py
# Compiled at: 2017-11-07 15:04:11
# Size of source mod 2**32: 817 bytes
"""
Query templates for use by the Redshift class.
"""
copy_from_s3 = "COPY {table}\nFROM '{manifest_key}'\nCREDENTIALS '{creds}'\nJSON '{jpaths_key}'\nMANIFEST GZIP TIMEFORMAT 'auto'\n"
all_privileges = 'SELECT\n  c.relkind,\n  n.oid as "schema_oid",\n  n.nspname as "schema",\n  c.oid as "rel_oid",\n  c.relname,\n  c.relowner AS "owner_id",\n  u.usename AS "owner_name",\n  pg_catalog.array_to_string(c.relacl, \'\n\') AS "privileges",\n  CASE c.relkind WHEN \'r\' THEN \'table\' WHEN \'v\' THEN \'view\' END AS "type"\nFROM pg_catalog.pg_class c\n     LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace\n     JOIN pg_catalog.pg_user u ON u.usesysid = c.relowner\nWHERE c.relkind IN (\'r\', \'v\', \'m\', \'S\', \'f\')\n  AND n.nspname !~ \'^pg_\' AND pg_catalog.pg_table_is_visible(c.oid)\nORDER BY c.relkind, n.oid, n.nspname;\n'