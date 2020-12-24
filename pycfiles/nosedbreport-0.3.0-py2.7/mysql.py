# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/nosedbreport/mysql.py
# Compiled at: 2014-02-26 22:25:53
import optparse
from datetime import datetime, timedelta
from base import NoseDBReporterBase
__author__ = 'Ali-Akber Saifee'
__email__ = 'ali@indydevs.org'
__copyright__ = 'Copyright 2014, Ali-Akber Saifee'

class NoseMySQLReporter(NoseDBReporterBase):
    """
    MySQL Connector. Reports the results of each test run into the tables
    ``testcase``, ``testsuite``, ``testcaseexecution`` and ``testsuiteexecution``
    """
    name = 'nosedbreport'
    run_insert_query = "\n    insert into testcaseexecution (testcase, startTime, timeTaken, status, traceback, suiteexecution)\n    values ('%(testcase)s', '%(startTime)s', '%(timeTaken)s', '%(status)s', '%(traceback)s', %(suiteexecution)d);\n    "
    case_start_query = "\n    insert into testcase values('%(id)s', '%(name)s', '%(description)s', '%(suite)s', '%(lastStarted)s', 0)\n    on duplicate key update lastStarted='%(lastStarted)s', description='%(description)s';\n    "
    suite_start_query = "\n    insert into testsuite (name, lastStarted) values('%(suite)s', '%(lastStarted)s')\n    on duplicate key update lastStarted='%(lastStarted)s';\n    "
    suite_complete_query = "\n    insert into testsuite (name, lastCompleted) values('%(suite)s', '%(lastCompleted)s')\n    on duplicate key update lastCompleted='%(lastCompleted)s';\n    "
    suiteexecution_complete_query = "\n    insert into testsuiteexecution (suite, startTime, endTime)\n    values ('%(suite)s', '%(startTime)s', '%(lastCompleted)s');\n    "
    case_complete_query = "\n    update testcase set lastCompleted = '%(lastCompleted)s';\n    "

    def __init__(self):
        NoseDBReporterBase.__init__(self)

    def __execute_query(self, query, args):
        """
        helper method to execute a MySQL query and commit
        the result.

        :param query: the query to execute
        :param args: variable arguments to use when formatting the query

        """
        for k, v in args.items():
            if type(v) == type('string'):
                args[k] = v.replace("'", "\\'")

        ret = 0
        try:
            import MySQLdb
            cursor = self.connection.cursor()
            ret = cursor.execute(query % args)
            self.connection.commit()
        except MySQLdb.ProgrammingError as e:
            self.logger.error('failed to execute query with error: %s' % str(e[1]))
        except Exception as e:
            self.logger.error('unknown error executing query: %s' % str(e))

        return ret

    def configure(self, options, conf):
        """
        sets up the MySQL database connection based on the options
        provided on the command line.
        """
        import MySQLdb
        try:
            self.connection = MySQLdb.connect(options.dbreport_host, options.dbreport_username, options.dbreport_password, options.dbreport_db, connect_timeout=5)
        except ImportError as e:
            self.enabled = False
            self.logger.error('The MySQLdb module is required for nosedbreporter to work with mysql')
        except MySQLdb.OperationalError as e:
            self.enabled = False
            self.logger.error(e[1])

    def report(self, stream):
        """
        After successful completion of a nose run, perform the final reporting
        of the test results to the MySQL database.
        """
        if self.connection:
            results = self.test_case_results
            suiteexecids = {}
            for suite in self.test_suites:
                suite_update = {'suite': suite, 'startTime': self.start_time, 'lastCompleted': self.test_suites[suite]['lastCompleted']}
                self.__execute_query(self.suite_complete_query, suite_update)
                self.__execute_query(self.suiteexecution_complete_query, suite_update)
                self.connection.query("\n                select id from testsuiteexecution where suite='%(suite)s' and\n                startTime='%(startTime)s' and\n                endTime='%(lastCompleted)s'\n                " % suite_update)
                result = self.connection.store_result()
                suiteexecids[suite] = result.fetch_row()[0][0]

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
        record initiation of a test case. Update the last start time
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
        super(NoseMySQLReporter, self).startTest(test)

    def construct_schema(self):
        """
        called when the `--dbreport_create_schema` command option
        is passed to the plugin to create the mysql table schema.
        """
        testcase_schema = '\n        CREATE TABLE `testcase` (\n          `id` varchar(255) NOT NULL,\n          `name` varchar(255) NOT NULL,\n          `description` varchar(255) NOT NULL,\n          `suite` varchar(255) NOT NULL,\n          `lastStarted` datetime DEFAULT NULL,\n          `lastCompleted` datetime DEFAULT NULL,\n          PRIMARY KEY (`id`),\n          KEY `idx_name` (`name`),\n          KEY `idx_suite` (`suite`),\n          CONSTRAINT `fk_suite_name` FOREIGN KEY (`suite`) REFERENCES `testsuite` (`name`)\n        ) ENGINE=InnoDB DEFAULT CHARSET=latin1\n        '
        testsuite_schema = '\n        CREATE TABLE `testsuite` (\n          `id` int(11) NOT NULL AUTO_INCREMENT,\n          `name` varchar(255) NOT NULL,\n          `lastStarted` datetime DEFAULT NULL,\n          `lastCompleted` datetime DEFAULT NULL,\n          PRIMARY KEY (`id`),\n          UNIQUE KEY `idx_name` (`name`) USING BTREE\n        ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1\n        '
        testcaseexecution_schema = "\n        CREATE TABLE `testcaseexecution` (\n          `id` int(11) NOT NULL AUTO_INCREMENT,\n          `testcase` varchar(255) NOT NULL,\n          `suiteexecution` int(11) NOT NULL,\n          `startTime` datetime NOT NULL,\n          `timeTaken` float NOT NULL,\n          `status` enum('success','fail','error','skipped','') NOT NULL,\n          `traceback` text NOT NULL,\n          PRIMARY KEY (`id`),\n          KEY `idx_status` (`status`),\n          KEY `idx_testcase` (`testcase`) USING BTREE,\n          KEY `idx_suiteexecution` (`suiteexecution`),\n          CONSTRAINT `fk_testcase_id` FOREIGN KEY (`testcase`) REFERENCES `testcase` (`id`),\n          CONSTRAINT `fk_suiteexec_id` FOREIGN KEY (`suiteexecution`) REFERENCES `testsuiteexecution` (`id`)\n        ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1\n        "
        testsuiteexecution_schema = '\n        CREATE TABLE `testsuiteexecution` (\n            `id` int(11) NOT NULL AUTO_INCREMENT,\n            `suite` varchar(255) NOT NULL,\n            `startTime` datetime NOT NULL,\n            `endTime` datetime NOT NULL,\n            PRIMARY KEY (`id`),\n            KEY `idx_start` (`startTime`),\n            KEY `idx_end` (`endTime`),\n            CONSTRAINT `fk_testsuite_name` FOREIGN KEY (`suite`) REFERENCES `testsuite` (`name`)\n        ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1\n        '
        if self.connection:
            cursor = self.connection.cursor()
            if not cursor.execute("show tables like 'test%%'") == 4:
                cursor.execute(testsuite_schema)
                cursor.execute(testcase_schema)
                cursor.execute(testsuiteexecution_schema)
                cursor.execute(testcaseexecution_schema)
            return True
        self.logger.error('Unable to setup scheme due to mysql configuration error')
        return False