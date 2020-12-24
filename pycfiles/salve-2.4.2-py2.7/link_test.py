# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/tests/system/link_test.py
# Compiled at: 2015-11-06 23:45:35
import os
from nose.tools import istest
from tests import system

class TestWithScratchdir(system.RunScratchContainer):

    @istest
    def copy_symlink(self):
        """
        System: Copy Symlink

        Runs a manifest which copies a symlink and verifies the contents of
        the destination link.
        """
        content = 'file { action copy source 1 target 2 }\n'
        self.write_file('1.man', content)
        fullname1 = self.get_fullname('1')
        fullname2 = self.get_fullname('2')
        man_fullname = self.get_fullname('1.man')
        os.symlink(man_fullname, fullname1)
        self.run_on_manifest('1.man')
        assert self.exists('2')
        s = self.read_file('2')
        assert s == content, '%s' % s
        assert os.path.islink(fullname2)
        assert os.readlink(fullname2) == man_fullname