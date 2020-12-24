# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/atlassian/bamboo/xml-data/build-dir/QUOR-TEST-JOB1/tests/test_quorra.py
# Compiled at: 2017-01-09 20:07:55
import unittest, os, sys, subprocess, pandas, random
from datetime import datetime
import quorra
from . import __base__

class TestEntryPoints(unittest.TestCase):

    def call(self, subcommand, *args):
        return subprocess.check_output(('python -m quorra {} {}').format(subcommand, (' ').join(args)), stderr=subprocess.STDOUT, shell=True, cwd=__base__)

    def test_version(self):
        res = self.call('version')
        self.assertTrue(res, quorra.__version__)


class TestExport(unittest.TestCase):

    def call(self, cmd, *args):
        return subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True, cwd=__base__)

    @classmethod
    def setUpClass(cls):
        cls._time = datetime.now()

    @classmethod
    def tearDownClass(cls):
        qtime = datetime.now() - cls._time
        if qtime.microseconds > 500000:
            sys.stderr.write('\n\nWarning: Export tests took more than 5s to run!\n\n')

    def test_light_export(self):
        data = pandas.DataFrame({'x': [ i for i in range(0, 10) ], 'y': [ round(random.gauss(100, 10), 2) for i in range(0, 10) ], 'group': [
                   'default'] * 10})
        plt = quorra.line().data(data, x='x', y='y', group='group').xlabel('X Label').ylabel('Y Label').zoomable(True)
        outfile = '.quorra-export-test-light-export.png'
        quorra.export(plt, outfile)
        self.assertTrue(os.path.exists(outfile))
        os.remove(outfile)

    def test_heavy_export(self):
        points = 10000
        groups = ['one', 'two', 'three', 'four', 'five']
        data = pandas.DataFrame({'x': [ i for i in range(0, points) ] * len(groups), 'y': [ round(random.gauss(100, 10), 2) for i in range(0, points * len(groups)) ], 'group': [ grp for grp in groups for j in range(0, points) ]})
        plt = quorra.line().data(data, x='x', y='y', group='group').xlabel('X Label').ylabel('Y Label')
        outfile = '.quorra-export-test-heavy-export.png'
        quorra.export(plt, outfile)
        self.assertTrue(os.path.exists(outfile))
        os.remove(outfile)

    def test_phantomjs_quit(self):
        try:
            self.call('ps aux | grep phantomjs | grep -v grep')
            self.assertTrue(False)
        except subprocess.CalledProcessError:
            self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()