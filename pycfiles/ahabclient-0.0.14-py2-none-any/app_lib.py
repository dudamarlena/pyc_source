# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/aha/recipe/gae/app_lib.py
# Compiled at: 2011-03-30 10:49:25
__doc__ = "\naha.recipe.gae:app_lib\n------------------------\nDownloads libs from PyPi them into the application lib directory,\n    extending appfy.recipe.gae:app_lib\nThe difference to the appfy.reciep.gae:app_lib is that it adds __init__.py \n so that the directory works as a python package.\nThis module imports some modules from appfy.\n\n\nExample\n~~~~~~~\n\n::\n\n  [app_lib]\n  recipe = aha.recipe.gae:app_lib\n  lib-directory = app/lib\n  app-directory = app/application\n  plugin-directory = app/plugin\n\n  # Define the libraries.\n  eggs =\n      aha\n      aha.application.coreblog3\n      aha.plugin.twitterauth\n\n  # Don't copy files that match these glob patterns.\n  ignore-globs =\n      *.c\n      *.pyc\n      *.pyo\n      */test\n      */tests\n      */testsuite\n      */django\n      */sqlalchemy\n\n  # Don't install these packages or modules.\n  ignore-packages =\n      distribute\n      setuptools\n      easy_install\n      site\n      pkg_resources\n"
import os, shutil, tempfile, uuid, datetime, pkg_resources
from appfy.recipe.gae import app_lib
from appfy.recipe import copytree, ignore_patterns, include_patterns, rmfiles, zipdir
PLUGIN_PREFIX = 'aha.plugin'
APPLICATION_PREFIX = 'aha.application'
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.realpath(__file__))))))

class Recipe(app_lib.Recipe):

    def __init__(self, buildout, name, opts):
        super(Recipe, self).__init__(buildout, name, opts)
        app_dir = opts.get('app-directory', 'application')
        self.app_path = os.path.abspath(app_dir)
        plugin_dir = opts.get('plugin-directory', 'plugin')
        self.plugin_path = os.path.abspath(plugin_dir)

    def install_in_app_dir(self, paths):
        lib_dir = self.lib_path
        app_dir = self.app_path
        plugin_dir = self.plugin_path
        self.delete_path(lib_dir)
        for (d, p) in ((plugin_dir, PLUGIN_PREFIX),
         (
          app_dir, APPLICATION_PREFIX)):
            if [ name for (name, src, pkgname) in paths if pkgname.startswith(p) ]:
                self.delete_path(d)

        for d in [lib_dir, plugin_dir]:
            if not os.path.exists(d):
                os.mkdir(d)

        for (name, src, pkgname) in paths:
            if name in self.ignore_packages:
                continue
            if pkgname.startswith('aha.application'):
                if src.endswith('application'):
                    dst = os.path.join(app_dir)
                else:
                    dst = os.path.split(app_dir)[0]
                    dst = os.path.join(dst, os.path.split(src)[1])
            elif pkgname.startswith('aha.plugin'):
                dst = os.path.join(plugin_dir, name)
            else:
                dst = os.path.join(lib_dir, name)
            if not os.path.isdir(src):
                src += '.py'
                dst += '.py'
                if not os.path.isfile(src) or os.path.isfile(dst):
                    continue
            self.logger.info('Copying %r to %r...' % (src, dst))
            copytree(src, dst, os.path.dirname(src) + os.sep, ignore=ignore_patterns(*self.ignore_globs), logger=self.logger)

        f = open(os.path.join(lib_dir, 'README.txt'), 'w')
        f.write(app_lib.LIB_README)
        f.close()
        for d in [lib_dir, plugin_dir]:
            open(os.path.join(d, '__init__.py'), 'w')

    def get_package_paths(self, ws):
        """Returns the list of package paths to be copied."""
        pkgs = []
        for path in ws.entries:
            lib_paths = self.get_lib_paths(path)
            if not lib_paths:
                self.logger.info('Library not installed: missing egg info for %r.' % path)
                continue
            for lib_path in lib_paths:
                p = os.path.basename(path)
                if os.path.exists(os.path.join(path, p + '.egg-info')):
                    p = p + '.egg-info'
                    dist = pkg_resources.Distribution.from_location(path, p)
                else:
                    dist = pkg_resources.Distribution.from_filename(path)
                pkgs.append((lib_path,
                 os.path.join(path, lib_path),
                 dist.project_name))

        return pkgs

    def delete_path(self, path):
        """If the `delete-safe` option is set to true, move the old stuff
        directory to a temporary directory inside the parts dir instead of
        deleting it.
        """
        if not os.path.exists(path):
            return
        if self.delete_safe is True:
            if not os.path.exists(self.temp_dir):
                os.makedirs(self.temp_dir)
            date = datetime.datetime.now().strftime('_%Y_%m_%d_%H_%M_%S')
            filename = os.path.basename(path.rstrip(os.sep))
            if self.use_zip:
                filename = filename[:-4] + date + '.zip'
            else:
                filename += date
            dst = os.path.join(self.temp_dir, filename)
            shutil.move(path, dst)
            self.logger.info('Saved libraries backup in %r.' % dst)
        elif self.use_zip:
            os.remove(path)
            self.logger.info('Removed lib-zip %r.' % path)
        else:
            shutil.rmtree(path)
            self.logger.info('Removed lib-directory %r.' % path)