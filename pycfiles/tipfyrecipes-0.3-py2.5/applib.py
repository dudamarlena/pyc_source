# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tipfyrecipes/gae/applib.py
# Compiled at: 2011-08-05 19:07:14
"""
Downloads libraries from PyPi and installs in the app directory. This recipe
extends `zc.recipe.egg.Scripts <http://pypi.python.org/pypi/zc.recipe.egg>`_,
so all the options from that recipe are also valid.

Options
~~~~~~~

:eggs: Package names to be installed.
:lib-directory: Destination directory for the libraries. Default is
        `distlib`.
:use-zipimport: If `true`, a zip file with the libraries is created
        instead of a directory. The zip filename will be the value of
        `lib-directory` plus `.zip`.
:ignore-globs: A list of glob patterns to not be copied from the library.
:ignore-packages: A list of top-level package names or modules to be ignored.
        This is useful to ignore dependencies that won't be used. Some packages may
        install distribute, setuptools or pkg_resources but these are not very
        useful on App Engine, so you can set them to be ignored, for example.
:delete-safe: If `true`, always move `lib-directory` to a temporary directory
        inside the parts dir as a backup when building, instead of deleting it.
        This is to avoid accidental deletion if `lib-directory` is badly
        configured. Default to `true`.

Example
~~~~~~~

::

  [app_lib]
  recipe = tipfyrecipes.gae:eggs
  lib-directory = app/distlib
  use-zipimport = false

  # Define the libraries.
  eggs =
          python-dateutil

  # Don't copy files that match these glob patterns.
  ignore-globs =
          *.c
          *.pyc
          *.pyo
          */test
          */tests
          */testsuite
          */django
          */sqlalchemy

  # Don't install these packages or modules.
  ignore-packages =
          distribute
          setuptools
          easy_install
          site
          pkg_resources
"""
import datetime, logging, os, shutil, tempfile, uuid
from z3c.recipe.scripts.scripts import Scripts
from tipfyrecipes import copytree, ignore_patterns, include_patterns, rmfiles, zipdir
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.realpath(__file__))))))
LIB_README = "Warning!\n========\n\nThis directory is removed every time the buildout tool runs, so don't place\nor edit things here because any changes will be lost!\n\nUse a different directory for extra libraries instead of this one."

class InstallAppLib(Scripts):

    def __init__(self, buildout, name, opts):
        self.logger = logging.getLogger(name)
        opts.setdefault('unzip', 'true')
        self.eggs_dir = buildout['buildout']['eggs-directory']
        self.parts_dir = buildout['buildout']['parts-directory']
        self.temp_dir = os.path.join(self.parts_dir, 'temp')
        lib_dir = opts.get('lib-directory', 'distlib')
        self.lib_path = os.path.abspath(lib_dir)
        self.use_zip = opts.get('use-zipimport', 'false') == 'true'
        if self.use_zip:
            self.lib_path += '.zip'
        self.ignore_globs = [ i for i in opts.get('ignore-globs', '').splitlines() if i.strip()
                            ]
        self.ignore_packages = [ i for i in opts.get('ignore-packages', '').splitlines() if i.strip()
                               ]
        self.delete_safe = opts.get('delete-safe', 'true') != 'false'
        opts.setdefault('eggs', '')
        super(InstallAppLib, self).__init__(buildout, name, opts)

    def install(self):
        (reqs, ws) = self.working_set()
        paths = self.get_package_paths(ws)
        self.install_in_app_dir(paths)
        return super(InstallAppLib, self).install()

    update = install

    def install_in_app_dir(self, paths):
        self.delete_libs()
        if self.use_zip:
            tmp_dir = os.path.join(tempfile.gettempdir(), uuid.uuid4().hex)
        else:
            tmp_dir = self.lib_path
        if not os.path.exists(tmp_dir):
            os.mkdir(tmp_dir)
        for (name, src) in paths:
            if name in self.ignore_packages:
                continue
            dst = os.path.join(tmp_dir, name)
            if not os.path.isdir(src):
                src += '.py'
                dst += '.py'
                if not os.path.isfile(src) or os.path.isfile(dst):
                    continue
            self.logger.info('Copying %r...' % src)
            copytree(src, dst, os.path.dirname(src) + os.sep, ignore=ignore_patterns(*self.ignore_globs), logger=self.logger)

        f = open(os.path.join(tmp_dir, 'README.txt'), 'w')
        f.write(LIB_README)
        f.close()
        if self.use_zip:
            zipdir(tmp_dir, self.lib_path)
            if os.path.isdir(tmp_dir):
                shutil.rmtree(tmp_dir)

    def get_package_paths(self, ws):
        """Returns the list of package paths to be copied."""
        pkgs = []
        for path in ws.entries:
            lib_paths = self.get_lib_paths(path)
            if not lib_paths:
                self.logger.info('Library not installed: missing egg info for %r.' % path)
                continue
            for lib_path in lib_paths:
                pkgs.append((lib_path, os.path.join(path, lib_path)))

        return pkgs

    def get_top_level_libs(self, egg_path):
        top_path = os.path.join(egg_path, 'top_level.txt')
        if not os.path.isfile(top_path):
            return
        f = open(top_path, 'r')
        libs = f.read().strip()
        f.close()
        return [ l.strip() for l in libs.splitlines() if l.strip() ]

    def get_lib_paths(self, path):
        """Returns the 'EGG-INFO' or '.egg-info' directory."""
        egg_path = os.path.join(path, 'EGG-INFO')
        if os.path.isdir(egg_path):
            return self.get_top_level_libs(egg_path)
        if os.path.isfile(path):
            return
        elif os.path.isdir(path):
            files = os.listdir(path)
            for filename in files:
                if filename.endswith('.egg-info'):
                    egg_path = os.path.join(path, filename)
                    return self.get_top_level_libs(egg_path)

        return

    def delete_libs(self):
        """If the `delete-safe` option is set to true, move the old libraries
                directory to a temporary directory inside the parts dir instead of
                deleting it.
                """
        if not os.path.exists(self.lib_path):
            return
        if self.delete_safe is True:
            if not os.path.exists(self.temp_dir):
                os.makedirs(self.temp_dir)
            date = datetime.datetime.now().strftime('_%Y_%m_%d_%H_%M_%S')
            filename = os.path.basename(self.lib_path.rstrip(os.sep))
            if self.use_zip:
                filename = filename[:-4] + date + '.zip'
            else:
                filename += date
            dst = os.path.join(self.temp_dir, filename)
            shutil.move(self.lib_path, dst)
            self.logger.info('Saved libraries backup in %r.' % dst)
        elif self.use_zip:
            os.remove(self.lib_path)
            self.logger.info('Removed lib-zip %r.' % self.lib_path)
        else:
            shutil.rmtree(self.lib_path)
            self.logger.info('Removed lib-directory %r.' % self.lib_path)