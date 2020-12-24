# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mcfletch/pylive/table/pytable/_postgresql/tableactions.py
# Compiled at: 2007-01-04 14:58:41
"""Actions for the PostgreSQL table

These are meta-queries/actions, they tell us about
the structure of the database schema by directly
querying the postgresql system catalogs.  They are
therefor entirely non-portable, evil things, but
they do appear to get the job done :) .
"""
from pytable import sqlquery, dbschema
from basicproperty import common
import traceback

def intSetToTuple(source):
    """Convert PyGreSQL's raw {1,2,3} set strings into lists

        These really should be getting converted to lists
        automatically by the driver, but it doesn't seem to
        want to do so :( .
        """
    if isinstance(source, (str, unicode)):
        items = source[1:-1]
        items = items.split(',')
        result = []
        for item in items:
            if item:
                try:
                    item = int(item)
                except ValueError, err:
                    try:
                        item = float(item)
                    except ValueError, err:
                        raise ValueError('Could not convert item %r of set %r to an integer or float value' % (
                         item, source))
                    else:
                        result.append(item)

        return result
    return source


class ListDatabases(sqlquery.SQLQuery):
    """Queries PostgreSQL server for list of database-names

        returns a simple list of string names
        """
    sql = "SELECT datname FROM pg_database\n\tWHERE datname != 'template1' AND datname != 'template0';"

    def processResults(self, cursor, **namedarguments):
        """Read database name list from cursor"""
        return [ row[0] for row in cursor.fetchall() ]


class ListDatatypes(sqlquery.SQLQuery):
    """Queries PostgreSQL server for list of base data-type names

        Only lists the set of defined, non-array base data-types

        returns typname:oid mapping
        """
    sql = "SELECT\n\t\ttypname, oid\n\tFROM\n\t\tpg_type\n\tWHERE\n\t\ttyptype = 'b' -- base types only\n\tAND\n\t\ttypisdefined='t' -- is actually available\n\tAND\n\t\ttypelem=0 -- is not an array type\n\t;"

    def processResults(self, cursor, **namedarguments):
        """Read database name list from cursor"""
        return dict([ (row[0], row[1]) for row in cursor.fetchall() ])


class ListTables(sqlquery.SQLQuery):
    """Queries connection/cursor for list of table-names

        returns a simple list of string names
        """
    sql = "\n\tSELECT \n\t  c.relname\n\tFROM pg_catalog.pg_class c\n\t\t LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace\n\tWHERE c.relkind IN ('r','v','')\n\t\t  AND n.nspname NOT IN ('pg_catalog', 'pg_toast')\n\t\t  AND pg_catalog.pg_table_is_visible(c.oid)\n\tORDER BY c.relname;\n\t"

    def processResults(self, cursor, **namedarguments):
        """Read table name list from cursor"""
        result = [ row[0] for row in cursor.fetchall() ]
        return result


class ListNamespaces(sqlquery.SQLQuery):
    """List sub-namespaces in the database"""
    sql = "SELECT\n\t\tns.nspname\n\tFROM\n\t\tpg_namespace ns\n\tWHERE\n\t\tns.nspname NOT LIKE 'pg_%%%%'\n\tAND\n\t\tns.nspname !='information_schema'\n\tAND\n\t\tns.nspname != 'public'\n\t;"

    def processResults(self, cursor, **namedarguments):
        """Read schema names list from cursor"""
        return [ row[0] for row in cursor.fetchall() ]


class ListNamespaceTables(sqlquery.SQLQuery):
    """List sub-namespace tables in the database

        That is, tables not in the public catalog, which therefor
        require a namespace prefix to reference.

        Returns a simple list of (namespace,tablename) tuples
        """
    sql = "SELECT\n\t\tt.schemaname,t.tablename\n\tFROM\n\t\tpg_namespace ns,\n\t\tpg_tables t\n\tWHERE\n\t\tns.nspname NOT LIKE 'pg_%%%%'\n\tAND\n\t\tns.nspname !='information_schema'\n\tAND\n\t\tns.nspname != 'public'\n\tAND\n\t\tt.schemaname = ns.nspname\n\tAND\n\t\tt.tablename NOT LIKE 'pg_%%%%'\n\tORDER BY t.schemaname, t.tablename\n\t;"

    def processResults(self, cursor, **namedarguments):
        """Read table name list from cursor"""
        result = [ (row[0], row[1]) for row in cursor.fetchall() ]
        return result


class TableStructure(sqlquery.SQLQuery):
    """Reverse-engineer table structure/schema from database

        This is a very heavy mechanism for design-time use
        which attempts to describe a table in the database
        using the dbschema objects which would normally
        be used to proactively define how we interact with
        the table.

        There are actually three different queries being
        done during the TableStructure query.  The first
        is the base query, which simply retrieves the
        DB API 2.0 column descriptions.  These provide
        much of the basic information required.

        The second stage retrieves the foreign-key
        constraints for the table.  Eventually this should
        also return general constraints (check restraints)
        to allow for automatically setting up constraint
        numeric and/or string data types.

        The third stage retrieves information about indices
        on the table.  This includes primary, unique and
        multi-field indices, but not check indices.
        """
    sql = '\n\tSELECT *\n\tFROM %(tableName)s\n\tLIMIT 1; -- this will hopefully optimize the query somewhat\n\t'

    def processResults(self, cursor, tableName, **namedarguments):
        """Build Table and Field descriptors through introspection
                """
        table = dbschema.TableSchema(name=tableName)
        descriptors = []
        nameMap = {}
        tableDescription = cursor.description
        for (index, description) in zip(range(len(tableDescription)), tableDescription):
            extras = {}
            try:
                extras['dbDataType'] = cursor.connection.driver.localToSQLType(description[1])
            except KeyError:
                pass
            else:
                try:
                    extras['dataType'] = cursor.connection.driver.sqlToDataType(extras['dbDataType'])
                except KeyError:
                    pass

                try:
                    extras['baseClass'] = cursor.connection.driver.sqlToBaseType(extras['dbDataType'])
                except KeyError:
                    pass

                new = dbschema.FieldSchema(name=description[0], index=index, table=table, internalSize=(description[3] or -1), displaySize=(description[2] or -1), **extras)
                if not description[6]:
                    new.constraints.append(dbschema.NotNullConstraint())
                descriptors.append(new)
                nameMap[new.name] = new

        table.fields = descriptors
        localNameSet = AttributeNumbers()(cursor, tableName=tableName)
        try:
            for (columnNumber, defaultString) in AttributeDefaultValue()(tableName=tableName, cursor=cursor).items():
                nameMap[localNameSet.get(columnNumber)].defaultValue = defaultString

        except:
            traceback.print_exc()

        try:
            tableDescription = ForeignConstraints()(cursor, tableName=tableName)
        except:
            print 'Unable to retrieve foreign constraints'
            traceback.print_exc()
        else:
            constraints = []
            for (localIndices, foreignTable, foreignIndices, foreignNamespace) in tableDescription:
                if foreignNamespace != 'public':
                    foreignTable = '%s.%s' % (foreignNamespace, foreignTable)
                localIndices = intSetToTuple(localIndices)
                foreignIndices = intSetToTuple(foreignIndices)
                localFields = [ localNameSet[int(i)] for i in localIndices ]
                foreignNameSet = AttributeNumbers()(cursor, tableName=foreignTable)
                foreignFields = [ foreignNameSet[int(i)] for i in foreignIndices ]
                new = dbschema.ForeignKeyConstraint(fields=localFields, foreignFields=foreignFields, foreignTable=foreignTable)
                constraints.append(new)

            if constraints:
                table.constraints = constraints

        indices = []
        for (id, fieldNums, unique, primary, name) in ListIndices()(cursor, tableName=tableName):
            skipIndex = 0
            for number in fieldNums.split():
                if int(number) <= 0:
                    skipIndex = 1

            if skipIndex:
                continue
            try:
                fields = [ nameMap[localNameSet[int(i)]].name for i in fieldNums.split()
                         ]
                indices.append(dbschema.IndexSchema(name=name, unique=unique, primary=primary, fields=fields))
            except KeyError, err:
                print 'Failure getting fields for index: %s' % (err,), (id, fieldNums, unique, primary, name, localNameSet)

        if indices:
            table.indices = indices
        return table


class ExpandTableName(sqlquery.SQLQuery):
    """ Provides tableName to namespace + tableName expansion
        
        """

    def __call__(self, cursor, tableName, namespace=None, **named):
        """ Override to provide default namespace"""
        if '.' in tableName:
            (namespace, tableName) = tableName.split('.', 1)
        if not namespace:
            namespace = 'public'
        return super(ExpandTableName, self).__call__(cursor=cursor, tableName=tableName, namespace=namespace, **named)


class ListIndices(ExpandTableName):
    """Get index-data-records for a given table

        namespace -- namespace where the table is defined, default is "public"
        tableName -- name of the table
        
        XXX Should build actual Index objects here, not
                just return data-values for interpretation.
        """
    sql = "\n\t\tSELECT\n\t\t\ti.indexrelid, -- the key-ID of the index\n\t\t\ti.indkey, -- list of field-indices participating\n\t\t\ti.indisunique, -- whether unique or not\n\t\t\ti.indisprimary, -- whether a primary-key index or not\n\t\t\tc2.relname -- index name\n\t\tFROM\n\t\t\tpg_class c, -- looking up table-name\n\t\t\tpg_class c2, -- looking up index-name\n\t\t\tpg_index i, -- getting extra index-specific information\n\t\t\tpg_namespace n -- looking up namespace\n\t\tWHERE\n\t\t\tn.nspname=%%(namespace)s AND -- the given namespace\n\t\t\tn.oid=c.relnamespace AND -- table reference to namespace\n\t\t\tc.relname=%%(tableName)s AND -- the given table's row in catalog\n\t\t\tc.oid = i.indrelid AND -- index entry refers to given table\n\t\t\ti.indexrelid=c2.oid -- lookup of index row key in table catalog\n\t\tORDER BY\n\t\t\tc2.relname;\n\t"

    def processResults(self, cursor, **named):
        """returns results of the selection as an unadorned set"""
        return cursor.fetchall()


class AttributeNumbers(ExpandTableName):
    """Query attnum:attname for a table
        
        namespace -- namespace where the table is defined, default is "public"
        tableName -- name of the table
        
        returns a dictionary of number:name
        """
    sql = "\n\t\tSELECT\n\t\t\ta.attname, a.attnum\n\t\tFROM\n\t\t\tpg_attribute a,\n\t\t\tpg_class c,\n\t\t\tpg_namespace n -- looking up namespace\n\t\tWHERE\n\t\t\tn.nspname=%%(namespace)s AND -- the given namespace\n\t\t\tn.oid=c.relnamespace AND -- table reference to namespace\n\t\t\tc.relname=%%(tableName)s AND\n\t\t\tc.oid = a.attrelid\n\t\t\t-- This excludes oid and other system columns, which means that\n\t\t\t-- we can't deal with oid indices...\n\t\t\t-- AND a.attnum > 0\n\t\tORDER BY\n\t\t\ta.attnum;\n\t"

    def processResults(self, cursor, **named):
        set = {}
        for (name, number) in cursor.fetchall():
            set[int(number)] = name

        return set


class AttributeDefaultValue(ExpandTableName):
    """Queries for attribute default values

        tableName -- name of the table
        """
    sql = '\n\t\tSELECT\n\t\t\ta.adnum,\n\t\t\ta.adsrc\n\t\tFROM\n\t\t\tpg_attrdef a,\n\t\t\tpg_class c,\n\t\t\tpg_namespace n -- looking up namespace\n\t\tWHERE\n\t\t\tn.nspname=%%(namespace)s AND -- the given namespace\n\t\t\tn.oid=c.relnamespace AND -- table reference to namespace\n\t\t\tc.relname=%%(tableName)s AND\n\t\t\tc.oid = a.adrelid;\n\t'

    def processResults(self, cursor, **named):
        set = {}
        for (number, value) in cursor.fetchall():
            set[int(number)] = value

        return set


class ForeignConstraints(ExpandTableName):
    sql = "\n\tSELECT \n\t\tcon.conkey, -- local key-columns\n\t\t-- con.confrelid, -- remote table id\n\t\tc2.relname, -- remote table name\n\t\tcon.confkey, -- remote key-columns\n\t\tn2.nspname -- remote table namespace\n\tFROM\n\t\tpg_constraint con,\n\t\tpg_class c,\n\t\tpg_class c2,\n\t\tpg_namespace n1,\n\t\tpg_namespace n2\n\tWHERE\n\t\tn1.nspname=%%(namespace)s AND -- the given namespace\n\t\tn1.oid=c.relnamespace AND -- table reference to namespace\n\t\tc.relname=%%(tableName)s AND\n\t\tc.oid = con.conrelid AND\n\t\tcon.contype = 'f' AND\n\t\tc2.oid = con.confrelid AND\n\t\tc2.relnamespace=n2.oid\n\t;"

    def processResults(self, cursor, **named):
        return cursor.fetchall()


class AttrNamesFromNumbers(ExpandTableName):
    """Get attr names from table-oid and set of attr indices"""
    sql = '\n\t\tSELECT\n\t\t\ta.adnum,\n\t\t\ta.adsrc\n\t\tFROM\n\t\t\tpg_attrdef a,\n\t\t\tpg_class c,\n\t\t\tpg_namespace n -- looking up namespace\n\t\tWHERE\n\t\t\tn.nspname=%%(namespace)s AND -- the given namespace\n\t\t\tn.oid=c.relnamespace AND -- table reference to namespace\n\t\t\tc.relname=%%(tableName)s AND\n\t\t\tc.oid = a.adrelid AND\n\t\t\ta.attnum IN %%(set)s;\n\t'

    def processResults(self, cursor, **named):
        return cursor.fetchall()


class AttributeFromNumber(ExpandTableName):
    """Get full field definition information for a single field

        This is normally only used for the system fields which are
        not normally part of the table definition...
        """
    sql = '\n\t\tSELECT\n\t\t\tpg_attribute.attname,\n\t\t\tpg_attribute.attnum,\n\t\t\tpg_attribute.attlen AS internallength,\n\t\t\tpg_attribute.atttypmod AS length,\n\t\t\tpg_attribute.attnotnull AS notnull,\n\t\t\tpg_attribute.atthasdef AS hasdefault,\n\t\t\tpg_attrdef.adsrc AS defaultvalue,\n\t\tFROM\n\t\t\tpg_attribute,\n\t\t\tpg_attrdef,\n\t\t\tpg_class,\n\t\t\tpg_namespace n -- looking up namespace\n\t\tWHERE\n\t\t\tn.nspname=%%(namespace)s AND -- the given namespace\n\t\t\tn.oid=c.relnamespace AND -- table reference to namespace\n\t\t\tpg_class.relname=%%(tableName)s\n\t\tAND\n\t\t\tpg_class.oid = pg_attrdef.adrelid\n\t\tAND\n\t\t\tpg_class.oid = pg_attribute.attrelid\n\t\tAND\n\t\t\tpg_attrdef.adnum = %%(attributeNumber)s\n\t\tAND\n\t\t\tpg_attribute.attnum = %%(attributeNumber)s\n\t\tAND\n\t\t\tpg_attrdef.attisdropped = False\n\t\t;\n\t'

    def processResults(self, cursor, **named):
        return cursor.fetchall()


class SequenceName(sqlquery.SQLQuery):
    """Retrieve sequence name for a given field"""
    sql = 'SELECT\n\t\tpg_attrdef.adsrc\n\tFROM\n\t\tpg_attrdef,\n\t\tpg_class,\n\t\tpg_attribute\n\tWHERE\n\t\tpg_attrdef.adnum = pg_attribute.attnum\n\tAND \n\t\tpg_attrdef.adrelid = pg_class.oid\n\tAND \n\t\tpg_attribute.attrelid = pg_class.oid\n\tAND \n\t\tpg_attribute.attname = %(field)s\n\tAND \n\t\tpg_class.relname = %(table)s\n\t'