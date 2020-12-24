# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/runner/work/pkgcheck/pkgcheck/build/lib/pkgcheck/sources.py
# Compiled at: 2020-02-09 15:46:32
# Size of source mod 2**32: 10317 bytes
"""Custom package sources used for feeding checks."""
import os
from collections import deque
from operator import attrgetter
from pkgcore.ebuild.repository import UnconfiguredTree
from pkgcore.restrictions import packages
from snakeoil.osutils import listdir_files, pjoin
from . import addons, base
from .packages import FilteredPkg, RawCPV, WrappedPkg

class Source:
    __doc__ = 'Base template for a source.'
    feed_type = base.repo_scope
    required_addons = ()

    def __init__(self, options, source):
        self._options = options
        self.source = source

    def __iter__(self):
        yield from self.source
        if False:
            yield None


class EmptySource(Source):
    __doc__ = 'Empty source meant for skipping item feed.'

    def __init__(self, options, scope=base.repo_scope):
        super().__init__(options, source=())
        self.feed_type = scope


class RepoSource(Source):
    __doc__ = 'Base template for a repository source.'
    feed_type = base.version_scope

    def __init__(self, options, source=None):
        self._options = options
        self._repo = options.target_repo
        self._source = source

    @property
    def source(self):
        """Source that packages are pulled from."""
        if self._source is not None:
            return self._source
        else:
            return self._repo

    def itermatch(self, restrict, **kwargs):
        """Yield packages matching the given restriction from the selected source."""
        kwargs.setdefault('sorter', sorted)
        unfiltered_iter = (self.source.itermatch)(restrict, **kwargs)
        if self._options.filter == 'latest':
            yield from LatestPkgsFilter(unfiltered_iter)
        else:
            yield from unfiltered_iter
        if False:
            yield None


class LatestPkgsFilter:
    __doc__ = 'Filter source packages, yielding those from the latest non-VCS and VCS slots.'

    def __init__(self, source_iter, partial_filtered=False):
        self._partial_filtered = partial_filtered
        self._source_iter = source_iter
        self._pkg_cache = deque()
        self._pkg_marker = None

    def __iter__(self):
        return self

    def __next__(self):
        if not self._pkg_cache:
            if self._pkg_marker is None:
                self._pkg_marker = next(self._source_iter)
            else:
                pkg = self._pkg_marker
                key = pkg.key
                selected_pkgs = {}
                if self._partial_filtered:
                    pkgs = []
                while key == pkg.key:
                    if pkg.live:
                        selected_pkgs[f"vcs-{pkg.slot}"] = pkg
                    else:
                        selected_pkgs[pkg.slot] = pkg
                    if self._partial_filtered:
                        pkgs.append(pkg)
                    try:
                        pkg = next(self._source_iter)
                    except StopIteration:
                        self._pkg_marker = None
                        break

                if self._pkg_marker is not None:
                    self._pkg_marker = pkg
                if self._partial_filtered:
                    selected_pkgs = set(selected_pkgs.values())
                    self._pkg_cache.extend((FilteredPkg(pkg=pkg) if pkg not in selected_pkgs else pkg) for pkg in pkgs)
                else:
                    self._pkg_cache.extend(selected_pkgs.values())
        return self._pkg_cache.popleft()


class Eclass:
    __doc__ = 'Generic eclass object.'

    def __init__(self, name, path):
        self.name = name
        self.path = path

    def __str__(self):
        return self.name

    @property
    def lines(self):
        with open(self.path) as (f):
            return tuple(f)

    def __lt__(self, other):
        if isinstance(other, Eclass):
            return self.name < other.name
        else:
            return self.name < other

    def __eq__(self, other):
        if isinstance(other, Eclass):
            return self.name == other.name
        else:
            return self.name == other


class EclassRepoSource(RepoSource):
    __doc__ = 'Repository eclass source.'
    feed_type = base.eclass_scope

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.eclasses = self._repo.eclass_cache.eclasses

    def itermatch(self, restrict, **kwargs):
        for name in sorted(self.eclasses):
            if restrict.match([name]):
                yield Eclass(name, self.eclasses[name].path)


class FilteredRepoSource(RepoSource):
    __doc__ = 'Ebuild repository source supporting custom package filtering.'

    def __init__(self, pkg_filter, partial_filtered, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self._pkg_filter = pkg_filter
        self._partial_filtered = partial_filtered

    def itermatch(self, restrict, **kwargs):
        yield from self._pkg_filter((super().itermatch)(restrict, **kwargs),
          partial_filtered=(self._partial_filtered))
        if False:
            yield None


class _RawRepo(UnconfiguredTree):
    __doc__ = 'Repository that allows matching against mismatched/invalid package names.'

    def __init__(self, repo):
        super().__init__(repo.location)

    def _get_versions(self, catpkg):
        """Pass through all packages that end with ".ebuild" extension.

        Deviates from parent in that no package name check is done.
        """
        cppath = pjoin(self.base, catpkg[0], catpkg[1])
        pkg = f"{catpkg[(-1)]}-"
        lp = len(pkg)
        extension = self.extension
        ext_len = -len(extension)
        try:
            return tuple(x[lp:ext_len] for x in listdir_files(cppath) if x[ext_len:] == extension)
        except EnvironmentError as e:
            path = pjoin(self.base, os.sep.join(catpkg))
            raise KeyError(f"failed fetching versions for package {path}: {e}") from e


class RawRepoSource(RepoSource):
    __doc__ = 'Ebuild repository source returning raw CPV objects.'

    def __init__(self, *args):
        (super().__init__)(*args)

    def itermatch(self, restrict, **kwargs):
        if self._options.filter == 'latest':
            yield from LatestPkgsFilter((super().itermatch)(restrict, **kwargs))
        else:
            self._repo = _RawRepo(self._repo)
            yield from (super().itermatch)(restrict, raw_pkg_cls=RawCPV, **kwargs)
        if False:
            yield None


class RestrictionRepoSource(RepoSource):
    __doc__ = 'Ebuild repository source supporting custom restrictions.'

    def __init__(self, restriction, *args):
        (super().__init__)(*args)
        self.restriction = restriction

    def itermatch(self, restrict, **kwargs):
        restrict = (packages.AndRestriction)(restrict, self.restriction*())
        yield from (super().itermatch)(restrict, **kwargs)
        if False:
            yield None


class UnmaskedRepoSource(RepoSource):
    __doc__ = 'Repository source that uses profiles/package.mask to filter packages.'

    def itermatch(self, restrict, **kwargs):
        filtered_repo = self._options.domain.filter_repo((self._repo),
          pkg_masks=(), pkg_unmasks=(), pkg_accept_keywords=(), pkg_keywords=(), profile=False)
        yield from (filtered_repo.itermatch)(restrict, **kwargs)
        if False:
            yield None


class _SourcePkg(WrappedPkg):
    __doc__ = 'Package object with file contents injected as an attribute.'
    __slots__ = ('lines', )

    def __init__(self, pkg):
        super().__init__(pkg)
        self.lines = tuple(pkg.ebuild.text_fileobj())


class EbuildFileRepoSource(RepoSource):
    __doc__ = 'Ebuild repository source yielding package objects and their file contents.'

    def itermatch(self, restrict, **kwargs):
        for pkg in (super().itermatch)(restrict, **kwargs):
            yield _SourcePkg(pkg)


class _CombinedSource(RepoSource):
    __doc__ = 'Generic source combining packages into similar chunks.'

    def keyfunc(self, pkg):
        """Function targeting attribute used to group packages."""
        raise NotImplementedError(self.keyfunc)

    def itermatch(self, restrict, **kwargs):
        key = None
        chunk = None
        for pkg in (super().itermatch)(restrict, **kwargs):
            new = self.keyfunc(pkg)
            if new == key:
                chunk.append(pkg)
            else:
                if chunk is not None:
                    yield chunk
                chunk = [
                 pkg]
                key = new

        if chunk is not None:
            yield chunk


class PackageRepoSource(_CombinedSource):
    __doc__ = 'Ebuild repository source yielding lists of versioned packages per package.'
    feed_type = base.package_scope
    keyfunc = attrgetter('key')


class CategoryRepoSource(_CombinedSource):
    __doc__ = 'Ebuild repository source yielding lists of versioned packages per category.'
    feed_type = base.category_scope
    keyfunc = attrgetter('category')


class RepositoryRepoSource(RepoSource):
    __doc__ = 'Ebuild repository source yielding lists of versioned packages per package.'
    feed_type = base.repo_scope


class _FilteredSource(RawRepoSource):
    __doc__ = 'Generic source yielding selected attribute from matching packages.'

    def keyfunc(self, pkg):
        raise NotImplementedError(self.keyfunc)

    def itermatch(self, restrict, **kwargs):
        key = None
        for pkg in (super().itermatch)(restrict, **kwargs):
            new = self.keyfunc(pkg)
            if new != key:
                if key is not None:
                    yield key
                key = new

        if key is not None:
            yield key


class UnversionedSource(_FilteredSource):
    __doc__ = 'Source yielding unversioned atoms from matching packages.'
    keyfunc = attrgetter('unversioned_atom')


class VersionedSource(_FilteredSource):
    __doc__ = 'Source yielding versioned atoms from matching packages.'
    keyfunc = attrgetter('versioned_atom')


def init_source--- This code section failed: ---

 L. 324         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'source'
                4  LOAD_GLOBAL              tuple
                6  CALL_FUNCTION_2       2  '2 positional arguments'
                8  POP_JUMP_IF_FALSE    84  'to 84'

 L. 325        10  LOAD_GLOBAL              len
               12  LOAD_FAST                'source'
               14  CALL_FUNCTION_1       1  '1 positional argument'
               16  LOAD_CONST               3
               18  COMPARE_OP               ==
               20  POP_JUMP_IF_FALSE    70  'to 70'

 L. 326        22  LOAD_FAST                'source'
               24  UNPACK_SEQUENCE_3     3 
               26  STORE_FAST               'source'
               28  STORE_FAST               'args'
               30  STORE_FAST               'kwargs'

 L. 327        32  LOAD_GLOBAL              dict
               34  LOAD_FAST                'kwargs'
               36  CALL_FUNCTION_1       1  '1 positional argument'
               38  STORE_FAST               'kwargs'

 L. 329        40  LOAD_STR                 'source'
               42  LOAD_FAST                'kwargs'
               44  COMPARE_OP               in
               46  POP_JUMP_IF_FALSE    82  'to 82'

 L. 330        48  LOAD_GLOBAL              init_source
               50  LOAD_FAST                'kwargs'
               52  LOAD_STR                 'source'
               54  BINARY_SUBSCR    
               56  LOAD_FAST                'options'
               58  LOAD_FAST                'addons_map'
               60  CALL_FUNCTION_3       3  '3 positional arguments'
               62  LOAD_FAST                'kwargs'
               64  LOAD_STR                 'source'
               66  STORE_SUBSCR     
               68  JUMP_ABSOLUTE        92  'to 92'
               70  ELSE                     '82'

 L. 332        70  LOAD_FAST                'source'
               72  UNPACK_SEQUENCE_2     2 
               74  STORE_FAST               'source'
               76  STORE_FAST               'args'

 L. 333        78  BUILD_MAP_0           0 
               80  STORE_FAST               'kwargs'
             82_0  COME_FROM            46  '46'
               82  JUMP_FORWARD         92  'to 92'
               84  ELSE                     '92'

 L. 335        84  BUILD_TUPLE_0         0 
               86  STORE_FAST               'args'

 L. 336        88  BUILD_MAP_0           0 
               90  STORE_FAST               'kwargs'
             92_0  COME_FROM            82  '82'

 L. 337        92  SETUP_LOOP          132  'to 132'
               94  LOAD_FAST                'source'
               96  LOAD_ATTR                required_addons
               98  GET_ITER         
              100  FOR_ITER            130  'to 130'
              102  STORE_FAST               'addon'

 L. 338       104  LOAD_GLOBAL              addons
              106  LOAD_ATTR                init_addon
              108  LOAD_FAST                'addon'
              110  LOAD_FAST                'options'
              112  LOAD_FAST                'addons_map'
              114  CALL_FUNCTION_3       3  '3 positional arguments'
              116  LOAD_FAST                'kwargs'
              118  LOAD_GLOBAL              base
              120  LOAD_ATTR                param_name
              122  LOAD_FAST                'addon'
              124  CALL_FUNCTION_1       1  '1 positional argument'
              126  STORE_SUBSCR     
              128  JUMP_BACK           100  'to 100'
              130  POP_BLOCK        
            132_0  COME_FROM_LOOP       92  '92'

 L. 339       132  LOAD_FAST                'source'
              134  LOAD_FAST                'args'
              136  LOAD_FAST                'options'
              138  BUILD_TUPLE_1         1 
              140  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
              142  LOAD_FAST                'kwargs'
              144  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              146  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 146