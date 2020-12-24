# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/plugins/ioplugins/test/test_virtualfilesystem.py
# Compiled at: 2018-10-10 10:26:28
# Size of source mod 2**32: 5803 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, random, shutil, string, tempfile, fastr

class TestVFS:

    def setup(self):
        self.vfs_plugin = fastr.plugin_manager['VirtualFileSystem']
        fastr.log.info('Setup')
        self.dir = os.path.join(fastr.config.mounts['tmp'], '_test')
        if os.path.exists(self.dir):
            fastr.log.warning('Cleaning up existing temporary test directory {}'.format(self.dir))
            shutil.rmtree(self.dir)
        os.makedirs(self.dir)
        fastr.log.info('Using temporary directory {}'.format(self.dir))
        if not os.path.isdir(self.dir):
            fastr.log.critical('Temporary directory not available!')
        self.source_dir = os.path.join(self.dir, 'source')
        os.mkdir(self.source_dir)
        self.destination_dir = os.path.join(self.dir, 'destination')
        os.mkdir(self.destination_dir)
        self.handle, self.absfilename = tempfile.mkstemp(dir=self.source_dir)
        self.filename = os.path.basename(self.absfilename)
        self.niigz_handle, self.niigz_absfilename = tempfile.mkstemp(dir=self.source_dir, suffix='.nii.gz')
        self.niigz_filename = os.path.basename(self.niigz_absfilename)
        fastr.log.info('Created {} and {}'.format(self.absfilename, self.niigz_absfilename))
        if not os.path.exists(self.absfilename):
            fastr.log.critical('Source file {} does not exist!'.format(self.absfilename))
        if not os.path.exists(self.niigz_absfilename):
            fastr.log.critical('Source file {} does not exist!'.format(self.niigz_absfilename))

    def random_unique_string(self, length=8, existing=None):
        """ Return a random alpha-numeric string with a certain length. """
        s = ''.join([random.choice(string.ascii_letters + string.digits) for ch in range(length)])
        if existing is not None and s in existing:
            s = self.random_unique_string(length, existing)
        return s

    def test_ioplugins_pull_source_data_no_extension(self):
        output_file = os.path.join(self.destination_dir, self.filename)
        self.vfs_plugin.pull_source_data('vfs://tmp/_test/source/{}'.format(self.filename), self.destination_dir, 'id_0', datatype=fastr.types['NiftiImageFile'])
        @py_assert1 = os.path
        @py_assert3 = @py_assert1.isfile
        @py_assert6 = @py_assert3(output_file)
        if not @py_assert6:
            @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.isfile\n}(%(py5)s)\n}') % {'py7': @pytest_ar._saferepr(@py_assert6), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(output_file) if 'output_file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output_file) else 'output_file'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert6 = None
        if os.path.isfile(output_file):
            os.remove(output_file)

    def test_ioplugins_pull_source_data_niigz(self):
        self.vfs_plugin.pull_source_data('vfs://tmp/_test/source/{}'.format(self.filename), self.destination_dir, 'id_nii_0', datatype=fastr.types['NiftiImageFileCompressed'])
        output_file = os.path.join(self.destination_dir, self.filename)
        @py_assert1 = os.path
        @py_assert3 = @py_assert1.isfile
        @py_assert6 = @py_assert3(output_file)
        if not @py_assert6:
            @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.isfile\n}(%(py5)s)\n}') % {'py7': @pytest_ar._saferepr(@py_assert6), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(output_file) if 'output_file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output_file) else 'output_file'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert6 = None
        if os.path.isfile(output_file):
            os.remove(output_file)

    def test_ioplugins_pull_source_data_mhd(self):
        absfilename_mhd = os.path.join(fastr.config.mounts['example_data'], 'images', 'mrwhite.mhd')
        absfilename_raw = os.path.join(fastr.config.mounts['example_data'], 'images', 'mrwhite.raw')
        filename_mhd = os.path.basename(absfilename_mhd)
        filename_raw = os.path.basename(absfilename_raw)
        destination_path = self.destination_dir
        destination_path_mhd = os.path.join(self.destination_dir, filename_mhd)
        destination_path_raw = os.path.join(self.destination_dir, filename_raw)
        if os.path.exists(destination_path_mhd):
            os.remove(destination_path_mhd)
        if os.path.exists(destination_path_raw):
            os.remove(destination_path_raw)
        self.vfs_plugin.pull_source_data(self.vfs_plugin.path_to_url(absfilename_mhd), destination_path, 'id_mhd_0', datatype=fastr.types['ITKImageFile'])
        @py_assert1 = os.path
        @py_assert3 = @py_assert1.isfile
        @py_assert6 = @py_assert3(destination_path_mhd)
        if not @py_assert6:
            @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.isfile\n}(%(py5)s)\n}') % {'py7': @pytest_ar._saferepr(@py_assert6), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(destination_path_mhd) if 'destination_path_mhd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(destination_path_mhd) else 'destination_path_mhd'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert6 = None
        @py_assert1 = os.path
        @py_assert3 = @py_assert1.isfile
        @py_assert6 = @py_assert3(destination_path_raw)
        if not @py_assert6:
            @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.isfile\n}(%(py5)s)\n}') % {'py7': @pytest_ar._saferepr(@py_assert6), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(destination_path_raw) if 'destination_path_raw' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(destination_path_raw) else 'destination_path_raw'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert6 = None

    def test_ioplugins_push_sink_data_niigz(self):
        random_filename = self.random_unique_string()
        output_file = os.path.join(self.destination_dir, random_filename) + '.nii.gz'
        output_url = self.vfs_plugin.path_to_url(output_file)
        self.vfs_plugin.push_sink_data(self.niigz_absfilename, output_url)
        @py_assert1 = os.path
        @py_assert3 = @py_assert1.isfile
        @py_assert6 = @py_assert3(output_file)
        if not @py_assert6:
            @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.isfile\n}(%(py5)s)\n}') % {'py7': @pytest_ar._saferepr(@py_assert6), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(output_file) if 'output_file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output_file) else 'output_file'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert6 = None
        if os.path.isfile(output_file):
            os.remove(output_file)

    def test_ioplugins_push_sink_data_mhd(self):
        absfilename_mhd = os.path.join(fastr.config.mounts['example_data'], 'images', 'mrwhite.mhd')
        absfilename_raw = os.path.join(fastr.config.mounts['example_data'], 'images', 'mrwhite.raw')
        filename_mhd = os.path.basename(absfilename_mhd)
        filename_raw = os.path.basename(absfilename_raw)
        push_target = os.path.join(self.destination_dir, 'sink')
        os.mkdir(push_target)
        destination_path_mhd = os.path.join(push_target, filename_mhd)
        destination_path_raw = os.path.join(push_target, filename_raw)
        destination_url_mhd = self.vfs_plugin.path_to_url(destination_path_mhd)
        if os.path.exists(destination_path_mhd):
            os.remove(destination_path_mhd)
        if os.path.exists(destination_path_raw):
            os.remove(destination_path_raw)
        self.vfs_plugin.push_sink_data(absfilename_mhd, destination_url_mhd)
        @py_assert1 = os.path
        @py_assert3 = @py_assert1.isfile
        @py_assert6 = @py_assert3(destination_path_mhd)
        if not @py_assert6:
            @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.isfile\n}(%(py5)s)\n}') % {'py7': @pytest_ar._saferepr(@py_assert6), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(destination_path_mhd) if 'destination_path_mhd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(destination_path_mhd) else 'destination_path_mhd'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert6 = None
        @py_assert1 = os.path
        @py_assert3 = @py_assert1.isfile
        @py_assert6 = @py_assert3(destination_path_raw)
        if not @py_assert6:
            @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.isfile\n}(%(py5)s)\n}') % {'py7': @pytest_ar._saferepr(@py_assert6), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(destination_path_raw) if 'destination_path_raw' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(destination_path_raw) else 'destination_path_raw'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert6 = None