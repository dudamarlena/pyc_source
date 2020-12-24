# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/cmdline/rbext.py
# Compiled at: 2020-02-11 04:03:56
"""Command line tool for helping develop extensions.

This tool, :command:`rbext`, currently provides the ability to easily run
extension-provided unit tests. In the future, it'll also help with other
development tasks, and with updating the Package Store with the latest versions
of an extension.
"""
from __future__ import print_function, unicode_literals
import argparse, logging, os, re, sys
from textwrap import dedent
os.environ.setdefault(b'DJANGO_SETTINGS_MODULE', b'reviewboard.settings')
rbext_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(rbext_dir, b'conf', b'rbext'))
import pkg_resources
from django.utils.translation import ugettext_lazy as _, ugettext
from reviewboard import get_manual_url

class BaseCommand(object):
    """Base class for a command."""
    name = None
    help_summary = b'Run unit tests for an extension.'

    def add_options(self, parser):
        """Add any command-specific options to the parser.

        Args:
            parser (argparse.ArgumentParser):
                The argument parser.
        """
        pass

    def run(self, options):
        """Run the command.

        This will perform common setup work and then hand things off to
        :py:meth:`main`.

        Args:
            options (argparse.Namespace):
                Options set from the arguments.
        """
        if options.settings_file:
            sys.path.insert(0, os.path.abspath(os.path.dirname(options.settings_file)))
        return self.main(options)

    def main(self, options):
        """Perform the main operations for the command.

        Args:
            options (argparse.Namespace):
                Options set from the arguments.

        Returns:
            int:
            The command's exit code.
        """
        raise NotImplementedError

    def error(self, msg):
        """Display a fatal error to the user and exit.

        Args:
            msg (unicode):
                The message to display.

        Raises:
            django.core.management.CommandError:
            The resulting error.
        """
        from django.core.management import CommandError
        raise CommandError(msg)


class TestCommand(BaseCommand):
    """A command that runs an extension's test suite."""
    name = b'test'
    help_summary = b'Run unit tests for an extension.'

    def add_options(self, parser):
        """Add command line arguments for running tests.

        Args:
            parser (argparse.ArgumentParser):
                The argument parser.
        """
        parser.add_argument(b'--tree-root', metavar=b'PATH', default=os.getcwd(), help=b'The path to the root of the source tree.')
        parser.add_argument(b'-m', b'--module', action=b'append', metavar=b'MODULE_NAME', dest=b'module_names', required=True, help=b'The name(s) of the extension module(s) to test. For example, if your tests are in "myextension.tests", you might want to use "myextension".')
        parser.add_argument(b'--with-coverage', action=b'store_true', default=False, help=b'Generate a code coverage report for the tests.')
        parser.add_argument(b'tests', metavar=b'TEST', nargs=b'*', help=b'Specific tests to run. This can be in the form of mypackage.mymodule, mypackage.mymodule:TestsClass, or mypackage.mymodule:TestsClass.test_method.')

    def main(self, options):
        """Main function for running unit tests for the extension.

        Args:
            options (argparse.Namespace):
                Options set from the arguments.

        Returns:
            int:
            The command's exit code.
        """
        os.environ[b'RB_TEST_MODULES'] = (b',').join(module_name.encode(b'utf-8') for module_name in options.module_names)
        os.chdir(options.tree_root)
        os.environ[b'RB_RUNNING_TESTS'] = b'1'
        from reviewboard.test import RBTestRunner
        test_runner = RBTestRunner(test_packages=options.module_names, cover_packages=options.module_names, verbosity=1)
        failures = test_runner.run_tests(options.tests)
        if failures:
            return 1
        else:
            return 0


class CreateCommand(BaseCommand):
    """A command for creating a new extension package."""
    name = b'create'
    help_summary = _(b'Create a new extension source tree.')

    def add_options(self, parser):
        """Add command line arguments for creating an extension.

        Args:
            parser (argparse.ArgumentParser):
                The argument parser.
        """
        parser.add_argument(b'--name', required=True, help=_(b'The human-readable name for the extension. This is required.'))
        parser.add_argument(b'--class-name', default=None, help=_(b'The class name for the extension (generally in CamelCase form, without spaces). If not provided, this will be based on the extension name.'))
        parser.add_argument(b'--package-name', default=None, help=_(b'The name of the package (using alphanumeric  ). If not provided, this will be based on the exension name.'))
        parser.add_argument(b'--package-version', default=b'1.0', help=_(b'The version for your extension and package.'))
        parser.add_argument(b'--summary', default=None, help=_(b'A one-line summary of the extension.'))
        parser.add_argument(b'--description', default=None, help=_(b'A short description of the extension.'))
        parser.add_argument(b'--author-name', default=None, help=_(b'The name of the author for the package and extension metadata. This can be a company name.'))
        parser.add_argument(b'--author-email', default=None, help=_(b'The e-mail address of the author for the package and extension metadata.'))
        parser.add_argument(b'--enable-configuration', action=b'store_true', default=False, help=_(b'Whether to enable a Configure button and view for the extension.'))
        parser.add_argument(b'--enable-static-media', action=b'store_true', default=False, help=_(b'Whether to enable static media files for the package.'))
        return

    def main(self, options):
        """Main function for creating an extension.

        Args:
            options (argparse.Namesapce):
                Options set from the arguments.

        Returns:
            int:
            The comamnd's exit code.
        """
        self._process_options(options)
        name = options.name
        package_name = options.package_name
        summary = options.summary
        description = options.description
        class_name = options.class_name
        configurable = options.enable_configuration
        enable_static_media = options.enable_static_media
        root_dir = package_name
        if os.path.exists(root_dir):
            self.error(ugettext(b'There\'s already a directory named "%s". You must remove it before you can create a new extension there.') % root_dir)
        ext_dir = os.path.join(root_dir, package_name)
        static_dir = os.path.join(ext_dir, b'static')
        templates_dir = os.path.join(ext_dir, b'templates')
        for path in (root_dir, ext_dir):
            os.mkdir(path, 493)

        if enable_static_media:
            os.mkdir(static_dir, 493)
            for path in ('css', 'js', 'images'):
                os.mkdir(os.path.join(static_dir, path))

        self._write_file(os.path.join(root_dir, b'README.rst'), self._create_readme(name=name, summary=summary, description=description))
        self._write_file(os.path.join(root_dir, b'MANIFEST.in'), self._create_manifest(static_dir=static_dir, templates_dir=templates_dir))
        self._write_file(os.path.join(root_dir, b'setup.py'), self._create_setup_py(package_name=package_name, version=options.package_version, summary=summary, author=options.author_name, author_email=options.author_email, class_name=class_name), mode=493)
        self._write_file(os.path.join(ext_dir, b'__init__.py'), b'')
        self._write_file(os.path.join(ext_dir, b'extension.py'), self._create_extension_py(name=name, package_name=package_name, class_name=class_name, summary=summary, configurable=configurable, has_static_media=enable_static_media))
        if configurable:
            form_class_name = b'%sForm' % class_name
            self._write_file(os.path.join(ext_dir, b'admin_urls.py'), self._create_admin_urls_py(package_name=package_name, class_name=class_name, form_class_name=form_class_name))
            self._write_file(os.path.join(ext_dir, b'forms.py'), self._create_forms_py(form_class_name=form_class_name))
        print(b'Generated a new extension in %s' % os.path.abspath(root_dir))
        print()
        print(b'For information on writing your extension, see')
        print(b'%sextending/' % get_manual_url())
        return 0

    def _process_options(self, options):
        """Process and normalize any provided options.

        This will attempt to provide suitable defaults for missing parameters,
        adn to check that others are valid.

        Args:
            options (argparse.Namesapce):
                Options set from the arguments.
        """
        name = options.name.strip()
        package_name = options.package_name
        class_name = options.class_name
        if not package_name:
            package_name = self._normalize_package_name(name)
            print(ugettext(b'Using "%s" as the package name.') % package_name)
        else:
            package_name = package_name.strip()
            if not re.match(b'[A-Za-z][A-Za-z0-9._-]*', package_name):
                self.error(ugettext(b'"%s" is not a valid package name. Try --package-name="%s"') % (
                 package_name,
                 self._normalize_package_name(package_name)))
        if not class_name:
            class_name = self._normalize_class_name(name)
            print(ugettext(b'Using "%s" as the extension class name.') % class_name)
        else:
            class_name = class_name.strip()
            if not re.match(b'[A-Za-z][A-Za-z0-9_]+Extension$', class_name):
                self.error(ugettext(b'"%s" is not a valid class name. Try --class-name="%s"') % (
                 package_name,
                 self._normalize_class_name(class_name)))
        options.name = name
        options.package_name = package_name
        options.class_name = class_name

    def _normalize_package_name(self, name):
        """Normalize a package name.

        This will ensure the package name is in a suitable format, replacing
        any invalid characters or dashes with ``_``, and converting it to
        lowercase.

        Args:
            name (unicode):
                The name of the package to normalize.

        Returns:
            unicode:
            The normalized name.
        """
        return pkg_resources.safe_name(name).replace(b'-', b'_').lower()

    def _normalize_class_name(self, name):
        """Normalize a class name.

        This will ensure the class name is in a suitable format, converting it
        to CamelCase and adding an "Extension" at the end if needed.

        Args:
            name (unicode):
                The name of the class to normalize.

        Returns:
            unicode:
            The normalized class name.
        """
        class_name = (b'').join(word.capitalize() for word in re.sub(b'[^A-Za-z0-9]+', b' ', name).split())
        if not class_name.endswith(b'Extension'):
            class_name += b'Extension'
        return class_name

    def _write_file(self, filename, content, mode=None):
        """Write content to a file.

        This will create the file and write the provided content. The content
        will be stripped and dedented, with a trailing newline added, allowing
        the generation code to make use of multi-line strings.

        Args:
            path (unicode):
                The path of the file to write.

            content (unicode):
                The content to write.

            mode (int):
                The optional permissions mode to set for the file.
        """
        with open(filename, b'w') as (fp):
            fp.write(dedent(content).strip())
            fp.write(b'\n')
        if mode is not None:
            os.chmod(filename, mode)
        return

    def _create_readme(self, name, summary, description):
        """Create the content for a README.rst file.

        Args:
            name (unicode):
                The extension's name.

            summary (unicode):
                The extension's summary.

            description (unicode):
                A description of the extension.

        Returns:
            unicode:
            The resulting content for the file.
        """
        return b'\n            %(header_bar)s\n            %(header)s\n            %(header_bar)s\n\n            %(content)s\n        ' % {b'header': name, 
           b'header_bar': b'=' * len(name), 
           b'content': (b'\n\n').join(content for content in (summary, description) if content) or ugettext(b'Describe your extension.')}

    def _create_manifest(self, templates_dir, static_dir):
        """Create the content for a MANIFEST.in file.

        Args:
            templates_dir (unicode):
                The relative path to the templates directory.

            static_dir (unicode):
                The relative path to the static media directory.

        Returns:
            unicode:
            The resulting content for the file.
        """
        return b'\n            graft %(templates_dir)s\n            graft %(static_dir)s\n\n            include COPYING\n            include INSTALL\n            include README.md\n            include *-requirements.txt\n\n            global-exclude .*.sw[op] *.py[co] __pycache__ .DS_Store .noseids\n        ' % {b'templates_dir': templates_dir, 
           b'static_dir': static_dir}

    def _create_setup_py(self, package_name, version, summary, author, author_email, class_name):
        """Create the content for a setup.py file.

        Args:
            package_name (unicode):
                The name of the package.

            version (unicode):
                The version of the package.

            summary (unicode):
                A summary of the package.

            author (unicode):
                The name of the author of the extension.

            author_email (unicode):
                The e-mail address of the author of the extension.

            class_name (unicode):
                The name of the extension class.

        Returns:
            unicode:
            The resulting content for the file.
        """
        return b'\n            #!/usr/bin/env python\n\n            from __future__ import unicode_literals\n\n            from reviewboard.extensions.packaging import setup\n            from setuptools import find_packages\n\n\n            setup(\n                name=\'%(package_name)s\',\n                version=\'%(version)s\',\n                description=%(description)s,\n                author=%(author)s,\n                author_email=%(author_email)s,\n                packages=find_packages(),\n                install_requires=[\n                    # Your package dependencies go here.\n                    # Don\'t include "ReviewBoard" in this list.\n                ],\n                entry_points={\n                    \'reviewboard.extensions\': [\n                        \'%(package_name)s = %(ext_class_path)s\',\n                    ],\n                },\n                classifiers=[\n                    # For a full list of package classifiers, see\n                    # %(classifiers_url)s\n\n                    \'Development Status :: 3 - Alpha\',\n                    \'Environment :: Web Framework\',\n                    \'Framework :: Review Board\',\n                    \'Operating System :: OS Independent\',\n                    \'Programming Language :: Python\',\n                ],\n            )\n        ' % {b'author': self._sanitize_string_for_python(author or b'<REPLACE ME>'), 
           b'author_email': self._sanitize_string_for_python(author_email or b'<REPLACE ME>'), 
           b'classifiers_url': b'https://pypi.python.org/pypi?%3Aaction=list_classifiers', 
           b'description': self._sanitize_string_for_python(summary or b'<REPLACE ME>'), 
           b'ext_class_path': b'%s.extension:%s' % (package_name, class_name), 
           b'package_name': package_name, 
           b'version': version}

    def _create_extension_py(self, name, package_name, class_name, summary, configurable, has_static_media):
        """Create the content for an extension.py file.

        Args:
            name (unicode):
                The name of the extension.

            package_name (unicode):
                The name of the package.

            class_name (unicode):
                The name of the extension class.

            summary (unicode):
                A summary of the extension.

            configurable (bool):
                Whether the package is set to be configurable.

            has_static_media (bool):
                Whether the package is set to have static media files.

        Returns:
            unicode:
            The resulting content for the file.
        """
        extension_docs_url = b'%sextending/extensions/' % get_manual_url()
        static_media_content = b"\n                # You can create a list of CSS bundles to compile and ship\n                # with your extension. These can include both *.css and\n                # *.less (http://lesscss.org/) files. See\n                # %(static_docs_url)s\n                css_bundles = {\n                    'my-bundle-name': {\n                        'source_filenames': [\n                            'css/style.less',\n                        ],\n                        'apply_to': ['my-view-url-name'],\n                    },\n                }\n\n                # JavaScript bundles are also supported. These support\n                # standard *.js files and *.es6.js files (which allow for\n                # writing and transpiling ES6 JavaScript).\n                js_bundles = {\n                    'my-bundle-name': {\n                        'source_filenames': [\n                            'js/script.es6.js',\n                            'js/another-script.js',\n                        ],\n                    },\n                }\n        " % {b'static_docs_url': b'%sstatic-files/' % extension_docs_url}
        configuration_content = b"\n                # Default values for any configuration settings for your\n                # extension.\n                default_settings = {\n                    'my_field_1': 'my default value',\n                    'my_field_2': False,\n                }\n\n                # Set is_configurable and define an admin_urls.py to add\n                # a standard configuration page for your extension.\n                # See %(configure_docs_url)s\n                is_configurable = True\n        " % {b'configure_docs_url': b'%sconfiguration/' % extension_docs_url}
        return b'\n            """%(name)s for Review Board."""\n\n            from __future__ import unicode_literals\n\n            from django.utils.translation import ugettext_lazy as _\n            from reviewboard.extensions.base import Extension\n            from reviewboard.extensions.hooks import TemplateHook\n\n\n            class %(class_name)s(Extension):\n                """Internal description for your extension here."""\n\n                metadata = {\n                    \'Name\': _(%(metadata_name)s),\n                    \'Summary\': _(%(metadata_summary)s),\n                }\n            %(extra_class_content)s\n                def initialize(self):\n                    """Initialize the extension."""\n                    # Set up any hooks your extension needs here. See\n                    # %(hooks_docs_url)s\n                    TemplateHook(self,\n                                 \'before-login-form\',\n                                 \'%(package_name)s/before-login-form.html\')\n        ' % {b'class_name': class_name, 
           b'extra_class_content': (b'').join(extra_content for extra_content, should_add in (
                                  (
                                   configuration_content, configurable),
                                  (
                                   static_media_content, has_static_media)) if should_add), 
           b'hooks_docs_url': b'%s#python-extension-hooks' % extension_docs_url, 
           b'metadata_name': self._sanitize_string_for_python(name), 
           b'metadata_summary': self._sanitize_string_for_python(summary or b'REPLACE ME'), 
           b'name': name, 
           b'package_name': package_name}

    def _create_admin_urls_py(self, package_name, class_name, form_class_name):
        """Create the content for an admin_urls.py file.

        Args:
            package_name (unicode):
                The name of the package.

            class_name (unicode):
                The name of the extension class.

            form_class_name (unicode):
                The name of the extension settings form class.

        Returns:
            unicode:
            The resulting content for the file.
        """
        return b'\n            """Administration and configuration URLs for the extension."""\n\n            from __future__ import unicode_literals\n\n            from django.conf.urls import url\n            from reviewboard.extensions.views import configure_extension\n\n            from %(package_name)s.extension import %(class_name)s\n            from %(package_name)s.forms import %(form_class_name)s\n\n\n            urlpatterns = [\n                url(r\'^$\',\n                    configure_extension,\n                    {\n                        \'ext_class\': %(class_name)s,\n                        \'form_class\': %(form_class_name)s,\n                    }),\n            ]\n        ' % {b'class_name': class_name, 
           b'form_class_name': form_class_name, 
           b'package_name': package_name}

    def _create_forms_py(self, form_class_name):
        """Create the content for a forms.py file.

        Args:
            form_class_name (unicode):
                The name of the extension settings form class.

        Returns:
            unicode:
            The resulting content for the file.
        """
        return b'\n            """Configuration forms for the extension."""\n\n            from __future__ import unicode_literals\n\n            from django import forms\n            from djblets.extensions.forms import SettingsForm\n\n\n            class %(form_class_name)s(SettingsForm):\n                my_field_1 = forms.CharField()\n                my_field_2 = forms.BooleanField()\n        ' % {b'form_class_name': form_class_name}

    def _sanitize_string_for_python(self, s):
        """Sanitize a string for inclusion in a Python source file.

        This will return a string representation without any leading ``u``
        (when run on Python 2.x).

        Args:
            s (unicode):
                The string to sanitize.

        Returns:
            unicode:
            The sanitized string.
        """
        s = repr(s)
        if s.startswith(b'u'):
            s = s[1:]
        return s


class RBExt(object):
    """Command line tool for helping develop Review Board extensions.

    This tool provides subcommands useful for extension developers. It
    currently provides:

    * ``test``: Runs an extension's test suite.
    """
    COMMANDS = [
     CreateCommand(),
     TestCommand()]

    def run(self, argv):
        """Run an rbext command with the provided arguments.

        During the duration of the run, :py:data:`sys.argv` will be set to
        the provided arguments.

        Args:
            argv (list of unicode):
                The command line arguments passed to the command. This should
                not include the executable name as the first element.

        Returns:
            int:
            The command's exit code.
        """
        command, options = self.parse_options(argv)
        old_argv = sys.argv
        sys.argv = argv
        try:
            try:
                return command.run(options)
            except Exception as e:
                logging.exception(b'Unexpected exception when running command "%s": %s', command.name, e)
                return 1

        finally:
            sys.argv = old_argv

    def parse_options(self, argv):
        """Parse arguments for the command.

        Args:
            argv (list of unicode):
                The arguments provided on the command line.

        Returns:
            unicode:
            The name of the command to run.
        """
        parser = argparse.ArgumentParser(prog=b'rbext', usage=b'%(prog)s <command>')
        subparsers = parser.add_subparsers(title=b'Commands', dest=b'command')
        commands = sorted(self.COMMANDS, key=lambda cmd: cmd.name)
        command_map = {}
        for command in commands:
            command_map[command.name] = command
            subparser = subparsers.add_parser(command.name, help=command.help_summary)
            subparser.add_argument(b'-d', b'--debug', action=b'store_true', dest=b'debug', default=False, help=b'Display debug output.')
            subparser.add_argument(b'-s', b'--settings-file', dest=b'settings_file', default=None, help=b'test_settings.py file to use for any custom settings.')
            command.add_options(subparser)

        try:
            i = argv.index(b'--')
            argv = argv[:i]
        except ValueError:
            pass

        options = parser.parse_args(argv)
        return (
         command_map[options.command], options)


def main():
    """Run rbext.

    This is used by the Python EntryPoint to run rbext. It will pass in any
    arguments found on the command line and exit with the correct error code.
    """
    sys.exit(RBExt().run(sys.argv[1:]))