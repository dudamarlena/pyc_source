# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xml2ddl/OracleInterface.py
# Compiled at: 2005-09-27 19:10:33
from downloadCommon import DownloadCommon, getSeqName
from DdlCommonInterface import DdlCommonInterface
import re

class OracleDownloader(DownloadCommon):
    __module__ = __name__

    def __init__(self):
        self.strDbms = 'oracle'

    def connect(self, info):
        try:
            import cx_Oracle
        except:
            print 'Missing Oracle support through cx_Oracle, see http://www.computronix.com/utilities.shtml#Oracle'
            return

        self.version = info['version']
        self.conn = cx_Oracle.connect(info['user'], info['pass'], info['dbname'])
        self.cursor = self.conn.cursor()

    def _tableInfo(self, strTable):
        self.cursor.execute('select * from %s' % (strTable,))
        for col in self.cursor.description:
            print col[0]

    def useConnection(self, con, version):
        self.conn = con
        self.version = version
        self.cursor = self.conn.cursor()

    def getTables(self, tableList):
        """ Returns the list of tables as a array of strings """
        if tableList and len(tableList) > 0:
            inTables = "AND upper(TABLE_NAME) IN ('%s')" % ("' , '").join([ name.upper() for name in tableList ])
        else:
            inTables = ''
        strQuery = "SELECT TABLE_NAME FROM ALL_TABLES WHERE \n            TABLE_NAME NOT IN ('DUAL')\n            AND OWNER NOT IN ('SYS', 'SYSTEM', 'OLAPSYS', 'WKSYS', 'WMSYS', 'CTXSYS', 'DMSYS', 'MDSYS', 'EXFSYS', 'ORDSYS')\n            AND TABLE_NAME NOT LIKE 'BIN$%%' \n            %s\n            ORDER BY TABLE_NAME\n            " % inTables
        self.cursor.execute(strQuery)
        rows = self.cursor.fetchall()
        if rows:
            return self._confirmReturns([ x[0] for x in rows ], tableList)
        return []

    def getTableColumns(self, strTable):
        """ Returns column in this format
            (nColIndex, strColumnName, strColType, CHARACTER_MAXIMUM_LENGTH, NUMERIC_PRECISION, bNotNull, strDefault, auto_increment)
        """
        strSql = '\n            SELECT COLUMN_ID, COLUMN_NAME, DATA_TYPE, DATA_LENGTH, DATA_PRECISION, DATA_SCALE, NULLABLE, DATA_DEFAULT\n            FROM ALL_TAB_COLUMNS\n            WHERE TABLE_NAME = :tablename\n            ORDER BY COLUMN_ID'
        self.cursor.execute(strSql, {'tablename': strTable})
        rows = self.cursor.fetchall()
        ret = []
        fixNames = {'character varying': 'varchar'}
        for row in rows:
            (attnum, name, type, size, numsize, numprec, nullable, default) = row
            if type in fixNames:
                type = fixNames[type]
            if nullable == 'Y':
                bNotNull = False
            else:
                bNotNull = True
            bAutoIncrement = False
            if numsize != None or numprec != None:
                size = numsize
            if type == 'DATE' or type == 'TIMESTAMP':
                size = None
            elif type == 'FLOAT' and size == 126:
                size = None
            if default:
                default = default.rstrip()
            ret.append((name, type, size, numprec, bNotNull, default, bAutoIncrement))

        return ret

    def getTableComment(self, strTableName):
        """ Returns the comment as a string """
        strSql = 'SELECT COMMENTS from ALL_TAB_COMMENTS WHERE TABLE_NAME = :TABLENAME'
        self.cursor.execute(strSql, {'TABLENAME': strTableName})
        rows = self.cursor.fetchall()
        if rows:
            return rows[0][0]
        return

    def getColumnComment(self, strTableName, strColumnName):
        """ Returns the comment as a string """
        strSql = 'SELECT COMMENTS from  ALL_COL_COMMENTS WHERE TABLE_NAME = :TABLENAME AND COLUMN_NAME = :COLUMNAME'
        self.cursor.execute(strSql, {'TABLENAME': strTableName, 'COLUMNAME': strColumnName})
        rows = self.cursor.fetchall()
        if rows:
            return rows[0][0]
        return []
        return

    def getTableIndexes(self, strTableName):
        """ Returns 
            (strIndexName, [strColumns,], bIsUnique, bIsPrimary, bIsClustered)
            or []
        """
        strSql = 'SELECT index_name, uniqueness, clustering_factor\n            FROM ALL_INDEXES\n            WHERE table_name = :tablename\n            '
        self.cursor.execute(strSql, {'tablename': strTableName})
        rows = self.cursor.fetchall()
        ret = []
        if not rows:
            return ret
        for row in rows:
            (strIndexName, bIsUnique, bIsClustered) = row
            strSql = 'SELECT column_name FROM ALL_IND_COLUMNS \n                WHERE table_name = :tablename AND index_name = :indexname\n                ORDER BY COLUMN_POSITION '
            self.cursor.execute(strSql, {'tablename': strTableName, 'indexname': strIndexName})
            colrows = self.cursor.fetchall()
            colList = [ col[0] for col in colrows ]
            bIsPrimary = False
            if bIsUnique == 'UNIQUE':
                strSql = "select c.*\n                    from   all_constraints c, all_cons_columns cc\n                    where  c.table_name = :tablename\n                    and    cc.constraint_name = c.constraint_name\n                    and    c.constraint_type = 'P'\n                    and    cc.column_name in (:colnames)\n                    and    c.status = 'ENABLED'"
                self.cursor.execute(strSql, {'tablename': strTableName, 'colnames': (',').join(colList)})
                indexRows = self.cursor.fetchall()
                if indexRows and len(indexRows) > 0:
                    bIsPrimary = True
            ret.append((strIndexName, colList, bIsUnique, bIsPrimary, bIsClustered))

        return ret

    def _getTableViaConstraintName(self, strConstraint):
        """ Returns strTablename """
        strSql = 'SELECT TABLE_NAME FROM ALL_CONSTRAINTS WHERE CONSTRAINT_NAME = :strConstraint'
        self.cursor.execute(strSql, {'strConstraint': strConstraint})
        rows = self.cursor.fetchall()
        if rows:
            return rows[0][0]
        return

    def _getColumnsViaConstraintName(self, strConstraint):
        """ Returns strTablename """
        strSql = 'SELECT COLUMN_NAME FROM all_cons_columns WHERE CONSTRAINT_NAME = :strConstraint ORDER BY POSITION'
        self.cursor.execute(strSql, {'strConstraint': strConstraint})
        rows = self.cursor.fetchall()
        if rows:
            return [ col[0] for col in rows ]
        return []

    def getTableRelations(self, strTableName):
        """ Returns 
            (strConstraintName, colName, fk_table, fk_columns, confupdtype, confdeltype)
            or []
        """
        strSql = "SELECT CONSTRAINT_NAME, TABLE_NAME, R_CONSTRAINT_NAME, DELETE_RULE\n            FROM  ALL_CONSTRAINTS\n            WHERE TABLE_NAME = :tablename\n            AND   CONSTRAINT_TYPE = 'R'\n            AND   STATUS='ENABLED'\n            "
        self.cursor.execute(strSql, {'tablename': strTableName})
        rows = self.cursor.fetchall()
        ret = []
        if not rows:
            return ret
        for row in rows:
            (strConstraintName, strTable, fk_constraint, chDelType) = row
            if fk_constraint:
                fk_table = self._getTableViaConstraintName(fk_constraint)
            else:
                fk_table = None
            colList = self._getColumnsViaConstraintName(strConstraintName)
            if fk_constraint:
                fkColList = self._getColumnsViaConstraintName(fk_constraint)
            else:
                fkColList = []
            if chDelType == 'NO ACTION':
                chDelType = 'a'
            elif chDelType == 'CASCADE':
                chDelType = 'c'
            elif chDelType == 'SET NULL':
                chDelType = 'n'
            elif chDelType == 'DEFAULT':
                chDelType = 'd'
            chUpdateType = ''
            ret.append((strConstraintName, colList, fk_table, fkColList, chUpdateType, chDelType))

        return ret

    def getViews(self, viewList):
        """ Returns the list of views as a array of strings """
        if viewList and len(viewList) > 0:
            inViews = "AND VIEW_NAME IN ('%s')" % ("','").join([ name.upper() for name in viewList ])
        else:
            inViews = ''
        strQuery = "SELECT VIEW_NAME \n        FROM ALL_VIEWS\n        WHERE OWNER NOT IN ('SYS', 'SYSTEM', 'OLAPSYS', 'WKSYS', 'WMSYS', 'CTXSYS', 'DMSYS', 'MDSYS', 'EXFSYS', 'ORDSYS', 'WK_TEST', 'XDB')\n        %s\n        ORDER BY VIEW_NAME" % inViews
        self.cursor.execute(strQuery)
        rows = self.cursor.fetchall()
        if rows:
            return self._confirmReturns([ x[0] for x in rows ], viewList)
        return []

    def getViewDefinition(self, strViewName):
        strQuery = 'SELECT TEXT FROM ALL_VIEWS WHERE VIEW_NAME = :viewName'
        self.cursor.execute(strQuery, {'viewName': strViewName})
        rows = self.cursor.fetchall()
        if rows:
            return rows[0][0].rstrip()
        return

    def getFunctions(self, functionList):
        """ Returns functions """
        if functionList and len(functionList) > 0:
            inFunctions = "AND OBJECT_NAME IN ('%s')" % ("','").join([ name.upper() for name in functionList ])
        else:
            inFunctions = ''
        strQuery = "SELECT OBJECT_NAME\n        FROM ALL_OBJECTS\n        WHERE OBJECT_TYPE in ('PROCEDURE', 'FUNCTION')\n        AND   OWNER NOT IN ('SYS', 'SYSTEM', 'OLAPSYS', 'WKSYS', 'WMSYS', 'CTXSYS', 'DMSYS', 'MDSYS', 'EXFSYS', 'ORDSYS', 'WK_TEST', 'XDB')\n        %s\n        ORDER BY OBJECT_NAME" % inFunctions
        self.cursor.execute(strQuery)
        rows = self.cursor.fetchall()
        if rows:
            return self._confirmReturns([ x[0] for x in rows ], functionList)
        return []

    def getFunctionDefinition(self, strSpecifiName):
        """ Returns (routineName, parameters, return, language, definition) """
        strSpecifiName = strSpecifiName.upper()
        strQuery = 'select TEXT from all_source where name=:strSpecifiName ORDER BY LINE'
        self.cursor.execute(strQuery, {'strSpecifiName': strSpecifiName})
        rows = self.cursor.fetchall()
        if not rows:
            return (None, None, None, None)
        lines = []
        for row in rows:
            lines.append(row[0])

        strDefinition = ('').join(lines)
        strDefinition = strDefinition.rstrip('; ')
        re_def = re.compile('.+\\s(AS|IS)\\s', re.IGNORECASE | re.MULTILINE | re.DOTALL)
        strDefinition = re_def.sub('', strDefinition)
        strQuery = "select lower(ARGUMENT_NAME), lower(DATA_TYPE), SEQUENCE, IN_OUT\n            FROM ALL_ARGUMENTS \n            WHERE object_name = :strSpecifiName AND ARGUMENT_NAME is not null\n            AND IN_OUT IN ('IN', 'IN/OUT') \n            ORDER BY POSITION"
        self.cursor.execute(strQuery, {'strSpecifiName': strSpecifiName})
        rows = self.cursor.fetchall()
        parameters = []
        if rows:
            for row in rows:
                (ARGUMENT_NAME, DATA_TYPE, SEQUENCE, IN_OUT) = row
                if ARGUMENT_NAME:
                    parameters.append(ARGUMENT_NAME + ' ' + DATA_TYPE)
                else:
                    parameters.append(DATA_TYPE)

        strQuery = "select lower(DATA_TYPE)\n            FROM ALL_ARGUMENTS\n            WHERE object_name = :strSpecifiName \n            AND IN_OUT = 'OUT'"
        self.cursor.execute(strQuery, {'strSpecifiName': strSpecifiName})
        rows = self.cursor.fetchall()
        strReturn = None
        if rows:
            if len(rows) > 1:
                print 'More than one return statement?, please check code'
            else:
                DATA_TYPE = rows[0][0]
                strReturn = DATA_TYPE
        return (
         strSpecifiName.lower(), parameters, strReturn, None, strDefinition)


class DdlOracle(DdlCommonInterface):
    __module__ = __name__

    def __init__(self, strDbms):
        DdlCommonInterface.__init__(self, strDbms)
        self.params['max_id_len'] = {'default': 63}
        self.params['alter_default'] = [
         'ALTER TABLE %(table_name)s MODIFY %(column_name)s %(column_type)s']
        self.params['drop_default'] = ['ALTER TABLE %(table_name)s ALTER %(column_name)s %(column_type)s']
        self.params['rename_column'] = ['ALTER TABLE %(table_name)s RENAME COLUMN %(old_col_name)s TO %(new_col_name)s']
        self.params['change_col_type'] = ['ALTER TABLE %(table_name)s MODIFY %(column_name)s %(column_type)s']
        self.params['drop_column'] = ['ALTER TABLE %(table_name)s DROP COLUMN %(column_name)s']
        self.params['add_relation'] = ['ALTER TABLE %(tablename)s ADD CONSTRAINT %(constraint)s FOREIGN KEY (%(thiscolumn)s) REFERENCES %(othertable)s(%(fk)s)%(ondelete)s']
        self.params['create_view'] = ['CREATE VIEW %(viewname)s AS %(contents)s']
        self.params['create_function'] = ['CREATE FUNCTION %(functionname)s(%(arguments)s) RETURN %(returns)s AS\n%(contents)s;']
        self.params['drop_function'] = ['DROP FUNCTION %(functionname)s']
        self.params['keywords'] = ('AS ASC AUDIT ACCESS BY ADD ALL ALTER CHAR AND ANY CHECK DATE CLUSTER COLUMN COMMENT DECIMAL DEFAULT COMPRESS\n            DELETE CONNECT DESC DISTINCT DROP CREATE CURRENT ELSE CURSOR GRANT GROUP EXCLUSIVE EXISTS HAVING IDENTIFIED IMMEDIATE\n            IN FILE INCREMENT INDEX FLOAT FOR INITIAL INSERT FROM INTEGER INTERSECT INTO IS MINUS MLSLABEL LEVEL LIKE MODE \n            MODIFY LOCK LONG NOAUDIT NOCOMPRESS MAXEXTENTS NOT NOTFOUND NOWAIT NULL NUMBER PCTFREE OF OFFLINE ON ONLINE PRIOR\n            PRIVILEGES OPTION OR PUBLIC ORDER RAW SELECT RENAME SESSION SET SHARE RESOURCE SIZE REVOKE SMALLINT ROW ROWID ROWLABEL\n            ROWNUM SQLBUF ROWS START UID SUCCESSFUL UNION UNIQUE SYNONYM SYSDATE TABLE UPDATE USER THEN VALIDATE VALIDATION VALUE\n            VALUES TO VARCHAR VARCHAR2 VIEW TRIGGER WHENEVER WHERE WITH').split()

    def addFunction(self, strNewFunctionName, argumentList, strReturn, strContents, attribs, diffs):
        newArgs = []
        for arg in argumentList:
            if ' IN ' not in arg.upper():
                arg = (' IN ').join(arg.split())
            newArgs.append(arg)

        info = {'functionname': self.quoteName(strNewFunctionName), 'arguments': (', ').join(newArgs), 'returns': strReturn, 'contents': strContents.replace("'", "''")}
        for strDdl in self.params['create_function']:
            diffs.append(('Add function', strDdl % info))