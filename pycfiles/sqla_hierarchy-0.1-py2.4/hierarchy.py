# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sqla_hierarchy/hierarchy.py
# Compiled at: 2011-03-23 09:51:45
"""Queries to generate hierarchical relations"""
from sqlalchemy import Integer, and_, String, Boolean
from sqlalchemy.sql import union_all, select
from sqlalchemy.sql.expression import func, literal_column, label, literal, cast
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.dialects.postgresql.base import ARRAY
from sqlalchemy.sql.expression import Executable, ClauseElement, TableClause, ColumnClause
__all__ = [
 'Hierarchy', 'supported_db', 'HierarchyLesserError', 'MissingForeignKey']
supported_db = {'postgresql': (8, 4, 0), 'oracle': (10, 0, 0)}

class HierarchyError(Exception):
    """Base error class for Hierarchy"""
    __module__ = __name__


class MissingForeignKey(HierarchyError):
    """If the selected table does not have a foreign key refering to itself,
    this error will be raised"""
    __module__ = __name__

    def __init__(self, relation):
        self.relation = relation

    def __str__(self):
        return "A proper foreign key couldn't be found in relation %s" % self.relation


class HierarchyLesserError(HierarchyError):
    """If the database version is lower than the version supported, this error
    will be raised"""
    __module__ = __name__

    def __init__(self, dialect, version):
        self.dialect = dialect
        self.version = version

    def __str__(self):
        return "This method hasn't been written for %s dialect/version lesser than %s yet" % (self.dialect, ('.').join([ str(x) for x in self.version ]))


def _build_table_clause(select, name, path_type):
    """For pgsql, it builds the recursive table needed to perform a
    hierarchical query.
    Parameters:
        * select instruction of type sqlalchemy.sql.expression.Select
        * a name for the new virtual table
        * the type for the connect_path column
    It returns a TableClause object
    """
    cols = []
    for ev in select.columns.keys():
        cols.append(ColumnClause(ev, type_=getattr(select.columns, ev).type))

    cols.append(ColumnClause('level', Integer))
    cols.append(ColumnClause('connect_path', ARRAY(path_type)))
    tb = TableClause(name, *cols)
    return tb


class Hierarchy(Executable, ClauseElement):
    """Given a sqlalchemy.schema.Table and a sqlalchemy.sql.expression.Select,
    this class will return the information from these objects with some extra
    columns that will properly denote the hierarchical relation between the
    rows. 
    The returned Hierarchy object could then be executed and it will return the
    same Select statement submitted plus the following columns:
        * level: the relative level of the row related to its parent
        * connect_path: a list with all the ids that compound this part of the
                        hierarchy, from the root node to the current value
        * is_leaf: boolean indicating is the particular id is a leaf or not
    The resultset will be returned properly ordered by the levels in the
    hierarchy
    Special remarks:
        * The selected table must have a self referential foreign key relation,
          otherwise it will raise MissingForeignKey
        * Not every database is supported (at the moment). Check the global var
          supported_db for an up2date list. Trying to execute Hierarchy with an
          unsupported db will raise NotImplementedError or HierarchyLesserError
          or HierarchyGreaterError (check the errors classes docstring for the
          exact meaning of each of them).
        * To prevent the query from returning every node as a different
          starting node and, therefore, having duplicate values, you can
          provide the 'starting_node' parameter in the **kwargs. The value you
          must provide is the parent id for the root node you want to start 
          building the hierarchical tree. 
          None has the same meaning as "0" since we perform a coalesce function 
          in the query. By default the system will add a 'starting_node'="0". If
          you don't want a starting node, pass 'starting_node'=False and the
          clause will not be added to the query
    For examples of Hierarchy, check the tests dir.
    """
    __module__ = __name__

    def __init__(self, Session, table, select, **kw):
        self.table = table
        self.select = select
        self.parent = None
        self.child = None
        self._bind = Session.bind
        self._whereclause = select._whereclause
        self.fk_type = None
        for ev in self.table.foreign_keys:
            if ev.column.table.name == ev.parent.table.name:
                self.parent = ev.parent.name
                self.child = ev.column.name
                break

        if self.parent is None or self.child is None:
            raise MissingForeignKey(self.table.name)
        for (k, v) in kw.iteritems():
            setattr(self, k, v)

        if not hasattr(self, 'starting_node') or self.starting_node is None:
            self.fk_type = self.table.columns.get(self.parent).type._type_affinity
            if self.fk_type == String:
                setattr(self, 'starting_node', 'a')
                self.type_length = self.table.columns.get(self.parent).type.length
            else:
                setattr(self, 'starting_node', '0')
        elif not self.starting_node:
            pass
        else:
            self.starting_node = str(self.starting_node)
        return


@compiles(Hierarchy)
def visit_hierarchy(element, compiler, **kw):
    """If the database bound to the connection is not supported, a
    NotImplementedError will be raised"""
    raise NotImplementedError("This method hasn't been written for %s dialect yet" % compiler.dialect.name)


@compiles(Hierarchy, 'oracle')
def visit_hierarchy(element, compiler, **kw):
    """visit compilation idiom for oracle"""
    if compiler.dialect.server_version_info < supported_db['oracle']:
        raise HierarchyLesserError(compiler.dialect.name, supported_db['oracle'])
    else:
        sel = element.select
        sel.append_column(literal_column('level', type_=Integer))
        sel.append_column(literal_column('CONNECT_BY_ISLEAF', type_=Boolean).label('is_leaf'))
        sel.append_column(literal_column("LTRIM(SYS_CONNECT_BY_PATH (%s,','),',')" % element.child, type_=String).label('connect_path'))
        qry = '%s' % compiler.process(sel)
        if hasattr(element, 'starting_node') and getattr(element, 'starting_node') is not False:
            if element.starting_node == 'a' and element.fk_type == String or element.starting_node == '0' and element.fk_type == Integer:
                qry += ' start with %s is null' % element.parent
            elif getattr(element, 'starting_node') is False:
                pass
            else:
                qry += ' start with %s=%s' % (element.parent, element.starting_node)
        qry += ' connect by prior %s=%s' % (element.child, element.parent)
        return qry


@compiles(Hierarchy, 'postgresql')
def visit_hierarchy(element, compiler, **kw):
    """visit compilation idiom for pgsql"""
    if compiler.dialect.server_version_info < supported_db['postgresql']:
        raise HierarchyLesserError(compiler.dialect.name, supported_db['postgresql'])
    else:
        if element.fk_type == String:
            element.fk_type = String(element.type_length)
            val = 'a'
        else:
            element.fk_type = Integer
            val = '0'
        rec = _build_table_clause(element.select, 'rec', element.fk_type)
        sel1 = element.select
        if hasattr(element, 'starting_node') and getattr(element, 'starting_node') is not False:
            sel1 = sel1.where(func.coalesce(literal_column(element.parent, type_=String), literal(val, type_=String)) == literal(element.starting_node, type_=String))
        sel1.append_column(literal_column('1', type_=Integer).label('level'))
        sel1.append_column(literal_column('ARRAY[%s]' % element.child, type_=ARRAY(element.fk_type)).label('connect_path'))
        sel1.append_column(literal_column('false', type_=Boolean).label('cycle'))
        sel2 = element.select
        sel2.append_column(label('level', rec.c.level + literal_column('1', type_=Integer)))
        sel2.append_column(label('connect_path', func.array_append(rec.c.connect_path, getattr(element.table.c, element.child))))
        sel2.append_column(literal_column('%s=ANY(connect_path)' % getattr(element.table.c, element.child)).label('cycle'))
        sel2 = sel2.where(and_(getattr(element.table.c, element.parent) == getattr(rec.c, element.child), 'not cycle'))
        sel3 = sel1.union_all(sel2)
        new_sel = select([rec])
        new_sel.append_column(literal_column('case connect_path <@ lead(connect_path, 1) over (order by connect_path) when true then false else true end').label('is_leaf'))
        qry = 'with recursive rec as (%s) %s order by connect_path' % (compiler.process(sel3), new_sel)
        return qry