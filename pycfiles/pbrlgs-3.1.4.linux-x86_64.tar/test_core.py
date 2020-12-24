# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pbr/tests/test_core.py
# Compiled at: 2017-12-04 07:19:32
import glob, os, tarfile, fixtures
from pbr.tests import base

class TestCore(base.BaseTestCase):
    cmd_names = ('pbr_test_cmd', 'pbr_test_cmd_with_class')

    def check_script_install(self, install_stdout):
        for cmd_name in self.cmd_names:
            install_txt = 'Installing %s script to %s' % (cmd_name,
             self.temp_dir)
            self.assertIn(install_txt, install_stdout)
            cmd_filename = os.path.join(self.temp_dir, cmd_name)
            script_txt = open(cmd_filename, 'r').read()
            self.assertNotIn('pkg_resources', script_txt)
            stdout, _, return_code = self._run_cmd(cmd_filename)
            self.assertIn('PBR', stdout)

    def test_setup_py_keywords(self):
        """setup.py --keywords.

        Test that the `./setup.py --keywords` command returns the correct
        value without balking.
        """
        self.run_setup('egg_info')
        stdout, _, _ = self.run_setup('--keywords')
        assert stdout == 'packaging,distutils,setuptools'

    def test_setup_py_build_sphinx(self):
        stdout, _, return_code = self.run_setup('build_sphinx')
        self.assertEqual(0, return_code)

    def test_sdist_extra_files(self):
        """Test that the extra files are correctly added."""
        stdout, _, return_code = self.run_setup('sdist', '--formats=gztar')
        try:
            tf_path = glob.glob(os.path.join('dist', '*.tar.gz'))[0]
        except IndexError:
            assert False, 'source dist not found'

        tf = tarfile.open(tf_path)
        names = [ ('/').join(p.split('/')[1:]) for p in tf.getnames() ]
        self.assertIn('extra-file.txt', names)

    def test_console_script_install(self):
        """Test that we install a non-pkg-resources console script."""
        if os.name == 'nt':
            self.skipTest('Windows support is passthrough')
        stdout, _, return_code = self.run_setup('install_scripts', '--install-dir=%s' % self.temp_dir)
        self.useFixture(fixtures.EnvironmentVariable('PYTHONPATH', '.'))
        self.check_script_install(stdout)

    def test_console_script_develop(self):
        """Test that we develop a non-pkg-resources console script."""
        if os.name == 'nt':
            self.skipTest('Windows support is passthrough')
        self.useFixture(fixtures.EnvironmentVariable('PYTHONPATH', '.:%s' % self.temp_dir))
        stdout, _, return_code = self.run_setup('develop', '--install-dir=%s' % self.temp_dir)
        self.check_script_install(stdout)


class TestGitSDist(base.BaseTestCase):

    def setUp(self):
        super(TestGitSDist, self).setUp()
        stdout, _, return_code = self._run_cmd('git', ('init', ))
        if return_code:
            self.skipTest('git not installed')
        stdout, _, return_code = self._run_cmd('git', ('add', '.'))
        stdout, _, return_code = self._run_cmd('git', ('commit', '-m', 'Turn this into a git repo'))
        stdout, _, return_code = self.run_setup('sdist', '--formats=gztar')

    def test_sdist_git_extra_files(self):
        """Test that extra files found in git are correctly added."""
        tf_path = glob.glob(os.path.join('dist', '*.tar.gz'))[0]
        tf = tarfile.open(tf_path)
        names = [ ('/').join(p.split('/')[1:]) for p in tf.getnames() ]
        self.assertIn('git-extra-file.txt', names)