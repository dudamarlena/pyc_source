# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tracbzr/backend.py
# Compiled at: 2010-11-01 09:39:15
"""Bazaar backend for trac's versioncontrol."""
import datetime, StringIO
from itertools import izip
import time, urllib, re, fnmatch, trac
from trac import versioncontrol, core, config, mimeview, util, wiki
from trac.web.chrome import Chrome
from trac.util.html import html, Markup
trac_version = (
 int(trac.__version__[0]), int(trac.__version__[2:4]))
if trac_version >= (0, 12):

    def _trac_construct(init):

        def wrapped_init(self, bzr_repo, *args, **kwargs):
            init(self, bzr_repo, *args, **kwargs)

        return wrapped_init


else:

    def _trac_construct(init):

        def wrapped_init(self, bzr_repo, *args, **kwargs):
            init(self, *args, **kwargs)

        return wrapped_init


if trac_version >= (0, 11):
    from trac.util.datefmt import utc

    def trac_timestamp(timestamp):
        return datetime.datetime.fromtimestamp(timestamp, utc)


    from trac.versioncontrol.web_ui.browser import IPropertyRenderer
else:

    def trac_timestamp(timestamp):
        return timestamp


    class IPropertyRenderer(core.Interface):
        __module__ = __name__


from bzrlib import branch as bzrlib_branch, bzrdir, errors, inventory, osutils, revision, transport
import bzrlib.api
from bzrlib.revision import CURRENT_REVISION, NULL_REVISION
config_section = 'tracbzr'

class BzrConnector(core.Component):
    """The necessary glue between our set of bzr branches and trac."""
    __module__ = __name__
    core.implements(versioncontrol.IRepositoryConnector)

    def __init__(self):
        if hasattr(self.env, 'systeminfo'):
            bzr_version = '%i.%i.%i' % bzrlib.api.get_current_api_version(None)
            self.env.systeminfo.append(('Bazaar', bzr_version))
            try:
                import tracbzr as tracbzr_mod
                tracbzr_version = util.get_pkginfo(tracbzr_mod).get('version')
            except Exception, e:
                self.log.warn(e)
                tracbzr_version = 'unknown'
            else:
                self.env.systeminfo.append(('TracBzr', tracbzr_version))
        return

    def get_supported_types(self):
        """Support for `repository_type = bzr`"""
        yield ('bzr', 8)

    def get_repository(self, repos_type, repos_dir, authname_or_params):
        """Return a `BzrRepository`"""
        assert repos_type == 'bzr'
        if trac_version < (0, 12):
            authname_or_params = None
        return BzrRepository(repos_dir, authname_or_params, self)


class BzrWikiMacros(core.Component):
    """Component for macros related to bzr."""
    __module__ = __name__
    core.implements(wiki.IWikiMacroProvider)

    def get_macros(self):
        yield 'Branches'

    def get_macro_description(self, name):
        assert name == 'Branches'
        return 'Render a list of available branches.'

    def render_macro(self, req, name, content):
        assert name == 'Branches'
        if trac_version >= (0, 11):
            chrome = Chrome(self.env)
            dateinfo = chrome.populate_data(req, {})['dateinfo']
        else:

            def dateinfo(timestamp):
                from trac.util.datefmt import format_datetime, pretty_timedelta
                date = format_datetime(timestamp)
                age = pretty_timedelta(timestamp)
                return html.SPAN(age, title=date)

        if trac_version >= (0, 12):
            from trac.wiki.api import parse_args
            from trac.versioncontrol.api import RepositoryManager
            (args, kwargs) = parse_args(content)
            reponame = kwargs.get('repo', '')
            rm = RepositoryManager(self.env)
            repo = rm.get_repository(reponame)
            if repo is None:
                raise core.TracError('No repository named %r' % (reponame,))
        else:
            repo = self.env.get_repository(req.authname)
        if not isinstance(repo, BzrRepository):
            raise core.TracError('Configured repository is not a bzr repository but a %s instead' % (repo.__class__.__name__,))
        try:
            branches = repo.get_branches()
            rows = []
            for (loc, target) in branches:
                try:
                    revid = target.last_revision()
                    revno = target.revision_id_to_revno(revid)
                    rev = repo.string_rev(target, revid)
                    if revid == NULL_REVISION:
                        timestamp = '—'
                        message = 'This branch is empty'
                    else:
                        revision = target.repository.get_revision(revid)
                        timestamp = revision.timestamp
                        timestamp = dateinfo(timestamp)
                        message = revision.message
                    rows.append(html.TR([ html.TD(x, class_=c) for (c, x) in [('name', html.A(loc, class_='dir', href=req.href.browser(loc))), ('nick', target.nick), ('rev', html.A('[%d]' % revno, href=req.href.changeset(rev))), ('age', timestamp), ('change', message)] ]))
                except errors.BzrError, e:
                    rows.append(html.TR(html.TD(html.A(loc, class_='dir', href=req.href.browser(loc)), class_='name'), html.TD(html.DIV(html.STRONG('Error getting branch details'), html.PRE(str(e)), class_='system-message'), colspan='4')))

            return html.TABLE(class_='listing')(html.THEAD(html.TR([ html.TH(x) for x in ['Path', 'Nick', 'Revision', 'Age', 'Last Change'] ])), html.TBODY(rows))
        finally:
            repo.close()
        return


class BzrPropertyRenderer(core.Component):
    """Renderer for bzr-specific properties."""
    __module__ = __name__
    core.implements(IPropertyRenderer)

    def match_property(self, name, mode):
        if name == 'parents' and mode == 'revprop':
            return 4
        return 0

    def render_property(self, name, mode, context, props):
        if name == 'parents' and mode == 'revprop':
            path = None
            if context.resource.realm == 'changeset':
                try:
                    path = context.req.args.get('new_path')
                except KeyError:
                    pass
                else:
                    if path is not None:
                        path = path.strip('/')
                    if path == '':
                        path = None
            content = html.TABLE(class_='wiki parents')(html.THEAD(html.TR([ html.TH(h) for h in ['Rev', 'Tree', 'Chgset'] ])), html.TBODY([ html.TR(html.TD(p.split(',')[(-1)]), html.TD(html.A('@%s' % p, href=context.href.browser(path, rev=p))), html.TD(html.A('[%s]' % p, href=context.href.changeset(p, path))))
             for p in props[name].split('\n') ]))
            return content
        return


class LockedBranches(object):
    """Keep track of locks and ensure they get unlocked one day.
    This deals with the fact that Trac doesn't always call the repository
    close method, and that a __del__ method in the repository itself causes
    trouble as described in https://bugs.launchpad.net/trac-bzr/+bug/484324"""
    __module__ = __name__

    def __init__(self):
        self._locked_branches = []

    def __del__(self):
        self.unlock()

    def append(self, branch):
        branch.lock_read()
        self._locked_branches.append(branch)

    def unlock(self):
        for branch in self._locked_branches:
            branch.unlock()

        self._locked_branches = []


class BzrRepository(versioncontrol.Repository):
    """Present a bzr branch as a trac repository."""
    __module__ = __name__
    primary_branches = config.ListOption(config_section, 'primary_branches', 'trunk', keep_empty=True, doc="Ordered list of primary branches.\n\n        These will be listed first in the Branches macro. When viewing\n        the timeline, each changeset will be associated with the first\n        primary branch that contains it. The value is a comma\n        separated list of globs, as used by the fnmatch module. An\n        empty list element can be used to denote the branch at the\n        root of the repository.\n\n        Defaults to 'trunk'.")
    include_sideline_changes = config.BoolOption(config_section, 'include_sideline_changes', True, doc='Include sideline changes in the list of changes.\n\n        This option controls whether sideline changes (i.e. changes\n        with dotted revision numbers only) are included in the list of\n        changes as reported by the timeline view. Note that there\n        might be other plugins using that information as well, so\n        there might be other components beside the timeline view that\n        get affected by this setting.\n\n        Defaults to True.')

    def __init__(self, location, auth_or_params, component):
        versioncontrol.Repository.__init__(self, location, auth_or_params, component.log)
        self.component = component
        self.config = component.config
        self.root_transport = transport.get_transport(location)
        self._tree_cache = {}
        self._locked_branches = LockedBranches()
        self._branch_cache = {}
        self._history = None
        self._previous = None
        self._revision_cache = {}
        return

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.root_transport.base)

    def branch_path(self, branch):
        """Determine the relative path to a branch from the root"""
        repo_path = self.root_transport.base
        branch_path = branch.bzrdir.root_transport.base
        if branch_path.startswith(repo_path):
            return branch_path[len(repo_path):].rstrip('/')
        else:
            repo_path = osutils.normalizepath(repo_path)
            branch_path = osutils.normalizepath(branch_path)
            return osutils.relpath(repo_path, branch_path)

    def string_rev(self, branch, revid):
        """Create a trac rev string.

        branch is None or a bzr branch.
        """
        if branch is None:
            return self._escape_revid(revid)
        relpath = self.branch_path(branch)
        try:
            return self._string_rev_revno(relpath, branch.revision_id_to_revno(revid))
        except errors.NoSuchRevision:
            dotted = self.dotted_revno(branch, revid)
            if dotted is not None:
                return self._string_rev_revno(relpath, dotted)
            else:
                return self._string_rev_revid(relpath, revid)

        return

    @staticmethod
    def _escape_revid(revid):
        return urllib.quote(revid, ':')

    @staticmethod
    def _unescape_revid(revid):
        return urllib.unquote(revid)

    @staticmethod
    def _escape_branch(relpath):
        if '%' in relpath or ',' in relpath:
            relpath = urllib.quote(relpath, '')
        else:
            relpath = relpath.replace('/', ',')
        return relpath

    @staticmethod
    def _unescape_branch(relpath):
        if '%' in relpath:
            relpath = urllib.unquote(relpath)
        else:
            relpath = relpath.replace(',', '/')
        return relpath

    @classmethod
    def _string_rev_revid(cls, relpath, revid):
        branch_name = cls._escape_branch(relpath)
        revid = cls._escape_revid(revid)
        if branch_name:
            return '%s,%s' % (branch_name, revid)
        else:
            return '%s' % revid

    @classmethod
    def _string_rev_revno(cls, relpath, revno):
        branch_name = cls._escape_branch(relpath)
        if branch_name:
            return '%s,%s' % (branch_name, revno)
        else:
            return str(revno)

    def _parse_rev(self, rev):
        """Translate a trac rev string into a (branch, revid) tuple.

        branch is None or a bzr branch object.

        Supported syntax:
         - "123" is revno 123 in the default branch.
         - "revid" is a revid in the default branch.
         - "spork,123" is revno 123 in the spork branch.
         - "spork,revid" is a revid in the spork branch.
           (currently revid is assumed to be in the branch ancestry!)
         - "spork," is latest revision in the spork branch.
         - "spork,1.2.3" is either revno or revid 1.2.3 in the spork branch.
         - "foo,bar,123" is revno 123 in the foo/bar branch.

        Branch paths have / replaced by , and existing , escaped by doubling.
        Revids are urlencoded.
        """
        rev = str(rev)
        split = rev.split(',')
        if len(split) == 1:
            rev_branch = ''
            rev_rev = rev
        elif len(split) >= 2:
            rev_branch = self._unescape_branch((',').join(split[:-1]))
            rev_rev = split[(-1)]
        else:
            raise versioncontrol.NoSuchChangeset(rev)
        rev_rev = self._unescape_revid(rev_rev)
        if len(split) == 1 and rev_rev in (CURRENT_REVISION, NULL_REVISION):
            return (
             None, rev_rev)
        try:
            branch = self.get_branch(rev_branch)
        except errors.NotBranchError:
            raise versioncontrol.NoSuchChangeset(rev)

        if rev_rev == '' or rev_rev == CURRENT_REVISION:
            revid = branch.last_revision()
        if rev_rev.isdigit():
            try:
                revid = branch.get_rev_id(int(rev_rev))
            except errors.NoSuchRevision:
                raise versioncontrol.NoSuchChangeset(rev)

        dotted = rev_rev.split('.')
        for segment in dotted:
            if not segment.isdigit():
                revid = rev_rev
                break
        else:
            cache = self.get_branch_cache(branch)
            revid = cache.revid_from_dotted(rev_rev)
            if revid is None:
                self.log.warn('%r is no dotted revno, will interpret as revid.', rev_rev)
                revid = rev_rev

        return (
         branch, revid)

    def close(self):
        """Release our branches. Trac does not *have* to call this!"""
        self._locked_branches.unlock()

    def get_branch(self, location):
        if location in self._branch_cache:
            return self._branch_cache[location].branch
        trans = self.root_transport
        for piece in location.split('/'):
            if piece:
                trans = trans.clone(piece)

        target_bzrdir = bzrdir.BzrDir.open_from_transport(trans)
        branch = target_bzrdir.open_branch()
        self._locked_branches.append(branch)
        self._branch_cache[location] = BranchCache(self, branch)
        return branch

    def get_containing_branch(self, location):
        (branch, relpath) = containing_branch(self.root_transport, location)
        real_location = location[:-len(relpath)].rstrip('/')
        if real_location not in self._branch_cache:
            self._branch_cache[real_location] = BranchCache(self, branch)
            self._locked_branches.append(branch)
        return (
         self._branch_cache[real_location].branch, relpath)

    def get_branches(self):
        """Get an ordered list of all branches in the repository.

        Returns a list of (relpath, branch) pairs. Branches will be
        locked for reading. Branches inside other branches will not be
        listed."""
        primary = self.primary_branches + ['*']
        branches = []
        for (loc, branch) in self._get_branches():
            for (index, pattern) in enumerate(primary):
                if fnmatch.fnmatch(loc, pattern):
                    branches.append((index, loc, branch))
                    break

        branches.sort()
        for (index, loc, branch) in branches:
            self._locked_branches.append(branch)

        return [ (loc, branch) for (index, loc, branch) in branches ]

    def _get_branches(self, trans=None, loc=()):
        """Find branches under a listable transport.

        Does not descend into control directories or branch directories.
        (branches inside other branches will not be listed)
        """
        if trans is None:
            trans = self.root_transport
        try:
            children = trans.list_dir('.')
            if '.bzr' in children:
                children.remove('.bzr')
                try:
                    target_bzrdir = bzrdir.BzrDir.open_from_transport(trans)
                    yield (('/').join(loc), target_bzrdir.open_branch())
                except errors.NotBranchError:
                    pass
                else:
                    return
            for child in children:
                for (child_loc, child_branch) in self._get_branches(trans.clone(child), loc + (child,)):
                    yield (
                     child_loc, child_branch)

        except errors.NoSuchFile, e:
            return

        return

    def get_changeset(self, rev):
        """Retrieve a Changeset."""
        (branch, revid) = self._parse_rev(rev)
        try:
            return BzrChangeset(self, branch, revid, self.log)
        except errors.NoSuchRevision, e:
            raise versioncontrol.NoSuchChangeset(rev)

    def get_changesets(self, start, stop):
        """Retrieve all changesets in a cetain time span."""
        seen = set()
        rhss = []
        inrange = []
        branches = self.get_branches()

        def walk(cache, revid):
            rhs = []
            while revid not in seen:
                seen.add(revid)
                revision = cache.get_revision(revid)
                time = trac_timestamp(revision.timestamp)
                if time < start:
                    break
                if time < stop:
                    chgset = BzrChangeset(self, branch, revid, self.log)
                    inrange.append((time, revid, chgset))
                parents = revision.parent_ids
                if not parents:
                    break
                if len(parents) > 1:
                    rhs.extend(parents[1:])
                revid = parents[0]

            return rhs

        for (relpath, branch) in branches:
            cache = self.get_branch_cache(branch)
            revid = branch.last_revision()
            if revid != NULL_REVISION:
                rhs = walk(cache, revid)
            else:
                rhs = []
            rhss.append(rhs)

        if self.include_sideline_changes:
            for ((relpath, branch), rhs) in zip(branches, rhss):
                cache = self.get_branch_cache(branch)
                while rhs:
                    revid = rhs.pop()
                    new_rhs = walk(cache, revid)
                    if new_rhs:
                        rhs.extend(new_rhs)

        inrange.sort()
        return [ chgset for (time, revid, chgset) in inrange ]

    def has_node(self, path, rev=None):
        """Return a boolean indicating if the node is present in a rev."""
        try:
            self.get_node(path, rev)
        except versioncontrol.NoSuchNode:
            return False
        else:
            return True

    def get_node(self, path, rev=None):
        """Return a Node object or raise NoSuchNode or NoSuchChangeset."""
        path = self.normalize_path(path)
        if rev is None:
            rev = self._escape_revid(CURRENT_REVISION)
        (revbranch, revid) = self._parse_rev(rev)
        try:
            (branch, relpath) = self.get_containing_branch(path)
        except errors.NotBranchError:
            if not self.root_transport.has(path):
                raise versioncontrol.NoSuchNode(path, rev)
            return UnversionedDirNode(self, revbranch, revid, path)

        if revbranch is None:
            revbranch = branch
        try:
            if revid == CURRENT_REVISION:
                tree = revbranch.basis_tree()
            else:
                tree = revbranch.repository.revision_tree(revid)
        except (errors.NoSuchRevision, errors.RevisionNotPresent):
            raise versioncontrol.NoSuchChangeset(rev)

        if not tree.inventory.root:
            return EmptyBranchNode(self, branch, path)
        file_id = tree.inventory.path2id(relpath)
        if file_id is None:
            raise versioncontrol.NoSuchNode(path, rev)
        entry = tree.inventory[file_id]
        klass = NODE_MAP[entry.kind]
        return klass(self, branch, tree, entry, path)

    def get_oldest_rev(self):
        return self.string_rev(None, NULL_REVISION)

    def get_youngest_rev(self):
        return self.string_rev(None, CURRENT_REVISION)

    def previous_rev(self, rev, path=''):
        if path:
            prev = self.get_node(path, rev).get_previous()
            if prev is None:
                return
            return prev[1]
        (branch, revid) = self._parse_rev(rev)
        if revid in (NULL_REVISION, CURRENT_REVISION) or branch is None:
            return
        ancestry = iter(branch.repository.iter_reverse_revision_history(revid))
        ancestry.next()
        try:
            return self.string_rev(branch, ancestry.next())
        except StopIteration:
            return self.string_rev(branch, NULL_REVISION)

        return

    def next_rev(self, rev, path=''):
        (branch, revid) = self._parse_rev(rev)
        if revid == CURRENT_REVISION:
            return
        if revid == NULL_REVISION:
            if branch is None:
                return CURRENT_REVISION
            revno = 0
        if branch is None:
            return
        try:
            revno = branch.revision_id_to_revno(revid)
        except errors.NoSuchRevision:
            return

        try:
            next_revid = branch.get_rev_id(revno + 1)
        except errors.NoSuchRevision:
            return

        return self.string_rev(branch, next_revid)

    def rev_older_than(self, rev1, rev2):
        if rev1 == rev2:
            return False
        (branch1, rrev1) = self._parse_rev(rev1)
        (branch2, rrev2) = self._parse_rev(rev2)
        if rrev1 == rrev2:
            return False
        both = frozenset([rrev1, rrev2])
        if NULL_REVISION in both:
            return NULL_REVISION == rrev1
        if CURRENT_REVISION in both:
            return CURRENT_REVISION == rrev2
        if branch1.repository.has_revisions(both) == both:
            heads = branch1.repository.get_graph().heads(both)
        elif branch2.repository.has_revisions(both) == both:
            heads = branch2.repository.get_graph().heads(both)
        else:
            heads = both
        if len(s) == 1:
            return rrev2 in heads
        return branch1.repository.get_revision(rrev1).timestamp < branch2.repository.get_revision(rrev2).timestamp

    def get_path_history(self, path, rev=None, limit=None):
        """Shortcut for Node's get_history."""
        return self.get_node(path, rev).get_history(limit)

    def normalize_path(self, path):
        """Remove leading and trailing '/'"""
        return path and path.strip('/') or ''

    def normalize_rev(self, rev):
        """Turn a user-specified rev into a "normalized" rev.

        This turns None into a rev, and may convert a revid-based rev into
        a revno-based one.
        """
        if rev is None or rev == '':
            branch = None
            revid = CURRENT_REVISION
        else:
            (branch, revid) = self._parse_rev(rev)
        if branch is not None:
            repository = branch.repository
        else:
            repository = None
        return self.string_rev(branch, revid)

    def short_rev(self, rev):
        """Attempt to shorten a rev.

        This returns the last 6 characters of the dotted revno.

        The result of this method is used above the line number
        columns in the diff/changeset viewer. There is *very* little
        room there. Tricks like using the branch nick simply do not fit.
        
        Those 6 chars seem to fit, at least if two of them are dots,
        and should be enough to clearly identify almost any two
        revisions named in a changeset.
        """
        (branch, revid) = self._parse_rev(rev)
        if branch is None:
            return revid
        dotted = self.dotted_revno(branch, revid)
        if dotted is None:
            return '????'
        return dotted[-6:]

    def get_changes(self, old_path, old_rev, new_path, new_rev, ignore_ancestry=1):
        """yields (old_node, new_node, kind, change) tuples."""
        if old_path != new_path:
            raise core.TracError('Currently the bzr plugin does not support this between different directories. Sorry.')
        (old_branch, old_revid) = self._parse_rev(old_rev)
        (new_branch, new_revid) = self._parse_rev(new_rev)
        old_tree = old_branch.repository.revision_tree(old_revid)
        new_tree = new_branch.repository.revision_tree(new_revid)
        prefix = self.branch_path(new_branch)
        subdir = new_path[len(prefix) + 1:]
        delta = new_tree.changes_from(old_tree, specific_files=[subdir])
        for (path, file_id, kind) in delta.added:
            path = osutils.pathjoin(prefix, path)
            entry = new_tree.inventory[file_id]
            node = NODE_MAP[kind](self, new_branch, new_tree, entry, path)
            yield (None, node, node.kind, versioncontrol.Changeset.ADD)

        for (path, file_id, kind) in delta.removed:
            path = osutils.pathjoin(prefix, path)
            entry = old_tree.inventory[file_id]
            node = NODE_MAP[kind](self, old_branch, old_tree, entry, path)
            yield (node, None, node.kind, versioncontrol.Changeset.DELETE)

        for (oldpath, newpath, file_id, kind, textmod, metamod) in delta.renamed:
            oldpath = osutils.pathjoin(prefix, oldpath)
            newpath = osutils.pathjoin(prefix, newpath)
            oldnode = NODE_MAP[kind](self, old_branch, old_tree, old_tree.inventory[file_id], oldpath)
            newnode = NODE_MAP[kind](self, new_branch, new_tree, new_tree.inventory[file_id], newpath)
            if oldnode.kind != newnode.kind:
                raise core.TracError('%s changed kinds, I do not know how to handle that' % (newpath,))
            yield (
             oldnode, newnode, oldnode.kind, versioncontrol.Changeset.MOVE)

        for (path, file_id, kind, textmod, metamod) in delta.modified:
            path = osutils.pathjoin(prefix, path)
            oldpath = osutils.pathjoin(prefix, old_tree.id2path(file_id))
            oldnode = NODE_MAP[kind](self, old_branch, old_tree, old_tree.inventory[file_id], oldpath)
            newnode = NODE_MAP[kind](self, new_branch, new_tree, new_tree.inventory[file_id], path)
            if oldnode.kind != newnode.kind:
                raise core.TracError('%s changed kinds, I do not know how to handle that' % (newpath,))
            if oldpath != path:
                action = versioncontrol.Changeset.MOVE
            else:
                action = versioncontrol.Changeset.EDIT
            yield (
             oldnode, newnode, oldnode.kind, action)

        return

    def dotted_revno(self, branch, revid):
        return self.get_branch_cache(branch).dotted_revno(revid)

    def get_branch_cache(self, branch):
        branch_key = branch.bzrdir.root_transport.base
        if branch_key not in self._branch_cache:
            self._branch_cache[branch_key] = BranchCache(self, branch)
        return self._branch_cache[branch_key]


class BzrNode(versioncontrol.Node):
    __module__ = __name__
    _super_init = _trac_construct(versioncontrol.Node.__init__)

    def __init__(self, bzr_repo, path, rev, kind):
        self.bzr_repo = bzr_repo
        self._super_init(bzr_repo, path, rev, kind)


class UnversionedDirNode(BzrNode):
    __module__ = __name__

    def __init__(self, bzr_repo, branch, revid, path):
        rev_string = BzrRepository._escape_revid(CURRENT_REVISION)
        BzrNode.__init__(self, bzr_repo, path, rev_string, versioncontrol.Node.DIRECTORY)
        self.transport = bzr_repo.root_transport.clone(path)
        self.branch = branch
        self.revid = revid
        self.path = path

    def __repr__(self):
        return 'UnversionedDirNode(path=%r)' % self.path

    def get_properties(self):
        return {}

    def get_entries(self):
        result = []
        for name in self.transport.list_dir(''):
            if name == '.bzr':
                continue
            stat_mode = self.transport.stat(name).st_mode
            kind = osutils.file_kind_from_stat_mode(stat_mode)
            if not kind == 'directory':
                continue
            child_path = osutils.pathjoin(self.path, name)
            try:
                branch = self.bzr_repo.get_branch(child_path)
            except errors.NotBranchError:
                result.append(UnversionedDirNode(self.bzr_repo, self.branch, self.revid, child_path))
            else:
                tree = branch.basis_tree()
                if tree.inventory.root:
                    node = BzrDirNode(self.bzr_repo, branch, tree, tree.inventory.root, child_path)
                else:
                    node = EmptyBranchNode(self.bzr_repo, branch, child_path)
                result.append(node)

        return result

    def get_content_length(self):
        return 0

    def get_content(self):
        return StringIO.StringIO('')

    def get_content_length(self):
        return

    def get_content_type(self):
        return

    def get_history(self, limit=None):
        if self.branch is not None:
            bpath = self.bzr_repo.branch_path(self.branch)
            if self.path == '' or bpath.startswith(self.path + '/'):
                repo = self.branch.repository
                ancestry = repo.iter_reverse_revision_history(self.revid)
                ancestry = iter(ancestry)
                for rev_id in ancestry:
                    yield (
                     self.path, self.bzr_repo.string_rev(self.branch, rev_id), versioncontrol.Changeset.EDIT)

                yield (
                 self.path, self.bzr_repo.string_rev(self.branch, NULL_REVISION), versioncontrol.Changeset.ADD)
                return
        yield (self.path, BzrRepository._escape_revid(CURRENT_REVISION), versioncontrol.Changeset.ADD)
        return


class EmptyBranchNode(BzrNode):
    __module__ = __name__

    def __init__(self, bzr_repo, branch, path):
        rev_string = bzr_repo.string_rev(branch, NULL_REVISION)
        BzrNode.__init__(self, bzr_repo, path, rev_string, versioncontrol.Node.DIRECTORY)
        self.branch = branch
        self.path = path

    def __repr__(self):
        return 'EmptyBranchNode(path=%r)' % self.path

    def get_properties(self):
        return {}

    def get_entries(self):
        return []

    def get_content_length(self):
        return

    def get_content(self):
        return StringIO.StringIO('')

    def get_content_type(self):
        return

    def get_history(self, limit=None):
        yield (self.path, self.bzr_repo.string_rev(self.branch, NULL_REVISION), versioncontrol.Changeset.ADD)


class BzrVersionedNode(BzrNode):
    __module__ = __name__
    _diff_map = {'modified': versioncontrol.Changeset.EDIT, 'unchanged': versioncontrol.Changeset.EDIT, 'added': versioncontrol.Changeset.ADD, inventory.InventoryEntry.RENAMED: versioncontrol.Changeset.MOVE, inventory.InventoryEntry.MODIFIED_AND_RENAMED: versioncontrol.Changeset.MOVE}

    def __init__(self, bzr_repo, branch, revisiontree, entry, path):
        """Initialize. path has to be a normalized path."""
        self.bzr_repo = bzr_repo
        self.log = bzr_repo.log
        self.repo = branch.repository
        self.branch = branch
        self.tree = revisiontree
        self.entry = entry
        rev_string = bzr_repo.string_rev(branch, self.get_content_revision())
        BzrNode.__init__(self, bzr_repo, path, rev_string, self.kind)
        self.created_rev = self.rev
        self.created_path = self.path
        self.root_path = path[:-len(self.tree.id2path(self.entry.file_id))]

    def get_properties(self):
        result = {}
        if self.entry.executable:
            result['executable'] = 'True'
        return result

    def get_history(self, limit=None):
        """Backward history.

        yields (path, rev, chg) tuples.

        path is the path to this entry, rev is the revid string.
        chg is a Changeset.ACTION thing.

        First thing should be for the current revision.

        This is special because it checks for changes recursively,
        not just to this directory. bzr only treats the dir as changed
        if it is renamed, not if its contents changed. Trac needs
        this recursive behaviour.

        limit is an int cap on how many entries to return.
        """
        current_entry = self.entry
        file_id = current_entry.file_id
        count = 0
        current_revid = self.get_content_revision()
        if current_revid == CURRENT_REVISION:
            current_revid = self.branch.last_revision()
        repo = self.branch.repository
        ancestry = repo.iter_reverse_revision_history(current_revid)
        ancestry = iter(ancestry)
        if self.entry.parent_id is None:
            for rev_id in ancestry:
                yield (
                 self.path, self.bzr_repo.string_rev(self.branch, rev_id), versioncontrol.Changeset.EDIT)

            yield (
             self.path, self.bzr_repo.string_rev(self.branch, NULL_REVISION), versioncontrol.Changeset.ADD)
            return
        chunksize = limit or 100
        chunk = []
        ancestry.next()
        current_tree = self.tree
        current_path = current_tree.id2path(file_id)
        path_prefix = self.path[:-len(current_path)]
        while True:
            chunk[:] = []
            try:
                for i in range(chunksize):
                    chunk.append(ancestry.next())

            except StopIteration:
                if not chunk:
                    yield (
                     path_prefix + current_path,
                     self.bzr_repo.string_rev(self.branch, current_revid), versioncontrol.Changeset.ADD)
                    return

            cache = self.bzr_repo.get_branch_cache(self.branch)
            for (previous_revid, previous_tree) in izip(chunk, cache.revision_trees(chunk)):
                if file_id in previous_tree.inventory:
                    previous_entry = previous_tree.inventory[file_id]
                else:
                    previous_entry = None
                delta = current_tree.changes_from(previous_tree, specific_files=[current_path])
                if not delta.has_changed():
                    current_entry = previous_entry
                    current_path = previous_tree.inventory.id2path(file_id)
                    current_revid = previous_revid
                    current_tree = previous_tree
                    continue
                diff = current_entry.describe_change(previous_entry, current_entry)
                if diff == 'added':
                    yield (
                     path_prefix + current_path,
                     self.bzr_repo.string_rev(self.branch, current_revid), versioncontrol.Changeset.ADD)
                    return
                elif diff == 'modified' or diff == 'unchanged':
                    yield (path_prefix + current_path,
                     self.bzr_repo.string_rev(self.branch, current_revid), versioncontrol.Changeset.EDIT)
                elif diff in (current_entry.RENAMED, current_entry.MODIFIED_AND_RENAMED):
                    yield (path_prefix + current_path,
                     self.bzr_repo.string_rev(self.branch, current_revid), versioncontrol.Changeset.MOVE)
                else:
                    raise Exception('unknown describe_change %r' % (diff,))
                count += 1
                if limit is not None and count >= limit:
                    return
                current_entry = previous_entry
                current_path = previous_tree.inventory.id2path(file_id)
                current_revid = previous_revid
                current_tree = previous_tree

        return

    def get_content_revision(self):
        """Obtain the revision at which this node was last changed.
        This should include changes to any children.
        This will be called by BzrVersionedNode's constructor, so overriding
        subclasses should ensure that this method can be called safely before
        calling BzrVersionedNode.__init__().
        """
        return self.entry.revision

    def get_last_modified(self):
        return self.tree.get_file_mtime(self.entry.file_id)


class BzrDirNode(BzrVersionedNode):
    __module__ = __name__
    isdir = True
    isfile = False
    kind = versioncontrol.Node.DIRECTORY

    def __init__(self, bzr_repo, branch, revisiontree, entry, path, revcache=None):
        if revcache is None:
            revcache = _FileToRevisionCache(bzr_repo, branch, revisiontree, entry)
        self.revcache = revcache
        BzrVersionedNode.__init__(self, bzr_repo, branch, revisiontree, entry, path)
        return

    def get_content_revision(self):
        """Determine the most recent change to the directory or its children."""
        if self.entry.parent_id is None:
            return self.tree.get_revision_id()
        return self.revcache[self.entry]

    def __repr__(self):
        return 'BzrDirNode(path=%r, relpath=%r)' % (self.path, self.entry.name)

    @classmethod
    def _get_cache(cls, cache, ancestry, entry, ancestry_idx=None):
        """Populate a file_id <-> revision_id mapping.
        
        This mapping is different from InventoryEntry.revision, but only for
        directories.  In this scheme, directories are considered modified
        if their contents are modified.

        The revision ids are not guaranteed to be in the mainline revision
        history.

        cache: The cache to populate
        ancestry: A topologically-sorted list of revisions, with more recent
            revisions having lower indexes.
        entry: The InventoryEntry to start at
        ancestry_idx: A mapping of revision_id <-> ancestry index.
        """
        if ancestry_idx is None:
            ancestry_idx = dict(((r, n) for (n, r) in enumerate(ancestry)))
        best = ancestry_idx[entry.revision]
        for child in entry.children.itervalues():
            if child.kind == 'directory':
                index = cls._get_cache(cache, ancestry, child, ancestry_idx)
                cache[child.file_id] = ancestry[index]
            else:
                index = ancestry_idx[child.revision]
            best = min(best, index)

        return best

    def get_content(self):
        """Return a file-like (read(length)) for a file, None for a dir."""
        return

    def get_entries(self):
        """Yield child Nodes if a dir, return None if a file."""
        for (name, entry) in self.entry.children.iteritems():
            childpath = ('/').join((self.path, name))
            klass = NODE_MAP[entry.kind]
            if klass is BzrDirNode:
                yield klass(self.bzr_repo, self.branch, self.tree, entry, childpath, self.revcache)
            else:
                yield klass(self.bzr_repo, self.branch, self.tree, entry, childpath)

    def get_content_length(self):
        return

    def get_content_type(self):
        return


class BzrFileNode(BzrVersionedNode):
    __module__ = __name__
    isfile = True
    isdir = False
    kind = versioncontrol.Node.FILE

    def __repr__(self):
        return 'BzrFileNode(path=%r)' % self.path

    def get_content(self):
        """Return a file-like (read(length)) for a file, None for a dir."""
        return self.tree.get_file(self.entry.file_id)

    def get_entries(self):
        return

    def get_content_length(self):
        return self.entry.text_size

    def get_content_type(self):
        return mimeview.get_mimetype(self.name)

    def get_annotations(self):
        annotation = self.tree.annotate_iter(self.entry.file_id)
        return [ self.bzr_repo.string_rev(self.branch, revid) for (revid, line) in annotation ]


class BzrSymlinkNode(BzrVersionedNode):
    """Kinda like a file only not really. Empty, properties only."""
    __module__ = __name__
    isfile = True
    isdir = False
    kind = versioncontrol.Node.FILE

    def __repr__(self):
        return 'BzrSymlinkNode(path=%r)' % self.path

    def get_content(self):
        return StringIO.StringIO('')

    def get_entries(self):
        return

    def get_content_length(self):
        return 0

    def get_content_type(self):
        return 'text/plain'

    def get_properties(self):
        return {'destination': self.entry.symlink_target}


NODE_MAP = {'directory': BzrDirNode, 'file': BzrFileNode, 'symlink': BzrSymlinkNode}

class BzrChangeset(versioncontrol.Changeset):
    __module__ = __name__
    _super_init = _trac_construct(versioncontrol.Changeset.__init__)

    def __init__(self, bzr_repo, branch, revid, log):
        """Initialize from a bzr repo, an unquoted revid and a logger."""
        assert isinstance(revid, str), 'revid is %r' % type(revid)
        self.log = log
        self.bzr_repo = bzr_repo
        self.branch = branch
        if revid == CURRENT_REVISION and branch is not None:
            revid = branch.revision_history()
        if revid in (CURRENT_REVISION, NULL_REVISION):
            self.revision = revision.Revision(revid, committer='', message='', timezone='')
            revidstr = bzr_repo.string_rev(branch, revid)
            self._super_init(bzr_repo, revidstr, '', '', trac_timestamp(time.time()))
            return
        if branch is None:
            assert isinstance(revid, str)
            raise errors.NoSuchRevision(None, revid)
        self.revision = bzr_repo.get_branch_cache(branch).get_revision(revid)
        authors = (';').join(self.revision.get_apparent_authors())
        self._super_init(bzr_repo, bzr_repo.string_rev(branch, revid), self.revision.message, authors, trac_timestamp(self.revision.timestamp))
        return

    def __repr__(self):
        return 'BzrChangeset(%r)' % self.revision.revision_id

    def get_properties(self):
        """Return an iterator of (name, value, is wikitext, html class)."""
        if trac_version >= (0, 11):
            result = {}

            def add_text(name, value):
                result[name] = value

            def add_parents(parents):
                result['parents'] = ('\n').join(parents)

        else:
            result = []

            def add_text(name, value):
                result.append((name, value, False, ''))

            def add_parents(parents):
                for (name, link) in [('parent trees', ' * source:@%s'), ('changesets', ' * [changeset:%s]')]:
                    wikitext = ('\n').join((link % parent for parent in parents))
                    result.append((name, wikitext, True, ''))

        add_text('revision id', self.revision.revision_id)
        for (name, value) in self.revision.properties.iteritems():
            add_text(name, value)

        if len(self.revision.parent_ids) > 1:
            add_parents([ self.bzr_repo.string_rev(self.branch, parent) for parent in self.revision.parent_ids ])
        return result

    def get_changes(self):
        """Yield changes.

        Return tuples are (path, kind, change, base_path, base_rev).
        change is self.ADD/COPY/DELETE/EDIT/MOVE.
        kind is Node.FILE or Node.DIRECTORY.
        base_path and base_rev are the location and revision of the file
        before "ours".
        """
        if self.revision.revision_id in (CURRENT_REVISION, NULL_REVISION):
            return
        branchpath = osutils.relpath(osutils.normalizepath(self.bzr_repo.root_transport.base), osutils.normalizepath(self.branch.bzrdir.root_transport.base))
        for (path, kind, change, base_path, base_rev) in self._get_changes():
            if path is not None:
                path = osutils.pathjoin(branchpath, path)
            if base_path is not None:
                base_path = osutils.pathjoin(branchpath, base_path)
            yield (
             path, kind, change, base_path, base_rev)

        return

    def _get_changes(self):
        if self.revision.revision_id in (CURRENT_REVISION, NULL_REVISION):
            return
        this = self.branch.repository.revision_tree(self.revision.revision_id)
        parents = self.revision.parent_ids
        if parents:
            parent_revid = parents[0]
        else:
            parent_revid = None
        other = self.branch.repository.revision_tree(parent_revid)
        delta = this.changes_from(other)
        kindmap = {'directory': versioncontrol.Node.DIRECTORY, 'file': versioncontrol.Node.FILE, 'symlink': versioncontrol.Node.FILE}
        for (path, file_id, kind) in delta.added:
            yield (
             path, kindmap[kind], self.ADD, None, None)

        for (path, file_id, kind) in delta.removed:
            yield (
             path, kindmap[kind], self.DELETE, path, self.bzr_repo.string_rev(self.branch, parent_revid))

        for (oldpath, newpath, file_id, kind, textmod, metamod) in delta.renamed:
            yield (
             newpath, kindmap[kind], self.MOVE, other.id2path(file_id), self.bzr_repo.string_rev(self.branch, parent_revid))

        for (path, file_id, kind, textmod, metamod) in delta.modified:
            yield (
             path, kindmap[kind], self.EDIT, other.id2path(file_id), self.bzr_repo.string_rev(self.branch, parent_revid))

        return


def containing_branch(transport, path):
    child_transport = transport.clone(path)
    (my_bzrdir, relpath) = bzrdir.BzrDir.open_containing_from_transport(child_transport)
    return (
     my_bzrdir.open_branch(), relpath)


class BranchCache(object):
    __module__ = __name__

    def __init__(self, bzr_repo, branch):
        self.bzr_repo = bzr_repo
        self.branch = branch
        self._revno_revid = None
        return

    def dotted_revno(self, revid):
        try:
            revno = self.branch.revision_id_to_dotted_revno(revid)
            dotted = ('.').join([ str(s) for s in revno ])
            return dotted
        except errors.NoSuchRevision:
            return

        return

    def revid_from_dotted(self, dotted_revno):
        try:
            revno = tuple([ int(s) for s in dotted_revno.split('.') ])
            revid = self.branch.dotted_revno_to_revision_id(revno)
            return revid
        except errors.NoSuchRevision:
            return

        return

    def revision_tree(self, revision_id):
        if revision_id not in self.bzr_repo._tree_cache:
            self.bzr_repo._tree_cache[revision_id] = self.branch.repository.revision_tree(revision_id)
            if revision_id == NULL_REVISION:
                self.bzr_repo._tree_cache[None] = self.bzr_repo._tree_cache[NULL_REVISION]
        return self.bzr_repo._tree_cache[revision_id]

    def revision_trees(self, revision_ids):
        if None in revision_ids or NULL_REVISION in revision_ids:
            self.revision_tree(NULL_REVISION)
        missing = [ r for r in revision_ids if r not in self.bzr_repo._tree_cache ]
        if len(missing) > 0:
            trees = self.branch.repository.revision_trees(missing)
            for tree in trees:
                self.bzr_repo._tree_cache[tree.get_revision_id()] = tree

        return [ self.bzr_repo._tree_cache[r] for r in revision_ids ]

    def cache_revisions(self, revision_ids):
        if self.bzr_repo.log:
            self.bzr_repo.log.debug('caching %d revisions' % len(revision_ids))
        missing = [ r for r in revision_ids if r not in self.bzr_repo._revision_cache ]
        revisions = self.branch.repository.get_revisions(missing)
        self.bzr_repo._revision_cache.update(dict(((r.revision_id, r) for r in revisions)))
        if self.bzr_repo.log:
            self.bzr_repo.log.debug('done caching %d revisions' % len(revision_ids))

    def get_revision(self, revision_id):
        try:
            return self.bzr_repo._revision_cache[revision_id]
        except KeyError:
            self.cache_revisions([revision_id])

        return self.bzr_repo._revision_cache[revision_id]


class _FileToRevisionCache(object):
    """Map from file_id to revision_id.

    This is used to determine the last modification to a directory.
    """
    __module__ = __name__

    def __init__(self, bzr_repo, branch, revisiontree, root):
        self.bzr_repo = bzr_repo
        self.branch = branch
        self.revisiontree = revisiontree
        self.root = root
        self.revcache = None
        return

    def __getitem__(self, entry):
        """Lazily fill cache only when needed."""
        if self.revcache is None:
            revid = self.revisiontree.get_revision_id()
            ancestry = self.branch.repository.get_ancestry(revid)
            ancestry.reverse()
            ancestry_idx = dict(((r, n) for (n, r) in enumerate(ancestry)))
            self.revcache = {}
            best = self._fill_cache(ancestry, ancestry_idx, self.root)
        return self.revcache[entry.file_id]

    def _fill_cache(self, ancestry, ancestry_idx, entry):
        """Populate a file_id <-> revision_id mapping.
        
        This mapping is different from InventoryEntry.revision, but only for
        directories.  In this scheme, directories are considered modified
        if their contents are modified.

        The revision ids are not guaranteed to be in the mainline revision
        history.

        ancestry: A topologically-sorted list of revisions, with more recent
            revisions having lower indexes.
        ancestry_idx: A mapping of revision_id <-> ancestry index.
        entry: The InventoryEntry to start at
        """
        best = ancestry_idx[entry.revision]
        for child in entry.children.itervalues():
            if child.kind == 'directory':
                index = self._fill_cache(ancestry, ancestry_idx, child)
            else:
                index = ancestry_idx[child.revision]
            best = min(best, index)

        self.revcache[entry.file_id] = ancestry[best]
        return best