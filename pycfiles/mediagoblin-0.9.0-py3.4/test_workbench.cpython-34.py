# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tests/test_workbench.py
# Compiled at: 2016-03-29 15:18:42
# Size of source mod 2**32: 4661 bytes
import os, tempfile
from mediagoblin.tools import workbench
from mediagoblin.mg_globals import setup_globals
from mediagoblin.decorators import get_workbench
from mediagoblin.tests.test_storage import get_tmp_filestorage, cleanup_storage

class TestWorkbench(object):

    def setup(self):
        self.workbench_base = tempfile.mkdtemp(prefix='gmg_workbench_testing')
        self.workbench_manager = workbench.WorkbenchManager(self.workbench_base)

    def teardown(self):
        os.rmdir(self.workbench_base)

    def test_create_workbench(self):
        workbench = self.workbench_manager.create()
        assert os.path.isdir(workbench.dir)
        assert workbench.dir.startswith(self.workbench_manager.base_workbench_dir)
        workbench.destroy()

    def test_joinpath(self):
        this_workbench = self.workbench_manager.create()
        tmpname = this_workbench.joinpath('temp.txt')
        assert tmpname == os.path.join(this_workbench.dir, 'temp.txt')
        this_workbench.destroy()

    def test_destroy_workbench(self):
        this_workbench = self.workbench_manager.create()
        tmpfile_name = this_workbench.joinpath('temp.txt')
        tmpfile = open(tmpfile_name, 'w')
        with tmpfile:
            tmpfile.write('lollerskates')
        assert os.path.exists(tmpfile_name)
        wb_dir = this_workbench.dir
        this_workbench.destroy()
        assert not os.path.exists(tmpfile_name)
        assert not os.path.exists(wb_dir)

    def test_localized_file(self):
        tmpdir, this_storage = get_tmp_filestorage()
        this_workbench = self.workbench_manager.create()
        filepath = [
         'dir1', 'dir2', 'ourfile.txt']
        with this_storage.get_file(filepath, 'w') as (our_file):
            our_file.write(b'Our file')
        filename = this_workbench.localized_file(this_storage, filepath)
        assert filename == os.path.join(tmpdir, 'dir1/dir2/ourfile.txt')
        this_storage.delete_file(filepath)
        cleanup_storage(this_storage, tmpdir, ['dir1', 'dir2'])
        tmpdir, this_storage = get_tmp_filestorage(fake_remote=True)
        with this_storage.get_file(filepath, 'w') as (our_file):
            our_file.write(b'Our file')
        filename = this_workbench.localized_file(this_storage, filepath)
        assert filename == os.path.join(this_workbench.dir, 'ourfile.txt')
        filename = this_workbench.localized_file(this_storage, filepath, 'thisfile')
        assert filename == os.path.join(this_workbench.dir, 'thisfile.txt')
        filename = this_workbench.localized_file(this_storage, filepath, 'thisfile.text', False)
        assert filename == os.path.join(this_workbench.dir, 'thisfile.text')
        this_storage.delete_file(filepath)
        cleanup_storage(this_storage, tmpdir, ['dir1', 'dir2'])
        this_workbench.destroy()

    def test_workbench_decorator(self):
        """Test @get_workbench decorator and automatic cleanup"""
        setup_globals(workbench_manager=self.workbench_manager)

        @get_workbench
        def create_it(workbench=None):
            assert os.path.isdir(workbench.dir)
            return workbench.dir

        benchdir = create_it()
        assert not os.path.isdir(benchdir)