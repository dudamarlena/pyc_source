# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/tyu030/work/calmjs.bower/src/calmjs/bower/__init__.py
# Compiled at: 2016-08-30 02:05:10
__doc__ = '\nModule for dealing with bower framework.\n\nProvides some helper functions that deal with bower.json, and also the\nsetuptools integration for certain bower features.\n'
from functools import partial
from calmjs.cli import PackageManagerDriver
from calmjs.command import PackageManagerCommand
from calmjs.dist import write_json_file
from calmjs.runtime import PackageManagerRuntime
BOWER_FIELD = 'bower_json'
BOWER_JSON = bower_json = 'bower.json'
BOWER = 'bower'
write_bower_json = partial(write_json_file, BOWER_FIELD)

class Driver(PackageManagerDriver):

    def __init__(self, **kw):
        kw['pkg_manager_bin'] = BOWER
        kw['pkgdef_filename'] = BOWER_JSON
        kw['description'] = 'bower compatibility helper'
        super(Driver, self).__init__(**kw)


class bower(PackageManagerCommand):
    """
    The bower specific setuptools command.
    """
    cli_driver = Driver.create_for_module_vars(globals())
    runtime = PackageManagerRuntime(cli_driver, package_name='calmjs.bower', description='bower support for the calmjs framework')
    description = cli_driver.description


bower._initialize_user_options()