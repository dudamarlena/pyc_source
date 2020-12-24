# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\rbtools\clients\perforce.py
# Compiled at: 2012-09-04 05:45:40
import logging, marshal, os, re, socket, stat, subprocess, sys
from rbtools.clients import SCMClient, RepositoryInfo
from rbtools.utils.checks import check_gnu_diff, check_install
from rbtools.utils.filesystem import make_tempfile
from rbtools.utils.process import die, execute

class PerforceClient(SCMClient):
    """
    A wrapper around the p4 Perforce tool that fetches repository information
    and generates compatible diffs.
    """
    DATE_RE = re.compile('(\\w+)\\s+(\\w+)\\s+(\\d+)\\s+(\\d\\d:\\d\\d:\\d\\d)\\s+(\\d\\d\\d\\d)')

    def __init__(self, **kwargs):
        super(PerforceClient, self).__init__(**kwargs)

    def get_repository_info(self):
        if not check_install('p4 help'):
            return None
        else:
            data = execute(['p4', 'info'], ignore_errors=True)
            m = re.search('^Server address: (.+)$', data, re.M)
            if not m:
                return None
            repository_path = m.group(1).strip()
            try:
                (hostname, port) = repository_path.split(':')
                info = socket.gethostbyaddr(hostname)
                if info[1]:
                    servers = [
                     info[0]] + info[1]
                    repository_path = [ '%s:%s' % (server, port) for server in servers
                                      ]
                else:
                    repository_path = '%s:%s' % (info[0], port)
            except (socket.gaierror, socket.herror):
                pass

            m = re.search('^Server version: [^ ]*/([0-9]+)\\.([0-9]+)/[0-9]+ .*$', data, re.M)
            self.p4d_version = (int(m.group(1)), int(m.group(2)))
            check_gnu_diff()
            return RepositoryInfo(path=repository_path, supports_changesets=True)

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
        counters_text = execute(['p4', 'counters'])
        m = re.search('^reviewboard.url = (\\S+)', counters_text, re.M)
        if m:
            return m.group(1)
        else:
            m2 = re.search('^reviewboard.url\\.(\\S+)', counters_text, re.M)
            if m2:
                return m2.group(1).replace('|', '/')
            return

    def get_changenum(self, args):
        if len(args) == 0:
            return 'default'
        else:
            if len(args) == 1:
                if args[0] == 'default':
                    return 'default'
                try:
                    return str(int(args[0]))
                except ValueError:
                    return

            else:
                return
            return

    def diff(self, args):
        """
        Goes through the hard work of generating a diff on Perforce in order
        to take into account adds/deletes and to provide the necessary
        revision information.
        """
        if self.options.p4_client:
            os.environ['P4CLIENT'] = self.options.p4_client
        if self.options.p4_port:
            os.environ['P4PORT'] = self.options.p4_port
        if self.options.p4_passwd:
            os.environ['P4PASSWD'] = self.options.p4_passwd
        changenum = self.get_changenum(args)
        if changenum is None:
            return self._path_diff(args)
        else:
            return self._changenum_diff(changenum)
            return

    def check_options(self):
        if self.options.revision_range:
            sys.stderr.write('The --revision-range option is not supported for Perforce repositories.  Please use the Perforce range path syntax instead.\n\nSee: http://www.reviewboard.org/docs/manual/dev/users/tools/post-review/#posting-paths')
            sys.exit(1)

    def _path_diff(self, args):
        """
        Process a path-style diff.  See _changenum_diff for the alternate
        version that handles specific change numbers.

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
        r_revision_range = re.compile('^(?P<path>//[^@#]+)' + '(?P<revision1>[#@][^,]+)?' + '(?P<revision2>,[#@][^,]+)?$')
        empty_filename = make_tempfile()
        tmp_diff_from_filename = make_tempfile()
        tmp_diff_to_filename = make_tempfile()
        diff_lines = []
        for path in args:
            m = r_revision_range.match(path)
            if not m:
                die('Path %r does not match a valid Perforce path.' % (path,))
            revision1 = m.group('revision1')
            revision2 = m.group('revision2')
            first_rev_path = m.group('path')
            if revision1:
                first_rev_path += revision1
            records = self._run_p4(['files', first_rev_path])
            files = {}
            for record in records:
                if record['action'] not in ('delete', 'move/delete'):
                    if revision2:
                        files[record['depotFile']] = [
                         record, None]
                    else:
                        files[record['depotFile']] = [
                         None, record]

            if revision2:
                second_rev_path = m.group('path') + revision2[1:]
                records = self._run_p4(['files', second_rev_path])
                for record in records:
                    if record['action'] not in ('delete', 'move/delete'):
                        try:
                            m = files[record['depotFile']]
                            m[1] = record
                        except KeyError:
                            files[record['depotFile']] = [
                             None, record]

            old_file = new_file = empty_filename
            changetype_short = None
            for (depot_path, (first_record, second_record)) in files.items():
                old_file = new_file = empty_filename
                if first_record is None:
                    self._write_file(depot_path + '#' + second_record['rev'], tmp_diff_to_filename)
                    new_file = tmp_diff_to_filename
                    changetype_short = 'A'
                    base_revision = 0
                elif second_record is None:
                    self._write_file(depot_path + '#' + first_record['rev'], tmp_diff_from_filename)
                    old_file = tmp_diff_from_filename
                    changetype_short = 'D'
                    base_revision = int(first_record['rev'])
                elif first_record['rev'] == second_record['rev']:
                    continue
                else:
                    self._write_file(depot_path + '#' + first_record['rev'], tmp_diff_from_filename)
                    self._write_file(depot_path + '#' + second_record['rev'], tmp_diff_to_filename)
                    new_file = tmp_diff_to_filename
                    old_file = tmp_diff_from_filename
                    changetype_short = 'M'
                    base_revision = int(first_record['rev'])
                dl = self._do_diff(old_file, new_file, depot_path, base_revision, changetype_short, ignore_unmodified=True)
                diff_lines += dl

        os.unlink(empty_filename)
        os.unlink(tmp_diff_from_filename)
        os.unlink(tmp_diff_to_filename)
        return (('').join(diff_lines), None)

    def _run_p4(self, command):
        """Execute a perforce command using the python marshal API.

        - command: A list of strings of the command to execute.

        The return type depends on the command being run.
        """
        command = [
         'p4', '-G'] + command
        p = subprocess.Popen(command, stdout=subprocess.PIPE)
        result = []
        has_error = False
        while 1:
            try:
                data = marshal.load(p.stdout)
            except EOFError:
                break
            else:
                result.append(data)
                if data.get('code', None) == 'error':
                    has_error = True

        rc = p.wait()
        if rc or has_error:
            for record in result:
                if 'data' in record:
                    print record['data']

            die('Failed to execute command: %s\n' % (command,))
        return result

    def sanitize_changenum(self, changenum):
        """
        Return a "sanitized" change number for submission to the Review Board
        server. For default changelists, this is always None. Otherwise, use
        the changelist number for submitted changelists, or if the p4d is
        2002.2 or newer.

        This is because p4d < 2002.2 does not return enough information about
        pending changelists in 'p4 describe' for Review Board to make use of
        them (specifically, the list of files is missing). This would result
        in the diffs being rejected.
        """
        if changenum == 'default':
            return None
        else:
            v = self.p4d_version
            if v[0] < 2002 or v[0] == '2002' and v[1] < 2:
                describeCmd = [
                 'p4']
                if self.options.p4_passwd:
                    describeCmd.append('-P')
                    describeCmd.append(self.options.p4_passwd)
                describeCmd = describeCmd + ['describe', '-s', changenum]
                description = execute(describeCmd, split_lines=True)
                if '*pending*' in description[0]:
                    return None
            return changenum

    def _changenum_diff(self, changenum):
        """
        Process a diff for a particular change number.  This handles both
        pending and submitted changelists.

        See _path_diff for the alternate version that does diffs of depot
        paths.
        """
        cl_is_pending = False
        logging.info('Generating diff for changenum %s' % changenum)
        description = []
        if changenum == 'default':
            cl_is_pending = True
        else:
            describeCmd = [
             'p4']
            if self.options.p4_passwd:
                describeCmd.append('-P')
                describeCmd.append(self.options.p4_passwd)
            describeCmd = describeCmd + ['describe', '-s', changenum]
            description = execute(describeCmd, split_lines=True)
            if re.search('no such changelist', description[0]):
                die('CLN %s does not exist.' % changenum)
            if '*pending*' in description[0] or '*pending*' in description[1]:
                cl_is_pending = True
        v = self.p4d_version
        if cl_is_pending and (v[0] < 2002 or v[0] == '2002' and v[1] < 2 or changenum == 'default'):
            info = execute(['p4', 'opened', '-c', str(changenum)], split_lines=True)
            if len(info) == 1 and info[0].startswith('File(s) not opened on this client.'):
                die("Couldn't find any affected files for this change.")
            for line in info:
                data = line.split(' ')
                description.append('... %s %s' % (data[0], data[2]))

        else:
            for (line_num, line) in enumerate(description):
                if 'Affected files ...' in line:
                    break
            else:
                die("Couldn't find any affected files for this change.")

            description = description[line_num + 2:]
        diff_lines = []
        empty_filename = make_tempfile()
        tmp_diff_from_filename = make_tempfile()
        tmp_diff_to_filename = make_tempfile()
        for line in description:
            line = line.strip()
            if not line:
                continue
            m = re.search('\\.\\.\\. ([^#]+)#(\\d+) (add|edit|delete|integrate|branch|move/add|move/delete)', line)
            if not m:
                die('Unsupported line from p4 opened: %s' % line)
            depot_path = m.group(1)
            base_revision = int(m.group(2))
            if not cl_is_pending:
                base_revision -= 1
            changetype = m.group(3)
            logging.debug('Processing %s of %s' % (changetype, depot_path))
            old_file = new_file = empty_filename
            old_depot_path = new_depot_path = None
            changetype_short = None
            if changetype in ('edit', 'integrate'):
                new_revision = base_revision + 1
                old_depot_path = '%s#%s' % (depot_path, base_revision)
                self._write_file(old_depot_path, tmp_diff_from_filename)
                old_file = tmp_diff_from_filename
                if cl_is_pending:
                    new_file = self._depot_to_local(depot_path)
                else:
                    new_depot_path = '%s#%s' % (depot_path, new_revision)
                    self._write_file(new_depot_path, tmp_diff_to_filename)
                    new_file = tmp_diff_to_filename
                changetype_short = 'M'
            elif changetype in ('add', 'branch', 'move/add'):
                if cl_is_pending:
                    new_file = self._depot_to_local(depot_path)
                else:
                    new_depot_path = '%s#%s' % (depot_path, 1)
                    self._write_file(new_depot_path, tmp_diff_to_filename)
                    new_file = tmp_diff_to_filename
                changetype_short = 'A'
            elif changetype in ('delete', 'move/delete'):
                old_depot_path = '%s#%s' % (depot_path, base_revision)
                self._write_file(old_depot_path, tmp_diff_from_filename)
                old_file = tmp_diff_from_filename
                changetype_short = 'D'
            else:
                die("Unknown change type '%s' for %s" % (changetype,
                 depot_path))
            dl = self._do_diff(old_file, new_file, depot_path, base_revision, changetype_short)
            diff_lines += dl

        os.unlink(empty_filename)
        os.unlink(tmp_diff_from_filename)
        os.unlink(tmp_diff_to_filename)
        return (('').join(diff_lines), None)

    def _do_diff(self, old_file, new_file, depot_path, base_revision, changetype_short, ignore_unmodified=False):
        """
        Do the work of producing a diff for Perforce.

        old_file - The absolute path to the "old" file.
        new_file - The absolute path to the "new" file.
        depot_path - The depot path in Perforce for this file.
        base_revision - The base perforce revision number of the old file as
            an integer.
        changetype_short - The change type as a single character string.
        ignore_unmodified - If True, will return an empty list if the file
            is not changed.

        Returns a list of strings of diff lines.
        """
        if hasattr(os, 'uname') and os.uname()[0] == 'SunOS':
            diff_cmd = [
             'gdiff', '-urNp', old_file, new_file]
        else:
            diff_cmd = [
             'diff', '-urNp', old_file, new_file]
        dl = execute(diff_cmd, extra_ignore_errors=(1, 2), translate_newlines=False)
        dl = dl.replace('\r\r\n', '\r\n')
        dl = dl.splitlines(True)
        cwd = os.getcwd()
        if depot_path.startswith(cwd):
            local_path = depot_path[len(cwd) + 1:]
        else:
            local_path = depot_path
        if len(dl) == 1 and dl[0].startswith('Files %s and %s differ' % (
         old_file, new_file)):
            dl = [
             'Binary files %s and %s differ\n' % (old_file, new_file)]
        if dl == [] or dl[0].startswith('Binary files '):
            if dl == []:
                if ignore_unmodified:
                    return []
                print 'Warning: %s in your changeset is unmodified' % local_path
            dl.insert(0, '==== %s#%s ==%s== %s ====\n' % (
             depot_path, base_revision, changetype_short, local_path))
            dl.append('\n')
        elif len(dl) > 1:
            m = re.search('(\\d\\d\\d\\d-\\d\\d-\\d\\d \\d\\d:\\d\\d:\\d\\d)', dl[1])
            if m:
                timestamp = m.group(1)
            else:
                m = self.DATE_RE.search(dl[1])
                if not m:
                    die('Unable to parse diff header: %s' % dl[1])
                month_map = {'Jan': '01', 
                   'Feb': '02', 
                   'Mar': '03', 
                   'Apr': '04', 
                   'May': '05', 
                   'Jun': '06', 
                   'Jul': '07', 
                   'Aug': '08', 
                   'Sep': '09', 
                   'Oct': '10', 
                   'Nov': '11', 
                   'Dec': '12'}
                month = month_map[m.group(2)]
                day = m.group(3)
                timestamp = m.group(4)
                year = m.group(5)
                timestamp = '%s-%s-%s %s' % (year, month, day, timestamp)
            dl[0] = '--- %s\t%s#%s\n' % (local_path, depot_path, base_revision)
            dl[1] = '+++ %s\t%s\n' % (local_path, timestamp)
            if dl[(-1)][(-1)] != '\n':
                dl.append('\n')
        else:
            die('ERROR, no valid diffs: %s' % dl[0])
        return dl

    def _write_file(self, depot_path, tmpfile):
        """
        Grabs a file from Perforce and writes it to a temp file. p4 print sets
        the file readonly and that causes a later call to unlink fail. So we
        make the file read/write.
        """
        logging.debug('Writing "%s" to "%s"' % (depot_path, tmpfile))
        execute(['p4', 'print', '-o', tmpfile, '-q', depot_path])
        os.chmod(tmpfile, stat.S_IREAD | stat.S_IWRITE)

    def _depot_to_local(self, depot_path):
        """
        Given a path in the depot return the path on the local filesystem to
        the same file.  If there are multiple results, take only the last
        result from the where command.
        """
        where_output = self._run_p4(['where', depot_path])
        try:
            return where_output[(-1)]['path']
        except:
            return where_output[(-1)]['data'].split(' ')[2].strip()