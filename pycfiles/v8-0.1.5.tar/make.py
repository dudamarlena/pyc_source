# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lex/projects/python-v8/libv8/build/gyp/pylib/gyp/generator/make.py
# Compiled at: 2014-04-20 15:47:30
import os, re, sys, subprocess, gyp, gyp.common, gyp.xcode_emulation
from gyp.common import GetEnvironFallback
generator_default_variables = {'EXECUTABLE_PREFIX': '', 
   'EXECUTABLE_SUFFIX': '', 
   'STATIC_LIB_PREFIX': 'lib', 
   'SHARED_LIB_PREFIX': 'lib', 
   'STATIC_LIB_SUFFIX': '.a', 
   'INTERMEDIATE_DIR': '$(obj).$(TOOLSET)/$(TARGET)/geni', 
   'SHARED_INTERMEDIATE_DIR': '$(obj)/gen', 
   'PRODUCT_DIR': '$(builddir)', 
   'RULE_INPUT_ROOT': '%(INPUT_ROOT)s', 
   'RULE_INPUT_DIRNAME': '%(INPUT_DIRNAME)s', 
   'RULE_INPUT_PATH': '$(abspath $<)', 
   'RULE_INPUT_EXT': '$(suffix $<)', 
   'RULE_INPUT_NAME': '$(notdir $<)', 
   'CONFIGURATION_NAME': '$(BUILDTYPE)'}
generator_supports_multiple_toolsets = True
generator_wants_sorted_dependencies = False
generator_additional_non_configuration_keys = []
generator_additional_path_sections = []
generator_extra_sources_for_rules = []
generator_filelist_paths = None

def CalculateVariables(default_variables, params):
    """Calculate additional variables for use in the build (called by gyp)."""
    global generator_additional_non_configuration_keys
    global generator_additional_path_sections
    global generator_extra_sources_for_rules
    flavor = gyp.common.GetFlavor(params)
    if flavor == 'mac':
        default_variables.setdefault('OS', 'mac')
        default_variables.setdefault('SHARED_LIB_SUFFIX', '.dylib')
        default_variables.setdefault('SHARED_LIB_DIR', generator_default_variables['PRODUCT_DIR'])
        default_variables.setdefault('LIB_DIR', generator_default_variables['PRODUCT_DIR'])
        import gyp.generator.xcode as xcode_generator
        generator_additional_non_configuration_keys = getattr(xcode_generator, 'generator_additional_non_configuration_keys', [])
        generator_additional_path_sections = getattr(xcode_generator, 'generator_additional_path_sections', [])
        generator_extra_sources_for_rules = getattr(xcode_generator, 'generator_extra_sources_for_rules', [])
        COMPILABLE_EXTENSIONS.update({'.m': 'objc', '.mm': 'objcxx'})
    else:
        operating_system = flavor
        if flavor == 'android':
            operating_system = 'linux'
        default_variables.setdefault('OS', operating_system)
        default_variables.setdefault('SHARED_LIB_SUFFIX', '.so')
        default_variables.setdefault('SHARED_LIB_DIR', '$(builddir)/lib.$(TOOLSET)')
        default_variables.setdefault('LIB_DIR', '$(obj).$(TOOLSET)')


def CalculateGeneratorInputInfo(params):
    """Calculate the generator specific info that gets fed to input (called by
  gyp)."""
    global generator_filelist_paths
    global generator_wants_sorted_dependencies
    generator_flags = params.get('generator_flags', {})
    android_ndk_version = generator_flags.get('android_ndk_version', None)
    if android_ndk_version:
        generator_wants_sorted_dependencies = True
    output_dir = params['options'].generator_output or params['options'].toplevel_dir
    builddir_name = generator_flags.get('output_dir', 'out')
    qualified_out_dir = os.path.normpath(os.path.join(output_dir, builddir_name, 'gypfiles'))
    generator_filelist_paths = {'toplevel': params['options'].toplevel_dir, 
       'qualified_out_dir': qualified_out_dir}
    return


SPACE_REPLACEMENT = '?'
LINK_COMMANDS_LINUX = 'quiet_cmd_alink = AR($(TOOLSET)) $@\ncmd_alink = rm -f $@ && $(AR.$(TOOLSET)) crs $@ $(filter %.o,$^)\n\nquiet_cmd_alink_thin = AR($(TOOLSET)) $@\ncmd_alink_thin = rm -f $@ && $(AR.$(TOOLSET)) crsT $@ $(filter %.o,$^)\n\n# Due to circular dependencies between libraries :(, we wrap the\n# special "figure out circular dependencies" flags around the entire\n# input list during linking.\nquiet_cmd_link = LINK($(TOOLSET)) $@\ncmd_link = $(LINK.$(TOOLSET)) $(GYP_LDFLAGS) $(LDFLAGS.$(TOOLSET)) -o $@ -Wl,--start-group $(LD_INPUTS) -Wl,--end-group $(LIBS)\n\n# We support two kinds of shared objects (.so):\n# 1) shared_library, which is just bundling together many dependent libraries\n# into a link line.\n# 2) loadable_module, which is generating a module intended for dlopen().\n#\n# They differ only slightly:\n# In the former case, we want to package all dependent code into the .so.\n# In the latter case, we want to package just the API exposed by the\n# outermost module.\n# This means shared_library uses --whole-archive, while loadable_module doesn\'t.\n# (Note that --whole-archive is incompatible with the --start-group used in\n# normal linking.)\n\n# Other shared-object link notes:\n# - Set SONAME to the library filename so our binaries don\'t reference\n# the local, absolute paths used on the link command-line.\nquiet_cmd_solink = SOLINK($(TOOLSET)) $@\ncmd_solink = $(LINK.$(TOOLSET)) -shared $(GYP_LDFLAGS) $(LDFLAGS.$(TOOLSET)) -Wl,-soname=$(@F) -o $@ -Wl,--whole-archive $(LD_INPUTS) -Wl,--no-whole-archive $(LIBS)\n\nquiet_cmd_solink_module = SOLINK_MODULE($(TOOLSET)) $@\ncmd_solink_module = $(LINK.$(TOOLSET)) -shared $(GYP_LDFLAGS) $(LDFLAGS.$(TOOLSET)) -Wl,-soname=$(@F) -o $@ -Wl,--start-group $(filter-out FORCE_DO_CMD, $^) -Wl,--end-group $(LIBS)\n'
LINK_COMMANDS_MAC = 'quiet_cmd_alink = LIBTOOL-STATIC $@\ncmd_alink = rm -f $@ && ./gyp-mac-tool filter-libtool libtool $(GYP_LIBTOOLFLAGS) -static -o $@ $(filter %.o,$^)\n\nquiet_cmd_link = LINK($(TOOLSET)) $@\ncmd_link = $(LINK.$(TOOLSET)) $(GYP_LDFLAGS) $(LDFLAGS.$(TOOLSET)) -o "$@" $(LD_INPUTS) $(LIBS)\n\nquiet_cmd_solink = SOLINK($(TOOLSET)) $@\ncmd_solink = $(LINK.$(TOOLSET)) -shared $(GYP_LDFLAGS) $(LDFLAGS.$(TOOLSET)) -o "$@" $(LD_INPUTS) $(LIBS)\n\nquiet_cmd_solink_module = SOLINK_MODULE($(TOOLSET)) $@\ncmd_solink_module = $(LINK.$(TOOLSET)) -bundle $(GYP_LDFLAGS) $(LDFLAGS.$(TOOLSET)) -o $@ $(filter-out FORCE_DO_CMD, $^) $(LIBS)\n'
LINK_COMMANDS_ANDROID = 'quiet_cmd_alink = AR($(TOOLSET)) $@\ncmd_alink = rm -f $@ && $(AR.$(TOOLSET)) crs $@ $(filter %.o,$^)\n\nquiet_cmd_alink_thin = AR($(TOOLSET)) $@\ncmd_alink_thin = rm -f $@ && $(AR.$(TOOLSET)) crsT $@ $(filter %.o,$^)\n\n# Due to circular dependencies between libraries :(, we wrap the\n# special "figure out circular dependencies" flags around the entire\n# input list during linking.\nquiet_cmd_link = LINK($(TOOLSET)) $@\nquiet_cmd_link_host = LINK($(TOOLSET)) $@\ncmd_link = $(LINK.$(TOOLSET)) $(GYP_LDFLAGS) $(LDFLAGS.$(TOOLSET)) -o $@ -Wl,--start-group $(LD_INPUTS) -Wl,--end-group $(LIBS)\ncmd_link_host = $(LINK.$(TOOLSET)) $(GYP_LDFLAGS) $(LDFLAGS.$(TOOLSET)) -o $@ $(LD_INPUTS) $(LIBS)\n\n# Other shared-object link notes:\n# - Set SONAME to the library filename so our binaries don\'t reference\n# the local, absolute paths used on the link command-line.\nquiet_cmd_solink = SOLINK($(TOOLSET)) $@\ncmd_solink = $(LINK.$(TOOLSET)) -shared $(GYP_LDFLAGS) $(LDFLAGS.$(TOOLSET)) -Wl,-soname=$(@F) -o $@ -Wl,--whole-archive $(LD_INPUTS) -Wl,--no-whole-archive $(LIBS)\n\nquiet_cmd_solink_module = SOLINK_MODULE($(TOOLSET)) $@\ncmd_solink_module = $(LINK.$(TOOLSET)) -shared $(GYP_LDFLAGS) $(LDFLAGS.$(TOOLSET)) -Wl,-soname=$(@F) -o $@ -Wl,--start-group $(filter-out FORCE_DO_CMD, $^) -Wl,--end-group $(LIBS)\nquiet_cmd_solink_module_host = SOLINK_MODULE($(TOOLSET)) $@\ncmd_solink_module_host = $(LINK.$(TOOLSET)) -shared $(GYP_LDFLAGS) $(LDFLAGS.$(TOOLSET)) -Wl,-soname=$(@F) -o $@ $(filter-out FORCE_DO_CMD, $^) $(LIBS)\n'
LINK_COMMANDS_AIX = 'quiet_cmd_alink = AR($(TOOLSET)) $@\ncmd_alink = rm -f $@ && $(AR.$(TOOLSET)) crs $@ $(filter %.o,$^)\n\nquiet_cmd_alink_thin = AR($(TOOLSET)) $@\ncmd_alink_thin = rm -f $@ && $(AR.$(TOOLSET)) crs $@ $(filter %.o,$^)\n\nquiet_cmd_link = LINK($(TOOLSET)) $@\ncmd_link = $(LINK.$(TOOLSET)) $(GYP_LDFLAGS) $(LDFLAGS.$(TOOLSET)) -o $@ $(LD_INPUTS) $(LIBS)\n\nquiet_cmd_solink = SOLINK($(TOOLSET)) $@\ncmd_solink = $(LINK.$(TOOLSET)) -shared $(GYP_LDFLAGS) $(LDFLAGS.$(TOOLSET)) -o $@ $(LD_INPUTS) $(LIBS)\n\nquiet_cmd_solink_module = SOLINK_MODULE($(TOOLSET)) $@\ncmd_solink_module = $(LINK.$(TOOLSET)) -shared $(GYP_LDFLAGS) $(LDFLAGS.$(TOOLSET)) -o $@ $(filter-out FORCE_DO_CMD, $^) $(LIBS)\n'
SHARED_HEADER = '# We borrow heavily from the kernel build setup, though we are simpler since\n# we don\'t have Kconfig tweaking settings on us.\n\n# The implicit make rules have it looking for RCS files, among other things.\n# We instead explicitly write all the rules we care about.\n# It\'s even quicker (saves ~200ms) to pass -r on the command line.\nMAKEFLAGS=-r\n\n# The source directory tree.\nsrcdir := %(srcdir)s\nabs_srcdir := $(abspath $(srcdir))\n\n# The name of the builddir.\nbuilddir_name ?= %(builddir)s\n\n# The V=1 flag on command line makes us verbosely print command lines.\nifdef V\n  quiet=\nelse\n  quiet=quiet_\nendif\n\n# Specify BUILDTYPE=Release on the command line for a release build.\nBUILDTYPE ?= %(default_configuration)s\n\n# Directory all our build output goes into.\n# Note that this must be two directories beneath src/ for unit tests to pass,\n# as they reach into the src/ directory for data with relative paths.\nbuilddir ?= $(builddir_name)/$(BUILDTYPE)\nabs_builddir := $(abspath $(builddir))\ndepsdir := $(builddir)/.deps\n\n# Object output directory.\nobj := $(builddir)/obj\nabs_obj := $(abspath $(obj))\n\n# We build up a list of every single one of the targets so we can slurp in the\n# generated dependency rule Makefiles in one pass.\nall_deps :=\n\n%(make_global_settings)s\n\nCC.target ?= %(CC.target)s\nCFLAGS.target ?= $(CFLAGS)\nCXX.target ?= %(CXX.target)s\nCXXFLAGS.target ?= $(CXXFLAGS)\nLINK.target ?= %(LINK.target)s\nLDFLAGS.target ?= $(LDFLAGS)\nAR.target ?= $(AR)\n\n# C++ apps need to be linked with g++.\n#\n# Note: flock is used to seralize linking. Linking is a memory-intensive\n# process so running parallel links can often lead to thrashing.  To disable\n# the serialization, override LINK via an envrionment variable as follows:\n#\n#   export LINK=g++\n#\n# This will allow make to invoke N linker processes as specified in -jN.\nLINK ?= %(flock)s $(builddir)/linker.lock $(CXX.target)\n\n# TODO(evan): move all cross-compilation logic to gyp-time so we don\'t need\n# to replicate this environment fallback in make as well.\nCC.host ?= %(CC.host)s\nCFLAGS.host ?=\nCXX.host ?= %(CXX.host)s\nCXXFLAGS.host ?=\nLINK.host ?= %(LINK.host)s\nLDFLAGS.host ?=\nAR.host ?= %(AR.host)s\n\n# Define a dir function that can handle spaces.\n# http://www.gnu.org/software/make/manual/make.html#Syntax-of-Functions\n# "leading spaces cannot appear in the text of the first argument as written.\n# These characters can be put into the argument value by variable substitution."\nempty :=\nspace := $(empty) $(empty)\n\n# http://stackoverflow.com/questions/1189781/using-make-dir-or-notdir-on-a-path-with-spaces\nreplace_spaces = $(subst $(space),' + SPACE_REPLACEMENT + ',$1)\nunreplace_spaces = $(subst ' + SPACE_REPLACEMENT + ',$(space),$1)\ndirx = $(call unreplace_spaces,$(dir $(call replace_spaces,$1)))\n\n# Flags to make gcc output dependency info.  Note that you need to be\n# careful here to use the flags that ccache and distcc can understand.\n# We write to a dep file on the side first and then rename at the end\n# so we can\'t end up with a broken dep file.\ndepfile = $(depsdir)/$(call replace_spaces,$@).d\nDEPFLAGS = -MMD -MF $(depfile).raw\n\n# We have to fixup the deps output in a few ways.\n# (1) the file output should mention the proper .o file.\n# ccache or distcc lose the path to the target, so we convert a rule of\n# the form:\n#   foobar.o: DEP1 DEP2\n# into\n#   path/to/foobar.o: DEP1 DEP2\n# (2) we want missing files not to cause us to fail to build.\n# We want to rewrite\n#   foobar.o: DEP1 DEP2 \\\n#               DEP3\n# to\n#   DEP1:\n#   DEP2:\n#   DEP3:\n# so if the files are missing, they\'re just considered phony rules.\n# We have to do some pretty insane escaping to get those backslashes\n# and dollar signs past make, the shell, and sed at the same time.\n# Doesn\'t work with spaces, but that\'s fine: .d files have spaces in\n# their names replaced with other characters.\ndefine fixup_dep\n# The depfile may not exist if the input file didn\'t have any #includes.\ntouch $(depfile).raw\n# Fixup path as in (1).\nsed -e "s|^$(notdir $@)|$@|" $(depfile).raw >> $(depfile)\n# Add extra rules as in (2).\n# We remove slashes and replace spaces with new lines;\n# remove blank lines;\n# delete the first line and append a colon to the remaining lines.\nsed -e \'s|\\\\||\' -e \'y| |\\n|\' $(depfile).raw |\\\n  grep -v \'^$$\'                             |\\\n  sed -e 1d -e \'s|$$|:|\'                     \\\n    >> $(depfile)\nrm $(depfile).raw\nendef\n\n# Command definitions:\n# - cmd_foo is the actual command to run;\n# - quiet_cmd_foo is the brief-output summary of the command.\n\nquiet_cmd_cc = CC($(TOOLSET)) $@\ncmd_cc = $(CC.$(TOOLSET)) $(GYP_CFLAGS) $(DEPFLAGS) $(CFLAGS.$(TOOLSET)) -c -o $@ $<\n\nquiet_cmd_cxx = CXX($(TOOLSET)) $@\ncmd_cxx = $(CXX.$(TOOLSET)) $(GYP_CXXFLAGS) $(DEPFLAGS) $(CXXFLAGS.$(TOOLSET)) -c -o $@ $<\n%(extra_commands)s\nquiet_cmd_touch = TOUCH $@\ncmd_touch = touch $@\n\nquiet_cmd_copy = COPY $@\n# send stderr to /dev/null to ignore messages when linking directories.\ncmd_copy = ln -f "$<" "$@" 2>/dev/null || (rm -rf "$@" && cp -af "$<" "$@")\n\n%(link_commands)s\n\n# Define an escape_quotes function to escape single quotes.\n# This allows us to handle quotes properly as long as we always use\n# use single quotes and escape_quotes.\nescape_quotes = $(subst \',\'\\\'\',$(1))\n# This comment is here just to include a \' to unconfuse syntax highlighting.\n# Define an escape_vars function to escape \'$\' variable syntax.\n# This allows us to read/write command lines with shell variables (e.g.\n# $LD_LIBRARY_PATH), without triggering make substitution.\nescape_vars = $(subst $$,$$$$,$(1))\n# Helper that expands to a shell command to echo a string exactly as it is in\n# make. This uses printf instead of echo because printf\'s behaviour with respect\n# to escape sequences is more portable than echo\'s across different shells\n# (e.g., dash, bash).\nexact_echo = printf \'%%s\\n\' \'$(call escape_quotes,$(1))\'\n\n# Helper to compare the command we\'re about to run against the command\n# we logged the last time we ran the command.  Produces an empty\n# string (false) when the commands match.\n# Tricky point: Make has no string-equality test function.\n# The kernel uses the following, but it seems like it would have false\n# positives, where one string reordered its arguments.\n#   arg_check = $(strip $(filter-out $(cmd_$(1)), $(cmd_$@)) \\\n#                       $(filter-out $(cmd_$@), $(cmd_$(1))))\n# We instead substitute each for the empty string into the other, and\n# say they\'re equal if both substitutions produce the empty string.\n# .d files contain ' + SPACE_REPLACEMENT + ' instead of spaces, take that into account.\ncommand_changed = $(or $(subst $(cmd_$(1)),,$(cmd_$(call replace_spaces,$@))),\\\n                       $(subst $(cmd_$(call replace_spaces,$@)),,$(cmd_$(1))))\n\n# Helper that is non-empty when a prerequisite changes.\n# Normally make does this implicitly, but we force rules to always run\n# so we can check their command lines.\n#   $? -- new prerequisites\n#   $| -- order-only dependencies\nprereq_changed = $(filter-out FORCE_DO_CMD,$(filter-out $|,$?))\n\n# Helper that executes all postbuilds until one fails.\ndefine do_postbuilds\n  @E=0;\\\n  for p in $(POSTBUILDS); do\\\n    eval $$p;\\\n    E=$$?;\\\n    if [ $$E -ne 0 ]; then\\\n      break;\\\n    fi;\\\n  done;\\\n  if [ $$E -ne 0 ]; then\\\n    rm -rf "$@";\\\n    exit $$E;\\\n  fi\nendef\n\n# do_cmd: run a command via the above cmd_foo names, if necessary.\n# Should always run for a given target to handle command-line changes.\n# Second argument, if non-zero, makes it do asm/C/C++ dependency munging.\n# Third argument, if non-zero, makes it do POSTBUILDS processing.\n# Note: We intentionally do NOT call dirx for depfile, since it contains ' + SPACE_REPLACEMENT + ' for\n# spaces already and dirx strips the ' + SPACE_REPLACEMENT + ' characters.\ndefine do_cmd\n$(if $(or $(command_changed),$(prereq_changed)),\n  @$(call exact_echo,  $($(quiet)cmd_$(1)))\n  @mkdir -p "$(call dirx,$@)" "$(dir $(depfile))"\n  $(if $(findstring flock,$(word %(flock_index)d,$(cmd_$1))),\n    @$(cmd_$(1))\n    @echo "  $(quiet_cmd_$(1)): Finished",\n    @$(cmd_$(1))\n  )\n  @$(call exact_echo,$(call escape_vars,cmd_$(call replace_spaces,$@) := $(cmd_$(1)))) > $(depfile)\n  @$(if $(2),$(fixup_dep))\n  $(if $(and $(3), $(POSTBUILDS)),\n    $(call do_postbuilds)\n  )\n)\nendef\n\n# Declare the "%(default_target)s" target first so it is the default,\n# even though we don\'t have the deps yet.\n.PHONY: %(default_target)s\n%(default_target)s:\n\n# make looks for ways to re-generate included makefiles, but in our case, we\n# don\'t have a direct way. Explicitly telling make that it has nothing to do\n# for them makes it go faster.\n%%.d: ;\n\n# Use FORCE_DO_CMD to force a target to run.  Should be coupled with\n# do_cmd.\n.PHONY: FORCE_DO_CMD\nFORCE_DO_CMD:\n\n'
SHARED_HEADER_MAC_COMMANDS = '\nquiet_cmd_objc = CXX($(TOOLSET)) $@\ncmd_objc = $(CC.$(TOOLSET)) $(GYP_OBJCFLAGS) $(DEPFLAGS) -c -o $@ $<\n\nquiet_cmd_objcxx = CXX($(TOOLSET)) $@\ncmd_objcxx = $(CXX.$(TOOLSET)) $(GYP_OBJCXXFLAGS) $(DEPFLAGS) -c -o $@ $<\n\n# Commands for precompiled header files.\nquiet_cmd_pch_c = CXX($(TOOLSET)) $@\ncmd_pch_c = $(CC.$(TOOLSET)) $(GYP_PCH_CFLAGS) $(DEPFLAGS) $(CXXFLAGS.$(TOOLSET)) -c -o $@ $<\nquiet_cmd_pch_cc = CXX($(TOOLSET)) $@\ncmd_pch_cc = $(CC.$(TOOLSET)) $(GYP_PCH_CXXFLAGS) $(DEPFLAGS) $(CXXFLAGS.$(TOOLSET)) -c -o $@ $<\nquiet_cmd_pch_m = CXX($(TOOLSET)) $@\ncmd_pch_m = $(CC.$(TOOLSET)) $(GYP_PCH_OBJCFLAGS) $(DEPFLAGS) -c -o $@ $<\nquiet_cmd_pch_mm = CXX($(TOOLSET)) $@\ncmd_pch_mm = $(CC.$(TOOLSET)) $(GYP_PCH_OBJCXXFLAGS) $(DEPFLAGS) -c -o $@ $<\n\n# gyp-mac-tool is written next to the root Makefile by gyp.\n# Use $(4) for the command, since $(2) and $(3) are used as flag by do_cmd\n# already.\nquiet_cmd_mac_tool = MACTOOL $(4) $<\ncmd_mac_tool = ./gyp-mac-tool $(4) $< "$@"\n\nquiet_cmd_mac_package_framework = PACKAGE FRAMEWORK $@\ncmd_mac_package_framework = ./gyp-mac-tool package-framework "$@" $(4)\n\nquiet_cmd_infoplist = INFOPLIST $@\ncmd_infoplist = $(CC.$(TOOLSET)) -E -P -Wno-trigraphs -x c $(INFOPLIST_DEFINES) "$<" -o "$@"\n'

def WriteRootHeaderSuffixRules(writer):
    extensions = sorted(COMPILABLE_EXTENSIONS.keys(), key=str.lower)
    writer.write('# Suffix rules, putting all outputs into $(obj).\n')
    for ext in extensions:
        writer.write('$(obj).$(TOOLSET)/%%.o: $(srcdir)/%%%s FORCE_DO_CMD\n' % ext)
        writer.write('\t@$(call do_cmd,%s,1)\n' % COMPILABLE_EXTENSIONS[ext])

    writer.write('\n# Try building from generated source, too.\n')
    for ext in extensions:
        writer.write('$(obj).$(TOOLSET)/%%.o: $(obj).$(TOOLSET)/%%%s FORCE_DO_CMD\n' % ext)
        writer.write('\t@$(call do_cmd,%s,1)\n' % COMPILABLE_EXTENSIONS[ext])

    writer.write('\n')
    for ext in extensions:
        writer.write('$(obj).$(TOOLSET)/%%.o: $(obj)/%%%s FORCE_DO_CMD\n' % ext)
        writer.write('\t@$(call do_cmd,%s,1)\n' % COMPILABLE_EXTENSIONS[ext])

    writer.write('\n')


SHARED_HEADER_SUFFIX_RULES_COMMENT1 = '# Suffix rules, putting all outputs into $(obj).\n'
SHARED_HEADER_SUFFIX_RULES_COMMENT2 = '# Try building from generated source, too.\n'
SHARED_FOOTER = '# "all" is a concatenation of the "all" targets from all the included\n# sub-makefiles. This is just here to clarify.\nall:\n\n# Add in dependency-tracking rules.  $(all_deps) is the list of every single\n# target in our tree. Only consider the ones with .d (dependency) info:\nd_files := $(wildcard $(foreach f,$(all_deps),$(depsdir)/$(f).d))\nifneq ($(d_files),)\n  include $(d_files)\nendif\n'
header = '# This file is generated by gyp; do not edit.\n\n'
COMPILABLE_EXTENSIONS = {'.c': 'cc', 
   '.cc': 'cxx', 
   '.cpp': 'cxx', 
   '.cxx': 'cxx', 
   '.s': 'cc', 
   '.S': 'cc'}

def Compilable(filename):
    """Return true if the file is compilable (should be in OBJS)."""
    for res in (filename.endswith(e) for e in COMPILABLE_EXTENSIONS):
        if res:
            return True

    return False


def Linkable(filename):
    """Return true if the file is linkable (should be on the link line)."""
    return filename.endswith('.o')


def Target(filename):
    """Translate a compilable filename to its .o target."""
    return os.path.splitext(filename)[0] + '.o'


def EscapeShellArgument(s):
    """Quotes an argument so that it will be interpreted literally by a POSIX
     shell. Taken from
     http://stackoverflow.com/questions/35817/whats-the-best-way-to-escape-ossystem-calls-in-python
     """
    return "'" + s.replace("'", "'\\''") + "'"


def EscapeMakeVariableExpansion(s):
    """Make has its own variable expansion syntax using $. We must escape it for
     string to be interpreted literally."""
    return s.replace('$', '$$')


def EscapeCppDefine(s):
    """Escapes a CPP define so that it will reach the compiler unaltered."""
    s = EscapeShellArgument(s)
    s = EscapeMakeVariableExpansion(s)
    return s.replace('#', '\\#')


def QuoteIfNecessary(string):
    """TODO: Should this ideally be replaced with one or more of the above
     functions?"""
    if '"' in string:
        string = '"' + string.replace('"', '\\"') + '"'
    return string


def StringToMakefileVariable(string):
    """Convert a string to a value that is acceptable as a make variable name."""
    return re.sub('[^a-zA-Z0-9_]', '_', string)


srcdir_prefix = ''

def Sourceify(path):
    """Convert a path to its source directory form."""
    global srcdir_prefix
    if '$(' in path:
        return path
    if os.path.isabs(path):
        return path
    return srcdir_prefix + path


def QuoteSpaces(s, quote='\\ '):
    return s.replace(' ', quote)


target_outputs = {}
target_link_deps = {}

class MakefileWriter():
    """MakefileWriter packages up the writing of one target-specific foobar.mk.

  Its only real entry point is Write(), and is mostly used for namespacing.
  """

    def __init__(self, generator_flags, flavor):
        self.generator_flags = generator_flags
        self.flavor = flavor
        self.suffix_rules_srcdir = {}
        self.suffix_rules_objdir1 = {}
        self.suffix_rules_objdir2 = {}
        for ext in COMPILABLE_EXTENSIONS.keys():
            self.suffix_rules_srcdir.update({ext: '$(obj).$(TOOLSET)/$(TARGET)/%%.o: $(srcdir)/%%%s FORCE_DO_CMD\n\t@$(call do_cmd,%s,1)\n' % (ext, COMPILABLE_EXTENSIONS[ext])})
            self.suffix_rules_objdir1.update({ext: '$(obj).$(TOOLSET)/$(TARGET)/%%.o: $(obj).$(TOOLSET)/%%%s FORCE_DO_CMD\n\t@$(call do_cmd,%s,1)\n' % (ext, COMPILABLE_EXTENSIONS[ext])})
            self.suffix_rules_objdir2.update({ext: '$(obj).$(TOOLSET)/$(TARGET)/%%.o: $(obj)/%%%s FORCE_DO_CMD\n\t@$(call do_cmd,%s,1)\n' % (ext, COMPILABLE_EXTENSIONS[ext])})

    def Write(self, qualified_target, base_path, output_filename, spec, configs, part_of_all):
        """The main entry point: writes a .mk file for a single target.

    Arguments:
      qualified_target: target we're generating
      base_path: path relative to source root we're building in, used to resolve
                 target-relative paths
      output_filename: output .mk file name to write
      spec, configs: gyp info
      part_of_all: flag indicating this target is part of 'all'
    """
        gyp.common.EnsureDirExists(output_filename)
        self.fp = open(output_filename, 'w')
        self.fp.write(header)
        self.qualified_target = qualified_target
        self.path = base_path
        self.target = spec['target_name']
        self.type = spec['type']
        self.toolset = spec['toolset']
        self.is_mac_bundle = gyp.xcode_emulation.IsMacBundle(self.flavor, spec)
        if self.flavor == 'mac':
            self.xcode_settings = gyp.xcode_emulation.XcodeSettings(spec)
        else:
            self.xcode_settings = None
        deps, link_deps = self.ComputeDeps(spec)
        extra_outputs = []
        extra_sources = []
        extra_link_deps = []
        extra_mac_bundle_resources = []
        mac_bundle_deps = []
        if self.is_mac_bundle:
            self.output = self.ComputeMacBundleOutput(spec)
            self.output_binary = self.ComputeMacBundleBinaryOutput(spec)
        else:
            self.output = self.output_binary = self.ComputeOutput(spec)
        self.is_standalone_static_library = bool(spec.get('standalone_static_library', 0))
        self._INSTALLABLE_TARGETS = ('executable', 'loadable_module', 'shared_library')
        if self.is_standalone_static_library or self.type in self._INSTALLABLE_TARGETS:
            self.alias = os.path.basename(self.output)
            install_path = self._InstallableTargetInstallPath()
        else:
            self.alias = self.output
            install_path = self.output
        self.WriteLn('TOOLSET := ' + self.toolset)
        self.WriteLn('TARGET := ' + self.target)
        if 'actions' in spec:
            self.WriteActions(spec['actions'], extra_sources, extra_outputs, extra_mac_bundle_resources, part_of_all)
        if 'rules' in spec:
            self.WriteRules(spec['rules'], extra_sources, extra_outputs, extra_mac_bundle_resources, part_of_all)
        if 'copies' in spec:
            self.WriteCopies(spec['copies'], extra_outputs, part_of_all)
        if self.is_mac_bundle:
            all_mac_bundle_resources = spec.get('mac_bundle_resources', []) + extra_mac_bundle_resources
            self.WriteMacBundleResources(all_mac_bundle_resources, mac_bundle_deps)
            self.WriteMacInfoPlist(mac_bundle_deps)
        all_sources = spec.get('sources', []) + extra_sources
        if all_sources:
            self.WriteSources(configs, deps, all_sources, extra_outputs, extra_link_deps, part_of_all, gyp.xcode_emulation.MacPrefixHeader(self.xcode_settings, lambda p: Sourceify(self.Absolutify(p)), self.Pchify))
            sources = filter(Compilable, all_sources)
            if sources:
                self.WriteLn(SHARED_HEADER_SUFFIX_RULES_COMMENT1)
                extensions = set([ os.path.splitext(s)[1] for s in sources ])
                for ext in extensions:
                    if ext in self.suffix_rules_srcdir:
                        self.WriteLn(self.suffix_rules_srcdir[ext])

                self.WriteLn(SHARED_HEADER_SUFFIX_RULES_COMMENT2)
                for ext in extensions:
                    if ext in self.suffix_rules_objdir1:
                        self.WriteLn(self.suffix_rules_objdir1[ext])

                for ext in extensions:
                    if ext in self.suffix_rules_objdir2:
                        self.WriteLn(self.suffix_rules_objdir2[ext])

                self.WriteLn('# End of this set of suffix rules')
                if self.is_mac_bundle:
                    mac_bundle_deps.append(self.output_binary)
        self.WriteTarget(spec, configs, deps, extra_link_deps + link_deps, mac_bundle_deps, extra_outputs, part_of_all)
        target_outputs[qualified_target] = install_path
        if self.type in ('static_library', 'shared_library'):
            target_link_deps[qualified_target] = self.output_binary
        if self.generator_flags.get('android_ndk_version', None):
            self.WriteAndroidNdkModuleRule(self.target, all_sources, link_deps)
        self.fp.close()
        return

    def WriteSubMake(self, output_filename, makefile_path, targets, build_dir):
        """Write a "sub-project" Makefile.

    This is a small, wrapper Makefile that calls the top-level Makefile to build
    the targets from a single gyp file (i.e. a sub-project).

    Arguments:
      output_filename: sub-project Makefile name to write
      makefile_path: path to the top-level Makefile
      targets: list of "all" targets for this sub-project
      build_dir: build output directory, relative to the sub-project
    """
        gyp.common.EnsureDirExists(output_filename)
        self.fp = open(output_filename, 'w')
        self.fp.write(header)
        self.WriteLn('export builddir_name ?= %s' % os.path.join(os.path.dirname(output_filename), build_dir))
        self.WriteLn('.PHONY: all')
        self.WriteLn('all:')
        if makefile_path:
            makefile_path = ' -C ' + makefile_path
        self.WriteLn('\t$(MAKE)%s %s' % (makefile_path, (' ').join(targets)))
        self.fp.close()

    def WriteActions(self, actions, extra_sources, extra_outputs, extra_mac_bundle_resources, part_of_all):
        """Write Makefile code for any 'actions' from the gyp input.

    extra_sources: a list that will be filled in with newly generated source
                   files, if any
    extra_outputs: a list that will be filled in with any outputs of these
                   actions (used to make other pieces dependent on these
                   actions)
    part_of_all: flag indicating this target is part of 'all'
    """
        env = self.GetSortedXcodeEnv()
        for action in actions:
            name = StringToMakefileVariable('%s_%s' % (self.qualified_target,
             action['action_name']))
            self.WriteLn('### Rules for action "%s":' % action['action_name'])
            inputs = action['inputs']
            outputs = action['outputs']
            dirs = set()
            for out in outputs:
                dir = os.path.split(out)[0]
                if dir:
                    dirs.add(dir)

            if int(action.get('process_outputs_as_sources', False)):
                extra_sources += outputs
            if int(action.get('process_outputs_as_mac_bundle_resources', False)):
                extra_mac_bundle_resources += outputs
            action_commands = action['action']
            if self.flavor == 'mac':
                action_commands = [ gyp.xcode_emulation.ExpandEnvVars(command, env) for command in action_commands ]
            command = gyp.common.EncodePOSIXShellList(action_commands)
            if 'message' in action:
                self.WriteLn('quiet_cmd_%s = ACTION %s $@' % (name, action['message']))
            else:
                self.WriteLn('quiet_cmd_%s = ACTION %s $@' % (name, name))
            if len(dirs) > 0:
                command = 'mkdir -p %s' % (' ').join(dirs) + '; ' + command
            cd_action = 'cd %s; ' % Sourceify(self.path or '.')
            command = command.replace('$(TARGET)', self.target)
            cd_action = cd_action.replace('$(TARGET)', self.target)
            self.WriteLn('cmd_%s = LD_LIBRARY_PATH=$(builddir)/lib.host:$(builddir)/lib.target:$$LD_LIBRARY_PATH; export LD_LIBRARY_PATH; %s%s' % (
             name, cd_action, command))
            self.WriteLn()
            outputs = map(self.Absolutify, outputs)
            self.WriteLn('%s: obj := $(abs_obj)' % QuoteSpaces(outputs[0]))
            self.WriteLn('%s: builddir := $(abs_builddir)' % QuoteSpaces(outputs[0]))
            self.WriteSortedXcodeEnv(outputs[0], self.GetSortedXcodeEnv())
            for input in inputs:
                assert ' ' not in input, 'Spaces in action input filenames not supported (%s)' % input

            for output in outputs:
                assert ' ' not in output, 'Spaces in action output filenames not supported (%s)' % output

            outputs = [ gyp.xcode_emulation.ExpandEnvVars(o, env) for o in outputs ]
            inputs = [ gyp.xcode_emulation.ExpandEnvVars(i, env) for i in inputs ]
            self.WriteDoCmd(outputs, map(Sourceify, map(self.Absolutify, inputs)), part_of_all=part_of_all, command=name)
            outputs_variable = 'action_%s_outputs' % name
            self.WriteLn('%s := %s' % (outputs_variable, (' ').join(outputs)))
            extra_outputs.append('$(%s)' % outputs_variable)
            self.WriteLn()

        self.WriteLn()

    def WriteRules(self, rules, extra_sources, extra_outputs, extra_mac_bundle_resources, part_of_all):
        """Write Makefile code for any 'rules' from the gyp input.

    extra_sources: a list that will be filled in with newly generated source
                   files, if any
    extra_outputs: a list that will be filled in with any outputs of these
                   rules (used to make other pieces dependent on these rules)
    part_of_all: flag indicating this target is part of 'all'
    """
        env = self.GetSortedXcodeEnv()
        for rule in rules:
            name = StringToMakefileVariable('%s_%s' % (self.qualified_target,
             rule['rule_name']))
            count = 0
            self.WriteLn('### Generated for rule %s:' % name)
            all_outputs = []
            for rule_source in rule.get('rule_sources', []):
                dirs = set()
                rule_source_dirname, rule_source_basename = os.path.split(rule_source)
                rule_source_root, rule_source_ext = os.path.splitext(rule_source_basename)
                outputs = [ self.ExpandInputRoot(out, rule_source_root, rule_source_dirname) for out in rule['outputs']
                          ]
                for out in outputs:
                    dir = os.path.dirname(out)
                    if dir:
                        dirs.add(dir)

                if int(rule.get('process_outputs_as_sources', False)):
                    extra_sources += outputs
                if int(rule.get('process_outputs_as_mac_bundle_resources', False)):
                    extra_mac_bundle_resources += outputs
                inputs = map(Sourceify, map(self.Absolutify, [rule_source] + rule.get('inputs', [])))
                actions = ['$(call do_cmd,%s_%d)' % (name, count)]
                if name == 'resources_grit':
                    actions += ['@touch --no-create $@']
                outputs = [ gyp.xcode_emulation.ExpandEnvVars(o, env) for o in outputs ]
                inputs = [ gyp.xcode_emulation.ExpandEnvVars(i, env) for i in inputs ]
                outputs = map(self.Absolutify, outputs)
                all_outputs += outputs
                self.WriteLn('%s: obj := $(abs_obj)' % outputs[0])
                self.WriteLn('%s: builddir := $(abs_builddir)' % outputs[0])
                self.WriteMakeRule(outputs, inputs + ['FORCE_DO_CMD'], actions)
                variables_with_spaces = re.compile('\\$\\([^ ]* \\$<\\)')
                for output in outputs:
                    output = re.sub(variables_with_spaces, '', output)
                    assert ' ' not in output, 'Spaces in rule filenames not yet supported (%s)' % output

                self.WriteLn('all_deps += %s' % (' ').join(outputs))
                action = [ self.ExpandInputRoot(ac, rule_source_root, rule_source_dirname) for ac in rule['action']
                         ]
                mkdirs = ''
                if len(dirs) > 0:
                    mkdirs = 'mkdir -p %s; ' % (' ').join(dirs)
                cd_action = 'cd %s; ' % Sourceify(self.path or '.')
                if self.flavor == 'mac':
                    action = [ gyp.xcode_emulation.ExpandEnvVars(command, env) for command in action ]
                action = gyp.common.EncodePOSIXShellList(action)
                action = action.replace('$(TARGET)', self.target)
                cd_action = cd_action.replace('$(TARGET)', self.target)
                mkdirs = mkdirs.replace('$(TARGET)', self.target)
                self.WriteLn('cmd_%(name)s_%(count)d = LD_LIBRARY_PATH=$(builddir)/lib.host:$(builddir)/lib.target:$$LD_LIBRARY_PATH; export LD_LIBRARY_PATH; %(cd_action)s%(mkdirs)s%(action)s' % {'action': action, 
                   'cd_action': cd_action, 
                   'count': count, 
                   'mkdirs': mkdirs, 
                   'name': name})
                self.WriteLn('quiet_cmd_%(name)s_%(count)d = RULE %(name)s_%(count)d $@' % {'count': count, 
                   'name': name})
                self.WriteLn()
                count += 1

            outputs_variable = 'rule_%s_outputs' % name
            self.WriteList(all_outputs, outputs_variable)
            extra_outputs.append('$(%s)' % outputs_variable)
            self.WriteLn('### Finished generating for rule: %s' % name)
            self.WriteLn()

        self.WriteLn('### Finished generating for all rules')
        self.WriteLn('')

    def WriteCopies(self, copies, extra_outputs, part_of_all):
        """Write Makefile code for any 'copies' from the gyp input.

    extra_outputs: a list that will be filled in with any outputs of this action
                   (used to make other pieces dependent on this action)
    part_of_all: flag indicating this target is part of 'all'
    """
        self.WriteLn('### Generated for copy rule.')
        variable = StringToMakefileVariable(self.qualified_target + '_copies')
        outputs = []
        for copy in copies:
            for path in copy['files']:
                path = Sourceify(self.Absolutify(path))
                filename = os.path.split(path)[1]
                output = Sourceify(self.Absolutify(os.path.join(copy['destination'], filename)))
                env = self.GetSortedXcodeEnv()
                output = gyp.xcode_emulation.ExpandEnvVars(output, env)
                path = gyp.xcode_emulation.ExpandEnvVars(path, env)
                self.WriteDoCmd([output], [path], 'copy', part_of_all)
                outputs.append(output)

        self.WriteLn('%s = %s' % (variable, (' ').join(map(QuoteSpaces, outputs))))
        extra_outputs.append('$(%s)' % variable)
        self.WriteLn()

    def WriteMacBundleResources(self, resources, bundle_deps):
        """Writes Makefile code for 'mac_bundle_resources'."""
        self.WriteLn('### Generated for mac_bundle_resources')
        for output, res in gyp.xcode_emulation.GetMacBundleResources(generator_default_variables['PRODUCT_DIR'], self.xcode_settings, map(Sourceify, map(self.Absolutify, resources))):
            self.WriteDoCmd([output], [res], 'mac_tool,,,copy-bundle-resource', part_of_all=True)
            bundle_deps.append(output)

    def WriteMacInfoPlist(self, bundle_deps):
        """Write Makefile code for bundle Info.plist files."""
        info_plist, out, defines, extra_env = gyp.xcode_emulation.GetMacInfoPlist(generator_default_variables['PRODUCT_DIR'], self.xcode_settings, lambda p: Sourceify(self.Absolutify(p)))
        if not info_plist:
            return
        if defines:
            intermediate_plist = '$(obj).$(TOOLSET)/$(TARGET)/' + os.path.basename(info_plist)
            self.WriteList(defines, intermediate_plist + ': INFOPLIST_DEFINES', '-D', quoter=EscapeCppDefine)
            self.WriteMakeRule([intermediate_plist], [info_plist], [
             '$(call do_cmd,infoplist)',
             '@plutil -convert xml1 $@ $@'])
            info_plist = intermediate_plist
        self.WriteSortedXcodeEnv(out, self.GetSortedXcodeEnv(additional_settings=extra_env))
        self.WriteDoCmd([out], [info_plist], 'mac_tool,,,copy-info-plist', part_of_all=True)
        bundle_deps.append(out)

    def WriteSources(self, configs, deps, sources, extra_outputs, extra_link_deps, part_of_all, precompiled_header):
        """Write Makefile code for any 'sources' from the gyp input.
    These are source files necessary to build the current target.

    configs, deps, sources: input from gyp.
    extra_outputs: a list of extra outputs this action should be dependent on;
                   used to serialize action/rules before compilation
    extra_link_deps: a list that will be filled in with any outputs of
                     compilation (to be used in link lines)
    part_of_all: flag indicating this target is part of 'all'
    """
        for configname in sorted(configs.keys()):
            config = configs[configname]
            self.WriteList(config.get('defines'), 'DEFS_%s' % configname, prefix='-D', quoter=EscapeCppDefine)
            if self.flavor == 'mac':
                cflags = self.xcode_settings.GetCflags(configname)
                cflags_c = self.xcode_settings.GetCflagsC(configname)
                cflags_cc = self.xcode_settings.GetCflagsCC(configname)
                cflags_objc = self.xcode_settings.GetCflagsObjC(configname)
                cflags_objcc = self.xcode_settings.GetCflagsObjCC(configname)
            else:
                cflags = config.get('cflags')
                cflags_c = config.get('cflags_c')
                cflags_cc = config.get('cflags_cc')
            self.WriteLn('# Flags passed to all source files.')
            self.WriteList(cflags, 'CFLAGS_%s' % configname)
            self.WriteLn('# Flags passed to only C files.')
            self.WriteList(cflags_c, 'CFLAGS_C_%s' % configname)
            self.WriteLn('# Flags passed to only C++ files.')
            self.WriteList(cflags_cc, 'CFLAGS_CC_%s' % configname)
            if self.flavor == 'mac':
                self.WriteLn('# Flags passed to only ObjC files.')
                self.WriteList(cflags_objc, 'CFLAGS_OBJC_%s' % configname)
                self.WriteLn('# Flags passed to only ObjC++ files.')
                self.WriteList(cflags_objcc, 'CFLAGS_OBJCC_%s' % configname)
            includes = config.get('include_dirs')
            if includes:
                includes = map(Sourceify, map(self.Absolutify, includes))
            self.WriteList(includes, 'INCS_%s' % configname, prefix='-I')

        compilable = filter(Compilable, sources)
        objs = map(self.Objectify, map(self.Absolutify, map(Target, compilable)))
        self.WriteList(objs, 'OBJS')
        for obj in objs:
            assert ' ' not in obj, 'Spaces in object filenames not supported (%s)' % obj

        self.WriteLn('# Add to the list of files we specially track dependencies for.')
        self.WriteLn('all_deps += $(OBJS)')
        self.WriteLn()
        if deps:
            self.WriteMakeRule(['$(OBJS)'], deps, comment='Make sure our dependencies are built before any of us.', order_only=True)
        if extra_outputs:
            self.WriteMakeRule(['$(OBJS)'], extra_outputs, comment='Make sure our actions/rules run before any of us.', order_only=True)
        pchdeps = precompiled_header.GetObjDependencies(compilable, objs)
        if pchdeps:
            self.WriteLn('# Dependencies from obj files to their precompiled headers')
            for source, obj, gch in pchdeps:
                self.WriteLn('%s: %s' % (obj, gch))

            self.WriteLn('# End precompiled header dependencies')
        if objs:
            extra_link_deps.append('$(OBJS)')
            self.WriteLn('# CFLAGS et al overrides must be target-local.\n# See "Target-specific Variable Values" in the GNU Make manual.')
            self.WriteLn('$(OBJS): TOOLSET := $(TOOLSET)')
            self.WriteLn('$(OBJS): GYP_CFLAGS := $(DEFS_$(BUILDTYPE)) $(INCS_$(BUILDTYPE)) %s ' % precompiled_header.GetInclude('c') + '$(CFLAGS_$(BUILDTYPE)) $(CFLAGS_C_$(BUILDTYPE))')
            self.WriteLn('$(OBJS): GYP_CXXFLAGS := $(DEFS_$(BUILDTYPE)) $(INCS_$(BUILDTYPE)) %s ' % precompiled_header.GetInclude('cc') + '$(CFLAGS_$(BUILDTYPE)) $(CFLAGS_CC_$(BUILDTYPE))')
            if self.flavor == 'mac':
                self.WriteLn('$(OBJS): GYP_OBJCFLAGS := $(DEFS_$(BUILDTYPE)) $(INCS_$(BUILDTYPE)) %s ' % precompiled_header.GetInclude('m') + '$(CFLAGS_$(BUILDTYPE)) $(CFLAGS_C_$(BUILDTYPE)) $(CFLAGS_OBJC_$(BUILDTYPE))')
                self.WriteLn('$(OBJS): GYP_OBJCXXFLAGS := $(DEFS_$(BUILDTYPE)) $(INCS_$(BUILDTYPE)) %s ' % precompiled_header.GetInclude('mm') + '$(CFLAGS_$(BUILDTYPE)) $(CFLAGS_CC_$(BUILDTYPE)) $(CFLAGS_OBJCC_$(BUILDTYPE))')
        self.WritePchTargets(precompiled_header.GetPchBuildCommands())
        extra_link_deps += filter(Linkable, sources)
        self.WriteLn()

    def WritePchTargets(self, pch_commands):
        """Writes make rules to compile prefix headers."""
        if not pch_commands:
            return
        for gch, lang_flag, lang, input in pch_commands:
            extra_flags = {'c': '$(CFLAGS_C_$(BUILDTYPE))', 'cc': '$(CFLAGS_CC_$(BUILDTYPE))', 
               'm': '$(CFLAGS_C_$(BUILDTYPE)) $(CFLAGS_OBJC_$(BUILDTYPE))', 
               'mm': '$(CFLAGS_CC_$(BUILDTYPE)) $(CFLAGS_OBJCC_$(BUILDTYPE))'}[lang]
            var_name = {'c': 'GYP_PCH_CFLAGS', 
               'cc': 'GYP_PCH_CXXFLAGS', 
               'm': 'GYP_PCH_OBJCFLAGS', 
               'mm': 'GYP_PCH_OBJCXXFLAGS'}[lang]
            self.WriteLn('%s: %s := %s ' % (gch, var_name, lang_flag) + '$(DEFS_$(BUILDTYPE)) $(INCS_$(BUILDTYPE)) $(CFLAGS_$(BUILDTYPE)) ' + extra_flags)
            self.WriteLn('%s: %s FORCE_DO_CMD' % (gch, input))
            self.WriteLn('\t@$(call do_cmd,pch_%s,1)' % lang)
            self.WriteLn('')
            assert ' ' not in gch, 'Spaces in gch filenames not supported (%s)' % gch
            self.WriteLn('all_deps += %s' % gch)
            self.WriteLn('')

    def ComputeOutputBasename(self, spec):
        """Return the 'output basename' of a gyp spec.

    E.g., the loadable module 'foobar' in directory 'baz' will produce
      'libfoobar.so'
    """
        assert not self.is_mac_bundle
        if self.flavor == 'mac' and self.type in ('static_library', 'executable', 'shared_library',
                                                  'loadable_module'):
            return self.xcode_settings.GetExecutablePath()
        target = spec['target_name']
        target_prefix = ''
        target_ext = ''
        if self.type == 'static_library':
            if target[:3] == 'lib':
                target = target[3:]
            target_prefix = 'lib'
            target_ext = '.a'
        elif self.type in ('loadable_module', 'shared_library'):
            if target[:3] == 'lib':
                target = target[3:]
            target_prefix = 'lib'
            target_ext = '.so'
        elif self.type == 'none':
            target = '%s.stamp' % target
        elif self.type != 'executable':
            print (
             'ERROR: What output file should be generated?',
             'type', self.type, 'target', target)
        target_prefix = spec.get('product_prefix', target_prefix)
        target = spec.get('product_name', target)
        product_ext = spec.get('product_extension')
        if product_ext:
            target_ext = '.' + product_ext
        return target_prefix + target + target_ext

    def _InstallImmediately(self):
        return self.toolset == 'target' and self.flavor == 'mac' and self.type in ('static_library',
                                                                                   'executable',
                                                                                   'shared_library',
                                                                                   'loadable_module')

    def ComputeOutput(self, spec):
        """Return the 'output' (full output path) of a gyp spec.

    E.g., the loadable module 'foobar' in directory 'baz' will produce
      '$(obj)/baz/libfoobar.so'
    """
        assert not self.is_mac_bundle
        path = os.path.join('$(obj).' + self.toolset, self.path)
        if self.type == 'executable' or self._InstallImmediately():
            path = '$(builddir)'
        path = spec.get('product_dir', path)
        return os.path.join(path, self.ComputeOutputBasename(spec))

    def ComputeMacBundleOutput(self, spec):
        """Return the 'output' (full output path) to a bundle output directory."""
        assert self.is_mac_bundle
        path = generator_default_variables['PRODUCT_DIR']
        return os.path.join(path, self.xcode_settings.GetWrapperName())

    def ComputeMacBundleBinaryOutput(self, spec):
        """Return the 'output' (full output path) to the binary in a bundle."""
        path = generator_default_variables['PRODUCT_DIR']
        return os.path.join(path, self.xcode_settings.GetExecutablePath())

    def ComputeDeps(self, spec):
        """Compute the dependencies of a gyp spec.

    Returns a tuple (deps, link_deps), where each is a list of
    filenames that will need to be put in front of make for either
    building (deps) or linking (link_deps).
    """
        deps = []
        link_deps = []
        if 'dependencies' in spec:
            deps.extend([ target_outputs[dep] for dep in spec['dependencies'] if target_outputs[dep]
                        ])
            for dep in spec['dependencies']:
                if dep in target_link_deps:
                    link_deps.append(target_link_deps[dep])

            deps.extend(link_deps)
        return (
         gyp.common.uniquer(deps), gyp.common.uniquer(link_deps))

    def WriteDependencyOnExtraOutputs(self, target, extra_outputs):
        self.WriteMakeRule([self.output_binary], extra_outputs, comment='Build our special outputs first.', order_only=True)

    def WriteTarget(self, spec, configs, deps, link_deps, bundle_deps, extra_outputs, part_of_all):
        """Write Makefile code to produce the final target of the gyp spec.

    spec, configs: input from gyp.
    deps, link_deps: dependency lists; see ComputeDeps()
    extra_outputs: any extra outputs that our target should depend on
    part_of_all: flag indicating this target is part of 'all'
    """
        self.WriteLn('### Rules for final target.')
        if extra_outputs:
            self.WriteDependencyOnExtraOutputs(self.output_binary, extra_outputs)
            self.WriteMakeRule(extra_outputs, deps, comment='Preserve order dependency of special output on deps.', order_only=True)
        target_postbuilds = {}
        if self.type != 'none':
            for configname in sorted(configs.keys()):
                config = configs[configname]
                if self.flavor == 'mac':
                    ldflags = self.xcode_settings.GetLdflags(configname, generator_default_variables['PRODUCT_DIR'], lambda p: Sourceify(self.Absolutify(p)))
                    gyp_to_build = gyp.common.InvertRelativePath(self.path)
                    target_postbuild = self.xcode_settings.AddImplicitPostbuilds(configname, QuoteSpaces(os.path.normpath(os.path.join(gyp_to_build, self.output))), QuoteSpaces(os.path.normpath(os.path.join(gyp_to_build, self.output_binary))))
                    if target_postbuild:
                        target_postbuilds[configname] = target_postbuild
                else:
                    ldflags = config.get('ldflags', [])
                    if any(dep.endswith('.so') or '.so.' in dep for dep in deps):
                        ldflags.append('-Wl,-rpath=\\$$ORIGIN/lib.%s/' % self.toolset)
                        ldflags.append('-Wl,-rpath-link=\\$(builddir)/lib.%s/' % self.toolset)
                library_dirs = config.get('library_dirs', [])
                ldflags += [ '-L%s' % library_dir for library_dir in library_dirs ]
                self.WriteList(ldflags, 'LDFLAGS_%s' % configname)
                if self.flavor == 'mac':
                    self.WriteList(self.xcode_settings.GetLibtoolflags(configname), 'LIBTOOLFLAGS_%s' % configname)

            libraries = spec.get('libraries')
            if libraries:
                libraries = gyp.common.uniquer(libraries)
                if self.flavor == 'mac':
                    libraries = self.xcode_settings.AdjustLibraries(libraries)
            self.WriteList(libraries, 'LIBS')
            self.WriteLn('%s: GYP_LDFLAGS := $(LDFLAGS_$(BUILDTYPE))' % QuoteSpaces(self.output_binary))
            self.WriteLn('%s: LIBS := $(LIBS)' % QuoteSpaces(self.output_binary))
            if self.flavor == 'mac':
                self.WriteLn('%s: GYP_LIBTOOLFLAGS := $(LIBTOOLFLAGS_$(BUILDTYPE))' % QuoteSpaces(self.output_binary))
        postbuilds = []
        if self.flavor == 'mac':
            if target_postbuilds:
                postbuilds.append('$(TARGET_POSTBUILDS_$(BUILDTYPE))')
            postbuilds.extend(gyp.xcode_emulation.GetSpecPostbuildCommands(spec))
        if postbuilds:
            self.WriteSortedXcodeEnv(self.output, self.GetSortedXcodePostbuildEnv())
            for configname in target_postbuilds:
                self.WriteLn('%s: TARGET_POSTBUILDS_%s := %s' % (
                 QuoteSpaces(self.output),
                 configname,
                 gyp.common.EncodePOSIXShellList(target_postbuilds[configname])))

            postbuilds.insert(0, gyp.common.EncodePOSIXShellList(['cd', self.path]))
            for i in xrange(len(postbuilds)):
                if not postbuilds[i].startswith('$'):
                    postbuilds[i] = EscapeShellArgument(postbuilds[i])

            self.WriteLn('%s: builddir := $(abs_builddir)' % QuoteSpaces(self.output))
            self.WriteLn('%s: POSTBUILDS := %s' % (
             QuoteSpaces(self.output), (' ').join(postbuilds)))
        if self.is_mac_bundle:
            self.WriteDependencyOnExtraOutputs(self.output, extra_outputs)
            self.WriteList(map(QuoteSpaces, bundle_deps), 'BUNDLE_DEPS')
            self.WriteLn('%s: $(BUNDLE_DEPS)' % QuoteSpaces(self.output))
            if self.type in ('shared_library', 'loadable_module'):
                self.WriteLn('\t@$(call do_cmd,mac_package_framework,,,%s)' % self.xcode_settings.GetFrameworkVersion())
            if postbuilds:
                self.WriteLn('\t@$(call do_postbuilds)')
            postbuilds = []
            self.WriteLn('\t@true  # No-op, used by tests')
            self.WriteLn('\t@touch -c %s' % QuoteSpaces(self.output))
        if postbuilds:
            assert not self.is_mac_bundle, "Postbuilds for bundles should be done on the bundle, not the binary (target '%s')" % self.target
            assert 'product_dir' not in spec, 'Postbuilds do not work with custom product_dir'
        if self.type == 'executable':
            self.WriteLn('%s: LD_INPUTS := %s' % (
             QuoteSpaces(self.output_binary),
             (' ').join(map(QuoteSpaces, link_deps))))
            if self.toolset == 'host' and self.flavor == 'android':
                self.WriteDoCmd([self.output_binary], link_deps, 'link_host', part_of_all, postbuilds=postbuilds)
            else:
                self.WriteDoCmd([self.output_binary], link_deps, 'link', part_of_all, postbuilds=postbuilds)
        elif self.type == 'static_library':
            for link_dep in link_deps:
                assert ' ' not in link_dep, 'Spaces in alink input filenames not supported (%s)' % link_dep

            if self.flavor not in ('mac', 'openbsd', 'win') and not self.is_standalone_static_library:
                self.WriteDoCmd([self.output_binary], link_deps, 'alink_thin', part_of_all, postbuilds=postbuilds)
            else:
                self.WriteDoCmd([self.output_binary], link_deps, 'alink', part_of_all, postbuilds=postbuilds)
        elif self.type == 'shared_library':
            self.WriteLn('%s: LD_INPUTS := %s' % (
             QuoteSpaces(self.output_binary),
             (' ').join(map(QuoteSpaces, link_deps))))
            self.WriteDoCmd([self.output_binary], link_deps, 'solink', part_of_all, postbuilds=postbuilds)
        elif self.type == 'loadable_module':
            for link_dep in link_deps:
                assert ' ' not in link_dep, 'Spaces in module input filenames not supported (%s)' % link_dep

            if self.toolset == 'host' and self.flavor == 'android':
                self.WriteDoCmd([self.output_binary], link_deps, 'solink_module_host', part_of_all, postbuilds=postbuilds)
            else:
                self.WriteDoCmd([
                 self.output_binary], link_deps, 'solink_module', part_of_all, postbuilds=postbuilds)
        elif self.type == 'none':
            self.WriteDoCmd([self.output_binary], deps, 'touch', part_of_all, postbuilds=postbuilds)
        else:
            print 'WARNING: no output for', self.type, target
        if self.output and self.output != self.target and self.type not in self._INSTALLABLE_TARGETS:
            self.WriteMakeRule([self.target], [self.output], comment='Add target alias', phony=True)
            if part_of_all:
                self.WriteMakeRule(['all'], [self.target], comment='Add target alias to "all" target.', phony=True)
        if self.type in self._INSTALLABLE_TARGETS or self.is_standalone_static_library:
            if self.type == 'shared_library':
                file_desc = 'shared library'
            elif self.type == 'static_library':
                file_desc = 'static library'
            else:
                file_desc = 'executable'
            install_path = self._InstallableTargetInstallPath()
            installable_deps = [self.output]
            assert self.flavor == 'mac' and 'product_dir' not in spec and self.toolset == 'target' and install_path == self.output, '%s != %s' % (
             install_path, self.output)
        self.WriteMakeRule([self.target], [install_path], comment='Add target alias', phony=True)
        if install_path != self.output:
            if not not self.is_mac_bundle:
                raise AssertionError
                self.WriteDoCmd([install_path], [self.output], 'copy', comment='Copy this to the %s output path.' % file_desc, part_of_all=part_of_all)
                installable_deps.append(install_path)
            if self.output != self.alias and self.alias != self.target:
                self.WriteMakeRule([self.alias], installable_deps, comment='Short alias for building this %s.' % file_desc, phony=True)
            if part_of_all:
                self.WriteMakeRule(['all'], [install_path], comment='Add %s to "all" target.' % file_desc, phony=True)

    def WriteList(self, value_list, variable=None, prefix='', quoter=QuoteIfNecessary):
        """Write a variable definition that is a list of values.

    E.g. WriteList(['a','b'], 'foo', prefix='blah') writes out
         foo = blaha blahb
    but in a pretty-printed style.
    """
        values = ''
        if value_list:
            value_list = [ quoter(prefix + l) for l in value_list ]
            values = ' \\\n\t' + (' \\\n\t').join(value_list)
        self.fp.write('%s :=%s\n\n' % (variable, values))

    def WriteDoCmd(self, outputs, inputs, command, part_of_all, comment=None, postbuilds=False):
        """Write a Makefile rule that uses do_cmd.

    This makes the outputs dependent on the command line that was run,
    as well as support the V= make command line flag.
    """
        suffix = ''
        if postbuilds:
            assert ',' not in command
            suffix = ',,1'
        self.WriteMakeRule(outputs, inputs, actions=[
         '$(call do_cmd,%s%s)' % (command, suffix)], comment=comment, force=True)
        outputs = [ QuoteSpaces(o, SPACE_REPLACEMENT) for o in outputs ]
        self.WriteLn('all_deps += %s' % (' ').join(outputs))

    def WriteMakeRule(self, outputs, inputs, actions=None, comment=None, order_only=False, force=False, phony=False):
        """Write a Makefile rule, with some extra tricks.

    outputs: a list of outputs for the rule (note: this is not directly
             supported by make; see comments below)
    inputs: a list of inputs for the rule
    actions: a list of shell commands to run for the rule
    comment: a comment to put in the Makefile above the rule (also useful
             for making this Python script's code self-documenting)
    order_only: if true, makes the dependency order-only
    force: if true, include FORCE_DO_CMD as an order-only dep
    phony: if true, the rule does not actually generate the named output, the
           output is just a name to run the rule
    """
        outputs = map(QuoteSpaces, outputs)
        inputs = map(QuoteSpaces, inputs)
        if comment:
            self.WriteLn('# ' + comment)
        if phony:
            self.WriteLn('.PHONY: ' + (' ').join(outputs))
        if order_only:
            order_insert = '| '
            pick_output = (' ').join(outputs)
        else:
            order_insert = ''
            pick_output = outputs[0]
        if force:
            force_append = ' FORCE_DO_CMD'
        else:
            force_append = ''
        if actions:
            self.WriteLn('%s: TOOLSET := $(TOOLSET)' % outputs[0])
        self.WriteLn('%s: %s%s%s' % (pick_output, order_insert, (' ').join(inputs),
         force_append))
        if actions:
            for action in actions:
                self.WriteLn('\t%s' % action)

        if not order_only and len(outputs) > 1:
            self.WriteLn('%s: %s' % ((' ').join(outputs[1:]), outputs[0]))
            self.WriteLn('%s: ;' % (' ').join(outputs[1:]))
        self.WriteLn()

    def WriteAndroidNdkModuleRule(self, module_name, all_sources, link_deps):
        """Write a set of LOCAL_XXX definitions for Android NDK.

    These variable definitions will be used by Android NDK but do nothing for
    non-Android applications.

    Arguments:
      module_name: Android NDK module name, which must be unique among all
          module names.
      all_sources: A list of source files (will be filtered by Compilable).
      link_deps: A list of link dependencies, which must be sorted in
          the order from dependencies to dependents.
    """
        if self.type not in ('executable', 'shared_library', 'static_library'):
            return
        self.WriteLn('# Variable definitions for Android applications')
        self.WriteLn('include $(CLEAR_VARS)')
        self.WriteLn('LOCAL_MODULE := ' + module_name)
        self.WriteLn('LOCAL_CFLAGS := $(CFLAGS_$(BUILDTYPE)) $(DEFS_$(BUILDTYPE)) $(CFLAGS_C_$(BUILDTYPE)) $(INCS_$(BUILDTYPE))')
        self.WriteLn('LOCAL_CPPFLAGS := $(CFLAGS_CC_$(BUILDTYPE))')
        self.WriteLn('LOCAL_C_INCLUDES :=')
        self.WriteLn('LOCAL_LDLIBS := $(LDFLAGS_$(BUILDTYPE)) $(LIBS)')
        cpp_ext = {'.cc': 0, '.cpp': 0, '.cxx': 0}
        default_cpp_ext = '.cpp'
        for filename in all_sources:
            ext = os.path.splitext(filename)[1]
            if ext in cpp_ext:
                cpp_ext[ext] += 1
                if cpp_ext[ext] > cpp_ext[default_cpp_ext]:
                    default_cpp_ext = ext

        self.WriteLn('LOCAL_CPP_EXTENSION := ' + default_cpp_ext)
        self.WriteList(map(self.Absolutify, filter(Compilable, all_sources)), 'LOCAL_SRC_FILES')

        def DepsToModules(deps, prefix, suffix):
            modules = []
            for filepath in deps:
                filename = os.path.basename(filepath)
                if filename.startswith(prefix) and filename.endswith(suffix):
                    modules.append(filename[len(prefix):-len(suffix)])

            return modules

        params = {'flavor': 'linux'}
        default_variables = {}
        CalculateVariables(default_variables, params)
        self.WriteList(DepsToModules(link_deps, generator_default_variables['SHARED_LIB_PREFIX'], default_variables['SHARED_LIB_SUFFIX']), 'LOCAL_SHARED_LIBRARIES')
        self.WriteList(DepsToModules(link_deps, generator_default_variables['STATIC_LIB_PREFIX'], generator_default_variables['STATIC_LIB_SUFFIX']), 'LOCAL_STATIC_LIBRARIES')
        if self.type == 'executable':
            self.WriteLn('include $(BUILD_EXECUTABLE)')
        elif self.type == 'shared_library':
            self.WriteLn('include $(BUILD_SHARED_LIBRARY)')
        elif self.type == 'static_library':
            self.WriteLn('include $(BUILD_STATIC_LIBRARY)')
        self.WriteLn()

    def WriteLn(self, text=''):
        self.fp.write(text + '\n')

    def GetSortedXcodeEnv(self, additional_settings=None):
        return gyp.xcode_emulation.GetSortedXcodeEnv(self.xcode_settings, '$(abs_builddir)', os.path.join('$(abs_srcdir)', self.path), '$(BUILDTYPE)', additional_settings)

    def GetSortedXcodePostbuildEnv(self):
        strip_save_file = self.xcode_settings.GetPerTargetSetting('CHROMIUM_STRIP_SAVE_FILE', '')
        return self.GetSortedXcodeEnv(additional_settings={'CHROMIUM_STRIP_SAVE_FILE': strip_save_file})

    def WriteSortedXcodeEnv(self, target, env):
        for k, v in env:
            self.WriteLn('%s: export %s := %s' % (QuoteSpaces(target), k, v))

    def Objectify(self, path):
        """Convert a path to its output directory form."""
        if '$(' in path:
            path = path.replace('$(obj)/', '$(obj).%s/$(TARGET)/' % self.toolset)
        if '$(obj)' not in path:
            path = '$(obj).%s/$(TARGET)/%s' % (self.toolset, path)
        return path

    def Pchify(self, path, lang):
        """Convert a prefix header path to its output directory form."""
        path = self.Absolutify(path)
        if '$(' in path:
            path = path.replace('$(obj)/', '$(obj).%s/$(TARGET)/pch-%s' % (
             self.toolset, lang))
            return path
        return '$(obj).%s/$(TARGET)/pch-%s/%s' % (self.toolset, lang, path)

    def Absolutify(self, path):
        """Convert a subdirectory-relative path into a base-relative path.
    Skips over paths that contain variables."""
        if '$(' in path:
            return path.rstrip('/')
        return os.path.normpath(os.path.join(self.path, path))

    def ExpandInputRoot(self, template, expansion, dirname):
        if '%(INPUT_ROOT)s' not in template and '%(INPUT_DIRNAME)s' not in template:
            return template
        path = template % {'INPUT_ROOT': expansion, 
           'INPUT_DIRNAME': dirname}
        return path

    def _InstallableTargetInstallPath(self):
        """Returns the location of the final output for an installable target."""
        if self.type == 'shared_library' and (self.flavor != 'mac' or self.toolset != 'target'):
            return '$(builddir)/lib.%s/%s' % (self.toolset, self.alias)
        return '$(builddir)/' + self.alias


def WriteAutoRegenerationRule(params, root_makefile, makefile_name, build_files):
    """Write the target to regenerate the Makefile."""
    options = params['options']
    build_files_args = [ gyp.common.RelativePath(filename, options.toplevel_dir) for filename in params['build_files_arg']
                       ]
    gyp_binary = gyp.common.FixIfRelativePath(params['gyp_binary'], options.toplevel_dir)
    if not gyp_binary.startswith(os.sep):
        gyp_binary = os.path.join('.', gyp_binary)
    root_makefile.write('quiet_cmd_regen_makefile = ACTION Regenerating $@\ncmd_regen_makefile = cd $(srcdir); %(cmd)s\n%(makefile_name)s: %(deps)s\n\t$(call do_cmd,regen_makefile)\n\n' % {'makefile_name': makefile_name, 
       'deps': (' ').join(map(Sourceify, build_files)), 
       'cmd': gyp.common.EncodePOSIXShellList([
             gyp_binary, '-fmake'] + gyp.RegenerateFlags(options) + build_files_args)})


def PerformBuild(data, configurations, params):
    options = params['options']
    for config in configurations:
        arguments = [
         'make']
        if options.toplevel_dir and options.toplevel_dir != '.':
            arguments += ('-C', options.toplevel_dir)
        arguments.append('BUILDTYPE=' + config)
        print 'Building [%s]: %s' % (config, arguments)
        subprocess.check_call(arguments)


def GenerateOutput(target_list, target_dicts, data, params):
    global srcdir_prefix
    options = params['options']
    flavor = gyp.common.GetFlavor(params)
    generator_flags = params.get('generator_flags', {})
    builddir_name = generator_flags.get('output_dir', 'out')
    android_ndk_version = generator_flags.get('android_ndk_version', None)
    default_target = generator_flags.get('default_target', 'all')

    def CalculateMakefilePath(build_file, base_name):
        """Determine where to write a Makefile for a given gyp file."""
        base_path = gyp.common.RelativePath(os.path.dirname(build_file), options.depth)
        output_file = os.path.join(options.depth, base_path, base_name)
        if options.generator_output:
            output_file = os.path.join(options.depth, options.generator_output, base_path, base_name)
        base_path = gyp.common.RelativePath(os.path.dirname(build_file), options.toplevel_dir)
        return (base_path, output_file)

    default_configuration = None
    toolsets = set([ target_dicts[target]['toolset'] for target in target_list ])
    for target in target_list:
        spec = target_dicts[target]
        if spec['default_configuration'] != 'Default':
            default_configuration = spec['default_configuration']
            break

    if not default_configuration:
        default_configuration = 'Default'
    srcdir = '.'
    makefile_name = 'Makefile' + options.suffix
    makefile_path = os.path.join(options.toplevel_dir, makefile_name)
    if options.generator_output:
        makefile_path = os.path.join(options.toplevel_dir, options.generator_output, makefile_name)
        srcdir = gyp.common.RelativePath(srcdir, options.generator_output)
        srcdir_prefix = '$(srcdir)/'
    flock_command = 'flock'
    header_params = {'default_target': default_target, 
       'builddir': builddir_name, 
       'default_configuration': default_configuration, 
       'flock': flock_command, 
       'flock_index': 1, 
       'link_commands': LINK_COMMANDS_LINUX, 
       'extra_commands': '', 
       'srcdir': srcdir}
    if flavor == 'mac':
        flock_command = './gyp-mac-tool flock'
        header_params.update({'flock': flock_command, 
           'flock_index': 2, 
           'link_commands': LINK_COMMANDS_MAC, 
           'extra_commands': SHARED_HEADER_MAC_COMMANDS})
    else:
        if flavor == 'android':
            header_params.update({'link_commands': LINK_COMMANDS_ANDROID})
        else:
            if flavor == 'solaris':
                header_params.update({'flock': './gyp-flock-tool flock', 
                   'flock_index': 2})
            else:
                if flavor == 'freebsd':
                    header_params.update({'flock': 'lockf'})
                else:
                    if flavor == 'aix':
                        header_params.update({'link_commands': LINK_COMMANDS_AIX, 
                           'flock': './gyp-flock-tool flock', 
                           'flock_index': 2})
                    header_params.update({'CC.target': GetEnvironFallback(('CC_target', 'CC'), '$(CC)'), 
                       'AR.target': GetEnvironFallback(('AR_target', 'AR'), '$(AR)'), 
                       'CXX.target': GetEnvironFallback(('CXX_target', 'CXX'), '$(CXX)'), 
                       'LINK.target': GetEnvironFallback(('LINK_target', 'LINK'), '$(LINK)'), 
                       'CC.host': GetEnvironFallback(('CC_host', ), 'gcc'), 
                       'AR.host': GetEnvironFallback(('AR_host', ), 'ar'), 
                       'CXX.host': GetEnvironFallback(('CXX_host', ), 'g++'), 
                       'LINK.host': GetEnvironFallback(('LINK_host', ), '$(CXX.host)')})
                    build_file, _, _ = gyp.common.ParseQualifiedTarget(target_list[0])
                    make_global_settings_array = data[build_file].get('make_global_settings', [])
                    wrappers = {}
                    wrappers['LINK'] = '%s $(builddir)/linker.lock' % flock_command
                    for key, value in make_global_settings_array:
                        if key.endswith('_wrapper'):
                            wrappers[key[:-len('_wrapper')]] = '$(abspath %s)' % value

                    make_global_settings = ''
                    for key, value in make_global_settings_array:
                        if re.match('.*_wrapper', key):
                            continue
                        if value[0] != '$':
                            value = '$(abspath %s)' % value
                        wrapper = wrappers.get(key)
                        if wrapper:
                            value = '%s %s' % (wrapper, value)
                            del wrappers[key]
                        if key in ('CC', 'CC.host', 'CXX', 'CXX.host'):
                            make_global_settings += 'ifneq (,$(filter $(origin %s), undefined default))\n' % key
                            env_key = key.replace('.', '_')
                            if env_key in os.environ:
                                value = os.environ[env_key]
                            make_global_settings += '  %s = %s\n' % (key, value)
                            make_global_settings += 'endif\n'
                        else:
                            make_global_settings += '%s ?= %s\n' % (key, value)

                    header_params['make_global_settings'] = make_global_settings
                    gyp.common.EnsureDirExists(makefile_path)
                    root_makefile = open(makefile_path, 'w')
                    root_makefile.write(SHARED_HEADER % header_params)
                    if android_ndk_version:
                        root_makefile.write('# Define LOCAL_PATH for build of Android applications.\nLOCAL_PATH := $(call my-dir)\n\n')
                    for toolset in toolsets:
                        root_makefile.write('TOOLSET := %s\n' % toolset)
                        WriteRootHeaderSuffixRules(root_makefile)

                    dest_path = os.path.dirname(makefile_path)
                    gyp.common.CopyTool(flavor, dest_path)
                    needed_targets = set()
                    for build_file in params['build_files']:
                        for target in gyp.common.AllTargets(target_list, target_dicts, build_file):
                            needed_targets.add(target)

                build_files = set()
                include_list = set()
                for qualified_target in target_list:
                    build_file, target, toolset = gyp.common.ParseQualifiedTarget(qualified_target)
                    this_make_global_settings = data[build_file].get('make_global_settings', [])
                    assert make_global_settings_array == this_make_global_settings, 'make_global_settings needs to be the same for all targets. %s vs. %s' % (
                     this_make_global_settings, make_global_settings)
                    build_files.add(gyp.common.RelativePath(build_file, options.toplevel_dir))
                    included_files = data[build_file]['included_files']
                    for included_file in included_files:
                        relative_include_file = gyp.common.RelativePath(gyp.common.UnrelativePath(included_file, build_file), options.toplevel_dir)
                        abs_include_file = os.path.abspath(relative_include_file)
                        if params['home_dot_gyp'] and abs_include_file.startswith(params['home_dot_gyp']):
                            build_files.add(abs_include_file)
                        else:
                            build_files.add(relative_include_file)

                    base_path, output_file = CalculateMakefilePath(build_file, target + '.' + toolset + options.suffix + '.mk')
                    spec = target_dicts[qualified_target]
                    configs = spec['configurations']
                    if flavor == 'mac':
                        gyp.xcode_emulation.MergeGlobalXcodeSettingsToSpec(data[build_file], spec)
                    writer = MakefileWriter(generator_flags, flavor)
                    writer.Write(qualified_target, base_path, output_file, spec, configs, part_of_all=qualified_target in needed_targets)
                    mkfile_rel_path = gyp.common.RelativePath(output_file, os.path.dirname(makefile_path))
                    include_list.add(mkfile_rel_path)

            depth_rel_path = gyp.common.RelativePath(options.depth, os.getcwd())
            for build_file in build_files:
                build_file = os.path.join(depth_rel_path, build_file)
                gyp_targets = [ target_dicts[target]['target_name'] for target in target_list if target.startswith(build_file) and target in needed_targets
                              ]
                if not gyp_targets:
                    continue
                base_path, output_file = CalculateMakefilePath(build_file, os.path.splitext(os.path.basename(build_file))[0] + '.Makefile')
                makefile_rel_path = gyp.common.RelativePath(os.path.dirname(makefile_path), os.path.dirname(output_file))
                writer.WriteSubMake(output_file, makefile_rel_path, gyp_targets, builddir_name)

        root_makefile.write('\n')
        for include_file in sorted(include_list):
            root_makefile.write('ifeq ($(strip $(foreach prefix,$(NO_LOAD),\\\n    $(findstring $(join ^,$(prefix)),\\\n                 $(join ^,' + include_file + ')))),)\n')
            root_makefile.write('  include ' + include_file + '\n')
            root_makefile.write('endif\n')

    root_makefile.write('\n')
    if not generator_flags.get('standalone') and generator_flags.get('auto_regeneration', True):
        WriteAutoRegenerationRule(params, root_makefile, makefile_name, build_files)
    root_makefile.write(SHARED_FOOTER)
    root_makefile.close()
    return