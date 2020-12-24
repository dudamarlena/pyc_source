# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/shuyucms/utils/tests.py
# Compiled at: 2016-05-20 23:26:47
from __future__ import unicode_literals
import os
from _ast import PyCF_ONLY_AST
from shutil import copyfile, copytree
from django.db import connection
from django.template import Context, Template
from django.test import TestCase as BaseTestCase
from future.builtins import open, range, str
from shuyucms.conf import settings
from shuyucms.utils.importing import path_for_import
from shuyucms.utils.models import get_user_model
User = get_user_model()
IGNORE_ERRORS = ("'from local_settings import *' used", "'__version__' imported but unused",
                 "redefinition of function 'nevercache'", "redefinition of function 'compress'",
                 "redefinition of unused 'conf'", 'continuation line', 'closing bracket does not match',
                 "redefinition of unused 'Image", "redefinition of unused 'get_user_model",
                 'shuyucms/utils/timezone', 'live_settings.py')

class TestCase(BaseTestCase):
    """
    This is the base test case providing common features for all tests
    across the different apps in shuyucms.
    """

    def setUp(self):
        """
        Creates an admin user and sets up the debug cursor, so that
        we can track the number of queries used in various places.
        """
        self._username = b'test'
        self._password = b'test'
        self._emailaddress = b'example@example.com'
        args = (self._username, self._emailaddress, self._password)
        self._user = User.objects.create_superuser(*args)
        self._debug_cursor = connection.use_debug_cursor
        connection.use_debug_cursor = True

    def tearDown(self):
        """
        Clean up the admin user created and debug cursor.
        """
        self._user.delete()
        connection.use_debug_cursor = self._debug_cursor

    def queries_used_for_template(self, template, **context):
        """
        Return the number of queries used when rendering a template
        string.
        """
        connection.queries = []
        t = Template(template)
        t.render(Context(context))
        return len(connection.queries)

    def create_recursive_objects(self, model, parent_field, **kwargs):
        """
        Create multiple levels of recursive objects.
        """
        per_level = list(range(3))
        for _ in per_level:
            kwargs[parent_field] = None
            level1 = model.objects.create(**kwargs)
            for _ in per_level:
                kwargs[parent_field] = level1
                level2 = model.objects.create(**kwargs)
                for _ in per_level:
                    kwargs[parent_field] = level2
                    model.objects.create(**kwargs)

        return


def copy_test_to_media(module, name):
    """
    Copies a file from shuyucms's test data path to MEDIA_ROOT.
    Used in tests and demo fixtures.
    """
    shuyucms_path = path_for_import(module)
    test_path = os.path.join(shuyucms_path, b'static', b'test', name)
    to_path = os.path.join(settings.MEDIA_ROOT, name)
    to_dir = os.path.dirname(to_path)
    if not os.path.exists(to_dir):
        os.makedirs(to_dir)
    if os.path.isdir(test_path):
        copy = copytree
    else:
        copy = copyfile
    try:
        copy(test_path, to_path)
    except OSError:
        pass


def _run_checker_for_package(checker, package_name, extra_ignore=None):
    """
    Runs the checker function across every Python module in the
    given package.
    """
    ignore_strings = IGNORE_ERRORS
    if extra_ignore:
        ignore_strings += extra_ignore
    package_path = path_for_import(package_name)
    for root, dirs, files in os.walk(str(package_path)):
        for f in files:
            if f == b'local_settings.py' or not f.endswith(b'.py') or root.split(os.sep)[(-1)] == b'migrations':
                continue
            for warning in checker(os.path.join(root, f)):
                for ignore in ignore_strings:
                    if ignore in warning:
                        break
                else:
                    yield warning.replace(package_path, package_name, 1)


def run_pyflakes_for_package(package_name, extra_ignore=None):
    """
    If pyflakes is installed, run it across the given package name
    returning any warnings found.
    """
    from pyflakes.checker import Checker

    def pyflakes_checker(path):
        with open(path, b'U') as (source_file):
            source = source_file.read()
        try:
            tree = compile(source, path, b'exec', PyCF_ONLY_AST)
        except (SyntaxError, IndentationError) as value:
            info = (
             path, value.lineno, value.args[0])
            yield b'Invalid syntax in %s:%d: %s' % info

        result = Checker(tree, path)
        for warning in result.messages:
            yield str(warning)

    args = (pyflakes_checker, package_name, extra_ignore)
    return _run_checker_for_package(*args)


def run_pep8_for_package(package_name, extra_ignore=None):
    """
    If pep8 is installed, run it across the given package name
    returning any warnings or errors found.
    """
    import pep8

    class Checker(pep8.Checker):
        """
        Subclass pep8's Checker to hook into error reporting.
        """

        def __init__(self, *args, **kwargs):
            super(Checker, self).__init__(*args, **kwargs)
            self.report_error = self._report_error

        def _report_error(self, line_number, offset, text, check):
            """
            Store pairs of line numbers and errors.
            """
            self.errors.append((line_number, text.split(b' ', 1)[1]))

        def check_all(self, *args, **kwargs):
            """
            Assign the errors attribute and return it after running.
            """
            self.errors = []
            super(Checker, self).check_all(*args, **kwargs)
            return self.errors

    def pep8_checker(path):
        for line_number, text in Checker(path).check_all():
            yield b'%s:%s: %s' % (path, line_number, text)

    args = (pep8_checker, package_name, extra_ignore)
    return _run_checker_for_package(*args)