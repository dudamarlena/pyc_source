# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/ore/svn/tests/_base.py
# Compiled at: 2008-05-06 04:09:09
"""
$Id: _base.py 2197 2008-05-06 08:09:08Z hazmat $
"""
import os, bz2, transaction
from unittest import TestCase
from svn import repos
from ore.svn import SubversionContext
from StringIO import StringIO
test_home = os.path.join(os.path.abspath(os.path.dirname(__file__)))
test_repo_path = os.path.join(test_home, 'testrepo')

def setUp(test):
    dumpfile = bz2.BZ2File(os.path.join(os.path.dirname(__file__), 'testrepo.dump.bz2'))
    repository = repos.create(test_repo_path, '', '', None, None)
    repos.load_fs2(repository, dumpfile, StringIO(), repos.svn_repos_load_uuid_default, '', 0, 0, None)
    return


def tearDown(test):
    transaction.abort()
    if os.path.exists(test_repo_path):
        repos.delete(test_repo_path)


class SubversionTest(TestCase):

    def setUp(self):
        setUp(self)
        self.ctx = SubversionContext(test_repo_path, '/core')
        self.root = self.ctx.getSVNRootObject()

    def tearDown(self):
        transaction.abort()
        del self.root
        self.ctx.clear()
        del self.ctx
        tearDown(self)