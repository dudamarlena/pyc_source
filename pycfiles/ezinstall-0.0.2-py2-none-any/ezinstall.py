# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/ezinstall-project/ezinstall/ezinstall.py
# Compiled at: 2017-08-29 19:59:53
"""
``ezinstall (Easy install)`` is a package allows you to instantly install
package to your python environment **without having** ``setup.py`` file.
It simply copy the source code to ``site-packages`` directory.
**It also works for virtualenv**. The behavior is exactly the same as
``pip install setup.py --ignore-installed``.

It doesn't install any dependencies from ``requirement.txt``.

-------------------------------------------------------------------------------

Copyright (c) 2014-2017 Sanhe Hu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from __future__ import print_function, unicode_literals
import os
from os.path import isabs, join, abspath, dirname, basename, splitext, exists
import shutil, hashlib, sys, platform
py_ver_major = sys.version_info.major
py_ver_minor = sys.version_info.minor
py_ver_micro = sys.version_info.micro
system = None
is_posix = None
system_name = platform.system()
if system_name == b'Windows':
    site_packages_path = join(dirname(sys.executable), b'Lib', b'site-packages')
    is_posix = False
elif system_name in ('Darwin', 'Linux'):
    site_packages_path = join(dirname(dirname(sys.executable)), b'lib', b'python%s.%s' % (py_ver_major, py_ver_minor), b'site-packages')
    is_posix = True
else:
    raise Exception(b'Unknown Operation System!')

class Path(object):
    """Represent a path.
    """

    def __init__(self, path, *parts):
        path = str(path)
        parts = [ str(part) for part in parts ]
        self.abspath = join(path, *parts)

    def __repr__(self):
        return self.abspath

    def is_absolute(self):
        """
        Test if it's an absolute path.
        """
        return isabs(self.abspath)

    def absolute(self):
        """
        Return absolute version of this path.
        """
        if self.is_absolute():
            return self
        else:
            return self.__class__(abspath(self.abspath))

    def exists(self):
        return exists(self.abspath)

    @property
    def basename(self):
        """
        ``/usr/bin/test.txt`` -> ``test.txt``
        """
        return basename(self.abspath)

    @property
    def ext(self):
        """
        ``/usr/bin/test.txt`` -> ``.txt``
        """
        return splitext(self.basename)[1]

    @property
    def fname(self):
        """
        ``/usr/bin/test.txt`` -> ``test``
        """
        return splitext(self.basename)[0]

    @property
    def dirname(self):
        """
        ``/usr/bin/test.txt`` -> ``bin``
        """
        return basename(self.dirpath)

    @property
    def dirpath(self):
        """
        ``/usr/bin/test.txt`` -> ``/usr/bin``
        """
        return dirname(self.abspath)

    @property
    def parent(self):
        """
        Parent directory.
        """
        return self.__class__(self.dirpath)

    @property
    def parts(self):
        r"""
        - ``/usr/bin/test.txt`` -> ["/", "usr", "bin", "test.txt]
        - ``C:\User\admin\test.txt`` -> ["C:\", "User", "admin", "test.txt"]
        """
        if is_posix:
            l = [ part for part in self.abspath.split(b'/') if part ]
            if self.absolute():
                l = [
                 b'/'] + l
        else:
            l = self.abspath.split(b'\\')
            if l[0].endswith(b':'):
                l[0] = l[0] + b'\\'
        return l

    def path_chain(self):
        """
        """
        path_list = [
         self]
        p = self
        for i in range(len(self.parts) - 1):
            p = p.parent
            path_list.append(p)

        return path_list

    def __eq__(self, other):
        return self.abspath == other.abspath


def remove_pyc_file(package_dirpath):
    """
    Remove all ``__pycache__`` folder and ``.pyc`` file from a directory.
    """
    pyc_folder_list = list()
    pyc_file_list = list()
    for root, _, basename_list in os.walk(package_dirpath):
        if os.path.basename(root) == b'__pycache__':
            pyc_folder_list.append(root)
        for basename in basename_list:
            if basename.endswith(b'.pyc'):
                abspath = os.path.join(root, basename)
                pyc_file_list.append(abspath)

    for folder in pyc_folder_list:
        try:
            shutil.rmtree(folder)
        except:
            pass

    for abspath in pyc_file_list:
        try:
            os.remove(abspath)
        except:
            pass


def md5_of_file(abspath):
    """
    Md5 value of a file.
    """
    chunk_size = 1048576
    m = hashlib.md5()
    with open(abspath, b'rb') as (f):
        while True:
            data = f.read(chunk_size)
            if not data:
                break
            m.update(data)

    return m.hexdigest()


def check_need_install(src, dst):
    """
    Check if installed package are exactly the same to this one.
    By checking md5 value of all files.
    """
    for root, _, basename_list in os.walk(src):
        if basename(root) != b'__pycache__':
            for file_basename in basename_list:
                if not file_basename.endswith(b'.pyc'):
                    before = join(root, file_basename)
                    after = join(root.replace(src, dst), file_basename)
                    if exists(after):
                        if md5_of_file(before) != md5_of_file(after):
                            return True
                    else:
                        return True

    return False


class Printer(object):
    """
    Simple printer to support ``enable_verbose`` argument.
    """
    verbose = True

    @classmethod
    def log(cls, message):
        if cls.verbose:
            print(message)


def install(package_dir, verbose=True):
    """Easy install main script.

    Create a ``zzz_ezinstall.py`` file, and put in your package folder (Next to
    the ``__init__.py`` file), and put following content::

        #!/usr/bin/env python
        # -*- coding: utf-8 -*-

        if __name__ == "__main__":
            import os
            from ezinstall import install

            install(os.path.dirname(__file__))

    :param package_dir: package source code directory.
    :param verbose: trigger to open log info.
    """
    if verbose:
        Printer.verbose = True
    else:
        Printer.verbose = False
    p = Path(package_dir).absolute()
    package_name = p.basename
    src = p.abspath
    dst = join(site_packages_path, package_name)
    Printer.log(b"Compare to '%s' ..." % dst)
    need_install_flag = check_need_install(src, dst)
    if not need_install_flag:
        Printer.log(b'    package is up-to-date, no need to install.')
        return
    Printer.log(b'    Difference been found, start installing ...')
    Printer.log(b'Remove *.pyc file ...')
    try:
        remove_pyc_file(src)
        Printer.log(b'    Success! all *.pyc file has been removed.')
    except Exception as e:
        Printer.log(b'    Faield! %r' % e)

    Printer.log(b"Remove installed '%s' from '%s' ..." % (package_name, dst))
    if exists(dst):
        try:
            shutil.rmtree(dst)
            Printer.log(b'    Success!')
        except Exception as e:
            Printer.log(b'    Faield! %r' % e)

    Printer.log(b"Install '%s' to '%s' ..." % (package_name, dst))
    try:
        shutil.copytree(src, dst)
        Printer.log(b'    Complete!')
    except Exception as e:
        Printer.log(b'    Failed! %r' % e)


if __name__ == b'__main__':
    import os
    install(os.path.dirname(__file__))