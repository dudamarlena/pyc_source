# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/namlook/Documents/projets/pypit/tests/test_pypit.py
# Compiled at: 2010-07-16 10:04:00
import unittest
from pypit import *
import os, yaml

class PypitTestCase(unittest.TestCase):

    def setUp(self):
        open('tests/test_file.txt', 'w').write('1\n5\n3\n4\n6\n8\n9\n2\n7\n')

    def tearDown(self):
        if 'pypit_test_buf' in os.listdir('/tmp'):
            os.remove('/tmp/pypit_test_buf')

    def test_pipe_via_stdin(self):
        config = '\n- \n    cmd: cat {{input}}\n\n- \n    cmd: sort \n    use_stdin: true\n'
        res = Pypit(config=yaml.load(config)).run(file_name='test_file.txt', cwd='tests')
        assert res == '1\n2\n3\n4\n5\n6\n7\n8\n9\n', res

    def test_pipe_via_file(self):
        config = '\n- \n    cmd: cat {{input}} > {{output}}\n    output_ext:  bla\n- \n    cmd: sort -r {{input}}\n'
        res = Pypit(config=yaml.load(config)).run(file_name='test_file.txt', cwd='tests')
        assert res == '9\n8\n7\n6\n5\n4\n3\n2\n1\n', res

    def test_pipe_shell(self):
        config = '\n- \n    cmd: echo "12345"\n\n- \n    cmd: wc -c\n    use_stdin: true\n'
        result = Pypit(config=yaml.load(config)).run()
        assert result == '6\n', '+' + result + '+'

    def test_pure_shell(self):
        config = '\n- \n    cmd: echo $PWD\n\n'
        result = Pypit(config=yaml.load(config)).run()
        assert result.strip() == os.environ['PWD'], result

    def test_3_progs(self):
        config = '\n- \n    cmd: cat {{input}} > {{output}}\n    output_ext: buf\n\n- \n    cmd: sort -r {{input}}\n-\n    cmd: wc -l\n    use_stdin: true\n'
        result = Pypit(config=yaml.load(config)).run(file_name='test_file.txt', cwd='/home/namlook/Documents/projets/pypit/tests')
        assert result == '9\n', '+' + result + '+'

    def test_dynamic_input(self):
        config = '\n-\n    cmd: sort -r\n    use_stdin: true\n-\n    cmd: wc -l\n    use_stdin: true\n'
        result = Pypit(config=yaml.load(config)).run(file_name='test_file.txt', cwd='tests')
        assert result == '9\n', '+' + result + '+'

    def test_dynamic_input2(self):
        config = '\n-\n    cmd: /usr/bin/sort -r\n    use_stdin: true\n-\n    cmd: /usr/bin/wc -l\n    use_stdin: true\n'
        result = Pypit(config=yaml.load(config)).run(file_name='test_file.txt', cwd='tests')
        assert result == '9\n', '+' + result + '+'