# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/nosedbreport/sqlite.py
# Compiled at: 2014-02-26 22:25:53
import optparse
from datetime import datetime, timedelta
from base import NoseDBReporterBase
__author__ = 'Ali-Akber Saifee'
__email__ = 'ali@indydevs.org'
__copyright__ = 'Copyright 2014, Ali-Akber Saifee'

class NoseSQLiteReporter(NoseDBReporterBase):
    """
    SQLLite Connector. Reports the results of each test run into the tables
    ``testcase``, ``testsuite``,``testcaseexecution`` and ``testsuiteexecution``
    """
    name = 'nosedbreport'
    run_insert_query = "\n    insert into testcaseexecution (testcase, startTime, timeTaken, status, traceback, suiteexecution)\n    values ('%(testcase)s', '%(startTime)s', '%(timeTaken)s', '%(status)s', '%(traceback)s', %(suiteexecution)d);\n    "
    case_start_query = "\n    replace into testcase values('%(id)s', '%(name)s', '%(description)s', '%(suite)s', '%(lastStarted)s', 0)\n    "
    suite_start_query = "\n    replace into testsuite (name, lastStarted) values('%(suite)s', '%(lastStarted)s')\n    "
    suite_complete_query = "\n    replace into testsuite (name, lastCompleted) values('%(suite)s', '%(lastCompleted)s');\n    "
    suiteexecution_complete_query = "\n    insert into testsuiteexecution (suite, startTime, endTime)\n    values ('%(suite)s', '%(startTime)s', '%(lastCompleted)s');\n    "
    case_complete_query = "\n    update testcase set lastCompleted = '%(lastCompleted)s';\n    "

    def __init__(self):
        NoseDBReporterBase.__init__(self)

    def __execute_query(self, query, args):
        """
        helper method to execute a sqlite query and commit
        the result.

        :param query: the query to execute
        :param args: variable length argument list used to format ``query``
        """
        for k, v in args.items():
            if type(v) == type('string'):
                args[k] = v.replace("'", "''")

        ret = 0
        try:
            import sqlite3
            cursor = self.connection.cursor()
            ret = cursor.execute(query % args)
            self.connection.commit()
        except sqlite3.ProgrammingError as e:
            self.logger.error('failed to execute query with error: %s' % str(e[1]))
        except Exception as e:
            self.logger.error('unknown error executing query %s: %s' % (query % args, str(e)))

        return ret

    def configure(self, options, conf):
        """
        sets up the sqlite database connection
        """
        import sqlite3
        try:
            self.connection = sqlite3.connect(options.dbreport_db)
        except ImportError as e:
            self.enabled = False
            self.logger.error('The sqlite3 module is required for nosedbreporter to work with sqlite')
        except sqlite3.OperationalError as e:
            self.enabled = False
            self.logger.error(e)

    def report(self, stream):
        """
        After successful completion of a nose run, perform the final reporting
        of the test results to the sqlite database.
        """
        if self.connection:
            results = self.test_case_results
            suiteexecids = {}
            for suite in self.test_suites:
                suite_update = {'suite': suite, 'startTime': self.start_time, 'lastCompleted': self.test_suites[suite]['lastCompleted']}
                self.__execute_query(self.suite_complete_query, suite_update)
                self.__execute_query(self.suiteexecution_complete_query, suite_update)
                cur = self.connection.cursor()
                cur.execute("\n                    select id from testsuiteexecution where suite='%(suite)s' and\n                    startTime='%(startTime)s' and\n                    endTime='%(lastCompleted)s'\n                    " % suite_update)
                suiteexecids[suite] = cur.fetchone()[0]

            for case in results:
                case_update = {'id': case, 'name': results[case]['name'], 'description': results[case]['description'], 
                   'suite': results[case]['suite'], 
                   'lastStarted': results[case]['lastStarted'], 
                   'lastCompleted': (datetime.strptime(results[case]['lastStarted'], self.time_fmt) + timedelta(seconds=results[case]['timeTaken'])).strftime(self.time_fmt)}
                run_update = {'testcase': case, 'suite': results[case]['suite'], 
                   'suiteexecution': suiteexecids[results[case]['suite']], 
                   'startTime': results[case]['lastStarted'], 
                   'timeTaken': results[case]['timeTaken'], 
                   'status': results[case]['status'], 
                   'traceback': results[case]['traceback']}
                self.__execute_query(self.case_complete_query, case_update)
                self.__execute_query(self.run_insert_query, run_update)

    def startTest(self, test):
        """
        record initiation of a test case (``test``). Update the last start time
        of the test suite &  test case.
        """
        if self.connection:
            description = self.get_full_doc(test)
            test_id = test.id()
            file_path, suite, case = test.address()
            case_update = {'id': test_id, 'name': case, 
               'description': description, 
               'suite': suite, 
               'lastStarted': NoseDBReporterBase.time_now()}
            suite_update = {'suite': suite, 'lastStarted': NoseDBReporterBase.time_now()}
            self.__execute_query(self.suite_start_query, suite_update)
            self.__execute_query(self.case_start_query, case_update)
        super(NoseSQLiteReporter, self).startTest(test)

    def construct_schema(self):
        """
        called when the `--dbreport_create_schema` command option
        is passed to the plugin to create the sqlite table schema.
        """
        testcase_schema = '\n        CREATE TABLE testcase(\n            id    TEXT PRIMARY KEY,\n            name  TEXT,\n            description TEXT,\n            suite TEXT,\n            lastStarted TEXT,\n            lastCompleted TEXT,\n            FOREIGN KEY(suite) REFERENCES testsuite(name)\n        )'
        testsuite_schema = '\n        CREATE TABLE testsuite(\n          id INTEGER PRIMARY KEY,\n          name TEXT UNIQUE,\n          lastStarted TEXT,\n          lastCompleted TEXT\n        )\n        '
        testcaseexecution_schema = '\n        CREATE TABLE testcaseexecution (\n          id INTEGER PRIMARY KEY,\n          testcase TEXT,\n          suiteexecution INTEGER,\n          startTime TEXT,\n          timeTaken REAL,\n          status TEXT,\n          traceback TEXT,\n          FOREIGN KEY(testcase) REFERENCES testcase(id),\n          FOREIGN KEY(suiteexecution) REFERENCES testsuiteexecution(id)\n        )\n        '
        testsuiteexecution_schema = '\n        CREATE TABLE `testsuiteexecution` (\n           id INTEGER PRIMARY KEY,\n           suite TEXT,\n           startTime TEXT,\n           endTime TEXT,\n           FOREIGN KEY(suite) REFERENCES testsuite(name)\n        )\n        '
        indices = ['CREATE INDEX idx_name on testcase(name)',
         'CREATE INDEX tc_idx_suite on testcase(suite)',
         'CREATE INDEX ts_idx_name on testsuite(name)',
         'CREATE INDEX tce_idx_status on testcaseexecution(status)',
         'CREATE INDEX tce_idx_testcase on testcaseexecution(testcase)',
         'CREATE INDEX tce_idx_suiteexecution on testcaseexecution(suiteexecution)',
         'CREATE INDEX tse_idx_start on testsuiteexecution(startTime)',
         'CREATE INDEX tse_idx_end on testsuiteexecution(endTime)']
        if self.connection:
            cursor = self.connection.cursor()
            cursor.execute(testsuite_schema)
            cursor.execute(testcase_schema)
            cursor.execute(testsuiteexecution_schema)
            cursor.execute(testcaseexecution_schema)
            for index in indices:
                cursor.execute(index)

            return True
        self.logger.error('Unable to setup scheme due to mysql configuration error')
        return False