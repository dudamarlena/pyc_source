# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/genes/mysql_bulk_insert.py
# Compiled at: 2019-05-07 08:43:55
# Size of source mod 2**32: 1634 bytes
__author__ = 'jpablo'
from django.db import connection, transaction
from django.db.models.fields import NOT_PROVIDED

def bulk_insert(object_list, show_sql=False):
    """
    Generate the sql code for bulk insertion
    @param object_list: Django model objects
    """
    if not len(object_list):
        return
    Model = type(object_list[0])
    table_name = Model._meta.db_table
    fields_names = [f.attname for f in Model._meta.fields if f.name != 'id']
    sql = 'insert into ' + table_name + ' (' + ','.join(fields_names) + ') values \n'
    defaults = dict([(f.attname, f.default if f.default is not NOT_PROVIDED else 'NULL') for f in Model._meta.fields])
    auto_now_add = [f.attname for f in Model._meta.fields if getattr(f, 'auto_now_add', False)]

    def get_values(ob, fields):
        ret = []
        for field in fields:
            val = getattr(ob, field)
            if val is None:
                val = defaults[field]
            if field in auto_now_add:
                val = date.today().strftime('%Y-%m-%d')
            ret.append(str(val))

        return ret

    lines = []
    for ob in object_list:
        line = '("' + '","'.join(get_values(ob, fields_names)) + '")'
        line = line.replace('"NULL"', 'NULL')
        line = line.replace('"False"', 'False')
        line = line.replace('"True"', 'False')
        lines.append(line)

    sql += ',\n'.join(lines) + ';'
    if show_sql:
        print(sql)
        return
    cursor = connection.cursor()
    cursor.execute(sql)
    transaction.commit_unless_managed()