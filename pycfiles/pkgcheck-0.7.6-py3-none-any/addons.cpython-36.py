# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/runner/work/pkgcheck/pkgcheck/build/lib/pkgcheck/addons.py
# Compiled at: 2020-02-09 15:46:32
# Size of source mod 2**32: 28843 bytes
"""Addon functionality shared by multiple checkers."""
import os, pickle, stat
from collections import UserDict, defaultdict
from functools import partial
from itertools import chain, filterfalse
from pkgcore.ebuild import domain, misc
from pkgcore.ebuild import profiles as profiles_mod
from pkgcore.restrictions import packages, values
from snakeoil.cli.arghparse import StoreBool
from snakeoil.cli.exceptions import UserException
from snakeoil.containers import ProtectedSet
from snakeoil.decorators import coroutine
from snakeoil.klass import jit_attr
from snakeoil.mappings import ImmutableDict
from snakeoil.osutils import abspath, pjoin
from snakeoil.sequences import iflatten_instance
from snakeoil.strings import pluralism
from . import base, caches, results
from .log import logger

class ArchesAddon(base.Addon):

    @classmethod
    def mangle_argparser(cls, parser):
        group = parser.add_argument_group('arches')
        group.add_argument('-a',
          '--arches', dest='selected_arches', metavar='ARCH', action='csv_negations',
          help='comma separated list of arches to enable/disable',
          docs="\n                Comma separated list of arches to enable and disable.\n\n                To specify disabled arches prefix them with '-'. Note that when\n                starting the argument list with a disabled arch an equals sign\n                must be used, e.g. -a=-arch, otherwise the disabled arch\n                argument is treated as an option.\n\n                By default all repo defined arches are used; however,\n                stable-related checks (e.g. UnstableOnly) default to the set of\n                arches having stable profiles in the target repo.\n            ")

    @staticmethod
    def check_args(parser, namespace):
        arches = namespace.selected_arches
        target_repo = getattr(namespace, 'target_repo', None)
        if target_repo is not None:
            all_arches = target_repo.known_arches
        else:
            all_arches = set()
        if arches is None:
            arches = (
             set(), all_arches)
        disabled, enabled = arches
        if not enabled:
            enabled = set(arch for arch in all_arches if '-' not in arch)
        arches = set(enabled).difference(set(disabled))
        if all_arches:
            unknown_arches = arches.difference(all_arches)
            if unknown_arches:
                es = pluralism(unknown_arches, plural='es')
                unknown = ', '.join(unknown_arches)
                valid = ', '.join(sorted(all_arches))
                parser.error(f"unknown arch{es}: {unknown} (valid arches: {valid})")
        namespace.arches = tuple(sorted(arches))


class ProfileData:

    def __init__(self, profile_name, key, provides, vfilter, iuse_effective, use, pkg_use, masked_use, forced_use, lookup_cache, insoluble, status, deprecated):
        self.key = key
        self.name = profile_name
        self.provides_repo = provides
        self.provides_has_match = getattr(provides, 'has_match', provides.match)
        self.iuse_effective = iuse_effective
        self.use = use
        self.pkg_use = pkg_use
        self.masked_use = masked_use
        self.forced_use = forced_use
        self.cache = lookup_cache
        self.insoluble = insoluble
        self.visible = vfilter.match
        self.status = status
        self.deprecated = deprecated

    def identify_use(self, pkg, known_flags):
        enabled = known_flags.intersection(self.forced_use.pull_data(pkg))
        immutable = enabled.union(filter(known_flags.__contains__, self.masked_use.pull_data(pkg)))
        force_disabled = self.masked_use.pull_data(pkg)
        if force_disabled:
            enabled = enabled.difference(force_disabled)
        return (
         immutable, enabled)


class _ProfilesCache(UserDict, caches.Cache):
    __doc__ = 'Class used to encapsulate cached profile data.'

    def __init__(self, data):
        super().__init__(data)
        self._cache = ProfileAddon.cache


class ProfileAddon(base.Addon, caches.CachedAddon):
    required_addons = (
     ArchesAddon,)
    non_profile_dirs = frozenset(['desc', 'updates'])
    cache = caches.CacheData(type='profiles', file='profiles.pickle', version=2)

    @staticmethod
    def mangle_argparser(parser):
        group = parser.add_argument_group('profiles')
        group.add_argument('-p',
          '--profiles', metavar='PROFILE', action='csv_negations', dest='selected_profiles',
          help='comma separated list of profiles to enable/disable',
          docs="\n                Comma separated list of profiles to enable and disable for\n                scanning. Any profiles specified in this fashion will be the\n                only profiles that get scanned, skipping any disabled profiles.\n                In addition, if no profiles are explicitly enabled, all\n                profiles defined in the target repo's profiles.desc file will be\n                scanned except those marked as experimental (exp).\n\n                To specify disabled profiles prefix them with ``-`` which\n                removes the from the list of profiles to be considered. Note\n                that when starting the argument list with a disabled profile an\n                equals sign must be used, e.g.  ``-p=-path/to/profile``,\n                otherwise the disabled profile argument is treated as an\n                option.\n\n                The special keywords of ``stable``, ``dev``, ``exp``, and\n                ``deprecated`` correspond to the lists of stable, development,\n                experimental, and deprecated profiles, respectively. Therefore,\n                to only scan all stable profiles pass the ``stable`` argument\n                to --profiles. Additionally the keyword ``all`` can be used to\n                scan all defined profiles in the target repo.\n            ")

    @staticmethod
    def check_args(parser, namespace):
        target_repo = namespace.target_repo
        selected_profiles = namespace.selected_profiles
        if selected_profiles is None:
            selected_profiles = (('exp', ), ())

        def norm_name(s):
            if s in ('dev', 'exp', 'stable', 'deprecated'):
                yield from target_repo.profiles.get_profiles(status=s)
            else:
                if s == 'all':
                    yield from target_repo.profiles
                else:
                    try:
                        yield target_repo.profiles[os.path.normpath(s)]
                    except KeyError:
                        parser.error(f"nonexistent profile: {s!r}")

        disabled, enabled = selected_profiles
        disabled = set(disabled)
        enabled = set(enabled)
        toggled = enabled.intersection(disabled)
        enabled = enabled.difference(toggled)
        disabled = disabled.difference(toggled)
        ignore_deprecated = 'deprecated' not in enabled
        disabled = set(chain.from_iterable(map(norm_name, disabled)))
        enabled = set(chain.from_iterable(map(norm_name, enabled)))
        if not enabled:
            enabled = set(target_repo.profiles)
        profiles = enabled.difference(disabled)
        namespace.arch_profiles = defaultdict(list)
        for p in sorted(profiles):
            if ignore_deprecated:
                if p.deprecated:
                    continue
            try:
                profile = target_repo.profiles.create_profile(p, load_profile_base=False)
            except profiles_mod.ProfileError as e:
                if namespace.selected_profiles is not None:
                    parser.error(f"invalid profile: {e.path!r}: {e.error}")
                continue

            if profile.arch is None:
                if namespace.selected_profiles is not None:
                    parser.error(f"profile make.defaults lacks ARCH setting: {p.path!r}")
                    continue
                    namespace.arch_profiles[profile.arch].append((profile, p))

    @coroutine
    def _profile_files(self):
        """Given a profile object, return its file set and most recent mtime."""
        cache = {}
        while True:
            profile = yield
            profile_mtime = 0
            profile_files = []
            for node in profile.stack:
                mtime, files = cache.get(node.path, (0, []))
                if not mtime:
                    for f in os.listdir(node.path):
                        p = pjoin(node.path, f)
                        st_obj = os.lstat(p)
                        if stat.S_ISREG(st_obj.st_mode):
                            files.append(p)
                            if st_obj.st_mtime > mtime:
                                mtime = st_obj.st_mtime

                    cache[node.path] = (
                     mtime, files)
                if mtime > profile_mtime:
                    profile_mtime = mtime
                profile_files.extend(files)

            yield (
             profile_mtime, frozenset(profile_files))

    @jit_attr
    def profile_data(self):
        """Mapping of profile age and file sets used to check cache viability."""
        data = {}
        if self.options.cache['profiles']:
            gen_profile_data = self._profile_files()
            for profile_obj, profile in chain.from_iterable(self.options.arch_profiles.values()):
                mtime, files = gen_profile_data.send(profile_obj)
                data[profile] = (mtime, files)
                next(gen_profile_data)

            del gen_profile_data
        return ImmutableDict(data)

    def __init__(self, *args, arches_addon=None):
        (super().__init__)(*args)
        target_repo = self.options.target_repo
        self.official_arches = target_repo.known_arches
        self.desired_arches = getattr(self.options, 'arches', None)
        if self.desired_arches is None or self.options.selected_arches is None:
            self.desired_arches = set(self.official_arches)
        self.global_insoluble = set()
        profile_filters = defaultdict(list)
        chunked_data_cache = {}
        cached_profiles = defaultdict(dict)
        if self.options.cache['profiles']:
            for repo in target_repo.trees:
                cache_file = self.cache_file(repo)
                cached_profiles[repo.config.profiles_base]['repo'] = repo
                try:
                    with open(cache_file, 'rb') as (f):
                        cache = pickle.load(f)
                    if cache.version == self.cache.version:
                        cached_profiles[repo.config.profiles_base].update(cache)
                    else:
                        logger.debug('forcing %s profile cache regen due to outdated version', repo.repo_id)
                        os.remove(cache_file)
                except FileNotFoundError as e:
                    pass
                except (AttributeError, EOFError, ImportError, IndexError) as e:
                    logger.debug('forcing %s profile cache regen: %s', repo.repo_id, e)
                    os.remove(cache_file)

        for k in sorted(self.desired_arches):
            if k.lstrip('~') not in self.desired_arches:
                continue
            stable_key = k.lstrip('~')
            unstable_key = '~' + stable_key
            stable_r = packages.PackageRestriction('keywords', values.ContainmentMatch2((stable_key,)))
            unstable_r = packages.PackageRestriction('keywords', values.ContainmentMatch2((stable_key, unstable_key)))
            default_masked_use = tuple(set(x for x in self.official_arches if x != stable_key))
            for profile_obj, profile in self.options.arch_profiles.get(k, []):
                files = self.profile_data.get(profile, None)
                try:
                    cached_profile = cached_profiles[profile.base][profile.path]
                    if files != cached_profile['files']:
                        raise KeyError
                    masks = cached_profile['masks']
                    unmasks = cached_profile['unmasks']
                    immutable_flags = cached_profile['immutable_flags']
                    stable_immutable_flags = cached_profile['stable_immutable_flags']
                    enabled_flags = cached_profile['enabled_flags']
                    stable_enabled_flags = cached_profile['stable_enabled_flags']
                    pkg_use = cached_profile['pkg_use']
                    iuse_effective = cached_profile['iuse_effective']
                    use = cached_profile['use']
                    provides_repo = cached_profile['provides_repo']
                except KeyError:
                    logger.debug('profile regen: %s', profile.path)
                    try:
                        masks = profile_obj.masks
                        unmasks = profile_obj.unmasks
                        immutable_flags = profile_obj.masked_use.clone(unfreeze=True)
                        immutable_flags.add_bare_global((), default_masked_use)
                        immutable_flags.optimize(cache=chunked_data_cache)
                        immutable_flags.freeze()
                        stable_immutable_flags = profile_obj.stable_masked_use.clone(unfreeze=True)
                        stable_immutable_flags.add_bare_global((), default_masked_use)
                        stable_immutable_flags.optimize(cache=chunked_data_cache)
                        stable_immutable_flags.freeze()
                        enabled_flags = profile_obj.forced_use.clone(unfreeze=True)
                        enabled_flags.add_bare_global((), (stable_key,))
                        enabled_flags.optimize(cache=chunked_data_cache)
                        enabled_flags.freeze()
                        stable_enabled_flags = profile_obj.stable_forced_use.clone(unfreeze=True)
                        stable_enabled_flags.add_bare_global((), (stable_key,))
                        stable_enabled_flags.optimize(cache=chunked_data_cache)
                        stable_enabled_flags.freeze()
                        pkg_use = profile_obj.pkg_use
                        iuse_effective = profile_obj.iuse_effective
                        provides_repo = profile_obj.provides_repo
                        use = set()
                        misc.incremental_expansion(use, profile_obj.use, 'while expanding USE')
                        use = frozenset(use)
                    except profiles_mod.ProfileError:
                        continue

                    if self.options.cache['profiles']:
                        cached_profiles[profile.base]['update'] = True
                        cached_profiles[profile.base][profile.path] = {'files':files, 
                         'masks':masks, 
                         'unmasks':unmasks, 
                         'immutable_flags':immutable_flags, 
                         'stable_immutable_flags':stable_immutable_flags, 
                         'enabled_flags':enabled_flags, 
                         'stable_enabled_flags':stable_enabled_flags, 
                         'pkg_use':pkg_use, 
                         'iuse_effective':iuse_effective, 
                         'use':use, 
                         'provides_repo':provides_repo}

                stable_cache = set()
                unstable_insoluble = ProtectedSet(self.global_insoluble)
                vfilter = domain.generate_filter(target_repo.pkg_masks | masks, unmasks)
                profile_filters[stable_key].append(ProfileData(profile.path, stable_key, provides_repo, packages.AndRestriction(vfilter, stable_r), iuse_effective, use, pkg_use, stable_immutable_flags, stable_enabled_flags, stable_cache, ProtectedSet(unstable_insoluble), profile.status, profile.deprecated))
                profile_filters[unstable_key].append(ProfileData(profile.path, unstable_key, provides_repo, packages.AndRestriction(vfilter, unstable_r), iuse_effective, use, pkg_use, immutable_flags, enabled_flags, ProtectedSet(stable_cache), unstable_insoluble, profile.status, profile.deprecated))

        for k, v in cached_profiles.items():
            if v.pop('update', False):
                repo = v.pop('repo')
                cache_file = self.cache_file(repo)
                try:
                    os.makedirs((os.path.dirname(cache_file)), exist_ok=True)
                    with open(cache_file, 'wb+') as (f):
                        pickle.dump(_ProfilesCache(cached_profiles[repo.config.profiles_base]), f)
                except IOError as e:
                    msg = f"failed dumping {repo.repo_id} profiles cache: {cache_file!r}: {e.strerror}"
                    raise UserException(msg)

        profile_evaluate_dict = {}
        for key, profile_list in profile_filters.items():
            similar = profile_evaluate_dict[key] = []
            for profile in profile_list:
                for existing in similar:
                    if existing[0].masked_use == profile.masked_use and existing[0].forced_use == profile.forced_use:
                        existing.append(profile)
                        break
                else:
                    similar.append([profile])

        self.profile_evaluate_dict = profile_evaluate_dict
        self.profile_filters = profile_filters

    def update_cache(self, output_lock, force=False):
        """Update related cache and push updates to disk."""
        pass

    def identify_profiles(self, pkg):
        l = []
        keywords = pkg.keywords
        unstable_keywords = tuple(f"~{x}" for x in keywords if x[0] != '~')
        for key in keywords + unstable_keywords:
            profile_grps = self.profile_evaluate_dict.get(key)
            if profile_grps is None:
                pass
            else:
                for profiles in profile_grps:
                    l2 = [x for x in profiles if x.visible(pkg)]
                    if not l2:
                        pass
                    else:
                        l.append(l2)

        return l

    def __getitem__(self, key):
        """Return profiles matching a given keyword."""
        return self.profile_filters[key]

    def get(self, key, default=None):
        """Return profiles matching a given keyword with a fallback if none exist."""
        try:
            return self.profile_filters[key]
        except KeyError:
            return default

    def __iter__(self):
        """Iterate over all profile data objects."""
        return chain.from_iterable(self.profile_filters.values())

    def __len__(self):
        return len([x for x in self])


class StableArchesAddon(base.Addon):
    __doc__ = 'Check relating to stable arches by default.'
    required_addons = (
     ArchesAddon,)

    def __init__(self, *args, arches_addon=None):
        (super().__init__)(*args)
        if self.options.selected_arches is None:
            stable_arches = (set().union)(*(repo.profiles.arches('stable') for repo in self.options.target_repo.trees))
        else:
            stable_arches = set(self.options.arches)
        self.options.stable_arches = stable_arches


class UnstatedIuse(results.VersionResult, results.Error):
    __doc__ = "Package is reliant on conditionals that aren't in IUSE."

    def __init__(self, attr, flags, profile=None, num_profiles=None, **kwargs):
        (super().__init__)(**kwargs)
        self.attr = attr
        self.flags = tuple(flags)
        self.profile = profile
        self.num_profiles = num_profiles

    @property
    def desc(self):
        msg = [f"attr({self.attr})"]
        if self.profile is not None:
            if self.num_profiles is not None:
                num_profiles = f" ({self.num_profiles} total)"
            else:
                num_profiles = ''
            msg.append(f"profile {self.profile!r}{num_profiles}")
        flags = ', '.join(self.flags)
        s = pluralism(self.flags)
        msg.extend([f"unstated flag{s}", f"[ {flags} ]"])
        return ': '.join(msg)


class UseAddon(base.Addon):
    required_addons = (
     ProfileAddon,)

    def __init__(self, *args, profile_addon):
        (super().__init__)(*args)
        c_implicit_iuse = set()
        if profile_addon:
            c_implicit_iuse = (set.intersection)(*(set(p.iuse_effective) for p in profile_addon))
        known_iuse = set()
        known_iuse_expand = set()
        for repo in self.options.target_repo.trees:
            known_iuse.update(flag for matcher, (flag, desc) in repo.config.use_desc)
            known_iuse_expand.update(flag for flags in repo.config.use_expand_desc.values() for flag, desc in flags)

        self.collapsed_iuse = misc.non_incremental_collapsed_restrict_to_data((
         (
          packages.AlwaysTrue, known_iuse),), (
         (
          packages.AlwaysTrue, known_iuse_expand),))
        self.profiles = profile_addon
        self.global_iuse = frozenset(known_iuse)
        self.global_iuse_expand = frozenset(known_iuse_expand)
        self.global_iuse_implicit = frozenset(c_implicit_iuse)
        self.ignore = not (c_implicit_iuse or known_iuse or known_iuse_expand)
        if self.ignore:
            logger.debug('disabling use/iuse validity checks since no usable use.desc and use.local.desc were found')

    def allowed_iuse(self, pkg):
        return self.collapsed_iuse.pull_data(pkg).union(pkg.local_use)

    def get_filter(self, attr=None):
        if self.ignore:
            return self.fake_use_validate
        else:
            if attr is not None:
                return partial((self.use_validate), attr=attr)
            return self.use_validate

    @staticmethod
    def fake_use_validate(klasses, pkg, seq, attr=None):
        return ({k:() for k in iflatten_instance(seq, klasses)}, ())

    def _flatten_restricts(self, nodes, skip_filter, stated, unstated, attr, restricts=None):
        for node in nodes:
            k = node
            v = restricts if restricts is not None else []
            if isinstance(node, packages.Conditional):
                unstated.update(filterfalse(stated.__contains__, node.restriction.vals))
                v.append(node.restriction)
                yield from self._flatten_restricts(iflatten_instance(node.payload, skip_filter), skip_filter, stated, unstated, attr, v)
                continue
            else:
                if attr == 'required_use':
                    unstated.update(filterfalse(stated.__contains__, node.vals))
            yield (
             k, tuple(v))

    def _unstated_iuse(self, pkg, attr, unstated_iuse):
        """Determine if packages use unstated IUSE for a given attribute."""
        if self.profiles:
            profiles_unstated = defaultdict(set)
            if attr is not None:
                for p in self.profiles:
                    profile_unstated = unstated_iuse - p.iuse_effective
                    if profile_unstated:
                        profiles_unstated[tuple(sorted(profile_unstated))].add(p.name)

            for unstated, profiles in profiles_unstated.items():
                profiles = sorted(profiles)
                if self.options.verbosity > 0:
                    for p in profiles:
                        yield UnstatedIuse(attr, unstated, p, pkg=pkg)

                else:
                    num_profiles = len(profiles)
                    yield UnstatedIuse(attr, unstated, (profiles[0]), num_profiles, pkg=pkg)

        elif unstated_iuse:
            unstated_iuse -= self.global_iuse_implicit
            if unstated_iuse:
                yield UnstatedIuse(attr, unstated_iuse, pkg=pkg)

    def use_validate(self, klasses, pkg, seq, attr=None):
        skip_filter = (
         packages.Conditional,) + klasses
        nodes = iflatten_instance(seq, skip_filter)
        unstated = set()
        vals = dict(self._flatten_restricts(nodes,
          skip_filter, stated=(pkg.iuse_stripped), unstated=unstated, attr=attr))
        return (vals, self._unstated_iuse(pkg, attr, unstated))


class NetAddon(base.Addon):
    __doc__ = 'Addon supporting network functionality.'

    @classmethod
    def mangle_argparser(cls, parser):
        group = parser.add_argument_group('network')
        group.add_argument('--timeout',
          type=float, default='5', help='timeout used for network checks')
        group.add_argument('--user-agent',
          default='Wget/1.20.3 (linux-gnu)', help='custom user agent spoofing')

    def __init__(self, *args):
        (super().__init__)(*args)
        try:
            from .net import Session
            self.session = Session(concurrent=(self.options.tasks),
              timeout=(self.options.timeout),
              user_agent=(self.options.user_agent))
        except ImportError as e:
            if e.name == 'requests':
                raise UserException('network checks require requests to be installed')
            raise


def init_addon(cls, options, addons_map=None):
    """Initialize a given addon."""
    if addons_map is None:
        addons_map = {}
    res = addons_map.get(cls)
    if res is not None:
        return res
    else:
        required_addons = chain.from_iterable(x.required_addons for x in cls.__mro__ if issubclass(x, base.Addon))
        kwargs = {base.param_name(addon):init_addon(addon, options, addons_map) for addon in required_addons}
        res = addons_map[cls] = cls(options, **kwargs)
        return res