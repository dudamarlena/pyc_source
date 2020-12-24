# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-pti7pv2_/pip/pip/_internal/commands/show.py
# Compiled at: 2020-02-14 17:24:43
# Size of source mod 2**32: 6792 bytes
from __future__ import absolute_import
import logging, os
from email.parser import FeedParser
from pip._vendor import pkg_resources
from pip._vendor.packaging.utils import canonicalize_name
from pip._internal.cli.base_command import Command
from pip._internal.cli.status_codes import ERROR, SUCCESS
from pip._internal.utils.misc import write_output
logger = logging.getLogger(__name__)

class ShowCommand(Command):
    __doc__ = '\n    Show information about one or more installed packages.\n\n    The output is in RFC-compliant mail header format.\n    '
    usage = '\n      %prog [options] <package> ...'
    ignore_require_venv = True

    def __init__(self, *args, **kw):
        (super(ShowCommand, self).__init__)(*args, **kw)
        self.cmd_opts.add_option('-f',
          '--files', dest='files',
          action='store_true',
          default=False,
          help='Show the full list of installed files for each package.')
        self.parser.insert_option_group(0, self.cmd_opts)

    def run(self, options, args):
        if not args:
            logger.warning('ERROR: Please provide a package name or names.')
            return ERROR
        else:
            query = args
            results = search_packages_info(query)
            return print_results(results,
              list_files=(options.files), verbose=(options.verbose)) or ERROR
        return SUCCESS


def search_packages_info(query):
    """
    Gather details from installed distributions. Print distribution name,
    version, location, and installed files. Installed files requires a
    pip generated 'installed-files.txt' in the distributions '.egg-info'
    directory.
    """
    installed = {}
    for p in pkg_resources.working_set:
        installed[canonicalize_name(p.project_name)] = p

    query_names = [canonicalize_name(name) for name in query]
    missing = sorted([name for name, pkg in zip(query, query_names) if pkg not in installed])
    if missing:
        logger.warning('Package(s) not found: %s', ', '.join(missing))

    def get_requiring_packages(package_name):
        canonical_name = canonicalize_name(package_name)
        return [pkg.project_name for pkg in pkg_resources.working_set if canonical_name in [canonicalize_name(required.name) for required in pkg.requires()]]

    for dist in [installed[pkg] for pkg in query_names if pkg in installed]:
        package = {'name':dist.project_name,  'version':dist.version, 
         'location':dist.location, 
         'requires':[dep.project_name for dep in dist.requires()], 
         'required_by':get_requiring_packages(dist.project_name)}
        file_list = None
        metadata = None
        if isinstance(dist, pkg_resources.DistInfoDistribution):
            if dist.has_metadata('RECORD'):
                lines = dist.get_metadata_lines('RECORD')
                paths = [l.split(',')[0] for l in lines]
                paths = [os.path.join(dist.location, p) for p in paths]
                file_list = [os.path.relpath(p, dist.location) for p in paths]
            if dist.has_metadata('METADATA'):
                metadata = dist.get_metadata('METADATA')
        else:
            if dist.has_metadata('installed-files.txt'):
                paths = dist.get_metadata_lines('installed-files.txt')
                paths = [os.path.join(dist.egg_info, p) for p in paths]
                file_list = [os.path.relpath(p, dist.location) for p in paths]
            if dist.has_metadata('PKG-INFO'):
                metadata = dist.get_metadata('PKG-INFO')
        if dist.has_metadata('entry_points.txt'):
            entry_points = dist.get_metadata_lines('entry_points.txt')
            package['entry_points'] = entry_points
        if dist.has_metadata('INSTALLER'):
            for line in dist.get_metadata_lines('INSTALLER'):
                if line.strip():
                    package['installer'] = line.strip()
                    break

        feed_parser = FeedParser()
        feed_parser.feed(metadata)
        pkg_info_dict = feed_parser.close()
        for key in ('metadata-version', 'summary', 'home-page', 'author', 'author-email',
                    'license'):
            package[key] = pkg_info_dict.get(key)

        classifiers = []
        for line in metadata.splitlines():
            if line.startswith('Classifier: '):
                classifiers.append(line[len('Classifier: '):])

        package['classifiers'] = classifiers
        if file_list:
            package['files'] = sorted(file_list)
        yield package


def print_results(distributions, list_files=False, verbose=False):
    """
    Print the informations from installed distributions found.
    """
    results_printed = False
    for i, dist in enumerate(distributions):
        results_printed = True
        if i > 0:
            write_output('---')
        write_output('Name: %s', dist.get('name', ''))
        write_output('Version: %s', dist.get('version', ''))
        write_output('Summary: %s', dist.get('summary', ''))
        write_output('Home-page: %s', dist.get('home-page', ''))
        write_output('Author: %s', dist.get('author', ''))
        write_output('Author-email: %s', dist.get('author-email', ''))
        write_output('License: %s', dist.get('license', ''))
        write_output('Location: %s', dist.get('location', ''))
        write_output('Requires: %s', ', '.join(dist.get('requires', [])))
        write_output('Required-by: %s', ', '.join(dist.get('required_by', [])))
        if verbose:
            write_output('Metadata-Version: %s', dist.get('metadata-version', ''))
            write_output('Installer: %s', dist.get('installer', ''))
            write_output('Classifiers:')
            for classifier in dist.get('classifiers', []):
                write_output('  %s', classifier)

            write_output('Entry-points:')
            for entry in dist.get('entry_points', []):
                write_output('  %s', entry.strip())

        if list_files:
            write_output('Files:')
            for line in dist.get('files', []):
                write_output('  %s', line.strip())

            if 'files' not in dist:
                write_output('Cannot locate installed-files.txt')

    return results_printed