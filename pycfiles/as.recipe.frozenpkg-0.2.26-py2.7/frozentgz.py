# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/as/recipe/frozenpkg/frozentgz.py
# Compiled at: 2013-03-25 12:36:39
import logging, os, sys, shutil, tempfile, zc.buildout, glob, fnmatch, subprocess
from frozen import Frozen

class FrozenTgz(Frozen):

    def install(self):
        """
        Create a RPM
        """
        additional_ops = []
        result_tgzs = []
        top_tgzbuild_dir = os.path.abspath(tempfile.mkdtemp(suffix='', prefix='tgzfreeze-'))
        pkg_name = self.options['pkg-name']
        pkg_version = self.options.get('pkg-version', '0.1')
        self.pkg_prefix = self.options.get('pkg-prefix', os.path.join('opt', pkg_name))
        buildroot_topdir = os.path.abspath(top_tgzbuild_dir + '/PKG/' + pkg_name)
        buildroot_projdir = os.path.abspath(buildroot_topdir + '/' + self.pkg_prefix)
        buildroot_tgzs = os.path.abspath(top_tgzbuild_dir + '/TGZ')
        self._setupPython(buildroot_projdir)
        pythonpath = self._copyAll(buildroot_topdir)
        for i in pythonpath:
            print '    ', i

        self._fixScripts(buildroot_projdir, pythonpath)
        tarfile = os.path.join(buildroot_tgzs, pkg_name + '-' + pkg_version + '.tar')
        tgzfile = self._createTar(buildroot_topdir, tarfile, compress=True)
        b_tgzfile = os.path.basename(tgzfile)
        full_tgzfile = os.path.join(self.buildout['buildout']['directory'], b_tgzfile)
        shutil.copy(tgzfile, full_tgzfile)
        self._log('Built %s' % full_tgzfile)
        result_tgzs = result_tgzs + [full_tgzfile]
        if not self.debug:
            shutil.rmtree(top_tgzbuild_dir)
        return result_tgzs

    def update(self):
        pass