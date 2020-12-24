# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pbr/builddoc.py
# Compiled at: 2017-12-04 07:19:32
from distutils import log
import fnmatch, os, sys
try:
    import cStringIO
except ImportError:
    import io as cStringIO

try:
    import sphinx
    from sphinx import apidoc
    from sphinx import application
    from sphinx import setup_command
except Exception as e:
    raise ImportError(str(e))

from pbr import git
from pbr import options
from pbr import version
_rst_template = '%(heading)s\n%(underline)s\n\n.. automodule:: %(module)s\n  :members:\n  :undoc-members:\n  :show-inheritance:\n'

def _find_modules(arg, dirname, files):
    for filename in files:
        if filename.endswith('.py') and filename != '__init__.py':
            arg['%s.%s' % (dirname.replace('/', '.'), filename[:-3])] = True


class LocalBuildDoc(setup_command.BuildDoc):
    builders = [
     'html']
    command_name = 'build_sphinx'
    sphinx_initialized = False

    def _get_source_dir(self):
        option_dict = self.distribution.get_option_dict('build_sphinx')
        pbr_option_dict = self.distribution.get_option_dict('pbr')
        _, api_doc_dir = pbr_option_dict.get('api_doc_dir', (None, 'api'))
        if 'source_dir' in option_dict:
            source_dir = os.path.join(option_dict['source_dir'][1], api_doc_dir)
        else:
            source_dir = 'doc/source/' + api_doc_dir
        if not os.path.exists(source_dir):
            os.makedirs(source_dir)
        return source_dir

    def generate_autoindex(self, excluded_modules=None):
        log.info('[pbr] Autodocumenting from %s' % os.path.abspath(os.curdir))
        modules = {}
        source_dir = self._get_source_dir()
        for pkg in self.distribution.packages:
            if '.' not in pkg:
                for dirpath, dirnames, files in os.walk(pkg):
                    _find_modules(modules, dirpath, files)

        def include(module):
            return not any(fnmatch.fnmatch(module, pat) for pat in excluded_modules)

        module_list = sorted(mod for mod in modules.keys() if include(mod))
        autoindex_filename = os.path.join(source_dir, 'autoindex.rst')
        with open(autoindex_filename, 'w') as (autoindex):
            autoindex.write('.. toctree::\n   :maxdepth: 1\n\n')
            for module in module_list:
                output_filename = os.path.join(source_dir, '%s.rst' % module)
                heading = 'The :mod:`%s` Module' % module
                underline = '=' * len(heading)
                values = dict(module=module, heading=heading, underline=underline)
                log.info('[pbr] Generating %s' % output_filename)
                with open(output_filename, 'w') as (output_file):
                    output_file.write(_rst_template % values)
                autoindex.write('   %s.rst\n' % module)

    def _sphinx_tree(self):
        source_dir = self._get_source_dir()
        cmd = ['apidoc', '.', '-H', 'Modules', '-o', source_dir]
        apidoc.main(cmd + self.autodoc_tree_excludes)

    def _sphinx_run(self):
        if not self.verbose:
            status_stream = cStringIO.StringIO()
        else:
            status_stream = sys.stdout
        confoverrides = {}
        if self.project:
            confoverrides['project'] = self.project
        if self.version:
            confoverrides['version'] = self.version
        if self.release:
            confoverrides['release'] = self.release
        if self.today:
            confoverrides['today'] = self.today
        if self.sphinx_initialized:
            confoverrides['suppress_warnings'] = ['app.add_directive', 'app.add_role',
             'app.add_generic_role', 'app.add_node',
             'image.nonlocal_uri']
        app = application.Sphinx(self.source_dir, self.config_dir, self.builder_target_dir, self.doctree_dir, self.builder, confoverrides, status_stream, freshenv=self.fresh_env, warningiserror=self.warning_is_error)
        self.sphinx_initialized = True
        try:
            app.build(force_all=self.all_files)
        except Exception as err:
            from docutils import utils
            if isinstance(err, utils.SystemMessage):
                sys.stder.write('reST markup error:\n')
                sys.stderr.write(err.args[0].encode('ascii', 'backslashreplace'))
                sys.stderr.write('\n')
            else:
                raise

        if self.link_index:
            src = app.config.master_doc + app.builder.out_suffix
            dst = app.builder.get_outfilename('index')
            os.symlink(src, dst)

    def run(self):
        option_dict = self.distribution.get_option_dict('pbr')
        if git._git_is_installed():
            git.write_git_changelog(option_dict=option_dict)
            git.generate_authors(option_dict=option_dict)
        tree_index = options.get_boolean_option(option_dict, 'autodoc_tree_index_modules', 'AUTODOC_TREE_INDEX_MODULES')
        auto_index = options.get_boolean_option(option_dict, 'autodoc_index_modules', 'AUTODOC_INDEX_MODULES')
        if not os.getenv('SPHINX_DEBUG'):
            if tree_index:
                self._sphinx_tree()
            if auto_index:
                self.generate_autoindex(set(option_dict.get('autodoc_exclude_modules', [
                 None, ''])[1].split()))
        self.finalize_options()
        is_multibuilder_sphinx = version.SemanticVersion.from_pip_string(sphinx.__version__) >= version.SemanticVersion(1, 6)
        if not is_multibuilder_sphinx:
            log.warning('[pbr] Support for Sphinx < 1.6 will be dropped in pbr 4.0. Upgrade to Sphinx 1.6+')
        if self.builders != ['html']:
            log.warning("[pbr] Sphinx 1.6 added native support for specifying multiple builders in the '[sphinx_build] builder' configuration option, found in 'setup.cfg'. As a result, the '[sphinx_build] builders' option has been deprecated and will be removed in pbr 4.0. Migrate to the 'builder' configuration option.")
            if is_multibuilder_sphinx:
                self.builder = self.builders
        if is_multibuilder_sphinx:
            return setup_command.BuildDoc.run(self)
        else:
            for builder in self.builder:
                self.builder = builder
                self.finalize_options()
                self._sphinx_run()

            return

    def initialize_options(self):
        setup_command.BuildDoc.initialize_options(self)
        self.autodoc_tree_excludes = [
         'setup.py']

    def finalize_options(self):
        setup_command.BuildDoc.finalize_options(self)
        option_dict = self.distribution.get_option_dict('build_sphinx')
        if 'command line' in option_dict.get('builder', [[]])[0]:
            self.builders = option_dict['builder'][1]
        if not isinstance(self.builders, list) and self.builders:
            self.builders = self.builders.split(',')
        self.project = self.distribution.get_name()
        self.version = self.distribution.get_version()
        self.release = self.distribution.get_version()
        opt = 'autodoc_tree_excludes'
        option_dict = self.distribution.get_option_dict('pbr')
        if opt in option_dict:
            self.autodoc_tree_excludes = option_dict[opt][1]
            self.ensure_string_list(opt)
        if not hasattr(self, 'warning_is_error'):
            self.warning_is_error = False