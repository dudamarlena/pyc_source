# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vwa13376/workspace/uploader/archer/projects/tests.py
# Compiled at: 2013-08-20 06:16:18
import logging, os, shutil, uuid
from django.utils.unittest import TestCase
from archer.projects.models import Project, FileSystem
from archer.core import exceptions
logger = logging.getLogger(__name__)

class ProjectTestCase(TestCase):

    def setUp(self):
        uid = str(uuid.uuid4())[0:8]
        self.mount_point = '/tmp/cvmfs-%s' % uid
        self.fs = FileSystem.objects.create(mount_point=self.mount_point)
        os.makedirs(self.fs.mount_point)
        self.project1 = Project(file_system=self.fs, directory='project1')

    def test_full_path(self):
        project2 = Project(file_system=self.fs, directory='project2')
        self.assertEqual(project2.full_path(), os.path.join(self.fs.mount_point, 'project2'))

    def test_clear_dir(self):
        directory = os.path.join(self.fs.mount_point, 'project2')
        if not os.path.exists(directory):
            os.makedirs(directory)
        project2 = Project(file_system=self.fs, directory='project2')
        try:
            project2.clear_dir()
        except (IOError, OSError, exceptions.ValidationError) as e:
            logger.error(e)
            self.fail(e)

    def test_clear_dir_no_dir(self):
        directory = os.path.join(self.fs.mount_point, 'project2')
        if os.path.exists(directory):
            shutil.rmtree(directory)
        with self.assertRaises(exceptions.ValidationError):
            p = Project(file_system=self.fs, directory='project2')
            p.clear_dir()

    def test_clear_dir_no_chmod(self):
        directory = os.path.join(self.fs.mount_point, 'project2')
        if not os.path.exists(directory):
            os.makedirs(directory)
        os.mkdir(os.path.join(directory, 'something'))
        os.chmod(directory, 1280)
        with self.assertRaises(OSError):
            p = Project(file_system=self.fs, directory='project2')
            p.clear_dir()

    def test_clear_dir_no_mount_point_chmod(self):
        directory = os.path.join(self.fs.mount_point, 'project2')
        if not os.path.exists(directory):
            os.makedirs(directory)
        os.mkdir(os.path.join(directory, 'something'))
        os.chmod(self.fs.mount_point, 1316)
        with self.assertRaises(exceptions.ValidationError):
            p = Project(file_system=self.fs, directory='project2')
            p.clear_dir()

    def test_subdir_none_or_empty(self):
        path = '%s/%s' % (self.mount_point, self.project1.directory)
        dir0 = self.project1.subdir()
        dir1 = self.project1.subdir(None)
        dir2 = self.project1.subdir('')
        dir3 = self.project1.subdir('.')
        dir4 = self.project1.subdir('././.')
        self.assertEqual(dir0, path)
        self.assertEqual(dir1, path)
        self.assertEqual(dir2, path)
        self.assertEqual(dir3, path)
        self.assertEqual(dir4, path)
        return

    def test_subdir_allowed_parent(self):
        subdir = 'foo/bar'
        path = '%s/%s/%s' % (self.mount_point, self.project1.directory, subdir)
        dir = self.project1.subdir('foo/bar/../bar')
        self.assertEqual(dir, path)

    def test_subdir_disallowed_parent(self):
        with self.assertRaises(exceptions.ValidationError):
            self.project1.subdir('foo/../../foo/bar')

    def test_subdir_root_dir(self):
        with self.assertRaises(exceptions.ValidationError):
            self.project1.subdir('/tmp')

    def tearDown(self):
        self.fs.delete()
        os.chmod(self.mount_point, 511)
        for r, d, f in os.walk(self.mount_point):
            os.chmod(r, 511)

        shutil.rmtree(self.mount_point, ignore_errors=False)