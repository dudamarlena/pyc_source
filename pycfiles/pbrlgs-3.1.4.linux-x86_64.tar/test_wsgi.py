# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pbr/tests/test_wsgi.py
# Compiled at: 2017-12-04 07:19:32
import os, re, subprocess, sys
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

from pbr.tests import base

class TestWsgiScripts(base.BaseTestCase):
    cmd_names = ('pbr_test_wsgi', 'pbr_test_wsgi_with_class')

    def _get_path(self):
        if os.path.isdir('%s/lib64' % self.temp_dir):
            path = '%s/lib64' % self.temp_dir
        elif os.path.isdir('%s/lib' % self.temp_dir):
            path = '%s/lib' % self.temp_dir
        else:
            if os.path.isdir('%s/site-packages' % self.temp_dir):
                return '.:%s/site-packages' % self.temp_dir
            raise Exception('Could not determine path for test')
        return '.:%s/python%s.%s/site-packages' % (
         path,
         sys.version_info[0],
         sys.version_info[1])

    def test_wsgi_script_install(self):
        """Test that we install a non-pkg-resources wsgi script."""
        if os.name == 'nt':
            self.skipTest('Windows support is passthrough')
        stdout, _, return_code = self.run_setup('install', '--prefix=%s' % self.temp_dir)
        self._check_wsgi_install_content(stdout)

    def test_wsgi_script_run(self):
        """Test that we install a runnable wsgi script.

        This test actually attempts to start and interact with the
        wsgi script in question to demonstrate that it's a working
        wsgi script using simple server.

        """
        if os.name == 'nt':
            self.skipTest('Windows support is passthrough')
        stdout, _, return_code = self.run_setup('install', '--prefix=%s' % self.temp_dir)
        self._check_wsgi_install_content(stdout)
        for cmd_name in self.cmd_names:
            self._test_wsgi(cmd_name, 'Hello World')

    def _test_wsgi(self, cmd_name, output, extra_args=None):
        cmd = os.path.join(self.temp_dir, 'bin', cmd_name)
        print 'Running %s -p 0' % cmd
        popen_cmd = [cmd, '-p', '0']
        if extra_args:
            popen_cmd.extend(extra_args)
        env = {'PYTHONPATH': self._get_path()}
        p = subprocess.Popen(popen_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=self.temp_dir, env=env)
        self.addCleanup(p.kill)
        stdoutdata = p.stdout.readline()
        stdoutdata = p.stdout.readline()
        self.assertIn('STARTING test server pbr_testpackage.wsgi', stdoutdata)
        stdoutdata = p.stdout.readline()
        print stdoutdata
        m = re.search('(http://[^:]+:\\d+)/', stdoutdata)
        self.assertIsNotNone(m, 'Regex failed to match on %s' % stdoutdata)
        stdoutdata = p.stdout.readline()
        self.assertIn('DANGER! For testing only, do not use in production', stdoutdata)
        stdoutdata = p.stdout.readline()
        f = urlopen(m.group(1).decode('utf-8'))
        self.assertEqual(output, f.read())
        urlopen(m.group(1).decode('utf-8'))
        stdoutdata = p.stderr.readline()
        status = '"GET / HTTP/1.1" 200 %d' % len(output)
        self.assertIn(status.encode('utf-8'), stdoutdata)

    def _check_wsgi_install_content(self, install_stdout):
        for cmd_name in self.cmd_names:
            install_txt = 'Installing %s script to %s' % (cmd_name,
             self.temp_dir)
            self.assertIn(install_txt, install_stdout)
            cmd_filename = os.path.join(self.temp_dir, 'bin', cmd_name)
            script_txt = open(cmd_filename, 'r').read()
            self.assertNotIn('pkg_resources', script_txt)
            main_block = 'if __name__ == "__main__":\n    import argparse\n    import socket\n    import sys\n    import wsgiref.simple_server as wss'
            if cmd_name == 'pbr_test_wsgi':
                app_name = 'main'
            else:
                app_name = 'WSGI.app'
            starting_block = 'STARTING test server pbr_testpackage.wsgi.%s' % app_name
            else_block = 'else:\n    application = None'
            self.assertIn(main_block, script_txt)
            self.assertIn(starting_block, script_txt)
            self.assertIn(else_block, script_txt)

    def test_with_argument(self):
        if os.name == 'nt':
            self.skipTest('Windows support is passthrough')
        stdout, _, return_code = self.run_setup('install', '--prefix=%s' % self.temp_dir)
        self._test_wsgi('pbr_test_wsgi', 'Foo Bar', ['--', '-c', 'Foo Bar'])