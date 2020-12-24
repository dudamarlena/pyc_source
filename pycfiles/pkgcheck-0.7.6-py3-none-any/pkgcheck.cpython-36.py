# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/runner/work/pkgcheck/pkgcheck/build/lib/pkgcheck/scripts/pkgcheck.py
# Compiled at: 2020-02-09 15:46:32
# Size of source mod 2**32: 38420 bytes
r"""
pkgcore-based QA utility for ebuild repos

pkgcheck is a QA utility based on **pkgcore**\(5) that supports scanning
ebuild repositories for various issues.
"""
import argparse, os, sys, textwrap
from collections import defaultdict
from functools import partial
from itertools import chain
from operator import attrgetter
from pkgcore import const as pkgcore_const
from pkgcore.repository import multiplex
from pkgcore.restrictions import boolean, packages
from pkgcore.restrictions.util import collect_package_restrictions
from pkgcore.util import commandline, parserestrict
from snakeoil.cli import arghparse
from snakeoil.cli.exceptions import UserException
from snakeoil.formatters import decorate_forced_wrapping
from snakeoil.osutils import abspath, pjoin
from snakeoil.strings import pluralism
from .. import base, const, objects, pipeline, reporters, results
from ..caches import CachedAddon
from ..addons import init_addon
from ..checks import NetworkCheck, init_checks
from ..cli import ConfigArgumentParser
from ..log import logger
pkgcore_config_opts = commandline.ArgumentParser(script=(__file__, __name__))
argparser = ConfigArgumentParser(suppress=True,
  description=__doc__,
  parents=(pkgcore_config_opts,),
  script=(
 __file__, __name__))
argparser.set_defaults(profile_override=(pjoin(pkgcore_const.DATA_PATH, 'stubrepo/profiles/default')))
subparsers = argparser.add_subparsers(description='check applets')
reporter_argparser = commandline.ArgumentParser(suppress=True)
reporter_options = reporter_argparser.add_argument_group('reporter options')
reporter_options.add_argument('-R',
  '--reporter', action='store', default=None, help='use a non-default reporter',
  docs='\n        Select a reporter to use for output.\n\n        Use ``pkgcheck show --reporters`` to see available options.\n    ')
reporter_options.add_argument('--format',
  dest='format_str', action='store', default=None, help='format string used with FormatReporter',
  docs="\n        Custom format string used to format output by FormatReporter.\n\n        Supports python format string syntax where result object attribute names\n        surrounded by curly braces are replaced with their values (if they exist).\n\n        For example, ``--format '{category}/{package}/{package}-{version}.ebuild``\n        will output ebuild paths in the target repo for results relating to\n        specific ebuild versions. If a result is for the generic package (or a\n        higher scope), no output will be produced for that result.\n\n        Furthermore, no output will be produced if a result object is missing any\n        requested attribute expansion in the format string. In other words,\n        ``--format {foo}`` will never produce any output because no result has the\n        ``foo`` attribute.\n    ")

@reporter_argparser.bind_final_check
def _setup_reporter(parser, namespace):
    if namespace.reporter is None:
        namespace.reporter = sorted((objects.REPORTERS.values()),
          key=(attrgetter('priority')), reverse=True)[0]
    else:
        try:
            namespace.reporter = objects.REPORTERS[namespace.reporter]
        except KeyError:
            available = ', '.join(objects.REPORTERS)
            parser.error(f"no reporter matches {namespace.reporter!r} (available: {available})")

        if namespace.reporter is reporters.FormatReporter:
            if not namespace.format_str:
                parser.error('missing or empty --format option required by FormatReporter')
            namespace.reporter = partial(namespace.reporter, namespace.format_str)
        elif namespace.format_str is not None:
            parser.error('--format option is only valid when using FormatReporter')


class CacheNegations(arghparse.CommaSeparatedNegations):
    __doc__ = 'Split comma-separated enabled and disabled cache types.'
    default = {cache.type:True for cache in CachedAddon.caches.values()}

    def parse_values(self, values):
        all_cache_types = {cache.type for cache in CachedAddon.caches.values()}
        disabled, enabled = [], list(all_cache_types)
        if values is None or values in ('y', 'yes', 'true'):
            pass
        else:
            if values in ('n', 'no', 'false'):
                disabled = list(all_cache_types)
            else:
                disabled, enabled = super().parse_values(values)
            disabled = set(disabled)
            enabled = set(enabled) if enabled else all_cache_types
            unknown = (disabled | enabled) - all_cache_types
            if unknown:
                unknowns = ', '.join(map(repr, unknown))
                choices = ', '.join(map(repr, sorted(self.default)))
                s = pluralism(unknown)
                raise argparse.ArgumentError(self, f"unknown cache type{s}: {unknowns} (choose from {choices})")
            enabled = set(enabled).difference(disabled)
            return enabled

    def __call__(self, parser, namespace, values, option_string=None):
        enabled = self.parse_values(values)
        caches = {}
        for cache in CachedAddon.caches.values():
            caches[cache.type] = cache.type in enabled

        setattr(namespace, self.dest, caches)


scan = subparsers.add_parser('scan',
  parents=(reporter_argparser,), description='scan targets for QA issues',
  configs=(
 const.SYSTEM_CONF_FILE, const.USER_CONF_FILE))
scan.add_argument('targets',
  metavar='TARGET', nargs='*', help='optional target atom(s)')
main_options = scan.add_argument_group('main options')
main_options.add_argument('--config',
  dest='config_file', help='config file to load scan settings from')
main_options.add_argument('-r',
  '--repo', metavar='REPO', dest='target_repo', action=(commandline.StoreRepoObject),
  repo_type='ebuild-raw',
  allow_external_repos=True,
  help='repo to pull packages from')
main_options.add_argument('-f',
  '--filter', choices=('latest', 'repo'), help='limit targeted packages for scanning',
  docs="\n        Support limiting targeted packages for scanning using a chosen filter.\n\n        If the 'repo' argument is used, all package visibility mechanisms used\n        by the package manager when resolving package dependencies such as\n        ACCEPT_KEYWORDS, ACCEPT_LICENSE, and package.mask will be enabled.\n\n        If the 'latest' argument is used, only the latest package per slot of\n        both VCS and non-VCS types will be scanned.\n    ")
main_options.add_argument('--sorted',
  action='store_true', help='sort all generated results',
  docs='\n        Globally sort all generated results. Note that this is only useful for\n        limited runs (e.g. using -k to restrict output to a single result type)\n        since it causes all generated results to be stored in memory and sorts\n        on a global scope.\n    ')
main_options.add_argument('-j',
  '--jobs', type=(arghparse.positive_int), default=(os.cpu_count()), help='number of checks to run in parallel',
  docs='\n        Number of checks to run in parallel, defaults to using all available\n        processors.\n    ')
main_options.add_argument('-t',
  '--tasks', type=(arghparse.positive_int), default=(os.cpu_count() * 5), help='number of asynchronous tasks to run concurrently',
  docs='\n        Number of asynchronous tasks to run concurrently (defaults to 5 * CPU count).\n    ')
main_options.add_argument('--cache',
  action=CacheNegations, default=(CacheNegations.default), help='forcibly enable/disable caches',
  docs="\n        All cache types are enabled by default, this option explicitly sets\n        which caches will be generated and used during scanning.\n\n        To enable only certain cache types, specify them in a comma-separated\n        list, e.g. ``--cache git,profiles`` will enable both the git and\n        profiles caches.\n\n        To disable specific cache types prefix them with ``-``. Note\n        that when starting the argument list with a disabled value an equals\n        sign must be used, e.g. ``--cache=-git``, otherwise the disabled\n        argument is treated as an option.\n\n        In order to disable all cache usage, it's easiest to use ``--cache no``\n        instead of explicitly listing all disabled cache types.\n\n        When disabled, no caches will be saved to disk and results requiring\n        caches (e.g. git-related checks) will be skipped.\n    ")

class ScopeArgs(arghparse.CommaSeparatedNegations):
    __doc__ = 'Filter enabled keywords by selected scopes.'

    def __call__(self, parser, namespace, values, option_string=None):
        disabled, enabled = self.parse_values(values)
        unknown_scopes = set(disabled + enabled) - set(base.scopes)
        if unknown_scopes:
            unknown = ', '.join(map(repr, unknown_scopes))
            available = ', '.join(base.scopes)
            s = pluralism(unknown_scopes)
            raise argparse.ArgumentError(self, f"unknown scope{s}: {unknown} (available scopes: {available})")
        disabled = {base.scopes[x] for x in disabled}
        enabled = {base.scopes[x] for x in enabled}
        setattr(namespace, self.dest, (disabled, enabled))


class KeywordArgs(arghparse.CommaSeparatedNegations):
    __doc__ = 'Filter enabled keywords by selected keywords.'

    def __call__(self, parser, namespace, values, option_string=None):
        disabled, enabled = self.parse_values(values)
        error = (k for k, v in objects.KEYWORDS.items() if issubclass(v, results.Error))
        warning = (k for k, v in objects.KEYWORDS.items() if issubclass(v, results.Warning))
        info = (k for k, v in objects.KEYWORDS.items() if issubclass(v, results.Info))
        alias_map = {'error':error, 
         'warning':warning,  'info':info}
        replace_aliases = lambda x: alias_map.get(x, [x])
        disabled = list(chain.from_iterable(map(replace_aliases, disabled)))
        enabled = list(chain.from_iterable(map(replace_aliases, enabled)))
        unknown_keywords = set(disabled + enabled) - set(objects.KEYWORDS)
        if unknown_keywords:
            unknown = ', '.join(map(repr, unknown_keywords))
            s = pluralism(unknown_keywords)
            raise argparse.ArgumentError(self, f"unknown keyword{s}: {unknown}")
        setattr(namespace, self.dest, (disabled, enabled))


class CheckArgs(arghparse.CommaSeparatedNegations):
    __doc__ = 'Determine checks to run on selection.'

    def __call__(self, parser, namespace, values, option_string=None):
        disabled, enabled = self.parse_values(values)
        available = set(objects.CHECKS)
        network = (c for c, v in objects.CHECKS.items() if issubclass(v, NetworkCheck))
        alias_map = {'all':available, 
         'net':network}
        replace_aliases = lambda x: alias_map.get(x, [x])
        disabled = set(chain.from_iterable(map(replace_aliases, disabled)))
        enabled = set(chain.from_iterable(map(replace_aliases, enabled)))
        unknown_checks = (disabled | enabled) - available
        if unknown_checks:
            unknown = ', '.join(map(repr, unknown_checks))
            s = pluralism(unknown_checks)
            raise argparse.ArgumentError(self, f"unknown check{s}: {unknown}")
        setattr(namespace, self.dest, (disabled, enabled))


check_options = scan.add_argument_group('check selection')
check_options.add_argument('-c',
  '--checks', metavar='CHECK', action=CheckArgs, dest='selected_checks', help='limit checks to run (comma-separated list)',
  docs='\n        Comma separated list of checks to enable and disable for\n        scanning. Any checks specified in this fashion will be the\n        only checks that get run, skipping any disabled checks.\n\n        To specify disabled checks prefix them with ``-``. Note that when\n        starting the argument list with a disabled check an equals sign must\n        be used, e.g. ``-c=-check``, otherwise the disabled check argument is\n        treated as an option.\n\n        The special argument of ``all`` corresponds to the list of all checks.\n        Therefore, to forcibly enable all checks use ``-c all``.\n\n        In addition, all network-related checks (which are disabled by default)\n        can be enabled using ``-c net``. This allows for easily running only\n        network checks without having to explicitly list them.\n\n        Use ``pkgcheck show --checks`` see available options.\n    ')
check_options.add_argument('-k',
  '--keywords', metavar='KEYWORD', action=KeywordArgs, dest='selected_keywords', help='limit keywords to scan for (comma-separated list)',
  docs='\n        Comma separated list of keywords to enable and disable for\n        scanning. Any keywords specified in this fashion will be the\n        only keywords that get reported, skipping any disabled keywords.\n\n        To specify disabled keywords prefix them with ``-``. Note that when\n        starting the argument list with a disabled keyword an equals sign must\n        be used, e.g. ``-k=-keyword``, otherwise the disabled keyword argument is\n        treated as an option.\n\n        The special arguments of ``error``, ``warning``, and ``info``\n        correspond to the lists of error, warning, and info keywords,\n        respectively. For example, to only scan for errors use ``-k error``.\n\n        Use ``pkgcheck show --keywords`` to see available options.\n    ')
check_options.add_argument('-s',
  '--scopes', metavar='SCOPE', action=ScopeArgs, dest='selected_scopes', help='limit keywords to scan for by scope (comma-separated list)',
  docs=('\n        Comma separated list of scopes to enable and disable for scanning. Any\n        scopes specified in this fashion will affect the keywords that get\n        reported. For example, running pkgcheck with only the repo scope\n        enabled will cause only repo-level keywords to be scanned for and\n        reported.\n\n        To specify disabled scopes prefix them with ``-`` similar to the\n        -k/--keywords option.\n\n        Available scopes: %s\n    ' % ', '.join(base.scopes)))
check_options.add_argument('--net',
  action='store_true', help='run checks that require internet access')
scan.plugin = scan.add_argument_group('plugin options')

def _determine_target_repo(namespace, parser):
    """Determine a target repo when none was explicitly selected.

    Returns a repository object if a matching one is found, otherwise None.
    """
    target_dir = namespace.cwd
    if namespace.targets:
        if len(namespace.targets) == 1:
            initial_target = namespace.targets[0]
            if os.path.exists(initial_target):
                target = os.path.abspath(initial_target)
                if os.path.isfile(target):
                    target = os.path.dirname(target)
                target_dir = target
            else:
                for repo in namespace.domain.ebuild_repos_raw:
                    if initial_target == repo.repo_id:
                        return repo

    for repo in namespace.domain.ebuild_repos_raw:
        if target_dir in repo:
            return repo

    return namespace.domain.find_repo(target_dir,
      config=(namespace.config), configure=False)


def _path_restrict(path, namespace):
    """Generate custom package restriction from a given path.

    This drops the repo restriction (initial entry in path restrictions)
    since runs can only be made against single repo targets so the extra
    restriction is redundant and breaks several custom sources involving
    raw pkgs (lacking a repo attr) or faked repos.
    """
    repo = namespace.target_repo
    restrictions = []
    path = os.path.realpath(path)
    try:
        restrictions = repo.path_restrict(path)[1:]
    except ValueError as e:
        raise UserException(str(e))

    restrict = (packages.AndRestriction)(*restrictions) if restrictions else packages.AlwaysTrue
    for scope in (x for x in base.scopes.values() if x.level == 0):
        scope_path = pjoin(namespace.target_repo.location, scope.desc)
        if path.startswith(scope_path):
            break
    else:
        scope = _restrict_to_scope(restrict)

    return (scope, restrict)


def _restrict_to_scope(restrict):
    """Determine a given restriction's scope level."""
    for scope, attrs in (
     (
      base.version_scope, ['fullver', 'version', 'rev']),
     (
      base.package_scope, ['package']),
     (
      base.category_scope, ['category'])):
        if any(collect_package_restrictions(restrict, attrs)):
            return scope

    return base.repo_scope


@scan.bind_reset_defaults
def _setup_scan_defaults(parser, namespace):
    """Re-initialize default namespace settings per arg parsing run."""
    namespace.forced_checks = []


def add_addon(addon, addon_set):
    """Determine the set of required addons for a given addon."""
    if addon not in addon_set:
        addon_set.add(addon)
        for dep in addon.required_addons:
            add_addon(dep, addon_set)


@scan.bind_pre_parse
def _setup_scan_addons(parser, namespace):
    """Load all checks and their argparser changes before parsing."""
    all_addons = set()
    for check in objects.CHECKS.values():
        add_addon(check, all_addons)

    for addon in all_addons:
        addon.mangle_argparser(parser)


@scan.bind_early_parse
def _setup_scan(parser, namespace, args):
    namespace = parser.parse_config_options(namespace)
    namespace, _ = parser._parse_known_args(args, namespace)
    try:
        namespace.cwd = abspath(os.getcwd())
    except FileNotFoundError as e:
        namespace.cwd = '/'

    if namespace.target_repo is None:
        target_repo = _determine_target_repo(namespace, parser)
        if target_repo is None:
            target_repo = namespace.config.get_default('repo')
        namespace.target_repo = target_repo
    if namespace.filter == 'repo':
        namespace.target_repo = namespace.domain.ebuild_repos[namespace.target_repo.repo_id]
    namespace.gentoo_repo = 'gentoo' in namespace.target_repo.aliases
    namespace.search_repo = (multiplex.tree)(*namespace.target_repo.trees)
    repo_config_file = os.path.join(namespace.target_repo.location, 'metadata', 'pkgcheck.conf')
    if namespace.config_file is not None:
        if namespace.config_file.lower() in ('false', 'no', 'n'):
            parser.configs = ()
        else:
            parser.configs = (
             namespace.config_file,)
    else:
        if os.path.isfile(repo_config_file):
            parser.configs += (repo_config_file,)
        for section in namespace.target_repo.aliases:
            if section in parser.config:
                namespace = parser.parse_config_options(namespace, section)
                break

        return (
         namespace, args)


@scan.bind_final_check
def _validate_scan_args(parser, namespace):
    cwd_in_repo = namespace.cwd in namespace.target_repo
    if namespace.targets:
        repo = namespace.target_repo
        if len(namespace.targets) == 1:
            if namespace.targets[0] == '-':

                def stdin():
                    while True:
                        line = sys.stdin.readline()
                        if not line:
                            break
                        yield line.rstrip()

                namespace.targets = stdin()

        def restrictions():
            for target in namespace.targets:
                if os.path.isabs(target) or os.path.exists(target) and cwd_in_repo:
                    try:
                        scope, restrict = _path_restrict(target, namespace)
                    except ValueError as e:
                        parser.error(e)

                else:
                    try:
                        restrict = parserestrict.parse_match(target)
                        scope = _restrict_to_scope(restrict)
                    except parserestrict.ParseError as e:
                        parser.error(e)

                    yield (
                     scope, restrict)

        namespace.restrictions = restrictions()
        if isinstance(namespace.targets, list):
            namespace.restrictions = list(namespace.restrictions)
            if len(namespace.restrictions) > 1:
                scopes = {scope for scope, restrict in namespace.restrictions}
                if len(scopes) > 1:
                    scan_scopes = ', '.join(sorted(map(str, scopes)))
                    parser.error(f"targets specify multiple scan scope levels: {scan_scopes}")
                combined_restrict = (boolean.OrRestriction)(*(r for s, r in namespace.restrictions))
                namespace.restrictions = [(scopes.pop(), combined_restrict)]
    else:
        if cwd_in_repo:
            scope, restrict = _path_restrict(namespace.cwd, namespace)
        else:
            restrict = packages.AlwaysTrue
            scope = base.repo_scope
        namespace.restrictions = [
         (
          scope, restrict)]
    namespace.enabled_checks = set()
    namespace.disabled_keywords = set()
    namespace.enabled_keywords = set()
    if namespace.selected_scopes is not None:
        namespace.disabled_keywords |= {k for k in objects.KEYWORDS.values() if k.scope in namespace.selected_scopes[0]}
        namespace.enabled_keywords |= {k for k in objects.KEYWORDS.values() if k.scope in namespace.selected_scopes[1]}
    if namespace.selected_checks is not None:
        if namespace.selected_checks[1]:
            namespace.enabled_checks |= {objects.CHECKS[c] for c in namespace.selected_checks[1]}
        elif namespace.selected_checks[0]:
            namespace.enabled_checks = set(objects.CHECKS.values()) - {objects.CHECKS[c] for c in namespace.selected_checks[0]}
    if namespace.selected_keywords is not None:
        namespace.disabled_keywords |= {objects.KEYWORDS[k] for k in namespace.selected_keywords[0]}
        namespace.enabled_keywords |= {objects.KEYWORDS[k] for k in namespace.selected_keywords[1]}
    namespace.filtered_keywords = None
    if namespace.enabled_keywords or namespace.disabled_keywords:
        if not namespace.enabled_keywords:
            namespace.enabled_keywords = set(objects.KEYWORDS.values())
        namespace.filtered_keywords = {}
        for keyword in namespace.enabled_keywords - namespace.disabled_keywords:
            for check in objects.CHECKS.values():
                for result in check.known_results:
                    if issubclass(result, keyword):
                        namespace.filtered_keywords[result] = check

        if not namespace.enabled_checks:
            namespace.enabled_checks = frozenset(namespace.filtered_keywords.values())
        namespace.filtered_keywords = frozenset(namespace.filtered_keywords)
    if not namespace.enabled_checks:
        namespace.enabled_checks = list(objects.CHECKS.values())
    namespace.enabled_checks = [c for c in namespace.enabled_checks if not c.skip(namespace)]
    if namespace.filter is not None:
        namespace.enabled_checks = [c for c in namespace.enabled_checks if c.scope is base.version_scope]
    if not namespace.enabled_checks:
        parser.error('no active checks')
    namespace.addons = set()
    for check in namespace.enabled_checks:
        add_addon(check, namespace.addons)

    try:
        for addon in namespace.addons:
            addon.check_args(parser, namespace)

    except argparse.ArgumentError as e:
        if namespace.debug:
            raise
        parser.error(str(e))


def _selected_check(options, scan_scope, scope):
    """Verify check scope against current scan scope to determine check activation."""
    if scope == 0:
        if options.selected_scopes is None:
            if scan_scope is base.repo_scope or scope is scan_scope:
                return True
            else:
                if scope in options.selected_scopes[1]:
                    return True
        else:
            if scan_scope > 0:
                if scope >= scan_scope:
                    return True
    elif options.commits:
        if scan_scope != 0:
            if scope is base.commit_scope:
                return True
    return False


@scan.bind_main_func
def _scan(options, out, err):
    enabled_checks, caches = init_checks(options.pop('addons'), options)
    if options.verbosity >= 1:
        msg = f"target repo: {options.target_repo.repo_id!r}"
        if options.target_repo.repo_id != options.target_repo.location:
            msg += f" at {options.target_repo.location!r}"
        err.write(msg)
    if caches:
        CachedAddon.update_caches(options, caches)
    with options.reporter(out, verbosity=(options.verbosity), keywords=(options.filtered_keywords)) as (reporter):
        for scan_scope, restrict in options.restrictions:
            pipes = [d for scope, d in enabled_checks.items() if _selected_check(options, scan_scope, scope)]
            if not pipes:
                err.write(f"{scan.prog}: no matching checks available for {scan_scope} scope")
            else:
                if options.verbosity >= 1:
                    err.write(f"Running {len(pipes)} tests")
                if options.debug:
                    err.write(f"restriction: {restrict}")
                err.flush()
                pipe = pipeline.Pipeline(options, scan_scope, pipes, restrict)
                reporter(pipe, sort=(options.sorted))

    return 0


cache = subparsers.add_parser('cache',
  description='update/remove pkgcheck caches', docs='\n        Caches of various types are used by pkgcheck. This command allows the\n        user to manually force cache updates or removals.\n    ')
cache_actions = cache.add_mutually_exclusive_group()
cache_actions.add_argument('-u',
  '--update', dest='update_cache', action='store_true', help='update caches')
cache_actions.add_argument('-r',
  '--remove', dest='remove_cache', action='store_true', help='forcibly remove caches')
cache.add_argument('-f',
  '--force', dest='force_cache', action='store_true', help='forcibly update/remove caches')
cache.add_argument('-n',
  '--dry-run', action='store_true', help='dry run without performing any changes')
cache.add_argument('-t',
  '--type', dest='cache', action=CacheNegations,
  default=(CacheNegations.default),
  help='target cache types')

@cache.bind_pre_parse
def _setup_cache_addons(parser, namespace):
    """Load all addons using caches and their argparser changes before parsing."""
    all_addons = set()
    cache_addons = set()
    for addon in CachedAddon.caches:
        cache_addons.add(addon)
        add_addon(addon, all_addons)

    for addon in all_addons:
        addon.mangle_argparser(parser)

    namespace.cache_addons = cache_addons


@cache.bind_final_check
def _validate_cache_args(parser, namespace):
    namespace.cache_addons = [addon for addon in namespace.cache_addons if namespace.cache.get(addon.cache.type, False)]
    namespace.target_repo = namespace.config.get_default('repo')
    try:
        for addon in namespace.cache_addons:
            addon.check_args(parser, namespace)

    except argparse.ArgumentError as e:
        if namespace.debug:
            raise
        parser.error(str(e))


@cache.bind_main_func
def _cache(options, out, err):
    ret = 0
    if options.remove_cache:
        ret = CachedAddon.remove_caches(options)
    else:
        if options.update_cache:
            caches = [init_addon(addon, options) for addon in options.pop('cache_addons')]
            ret = CachedAddon.update_caches(options, caches)
        else:
            repos_dir = pjoin(const.USER_CACHE_DIR, 'repos')
            for cache_type, paths in CachedAddon.existing().items():
                if options.cache.get(cache_type, False):
                    if paths:
                        out.write(out.fg('yellow'), f"{cache_type} caches: ", out.reset)
                    for path in paths:
                        repo = str(path.parent)[len(repos_dir):]
                        if repo.count(os.sep) == 1:
                            repo = repo.lstrip(os.sep)
                        out.write(repo)

    return ret


replay = subparsers.add_parser('replay',
  parents=(reporter_argparser,), description='replay result streams',
  docs='\n        Replay previous result streams, feeding the results into a reporter.\n        Currently supports replaying streams from PickleStream or JsonStream\n        reporters.\n\n        Useful if you need to delay acting on results until it can be done in\n        one minimal window, e.g. updating a database, or want to generate\n        several different reports.\n    ')
replay.add_argument(dest='results',
  metavar='FILE',
  type=(arghparse.FileType('rb')),
  help='path to serialized results file')

@replay.bind_main_func
def _replay(options, out, err):
    processed = 0
    exc = None
    with options.reporter(out) as (reporter):
        try:
            for result in reporters.JsonStream.from_file(options.results):
                reporter.report(result)
                processed += 1

        except reporters.DeserializationError as e:
            if not processed:
                options.results.seek(0)
                try:
                    for result in reporters.PickleStream.from_file(options.results):
                        reporter.report(result)
                        processed += 1

                except reporters.DeserializationError as e:
                    exc = e

            else:
                exc = e

    if exc:
        if not processed:
            raise UserException('invalid or unsupported replay file')
        raise UserException(f"corrupted results file {options.results.name!r}: {exc}")
    return 0


def dump_docstring(out, obj, prefix=None):
    if prefix is not None:
        out.first_prefix.append(prefix)
        out.later_prefix.append(prefix)
    try:
        if obj.__doc__ is None:
            raise ValueError('no docs for {obj!r}')
        else:
            lines = obj.__doc__.split('\n')
            firstline = lines[0].strip()
            if firstline:
                out.write(firstline)
            if len(lines) > 1:
                for line in textwrap.dedent('\n'.join(lines[1:])).split('\n'):
                    out.write(line)

            else:
                out.write()
    finally:
        if prefix is not None:
            out.first_prefix.pop()
            out.later_prefix.pop()


@decorate_forced_wrapping()
def display_keywords(out, options):
    if options.verbosity < 1:
        out.write(('\n'.join(sorted(objects.KEYWORDS))), wrap=False)
    else:
        scopes = defaultdict(set)
        for keyword in objects.KEYWORDS.values():
            scopes[keyword.scope].add(keyword)

        for scope in reversed(sorted(scopes)):
            out.write(out.bold, f"{str(scope).capitalize()} scope:")
            out.write()
            keywords = sorted((scopes[scope]), key=(attrgetter('__name__')))
            try:
                out.first_prefix.append('  ')
                out.later_prefix.append('  ')
                for keyword in keywords:
                    out.write(out.fg(keyword.color), keyword.__name__, out.reset, ':')
                    dump_docstring(out, keyword, prefix='  ')

            finally:
                out.first_prefix.pop()
                out.later_prefix.pop()


@decorate_forced_wrapping()
def display_checks(out, options):
    if options.verbosity < 1:
        out.write(('\n'.join(sorted(objects.CHECKS))), wrap=False)
    else:
        d = defaultdict(list)
        for x in objects.CHECKS.values():
            d[x.__module__].append(x)

        for module_name in sorted(d):
            out.write(out.bold, f"{module_name}:")
            out.write()
            l = d[module_name]
            l.sort(key=(attrgetter('__name__')))
            try:
                out.first_prefix.append('  ')
                out.later_prefix.append('  ')
                for check in l:
                    out.write(out.fg('yellow'), check.__name__, out.reset, ':')
                    dump_docstring(out, check, prefix='  ')
                    keywords = []
                    for r in sorted((check.known_results), key=(attrgetter('__name__'))):
                        keywords.extend([out.fg(r.color), r.__name__, out.reset, ', '])

                    keywords.pop()
                    (out.write)(*['  (known results: '] + keywords + [')'])
                    out.write()

            finally:
                out.first_prefix.pop()
                out.later_prefix.pop()


@decorate_forced_wrapping()
def display_reporters(out, options):
    if options.verbosity < 1:
        out.write(('\n'.join(sorted(objects.REPORTERS))), wrap=False)
    else:
        out.write()
        out.write('reporters:')
        out.write()
        out.first_prefix.append('  ')
        out.later_prefix.append('  ')
        for reporter in sorted((objects.REPORTERS.values()), key=(attrgetter('__name__'))):
            out.write(out.bold, out.fg('yellow'), reporter.__name__)
            dump_docstring(out, reporter, prefix='  ')


show = subparsers.add_parser('show', description='show various pkgcheck info')
list_options = show.add_argument_group('list options')
output_types = list_options.add_mutually_exclusive_group()
output_types.add_argument('--keywords',
  action='store_true', default=False, help='show available warning/error keywords',
  docs='\n        List all available keywords.\n\n        Use -v/--verbose to show keywords sorted into the scope they run at\n        (repository, category, package, or version) along with their\n        descriptions.\n    ')
output_types.add_argument('--checks',
  action='store_true', default=False, help='show available checks',
  docs='\n        List all available checks.\n\n        Use -v/--verbose to show descriptions and possible keyword results for\n        each check.\n    ')
output_types.add_argument('--scopes',
  action='store_true', default=False, help='show available keyword/check scopes',
  docs='\n        List all available keyword and check scopes.\n\n        Use -v/--verbose to show scope descriptions.\n    ')
output_types.add_argument('--reporters',
  action='store_true', default=False, help='show available reporters',
  docs='\n        List all available reporters.\n\n        Use -v/--verbose to show reporter descriptions.\n    ')

@show.bind_main_func
def _show(options, out, err):
    list_option_selected = any(getattr(options, attr) for attr in ('keywords', 'checks',
                                                                   'scopes', 'reporters'))
    if not list_option_selected:
        options.keywords = True
    if options.keywords:
        display_keywords(out, options)
    if options.checks:
        display_checks(out, options)
    if options.scopes:
        if options.verbosity < 1:
            out.write('\n'.join(base.scopes))
        else:
            for name, scope in base.scopes.items():
                out.write(f"{name} -- {scope.desc} scope")

    if options.reporters:
        display_reporters(out, options)
    return 0