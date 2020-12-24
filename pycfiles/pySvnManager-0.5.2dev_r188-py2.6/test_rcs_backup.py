# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysvnmanager/tests/test_rcs_backup.py
# Compiled at: 2010-06-08 22:36:02
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from pysvnmanager.tests import *
from pysvnmanager import model
from pysvnmanager.model import rcsbackup as rcs
import StringIO, time

class TestRcsBackup(TestController):
    wcfile = '%s/%s' % (os.path.dirname(os.path.abspath(__file__)), 'rcstest.txt')
    wcpath = os.path.dirname(os.path.abspath(wcfile))
    if os.path.isdir(wcpath + '/RCS'):
        rcsfile = wcpath + '/RCS/' + os.path.basename(wcfile) + ',v'
    else:
        rcsfile = wcfile + ',v'

    def setUp(self):
        if os.access(self.wcfile, os.R_OK):
            os.remove(self.wcfile)
        if os.access(self.rcsfile, os.R_OK):
            os.remove(self.rcsfile)

    def tearDown(self):
        if os.access(self.wcfile, os.R_OK):
            os.remove(self.wcfile)
        if os.access(self.rcsfile, os.R_OK):
            os.remove(self.rcsfile)

    def writefile(self, rev=None):
        if not rev:
            rev = self.get_revision() + 1
        elif not isinstance(rev, int):
            rev = int(rev)
        f = open(self.wcfile, 'w')
        f.write('RCS working copy file\n')
        f.write('====================' + '\n')
        f.write('Revision: %d\n' % rev)
        f.write('Date: %s\n' % time.strftime('%F'))
        f.close()

    def get_revision(self):
        rev = 0
        if os.access(self.wcfile, os.F_OK):
            f = open(self.wcfile, 'r')
            for line in f:
                line = line.strip()
                if line.startswith('Revision: '):
                    rev = int(line.split(':', 1)[1])
                    break

        return rev

    def testBackup(self):
        self.writefile()
        assert self.get_revision() == 1, self.get_revision()
        assert os.access(self.wcfile, os.R_OK)
        assert not os.access(self.rcsfile, os.R_OK)
        rcs.backup(self.wcfile)
        assert os.access(self.wcfile, os.R_OK)
        assert os.path.exists(self.rcsfile)
        assert os.access(self.rcsfile, os.R_OK), self.rcsfile
        self.writefile()
        assert os.access(self.rcsfile, os.R_OK)
        rcs.backup(self.wcfile)
        self.assertRaises(Exception, rcs.backup, '')

    def testRestore(self):
        rcs.restore('')
        self.writefile()
        rcs.backup(self.wcfile)
        os.remove(self.wcfile)
        assert not os.access(self.wcfile, os.R_OK)
        rcs.restore(self.wcfile)
        assert self.get_revision() == 1, self.get_revision()
        self.writefile()
        rcs.backup(self.wcfile)
        self.writefile()
        assert self.get_revision() == 3, self.get_revision()
        rcs.restore(self.wcfile)
        assert self.get_revision() == 2, self.get_revision()
        rcs.restore(self.wcfile, '1.1')
        assert self.get_revision() == 1, self.get_revision()
        self.writefile(5)
        rcs.backup(self.wcfile)
        assert self.get_revision() == 5, self.get_revision()
        os.remove(self.wcfile)
        assert not os.access(self.wcfile, os.R_OK)
        rcs.restore(self.wcfile)
        assert self.get_revision() == 5, self.get_revision()

    def testRevision(self):
        self.writefile()
        assert os.access(self.wcfile, os.R_OK)

    def testLogs(self):
        rcslog = rcs.RcsLog(self.wcfile)
        rcslog.log_per_page = 10
        for i in range(1, rcslog.log_per_page + 1):
            self.writefile(i)
            rcs.backup(self.wcfile, comment='Test no. %d' % i, user='User1')
            rcslog.reload()
            assert rcslog.total == i, rcslog.total
            assert rcslog.total_page == 1, rcslog.total_page

        rcslog.reload()
        assert 'rcstest.txt,v' in rcslog.rcsfile, rcslog.rcsfile
        assert rcslog.head == '1.10', rcslog.head
        assert rcslog.total == 10, rcslog.total
        for i in range(11, 15):
            self.writefile(i)
            rcs.backup(self.wcfile, comment='第 %d 次提交测试。' % i, user='蒋鑫')

        assert rcslog.head == '1.10', rcslog.head
        rcslog.reload()
        assert rcslog.head == '1.14', rcslog.head
        assert rcslog.total == 14, rcslog.total
        logs = rcslog.get_logs()
        assert len(logs) == 14, logs
        assert logs[3]['revision'] == '1.4', logs[3]['revision']
        assert logs[3]['author'] == 'User1', logs[3]['author']
        assert logs[3]['log'] == 'Test no. 4', logs[3]['log']
        assert logs[13]['revision'] == '1.14', logs[13]['revision']
        assert logs[13]['author'] == '蒋鑫', logs[13]['author'].encode('utf-8')
        assert logs[13]['log'] == '第 14 次提交测试。', logs[13]['log'].encode('utf-8')
        logs = rcslog.get_logs('1.9', '1.12')
        assert len(logs) == 4, logs
        assert logs[1]['revision'] == '1.10', logs[1]['revision']
        assert logs[1]['author'] == 'User1', logs[1]['author']
        assert logs[1]['log'] == 'Test no. 10', logs[1]['log']
        assert logs[2]['revision'] == '1.11', logs[2]['revision']
        assert logs[2]['author'] == '蒋鑫', logs[2]['author'].encode('utf-8')
        assert logs[2]['log'] == '第 11 次提交测试。', logs[2]['log'].encode('utf-8')
        logs = rcslog.get_logs('', '1.12')
        assert len(logs) == 12, logs
        assert logs[10]['revision'] == '1.11', logs[10]['revision']
        logs = rcslog.get_logs('1.12', '')
        assert len(logs) == 3, len(logs)
        assert logs[1]['revision'] == '1.13', logs[1]['revision']
        logs = rcslog.get_logs('1.7', '1.11', '1.14')
        assert len(logs) == 6, len(logs)
        assert logs[4]['revision'] == '1.11', logs[1]['revision']
        assert logs[5]['revision'] == '1.14', logs[1]['revision']
        assert rcslog.total_page == 2, rcslog.total_page
        rcslog.log_per_page = 0
        assert rcslog.log_per_page > 1, rcslog.log_per_page
        rcslog.log_per_page = 5
        assert rcslog.log_per_page == 5, rcslog.log_per_page
        assert rcslog.total_page == 3, rcslog.total_page
        logs = rcslog.get_page_logs(1)
        logs2 = rcslog.get_page_logs(0)
        assert logs == logs2
        assert [ x['revision'] for x in logs ] == [
         '1.9', '1.10', '1.11', '1.12', '1.13', '1.14'], [ x['revision'] for x in logs ]
        logs = rcslog.get_page_logs(2)
        assert [ x['revision'] for x in logs ] == [
         '1.5', '1.6', '1.7', '1.8', '1.9', '1.14'], [ x['revision'] for x in logs ]
        logs = rcslog.get_page_logs(3)
        logs2 = rcslog.get_page_logs(30)
        assert logs == logs2
        assert [ x['revision'] for x in logs ] == [
         '1.1', '1.2', '1.3', '1.4', '1.5', '1.14'], [ x['revision'] for x in logs ]
        buff = rcslog.differ('1.2', '1.5')
        assert '-Revision: 2\n+Revision: 5' in buff, buff
        buff = rcslog.differ('1.13')
        assert '-Revision: 13\n+Revision: 14' in buff, buff
        buff = rcslog.cat()
        assert 'Revision: 14\n' in buff, buff
        buff = rcslog.cat('1.8')
        assert 'Revision: 8\n' in buff, buff

    def testLogsNone(self):
        rcslog = rcs.RcsLog(self.wcfile)
        assert rcslog.rcsfile == '', rcslog.rcsfile
        assert rcslog.total == 0, rcslog.total
        assert rcslog.get_page_logs(1) == [], rcslog.get_page_logs(1)
        assert rcslog.cat() == ''


if __name__ == '__main__':
    import unittest
    unittest.main()