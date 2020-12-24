# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-sin1koo5/setuptools/setuptools/command/bdist_rpm.py
# Compiled at: 2019-07-30 18:46:55
# Size of source mod 2**32: 1508 bytes
import distutils.command.bdist_rpm as orig

class bdist_rpm(orig.bdist_rpm):
    __doc__ = "\n    Override the default bdist_rpm behavior to do the following:\n\n    1. Run egg_info to ensure the name and version are properly calculated.\n    2. Always run 'install' using --single-version-externally-managed to\n       disable eggs in RPM distributions.\n    3. Replace dash with underscore in the version numbers for better RPM\n       compatibility.\n    "

    def run(self):
        self.run_command('egg_info')
        orig.bdist_rpm.run(self)

    def _make_spec_file(self):
        version = self.distribution.get_version()
        rpmversion = version.replace('-', '_')
        spec = orig.bdist_rpm._make_spec_file(self)
        line23 = '%define version ' + version
        line24 = '%define version ' + rpmversion
        spec = [line.replace('Source0: %{name}-%{version}.tar', 'Source0: %{name}-%{unmangled_version}.tar').replace('setup.py install ', 'setup.py install --single-version-externally-managed ').replace('%setup', '%setup -n %{name}-%{unmangled_version}').replace(line23, line24) for line in spec]
        insert_loc = spec.index(line24) + 1
        unmangled_version = '%define unmangled_version ' + version
        spec.insert(insert_loc, unmangled_version)
        return spec