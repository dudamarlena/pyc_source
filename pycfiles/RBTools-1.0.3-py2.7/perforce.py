# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/rbtools/clients/perforce.py
# Compiled at: 2020-04-14 20:27:46
"""A client for Perforce."""
from __future__ import print_function, unicode_literals
import logging, marshal, os, re, socket, stat, string, subprocess, sys
from fnmatch import fnmatch
from locale import getpreferredencoding
import six
from rbtools.clients import SCMClient, RepositoryInfo
from rbtools.clients.errors import AmendError, EmptyChangeError, InvalidRevisionSpecError, SCMError, TooManyRevisionsError
from rbtools.utils.checks import check_gnu_diff, check_install
from rbtools.utils.encoding import force_unicode
from rbtools.utils.filesystem import make_empty_files, make_tempfile
from rbtools.utils.process import execute

class P4Wrapper(object):
    """A wrapper around p4 commands.

    All calls out to p4 go through an instance of this class. It keeps a
    separation between all the standard SCMClient logic and any parsing
    and handling of p4 invocation and results.
    """
    KEYVAL_RE = re.compile(b'^([^:]+): (.+)$')
    COUNTERS_RE = re.compile(b'^([^ ]+) = (.+)$')

    def __init__(self, options):
        """Initialize the wrapper.

        Args:
            options (argparse.Namespace):
                The parsed command line options.
        """
        self.options = options

    def is_supported(self):
        """Check whether the p4 command is usable.

        Returns:
            bool:
            ``True`` if there's an executable p4.
        """
        return check_install([b'p4', b'help'])

    def counters(self):
        """Return the Perforce counters.

        Returns:
            dict:
            The parsed Perforce counters.
        """
        lines = self.run_p4([b'counters'], split_lines=True)
        return self._parse_keyval_lines(lines, self.COUNTERS_RE)

    def change(self, changenum, marshalled=True):
        """Return the contents of a p4 change description.

        Args:
            changenum (int):
                The number of the changeset to list.

            marshalled (bool, optional):
                Whether to return the data in marshalled form.

        Returns:
            object:
            The contents of the change description, either as a unicode
            object or a list depending on the value of ``marshalled``.
        """
        return self.run_p4([b'change', b'-o', str(changenum)], ignore_errors=True, none_on_ignored_error=True, marshalled=marshalled)

    def modify_change(self, new_change_spec):
        """Modify a change description.

        Args:
            new_change_spec (unicode):
                The new changeset description. This must contain the changelist
                number.
        """
        self.run_p4([b'change', b'-i'], input_string=new_change_spec)

    def files(self, path):
        """Return the opened files within the given path.

        Args:
            path (unicode):
                The Perforce path to check. This can be a mix of file paths
                (``//...``) and revisions (``...@X``).

        Returns:
            list:
            A list of the opened files.
        """
        return self.run_p4([b'files', path], marshalled=True)

    def filelog(self, path):
        """Return a list of all the changed files within the given path.

        Args:
            path (unicode):
                The Perforce path to check. This is expected to be a path with
                two revision markers (``//...@X,Y``).

        Returns:
            list:
            A list of the various changed files and how they were changed.
        """
        return self.run_p4([b'filelog', path], marshalled=True)

    def fstat(self, depot_path, fields=[]):
        """Run p4 fstat on a given depot path.

        Args:
            depot_path (unicode):
                The file path to stat.

            fields (list of unicode, optional):
                The fields to fetch.

        Returns:
            dict:
            The file stat info.
        """
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
        """Run p4 info and return the results.

        Returns:
            dict:
                The parsed output from :command:`p4 info`.
        """
        lines = self.run_p4([b'info'], ignore_errors=True, split_lines=True)
        return self._parse_keyval_lines(lines)

    def opened(self, changenum):
        """Return the list of opened files in the given changeset.

        Args:
            changenum (int):
                The number of the changeset.

        Returns:
            list:
            A list of the opened files in the given changeset.
        """
        return self.run_p4([b'opened', b'-c', str(changenum)], marshalled=True)

    def print_file(self, depot_path, out_file=None):
        """Print the contents of the given file.

        Args:
            depot_path (unicode):
                A Perforce path, including filename and revision.

            out_files (unicode, optional):
                A filename to write to. If not specified, the data will be
                returned.

        Returns:
            unicode:
            The output of the print operation.
        """
        cmd = [
         b'print']
        if out_file:
            cmd += [b'-o', out_file]
        cmd += [b'-q', depot_path]
        return self.run_p4(cmd)

    def where(self, depot_path):
        """Return the local path for a depot path.

        Args:
            depot_path (unicode):
                A Perforce path to a file in the depot.

        Returns:
            list:
            A marshalled representation of the data showing where the file
            exists in the local client.
        """
        return self.run_p4([b'where', depot_path], marshalled=True)

    def run_p4(self, p4_args, marshalled=False, ignore_errors=False, input_string=None, *args, **kwargs):
        """Invoke p4.

        In the current implementation, the arguments 'marshalled' and
        'input_string' cannot be used together, i.e. this command doesn't
        allow inputting and outputting at the same time.

        Args:
            p4_args (list):
                Additional arguments to pass to :command:`p4`.

            marshalled (bool, optional):
                Whether to return the data in marshalled format. This will
                return a more computer-readable version.

            ignore_errors (bool, optional):
                Whether to ignore return codes that typically indicate error
                conditions.

            input_string (unicode, optional):
                A string to pass to :command:`p4` on stdin.

            *args (list):
                Additional arguments to pass through to
                :py:func:`rbtools.utils.process.execute`.

            **kwargs (dict):
                Additional keyword arguments to pass through to
                :py:func:`rbtools.utils.process.execute`.

        Returns:
            object:
            If passing ``marshalled=True``, then this will be a list of
            dictionaries containing results from the command.

            If passing ``input_string``, this will always return ``None``.

            In all other cases, this will return the result of
            :py:func:`~rbtools.utils.process.execute`, depending on the
            arguments provided.

        Raises:
            rbtools.clients.errors.SCMError:
                There was an error with the call to Perforce. Details are in
                the error message.
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
        if marshalled:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            result = []
            has_error = False
            while 1:
                try:
                    decoded_data = marshal.load(p.stdout)
                except EOFError:
                    break
                else:
                    if not isinstance(decoded_data, dict):
                        logging.debug(b'Unexpected decoded data from Perforce command: %r', decoded_data)
                        raise SCMError(b'Expected a dictionary from Perforce, but got back a %s instead. Please file a bug about this.' % type(decoded_data))
                    data = {}
                    for key, value in six.iteritems(decoded_data):
                        key = force_unicode(key)
                        if isinstance(value, bytes):
                            value = force_unicode(value)
                        data[key] = value

                    result.append(data)
                    if data.get(b'code') == b'error':
                        has_error = True

            rc = p.wait()
            if not ignore_errors and (rc or has_error):
                for record in result:
                    if b'data' in record:
                        print(record[b'data'])

                raise SCMError(b'Failed to execute command: %s' % cmd)
            return result
        if input_string is not None:
            p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
            p.communicate(input_string)
            if not ignore_errors and p.returncode:
                raise SCMError(b'Failed to execute command: %s' % cmd)
            return
        result = execute(cmd, ignore_errors=ignore_errors, *args, **kwargs)
        return result

    def _parse_keyval_lines(self, lines, regex=KEYVAL_RE):
        """Parse a set of key:value lines into a dictionary.

        Args:
            lines (list of unicode):
                The set of lines to parse.

            regex (re.RegexObject, optional):
                A regular expression to use to parse each line.

        Returns:
            dict:
            The parsed key/value pairs.
        """
        keyvals = {}
        for line in lines:
            m = regex.match(line)
            if m:
                key = m.groups()[0]
                value = m.groups()[1]
                keyvals[key] = value.strip()

        return keyvals


class PerforceClient(SCMClient):
    """A client for Perforce.

    This is a wrapper around the :command:`p4` executable that fetches
    repository information and generates compatible diffs.
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
        """Initialize the client.

        Args:
            p4_class (type, optional):
                The class type to use for the wrapper.

            **kwargs (dict):
                Keyword arguments to pass through to the superclass.
        """
        super(PerforceClient, self).__init__(**kwargs)
        self.p4 = p4_class(self.options)

    def get_repository_info(self):
        """Return repository information for the current Perforce working tree.

        Returns:
            rbtools.clients.RepositoryInfo:
            The repository info structure.
        """
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
                local_path = os.path.normcase(os.path.realpath(client_root) + os.path.sep)
                if not norm_cwd.startswith(local_path):
                    return
            else:
                local_path = None
            try:
                parts = repository_path.split(b':')
                hostname = None
                if len(parts) == 3 and parts[0] == b'ssl':
                    hostname = parts[1]
                    port = parts[2]
                elif len(parts) == 2:
                    hostname, port = parts
                if not hostname:
                    raise SCMError(b'Path %s is not a valid Perforce P4PORT' % repository_path)
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
            return RepositoryInfo(path=repository_path, local_path=local_path, supports_changesets=True)

    def parse_revision_spec(self, revisions=[]):
        """Parse the given revision spec.

        Args:
            revisions (list of unicode, optional):
                A list of revisions as specified by the user. Items in the list
                do not necessarily represent a single revision, since the user
                can use SCM-native syntaxes such as ``r1..r2`` or ``r1:r2``.
                SCMTool-specific overrides of this method are expected to deal
                with such syntaxes.

        Raises:
            rbtools.clients.errors.InvalidRevisionSpecError:
                The given revisions could not be parsed.

            rbtools.clients.errors.TooManyRevisionsError:
                The specified revisions list contained too many revisions.

        Returns:
            dict:
            A dictionary with the following keys:

            ``base`` (:py:class:`unicode`):
                A revision to use as the base of the resulting diff.

            ``tip`` (:py:class:`unicode`):
                A revision to use as the tip of the resulting diff.

            These will be used to generate the diffs to upload to Review Board
            (or print). The diff for review will include the changes in (base,
            tip].

            If zero revisions are passed in, this will return the current sync
            changelist as "tip", and the upstream branch as "base". The result
            may have special internal revisions or prefixes based on whether
            the changeset is submitted, pending, or shelved.

            If a single revision is passed in, this will return the parent of
            that revision for "base" and the passed-in revision for "tip".

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
        """Return the status of a changelist.

        Args:
            changelist (int):
                The changelist to check.

        Returns:
            unicode:
            The current status of the changelist (such as "pending" or
            "submitted").
        """
        if changelist == self.REVISION_DEFAULT_CLN:
            return b'pending'
        else:
            change = self.p4.change(changelist)
            if len(change) == 1 and b'Status' in change[0]:
                return change[0][b'Status']
            return

    def scan_for_server(self, repository_info):
        """Find the Review Board server matching this repository.

        Args:
            repository_info (rbtools.clients.RepositoryInfo):
                The repository information structure.

        Returns:
            unicode:
            The Review Board server URL, if available.
        """
        server_url = super(PerforceClient, self).scan_for_server(repository_info)
        if server_url:
            return server_url
        return self.scan_for_server_counter(repository_info)

    def scan_for_server_counter(self, repository_info):
        """Find if a Review Board server has been defined in the p4 counters.

        This checks the Perforce counters to see if the Review Board server's
        URL is specified. Since Perforce only started supporting non-numeric
        counter values in server version 2008.1, we support both a normal
        counter ``reviewboard.url`` with a string value and embedding the URL
        in a counter name like
        ``reviewboard.url.http:||reviewboard.example.com``. Note that forward
        slashes aren't allowed in counter names, so pipe ('|') characters
        should be used. These should be safe because they should not be used
        unencoded in URLs.

        Args:
            repository_info (rbtools.clients.RepositoryInfo):
                The repository information structure.

        Returns:
            unicode:
            The Review Board server URL, if available.
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

    def diff(self, revisions, include_files=[], exclude_patterns=[], no_renames=False, extra_args=[]):
        """Perform a diff using the given revisions.

        This goes through the hard work of generating a diff on Perforce in
        order to take into account adds/deletes and to provide the necessary
        revision information.

        Args:
            revisions (dict):
                A dictionary of revisions, as returned by
                :py:meth:`parse_revision_spec`.

            include_files (list of unicode, optional):
                A list of files to whitelist during the diff generation.

            exclude_patterns (list of unicode, optional):
                A list of shell-style glob patterns to blacklist during diff
                generation.

            extra_args (list, unused):
                Additional arguments to be passed to the diff generation.
                Unused for git.

        Returns:
            dict:
            A dictionary containing the following keys:

            ``diff`` (:py:class:`bytes`):
                The contents of the diff to upload.

            ``changenum`` (:py:class:`unicode`):
                The number of the changeset being posted (if ``revisions``
                represents a single changeset).
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
            logging.info(b'Generating diff for shelved changeset %s', tip)
        else:
            logging.info(b'Generating diff for pending changeset %s', tip)
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
                raise SCMError(b'Unsupported action type "%s" for %s' % (
                 action, depot_file))

            if changetype_short == b'M':
                try:
                    old_file, new_file = self._extract_edit_files(depot_file, local_file, base_revision, tip, cl_is_shelved, False)
                except ValueError as e:
                    if not self.config.get(b'SUPPRESS_CLIENT_WARNINGS', False):
                        logging.warning(b'Skipping file %s: %s', depot_file, e)
                    continue

            elif changetype_short == b'A':
                base_revision = 0
                try:
                    old_file, new_file = self._extract_add_files(depot_file, local_file, tip, cl_is_shelved, cl_is_pending)
                except ValueError as e:
                    if not self.config.get(b'SUPPRESS_CLIENT_WARNINGS', False):
                        logging.warning(b'Skipping file %s: %s', depot_file, e)
                    continue

                if os.path.islink(new_file):
                    if not self.config.get(b'SUPPRESS_CLIENT_WARNINGS', False):
                        logging.warning(b'Skipping symlink %s', new_file)
                    continue
            elif changetype_short == b'D':
                try:
                    old_file, new_file = self._extract_delete_files(depot_file, base_revision)
                except ValueError as e:
                    if not self.config.get(b'SUPPRESS_CLIENT_WARNINGS', False):
                        logging.warning(b'Skipping file %s#%s: %s', depot_file, base_revision, e)
                    continue

            elif changetype_short == b'MV-a':
                continue
            elif changetype_short == b'MV':
                try:
                    old_file, new_file, new_depot_file = self._extract_move_files(depot_file, tip, base_revision, cl_is_shelved)
                except ValueError as e:
                    if not self.config.get(b'SUPPRESS_CLIENT_WARNINGS', False):
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

        Args:
            base (unicode):
                The base of the revision range.

            tip (unicode):
                The tip of the revision range.

            depot_include_files (list of unicode):
                A list of depot paths to whitelist during diff generation.

            local_include_files (list of unicode):
                A list of local filesystem paths to whitelist during diff
                generation.

            exclude_patterns (list of unicode):
                A list of shell-style glob patterns to blacklist during diff
                generation.

        Returns:
            dict:
            A dictionary with a single ``diff`` key.
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
                    if not self.config.get(b'SUPPRESS_CLIENT_WARNINGS', False):
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
                        if not self.config.get(b'SUPPRESS_CLIENT_WARNINGS', False):
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
                if not self.config.get(b'SUPPRESS_CLIENT_WARNINGS', False):
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
                    if not self.config.get(b'SUPPRESS_CLIENT_WARNINGS', False):
                        logging.warning(b'Skipping file %s: %s', depot_file, e)
                    continue

                diff_lines += self._do_diff(old_file, new_file, depot_file, 0, b'', b'A', ignore_unmodified=True)
            elif action == b'delete':
                try:
                    old_file, new_file = self._extract_delete_files(initial_depot_file, initial_rev)
                except ValueError as e:
                    if not self.config.get(b'SUPPRESS_CLIENT_WARNINGS', False):
                        logging.warning(b'Skipping file %s: %s', depot_file, e)
                    continue

                diff_lines += self._do_diff(old_file, new_file, initial_depot_file, initial_rev, depot_file, b'D', ignore_unmodified=True)
            elif action == b'edit':
                try:
                    old_file, new_file = self._extract_edit_files(depot_file, local_file, initial_rev, rev, False, True)
                except ValueError as e:
                    if not self.config.get(b'SUPPRESS_CLIENT_WARNINGS', False):
                        logging.warning(b'Skipping file %s: %s', depot_file, e)
                    continue

                diff_lines += self._do_diff(old_file, new_file, initial_depot_file, initial_rev, depot_file, b'M', ignore_unmodified=True)
            elif action == b'move':
                try:
                    old_file_a, new_file_a = self._extract_add_files(depot_file, local_file, rev, False, False)
                    old_file_b, new_file_b = self._extract_delete_files(initial_depot_file, initial_rev)
                except ValueError as e:
                    if not self.config.get(b'SUPPRESS_CLIENT_WARNINGS', False):
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
        """Compute the effects of a given change on a given file.

        Args:
            file_entry (dict):
                A dictionary containing information about the accumulated state
                of the given file. The results of this method will write the
                data back out to this dict.

            change (dict):
                A dictionary containing information about the new change to be
                applied to the given file.
        """
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
        """Extract the "old" and "new" files for an edit operation.

        Args:
            depot_file (unicode):
                The depot path of the file.

            local_file (unicode):
                The local filesystem path of the file.

            rev_a (unicode):
                The original revision of the file.

            rev_b (unicode):
                The new revision of the file.

            cl_is_shelved (bool):
                Whether the containing changeset is shelved.

            cl_is_submitted (bool):
                Whether the containing changeset is submitted.

        Returns:
            tuple:
            A 2-tuple containing the filenames of the old version and new
            version.

        Raises:
            ValueError:
                The file extraction failed.
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
        """Extract the "old" and "new" files for an add operation.

        Args:
            depot_file (unicode):
                The depot path of the file.

            local_file (unicode):
                The local filesystem path of the file.

            revision (unicode):
                The new revision of the file.

            cl_is_shelved (bool):
                Whether the containing changeset is shelved.

            cl_is_pending (bool):
                Whether the containing changeset is pending.

        Returns:
            tuple:
            A 2-tuple containing the filenames of the old version and new
            version. Because this is an add operation, the old filename will
            contain an empty file.

        Raises:
            ValueError:
                The file extraction failed.
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
        """Extract the "old" and "new" files for a delete operation.

        Returns a tuple of (old filename, new filename). This can raise a
        ValueError if extraction fails.

        Args:
            depot_file (unicode):
                The depot path of the file.

            revision (unicode):
                The old revision of the file.

        Returns:
            tuple:
            A 2-tuple containing the filenames of the old version and new
            version. Because this is a delete operation, the new filename will
            contain an empty file.

        Raises:
            ValueError:
                The file extraction failed.
        """
        old_filename = make_tempfile()
        self._write_file(b'%s#%s' % (depot_file, revision), old_filename)
        new_filename = make_tempfile()
        return (
         old_filename, new_filename)

    def _extract_move_files(self, old_depot_file, tip, base_revision, cl_is_shelved):
        """Extract the "old" and "new" files for a move operation.

        Returns a tuple of (old filename, new filename, new depot path). This
        can raise a ValueError if extraction fails.

        Args:
            old_depot_file (unicode):
                The depot path of the old version of the file.

            tip (unicode):
                The new revision of the file.

            base_revision (unicode):
                The old revision of the file.

            cl_is_shelved (bool):
                Whether the containing changeset is shelved.

        Returns:
            tuple:
            A 2-tuple containing the filenames of the old version and new
            version.

        Raises:
            ValueError:
                The file extraction failed.
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
        """Process a path-style diff.

        This allows people to post individual files in various ways.

        Args:
            args (list of unicode):
                A list of paths to add. The path styles supported are:

                ``//path/to/file``:
                    Upload file as a "new" file.

                ``//path/to/dir/...``:
                    Upload all files as "new" files.

                ``//path/to/file[@#]rev``:
                    Upload file from that rev as a "new" file.

                ``//path/to/file[@#]rev,[@#]rev``:
                    Upload a diff between revs.

                ``//path/to/dir/...[@#]rev,[@#]rev``:
                    Upload a diff of all files between revs in that directory.

            exclude_patterns (list of unicode):
                A list of shell-style glob patterns to blacklist during diff
                generation.

        Returns:
            dict:
            A dictionary containing a ``diff`` key.
        """
        r_revision_range = re.compile(b'^(?P<path>//[^@#]+)' + b'(?P<revision1>[#@][^,]+)?' + b'(?P<revision2>,[#@][^,]+)?$')
        empty_filename = make_tempfile()
        tmp_diff_from_filename = make_tempfile()
        tmp_diff_to_filename = make_tempfile()
        diff_lines = []
        for path in args:
            m = r_revision_range.match(path)
            if not m:
                raise SCMError(b'Path %s does not match a valid Perforce path.' % path)
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
        """Create a diff of a single file.

        Args:
            old_file (unicode):
                The absolute path of the "old" file.

            new_file (unicode):
                The absolute path of the "new" file.

            depot_file (unicode):
                The depot path in Perforce for this file.

            base_revision (int):
                The base Perforce revision number of the old file.

            new_depot_file (unicode):
                The depot path in Perforce for the new location of this ifle.
                Only used if the file was moved.

            changetype_short (unicode):
                The change type provided by Perforce.

            ignore_unmodified (bool, optional):
                Whether to return an empty list if the file was not changed.

        Returns:
            list of bytes:
            The diff, split into lines.
        """
        if hasattr(os, b'uname') and os.uname()[0] == b'SunOS':
            diff_cmd = [
             b'gdiff', b'-urNp', old_file, new_file]
        else:
            diff_cmd = [
             b'diff', b'-urNp', old_file, new_file]
        dl = execute(diff_cmd, extra_ignore_errors=(1, 2), log_output_on_error=False, results_unicode=False)
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
         old_file.encode(b'utf-8'),
         new_file.encode(b'utf-8'))):
            dl = [
             b'Binary files %s and %s differ\n' % (
              old_file.encode(b'utf-8'),
              new_file.encode(b'utf-8'))]
        is_binary = dl != [] and dl[0].startswith(b'Binary files ')
        if dl == [] or is_binary:
            is_empty_and_changed = self.supports_empty_files() and changetype_short in ('A',
                                                                                        'D')
            if dl == [] and (is_move or is_empty_and_changed) or is_binary:
                line = b'==== %s#%d ==%s== %s ====\n' % (
                 depot_file.encode(b'utf-8'),
                 base_revision,
                 changetype_short.encode(b'utf-8'),
                 new_local_path.encode(b'utf-8'))
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
                    raise SCMError(b'Unable to parse diff header: %s' % dl[1])
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
            dl[0] = b'--- %s\t%s#%d\n' % (
             local_path.encode(b'utf-8'),
             depot_file.encode(b'utf-8'),
             base_revision)
            dl[1] = b'+++ %s\t%s\n' % (
             new_local_path.encode(b'utf-8'),
             timestamp.encode(b'utf-8'))
            if is_move:
                dl.insert(0, b'Moved to: %s\n' % new_depot_file.encode(b'utf-8'))
                dl.insert(0, b'Moved from: %s\n' % depot_file.encode(b'utf-8'))
            if not dl[(-1)].endswith(b'\n'):
                dl.append(b'\n')
        else:
            raise SCMError(b'No valid diffs: %s' % dl[0].decode(b'utf-8'))
        return dl

    def _write_file(self, depot_path, tmpfile):
        """Grab a file from Perforce and writes it to a temp file.

        Args:
            depot_path (unicode):
                The depot path (including revision) of the file to write.

            tmpfile (unicode):
                The name of a temporary file to write to.
        """
        logging.debug(b'Writing "%s" to "%s"', depot_path, tmpfile)
        self.p4.print_file(depot_path, out_file=tmpfile)
        if os.path.islink(tmpfile):
            raise ValueError(b'"%s" is a symlink' % depot_path)
        else:
            os.chmod(tmpfile, stat.S_IREAD | stat.S_IWRITE)

    def _depot_to_local(self, depot_path):
        """Convert a depot path to a local path.

        Given a path in the depot return the path on the local filesystem to
        the same file.  If there are multiple results, take only the last
        result from the where command.

        Args:
            depot_path (unicode):
                The path of a file within the Perforce depot.

        Returns:
            unicode:
            The location of that same file within the local client, if
            available.
        """
        where_output = self.p4.where(depot_path)
        try:
            return where_output[(-1)][b'path']
        except KeyError:
            return where_output[(-1)][b'data'].split(b' ')[2].strip()

    def get_raw_commit_message(self, revisions):
        """Extract the commit message based on the provided revision range.

        Since local changelists in Perforce are not ordered with respect to
        one another, this implementation looks at only the tip revision.

        Args:
            revisions (dict):
                A dictionary containing ``base`` and ``tip`` keys.

        Returns:
            unicode:
            The commit messages of all commits between (base, tip].
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
                return change[0][b'Description']
            return b''

    def apply_patch_for_empty_files(self, patch, p_num, revert=False):
        """Return whether any empty files in the patch are applied.

        Args:
            patch (bytes):
                The contents of the patch.

            p_num (unicode):
                The prefix level of the diff.

            revert (bool, optional):
                Whether the patch should be reverted rather than applied.

        Returns:
            ``True`` if there are empty files in the patch. ``False`` if there
            were no empty files, or if an error occurred while applying the
            patch.
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
        """Return whether the Review Board server supports moved files.

        Returns:
            bool:
            ``True`` if the Review Board server can support showing moves.
        """
        return self.capabilities and self.capabilities.has_capability(b'scmtools', b'perforce', b'moved_files')

    def _supports_empty_files(self):
        """Return whether the Review Board server supports empty files.

        Returns:
            bool:
            ``True`` if the Review Board server can support showing empty
            files.
        """
        return self.capabilities and self.capabilities.has_capability(b'scmtools', b'perforce', b'empty_files')

    def _should_exclude_file(self, local_file, depot_file, exclude_patterns):
        """Determine if a file should be excluded from a diff.

        Check if the file identified by (local_file, depot_file) should be
        excluded from the diff. If a pattern beings with '//', then it will be
        matched against the depot_file. Otherwise, it will be matched against
        the local file.

        Args:
            local_file (unicode):
                The local filename of the file.

            depot_file (unicode):
                The Perforce path of the file.

            exclude_patterns (list of unicode):
                A list of shell-style glob patterns to blacklist during diff
                generation. This is expected to have already been normalized.

        Returns:
            bool:
            ``True`` if the given file should be excluded.
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

        Args:
            patterns (list of unicode):
                A list of shell-style glob patterns to blacklist during diff
                generation.

        Returns:
            list of unicode:
            The normalized patterns.
        """
        cwd = os.getcwd()
        base_dir = self.p4.info().get(b'Client root')

        def normalize(p):
            if p.startswith(b'//'):
                return p
            else:
                if p.startswith(os.path.sep):
                    assert base_dir is not None
                    p = os.path.join(base_dir, p[1:])
                else:
                    p = os.path.join(cwd, p)
                return os.path.normpath(p)

        return [ normalize(pattern) for pattern in patterns ]

    def _replace_description_in_changelist_spec(self, old_spec, new_description):
        """Replace the description in the given changelist spec.

        Args:
            old_spec (unicode):
                The p4 changelist spec string (the raw output from p4 change).

            new_description (unicode):
                The new description text to use.

        Returns:
            unicode:
            The new changelist spec.
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

        Since local changelists on Perforce have no ordering with respect to
        each other, the revisions argument is mandatory.

        Args:
            message (unicode):
                The commit message to use when amending the commit.

            revisions (dict):
                A dictionary of revisions, as returned by
                :py:meth:`parse_revision_spec`.

        Raises:
            rbtools.clients.errors.AmendError:
                The given changelist could not be amended.
        """
        changelist_id = revisions[b'tip']
        logging.debug(b'Preparing to amend change %s', changelist_id)
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