# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-sin1koo5/setuptools/setuptools/command/sdist.py
# Compiled at: 2019-07-30 18:46:55
# Size of source mod 2**32: 7388 bytes
from distutils import log
import distutils.command.sdist as orig, os, sys, io, contextlib
from setuptools.extern import six
from .py36compat import sdist_add_defaults
import pkg_resources
_default_revctrl = list

def walk_revctrl(dirname=''):
    """Find all files under revision control"""
    for ep in pkg_resources.iter_entry_points('setuptools.file_finders'):
        for item in ep.load()(dirname):
            yield item


class sdist(sdist_add_defaults, orig.sdist):
    __doc__ = 'Smart sdist that finds anything supported by revision control'
    user_options = [
     ('formats=', None, 'formats for source distribution (comma-separated list)'),
     ('keep-temp', 'k', 'keep the distribution tree around after creating archive file(s)'),
     ('dist-dir=', 'd', 'directory to put the source distribution archive(s) in [default: dist]')]
    negative_opt = {}
    README_EXTENSIONS = [
     '', '.rst', '.txt', '.md']
    READMES = tuple('README{0}'.format(ext) for ext in README_EXTENSIONS)

    def run(self):
        self.run_command('egg_info')
        ei_cmd = self.get_finalized_command('egg_info')
        self.filelist = ei_cmd.filelist
        self.filelist.append(os.path.join(ei_cmd.egg_info, 'SOURCES.txt'))
        self.check_readme()
        for cmd_name in self.get_sub_commands():
            self.run_command(cmd_name)

        self.make_distribution()
        dist_files = getattr(self.distribution, 'dist_files', [])
        for file in self.archive_files:
            data = (
             'sdist', '', file)
            if data not in dist_files:
                dist_files.append(data)

    def initialize_options(self):
        orig.sdist.initialize_options(self)
        self._default_to_gztar()

    def _default_to_gztar(self):
        if sys.version_info >= (3, 6, 0, 'beta', 1):
            return
        self.formats = [
         'gztar']

    def make_distribution(self):
        """
        Workaround for #516
        """
        with self._remove_os_link():
            orig.sdist.make_distribution(self)

    @staticmethod
    @contextlib.contextmanager
    def _remove_os_link():
        """
        In a context, remove and restore os.link if it exists
        """

        class NoValue:
            pass

        orig_val = getattr(os, 'link', NoValue)
        try:
            del os.link
        except Exception:
            pass

        try:
            yield
        finally:
            if orig_val is not NoValue:
                setattr(os, 'link', orig_val)

    def __read_template_hack(self):
        try:
            orig.sdist.read_template(self)
        except Exception:
            _, _, tb = sys.exc_info()
            tb.tb_next.tb_frame.f_locals['template'].close()
            raise

    has_leaky_handle = sys.version_info < (2, 7, 2) or (3, 0) <= sys.version_info < (3,
                                                                                     1,
                                                                                     4) or (3,
                                                                                            2) <= sys.version_info < (3,
                                                                                                                      2,
                                                                                                                      1)
    if has_leaky_handle:
        read_template = _sdist__read_template_hack

    def _add_defaults_python(self):
        """getting python files"""
        if self.distribution.has_pure_modules():
            build_py = self.get_finalized_command('build_py')
            self.filelist.extend(build_py.get_source_files())
            if not self.distribution.include_package_data:
                for _, src_dir, _, filenames in build_py.data_files:
                    self.filelist.extend([os.path.join(src_dir, filename) for filename in filenames])

    def _add_defaults_data_files(self):
        try:
            if six.PY2:
                sdist_add_defaults._add_defaults_data_files(self)
            else:
                super()._add_defaults_data_files()
        except TypeError:
            log.warn('data_files contains unexpected objects')

    def check_readme(self):
        for f in self.READMES:
            if os.path.exists(f):
                return
        else:
            self.warn('standard file not found: should have one of ' + ', '.join(self.READMES))

    def make_release_tree(self, base_dir, files):
        orig.sdist.make_release_tree(self, base_dir, files)
        dest = os.path.join(base_dir, 'setup.cfg')
        if hasattr(os, 'link'):
            if os.path.exists(dest):
                os.unlink(dest)
                self.copy_file('setup.cfg', dest)
        self.get_finalized_command('egg_info').save_version_info(dest)

    def _manifest_is_not_generated(self):
        if not os.path.isfile(self.manifest):
            return False
        else:
            with io.open(self.manifest, 'rb') as (fp):
                first_line = fp.readline()
            return first_line != '# file GENERATED by distutils, do NOT edit\n'.encode()

    def read_manifest(self):
        """Read the manifest file (named by 'self.manifest') and use it to
        fill in 'self.filelist', the list of files to include in the source
        distribution.
        """
        log.info("reading manifest file '%s'", self.manifest)
        manifest = open(self.manifest, 'rb')
        for line in manifest:
            if six.PY3:
                try:
                    line = line.decode('UTF-8')
                except UnicodeDecodeError:
                    log.warn('%r not UTF-8 decodable -- skipping' % line)
                    continue

                line = line.strip()
                if line.startswith('#') or not line:
                    pass
                else:
                    self.filelist.append(line)

        manifest.close()

    def check_license(self):
        """Checks if license_file' is configured and adds it to
        'self.filelist' if the value contains a valid path.
        """
        opts = self.distribution.get_option_dict('metadata')
        _, license_file = opts.get('license_file', (None, None))
        if license_file is None:
            log.debug("'license_file' option was not specified")
            return
        if not os.path.exists(license_file):
            log.warn("warning: Failed to find the configured license file '%s'", license_file)
            return
        self.filelist.append(license_file)