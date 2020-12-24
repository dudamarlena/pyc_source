# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-1.7.35-i686/egg/seedbox/tests/tasks/test_filecopy.py
# Compiled at: 2015-06-14 13:30:57
import os
from seedbox.db import models
from seedbox.tasks import filecopy
from seedbox.tests import test

class FileCopyTest(test.ConfiguredBaseTestCase):

    def setUp(self):
        super(FileCopyTest, self).setUp()
        if not os.path.exists(self.CONF.tasks.sync_path):
            os.mkdir(self.CONF.tasks.sync_path)
        self.media_file = models.MediaFile.make_empty()
        self.media_file.compressed = 0
        self.media_file.filename = 'fake_copy.mp4'
        self.media_file.file_path = '/tmp'
        open(os.path.join('/tmp', 'fake_copy.mp4'), 'w').close()

    def test_actionable(self):
        self.assertTrue(filecopy.CopyFile.is_actionable(self.media_file))

    def test_execute(self):
        task = filecopy.CopyFile(self.media_file)
        files = task()
        self.assertEqual(files[0].file_path, self.CONF.tasks.sync_path)