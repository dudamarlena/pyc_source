# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/prometeo/projects/ardy/ardy/core/build/build.py
# Compiled at: 2018-04-15 10:04:49
from __future__ import unicode_literals, print_function
import datetime, os, zipfile
from builtins import str
from shutil import copy2
from tempfile import mkdtemp
import pip
from ardy.config import ConfigMixin
from ardy.core.exceptions import ArdyNoFileError
from ardy.utils.log import logger

class Build(ConfigMixin):
    src_path = b''

    def __init__(self, *args, **kwargs):
        self.config = kwargs.get(b'config', False)
        if not self.config:
            super(Build, self).__init__(*args, **kwargs)

    def mkdir(self, path):
        path = os.path.join(self.config.get_projectdir(), path)
        if not os.path.exists(path):
            os.makedirs(path)
            return True
        return False

    @staticmethod
    def read(path, loader=None):
        with open(path, b'rb') as (fh):
            if not loader:
                return fh.read()
            else:
                return loader(fh.read())

    @staticmethod
    def timestamp(fmt=b'%Y-%m-%d-%H%M%S'):
        now = datetime.datetime.utcnow()
        return now.strftime(fmt)

    def create_artefact(self, src, dest, filename):
        if not os.path.isabs(dest):
            dest = os.path.join(self.config.get_projectdir(), dest)
        dest = os.path.abspath(dest)
        if not os.path.isabs(src):
            src = os.path.join(self.config.get_projectdir(), src)
        relroot = os.path.abspath(src)
        output = os.path.join(dest, filename)
        excluded_folders = [b'dist']
        excluded_files = []
        if not os.path.isdir(src) and not os.path.isfile(src):
            raise ArdyNoFileError((b'{} not exists').format(src))
        with zipfile.ZipFile(output, b'a', compression=zipfile.ZIP_DEFLATED) as (zf):
            for root, subdirs, files in os.walk(src):
                excluded_dirs = []
                for subdir in subdirs:
                    for excluded in excluded_folders:
                        if subdir.startswith(excluded):
                            excluded_dirs.append(subdir)

                for excluded in excluded_dirs:
                    subdirs.remove(excluded)

                try:
                    dir_path = os.path.relpath(root, relroot)
                    dir_path = os.path.normpath(os.path.splitdrive(dir_path)[1])
                    while dir_path[0] in (os.sep, os.altsep):
                        dir_path = dir_path[1:]

                    dir_path += b'/'
                    zf.getinfo(dir_path)
                except KeyError:
                    zf.write(root, dir_path)

                for filename in files:
                    if filename not in excluded_files:
                        filepath = os.path.join(root, filename)
                        if os.path.isfile(filepath):
                            arcname = os.path.join(os.path.relpath(root, relroot), filename)
                            try:
                                zf.getinfo(arcname)
                            except KeyError:
                                zf.write(filepath, arcname)

        return output

    def copytree(self, src, dst, symlinks=False, ignore=None):
        if not os.path.exists(dst):
            os.makedirs(dst)
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                self.copytree(s, d, symlinks, ignore)
            elif not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                copy2(s, d)

    def set_src_path(self, src_folder):
        self.src_path = os.path.abspath(os.path.join(self.config.get_projectdir(), src_folder))

    def get_src_path(self):
        return self.src_path

    def run(self, src_folder, requirements=b'requirements.txt', local_package=None):
        """Builds the file bundle.
        :param str src:
           The path to your Lambda ready project (folder must contain a valid
            config.yaml and handler module (e.g.: service.py).
        :param str local_package:
            The path to a local package with should be included in the deploy as
            well (and/or is not available on PyPi)
        """
        self.set_src_path(src_folder)
        if not os.path.isdir(self.get_src_path()):
            raise ArdyNoFileError((b'File {} not exist').format(self.get_src_path()))
        dist_directory = b'dist'
        path_to_dist = os.path.join(self.get_src_path(), dist_directory)
        self.mkdir(path_to_dist)
        output_filename = (b'{0}.zip').format(self.timestamp())
        path_to_temp = mkdtemp(prefix=b'aws-lambda')
        self.pip_install_to_target(path_to_temp, requirements=requirements, local_package=local_package)
        if os.path.isabs(src_folder):
            src_folder = src_folder.split(os.sep)[(-1)]
        self.copytree(self.get_src_path(), os.path.join(path_to_temp, src_folder))
        path_to_zip_file = self.create_artefact(path_to_temp, path_to_dist, output_filename)
        return path_to_zip_file

    def _install_packages(self, path, packages):
        """Install all packages listed to the target directory.
        Ignores any package that includes Python itself and python-lambda as well
        since its only needed for deploying and not running the code
        :param str path:
            Path to copy installed pip packages to.
        :param list packages:
            A list of packages to be installed via pip.
        """

        def _filter_blacklist(package):
            blacklist = [
             b'-i', b'#', b'Python==', b'ardy==']
            return all(package.startswith(entry.encode()) is False for entry in blacklist)

        filtered_packages = filter(_filter_blacklist, packages)
        for package in filtered_packages:
            package = str(package, b'utf-8')
            if package.startswith(b'-e '):
                package = package.replace(b'-e ', b'')
            logger.info((b'Installing {package}').format(package=package))
            pip.main([b'install', package, b'-t', path, b'--ignore-installed', b'-q'])

    def pip_install_to_target(self, path, requirements=b'', local_package=None):
        """For a given active virtualenv, gather all installed pip packages then
        copy (re-install) them to the path provided.
        :param str path:
            Path to copy installed pip packages to.
        :param str requirements:
            If set, only the packages in the requirements.txt file are installed.
            The requirements.txt file needs to be in the same directory as the
            project which shall be deployed.
            Defaults to false and installs all pacakges found via pip freeze if
            not set.
        :param str local_package:
            The path to a local package with should be included in the deploy as
            well (and/or is not available on PyPi)
        """
        packages = []
        if not requirements:
            logger.debug(b'Gathering pip packages')
        else:
            requirements_path = os.path.join(self.get_src_path(), requirements)
            logger.debug((b'Gathering packages from requirements: {}').format(requirements_path))
            if os.path.isfile(requirements_path):
                data = self.read(requirements_path)
                packages.extend(data.splitlines())
            else:
                logger.debug((b'No requirements file in {}').format(requirements_path))
        if local_package is not None:
            if not isinstance(local_package, (list, tuple)):
                local_package = [
                 local_package]
            for l_package in local_package:
                packages.append(l_package)

        self._install_packages(path, packages)
        return