# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/formish/tests/unittests/test_renderer.py
# Compiled at: 2010-03-01 05:16:45
import os, shutil, tempfile, unittest
from formish.renderer import Renderer, _default_renderer

class TestRenderer(unittest.TestCase):

    def test_default_renderer(self):
        self.assertTrue('/form' in _default_renderer('formish/form/footer.html', {}))

    def test_custom_renderer(self):
        template = 'formish/form/footer.html'
        tmpdir = tempfile.mkdtemp()
        tmptemplate = os.path.join(tmpdir, template)
        os.makedirs(os.path.dirname(tmptemplate))
        open(tmptemplate, 'w').write('custom')
        renderer = Renderer([tmpdir])
        self.assertTrue(renderer('formish/form/footer.html', {}) == 'custom')
        shutil.rmtree(tmpdir)


if __name__ == '__main__':
    unittest.main()