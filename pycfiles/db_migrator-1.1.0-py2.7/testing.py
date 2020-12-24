# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dbmigrator/tests/testing.py
# Compiled at: 2018-01-03 12:06:07
from contextlib import contextmanager
from io import StringIO
import os.path, sys, pip
here = os.path.abspath(os.path.dirname(__file__))
db_connection_string = 'dbname=travis user=travis host=localhost'
test_data_path = os.path.join(here, 'data')
test_packages = ['package-a', 'package-b']
test_config_path = os.path.join(test_data_path, 'config.ini')
test_config2_path = os.path.join(test_data_path, 'config2.ini')
test_migrations_directories = [
 os.path.join(test_data_path, 'package-a', 'package_a', 'migrations'),
 os.path.join(test_data_path, 'package-b', 'package_b', 'm')]

@contextmanager
def captured_output():
    if sys.version_info[0] == 3:
        new_out, new_err = StringIO(), StringIO()
    else:
        from io import BytesIO
        new_out, new_err = BytesIO(), BytesIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield (sys.stdout, sys.stderr)
    finally:
        sys.stdout, sys.stderr = old_out, old_err


def install_test_packages(packages=None):
    if packages is None:
        packages = test_packages
    for package in packages:
        with captured_output() as (out, err):
            pip.main(['install', '-e', os.path.join(test_data_path, package)])
        stderr = err.getvalue()
        sys.stderr.write(stderr)

    return