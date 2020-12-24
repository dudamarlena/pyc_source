# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mrdon/dev/flask-async/venv/lib/python3.3/site-packages/flask/testsuite/ext.py
# Compiled at: 2014-01-20 12:41:11
# Size of source mod 2**32: 5156 bytes
"""
    flask.testsuite.ext
    ~~~~~~~~~~~~~~~~~~~

    Tests the extension import thing.

    :copyright: (c) 2014 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
import sys, unittest
try:
    from imp import reload as reload_module
except ImportError:
    reload_module = reload

from flask.testsuite import FlaskTestCase
from flask._compat import PY2

class ExtImportHookTestCase(FlaskTestCase):

    def setup(self):
        for entry, value in list(sys.modules.items()):
            if (entry.startswith('flask.ext.') or entry.startswith('flask_') or entry.startswith('flaskext.') or entry == 'flaskext') and value is not None:
                sys.modules.pop(entry, None)
                continue

        from flask import ext
        reload_module(ext)
        import_hooks = 0
        for item in sys.meta_path:
            cls = type(item)
            if cls.__module__ == 'flask.exthook' and cls.__name__ == 'ExtensionImporter':
                import_hooks += 1
                continue

        self.assert_equal(import_hooks, 1)
        return

    def teardown(self):
        from flask import ext
        for key in ext.__dict__:
            self.assert_not_in('.', key)

    def test_flaskext_new_simple_import_normal(self):
        from flask.ext.newext_simple import ext_id
        self.assert_equal(ext_id, 'newext_simple')

    def test_flaskext_new_simple_import_module(self):
        from flask.ext import newext_simple
        self.assert_equal(newext_simple.ext_id, 'newext_simple')
        self.assert_equal(newext_simple.__name__, 'flask_newext_simple')

    def test_flaskext_new_package_import_normal(self):
        from flask.ext.newext_package import ext_id
        self.assert_equal(ext_id, 'newext_package')

    def test_flaskext_new_package_import_module(self):
        from flask.ext import newext_package
        self.assert_equal(newext_package.ext_id, 'newext_package')
        self.assert_equal(newext_package.__name__, 'flask_newext_package')

    def test_flaskext_new_package_import_submodule_function(self):
        from flask.ext.newext_package.submodule import test_function
        self.assert_equal(test_function(), 42)

    def test_flaskext_new_package_import_submodule(self):
        from flask.ext.newext_package import submodule
        self.assert_equal(submodule.__name__, 'flask_newext_package.submodule')
        self.assert_equal(submodule.test_function(), 42)

    def test_flaskext_old_simple_import_normal(self):
        from flask.ext.oldext_simple import ext_id
        self.assert_equal(ext_id, 'oldext_simple')

    def test_flaskext_old_simple_import_module(self):
        from flask.ext import oldext_simple
        self.assert_equal(oldext_simple.ext_id, 'oldext_simple')
        self.assert_equal(oldext_simple.__name__, 'flaskext.oldext_simple')

    def test_flaskext_old_package_import_normal(self):
        from flask.ext.oldext_package import ext_id
        self.assert_equal(ext_id, 'oldext_package')

    def test_flaskext_old_package_import_module(self):
        from flask.ext import oldext_package
        self.assert_equal(oldext_package.ext_id, 'oldext_package')
        self.assert_equal(oldext_package.__name__, 'flaskext.oldext_package')

    def test_flaskext_old_package_import_submodule(self):
        from flask.ext.oldext_package import submodule
        self.assert_equal(submodule.__name__, 'flaskext.oldext_package.submodule')
        self.assert_equal(submodule.test_function(), 42)

    def test_flaskext_old_package_import_submodule_function(self):
        from flask.ext.oldext_package.submodule import test_function
        self.assert_equal(test_function(), 42)

    def test_flaskext_broken_package_no_module_caching(self):
        for x in range(2):
            with self.assert_raises(ImportError):
                import flask.ext.broken

    def test_no_error_swallowing(self):
        try:
            import flask.ext.broken
        except ImportError:
            exc_type, exc_value, tb = sys.exc_info()
            self.assert_true(exc_type is ImportError)
            if PY2:
                message = 'No module named missing_module'
            else:
                message = "No module named 'missing_module'"
            self.assert_equal(str(exc_value), message)
            self.assert_true(tb.tb_frame.f_globals is globals())
            next = tb.tb_next.tb_next
            if not PY2:
                next = next.tb_next
            self.assert_in('flask_broken/__init__.py', next.tb_frame.f_code.co_filename)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ExtImportHookTestCase))
    return suite