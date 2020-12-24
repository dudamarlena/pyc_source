# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pirogue/single_inheritance.py
# Compiled at: 2019-11-29 08:49:00
# Size of source mod 2**32: 7525 bytes
import os, psycopg2, psycopg2.extras
from pirogue.utils import table_parts, select_columns, insert_command, update_command
from pirogue.information_schema import reference_columns, primary_key, default_value
from pirogue.exceptions import TableHasNoPrimaryKey

class SingleInheritance:
    __doc__ = '\n    Creates a join view with associated triggers to edit for a single inheritance.\n    '

    def __init__(self, parent_table: str, child_table: str, pg_service: str=None, view_schema: str=None, view_name: str=None, pkey_default_value: bool=False):
        """
        Produces the SQL code of the join table and triggers

        Parameters
        ----------
        pg_service
            if not given, it is determined using environment variable PGSERVICE
        parent_table
            the parent table, can be schema specified
        child_table
            the child table, can be schema specified
        view_schema
            the schema where the view will written to
        view_name
            the name of the created view, defaults to vw_{parent_table}_{join_table}
        pkey_default_value
            the primary key column of the view will have a default value according to the child primary key table
        """
        if pg_service is None:
            pg_service = os.getenv('PGSERVICE')
        else:
            self.conn = psycopg2.connect('service={0}'.format(pg_service))
            self.cursor = self.conn.cursor()
            self.pkey_default_value = pkey_default_value
            self.parent_schema, self.parent_table = table_parts(parent_table)
            self.child_schema, self.child_table = table_parts(child_table)
            if view_schema is None:
                if self.parent_schema != self.child_schema:
                    raise ValueError('Destination schema cannot be guessed if different on sources tables.')
                else:
                    self.view_schema = self.parent_schema
            else:
                self.view_schema = view_schema
            self.view_name = view_name or 'vw_{pt}_{ct}'.format(pt=(self.parent_table), ct=(self.child_table))
            self.ref_parent_key, parent_referenced_key = reference_columns(self.cursor, self.child_schema, self.child_table, self.parent_schema, self.parent_table)
            try:
                self.child_pkey = primary_key(self.cursor, self.child_schema, self.child_table)
            except TableHasNoPrimaryKey:
                self.child_pkey = self.ref_parent_key

            self.parent_pkey = primary_key(self.cursor, self.parent_schema, self.parent_table)
            assert self.parent_pkey == parent_referenced_key

    def create(self) -> bool:
        """
        Creates the merge view on the specified service
        Returns True in case of success
        """
        success = True
        for sql in [self._SingleInheritance__view(),
         self._SingleInheritance__insert_trigger(),
         self._SingleInheritance__update_trigger(),
         self._SingleInheritance__delete_trigger(),
         self._SingleInheritance__extras()]:
            try:
                if sql:
                    self.cursor.execute(sql)
            except psycopg2.Error as e:
                success = False
                print('*** Failing:\n{}\n***'.format(sql))
                raise e

        self.conn.commit()
        self.conn.close()
        return success

    def __view(self) -> str:
        """
        Create the SQL code for the view
        :return: the SQL code
        """
        sql = '\nCREATE OR REPLACE VIEW {vs}.{vn} AS SELECT\n  {child_cols},\n  {parent_cols}\n  FROM {cs}.{ct}\n  LEFT JOIN {ps}.{pt} ON {pt}.{prk} = {ct}.{rpk};\n'.format(vs=(self.view_schema), vn=(self.view_name),
          parent_cols=select_columns((self.cursor), (self.parent_schema), (self.parent_table), table_alias=(self.parent_table), remove_pkey=True),
          child_cols=select_columns((self.cursor), (self.child_schema), (self.child_table), table_alias=(self.child_table)),
          cs=(self.child_schema),
          ct=(self.child_table),
          ps=(self.parent_schema),
          pt=(self.parent_table),
          rpk=(self.ref_parent_key),
          prk=(self.parent_pkey))
        return sql

    def __insert_trigger(self) -> str:
        """

        :return:
        """
        sql = '\n-- INSERT TRIGGER\nCREATE OR REPLACE FUNCTION {vs}.ft_{vn}_insert() RETURNS trigger AS\n$BODY$\nBEGIN\n{insert_parent}\n\n{insert_child}\nRETURN NEW;\nEND;\n$BODY$\nLANGUAGE plpgsql;\n\nDROP TRIGGER IF EXISTS tr_{vn}_on_insert ON {vs}.{vn};\n\nCREATE TRIGGER tr_{vn}_on_insert\n  INSTEAD OF INSERT ON {vs}.{vn}\n  FOR EACH ROW EXECUTE PROCEDURE {vs}.ft_{vn}_insert();\n'.format(vs=(self.view_schema), vn=(self.view_name),
          insert_parent=insert_command((self.cursor), (self.parent_schema), (self.parent_table), remove_pkey=False,
          coalesce_pkey_default=True,
          remap_columns={self.parent_pkey: self.ref_parent_key},
          returning='{ppk} INTO NEW.{prk}'.format(ppk=(self.parent_pkey), prk=(self.ref_parent_key))),
          insert_child=insert_command((self.cursor), (self.child_schema), (self.child_table), remove_pkey=False,
          pkey=(self.child_pkey)))
        return sql

    def __update_trigger(self):
        sql = '\n-- UPDATE TRIGGER\nCREATE OR REPLACE FUNCTION {vs}.ft_{vn}_update() RETURNS trigger AS\n$BODY$\nBEGIN\n{update_master}\n\n{update_child}\nRETURN NEW;\nEND;\n$BODY$\nLANGUAGE plpgsql;\n\nDROP TRIGGER IF EXISTS tr_{vn}_on_update ON {vs}.{vn};\n\nCREATE TRIGGER tr_{vn}_on_update\n  INSTEAD OF UPDATE ON {vs}.{vn}\n  FOR EACH ROW EXECUTE PROCEDURE {vs}.ft_{vn}_update();\n'.format(vs=(self.view_schema), vn=(self.view_name),
          update_master=update_command((self.cursor), (self.parent_schema), (self.parent_table), remap_columns={self.parent_pkey: self.ref_parent_key}),
          update_child=update_command((self.cursor), (self.child_schema), (self.child_table), pkey=(self.child_pkey), remove_pkey=False))
        return sql

    def __delete_trigger(self):
        sql = '\nCREATE OR REPLACE FUNCTION {vs}.ft_{vn}_delete() RETURNS trigger AS\n$BODY$\nBEGIN\n  DELETE FROM {cs}.{ct} WHERE {rpk} = OLD.{rpk};\n  DELETE FROM {ps}.{pt} WHERE {ppk} = OLD.{rpk};\nRETURN NULL;\nEND;\n$BODY$\nLANGUAGE plpgsql;\n\nDROP TRIGGER IF EXISTS tr_{vn}_on_delete ON {vs}.{vn};\n\nCREATE TRIGGER tr_{vn}_on_delete\n  INSTEAD OF DELETE ON {vs}.{vn}\n  FOR EACH ROW EXECUTE PROCEDURE {vs}.ft_{vn}_delete();\n'.format(vs=(self.view_schema), vn=(self.view_name),
          cs=(self.child_schema),
          ct=(self.child_table),
          rpk=(self.ref_parent_key),
          ppk=(self.parent_pkey),
          ps=(self.parent_schema),
          pt=(self.parent_table))
        return sql

    def __extras(self):
        sql = ''
        if self.pkey_default_value:
            sql += 'ALTER VIEW {vs}.{vn} ALTER {rpk} SET DEFAULT {dv};'.format(vs=(self.view_schema),
              vn=(self.view_name),
              rpk=(self.child_pkey),
              dv=(default_value(self.cursor, self.child_schema, self.child_table, self.child_pkey)))
        return sql