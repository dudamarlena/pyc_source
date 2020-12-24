# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Lib\DistExt\BDistInno.py
# Compiled at: 2006-10-30 16:17:59
import os, sys, zipfile
from distutils import util
from distutils.core import Command
from distutils.errors import DistutilsInternalError, DistutilsPlatformError
from distutils.dir_util import remove_tree
from distutils.sysconfig import get_python_version
INNO_MIN_VERSION = '5.1.5'
INNO_MAX_VERSION = '5.1.7'
PY_SOURCE_EXTS = (
 '.py', '.pyw')
ISCC_TEMPLATE = '\n[Setup]\nOutputDir=%(output-dir)s\nOutputBaseFilename=%(output-basename)s\nCompression=lzma\nSolidCompression=yes\nAppName=%(name)s\nAppVersion=%(version)s\nAppVerName=%(name)s %(version)s for Python %(target-version)s\nAppId=%(name)s-%(target-version)s\nAppPublisher=%(publisher)s\nAppPublisherURL=%(publisher-url)s\nAppSupportURL=%(support-url)s\nUninstallFilesDir=%(uninstall-dir)s\nDefaultDirName={code:GetDefaultDir}\nDefaultGroupName={code:GetDefaultGroup}\nLicenseFile=%(license-file)s\nUserInfoPage=no\nDisableReadyMemo=yes\nDirExistsWarning=no\nAppendDefaultDirName=no\n\n[Types]\nName: "full"; Description: "Full installation"\nName: "compact"; Description: "Compact installation"\nName: "custom"; Description: "Custom installation"; Flags: iscustom\n\n[Components]\n%(components)s\n\n%(sections)s\n\n[Code]\n{ Define parameters as constants to easy sharing between the script file\n  and the template in BDistInno.py }\nconst\n  GroupName = \'%(name)s\';\n  TargetVersion = \'%(target-version)s\';\n\nvar\n  PythonDir, PythonGroup: String;\n\nfunction GetDefaultDir(Param: String): String;\nbegin\n  Result := RemoveBackslashUnlessRoot(PythonDir);\nend; { GetDefaultDir }\n\nfunction GetDefaultGroup(Param: String): String;\nbegin\n  Result := AddBackslash(PythonGroup) + GroupName;\nend; { GetDefaultGroup }\n\nprocedure MutateConfigFile(Filename: String);\nvar\n  Config: String;\n  Prefix: String;\nbegin\n  Filename := ExpandConstant(Filename);\n  LoadStringFromFile(Filename, Config);\n  Prefix := AddBackslash(WizardDirValue());\n  StringChange(Prefix, \'\\\', \'\\\\\')\n  StringChange(Config, \'\\\\PREFIX\\\\\', Prefix);\n  SaveStringToFile(Filename, Config, False);\nend; { MutateConfigFile }\n\nprocedure InitializeSelectDirPage;\nvar\n  Page: TWizardPage;\n  Text: TLabel;\n  Top, Left, Width: Integer;\nbegin\n  Page := PageFromID(wpSelectDir);\n  Top := WizardForm.DirEdit.Top + WizardForm.DirEdit.Height + 16;\n  Left := WizardForm.SelectDirBrowseLabel.Left;\n  Width := WizardForm.SelectDirBrowseLabel.Width;\n\n  Text := TLabel.Create(Page);\n  Text.Parent := Page.Surface;\n  Text.Top := Top;\n  Text.Left := Left;\n  Text.Font.Style := [fsBold];\n  Text.AutoSize := True;\n  Text.WordWrap := True;\n  Text.Width := Width;\n  Text.Caption := \'Warning: A valid Python \' + TargetVersion +\n                  \' installation could not be found.\';\n  Top := Top + Text.Height + 16;\n\n  Text := TLabel.Create(Page);\n  Text.Parent := Page.Surface;\n  Text.Top := Top;\n  Text.Left := Left;\n  Text.AutoSize := True;\n  Text.WordWrap := True;\n  Text.Width := Width;\n  Text.Caption := \'If you have a custom build of Python installed, select\' +\n                  \' the folder where it is installed as the installation\' +\n                  \' location.\';\nend; { InitializeSelectDirPage }\n\nprocedure InitializeWizard;\nbegin\n  { Add customizations to the SelectDir page if Python is not found }\n  if PythonDir = \'\' then\n    InitializeSelectDirPage;\nend; { InitializeWizard }\n\nfunction InitializeSetup(): Boolean;\nvar\n  Key: String;\nbegin\n  { Get the default installation directory }\n  Key := \'Software\\Python\\PythonCore\\\' + TargetVersion + \'\\InstallPath\';\n  if not RegQueryStringValue(HKEY_CURRENT_USER, Key, \'\', PythonDir) then\n    RegQueryStringValue(HKEY_LOCAL_MACHINE, Key, \'\', PythonDir);\n\n  { Get default Start Menu group }\n  Key := Key + \'\\InstallGroup\';\n  if not RegQueryStringValue(HKEY_CURRENT_USER, Key, \'\', PythonGroup) then\n    RegQueryStringValue(HKEY_LOCAL_MACHINE, Key, \'\', PythonGroup);\n\n  Result := True;\nend; { InitializeSetup }\n\nfunction NextButtonClick(CurPage: Integer): Boolean;\nbegin\n  Result := True;\n  if CurPage = wpSelectDir then\n  begin\n    { Check that the install directory is part of PYTHONPATH }\n  end\nend; { NextButtonClick }\n'

class Section(object):
    __module__ = __name__
    section_name = None
    required_parameters = None
    optional_parameters = ['Languages', 'MinVersion', 'OnlyBelowVersion', 'BeforeInstall', 'AfterInstall']

    def __init__(self):
        assert self.section_name is not None, "'section_name' must be defined"
        assert self.required_parameters is not None, "'required_parameters' must be defined"
        self.entries = []
        return

    def addEntry(self, **parameters):
        entry = []
        for parameter in self.required_parameters:
            try:
                value = parameters[parameter]
            except KeyError:
                raise DistutilsInternalError("missing required parameter '%s'" % parameter)
            else:
                del parameters[parameter]

            entry.append('%s: %s' % (parameter, value))

        for parameter in self.optional_parameters:
            if parameter in parameters:
                entry.append('%s: %s' % (parameter, parameters[parameter]))
                del parameters[parameter]

        for parameter in parameters:
            raise DistutilsInternalError("unsupported parameter '%s'" % parameter)

        self.entries.append(('; ').join(entry))
        return


class DirsSection(Section):
    __module__ = __name__
    section_name = 'Dirs'
    required_parameters = ['Name']
    optional_parameters = Section.optional_parameters + ['Attribs', 'Permissions', 'Flags']


class FilesSection(Section):
    __module__ = __name__
    section_name = 'Files'
    required_parameters = ['Source', 'DestDir']
    optional_parameters = Section.optional_parameters + ['DestName', 'Excludes', 'CopyMode', 'Attribs', 'Permissions', 'FontInstall', 'Flags']


class IconsSection(Section):
    __module__ = __name__
    section_name = 'Icons'
    required_parameters = ['Name', 'Filename']
    optional_parameters = Section.optional_parameters + ['Parameters', 'WorkingDir', 'HotKey', 'Comment', 'IconFilename', 'IconIndex', 'Flags']


class RunSection(Section):
    __module__ = __name__
    section_name = 'Run'
    required_parameters = ['Filename']
    optional_parameters = Section.optional_parameters + ['Description', 'Parameters', 'WorkingDir', 'StatusMsg', 'RunOnceId', 'Flags']


class UninstallDeleteSection(Section):
    __module__ = __name__
    section_name = 'UninstallDelete'
    required_parameters = ['Type', 'Name']


class Component:
    __module__ = __name__
    section_mapping = {'Dirs': DirsSection, 'Files': FilesSection, 'Icons': IconsSection, 'Run': RunSection, 'UninstallDelete': UninstallDeleteSection}

    def __init__(self, name, description, types):
        self.name = name
        self.description = description
        self.types = types
        self.sections = {}

    def getEntry(self):
        return 'Name: "%s"; Description: "%s"; Types: %s' % (self.name, self.description, self.types)

    def hasEntries(self):
        for section in self.sections.itervalues():
            if section.entries:
                return True

        return False

    def getSection(self, name):
        if name not in self.sections:
            try:
                section_class = self.section_mapping[name]
            except KeyError:
                raise DistutilsInternalError("unknown section '%s'" % name)
            else:
                self.sections[name] = section_class()
        return self.sections[name]

    def getSectionEntries(self, name):
        return [ '%s; Components: %s' % (entry, self.name) for entry in self.getSection(name).entries ]


class BDistInno(Command):
    __module__ = __name__
    command_name = 'bdist_inno'
    description = 'create an executable installer for MS Windows'
    user_options = [
     (
      'bdist-dir=', None, 'temporary directory for creating the distribution'), ('keep-temp', 'k', 'keep the pseudo-installation tree around after ' + 'creating the distribution archive'), ('target-version=', None, 'require a specific python version on the target system'), ('no-target-compile', 'c', 'do not compile .py to .pyc on the target system'), ('no-target-optimize', 'o', 'do not compile .py to .pyo (optimized) on the target system'), ('dist-dir=', 'd', 'directory to put final built distributions in'), ('skip-build', None, 'skip rebuilding everything (for testing/debugging)')]
    boolean_options = [
     'keep-temp', 'no-target-compile', 'no-target-optimize', 'skip-build']

    def initialize_options(self):
        self.bdist_dir = None
        self.keep_temp = None
        self.target_version = None
        self.no_target_compile = None
        self.no_target_optimize = None
        self.dist_dir = None
        self.skip_build = None
        self.byte_compile = True
        return
        return

    def finalize_options(self):
        if self.bdist_dir is None:
            bdist_base = self.get_finalized_command('bdist').bdist_base
            self.bdist_dir = os.path.join(bdist_base, 'inno')
        self.set_undefined_options('bdist', (
         'keep_temp', 'keep_temp'), (
         'dist_dir', 'dist_dir'), (
         'skip_build', 'skip_build'))
        if not self.target_version:
            self.target_version = get_python_version()
        if not self.skip_build and (self.distribution.has_ext_modules() or self.distribution.has_scripts()):
            short_version = get_python_version()
            if self.target_version != short_version:
                raise DistutilsOptionError("target version can only be %s, or the '--skip_build' option must be specified" % short_version)
            self.target_version = short_version
        self.license_file = self.distribution.license_file
        if self.license_file:
            self.license_file = util.convert_path(self.license_file)
        self.output_basename = '%s.win32'
        return
        return

    def run(self):
        if sys.platform != 'win32':
            raise DistutilsPlatformError('InnoSetup distributions must be created on a Windows platform')
        from _winreg import OpenKeyEx, QueryValueEx, HKEY_LOCAL_MACHINE
        try:
            key = OpenKeyEx(HKEY_LOCAL_MACHINE, 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Inno Setup 5_is1')
            inno_version = QueryValueEx(key, 'DisplayVersion')[0]
            inno_path = QueryValueEx(key, 'InstallLocation')[0]
        except WindowsError:
            raise DistutilsPlatformError('Inno Setup version %s to %s is required to build the installer, but was not found on this system.' % (INNO_MIN_VERSION, INNO_MAX_VERSION))

        if inno_version < INNO_MIN_VERSION or inno_version > INNO_MAX_VERSION:
            raise DistutilsPlatformError('Inno Setup version %s to %s is required to build the installer, but version %s was found on this system.' % (INNO_MIN_VERSION, INNO_MAX_VERSION, inno_version))
        iss_compiler = os.path.join(inno_path, 'iscc.exe')
        if not self.skip_build:
            self.run_command('build')
        self.mkpath(self.bdist_dir)
        config = self.reinitialize_command('config')
        config.cache_filename = None
        config.prefix = 'PREFIX'
        config.ensure_finalized()
        install = self.reinitialize_command('install')
        install.root = self.bdist_dir
        install.skip_build = self.skip_build
        install.compile = install.optimize = self.byte_compile
        install.warn_dir = False
        install.with_docs = True
        self.announce('installing to %s' % self.bdist_dir, 2)
        install.ensure_finalized()
        install.run()
        if self.license_file:
            self.copy_file(self.license_file, self.bdist_dir)
        iss_file = self.build_iss_file()
        iss_path = os.path.join(self.bdist_dir, '%s.iss' % self.distribution.get_name())
        self.announce('writing %r' % iss_path)
        if not self.dry_run:
            f = open(iss_path, 'w')
            f.write(iss_file)
            f.close()
        self.announce('creating Inno Setup installer', 2)
        self.spawn([iss_compiler, iss_path])
        dist_filename = self.get_installer_filename()
        if os.path.exists(dist_filename) and not self.dry_run:
            install_egg_info = self.get_finalized_command('install_egg_info')
            install_dir = install_egg_info.install_dir
            zip_dir = 'PLATLIB'
            if install_dir.endswith(os.sep):
                zip_dir += os.sep
            zip_file = zipfile.ZipFile(dist_filename, 'a')
            for filename in install_egg_info.get_outputs():
                arcname = filename.replace(install_dir, zip_dir, 1)
                zip_file.write(filename, arcname)

            zip_file.close()
        if hasattr(self.distribution, 'dist_files'):
            target_version = self.target_version or 'any'
            spec = ('bdist_wininst', target_version, dist_filename)
            self.distribution.dist_files.append(spec)
        if not self.keep_temp:
            remove_tree(self.bdist_dir, self.verbose, self.dry_run)
        return
        return

    def build_iss_file(self):
        """Generate the text of an InnoSetup iss file and return it as a
        list of strings (one per line).
        """
        filespec = 'Source: "%s"; DestDir: "%s"; Components: %s'
        dirspec = 'Name: "%s"; Components: %s'
        uninstallspec = 'Type: files; Name: "%s"'
        iconspec = 'Name: "%s"; Filename: "%s"; Components: %s'
        runspec = 'Description: "%s"; Filename: "%s"; Components: %s; Flags: %s'
        main_component = Component('Main', self.distribution.get_name() + ' Library', 'full compact custom')
        docs_component = Component('Main\\Documentation', 'Documentation', 'full')
        test_component = Component('Main\\Testsuite', 'Test suite', 'full')
        install = self.get_finalized_command('install')
        for command_name in install.get_sub_commands():
            command = self.get_finalized_command(command_name)
            (dirs, files, uninstall) = self._mutate_outputs(command)
            if command_name == 'install_html':
                component = docs_component
                for document in command.documents:
                    flags = getattr(document, 'flags', ())
                    if 'postinstall' in flags:
                        section = component.getSection('Run')
                        filename = command.get_output_filename(document)
                        filename = self._mutate_filename(filename)[1]
                        section.addEntry(Description='"View %s"' % document.title, Filename='"%s"' % filename, Flags='postinstall shellexec skipifsilent')
                    if 'shortcut' in flags:
                        section = component.getSection('Icons')
                        filename = command.get_output_filename(document)
                        filename = self._mutate_filename(filename)[1]
                        section.addEntry(Name='"{group}\\%s"' % document.title, Filename='"%s"' % filename)

            elif command_name == 'install_text':
                component = docs_component
            elif command_name == 'install_devel':
                component = test_component
            elif command_name == 'install_config':
                component = main_component
                section = component.getSection('Files')
                for (source, destdir, extra) in files:
                    dest = os.path.join(destdir, os.path.basename(source))
                    extra['AfterInstall'] = "MutateConfigFile('%s')" % dest

            else:
                component = main_component
            if dirs:
                section = component.getSection('Dirs')
                for name in dirs:
                    section.addEntry(Name='"%s"' % name)

            if files:
                section = component.getSection('Files')
                for (source, destdir, extra) in files:
                    section.addEntry(Source=('"%s"' % source), DestDir=('"%s"' % destdir), Flags='ignoreversion', **extra)

            if uninstall:
                section = component.getSection('UninstallDelete')
                for name in uninstall:
                    section.addEntry(Type='files', Name='"%s"' % name)

        components = []
        sections = {}
        for component in (main_component, docs_component, test_component):
            has_entries = False
            for section in component.sections:
                entries = component.getSectionEntries(section)
                if entries:
                    has_entries = True
                    if section not in sections:
                        sections[section] = [
                         '[%s]' % section]
                    sections[section].extend(entries)

            if has_entries:
                components.append(component.getEntry())

        components = ('\n').join(components)
        for name in sections:
            sections[name] = ('\n').join(sections[name])

        sections = ('\n\n').join(sections.values())
        output_filename = self.get_installer_filename()
        (output_dir, output_basename) = os.path.split(output_filename)
        output_basename = os.path.splitext(output_basename)[0]
        uninstall_dir = os.path.join(install.install_localstate, 'Uninstall')
        (_, uninstall_dir) = self._mutate_filename(uninstall_dir)
        subst = {'output-dir': os.path.abspath(output_dir), 'output-basename': output_basename, 'name': self.distribution.get_name(), 'version': self.distribution.get_version(), 'publisher': self.distribution.get_author(), 'publisher-url': self.distribution.get_author_email(), 'support-url': self.distribution.get_url(), 'uninstall-dir': uninstall_dir, 'license-file': os.path.basename(self.license_file or ''), 'target-version': sys.version[:3], 'custom-page': self.license_file and 'wpLicense' or 'wpWelcome', 'components': components, 'sections': sections}
        return ISCC_TEMPLATE % subst

    def _mutate_filename(self, filename):
        source = filename[len(self.bdist_dir) + len(os.sep):]
        dest = source.replace('PREFIX', '{app}', 1)
        return (source, dest)

    def _mutate_outputs(self, command):
        dirs = []
        files = []
        uninstall = []
        compile = getattr(command, 'compile', 0)
        optimize = getattr(command, 'optimize', 0)
        for filename in command.get_outputs():
            (source, dest) = self._mutate_filename(filename)
            if os.path.isdir(filename):
                dirs.append(dest)
            else:
                files.append((source, os.path.dirname(dest), {}))
                for extension in PY_SOURCE_EXTS:
                    if dest.endswith(extension):
                        barename = dest[:-len(extension)]
                        if not compile:
                            uninstall.append(barename + '.pyc')
                        if not optimize:
                            uninstall.append(barename + '.pyo')

        return (
         dirs, files, uninstall)

    def get_installer_filename(self):
        installer_name = '%s.win32' % self.distribution.get_fullname()
        if self.target_version:
            installer_name += '-py' + self.target_version
        return os.path.join(self.dist_dir, installer_name + '.exe')