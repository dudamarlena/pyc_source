# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\rbtools\clients\perforce.py
# Compiled at: 2017-04-19 05:14:02
from __future__ import print_function, unicode_literals
import logging, marshal, os, re, six, socket, stat, string, subprocess, sys
from fnmatch import fnmatch
from locale import getpreferredencoding
from rbtools.clients import SCMClient, RepositoryInfo
from rbtools.clients.errors import AmendError, EmptyChangeError, InvalidRevisionSpecError, SCMError, TooManyRevisionsError
from rbtools.utils.checks import check_gnu_diff, check_install
from rbtools.utils.filesystem import make_empty_files, make_tempfile
from rbtools.utils.process import die, execute

class P4Wrapper(object):
    """A wrapper around p4 commands.

    All calls out to p4 go through an instance of this class. It keeps a
    separation between all the standard SCMClient logic and any parsing
    and handling of p4 invocation and results.
    """
    KEYVAL_RE = re.compile(b'^([^:]+): (.+)$')
    COUNTERS_RE = re.compile(b'^([^ ]+) = (.+)$')

    def __init__(self, options):
        self.options = options

    def is_supported(self):
        return check_install([b'p4', b'help'])

    def counters(self):
        lines = self.run_p4([b'counters'], split_lines=True)
        return self._parse_keyval_lines(lines, self.COUNTERS_RE)

    def change(self, changenum, marshalled=True, password=None):
        return self.run_p4([b'change', b'-o', str(changenum)], password=password, ignore_errors=True, none_on_ignored_error=True, marshalled=marshalled)

    def modify_change(self, new_change_spec):
        """new_change_spec must contain the changelist number."""
        return self.run_p4([b'change', b'-i'], input_string=new_change_spec)

    def files(self, path):
        return self.run_p4([b'files', path], marshalled=True)

    def filelog(self, path):
        return self.run_p4([b'filelog', path], marshalled=True)

    def fstat(self, depot_path, fields=[]):
        args = [
         b'fstat']
        if fields:
            args += [b'-T', (b',').join(fields)]
        args.append(depot_path)
        lines = self.run_p4(args, split_lines=True)
        stat_info = {}
        for line in lines:
            line = line.strip()
            if line.startswith(b'... '):
                parts = line.split(b' ', 2)
                stat_info[parts[1]] = parts[2]

        return stat_info

    def info(self):
        lines = self.run_p4([b'info'], ignore_errors=True, split_lines=True)
        return self._parse_keyval_lines(lines)

    def opened(self, changenum):
        return self.run_p4([b'opened', b'-c', str(changenum)], marshalled=True)

    def print_file(self, depot_path, out_file=None):
        cmd = [b'print']
        if out_file:
            cmd += [b'-o', out_file]
        cmd += [b'-q', depot_path]
        return self.run_p4(cmd)

    def where(self, depot_path):
        return self.run_p4([b'where', depot_path], marshalled=True)

    def run_p4(self, p4_args, marshalled=False, password=None, ignore_errors=False, input_string=None, *args, **kwargs):
        """Invoke p4.

        In the current implementation, the arguments 'marshalled' and
        'input_string' cannot be used together, i.e. this command doesn't
        allow inputting and outputting at the same time.
        """
        cmd = [
         b'p4']
        if marshalled:
            cmd += [b'-G']
        if getattr(self.options, b'p4_client', None):
            cmd += [b'-c', self.options.p4_client]
        if getattr(self.options, b'p4_port', None):
            cmd += [b'-p', self.options.p4_port]
        if getattr(self.options, b'p4_passwd', None):
            cmd += [b'-P', self.options.p4_passwd]
        cmd += p4_args
        if password is not None:
            cmd += [b'-P', password]
        if marshalled:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            result = []
            has_error = False
            while 1:
                try:
                    data = marshal.load(p.stdout)
                except EOFError:
                    break
                else:
                    result.append(data)
                    if data.get(b'code', None) == b'error':
                        has_error = True

            rc = p.wait()
            if not ignore_errors and (rc or has_error):
                for record in result:
                    if b'data' in record:
                        print(record[b'data'])

                raise SCMError(b'Failed to execute command: %s\n' % cmd)
            return result
        if input_string is not None:
            p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
            p.communicate(input_string)
            if not ignore_errors and p.returncode:
                raise SCMError(b'Failed to execute command: %s\n' % cmd)
            return
        result = execute(cmd, ignore_errors=ignore_errors, *args, **kwargs)
        return result

    def _parse_keyval_lines(self, lines, regex=KEYVAL_RE):
        keyvals = {}
        for line in lines:
            m = regex.match(line)
            if m:
                key = m.groups()[0]
                value = m.groups()[1]
                keyvals[key] = value.strip()

        return keyvals


class PerforceClient(SCMClient):
    """
    A wrapper around the p4 Perforce tool that fetches repository information
    and generates compatible diffs.
    """
    name = b'Perforce'
    can_amend_commit = True
    supports_diff_exclude_patterns = True
    supports_diff_extra_args = True
    supports_patch_revert = True
    DATE_RE = re.compile(b'(\\w+)\\s+(\\w+)\\s+(\\d+)\\s+(\\d\\d:\\d\\d:\\d\\d)\\s+(\\d\\d\\d\\d)')
    ENCODED_COUNTER_URL_RE = re.compile(b'reviewboard.url\\.(\\S+)')
    REVISION_CURRENT_SYNC = b'--rbtools-current-sync'
    REVISION_PENDING_CLN_PREFIX = b'--rbtools-pending-cln:'
    REVISION_DEFAULT_CLN = b'default'
    ADDED_FILES_RE = re.compile(b'^==== //depot/(\\S+)#\\d+ ==A== \\S+ ====$', re.M)
    DELETED_FILES_RE = re.compile(b'^==== //depot/(\\S+)#\\d+ ==D== \\S+ ====$', re.M)

    def __init__(self, p4_class=P4Wrapper, **kwargs):
        super(PerforceClient, self).__init__(**kwargs)
        self.p4 = p4_class(self.options)

    def get_repository_info(self):
        if not self.p4.is_supported():
            logging.debug(b'Unable to execute "p4 help": skipping Perforce')
            return
        else:
            p4_info = self.p4.info()
            repository_path = p4_info.get(b'Broker address') or p4_info.get(b'Server address')
            if repository_path is None:
                return
            client_root = p4_info.get(b'Client root')
            if client_root is None:
                return
            if client_root.lower() != b'null' or not sys.platform.startswith(b'win'):
                norm_cwd = os.path.normcase(os.path.realpath(os.getcwd()) + os.path.sep)
                norm_client_root = os.path.normcase(os.path.realpath(client_root) + os.path.sep)
                if not norm_cwd.startswith(norm_client_root):
                    return
            try:
                parts = repository_path.split(b':')
                hostname = None
                if len(parts) == 3 and parts[0] == b'ssl':
                    hostname = parts[1]
                    port = parts[2]
                elif len(parts) == 2:
                    hostname, port = parts
                if not hostname:
                    die(b'Path %s is not a valid Perforce P4PORT' % repository_path)
                info = socket.gethostbyaddr(hostname)
                servers = [
                 hostname]
                if info[0] != hostname:
                    servers.append(info[0])
                if info[1]:
                    servers += info[1]
                repository_path = [ b'%s:%s' % (server, port) for server in servers
                                  ]
                if len(repository_path) == 1:
                    repository_path = repository_path[0]
            except (socket.gaierror, socket.herror):
                pass

            server_version = p4_info.get(b'Server version', None)
            if not server_version:
                return
            m = re.search(b'[^ ]*/([0-9]+)\\.([0-9]+)/[0-9]+ .*$', server_version, re.M)
            if m:
                self.p4d_version = (
                 int(m.group(1)), int(m.group(2)))
            else:
                return
            check_gnu_diff()
            return RepositoryInfo(path=repository_path, supports_changesets=True)

    def parse_revision_spec(self, revisions=[]):
        """Parses the given revision spec.

        The 'revisions' argument is a list of revisions as specified by the
        user. Items in the list do not necessarily represent a single revision,
        since the user can use SCM-native syntaxes such as "r1..r2" or "r1:r2".
        SCMTool-specific overrides of this method are expected to deal with
        such syntaxes.

        This will return a dictionary with the following keys:
            'base':        A revision to use as the base of the resulting diff.
            'tip':         A revision to use as the tip of the resulting diff.

        These will be used to generate the diffs to upload to Review Board (or
        print). The diff for review will include the changes in (base, tip].

        If zero revisions are passed in, this will return the 'default'
        changelist.

        If a single revision is passed in, this will return the parent of that
        revision for 'base' and the passed-in revision for 'tip'. The result
        may have special internal revisions or prefixes based on whether the
        changeset is submitted, pending, or shelved.

        If two revisions are passed in, they need to both be submitted
        changesets.
        """
        n_revs = len(revisions)
        if n_revs == 0:
            return {b'base': self.REVISION_CURRENT_SYNC, 
               b'tip': self.REVISION_PENDING_CLN_PREFIX + self.REVISION_DEFAULT_CLN}
        if n_revs == 1:
            status = self._get_changelist_status(revisions[0])
            if status in ('pending', 'shelved'):
                return {b'base': self.REVISION_CURRENT_SYNC, 
                   b'tip': self.REVISION_PENDING_CLN_PREFIX + revisions[0]}
            if status == b'submitted':
                try:
                    cln = int(revisions[0])
                    return {b'base': str(cln - 1), 
                       b'tip': str(cln)}
                except ValueError:
                    raise InvalidRevisionSpecError(b'%s does not appear to be a valid changelist' % revisions[0])

            else:
                raise InvalidRevisionSpecError(b'%s does not appear to be a valid changelist' % revisions[0])
        else:
            if n_revs == 2:
                result = {}
                status = self._get_changelist_status(revisions[0])
                if status == b'submitted':
                    result[b'base'] = revisions[0]
                elif status in ('pending', 'shelved'):
                    raise InvalidRevisionSpecError(b'%s cannot be used as the base CLN for a diff because it is %s.' % (
                     revisions[0], status))
                else:
                    raise InvalidRevisionSpecError(b'%s does not appear to be a valid changelist' % revisions[0])
                status = self._get_changelist_status(revisions[1])
                if status == b'submitted':
                    result[b'tip'] = revisions[1]
                elif status in ('pending', 'shelved'):
                    raise InvalidRevisionSpecError(b'%s cannot be used for a revision range diff because it is %s' % (
                     revisions[1], status))
                else:
                    raise InvalidRevisionSpecError(b'%s does not appear to be a valid changelist' % revisions[1])
                return result
            raise TooManyRevisionsError

    def _get_changelist_status(self, changelist):
        if changelist == self.REVISION_DEFAULT_CLN:
            return b'pending'
        else:
            change = self.p4.change(changelist)
            if len(change) == 1 and b'Status' in change[0]:
                return change[0][b'Status']
            return

    def scan_for_server(self, repository_info):
        server_url = super(PerforceClient, self).scan_for_server(repository_info)
        if server_url:
            return server_url
        return self.scan_for_server_counter(repository_info)

    def scan_for_server_counter(self, repository_info):
        """
        Checks the Perforce counters to see if the Review Board server's url
        is specified. Since Perforce only started supporting non-numeric
        counter values in server version 2008.1, we support both a normal
        counter 'reviewboard.url' with a string value and embedding the url in
        a counter name like 'reviewboard.url.http:||reviewboard.example.com'.
        Note that forward slashes aren't allowed in counter names, so
        pipe ('|') characters should be used. These should be safe because they
        should not be used unencoded in urls.
        """
        counters = self.p4.counters()
        url = counters.get(b'reviewboard.url', None)
        if url:
            return url
        else:
            for key, value in six.iteritems(counters):
                m = self.ENCODED_COUNTER_URL_RE.match(key)
                if m:
                    return m.group(1).replace(b'|', b'/')

            return

    def diff(self, revisions, include_files=[], exclude_patterns=[], extra_args=[]):
        """
        Goes through the hard work of generating a diff on Perforce in order
        to take into account adds/deletes and to provide the necessary
        revision information.
        """
        exclude_patterns = self.normalize_exclude_patterns(exclude_patterns)
        if not revisions:
            return self._path_diff(extra_args, exclude_patterns)
        depot_include_files = []
        local_include_files = []
        for filename in include_files:
            if filename.startswith(b'//'):
                depot_include_files.append(filename)
            else:
                local_include_files.append(os.path.realpath(os.path.abspath(filename)))

        base = revisions[b'base']
        tip = revisions[b'tip']
        cl_is_pending = tip.startswith(self.REVISION_PENDING_CLN_PREFIX)
        cl_is_shelved = False
        if not cl_is_pending:
            logging.info(b'Generating diff for range of submitted changes: %s to %s', base, tip)
            return self._compute_range_changes(base, tip, depot_include_files, local_include_files, exclude_patterns)
        tip = tip.split(b':', 1)[1]
        opened_files = self.p4.opened(tip)
        if not opened_files:
            opened_files = self.p4.files(b'//...@=%s' % tip)
            cl_is_shelved = True
        if not opened_files:
            raise EmptyChangeError
        if cl_is_shelved:
            logging.info(b'Generating diff for shelved changeset %s' % tip)
        else:
            logging.info(b'Generating diff for pending changeset %s' % tip)
        diff_lines = []
        action_mapping = {b'edit': b'M', 
           b'integrate': b'M', 
           b'add': b'A', 
           b'branch': b'A', 
           b'import': b'A', 
           b'delete': b'D'}
        if self._supports_moves() and not cl_is_shelved:
            action_mapping[b'move/add'] = b'MV-a'
            action_mapping[b'move/delete'] = b'MV'
        else:
            action_mapping[b'move/add'] = b'A'
            action_mapping[b'move/delete'] = b'D'
        for f in opened_files:
            depot_file = f[b'depotFile']
            local_file = self._depot_to_local(depot_file)
            new_depot_file = b''
            try:
                base_revision = int(f[b'rev'])
            except ValueError:
                base_revision = f[b'rev']

            action = f[b'action']
            if depot_include_files and depot_file not in depot_include_files or local_include_files and local_file not in local_include_files or self._should_exclude_file(local_file, depot_file, exclude_patterns):
                continue
            old_file = b''
            new_file = b''
            logging.debug(b'Processing %s of %s', action, depot_file)
            try:
                changetype_short = action_mapping[action]
            except KeyError:
                die(b'Unsupported action type "%s" for %s' % (
                 action, depot_file))

            if changetype_short == b'M':
                try:
                    old_file, new_file = self._extract_edit_files(depot_file, local_file, base_revision, tip, cl_is_shelved, False)
                except ValueError as e:
                    logging.warning(b'Skipping file %s: %s', depot_file, e)
                    continue

            elif changetype_short == b'A':
                base_revision = 0
                try:
                    old_file, new_file = self._extract_add_files(depot_file, local_file, tip, cl_is_shelved, cl_is_pending)
                except ValueError as e:
                    logging.warning(b'Skipping file %s: %s', depot_file, e)
                    continue

                if os.path.islink(new_file):
                    logging.warning(b'Skipping symlink %s', new_file)
                    continue
            elif changetype_short == b'D':
                try:
                    old_file, new_file = self._extract_delete_files(depot_file, base_revision)
                except ValueError as e:
                    logging.warning(b'Skipping file %s#%s: %s', depot_file, base_revision, e)
                    continue

            elif changetype_short == b'MV-a':
                continue
            elif changetype_short == b'MV':
                try:
                    old_file, new_file, new_depot_file = self._extract_move_files(depot_file, tip, base_revision, cl_is_shelved)
                except ValueError as e:
                    logging.warning(b'Skipping file %s: %s', depot_file, e)
                    continue

            dl = self._do_diff(old_file, new_file, depot_file, base_revision, new_depot_file, changetype_short, ignore_unmodified=True)
            diff_lines += dl

        return {b'diff': (b'').join(diff_lines), 
           b'changenum': self.get_changenum(revisions)}

    def get_changenum(self, revisions):
        """Return the change number for the given revisions.

        This is only used when the client is supposed to send a change number
        to the server (such as with Perforce).

        Args:
            revisions (dict):
                A revisions dictionary as returned by ``parse_revision_spec``.

        Returns:
            unicode:
            The change number to send to the Review Board server.
        """
        if revisions is not None:
            tip = revisions[b'tip']
            if tip.startswith(self.REVISION_PENDING_CLN_PREFIX):
                tip = tip[len(self.REVISION_PENDING_CLN_PREFIX):]
                if tip != self.REVISION_DEFAULT_CLN:
                    return tip
        return

    def _compute_range_changes(self, base, tip, depot_include_files, local_include_files, exclude_patterns):
        """Compute the changes across files given a revision range.

        This will look at the history of all changes within the given range and
        compute the full set of changes contained therein. Just looking at the
        two trees isn't enough, since files may have moved around and we want
        to include that information.
        """
        changesets = {}
        real_base = str(int(base) + 1)
        for file_entry in self.p4.filelog(b'//...@%s,%s' % (real_base, tip)):
            cid = 0
            while True:
                change_key = b'change%d' % cid
                if change_key not in file_entry:
                    break
                action = file_entry[(b'action%d' % cid)]
                depot_file = file_entry[b'depotFile']
                try:
                    cln = int(file_entry[change_key])
                except ValueError:
                    logging.warning(b'Skipping file %s: unable to parse change number "%s"', depot_file, file_entry[change_key])
                    break

                if action == b'integrate':
                    action = b'edit'
                else:
                    if action == b'branch':
                        action = b'add'
                    if action not in ('edit', 'add', 'delete', 'move/add', 'move/delete'):
                        raise Exception(b'Unsupported action type "%s" for %s' % (
                         action, depot_file))
                    try:
                        rev_key = b'rev%d' % cid
                        rev = int(file_entry[rev_key])
                    except ValueError:
                        logging.warning(b'Skipping file %s: unable to parse revision number "%s"', depot_file, file_entry[rev_key])
                        break

                change = {b'rev': rev, b'action': action}
                if action == b'move/add':
                    change[b'oldFilename'] = file_entry[(b'file0,%d' % cid)]
                elif action == b'move/delete':
                    change[b'newFilename'] = file_entry[(b'file1,%d' % cid)]
                cid += 1
                changesets.setdefault(cln, {})[depot_file] = change

        files = []
        for cln in sorted(changesets.keys()):
            changeset = changesets[cln]
            for depot_file, change in six.iteritems(changeset):
                action = change[b'action']
                if action == b'move/add':
                    continue
                file_entry = None
                for f in files:
                    if f[b'depotFile'] == depot_file:
                        file_entry = f
                        break

                if file_entry is None:
                    file_entry = {b'initialDepotFile': depot_file, b'initialRev': change[b'rev'], 
                       b'newFile': action == b'add', 
                       b'rev': change[b'rev'], 
                       b'action': b'none'}
                    files.append(file_entry)
                self._accumulate_range_change(file_entry, change)

        if not files:
            raise EmptyChangeError
        supports_moves = self._supports_moves()
        diff_lines = []
        for f in files:
            action = f[b'action']
            depot_file = f[b'depotFile']
            try:
                local_file = self._depot_to_local(depot_file)
            except SCMError:
                logging.warning(b'Could not find local filename for "%s"', depot_file)
                local_file = None

            rev = f[b'rev']
            initial_depot_file = f[b'initialDepotFile']
            initial_rev = f[b'initialRev']
            if depot_include_files and depot_file not in depot_include_files or local_include_files and local_file and local_file not in local_include_files or self._should_exclude_file(local_file, depot_file, exclude_patterns):
                continue
            if action == b'add':
                try:
                    old_file, new_file = self._extract_add_files(depot_file, local_file, rev, False, False)
                except ValueError as e:
                    logging.warning(b'Skipping file %s: %s', depot_file, e)
                    continue

                diff_lines += self._do_diff(old_file, new_file, depot_file, 0, b'', b'A', ignore_unmodified=True)
            elif action == b'delete':
                try:
                    old_file, new_file = self._extract_delete_files(initial_depot_file, initial_rev)
                except ValueError:
                    logging.warning(b'Skipping file %s: %s', depot_file, e)
                    continue

                diff_lines += self._do_diff(old_file, new_file, initial_depot_file, initial_rev, depot_file, b'D', ignore_unmodified=True)
            elif action == b'edit':
                try:
                    old_file, new_file = self._extract_edit_files(depot_file, local_file, initial_rev, rev, False, True)
                except ValueError:
                    logging.warning(b'Skipping file %s: %s', depot_file, e)
                    continue

                diff_lines += self._do_diff(old_file, new_file, initial_depot_file, initial_rev, depot_file, b'M', ignore_unmodified=True)
            elif action == b'move':
                try:
                    old_file_a, new_file_a = self._extract_add_files(depot_file, local_file, rev, False, False)
                    old_file_b, new_file_b = self._extract_delete_files(initial_depot_file, initial_rev)
                except ValueError:
                    logging.warning(b'Skipping file %s: %s', depot_file, e)
                    continue

                if supports_moves:
                    diff_lines += self._do_diff(old_file_a, new_file_b, initial_depot_file, initial_rev, depot_file, b'MV', ignore_unmodified=True)
                else:
                    diff_lines += self._do_diff(old_file_a, new_file_a, depot_file, 0, b'', b'A', ignore_unmodified=True)
                    diff_lines += self._do_diff(old_file_b, new_file_b, initial_depot_file, initial_rev, depot_file, b'D', ignore_unmodified=True)
            elif action == b'skip':
                continue
            elif not False:
                raise AssertionError

        return {b'diff': (b'').join(diff_lines)}

    def _accumulate_range_change(self, file_entry, change):
        """Compute the effects of a given change on a given file"""
        old_action = file_entry[b'action']
        current_action = change[b'action']
        if old_action == b'none':
            new_action = current_action
            file_entry[b'depotFile'] = file_entry[b'initialDepotFile']
            if current_action in ('edit', 'delete'):
                file_entry[b'initialRev'] -= 1
        elif current_action == b'add':
            if old_action == b'skip':
                new_action = b'add'
            else:
                new_action = b'edit'
        elif current_action == b'edit':
            new_action = old_action
        elif current_action == b'delete':
            if file_entry[b'newFile']:
                new_action = b'skip'
            else:
                new_action = b'delete'
        elif current_action == b'move/delete':
            new_action = b'move'
            file_entry[b'depotFile'] = change[b'newFilename']
        file_entry[b'rev'] = change[b'rev']
        file_entry[b'action'] = new_action

    def _extract_edit_files(self, depot_file, local_file, rev_a, rev_b, cl_is_shelved, cl_is_submitted):
        """Extract the 'old' and 'new' files for an edit operation.

        Returns a tuple of (old filename, new filename). This can raise a
        ValueError if the extraction fails.
        """
        old_filename = make_tempfile()
        self._write_file(b'%s#%s' % (depot_file, rev_a), old_filename)
        if cl_is_shelved:
            new_filename = make_tempfile()
            self._write_file(b'%s@=%s' % (depot_file, rev_b), new_filename)
        elif cl_is_submitted:
            new_filename = make_tempfile()
            self._write_file(b'%s#%s' % (depot_file, rev_b), new_filename)
        else:
            new_filename = local_file
        return (old_filename, new_filename)

    def _extract_add_files(self, depot_file, local_file, revision, cl_is_shelved, cl_is_pending):
        """Extract the 'old' and 'new' files for an add operation.

        Returns a tuple of (old filename, new filename). This can raise a
        ValueError if the extraction fails.
        """
        old_filename = make_tempfile()
        if cl_is_shelved:
            new_filename = make_tempfile()
            self._write_file(b'%s@=%s' % (depot_file, revision), new_filename)
        elif cl_is_pending:
            new_filename = local_file
        else:
            new_filename = make_tempfile()
            self._write_file(b'%s#%s' % (depot_file, revision), new_filename)
        return (old_filename, new_filename)

    def _extract_delete_files(self, depot_file, revision):
        """Extract the 'old' and 'new' files for a delete operation.

        Returns a tuple of (old filename, new filename). This can raise a
        ValueError if extraction fails.
        """
        old_filename = make_tempfile()
        self._write_file(b'%s#%s' % (depot_file, revision), old_filename)
        new_filename = make_tempfile()
        return (
         old_filename, new_filename)

    def _extract_move_files(self, old_depot_file, tip, base_revision, cl_is_shelved):
        """Extract the 'old' and 'new' files for a move operation.

        Returns a tuple of (old filename, new filename, new depot path). This
        can raise a ValueError if extraction fails.
        """
        assert not cl_is_shelved
        fstat_path = old_depot_file
        stat_info = self.p4.fstat(fstat_path, [
         b'clientFile', b'movedFile'])
        if b'clientFile' not in stat_info or b'movedFile' not in stat_info:
            raise ValueError(b'Unable to get moved file information')
        old_filename = make_tempfile()
        self._write_file(b'%s#%s' % (old_depot_file, base_revision), old_filename)
        fstat_path = stat_info[b'movedFile']
        stat_info = self.p4.fstat(fstat_path, [
         b'clientFile', b'depotFile'])
        if b'clientFile' not in stat_info or b'depotFile' not in stat_info:
            raise ValueError(b'Unable to get moved file information')
        new_depot_file = stat_info[b'depotFile']
        new_filename = stat_info[b'clientFile']
        return (
         old_filename, new_filename, new_depot_file)

    def _path_diff(self, args, exclude_patterns):
        """
        Process a path-style diff. This allows people to post individual files
        in various ways.

        Multiple paths may be specified in `args`.  The path styles supported
        are:

        //path/to/file
        Upload file as a "new" file.

        //path/to/dir/...
        Upload all files as "new" files.

        //path/to/file[@#]rev
        Upload file from that rev as a "new" file.

        //path/to/file[@#]rev,[@#]rev
        Upload a diff between revs.

        //path/to/dir/...[@#]rev,[@#]rev
        Upload a diff of all files between revs in that directory.
        """
        r_revision_range = re.compile(b'^(?P<path>//[^@#]+)' + b'(?P<revision1>[#@][^,]+)?' + b'(?P<revision2>,[#@][^,]+)?$')
        empty_filename = make_tempfile()
        tmp_diff_from_filename = make_tempfile()
        tmp_diff_to_filename = make_tempfile()
        diff_lines = []
        for path in args:
            m = r_revision_range.match(path)
            if not m:
                die(b'Path %r does not match a valid Perforce path.' % (path,))
            revision1 = m.group(b'revision1')
            revision2 = m.group(b'revision2')
            first_rev_path = m.group(b'path')
            if revision1:
                first_rev_path += revision1
            records = self.p4.files(first_rev_path)
            files = {}
            for record in records:
                if record[b'action'] not in ('delete', 'move/delete'):
                    if revision2:
                        files[record[b'depotFile']] = [
                         record, None]
                    else:
                        files[record[b'depotFile']] = [
                         None, record]

            if revision2:
                second_rev_path = m.group(b'path') + revision2[1:]
                records = self.p4.files(second_rev_path)
                for record in records:
                    if record[b'action'] not in ('delete', 'move/delete'):
                        try:
                            m = files[record[b'depotFile']]
                            m[1] = record
                        except KeyError:
                            files[record[b'depotFile']] = [
                             None, record]

            old_file = new_file = empty_filename
            changetype_short = None
            for depot_path, (first_record, second_record) in six.iteritems(files):
                old_file = new_file = empty_filename
                if first_record is None:
                    new_path = b'%s#%s' % (depot_path, second_record[b'rev'])
                    self._write_file(new_path, tmp_diff_to_filename)
                    new_file = tmp_diff_to_filename
                    changetype_short = b'A'
                    base_revision = 0
                elif second_record is None:
                    old_path = b'%s#%s' % (depot_path, first_record[b'rev'])
                    self._write_file(old_path, tmp_diff_from_filename)
                    old_file = tmp_diff_from_filename
                    changetype_short = b'D'
                    base_revision = int(first_record[b'rev'])
                elif first_record[b'rev'] == second_record[b'rev']:
                    continue
                else:
                    old_path = b'%s#%s' % (depot_path, first_record[b'rev'])
                    new_path = b'%s#%s' % (depot_path, second_record[b'rev'])
                    self._write_file(old_path, tmp_diff_from_filename)
                    self._write_file(new_path, tmp_diff_to_filename)
                    new_file = tmp_diff_to_filename
                    old_file = tmp_diff_from_filename
                    changetype_short = b'M'
                    base_revision = int(first_record[b'rev'])
                local_path = self._depot_to_local(depot_path)
                if self._should_exclude_file(local_path, depot_path, exclude_patterns):
                    continue
                dl = self._do_diff(old_file, new_file, depot_path, base_revision, b'', changetype_short, ignore_unmodified=True)
                diff_lines += dl

        os.unlink(empty_filename)
        os.unlink(tmp_diff_from_filename)
        os.unlink(tmp_diff_to_filename)
        return {b'diff': (b'').join(diff_lines)}

    def _do_diff(self, old_file, new_file, depot_file, base_revision, new_depot_file, changetype_short, ignore_unmodified=False):
        """
        Do the work of producing a diff for Perforce.

        old_file - The absolute path to the "old" file.
        new_file - The absolute path to the "new" file.
        depot_file - The depot path in Perforce for this file.
        base_revision - The base perforce revision number of the old file as
            an integer.
        new_depot_file - Location of the new file. Only used for moved files.
        changetype_short - The change type as a short string.
        ignore_unmodified - If True, will return an empty list if the file
            is not changed.

        Returns a list of strings of diff lines.
        """
        if hasattr(os, b'uname') and os.uname()[0] == b'SunOS':
            diff_cmd = [
             b'gdiff', b'-urNp', old_file, new_file]
        else:
            diff_cmd = [
             b'diff', b'-urNp', old_file, new_file]
        dl = execute(diff_cmd, extra_ignore_errors=(1, 2), log_output_on_error=False, translate_newlines=False, results_unicode=False)
        dl = dl.replace(b'\r\r\n', b'\r\n')
        dl = dl.splitlines(True)
        cwd = os.getcwd()
        if depot_file.startswith(cwd):
            local_path = depot_file[len(cwd) + 1:]
        else:
            local_path = depot_file
        if changetype_short == b'MV':
            is_move = True
            if new_depot_file.startswith(cwd):
                new_local_path = new_depot_file[len(cwd) + 1:]
            else:
                new_local_path = new_depot_file
        else:
            is_move = False
            new_local_path = local_path
        if len(dl) == 1 and dl[0].startswith(b'Files %s and %s differ' % (
         old_file, new_file)):
            dl = [
             b'Binary files %s and %s differ\n' % (old_file, new_file)]
        if dl == [] or dl[0].startswith(b'Binary files '):
            is_empty_and_changed = self.supports_empty_files() and changetype_short in ('A',
                                                                                        'D')
            if dl == [] and (is_move or is_empty_and_changed):
                line = (b'==== %s#%s ==%s== %s ====\n' % (
                 depot_file, base_revision, changetype_short,
                 new_local_path)).encode(b'utf-8')
                dl.insert(0, line)
                dl.append(b'\n')
            else:
                if ignore_unmodified:
                    return []
                print(b'Warning: %s in your changeset is unmodified' % local_path)
        elif len(dl) > 1:
            m = re.search(b'(\\d\\d\\d\\d-\\d\\d-\\d\\d \\d\\d:\\d\\d:\\d\\d)', dl[1])
            if m:
                timestamp = m.group(1).decode(b'utf-8')
            else:
                m = self.DATE_RE.search(dl[1])
                if not m:
                    die(b'Unable to parse diff header: %s' % dl[1])
                month_map = {b'Jan': b'01', 
                   b'Feb': b'02', 
                   b'Mar': b'03', 
                   b'Apr': b'04', 
                   b'May': b'05', 
                   b'Jun': b'06', 
                   b'Jul': b'07', 
                   b'Aug': b'08', 
                   b'Sep': b'09', 
                   b'Oct': b'10', 
                   b'Nov': b'11', 
                   b'Dec': b'12'}
                month = month_map[m.group(2)]
                day = m.group(3)
                timestamp = m.group(4)
                year = m.group(5)
                timestamp = b'%s-%s-%s %s' % (year, month, day, timestamp)
            dl[0] = (b'--- %s\t%s#%s\n' % (
             local_path, depot_file, base_revision)).encode(b'utf-8')
            dl[1] = (b'+++ %s\t%s\n' % (
             new_local_path, timestamp)).encode(b'utf-8')
            if is_move:
                dl.insert(0, (b'Moved to: %s\n' % new_depot_file).encode(b'utf-8'))
                dl.insert(0, (b'Moved from: %s\n' % depot_file).encode(b'utf-8'))
            if not dl[(-1)].endswith(b'\n'):
                dl.append(b'\n')
        else:
            die(b'ERROR, no valid diffs: %s' % dl[0].decode(b'utf-8'))
        return dl

    def _write_file(self, depot_path, tmpfile):
        """
        Grabs a file from Perforce and writes it to a temp file. p4 print sets
        the file readonly and that causes a later call to unlink fail. So we
        make the file read/write.
        """
        logging.debug(b'Writing "%s" to "%s"' % (depot_path, tmpfile))
        self.p4.print_file(depot_path, out_file=tmpfile)
        if os.path.islink(tmpfile):
            raise ValueError(b'"%s" is a symlink' % depot_path)
        else:
            os.chmod(tmpfile, stat.S_IREAD | stat.S_IWRITE)

    def _depot_to_local(self, depot_path):
        """
        Given a path in the depot return the path on the local filesystem to
        the same file.  If there are multiple results, take only the last
        result from the where command.
        """
        where_output = self.p4.where(depot_path)
        try:
            return where_output[(-1)][b'path']
        except:
            return where_output[(-1)][b'data'].split(b' ')[2].strip()

    def get_raw_commit_message(self, revisions):
        """Extract the commit message based on the provided revision range.

        Since local changelists in perforce are not ordered with respect to
        one another, this implementation looks at only the tip revision.
        """
        changelist = revisions[b'tip']
        if b':' in changelist:
            changelist = changelist.split(b':', 1)[1]
        if changelist == self.REVISION_DEFAULT_CLN:
            return b''
        else:
            logging.debug(b'Fetching description for changelist %s', changelist)
            change = self.p4.change(changelist)
            if len(change) == 1 and b'Description' in change[0]:
                return change[0][b'Description'].decode(getpreferredencoding())
            return b''

    def apply_patch_for_empty_files(self, patch, p_num, revert=False):
        """Returns True if any empty files in the patch are applied.

        If there are no empty files in the patch or if an error occurs while
        applying the patch, we return False.
        """
        patched_empty_files = False
        if revert:
            added_files = self.DELETED_FILES_RE.findall(patch)
            deleted_files = self.ADDED_FILES_RE.findall(patch)
        else:
            added_files = self.ADDED_FILES_RE.findall(patch)
            deleted_files = self.DELETED_FILES_RE.findall(patch)
        p4_info = self.p4.info()
        client_root = p4_info.get(b'Client root')
        added_files = [ b'%s/%s' % (client_root, f) for f in added_files ]
        deleted_files = [ b'%s/%s' % (client_root, f) for f in deleted_files ]
        if added_files:
            make_empty_files(added_files)
            result = execute([b'p4', b'add'] + added_files, ignore_errors=True, none_on_ignored_error=True)
            if result is None:
                logging.error(b'Unable to execute "p4 add" on: %s', (b', ').join(added_files))
            else:
                patched_empty_files = True
        if deleted_files:
            result = execute([b'p4', b'delete'] + deleted_files, ignore_errors=True, none_on_ignored_error=True)
            if result is None:
                logging.error(b'Unable to execute "p4 delete" on: %s', (b', ').join(deleted_files))
            else:
                patched_empty_files = True
        return patched_empty_files

    def _supports_moves(self):
        return self.capabilities and self.capabilities.has_capability(b'scmtools', b'perforce', b'moved_files')

    def _supports_empty_files(self):
        """Checks if the RB server supports added/deleted empty files."""
        return self.capabilities and self.capabilities.has_capability(b'scmtools', b'perforce', b'empty_files')

    def _should_exclude_file(self, local_file, depot_file, exclude_patterns):
        """Determine if a file should be excluded from a diff.

        Check if the file identified by (local_file, depot_file) should be
        excluded from the diff. If a pattern beings with '//', then it will be
        matched against the depot_file. Otherwise, it will be matched against
        the local file.

        This function expects `exclude_patterns` to be normalized.
        """
        for pattern in exclude_patterns:
            if pattern.startswith(b'//'):
                if fnmatch(depot_file, pattern):
                    return True
            elif local_file and fnmatch(local_file, pattern):
                return True

        return False

    def normalize_exclude_patterns(self, patterns):
        """Normalize the set of patterns so all non-depot paths are absolute.

        A path with a leading // is interpreted as a depot pattern and remains
        unchanged. A path with a leading path separator is interpreted as being
        relative to the Perforce client root. All other paths are interpreted
        as being relative to the current working directory. Non-depot paths are
        transformed into absolute paths.
        """
        cwd = os.getcwd()
        base_dir = self.p4.info().get(b'Client root')

        def normalize(p):
            if p.startswith(b'//'):
                return p
            else:
                if pattern.startswith(os.path.sep):
                    assert base_dir is not None
                    p = os.path.join(base_dir, p[1:])
                else:
                    p = os.path.join(cwd, p)
                return os.path.normpath(p)

        return [ normalize(pattern) for pattern in patterns ]

    def _replace_description_in_changelist_spec(self, old_spec, new_description):
        """Replace the description in the given changelist spec.

        old_spec is a formatted p4 changelist spec string (the raw output from
        p4 change). This method replaces the existing description with
        new_description, and returns the new changelist spec.
        """
        new_spec = b''
        whitespace = tuple(string.whitespace)
        description_key = b'Description:'
        skipping_old_description = False
        for line in old_spec.splitlines(True):
            if not skipping_old_description:
                if not line.startswith(description_key):
                    new_spec += line
                else:
                    skipping_old_description = True
                    new_spec += description_key
                    for desc_line in new_description.splitlines():
                        new_spec += b'\t%s\n' % desc_line

            elif line.startswith(whitespace):
                continue
            else:
                skipping_old_description = False
                new_spec += b'\n%s' % line

        return new_spec

    def amend_commit_description(self, message, revisions):
        """Update a commit message to the given string.

        Since local changelists on perforce have no ordering with respect to
        each other, the revisions argument is mandatory.
        """
        changelist_id = revisions[b'tip']
        logging.debug(b'Preparing to amend change %s' % changelist_id)
        if not changelist_id.startswith(self.REVISION_PENDING_CLN_PREFIX):
            raise AmendError(b'Cannot modify submitted changelist %s' % changelist_id)
        changelist_num = changelist_id.split(b':', 1)[1]
        if changelist_num == self.REVISION_DEFAULT_CLN:
            raise AmendError(b'Cannot modify the default changelist')
        elif not changelist_num.isdigit():
            raise AmendError(b'%s is an invalid changelist ID' % changelist_num)
        change = self.p4.change(changelist_num, marshalled=False)
        new_change = self._replace_description_in_changelist_spec(change, message)
        self.p4.modify_change(new_change)