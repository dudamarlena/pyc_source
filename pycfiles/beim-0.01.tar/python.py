# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/linjiao/dv/beim/beim/paths/Python.py
# Compiled at: 2013-12-08 21:45:16
"""
handle paths for python itself
"""
name = 'python'
description = 'python itself'
from distutils import sysconfig
import sys, os
from .PathsFinder import PathsFinder

class PythonPaths(PathsFinder):
    mechanism = 'extract python includes and libs using distutils module sysconfig'

    def extract(self):
        """
        extract my paths from sysconfig, which is a module in distutils
        """
        something = self._hintsToFindPaths
        derivedFrom = self._derivedFrom
        if something is None:
            something = sysconfig
        include_dirs = []
        py_include = something.get_python_inc()
        plat_py_include = something.get_python_inc(plat_specific=1)
        include_dirs.append(py_include)
        if plat_py_include != py_include:
            include_dirs.append(plat_py_include)
        library_dirs = [something.get_config_var('LIBDEST')]
        runtimelib_dirs = []
        if os.name == 'nt':
            library_dirs.append(os.path.join(sys.exec_prefix, 'libs'))
            include_dirs.append(os.path.join(sys.exec_prefix, 'PC'))
            library_dirs.append(os.path.join(sys.exec_prefix, 'PCBuild'))
        if os.name == 'os2':
            library_dirs.append(os.path.join(sys.exec_prefix, 'Config'))
        if sys.platform[:6] == 'cygwin' or sys.platform[:6] == 'atheos':
            if str.find(sys.executable, sys.exec_prefix) != -1:
                library_dirs.append(os.path.join(sys.prefix, 'lib', 'python' + get_python_version(), 'config'))
            else:
                library_dirs.append('.')
        root = None
        modules = None
        if os.name == 'nt':
            from .NTPythonRoot import pythonInstallationPath as root
            modules = [
             os.path.join(root, 'Lib', 'site-packages')]
        config_dir = something.get_config_var('LIBPL')
        from .Paths import Paths
        ret = Paths(self.name, root=root, includes=include_dirs, clibs=library_dirs, modules=modules, description=self.description, origin=self.mechanism)
        ret.config_dir = config_dir
        return ret


def find():
    toolset = [
     PythonPaths(name, description, hints=None)]
    from .search import search
    return search(toolset)