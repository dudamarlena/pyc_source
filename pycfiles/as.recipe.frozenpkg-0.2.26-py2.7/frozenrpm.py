# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/as/recipe/frozenpkg/frozenrpm.py
# Compiled at: 2013-05-03 04:37:59
import StringIO, os, sys, shutil, tempfile, glob, fnmatch, subprocess
from frozen import Frozen
import logging
logger = logging.getLogger(__name__)
RPM_SPEC_TEMPLATE = '\n\n# empty lines\n\n%define _topdir         @TOP_DIR@\n%define _name           @PKG_NAME@\n\n%define _rpmtopdir      @TOP_DIR@/%{_name}\n%define _sourcedir      @TOP_DIR@/SOURCES\n%define _specdir        @TOP_DIR@/SPECS\n%define _rpmdir         @TOP_DIR@/RPMS\n%define _srcrpmdir      @TOP_DIR@/SRPMS\n\n# define _rpmfilename   SOMEFILENAME\n# define _arch          SOMEARCH\n# define _cpu           SOMECPU\n\n%define _unpackaged_files_terminate_build       0\n%define __prelink_undo_cmd                      /bin/true\n\nName:                 @PKG_NAME@\nVersion:              @PKG_VERSION@\nRelease:              @PKG_RELEASE@\nSummary:              @PKG_NAME@\nURL:                  @PKG_URL@\nLicense:              @PKG_LICENSE@\nVendor:               @PKG_VENDOR@\nPackager:             @PKG_PACKAGER@\nGroup:                @PKG_GROUP@\nAutoReqProv:          @PKG_AUTODEPS@\n\n@ADDITIONAL_OPS@\n\n%description\n\nThe @PKG_NAME@ package.\n@PKG_LICENSE@\n\n@SCRIPTS@\n\n%files\n\n%defattr(-, @ATTR_DEFAULT_USER@, @ATTR_DEFAULT_GROUP@, @ATTR_DEFAULT_MODE@)\n\n@PKG_PREFIX@\n\n@ATTR_CONFS@\n\n# empty lines\n'
RPM_BUILD_DIRS = [
 'BUILDROOT',
 'RPMS',
 'SOURCES',
 'SPECS',
 'SRPMS']

class FrozenRPM(Frozen):

    def _save_spec_file(self):
        rpmspec = RPM_SPEC_TEMPLATE
        rpmspec = rpmspec.replace('@TOP_DIR@', self.rpmbuild_dir)
        rpmspec = rpmspec.replace('@PKG_NAME@', self.pkg_name)
        rpmspec = rpmspec.replace('@PKG_VENDOR@', self.pkg_vendor)
        rpmspec = rpmspec.replace('@PKG_VERSION@', self.pkg_version)
        rpmspec = rpmspec.replace('@PKG_RELEASE@', self.pkg_release)
        rpmspec = rpmspec.replace('@PKG_PACKAGER@', self.pkg_packager)
        rpmspec = rpmspec.replace('@PKG_URL@', self.pkg_url)
        rpmspec = rpmspec.replace('@PKG_LICENSE@', self.pkg_license)
        rpmspec = rpmspec.replace('@PKG_GROUP@', self.pkg_group)
        rpmspec = rpmspec.replace('@PKG_AUTODEPS@', self.pkg_autodeps)
        rpmspec = rpmspec.replace('@PKG_PREFIX@', self.pkg_prefix)
        rpmspec = rpmspec.replace('@BUILD_ROOT@', self.buildroot)
        additional_ops = []
        if self.options.has_key('pkg-deps'):
            additional_ops = additional_ops + ['Requires: ' + self.options['pkg-deps']]
        rpmspec = rpmspec.replace('@ADDITIONAL_OPS@', ('\n').join(additional_ops))
        scripts = ''
        pre_cmds = self.options.get('pkg-pre-install', None)
        if pre_cmds:
            scripts += '%pre\n' + pre_cmds.strip() + '\n\n'
        post_cmds = self.options.get('pkg-post-install', None)
        if post_cmds:
            scripts += '%post\n' + post_cmds.strip() + '\n\n'
        rpmspec = rpmspec.replace('@SCRIPTS@', scripts)
        rpmspec = rpmspec.replace('@ATTR_DEFAULT_USER@', self.options.get('attr-def-user', 'root'))
        rpmspec = rpmspec.replace('@ATTR_DEFAULT_GROUP@', self.options.get('attr-def-group', 'root'))
        rpmspec = rpmspec.replace('@ATTR_DEFAULT_MODE@', self.options.get('attr-def-mode', '0755'))
        conf_lines = self.options.get('attr-conf', None)
        conf_lines_str = ''
        if conf_lines:
            for line in StringIO.StringIO(conf_lines).readlines():
                if not os.path.isabs(line):
                    line = os.path.abspath(self.pkg_prefix + '/' + line)
                conf_lines_str += '\n%config ' + line

        rpmspec = rpmspec.replace('@ATTR_CONFS@', conf_lines_str)
        spec_filename = os.path.abspath(os.path.join(self.buildroot, self.pkg_name) + '.spec')
        logger.debug('Using spec file %s' % spec_filename)
        spec_file = None
        try:
            spec_file = open(spec_filename, 'w')
            spec_file.write(rpmspec)
            spec_file.flush()
        except Exception as e:
            return []

        if spec_file:
            spec_file.close()
        return

    def install(self):
        """
        Create a RPM
        """
        super(FrozenRPM, self).install()
        self._create_rpm_dirs()
        self._save_spec_file()
        self._copy_eggs()
        self._copy_outputs()
        self._create_extra_dirs()
        self._copy_extra_files()
        self._extra_cleanups()
        self._prepare_venv()
        tar_filename = os.path.join(self.rpmbuild_dir, 'SOURCES', self.pkg_name + '.tar')
        tar_filename = self._create_tar(tar_filename)
        command = [
         'rpmbuild',
         '--buildroot', self.buildroot,
         '--define',
         '_topdir %s' % self.rpmbuild_dir,
         '-ta', tar_filename]
        logger.info('Launching "%s".' % (' ').join(command))
        job = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, _ = job.communicate()
        if job.returncode != 0:
            logger.critical('could not build the RPM.')
            print stdout
            return []
        result_rpms = []
        for arch_dir in os.listdir(os.path.join(self.rpmbuild_dir, 'RPMS')):
            full_arch_dir = os.path.abspath(os.path.join(self.rpmbuild_dir, 'RPMS', arch_dir))
            if os.path.isdir(full_arch_dir):
                for rpm_file in os.listdir(full_arch_dir):
                    if fnmatch.fnmatch(rpm_file, '*.rpm'):
                        full_rpm_file = os.path.abspath(os.path.join(full_arch_dir, rpm_file))
                        shutil.copy(full_rpm_file, self.buildout['buildout']['directory'])
                        logger.debug('Built %s' % rpm_file)
                        result_rpms = result_rpms + [rpm_file]

        if not self.debug:
            shutil.rmtree(self.rpmbuild_dir)
        return result_rpms

    def _create_rpm_dirs(self):
        """
        Create all the top dirs
        """
        for p in RPM_BUILD_DIRS:
            full_p = os.path.join(self.rpmbuild_dir, p)
            if not os.path.exists(full_p):
                try:
                    os.makedirs(full_p)
                except:
                    logger.critical('ERROR: could not create directory "%s"' % full_p)
                    shutil.rmtree(self.rpmbuild_dir, ignore_errors=True)
                    raise

    def update(self):
        pass