# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/test/test_notebooks.py
# Compiled at: 2020-03-20 04:44:53
# Size of source mod 2**32: 1397 bytes
import unittest, os, jittor as jt
from jittor import LOG
import json
dirname = os.path.join(jt.flags.jittor_path, 'notebook')
notebook_dir = os.path.join(jt.flags.cache_path, 'notebook')
tests = []
for mdname in os.listdir(dirname):
    if not mdname.endswith('.src.md'):
        continue
    tests.append(mdname[:-3])

try:
    jt.compiler.run_cmd('ipython --help')
    has_ipython = True
except:
    has_ipython = False

def test(name):
    LOG.i(f"Run test {name} from {dirname}")
    ipynb_name = os.path.join(notebook_dir, name + '.ipynb')
    jt.compiler.run_cmd('ipython ' + ipynb_name)


def init():
    jt.compiler.run_cmd('python3 ' + os.path.join(dirname, 'md_to_ipynb.py'))


src = 'class TestNodebooks(unittest.TestCase):\n    @classmethod\n    def setUpClass(self):\n        init()\n'
for name in tests:
    src += f"""\n    @unittest.skipIf(not has_ipython, "No IPython found")\n    def test_{name.replace('.src', '')}(self):\n        test("{name}")\n    """

LOG.vvv('eval src\n' + src)
exec(src)
if __name__ == '__main__':
    unittest.main()