# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/joshbraegger/bc/git-crucible/crucible/tests/test_git.py
# Compiled at: 2012-03-26 00:22:52
import unittest
from mock import patch, MagicMock
from crucible import git
import urllib2, os

class GitTest(unittest.TestCase):

    def setUp(self):
        self.curr = os.getcwd()
        os.chdir(os.path.join(os.path.dirname(__file__), 'data/repo1'))
        os.rename('git', '.git')

    def tearDown(self):
        os.rename('.git', 'git')
        os.chdir(self.curr)

    def test_diff(self):
        res = git.diff('HEAD^..')
        self.assertEquals(res, 'diff --git a/test2 b/test2\nindex 180cf83..84a746b 100644\n--- a/test2\n+++ b/test2\n@@ -1 +1,2 @@\n test2\n+test3\n')

    def test_diff_error(self):
        try:
            res = git.diff('HEAD^^^..')
        except Exception, e:
            self.assertEquals(str(e), "fatal: ambiguous argument 'HEAD^^^..': unknown revision or path not in the working tree.\nUse '--' to separate paths from revisions\n")
        else:
            assert False, "Didn't raise an exception"

    def test_show(self):
        res = git.show('HEAD^^..')
        self.assertEquals(len(res), 2)
        self.assertEquals(res[0]['commit'], '970c00a734bae26c459c09e9d346b3457fdf8e40')
        self.assertEquals(res[0]['patch'], 'diff --git a/test2 b/test2\nnew file mode 100644\nindex 0000000..180cf83\n--- /dev/null\n+++ b/test2\n@@ -0,0 +1 @@\n+test2\n\n')
        self.assertEquals(res[1]['commit'], '9cca389d388e75eda4e07d4a0e0eba078a08e3dc')
        self.assertEquals(res[1]['patch'], 'diff --git a/test2 b/test2\nindex 180cf83..84a746b 100644\n--- a/test2\n+++ b/test2\n@@ -1 +1,2 @@\n test2\n+test3\n\n')