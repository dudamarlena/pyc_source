# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/me/projects/keystone.git/tmp/keystone.git/llvm/utils/llvm-build/llvmbuild/main.py
# Compiled at: 2016-06-04 06:22:29
from __future__ import absolute_import
import filecmp, os, sys, llvmbuild.componentinfo as componentinfo, llvmbuild.configutil as configutil
from llvmbuild.util import fatal, note

def cmake_quote_string(value):
    """
    cmake_quote_string(value) -> str

    Return a quoted form of the given value that is suitable for use in CMake
    language files.
    """
    value = value.replace('\\', '\\\\')
    return value


def cmake_quote_path(value):
    """
    cmake_quote_path(value) -> str

    Return a quoted form of the given value that is suitable for use in CMake
    language files.
    """
    value = value.replace('\\', '/')
    return value


def mk_quote_string_for_target(value):
    """
    mk_quote_string_for_target(target_name) -> str

    Return a quoted form of the given target_name suitable for including in a
    Makefile as a target name.
    """
    return value.replace(':', '\\:')


def make_install_dir(path):
    """
    make_install_dir(path) -> None

    Create the given directory path for installation, including any parents.
    """
    if not os.path.exists(path):
        os.makedirs(path)


class LLVMProjectInfo(object):

    @staticmethod
    def load_infos_from_path(llvmbuild_source_root):

        def recurse(subpath):
            llvmbuild_path = os.path.join(llvmbuild_source_root + subpath, 'LLVMBuild.txt')
            if not os.path.exists(llvmbuild_path):
                fatal('missing LLVMBuild.txt file at: %r' % (llvmbuild_path,))
            common, info_iter = componentinfo.load_from_path(llvmbuild_path, subpath)
            for info in info_iter:
                yield info

            for subdir in common.get_list('subdirectories'):
                for item in recurse(os.path.join(subpath, subdir)):
                    yield item

        return recurse('/')

    @staticmethod
    def load_from_path(source_root, llvmbuild_source_root):
        infos = list(LLVMProjectInfo.load_infos_from_path(llvmbuild_source_root))
        return LLVMProjectInfo(source_root, infos)

    def __init__(self, source_root, component_infos):
        self.source_root = source_root
        self.component_infos = list(component_infos)
        self.component_info_map = None
        self.ordered_component_infos = None
        return

    def validate_components(self):
        """validate_components() -> None

        Validate that the project components are well-defined. Among other
        things, this checks that:
          - Components have valid references.
          - Components references do not form cycles.

        We also construct the map from component names to info, and the
        topological ordering of components.
        """
        self.component_info_map = {}
        for ci in self.component_infos:
            existing = self.component_info_map.get(ci.name)
            if existing is not None:
                fatal('found duplicate component %r (at %r and %r)' % (
                 ci.name, ci.subpath, existing.subpath))
            self.component_info_map[ci.name] = ci

        if 'all' in self.component_info_map:
            fatal("project is not allowed to define 'all' component")
        if '$ROOT' in self.component_info_map:
            fatal('project is not allowed to define $ROOT component')
        self.component_info_map['$ROOT'] = componentinfo.GroupComponentInfo('/', '$ROOT', None)
        self.component_infos.append(self.component_info_map['$ROOT'])

        def visit_component_info(ci, current_stack, current_set):
            if ci in current_set:
                cycle_description = (' -> ').join('%r (%s)' % (ci.name, relation) for relation, ci in current_stack)
                fatal('found cycle to %r after following: %s -> %s' % (
                 ci.name, cycle_description, ci.name))
            if ci not in components_to_visit:
                return
            else:
                components_to_visit.remove(ci)
                if ci.parent is not None:
                    parent = self.component_info_map.get(ci.parent)
                    if parent is None:
                        fatal('component %r has invalid reference %r (via %r)' % (
                         ci.name, ci.parent, 'parent'))
                    ci.set_parent_instance(parent)
                for relation, referent_name in ci.get_component_references():
                    referent = self.component_info_map.get(referent_name)
                    if referent is None:
                        fatal('component %r has invalid reference %r (via %r)' % (
                         ci.name, referent_name, relation))
                    current_stack.append((relation, ci))
                    current_set.add(ci)
                    visit_component_info(referent, current_stack, current_set)
                    current_set.remove(ci)
                    current_stack.pop()

                self.ordered_component_infos.append(ci)
                return

        self.ordered_component_infos = []
        components_to_visit = sorted(set(self.component_infos), key=lambda c: c.name)
        while components_to_visit:
            visit_component_info(components_to_visit[0], [], set())

        for c in self.ordered_component_infos:
            c.children.sort(key=lambda c: c.name)

        return

    def print_tree(self):

        def visit(node, depth=0):
            print '%s%-40s (%s)' % ('  ' * depth, node.name, node.type_name)
            for c in node.children:
                visit(c, depth + 1)

        visit(self.component_info_map['$ROOT'])

    def write_components(self, output_path):
        info_basedir = {}
        for ci in self.component_infos:
            if ci.parent is None:
                continue
            info_basedir[ci.subpath] = info_basedir.get(ci.subpath, []) + [ci]

        subpath_subdirs = {}
        for ci in self.component_infos:
            if ci.subpath == '/':
                continue
            parent_path = os.path.dirname(ci.subpath)
            subpath_subdirs[parent_path] = parent_list = subpath_subdirs.get(parent_path, set())
            parent_list.add(os.path.basename(ci.subpath))

        for subpath, infos in info_basedir.items():
            infos.sort(key=lambda ci: ci.name)
            fragments = []
            subdirectories = subpath_subdirs.get(subpath)
            if subdirectories:
                fragment = 'subdirectories = %s\n' % ((' ').join(sorted(subdirectories)),)
                fragments.append(('common', fragment))
            num_common_fragments = len(fragments)
            for ci in infos:
                fragment = ci.get_llvmbuild_fragment()
                if fragment is None:
                    continue
                name = 'component_%d' % (len(fragments) - num_common_fragments)
                fragments.append((name, fragment))

            if not fragments:
                continue
            if not subpath.startswith('/'):
                raise AssertionError
                directory_path = os.path.join(output_path, subpath[1:])
                os.path.exists(directory_path) or os.makedirs(directory_path)
            f = open(infos[0]._source_path)
            comments_map = {}
            comment_block = ''
            for ln in f:
                if ln.startswith(';'):
                    comment_block += ln
                elif ln.startswith('[') and ln.endswith(']\n'):
                    comments_map[ln[1:-2]] = comment_block
                else:
                    comment_block = ''

            f.close()
            file_path = os.path.join(directory_path, 'LLVMBuild.txt')
            f = open(file_path, 'w')
            header_fmt = ';===- %s %s-*- Conf -*--===;'
            header_name = '.' + os.path.join(subpath, 'LLVMBuild.txt')
            header_pad = '-' * (80 - len(header_fmt % (header_name, '')))
            header_string = header_fmt % (header_name, header_pad)
            f.write('%s\n;\n;                     The LLVM Compiler Infrastructure\n;\n; This file is distributed under the University of Illinois Open Source\n; License. See LICENSE.TXT for details.\n;\n;===------------------------------------------------------------------------===;\n;\n; This is an LLVMBuild description file for the components in this subdirectory.\n;\n; For more information on the LLVMBuild system, please see:\n;\n;   http://llvm.org/docs/LLVMBuild.html\n;\n;===------------------------------------------------------------------------===;\n\n' % header_string)
            for name, fragment in fragments:
                comment = comments_map.get(name)
                if comment is not None:
                    f.write(comment)
                f.write('[%s]\n' % name)
                f.write(fragment)
                if fragment is not fragments[(-1)][1]:
                    f.write('\n')

            f.close()

        return

    def write_library_table(self, output_path, enabled_optional_components):
        entries = {}
        for c in self.ordered_component_infos:
            if c.type_name == 'OptionalLibrary' and c.name not in enabled_optional_components:
                continue
            tg = c.get_parent_target_group()
            if tg and not tg.enabled:
                continue
            if c.type_name not in ('Library', 'OptionalLibrary', 'LibraryGroup', 'TargetGroup'):
                continue
            llvmconfig_component_name = c.get_llvmconfig_component_name()
            if c.type_name == 'Library' or c.type_name == 'OptionalLibrary':
                library_name = c.get_prefixed_library_name()
                is_installed = c.installed
            else:
                library_name = None
                is_installed = True
            required_llvmconfig_component_names = [ self.component_info_map[dep].get_llvmconfig_component_name() for dep in c.required_libraries
                                                  ]
            for dep in c.add_to_library_groups:
                entries[dep][2].append(llvmconfig_component_name)

            entries[c.name] = (
             llvmconfig_component_name, library_name,
             required_llvmconfig_component_names,
             is_installed)

        entries = list(entries.values())
        root_entries = set(e[0] for e in entries)
        for _, _, deps, _ in entries:
            root_entries -= set(deps)

        entries.append(('all', None, root_entries, True))
        entries.sort()
        max_required_libraries = max(len(deps) for _, _, deps, _ in entries) + 1
        make_install_dir(os.path.dirname(output_path))
        f = open(output_path + '.new', 'w')
        f.write('//===- llvm-build generated file --------------------------------*- C++ -*-===//\n//\n// Component Library Depenedency Table\n//\n// Automatically generated file, do not edit!\n//\n//===----------------------------------------------------------------------===//\n\n')
        f.write('struct AvailableComponent {\n')
        f.write('  /// The name of the component.\n')
        f.write('  const char *Name;\n')
        f.write('\n')
        f.write('  /// The name of the library for this component (or NULL).\n')
        f.write('  const char *Library;\n')
        f.write('\n')
        f.write('  /// Whether the component is installed.\n')
        f.write('  bool IsInstalled;\n')
        f.write('\n')
        f.write('  /// The list of libraries required when linking this component.\n')
        f.write('  const char *RequiredLibraries[%d];\n' % max_required_libraries)
        f.write('} AvailableComponents[%d] = {\n' % len(entries))
        for name, library_name, required_names, is_installed in entries:
            if library_name is None:
                library_name_as_cstr = 'nullptr'
            else:
                library_name_as_cstr = '"lib%s.a"' % library_name
            if is_installed:
                is_installed_as_cstr = 'true'
            else:
                is_installed_as_cstr = 'false'
            f.write('  { "%s", %s, %s, { %s } },\n' % (
             name, library_name_as_cstr, is_installed_as_cstr,
             (', ').join('"%s"' % dep for dep in required_names)))

        f.write('};\n')
        f.close()
        if not os.path.isfile(output_path):
            os.rename(output_path + '.new', output_path)
        elif filecmp.cmp(output_path, output_path + '.new'):
            os.remove(output_path + '.new')
        else:
            os.remove(output_path)
            os.rename(output_path + '.new', output_path)
        return

    def get_required_libraries_for_component(self, ci, traverse_groups=False):
        """
        get_required_libraries_for_component(component_info) -> iter

        Given a Library component info descriptor, return an iterator over all
        of the directly required libraries for linking with this component. If
        traverse_groups is True, then library and target groups will be
        traversed to include their required libraries.
        """
        assert ci.type_name in ('Library', 'OptionalLibrary', 'LibraryGroup', 'TargetGroup')
        for name in ci.required_libraries:
            dep = self.component_info_map[name]
            if dep.type_name == 'Library' or dep.type_name == 'OptionalLibrary':
                yield dep
                continue
            if dep.type_name in ('LibraryGroup', 'TargetGroup'):
                if not traverse_groups:
                    yield dep
                    continue
                for res in self.get_required_libraries_for_component(dep, True):
                    yield res

    def get_fragment_dependencies(self):
        """
        get_fragment_dependencies() -> iter

        Compute the list of files (as absolute paths) on which the output
        fragments depend (i.e., files for which a modification should trigger a
        rebuild of the fragment).
        """
        build_paths = set()
        for ci in self.component_infos:
            p = os.path.join(self.source_root, ci.subpath[1:], 'LLVMBuild.txt')
            if p not in build_paths:
                yield p
                build_paths.add(p)

        for module in sys.modules.values():
            if not hasattr(module, '__file__'):
                continue
            path = getattr(module, '__file__')
            if not path:
                continue
            if os.path.splitext(path)[1] in ('.pyc', '.pyo', '.pyd'):
                path = path[:-1]
            if path.startswith(self.source_root) and os.path.exists(path):
                yield path

    def foreach_cmake_library(self, f, enabled_optional_components, skip_disabled, skip_not_installed):
        for ci in self.ordered_component_infos:
            if ci.type_name == 'OptionalLibrary' and ci.name not in enabled_optional_components:
                continue
            if ci.type_name not in ('Library', 'OptionalLibrary'):
                continue
            if skip_disabled:
                tg = ci.get_parent_target_group()
                if tg and not tg.enabled:
                    continue
            if skip_not_installed and not ci.installed:
                continue
            f(ci)

    def write_cmake_fragment(self, output_path, enabled_optional_components):
        """
        write_cmake_fragment(output_path) -> None

        Generate a CMake fragment which includes all of the collated LLVMBuild
        information in a format that is easily digestible by a CMake. The exact
        contents of this are closely tied to how the CMake configuration
        integrates LLVMBuild, see CMakeLists.txt in the top-level.
        """
        dependencies = list(self.get_fragment_dependencies())
        make_install_dir(os.path.dirname(output_path))
        f = open(output_path, 'w')
        header_fmt = '#===-- %s - LLVMBuild Configuration for LLVM %s-*- CMake -*--===#'
        header_name = os.path.basename(output_path)
        header_pad = '-' * (80 - len(header_fmt % (header_name, '')))
        header_string = header_fmt % (header_name, header_pad)
        f.write('%s\n#\n#                     The LLVM Compiler Infrastructure\n#\n# This file is distributed under the University of Illinois Open Source\n# License. See LICENSE.TXT for details.\n#\n#===------------------------------------------------------------------------===#\n#\n# This file contains the LLVMBuild project information in a format easily\n# consumed by the CMake based build system.\n#\n# This file is autogenerated by llvm-build, do not edit!\n#\n#===------------------------------------------------------------------------===#\n\n' % header_string)
        f.write("\n# LLVMBuild CMake fragment dependencies.\n#\n# CMake has no builtin way to declare that the configuration depends on\n# a particular file. However, a side effect of configure_file is to add\n# said input file to CMake's internal dependency list. So, we use that\n# and a dummy output file to communicate the dependency information to\n# CMake.\n#\n# FIXME: File a CMake RFE to get a properly supported version of this\n# feature.\n")
        for dep in dependencies:
            f.write('configure_file("%s"\n               ${CMAKE_CURRENT_BINARY_DIR}/DummyConfigureOutput)\n' % (
             cmake_quote_path(dep),))

        f.write('\n# Explicit library dependency information.\n#\n# The following property assignments effectively create a map from component\n# names to required libraries, in a way that is easily accessed from CMake.\n')
        self.foreach_cmake_library(lambda ci: f.write('set_property(GLOBAL PROPERTY LLVMBUILD_LIB_DEPS_%s %s)\n' % (
         ci.get_prefixed_library_name(),
         (' ').join(sorted(dep.get_prefixed_library_name() for dep in self.get_required_libraries_for_component(ci))))), enabled_optional_components, skip_disabled=False, skip_not_installed=False)
        f.close()

    def write_cmake_exports_fragment(self, output_path, enabled_optional_components):
        """
        write_cmake_exports_fragment(output_path) -> None

        Generate a CMake fragment which includes LLVMBuild library
        dependencies expressed similarly to how CMake would write
        them via install(EXPORT).
        """
        dependencies = list(self.get_fragment_dependencies())
        make_install_dir(os.path.dirname(output_path))
        f = open(output_path, 'w')
        f.write('# Explicit library dependency information.\n#\n# The following property assignments tell CMake about link\n# dependencies of libraries imported from LLVM.\n')
        self.foreach_cmake_library(lambda ci: f.write('set_property(TARGET %s PROPERTY IMPORTED_LINK_INTERFACE_LIBRARIES %s)\n' % (
         ci.get_prefixed_library_name(),
         (' ').join(sorted(dep.get_prefixed_library_name() for dep in self.get_required_libraries_for_component(ci))))), enabled_optional_components, skip_disabled=True, skip_not_installed=True)
        f.close()

    def write_make_fragment(self, output_path, enabled_optional_components):
        """
        write_make_fragment(output_path) -> None

        Generate a Makefile fragment which includes all of the collated
        LLVMBuild information in a format that is easily digestible by a
        Makefile. The exact contents of this are closely tied to how the LLVM
        Makefiles integrate LLVMBuild, see Makefile.rules in the top-level.
        """
        dependencies = list(self.get_fragment_dependencies())
        make_install_dir(os.path.dirname(output_path))
        f = open(output_path, 'w')
        header_fmt = '#===-- %s - LLVMBuild Configuration for LLVM %s-*- Makefile -*--===#'
        header_name = os.path.basename(output_path)
        header_pad = '-' * (80 - len(header_fmt % (header_name, '')))
        header_string = header_fmt % (header_name, header_pad)
        f.write('%s\n#\n#                     The LLVM Compiler Infrastructure\n#\n# This file is distributed under the University of Illinois Open Source\n# License. See LICENSE.TXT for details.\n#\n#===------------------------------------------------------------------------===#\n#\n# This file contains the LLVMBuild project information in a format easily\n# consumed by the Makefile based build system.\n#\n# This file is autogenerated by llvm-build, do not edit!\n#\n#===------------------------------------------------------------------------===#\n\n' % header_string)
        f.write('# Clients must explicitly enable LLVMBUILD_INCLUDE_DEPENDENCIES to get\n# these dependencies. This is a compromise to help improve the\n# performance of recursive Make systems.\n')
        f.write('ifeq ($(LLVMBUILD_INCLUDE_DEPENDENCIES),1)\n')
        f.write('# The dependencies for this Makefile fragment itself.\n')
        f.write('%s: \\\n' % (mk_quote_string_for_target(output_path),))
        for dep in dependencies:
            f.write('\t%s \\\n' % (dep,))

        f.write('\n')
        f.write('# The dummy targets to allow proper regeneration even when files are moved or\n# removed.\n')
        for dep in dependencies:
            f.write('%s:\n' % (mk_quote_string_for_target(dep),))

        f.write('endif\n')
        f.write("\n# List of libraries to be exported for use by applications.\n# See 'cmake/modules/Makefile'.\nLLVM_LIBS_TO_EXPORT :=")
        self.foreach_cmake_library(lambda ci: f.write(' \\\n  %s' % ci.get_prefixed_library_name()), enabled_optional_components, skip_disabled=True, skip_not_installed=True)
        f.write('\n')
        f.close()


def add_magic_target_components(parser, project, opts):
    """add_magic_target_components(project, opts) -> None

    Add the "magic" target based components to the project, which can only be
    determined based on the target configuration options.

    This currently is responsible for populating the required_libraries list of
    the "all-targets", "Native", "NativeCodeGen", and "Engine" components.
    """
    available_targets = dict((ci.name, ci) for ci in project.component_infos if ci.type_name == 'TargetGroup')
    native_target_name = {'x86': 'X86', 'x86_64': 'X86', 
       'Unknown': None}.get(opts.native_target, opts.native_target)
    if native_target_name is None:
        native_target = None
    else:
        native_target = available_targets.get(native_target_name)
        if native_target is None:
            parser.error('invalid native target: %r (not in project)' % (
             opts.native_target,))
        if native_target.type_name != 'TargetGroup':
            parser.error('invalid native target: %r (not a target)' % (
             opts.native_target,))
        if opts.enable_targets is None:
            enable_targets = available_targets.values()
        elif opts.enable_targets == '':
            enable_target_names = []
        else:
            if ' ' in opts.enable_targets:
                enable_target_names = opts.enable_targets.split()
            else:
                enable_target_names = opts.enable_targets.split(';')
            enable_targets = []
            for name in enable_target_names:
                target = available_targets.get(name)
                if target is None:
                    parser.error('invalid target to enable: %r (not in project)' % (
                     name,))
                if target.type_name != 'TargetGroup':
                    parser.error('invalid target to enable: %r (not a target)' % (
                     name,))
                enable_targets.append(target)

        def find_special_group(name):
            info = info_map.get(name)
            if info is None:
                fatal('expected project to contain special %r component' % (
                 name,))
            if info.type_name != 'LibraryGroup':
                fatal('special component %r should be a LibraryGroup' % (
                 name,))
            if info.required_libraries:
                fatal('special component %r must have empty %r list' % (
                 name, 'required_libraries'))
            if info.add_to_library_groups:
                fatal('special component %r must have empty %r list' % (
                 name, 'add_to_library_groups'))
            info._is_special_group = True
            return info

        info_map = dict((ci.name, ci) for ci in project.component_infos)
        all_targets = find_special_group('all-targets')
        native_group = find_special_group('Native')
        engine_group = find_special_group('Engine')
        for ci in enable_targets:
            all_targets.required_libraries.append(ci.name)
            ci.enabled = True

    if native_target and native_target.enabled:
        native_group.required_libraries.append(native_target.name)
    if native_target and native_target.enabled and native_target.has_jit:
        engine_group.required_libraries.append(native_group.name)
    return


def main():
    from optparse import OptionParser, OptionGroup
    parser = OptionParser('usage: %prog [options]')
    group = OptionGroup(parser, 'Input Options')
    group.add_option('', '--source-root', dest='source_root', metavar='PATH', help='Path to the LLVM source (inferred if not given)', action='store', default=None)
    group.add_option('', '--llvmbuild-source-root', dest='llvmbuild_source_root', help='If given, an alternate path to search for LLVMBuild.txt files', action='store', default=None, metavar='PATH')
    group.add_option('', '--build-root', dest='build_root', metavar='PATH', help='Path to the build directory (if needed) [%default]', action='store', default=None)
    parser.add_option_group(group)
    group = OptionGroup(parser, 'Output Options')
    group.add_option('', '--print-tree', dest='print_tree', help='Print out the project component tree [%default]', action='store_true', default=False)
    group.add_option('', '--write-llvmbuild', dest='write_llvmbuild', help='Write out the LLVMBuild.txt files to PATH', action='store', default=None, metavar='PATH')
    group.add_option('', '--write-library-table', dest='write_library_table', metavar='PATH', help='Write the C++ library dependency table to PATH', action='store', default=None)
    group.add_option('', '--write-cmake-fragment', dest='write_cmake_fragment', metavar='PATH', help='Write the CMake project information to PATH', action='store', default=None)
    group.add_option('', '--write-cmake-exports-fragment', dest='write_cmake_exports_fragment', metavar='PATH', help='Write the CMake exports information to PATH', action='store', default=None)
    group.add_option('', '--write-make-fragment', dest='write_make_fragment', metavar='PATH', help='Write the Makefile project information to PATH', action='store', default=None)
    group.add_option('', '--configure-target-def-file', dest='configure_target_def_files', help="Configure the given file at SUBPATH (relative to\nthe inferred or given source root, and with a '.in' suffix) by replacing certain\nsubstitution variables with lists of targets that support certain features (for\nexample, targets with AsmPrinters) and write the result to the build root (as\ngiven by --build-root) at the same SUBPATH", metavar='SUBPATH', action='append', default=None)
    parser.add_option_group(group)
    group = OptionGroup(parser, 'Configuration Options')
    group.add_option('', '--native-target', dest='native_target', metavar='NAME', help="Treat the named target as the 'native' one, if given [%default]", action='store', default=None)
    group.add_option('', '--enable-targets', dest='enable_targets', metavar='NAMES', help='Enable the given space or semi-colon separated list of targets, or all targets if not present', action='store', default=None)
    group.add_option('', '--enable-optional-components', dest='optional_components', metavar='NAMES', help='Enable the given space or semi-colon separated list of optional components', action='store', default='')
    parser.add_option_group(group)
    opts, args = parser.parse_args()
    source_root = opts.source_root
    if source_root:
        if not os.path.exists(os.path.join(source_root, 'lib', 'IR', 'Function.cpp')):
            parser.error('invalid LLVM source root: %r' % source_root)
    else:
        llvmbuild_path = os.path.dirname(__file__)
        llvm_build_path = os.path.dirname(llvmbuild_path)
        utils_path = os.path.dirname(llvm_build_path)
        source_root = os.path.dirname(utils_path)
    llvmbuild_source_root = opts.llvmbuild_source_root or source_root
    project_info = LLVMProjectInfo.load_from_path(source_root, llvmbuild_source_root)
    add_magic_target_components(parser, project_info, opts)
    project_info.validate_components()
    if opts.print_tree:
        project_info.print_tree()
    if opts.write_llvmbuild:
        project_info.write_components(opts.write_llvmbuild)
    if opts.write_library_table:
        project_info.write_library_table(opts.write_library_table, opts.optional_components)
    if opts.write_make_fragment:
        project_info.write_make_fragment(opts.write_make_fragment, opts.optional_components)
    if opts.write_cmake_fragment:
        project_info.write_cmake_fragment(opts.write_cmake_fragment, opts.optional_components)
    if opts.write_cmake_exports_fragment:
        project_info.write_cmake_exports_fragment(opts.write_cmake_exports_fragment, opts.optional_components)
    if opts.configure_target_def_files:
        if not opts.build_root:
            parser.error('must specify --build-root when using --configure-target-def-file')
        available_targets = [ ci for ci in project_info.component_infos if ci.type_name == 'TargetGroup'
                            ]
        substitutions = [
         (
          '@LLVM_ENUM_TARGETS@',
          (' ').join('LLVM_TARGET(%s)' % ci.name for ci in available_targets)),
         (
          '@LLVM_ENUM_ASM_PRINTERS@',
          (' ').join('LLVM_ASM_PRINTER(%s)' % ci.name for ci in available_targets if ci.has_asmprinter)),
         (
          '@LLVM_ENUM_ASM_PARSERS@',
          (' ').join('LLVM_ASM_PARSER(%s)' % ci.name for ci in available_targets if ci.has_asmparser)),
         (
          '@LLVM_ENUM_DISASSEMBLERS@',
          (' ').join('LLVM_DISASSEMBLER(%s)' % ci.name for ci in available_targets if ci.has_disassembler))]
        for subpath in opts.configure_target_def_files:
            inpath = os.path.join(source_root, subpath + '.in')
            outpath = os.path.join(opts.build_root, subpath)
            result = configutil.configure_file(inpath, outpath, substitutions)
            if not result:
                note("configured file %r hasn't changed" % outpath)

    return


if __name__ == '__main__':
    main()