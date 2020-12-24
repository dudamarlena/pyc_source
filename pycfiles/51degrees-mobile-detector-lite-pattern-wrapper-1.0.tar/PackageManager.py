# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Lib\DistExt\PackageManager.py
# Compiled at: 2006-10-30 16:51:37
from __future__ import generators
import os, sys, types, copy, warnings
from distutils import core
from distutils.core import DEBUG
from distutils.errors import *
from distutils.fancy_getopt import translate_longopt
from Ft.Lib import ImportUtil
from Ft.Lib.DistExt import Dist, Structures, Version
core.USAGE = 'Usage:\n  %(script)s [global_opts] cmd1 [cmd1_opts] [cmd2 [cmd2_opts] ...]\n  %(script)s --help [cmd1 cmd2 ...]\n  %(script)s cmd --help\n  %(script)s --help-commands\n  %(script)s --help-packages\n'
PKGINFO_FORMAT = {'name': str, 'package': str, 'version': str, 'description': str, 'long_description': str, 'package_file': str, 'keywords': list, 'classifiers': list, 'download_url': str, 'requires': list, 'provides': list, 'obsoletes': list, 'requires_python': list, 'validate_templates': list, 'manifest_templates': list, 'bgen_files': list, 'config_module': str, 'packages': list, 'package_data': dict, 'package_dir': dict, 'py_modules': list, 'libraries': list, 'ext_modules': list, 'scripts': list, 'doc_files': list, 'l10n': list, 'headers': list, 'data_files': list, 'sysconf_files': list, 'localstate_files': list, 'devel_files': list}

class PackageManager(Dist.Dist):
    __module__ = __name__
    toplevel_options = Dist.Dist.toplevel_options + [('package=', 'p', 'limit command(s) to a given package')]
    display_options = [
     (
      'help-packages', None, 'list all available packages')] + Dist.Dist.display_options
    display_option_names = [
     'help_packages'] + Dist.Dist.display_option_names

    def __init__(self, attrs):
        self.package_options = {}
        self.package = None
        self.package_files = []
        self.package_defaults = {}
        self._nonpackage_options = list(vars(self))
        if attrs:
            for name in self._nonpackage_options:
                if name in attrs:
                    setattr(self, name, attrs[name])
                    del attrs[name]

        Dist.Dist.__init__(self, attrs)
        if attrs:
            for name in ('manifest_templates', 'validate_templates'):
                if name in attrs:
                    del attrs[name]

            self.package_defaults.update(attrs)
        return
        return

    def finalize_options(self):
        for (package, options) in self.package_options.items():
            try:
                self.check_package_options(options)
            except DistutilsSetupError, error:
                raise DistutilsSetupError("in 'package_options' package %r: %s" % (package, error))

            assert options['package'] == package, "'package' conflicts with 'package_options' key"

        self.distributions = {}
        Dist.Dist.finalize_options(self)
        return

    def check_package_options(self, options):
        """
        Ensure that the package attributes are valid and the required
        fields are provided.

        Raise DistutilsSetupError if the stucture is invalid anywhere.
        """
        for (option, value) in options.items():
            try:
                typeinfo = PKGINFO_FORMAT[option]
            except KeyError:
                raise DistutilsSetupError('unsupported package attribute: %s' % option)

            if not isinstance(value, typeinfo):
                expected_type = typeinfo.__name__
                compared_type = type(value).__name__
                raise DistutilsSetupError('package attribute %r must be %s, not %s' % (option, expected_type, compared_type))

        if 'name' not in options:
            if 'package' not in options:
                raise DistutilsSetupError("one of 'name' or 'package' is required")
            options['name'] = '%s-%s' % (self.get_name(), options['package'])
        if 'version' not in options:
            options['version'] = self.get_version()
        for option in ('description', 'long_description'):
            if option not in options:
                raise DistutilsSetupError('missing required %r field' % option)

        return

    def parse_config_files(self, filenames=None):
        """
        Overrides parse_config_files() to update 'package_defaults' with
        any global values from the config files and to parse the package
        files to populate the 'package_options' dictionary.
        """
        Dist.Dist.parse_config_files(self, filenames)
        if DEBUG:
            print 'PackageManager.parse_config_files():'
        if 'global' in self.command_options:
            options = {}
            for opt in self.command_options['global']:
                if opt in self.negative_opt:
                    opt = self.negative_opt[opt]
                if opt not in self._nonpackage_options:
                    self.package_defaults[opt] = getattr(self, opt)

        for filename in self.package_files:
            (name, options) = self.parse_package_file(filename)
            self.get_package_options(name).update(options)

        for options in self.package_options.values():
            if 'namespace_packages' in options or 'packages' not in options:
                continue
            namespace_packages = {}
            packages = options['packages']
            for package in packages:
                if '.' in package:
                    parent = ('.').join(package.split('.')[:-1])
                    if parent not in packages:
                        namespace_packages[parent] = package

            options['namespace_packages'] = list(namespace_packages)

        return

    def parse_package_file(self, filename):
        """
        Returns a dictionary of the options defined in the package definition
        'filename'.
        """
        if DEBUG:
            print 'PackageManager.parse_package_file(): parsing %r' % filename
        structs = {'Extension': core.Extension}
        for name in Structures.__all__:
            structs[name] = getattr(Structures, name)

        options = {}
        execfile(filename, structs, options)
        ignored_types = (
         types.ModuleType, types.NoneType)
        for (option, value) in options.items():
            if option.startswith('_') or isinstance(value, ignored_types):
                del options[option]

        try:
            self.check_package_options(options)
        except DistutilsSetupError, error:
            raise DistutilsSetupError('in %s: %s' % (filename, error))

        name = options['name']
        if name in self.package_options:
            existing = self.package_options[name]['package_file']
            raise DistutilsSetupError('package file %r conflicts with %r' % filename, existing)
        options['package_file'] = filename
        return (
         name, options)

    def parse_command_line(self):
        """
        Overrides parse_command_line() to validate the '--package' option and
        to add the command-line options to the default package options.
        """
        ok = Dist.Dist.parse_command_line(self)
        if ok:
            if DEBUG:
                print 'PackageManager.parse_command_line():'
            if self.package and self.package not in self.package_options:
                raise DistutilsArgError("package '%s' is unknown, use --help-packages to get a complete listing" % self.package)
            defaults = self.package_defaults.setdefault('command_options', {})
            for (command, options) in self.command_options.items():
                command_options = defaults.setdefault(command, {})
                command_options.update(options)

        return ok

    def handle_display_options(self, option_order):
        """
        Overrides handle_display_options() to update 'package_defaults'
        and handle the '--help-packages' option.
        """
        toplevel_options = {}
        help_options = {}
        display_options = {}
        any_display_options = False
        any_help_options = False
        for option in Dist.Dist._get_toplevel_options(self):
            toplevel_options[option[0]] = True

        for option in self.display_options:
            option = option[0]
            if option.startswith('help'):
                help_options[option] = True
            else:
                display_options[option] = True

        for (option, value) in option_order:
            if option in toplevel_options:
                name = translate_longopt(option)
                self.package_defaults[name] = value
            elif option in display_options:
                any_display_options = True
            elif option in help_options:
                any_help_options = True

        if self.help_packages:
            self.print_packages()
            print
            print core.gen_usage(self.script_name)
            return 1
        if any_help_options:
            return Dist.Dist.handle_display_options(self, option_order)
        elif any_display_options:
            for dist in self.get_distributions():
                print "Information for '%s' package:" % dist.get_name()
                for (option, value) in option_order:
                    if value and option in display_options:
                        name = translate_longopt(option)
                        value = getattr(dist.metadata, 'get_' + name)()
                        if name in ('keywords', 'platforms'):
                            value = (',').join(value)
                        elif isinstance(value, list):
                            value = ('\n  ').join(value)
                        print '  ' + value

                print

        return any_display_options

    def print_packages(self):
        """Print out a help message listing all available packages with a
        description of each.  The descriptions come from the package
        definition's 'description' field.
        """
        packages = list(self.package_options)
        packages.sort()
        max_length = max(map(len, packages))
        print 'Available packages:'
        for package in packages:
            options = self.get_package_options(package)
            try:
                description = options['description']
            except KeyError:
                description = '(no description available)'

            print '  %-*s  %s' % (max_length, package, description)

        return

    def get_package_options(self, package):
        """Get the option dictionary for a given package.  If that packages's
        option dictionary hasn't been created yet, then create it and return
        the new dictionary; otherwise, return the existing option dictionary.
        """
        dict = self.package_options.get(package)
        if dict is None:
            dict = self.package_options[package] = {}
        return dict
        return

    def get_package_distribution(self, package):
        """
        Return the distribution object for 'package'. Normally this object
        is cached on a previous call to 'get_package_distribution()'; if no
        distribution object is in the cache, then it is created.
        """
        if package in self.distributions:
            return self.distributions[package]
        if DEBUG:
            print "PackageManager.get_package_distriution(): creating '%s' distribution object" % package
        try:
            options = self.package_options[package]
        except KeyError:
            raise DistutilsSetupError('invalid package: %s' % package)

        attrs = copy.deepcopy(self.package_defaults)
        for (option, value) in options.items():
            if isinstance(value, tuple):
                value = list(value)
            current = attrs.get(option)
            if current is None or option in ('name', 'version'):
                attrs[option] = value
            elif isinstance(current, list) and isinstance(value, list):
                current.extend(value)
            elif isinstance(current, dict) and isinstance(value, dict):
                current.update(value)
            else:
                raise DistutilsSetupError('duplicate values for %r field' % option)

        attrs['main_distribution'] = self
        dist = self.distributions[package] = Dist.Dist(attrs)
        return dist
        return

    def get_distributions(self):
        if self.package:
            distributions = [self.get_package_distribution(self.package)]
        else:
            distributions = [ self.get_package_distribution(package) for package in self.package_options ]
            distributions = self._sort_distributions(distributions)
        return distributions

    def _find_installed_packages(self, paths=None):
        for path in paths or sys.path:
            for package in self._scan_path(path):
                yield package

        return

    def _scan_path(self, path):
        if DEBUG:
            print 'PackageManager._scan_path(): scanning', path
        if path.endswith('.egg'):
            pathname = os.path.join(path, 'EGG-INFO', 'PKG-INFO')
            if DEBUG:
                print '  loading', pathname
            if os.path.isdir(path):
                yield Dist.DistributionMetadata.from_filename(pathname)
            else:
                importer = ImportUtil.GetImporter(path)
                if importer is not None:
                    data = importer.get_data(pathname)
                    yield Dist.DistributionMetadata.from_string(data)
        elif os.path.isdir(path):
            for name in os.listdir(path):
                if name.endswith('.egg-info'):
                    pathname = os.path.join(path, name)
                    if os.path.isdir(pathname):
                        pathname = os.path.join(pathname, 'PKG-INFO')
                    if DEBUG:
                        print '  loading', pathname
                    yield Dist.DistributionMetadata.from_filename(pathname)

        return
        return

    def _sort_distributions(self, distributions):
        """
        Sort a list of distribution objects based on the "internal"
        'requires' and 'provides' lists.
        """
        if DEBUG:
            print 'PackageManager._sort_distributions():'

        def get_provides(package):
            provides = {}
            package_version = Version.CommonVersion(package.get_version())
            for provision in package.get_provides():
                (name, vers) = Version.SplitProvision(provision)
                provides[name] = vers or package_version

            return provides

        installed_provides = {}
        for package in self._find_installed_packages():
            installed_provides.update(get_provides(package))

        package_provides = {}
        for dist in distributions:
            package_provides.update(get_provides(dist))

        unsorted = list(distributions)
        satisfied = {}
        sorted = []
        while unsorted:
            changed = 0
            if DEBUG:
                print '  begin sort:'
            for dist in tuple(unsorted):
                if DEBUG:
                    print '    trying', dist.get_name()
                for req in dist.get_requires():
                    req = Version.VersionPredicate(req)
                    if req.name in package_provides:
                        if req.name in satisfied:
                            continue
                        else:
                            break
                    if req.name in installed_provides:
                        if not req.satisfied_by(installed_provides[req.name]):
                            raise DistutilsSetupError("requirement '%s' not satisfied" % req)
                    elif req.name not in installed_provides:
                        try:
                            __import__(req.name)
                        except ImportError:
                            raise DistutilsSetupError("requirement '%s' not found" % req)

                else:
                    if DEBUG:
                        print '    sorted', dist.get_name()
                    satisfied.update(get_provides(dist))
                    sorted.append(dist)
                    unsorted.remove(dist)
                    changed = 1

            if not changed:
                names = (', ').join([ dist.get_name() for dist in unsorted ])
                raise DistutilsFileError('circular dependency: %s' % names)

        if DEBUG:
            names = (', ').join([ dist.get_name() for dist in sorted ])
            print '  sorted:', names
        return sorted

    def run_commands(self):
        """
        Overrides run_commands() to handle multiple source packages in a
        single setup script.
        """
        if not self.package_options:
            Dist.Dist.run_commands(self)
            return
        if DEBUG:
            print 'PackageManager.run_commands():'
        for dist in self.get_distributions():
            for command in self.commands:
                dist.run_command(command)

        return