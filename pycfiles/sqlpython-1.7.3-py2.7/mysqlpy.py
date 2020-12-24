# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sqlpython/mysqlpy.py
# Compiled at: 2012-05-26 21:31:46
from sqlpyPlus import *
import sys, tempfile, optparse, unittest

class mysqlpy(sqlpyPlus):
    r"""
MySqlPy V1.7.3 - 'sqlplus in python'
Author: Luca.Canali@cern.ch
Rev: 1.7.3, 06-Feb-10

Companion of SqlPython, a python module that reproduces Oracle's command line within python
and sqlpyPlus. Major contributions by Catherine Devlin, http://catherinedevlin.blogspot.com

Usage: sqlpython [connect string] [single-word command] ["multi-word command"]...

Quick start command list:

- top     -> executes a query to list all active sessions in (Oracle 10g and RAC)
             (use: instance activity monitoring, a DBA tool)
- tselect -> prints the result set in trasposed form, useful to print result sets with
             many columns such as dba_ or v$ views (ex: dba_tables or v$instance)
- py      -> execute a python command (C.D.) 
- db      -> quick connect using credentials in pass.txt file
             (Ex: write username and pass in pass.txt and then "db db_alias" to connect)
- sql     -> prints the sql text from the cache. parameter: sql_id of the statement
             (Ex: sql fzqa1qj65nagki)
- explain -> prints the execution plan from the cache. parameter: sql_id of the statement 
- sessinfo-> prints session information. 1 parameter sid (Ex: sql 101 print info for sid 101)
- longops -> prints from gv$session_longops (running full scans, etc)
- load    -> prints the OS load on all cluster nodes (10g RAC)
- sleect,slect  -> alias for select (I mistyped select this way too many times...)
- top9i   -> 9i (and single instance) version of top
- describe, @, !, spool, show, set, list, get, write -> sql*plus-like, from sqlpyPlus (C.D.)
- shortcuts: \c (connect), \d (describe), etc, from sqlpyPlus (C.D.)
- :myvarname = xx, set autobind 1, print -> bind variables management extension, to sqlplus (C.D.)

Example:
 SQL> connect username@dbalias or username/pass@dbalias
 SQL> select sysdate from dual;
 SQL> exit
    """

    def __init__(self):
        sqlpyPlus.__init__(self)
        self.maxtselctrows = 10
        self.query_load10g = "\n\t  ins.instance_name,ins.host_name,round(os.value,2) load\n\t  from gv$osstat os, gv$instance ins\n\t  where os.inst_id=ins.inst_id and os.stat_name='LOAD'\n\t  order by 3 desc\n        "
        self.query_top9i = 'SELECT\n          sid,username,osuser||\'@\'||terminal "Server User@terminal",program,taddr, status,\n\t  module, sql_hash_value hash, fixed_table_sequence seq, last_call_et elaps \n          from v$session \n          where username is not null and program not like \'emagent%\' and status=\'ACTIVE\'\n                and audsid !=sys_context(\'USERENV\',\'SESSIONID\') ;\n        '
        self.query_ractop = 'SELECT \n \tinst_id||\'_\'||sid inst_sid,username,osuser||\'@\'||terminal "User@Term",program, decode(taddr,null,null,\'NN\') tr,  \n\tsql_id, \'.\'||mod(fixed_table_sequence,1000) seq, state||\': \'||event event,\n\tcase state when \'WAITING\' then seconds_in_wait else wait_time end w_tim, last_call_et elaps\n        from gv$session \n        where status=\'ACTIVE\' and username is not null \n\t      and not (event like \'% waiting for messages in the queue\' and state=\'WAITING\')\n              and audsid !=sys_context(\'USERENV\',\'SESSIONID\');\n        '
        self.query_longops = 'SELECT\n        inst_id,sid,username,time_remaining remaining, elapsed_seconds elapsed, sql_hash_value hash, opname,message\n        from gv$session_longops\n        where time_remaining>0;\n        '

    def do_top9i(self, args):
        """Runs query_top9i defined above, to display active sessions in Oracle 9i
           (Availability: Oracle)"""
        self.onecmd(self.query_top9i)

    def do_top(self, args):
        """Runs query_ractop defined above, to display active sessions in Oracle 10g (and RAC)
           (Availability: Oracle)"""
        self.onecmd(self.query_ractop)

    def do_longops(self, args):
        """Runs query_longops defined above, to display long running operations (full scans, etc)
           (Availability: Oracle)"""
        self.onecmd(self.query_longops)

    def do_load(self, args):
        """Runs query_load10g defined above, to display OS load on cluster nodes (10gRAC)
Do not confuse with `GET myfile.sql` and `@myfile.sql`,
which get and run SQL scripts from disk.
           (Availability: Oracle)"""
        self.onecmd(self.query_load10g)

    def do_db(self, args, filepath='pass.txt'):
        """Exec do_connect to db_alias in args (credentials form the file pass.txt) """
        try:
            f = open(filepath, 'r')
        except IOError:
            self.perror('Need a file %s containing username/password' % filepath)
            raise

        connectstr = f.readline().strip()
        if args:
            connectstr += '@' + args
        self.do_connect(connectstr)
        f.close()

    def do_tselect(self, arg):
        r"""
        Executes a query and prints the result in trasposed form;
        equivalent to terminating query with `\t` instead of `;`.
        Useful when querying tables with many columns and few rows."""
        self.do_select(self.parsed(arg, terminator='\\t'))

    def do_sql(self, args):
        """prints sql statement give the sql_id (Oracle 10gR2)"""
        self.query = "select inst_id, sql_fulltext from gv$sqlstats where sql_id='" + args + "'"
        try:
            self.curs.execute(self.query)
            row = self.curs.fetchone()
            self.poutput('\nSQL statement from cache')
            self.poutput('------------------------\n')
            while row:
                self.poutput('\nINST_ID = ' + str(row[0]) + ' - SQL TEXT:\n' + row[1].read())
                row = self.curs.next()

        except Exception as e:
            self.perror(e)

    def do_explain(self, args):
        """prints the plan of a given statement from the sql cache. 1 parameter: sql_id, see also do_sql
           (Availability: Oracle)"""
        words = args.split()
        if len(words) > 2 and words[0].lower() == 'plan' and words[1].lower() == 'for':
            self.curs.execute('explain %s' % args)
            self.pfeedback('Explained.  (see plan table)')
            return
        self.query = "select * from table(dbms_xplan.display_cursor('" + args + "'))"
        try:
            self.curs.execute(self.query)
            rows = self.curs.fetchall()
            desc = self.curs.description
            self.rc = self.curs.rowcount
            if self.rc > 0:
                self.poutput('\n' + self.pmatrix(rows, desc, 200))
        except Exception as e:
            self.perror(e)

    if cx_Oracle:

        def do_sessinfo(self, args):
            """Reports session info for the given sid, extended to RAC with gv$"""
            try:
                if not args:
                    self.curs.execute('SELECT sid FROM v$mystat')
                    args = self.curs.fetchone()[0]
                self.onecmd('SELECT * from gv$session where sid=%s\\t' % args)
            except cx_Oracle.DatabaseError as e:
                if 'table or view does not exist' in str(e):
                    self.perror('This account has not been granted SELECT privileges to v$mystat or gv$session.')
                else:
                    raise

    def do_sleect(self, args):
        """implements sleect = select, a common typo"""
        self.do_select(args)

    do_slect = do_sleect


def run():
    mysqlpy().cmdloop()


if __name__ == '__main__':
    run()