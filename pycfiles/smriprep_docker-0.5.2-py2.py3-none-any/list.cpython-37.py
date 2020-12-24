# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-pn36swhz/pip/pip/_internal/commands/list.py
# Compiled at: 2020-02-14 17:24:54
# Size of source mod 2**32: 10563 bytes
from __future__ import absolute_import
import json, logging
from pip._vendor import six
from pip._vendor.six.moves import zip_longest
from pip._internal.cli import cmdoptions
from pip._internal.cli.req_command import IndexGroupCommand
from pip._internal.exceptions import CommandError
from pip._internal.index.package_finder import PackageFinder
from pip._internal.models.selection_prefs import SelectionPreferences
from pip._internal.self_outdated_check import make_link_collector
from pip._internal.utils.misc import dist_is_editable, get_installed_distributions, write_output
from pip._internal.utils.packaging import get_installer
logger = logging.getLogger(__name__)

class ListCommand(IndexGroupCommand):
    __doc__ = '\n    List installed packages, including editables.\n\n    Packages are listed in a case-insensitive sorted order.\n    '
    usage = '\n      %prog [options]'

    def __init__(self, *args, **kw):
        (super(ListCommand, self).__init__)(*args, **kw)
        cmd_opts = self.cmd_opts
        cmd_opts.add_option('-o',
          '--outdated', action='store_true',
          default=False,
          help='List outdated packages')
        cmd_opts.add_option('-u',
          '--uptodate', action='store_true',
          default=False,
          help='List uptodate packages')
        cmd_opts.add_option('-e',
          '--editable', action='store_true',
          default=False,
          help='List editable projects.')
        cmd_opts.add_option('-l',
          '--local', action='store_true',
          default=False,
          help='If in a virtualenv that has global access, do not list globally-installed packages.')
        self.cmd_opts.add_option('--user',
          dest='user',
          action='store_true',
          default=False,
          help='Only output packages installed in user-site.')
        cmd_opts.add_option(cmdoptions.list_path())
        cmd_opts.add_option('--pre',
          action='store_true',
          default=False,
          help='Include pre-release and development versions. By default, pip only finds stable versions.')
        cmd_opts.add_option('--format',
          action='store',
          dest='list_format',
          default='columns',
          choices=('columns', 'freeze', 'json'),
          help='Select the output format among: columns (default), freeze, or json')
        cmd_opts.add_option('--not-required',
          action='store_true',
          dest='not_required',
          help='List packages that are not dependencies of installed packages.')
        cmd_opts.add_option('--exclude-editable',
          action='store_false',
          dest='include_editable',
          help='Exclude editable package from output.')
        cmd_opts.add_option('--include-editable',
          action='store_true',
          dest='include_editable',
          help='Include editable package from output.',
          default=True)
        index_opts = cmdoptions.make_option_group(cmdoptions.index_group, self.parser)
        self.parser.insert_option_group(0, index_opts)
        self.parser.insert_option_group(0, cmd_opts)

    def _build_package_finder(self, options, session):
        """
        Create a package finder appropriate to this list command.
        """
        link_collector = make_link_collector(session, options=options)
        selection_prefs = SelectionPreferences(allow_yanked=False,
          allow_all_prereleases=(options.pre))
        return PackageFinder.create(link_collector=link_collector,
          selection_prefs=selection_prefs)

    def run(self, options, args):
        if options.outdated:
            if options.uptodate:
                raise CommandError('Options --outdated and --uptodate cannot be combined.')
        else:
            cmdoptions.check_list_path_option(options)
            packages = get_installed_distributions(local_only=(options.local),
              user_only=(options.user),
              editables_only=(options.editable),
              include_editables=(options.include_editable),
              paths=(options.path))
            if options.not_required:
                packages = self.get_not_required(packages, options)
            if options.outdated:
                packages = self.get_outdated(packages, options)
            else:
                if options.uptodate:
                    packages = self.get_uptodate(packages, options)
        self.output_package_listing(packages, options)

    def get_outdated(self, packages, options):
        return [dist for dist in self.iter_packages_latest_infos(packages, options) if dist.latest_version > dist.parsed_version]

    def get_uptodate(self, packages, options):
        return [dist for dist in self.iter_packages_latest_infos(packages, options) if dist.latest_version == dist.parsed_version]

    def get_not_required(self, packages, options):
        dep_keys = set()
        for dist in packages:
            dep_keys.update((requirement.key for requirement in dist.requires()))

        return {pkg for pkg in packages if pkg.key not in dep_keys}

    def iter_packages_latest_infos(self, packages, options):
        with self._build_session(options) as (session):
            finder = self._build_package_finder(options, session)
            for dist in packages:
                typ = 'unknown'
                all_candidates = finder.find_all_candidates(dist.key)
                if not options.pre:
                    all_candidates = [candidate for candidate in all_candidates if not candidate.version.is_prerelease]
                else:
                    evaluator = finder.make_candidate_evaluator(project_name=(dist.project_name))
                    best_candidate = evaluator.sort_best_candidate(all_candidates)
                    if best_candidate is None:
                        continue
                    remote_version = best_candidate.version
                    if best_candidate.link.is_wheel:
                        typ = 'wheel'
                    else:
                        typ = 'sdist'
                dist.latest_version = remote_version
                dist.latest_filetype = typ
                yield dist

    def output_package_listing--- This code section failed: ---

 L. 212         0  LOAD_GLOBAL              sorted

 L. 213         2  LOAD_FAST                'packages'

 L. 214         4  LOAD_LAMBDA              '<code_object <lambda>>'
                6  LOAD_STR                 'ListCommand.output_package_listing.<locals>.<lambda>'
                8  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               10  LOAD_CONST               ('key',)
               12  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               14  STORE_FAST               'packages'

 L. 216        16  LOAD_FAST                'options'
               18  LOAD_ATTR                list_format
               20  LOAD_STR                 'columns'
               22  COMPARE_OP               ==
               24  POP_JUMP_IF_FALSE    58  'to 58'
               26  LOAD_FAST                'packages'
               28  POP_JUMP_IF_FALSE    58  'to 58'

 L. 217        30  LOAD_GLOBAL              format_for_columns
               32  LOAD_FAST                'packages'
               34  LOAD_FAST                'options'
               36  CALL_FUNCTION_2       2  '2 positional arguments'
               38  UNPACK_SEQUENCE_2     2 
               40  STORE_FAST               'data'
               42  STORE_FAST               'header'

 L. 218        44  LOAD_FAST                'self'
               46  LOAD_METHOD              output_package_listing_columns
               48  LOAD_FAST                'data'
               50  LOAD_FAST                'header'
               52  CALL_METHOD_2         2  '2 positional arguments'
               54  POP_TOP          
               56  JUMP_FORWARD        156  'to 156'
             58_0  COME_FROM            28  '28'
             58_1  COME_FROM            24  '24'

 L. 219        58  LOAD_FAST                'options'
               60  LOAD_ATTR                list_format
               62  LOAD_STR                 'freeze'
               64  COMPARE_OP               ==
               66  POP_JUMP_IF_FALSE   132  'to 132'

 L. 220        68  SETUP_LOOP          156  'to 156'
               70  LOAD_FAST                'packages'
               72  GET_ITER         
               74  FOR_ITER            128  'to 128'
               76  STORE_FAST               'dist'

 L. 221        78  LOAD_FAST                'options'
               80  LOAD_ATTR                verbose
               82  LOAD_CONST               1
               84  COMPARE_OP               >=
               86  POP_JUMP_IF_FALSE   110  'to 110'

 L. 222        88  LOAD_GLOBAL              write_output
               90  LOAD_STR                 '%s==%s (%s)'
               92  LOAD_FAST                'dist'
               94  LOAD_ATTR                project_name

 L. 223        96  LOAD_FAST                'dist'
               98  LOAD_ATTR                version
              100  LOAD_FAST                'dist'
              102  LOAD_ATTR                location
              104  CALL_FUNCTION_4       4  '4 positional arguments'
              106  POP_TOP          
              108  JUMP_BACK            74  'to 74'
            110_0  COME_FROM            86  '86'

 L. 225       110  LOAD_GLOBAL              write_output
              112  LOAD_STR                 '%s==%s'
              114  LOAD_FAST                'dist'
              116  LOAD_ATTR                project_name
              118  LOAD_FAST                'dist'
              120  LOAD_ATTR                version
              122  CALL_FUNCTION_3       3  '3 positional arguments'
              124  POP_TOP          
              126  JUMP_BACK            74  'to 74'
              128  POP_BLOCK        
              130  JUMP_FORWARD        156  'to 156'
            132_0  COME_FROM            66  '66'

 L. 226       132  LOAD_FAST                'options'
              134  LOAD_ATTR                list_format
              136  LOAD_STR                 'json'
              138  COMPARE_OP               ==
              140  POP_JUMP_IF_FALSE   156  'to 156'

 L. 227       142  LOAD_GLOBAL              write_output
              144  LOAD_GLOBAL              format_for_json
              146  LOAD_FAST                'packages'
              148  LOAD_FAST                'options'
              150  CALL_FUNCTION_2       2  '2 positional arguments'
              152  CALL_FUNCTION_1       1  '1 positional argument'
              154  POP_TOP          
            156_0  COME_FROM           140  '140'
            156_1  COME_FROM           130  '130'
            156_2  COME_FROM_LOOP       68  '68'
            156_3  COME_FROM            56  '56'

Parse error at or near `COME_FROM_LOOP' instruction at offset 156_2

    def output_package_listing_columns(self, data, header):
        if len(data) > 0:
            data.insert(0, header)
        pkg_strings, sizes = tabulate(data)
        if len(data) > 0:
            pkg_strings.insert(1, ' '.join(map(lambda x: '-' * x, sizes)))
        for val in pkg_strings:
            write_output(val)


def tabulate(vals):
    assert len(vals) > 0
    sizes = [
     0] * max((len(x) for x in vals))
    for row in vals:
        sizes = [max(s, len(str(c))) for s, c in zip_longest(sizes, row)]

    result = []
    for row in vals:
        display = ' '.join([str(c).ljust(s) if c is not None else '' for s, c in zip_longest(sizes, row)])
        result.append(display)

    return (result, sizes)


def format_for_columns(pkgs, options):
    """
    Convert the package data into something usable
    by output_package_listing_columns.
    """
    running_outdated = options.outdated
    if running_outdated:
        header = [
         'Package', 'Version', 'Latest', 'Type']
    else:
        header = [
         'Package', 'Version']
    data = []
    if options.verbose >= 1 or any((dist_is_editable(x) for x in pkgs)):
        header.append('Location')
    if options.verbose >= 1:
        header.append('Installer')
    for proj in pkgs:
        row = [
         proj.project_name, proj.version]
        if running_outdated:
            row.append(proj.latest_version)
            row.append(proj.latest_filetype)
        if not options.verbose >= 1:
            if dist_is_editable(proj):
                row.append(proj.location)
            if options.verbose >= 1:
                row.append(get_installer(proj))
            data.append(row)

    return (
     data, header)


def format_for_json(packages, options):
    data = []
    for dist in packages:
        info = {'name':dist.project_name, 
         'version':six.text_type(dist.version)}
        if options.verbose >= 1:
            info['location'] = dist.location
            info['installer'] = get_installer(dist)
        if options.outdated:
            info['latest_version'] = six.text_type(dist.latest_version)
            info['latest_filetype'] = dist.latest_filetype
        data.append(info)

    return json.dumps(data)