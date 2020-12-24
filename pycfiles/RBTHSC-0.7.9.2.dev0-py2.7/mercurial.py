# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\rbtools\clients\mercurial.py
# Compiled at: 2017-04-19 05:14:02
from __future__ import unicode_literals
import logging, os, re, uuid
from six.moves.urllib.parse import urlsplit, urlunparse
from rbtools.clients import PatchResult, SCMClient, RepositoryInfo
from rbtools.clients.errors import InvalidRevisionSpecError, TooManyRevisionsError
from rbtools.clients.svn import SVNClient
from rbtools.utils.checks import check_install
from rbtools.utils.filesystem import make_empty_files
from rbtools.utils.console import edit_text
from rbtools.utils.process import die, execute

class MercurialClient(SCMClient):
    """
    A wrapper around the hg Mercurial tool that fetches repository
    information and generates compatible diffs.
    """
    name = b'Mercurial'
    PRE_CREATION = b'/dev/null'
    PRE_CREATION_DATE = b'Thu Jan 01 00:00:00 1970 +0000'
    supports_diff_exclude_patterns = True

    def __init__(self, **kwargs):
        super(MercurialClient, self).__init__(**kwargs)
        self.hgrc = {}
        self._type = b'hg'
        self._remote_path = ()
        self._initted = False
        self._hg_env = {b'HGPLAIN': b'1'}
        self._hgext_path = os.path.normpath(os.path.join(os.path.dirname(__file__), b'..', b'helpers', b'hgext.py'))
        self._remote_path_candidates = [
         b'reviewboard', b'origin', b'parent',
         b'default']

    @property
    def hidden_changesets_supported(self):
        """Return whether the repository supports hidden changesets.

        Mercurial 1.9 and above support hidden changesets. These are changesets
        that have been hidden from regular repository view. They still exist
        and are accessible, but only if the --hidden command argument is
        specified.

        Since we may encounter hidden changesets (e.g. the user specifies
        hidden changesets as part of the revision spec), we need to be aware
        of hidden changesets.
        """
        if not hasattr(self, b'_hidden_changesets_supported'):
            result = execute([b'hg', b'parents', b'--hidden', b'-r', b'0'], ignore_errors=True, with_errors=False, none_on_ignored_error=True)
            self._hidden_changesets_supported = result is not None
        return self._hidden_changesets_supported

    @property
    def hg_root(self):
        """Return the root of the working directory.

        This will return the root directory of the current repository. If the
        current working directory is not inside a mercurial repository, this
        returns None.
        """
        if not hasattr(self, b'_hg_root'):
            root = execute([b'hg', b'root'], env=self._hg_env, ignore_errors=True)
            if not root.startswith(b'abort:'):
                self._hg_root = root.strip()
            else:
                self._hg_root = None
        return self._hg_root

    def _init(self):
        """Initialize the client."""
        if self._initted or not self.hg_root:
            return
        self._load_hgrc()
        svn_info = execute([b'hg', b'svn', b'info'], ignore_errors=True)
        if not svn_info.startswith(b'abort:') and not svn_info.startswith(b'hg: unknown command') and not svn_info.lower().startswith(b'not a child of'):
            self._type = b'svn'
            self._svn_info = svn_info
        else:
            self._type = b'hg'
            for candidate in self._remote_path_candidates:
                rc_key = b'paths.%s' % candidate
                if rc_key in self.hgrc:
                    self._remote_path = (
                     candidate, self.hgrc[rc_key])
                    logging.debug(b'Using candidate path %r: %r' % self._remote_path)
                    break

        self._initted = True

    def get_repository_info(self):
        """Return the repository info object."""
        if not check_install([b'hg', b'--help']):
            logging.debug(b'Unable to execute "hg --help": skipping Mercurial')
            return
        else:
            self._init()
            if not self.hg_root:
                return
            if self._type == b'svn':
                return self._calculate_hgsubversion_repository_info(self._svn_info)
            path = self.hg_root
            base_path = b'/'
            if self._remote_path:
                path = self._remote_path[1]
                base_path = b''
            return RepositoryInfo(path=path, base_path=base_path, supports_parent_diffs=True)
            return

    def parse_revision_spec(self, revisions=[]):
        """Parse the given revision spec.

        The 'revisions' argument is a list of revisions as specified by the
        user. Items in the list do not necessarily represent a single revision,
        since the user can use SCM-native syntaxes such as "r1..r2" or "r1:r2".
        SCMTool-specific overrides of this method are expected to deal with
        such syntaxes.

        This will return a dictionary with the following keys:
            'base':        A revision to use as the base of the resulting diff.
            'tip':         A revision to use as the tip of the resulting diff.
            'parent_base': (optional) The revision to use as the base of a
                           parent diff.
            'commit_id':   (optional) The ID of the single commit being posted,
                           if not using a range.

        These will be used to generate the diffs to upload to Review Board (or
        print). The diff for review will include the changes in (base, tip],
        and the parent diff (if necessary) will include (parent, base].

        If zero revisions are passed in, this will return the outgoing changes
        from the parent of the working directory.

        If a single revision is passed in, this will return the parent of that
        revision for 'base' and the passed-in revision for 'tip'. This will
        result in generating a diff for the changeset specified.

        If two revisions are passed in, they will be used for the 'base'
        and 'tip' revisions, respectively.

        In all cases, a parent base will be calculated automatically from
        changesets not present on the remote.
        """
        self._init()
        n_revisions = len(revisions)
        if n_revisions == 1:
            revisions = re.split(b'\\.\\.|::', revisions[0])
            n_revisions = len(revisions)
        result = {}
        if n_revisions == 0:
            if self._type == b'svn':
                result[b'base'] = self._get_parent_for_hgsubversion()
                result[b'tip'] = b'.'
            else:
                outgoing = self._get_bottom_and_top_outgoing_revs_for_remote(rev=b'.')
                if outgoing[0] is None or outgoing[1] is None:
                    raise InvalidRevisionSpecError(b'There are no outgoing changes')
                result[b'base'] = self._identify_revision(outgoing[0])
                result[b'tip'] = self._identify_revision(outgoing[1])
                result[b'commit_id'] = result[b'tip']
                if self.has_pending_changes():
                    logging.warning(b'Your working directory is not clean. Any changes which have not been committed to a branch will not be included in your review request.')
            if self.options.parent_branch:
                result[b'parent_base'] = result[b'base']
                result[b'base'] = self._identify_revision(self.options.parent_branch)
        elif n_revisions == 1:
            result[b'tip'] = self._identify_revision(revisions[0])
            result[b'commit_id'] = result[b'tip']
            result[b'base'] = self._execute([
             b'hg', b'parents', b'--hidden', b'-r', result[b'tip'],
             b'--template', b'{node|short}']).split()[0]
            if len(result[b'base']) != 12:
                raise InvalidRevisionSpecError(b"Can't determine parent revision")
        elif n_revisions == 2:
            result[b'base'] = self._identify_revision(revisions[0])
            result[b'tip'] = self._identify_revision(revisions[1])
        else:
            raise TooManyRevisionsError
        if b'base' not in result or b'tip' not in result:
            raise InvalidRevisionSpecError(b'"%s" does not appear to be a valid revision spec' % revisions)
        if self._type == b'hg' and b'parent_base' not in result:
            outgoing = self._get_outgoing_changesets(self._get_remote_branch(), rev=result[b'base'])
            logging.debug(b'%d outgoing changesets between remote and base.', len(outgoing))
            if not outgoing:
                return result
            parent_base = self._execute([
             b'hg', b'parents', b'--hidden', b'-r', outgoing[0][1],
             b'--template', b'{node|short}']).split()
            if len(parent_base) == 0:
                raise Exception(b'Could not find parent base revision. Ensure upstream repository is not empty.')
            result[b'parent_base'] = parent_base[0]
            logging.debug(b'Identified %s as parent base', result[b'parent_base'])
        return result

    def _identify_revision(self, revision):
        identify = self._execute([
         b'hg', b'identify', b'-i', b'--hidden', b'-r', str(revision)], ignore_errors=True, none_on_ignored_error=True)
        if identify is None:
            raise InvalidRevisionSpecError(b'"%s" does not appear to be a valid revision' % revision)
        else:
            return identify.split()[0]
        return

    def _calculate_hgsubversion_repository_info(self, svn_info):

        def _info(r):
            m = re.search(r, svn_info, re.M)
            if m:
                return urlsplit(m.group(1))
            else:
                return
                return

        self._type = b'svn'
        root = _info(b'^Repository Root: (.+)$')
        url = _info(b'^URL: (.+)$')
        if not (root and url):
            return None
        else:
            scheme, netloc, path, _, _ = root
            root = urlunparse([scheme, root.netloc.split(b'@')[(-1)], path,
             b'', b'', b''])
            base_path = url.path[len(path):]
            return RepositoryInfo(path=root, base_path=base_path, supports_parent_diffs=True)

    def _load_hgrc(self):
        for line in execute([b'hg', b'showconfig'], split_lines=True):
            line = line.split(b'=', 1)
            if len(line) == 2:
                key, value = line
            else:
                key = line[0]
                value = b''
            self.hgrc[key] = value.strip()

    def get_raw_commit_message(self, revisions):
        """Return the raw commit message.

        This extracts all descriptions in the given revision range and
        concatenates them, most recent ones going first.
        """
        rev1 = revisions[b'base']
        rev2 = revisions[b'tip']
        delim = str(uuid.uuid1())
        descs = self._execute([
         b'hg', b'log', b'--hidden', b'-r', b'%s::%s' % (rev1, rev2),
         b'--template', b'{desc}%s' % delim], env=self._hg_env, results_unicode=False)
        descs = descs.split(delim)[1:-1]
        return (b'\n\n').join([ desc.strip() for desc in descs ])

    def diff(self, revisions, include_files=[], exclude_patterns=[], extra_args=[]):
        """Return a diff across all modified files in the given revisions."""
        self._init()
        diff_cmd = [
         b'hg', b'diff', b'--hidden']
        if self._type == b'svn':
            diff_cmd.append(b'--svn')
        diff_cmd += include_files
        for pattern in exclude_patterns:
            diff_cmd.append(b'-X')
            diff_cmd.append(pattern)

        diff = self._execute(diff_cmd + [b'-r', revisions[b'base'], b'-r', revisions[b'tip']], env=self._hg_env, log_output_on_error=False, results_unicode=False)
        supports_empty_files = self.supports_empty_files()
        if supports_empty_files:
            diff = self._handle_empty_files(diff, revisions[b'base'], revisions[b'tip'], exclude_files=exclude_patterns)
        if b'parent_base' in revisions:
            base_commit_id = revisions[b'parent_base']
            parent_diff = self._execute(diff_cmd + [b'-r', base_commit_id, b'-r', revisions[b'base']], env=self._hg_env, results_unicode=False)
            if supports_empty_files:
                parent_diff = self._handle_empty_files(parent_diff, base_commit_id, revisions[b'base'], exclude_files=exclude_patterns)
        else:
            base_commit_id = revisions[b'base']
            parent_diff = None
        base_commit_id = self._execute([
         b'hg', b'log', b'-r', base_commit_id, b'--template', b'{node}'], env=self._hg_env, results_unicode=False)
        return {b'diff': diff, 
           b'parent_diff': parent_diff, 
           b'commit_id': revisions.get(b'commit_id'), 
           b'base_commit_id': base_commit_id}

    def _handle_empty_files(self, diff, base, tip, exclude_files=[]):
        """Add added and deleted 0-length files to the diff output.

        Since the diff output from hg diff does not give any information on
        0-length files, we manually add this extra information to the patch.
        """
        base_files = self._get_files_in_changeset(base)
        tip_files = self._get_files_in_changeset(tip)
        if base_files == tip_files:
            return diff
        tip_empty_files = self._get_files_in_changeset(tip, get_empty=True)
        added_empty_files = tip_empty_files - base_files
        base_empty_files = self._get_files_in_changeset(base, get_empty=True)
        deleted_empty_files = base_empty_files - tip_files
        if not (added_empty_files or deleted_empty_files):
            return diff
        dates = execute([b'hg', b'log', b'-r', base, b'-r', tip,
         b'--template', b'{date|date}\\t'], env=self._hg_env)
        base_date, tip_date = dates.strip().split(b'\t')
        for filename in added_empty_files:
            if filename not in exclude_files:
                diff += (b'diff -r %s -r %s %s\n--- %s\t%s\n+++ b/%s\t%s\n' % (
                 base, tip, filename,
                 self.PRE_CREATION, self.PRE_CREATION_DATE,
                 filename, tip_date)).encode(b'utf-8')

        for filename in deleted_empty_files:
            if filename not in exclude_files:
                diff += (b'diff -r %s -r %s %s\n--- a/%s\t%s\n+++ %s\t%s\n' % (
                 base, tip, filename,
                 filename, base_date,
                 self.PRE_CREATION,
                 self.PRE_CREATION_DATE)).encode(b'utf-8')

        return diff

    def _get_files_in_changeset(self, rev, get_empty=False):
        """Return a set of all files in the specified changeset.

        If get_empty is True, we return only 0-length files in the changeset.
        """
        cmd = [
         b'hg', b'locate', b'-r', rev]
        if get_empty:
            cmd.append(b'set:size(0)')
        files = execute(cmd, env=self._hg_env, ignore_errors=True, none_on_ignored_error=True)
        if files:
            files = files.replace(b'\\', b'/')
            return set(files.splitlines())
        return set()

    def _get_parent_for_hgsubversion(self):
        """Return the parent Subversion branch.

        Returns the parent branch defined in the command options if it exists,
        otherwise returns the parent Subversion branch of the current
        repository.
        """
        return getattr(self.options, b'tracking', None) or execute([b'hg', b'parent', b'--svn', b'--template',
         b'{node}\n']).strip()

    def _get_remote_branch(self):
        """Return the remote branch assoicated with this repository.

        If the remote branch is not defined, the parent branch of the
        repository is returned.
        """
        remote = getattr(self.options, b'tracking', None)
        if not remote:
            try:
                remote = self._remote_path[0]
            except IndexError:
                remote = None

        if not remote:
            die(b'Could not determine remote branch to use for diff creation. Specify --tracking-branch to continue.')
        return remote

    def create_commit(self, message, author, run_editor, files=[], all_files=False):
        """Commit the given modified files.

        This is expected to be called after applying a patch. This commits the
        patch using information from the review request, opening the commit
        message in $EDITOR to allow the user to update it.
        """
        if run_editor:
            modified_message = edit_text(message)
        else:
            modified_message = message
        hg_command = [b'hg', b'commit', b'-m', modified_message,
         b'-u %s <%s>' % (author.fullname, author.email)]
        execute(hg_command + files)

    def _get_current_branch(self):
        """Return the current branch of this repository."""
        return execute([b'hg', b'branch'], env=self._hg_env).strip()

    def _get_bottom_and_top_outgoing_revs_for_remote(self, rev=None):
        """Return the bottom and top outgoing revisions.

        Returns the bottom and top outgoing revisions for the changesets
        between the current branch and the remote branch.
        """
        remote = self._get_remote_branch()
        current_branch = self._get_current_branch()
        outgoing = [ o for o in self._get_outgoing_changesets(remote, rev=rev) if current_branch == o[2]
                   ]
        if outgoing:
            top_rev, bottom_rev = self._get_top_and_bottom_outgoing_revs(outgoing)
        else:
            top_rev = None
            bottom_rev = None
        return (bottom_rev, top_rev)

    def _get_outgoing_changesets(self, remote, rev=None):
        """Return the outgoing changesets between us and a remote.

        This will return a list of tuples of (rev, node, branch) for
        each outgoing changeset. The list will be sorted in revision order.

        If rev is specified, we will limit the changesets to ancestors of
        the specified revision. Otherwise, all changesets not in the remote
        will be returned.
        """
        outgoing_changesets = []
        args = [
         b'hg', b'-q', b'outgoing', b'--template',
         b'{rev}\\t{node|short}\\t{branch}\\n',
         remote]
        if rev:
            args.extend([b'-r', rev])
        raw_outgoing = execute(args, env=self._hg_env, extra_ignore_errors=(1, ))
        for line in raw_outgoing.splitlines():
            if not line:
                continue
            if line.startswith(b'warning: '):
                continue
            rev, node, branch = [ f.strip() for f in line.split(b'\t') ]
            branch = branch or b'default'
            if not rev.isdigit():
                raise Exception(b'Unexpected output from hg: %s' % line)
            logging.debug(b'Found outgoing changeset %s:%s' % (rev, node))
            outgoing_changesets.append((int(rev), node, branch))

        return outgoing_changesets

    def _get_top_and_bottom_outgoing_revs(self, outgoing_changesets):
        revs = set(t[0] for t in outgoing_changesets)
        top_rev = max(revs)
        bottom_rev = min(revs)
        for rev, node, branch in reversed(outgoing_changesets):
            parents = execute([
             b'hg', b'log', b'-r', str(rev), b'--template', b'{parents}'], env=self._hg_env)
            parents = re.split(b':[^\\s]+\\s*', parents)
            parents = [ int(p) for p in parents if p != b'' ]
            parents = [ p for p in parents if p not in outgoing_changesets ]
            if len(parents) > 0:
                bottom_rev = parents[0]
                break
            else:
                bottom_rev = rev - 1

        bottom_rev = max(0, bottom_rev)
        return (
         top_rev, bottom_rev)

    def scan_for_server(self, repository_info):
        server_url = super(MercurialClient, self).scan_for_server(repository_info)
        if not server_url and self.hgrc.get(b'reviewboard.url'):
            server_url = self.hgrc.get(b'reviewboard.url').strip()
        if not server_url and self._type == b'svn':
            prop = SVNClient().scan_for_server_property(repository_info)
            if prop:
                return prop
        return server_url

    def _execute(self, cmd, *args, **kwargs):
        if not self.hidden_changesets_supported and b'--hidden' in cmd:
            cmd = [ p for p in cmd if p != b'--hidden' ]
        cmd.extend([
         b'--config',
         b'extensions.rbtoolsnormalize=%s' % self._hgext_path])
        return execute(cmd, *args, **kwargs)

    def has_pending_changes(self):
        """Check if there are changes waiting to be committed.

        Returns True if the working directory has been modified,
        otherwise returns False.
        """
        status = execute([b'hg', b'status', b'--modified', b'--added',
         b'--removed', b'--deleted'])
        return status != b''

    def apply_patch(self, patch_file, base_path=None, base_dir=None, p=None, revert=False):
        """Import the given patch.

        This will take the given patch file and apply it to the working
        directory.
        """
        cmd = [
         b'hg', b'patch', b'--no-commit']
        if p:
            cmd += [b'-p', p]
        cmd.append(patch_file)
        rc, data = self._execute(cmd, with_errors=True, return_error_code=True)
        return PatchResult(applied=rc == 0, patch_output=data)

    def apply_patch_for_empty_files(self, patch, p_num, revert=False):
        """Return True if any empty files in the patch are applied.

        If there are no empty files in the patch or if an error occurs while
        applying the patch, we return False.
        """
        patched_empty_files = False
        added_files = re.findall(b'--- %s\\t%s\\n\\+\\+\\+ b/(\\S+)\\t[^\\r\\n\\t\\f]+\\n(?:[^@]|$)' % (
         self.PRE_CREATION,
         re.escape(self.PRE_CREATION_DATE)), patch)
        deleted_files = re.findall(b'--- a/(\\S+)\\t[^\\r\\n\\t\\f]+\\n\\+\\+\\+ %s\\t%s\\n(?:[^@]|$)' % (
         self.PRE_CREATION,
         re.escape(self.PRE_CREATION_DATE)), patch)
        if added_files:
            added_files = self._strip_p_num_slashes(added_files, int(p_num))
            make_empty_files(added_files)
            result = execute([b'hg', b'add'] + added_files, ignore_errors=True, none_on_ignored_error=True)
            if result is None:
                logging.error(b'Unable to execute "hg add" on: %s', (b', ').join(added_files))
            else:
                patched_empty_files = True
        if deleted_files:
            deleted_files = self._strip_p_num_slashes(deleted_files, int(p_num))
            result = execute([b'hg', b'remove'] + deleted_files, ignore_errors=True, none_on_ignored_error=True)
            if result is None:
                logging.error(b'Unable to execute "hg remove" on: %s', (b', ').join(deleted_files))
            else:
                patched_empty_files = True
        return patched_empty_files

    def supports_empty_files(self):
        """Check if the RB server supports added/deleted empty files."""
        return self.capabilities and self.capabilities.has_capability(b'scmtools', b'mercurial', b'empty_files')