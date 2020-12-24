# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/scmtools/perforce.py
# Compiled at: 2020-02-11 04:03:56
"""Repository support for Perforce."""
from __future__ import unicode_literals
import logging, os, random, re, shutil, signal, socket, stat, subprocess, tempfile, time
from contextlib import contextmanager
from django.conf import settings
from django.utils import six
from django.utils.encoding import force_str
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from djblets.util.filesystem import is_exe_in_path
from reviewboard.diffviewer.parser import DiffParser
from reviewboard.scmtools.certs import Certificate
from reviewboard.scmtools.core import SCMTool, ChangeSet, HEAD, PRE_CREATION
from reviewboard.scmtools.errors import SCMError, EmptyChangeSetError, AuthenticationError, InvalidRevisionFormatError, RepositoryNotFoundError, UnverifiedCertificateError

class STunnelProxy(object):
    """Secure Perforce communication proxy using stunnel.

    This establishes a secure communication channel to a Perforce server
    using `stunnel <https://www.stunnel.org/index.html>`_. This allows a
    non-SSL-enabled Perforce server to be used across a public network
    without risk of data leaks.

    This proxy supports stunnel versions 3 and 4.
    """

    def __init__(self, target):
        """Initialize the proxy.

        Args:
            target (unicode):
                The target server to proxy to.
        """
        if not is_exe_in_path(b'stunnel'):
            raise OSError(b'stunnel was not found in the exec path')
        self.target = target
        self.pid = None
        return

    @cached_property
    def stunnel_use_config(self):
        """Whether stunnel uses a config-based model.

        stunnel 4+ switched to a config-based model, instead of passing
        arguments on the command line. This property returns whether that
        mode should be used.
        """
        try:
            subprocess.check_call([b'stunnel', b'-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError:
            return False

    def start_server(self, certfile):
        """Start stunnel as a server for clients to connect to.

        Args:
            certfile (unicode):
                The SSL certificate to use for the connection.
        """
        self._start(server=True, certfile=certfile)

    def start_client(self):
        """Start stunnel as a client connecting to a server."""
        self._start(server=False)

    def _start(self, server, certfile=None):
        """Start stunnel as a client or server.

        This will determine the version of stunnel being used and invoke it
        with the necessary configuration to run as either a client or a
        server for the tunnel.

        Args:
            server (bool):
                Whether to run as the server end of the tunnel.

            certfile (unicode):
                The SSL certificate to use for the connection.
        """
        self.port = self._find_port()
        tempdir = tempfile.mkdtemp()
        pid_filename = os.path.join(tempdir, b'stunnel.pid')
        if self.stunnel_use_config:
            conf_filename = os.path.join(tempdir, b'stunnel.conf')
            with open(conf_filename, b'w') as (fp):
                fp.write(b'pid = %s\n' % pid_filename)
                if server:
                    fp.write(b'[p4d]\n')
                    if certfile:
                        fp.write(b'cert = %s\n' % certfile)
                    fp.write(b'accept = %s\n' % self.port)
                    fp.write(b'connect = %s\n' % self.target)
                else:
                    fp.write(b'[p4]\n')
                    fp.write(b'client = yes\n')
                    fp.write(b'accept = 127.0.0.1:%s\n' % self.port)
                    fp.write(b'connect = %s\n' % self.target)
            args = [
             conf_filename]
        else:
            args = [
             b'-P', pid_filename,
             b'-d', b'127.0.0.1:%d' % self.port,
             b'-r', self.target]
            if server:
                args += [b'-p', certfile]
            else:
                args.append(b'-c')
            try:
                subprocess.check_call([b'stunnel'] + args)
            except subprocess.CalledProcessError:
                if self.stunnel_use_config:
                    with open(conf_filename, b'r') as (fp):
                        logging.error(b'Unable to create an stunnel using config:\n%s\n' % fp.read())
                else:
                    logging.error(b'Unable to create an stunnel with args: %s\n' % (b' ').join(args))
            else:
                time.sleep(0.1)
                try:
                    with open(pid_filename) as (f):
                        self.pid = int(f.read())
                        f.close()
                except IOError as e:
                    logging.exception(b'Unable to open stunnel PID file %s: %s\n' % (
                     pid_filename, e))

        shutil.rmtree(tempdir)

    def shutdown(self):
        """Shut down the tunnel."""
        if self.pid:
            os.kill(self.pid, signal.SIGTERM)
            self.pid = None
        return

    def _find_port(self):
        """Find an available port for the tunnel.

        This will attempt to find an unused port in the range of 30000 and
        60000 for the connection. It will continue trying until it finds a
        port.

        Returns:
            int:
            The unused port number.
        """
        while True:
            port = random.randint(30000, 60000)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.bind((b'127.0.0.1', port))
                s.listen(1)
                return port
            finally:
                try:
                    s.close()
                except:
                    pass


class PerforceClient(object):
    """Client for talking to a Perforce server.

    This manages Perforce connections to the server, and provides a set of
    operations needed by :py:class:`PerforceTool`.
    """
    TICKET_RENEWAL_SECS = 3600

    def __init__(self, path, username, password, encoding=b'', host=None, client_name=None, local_site_name=None, use_ticket_auth=False):
        """Initialize the client.

        Args:
            path (unicode):
                The path to the repository (equivalent to :envvar:`P4PORT`).

            username (unicode):
                The username for the connection.

            password (unicode):
                The password for the connection.

            encoding (unicode, optional):
                The encoding to use for the connection.

            host (unicode, optional):
                The client's host name to use for the connection (equivalent
                to :envvar:`P4HOST`).

            client_name (unicode, optional):
                The name of the Perforce client (equivalent to
                :envvar:`P4CLIENT`).

            local_site_name (unicode, optional):
                The name of the local site used for the repository.

            use_ticket_auth (bool, optional):
                Whether to use ticket-based authentication. By default, this
                is not used.
        """
        if path.startswith(b'stunnel:'):
            path = path[8:]
            self.use_stunnel = True
        else:
            self.use_stunnel = False
        self.p4port = path
        self.username = username
        self.password = password or b''
        self.encoding = encoding
        self.p4host = host
        self.client_name = client_name
        self.local_site_name = local_site_name
        self.use_ticket_auth = use_ticket_auth
        import P4
        self.p4 = P4.P4()
        if self.use_stunnel and not is_exe_in_path(b'stunnel'):
            raise AttributeError(b'stunnel proxy was requested, but stunnel binary is not in the exec path.')

    def get_ticket_status(self):
        """Return the status of the current login ticket.

        Returns:
            dict:
            A dictionary containing the following keys:

            ``user`` (:py:class:`unicode`):
                The user owning the ticket.

            ``expiration_secs`` (:py:class:`int`):
                The number of seconds until the ticket expires.
        """
        from P4 import P4Exception
        try:
            status = self.p4.run_login(b'-s')[0]
        except (IndexError, P4Exception):
            return

        return {b'user': status[b'User'], 
           b'expiration_secs': int(status[b'TicketExpiration'])}

    def check_refresh_ticket(self):
        """Refreshes a ticket or re-authenticates if needed.

        If the ticket has expired, is close to expiring, or the username has
        changed, a login will be performed.
        """
        ticket_status = self.get_ticket_status()
        if not ticket_status or ticket_status[b'user'] != self.username:
            logging.info(b'Perforce ticket for host "%s" (user "%s") does not exist or has expired. Refreshing...', self.p4port, self.username)
        elif ticket_status[b'expiration_secs'] < self.TICKET_RENEWAL_SECS:
            logging.info(b'Perforce ticket for host "%s" (user "%s") will soon expire. Refreshing...', self.p4port, self.username)
        else:
            return
        self.login()

    def login(self):
        """Log into Perforce.

        If there's an existing ticket, this will extend the ticket instead
        of creating a new one.
        """
        logging.info(b'Logging into Perforce host "%s" (user "%s")', self.p4port, self.username)
        self.p4.password = force_str(self.password)
        self.p4.run_login()

    @contextmanager
    def connect(self):
        """Connect to the Perforce server.

        This is a context manager used to set up, open, and then close a
        connection to the Perforce server. Generally, :py:meth:`run_worker`
        should be used instead, as this will convert certain P4 exceptions to
        Review Board exceptions.

        Context:
            The context for the connection. Once the context ends, the
            connection will close.

            No variables are passed to the context.

        Example:
            .. code-block:: python

                with client.connect():
                    ...
        """
        self.p4.user = force_str(self.username)
        if self.encoding:
            self.p4.charset = force_str(self.encoding)
        self.p4.exception_level = 1
        if self.use_stunnel:
            proxy = STunnelProxy(self.p4port)
            proxy.start_client()
            p4_port = b'127.0.0.1:%d' % proxy.port
        else:
            proxy = None
            p4_port = self.p4port
        self.p4.port = force_str(p4_port)
        if self.p4host:
            self.p4.host = force_str(self.p4host)
        if self.client_name:
            self.p4.client = force_str(self.client_name)
        if self.use_ticket_auth:
            tickets_dir = os.path.join(settings.SITE_DATA_DIR, b'p4')
            if self.local_site_name:
                tickets_dir = os.path.join(tickets_dir, self.local_site_name)
            if not os.path.exists(tickets_dir):
                try:
                    os.makedirs(tickets_dir, 448)
                except Exception as e:
                    logging.warning(b'Unable to create Perforce tickets directory %s: %s', tickets_dir, e)
                    tickets_dir = None

            if tickets_dir:
                self.p4.ticket_file = force_str(os.path.join(tickets_dir, b'p4tickets'))
        else:
            self.p4.password = force_str(self.password)
        try:
            with self.p4.connect():
                if self.use_ticket_auth:
                    self.check_refresh_ticket()
                yield
        finally:
            if proxy:
                try:
                    proxy.shutdown()
                except:
                    pass

        return

    @contextmanager
    def run_worker(self):
        """Run a Perforce command from within a Perforce connection context.

        This will set up a Perforce connection for an operation, disconnecting
        when the context is finished, and raising a suitable exception if
        anything goes wrong.

        Context:
            The context for the connection. Once the context ends, the
            connection will close.

            No variables are passed to the context.

        Raises:
            reviewboard.scmtools.errors.AuthenticationError:
                There was an error authenticating with Perforce. Credentials
                may be incorrect. The exception message will have more details.

            reviewboard.scmtools.errors.RepositoryNotFoundError:
                The repository this was attempting to use could not be found.

            reviewboard.scmtools.errors.SCMError:
                There was a general error with talking to the repository or
                executing a command. The exception message will have more
                details.

            reviewboard.scmtools.errors.UnverifiedCertificateError:
                The SSL certificate for the Perforce server could not be
                verified. It may be self-signed. The certificate information
                will be available in the exception.

        Example:
            .. code-block:: python

                with client.run_worker():
                    ...
        """
        from P4 import P4Exception
        try:
            with self.connect():
                yield
        except P4Exception as e:
            error = six.text_type(e)
            if b'Perforce password' in error or b'Password must be set' in error:
                raise AuthenticationError(msg=error)
            elif b'SSL library must be at least version' in error:
                raise SCMError(_(b'The specified Perforce port includes ssl:, but the p4python library was built without SSL support or the system library path is incorrect.'))
            elif b'check $P4PORT' in error or error.startswith(b'[P4.connect()] TCP connect to') and b'failed.' in error:
                raise RepositoryNotFoundError
            elif b"To allow connection use the 'p4 trust' command" in error:
                fingerprint = error.split(b'\\n')[3]
                raise UnverifiedCertificateError(Certificate(fingerprint=fingerprint))
            else:
                raise SCMError(error)

    def get_changeset(self, changeset_id):
        """Return information about a server-side changeset.

        Args:
            changeset_id (int):
                The Perforce changeset ID.

        Returns:
            dict:
            Information about the changeset.
        """
        changeset_id = six.text_type(changeset_id)
        with self.run_worker():
            try:
                change = self.p4.run_change(b'-o', b'-O', changeset_id)
                changeset_id = change[0][b'Change']
            except Exception as e:
                logging.warning(b'Failed to get updated changeset information for CLN %s (%s): %s', changeset_id, self.p4port, e, exc_info=True)

            return self.p4.run_describe(b'-s', changeset_id)

    def get_info(self):
        """Return information on a Perforce server connection.

        Returns:
            list of dict:
            A list of connection detail dictionaries.
        """
        with self.run_worker():
            return self.p4.run_info()

    def get_file(self, path, revision):
        """Return the contents of a file at a specified revision.

        Args:
            path (unicode):
                The Perforce depot path, without a revision.

            revision (unicode):
                The revision for the path.

        Returns:
            bytes:
            The contents of the file.
        """
        if revision == PRE_CREATION:
            return b''
        if revision == HEAD:
            depot_path = path
        else:
            depot_path = b'%s#%s' % (path, revision)
        with self.run_worker():
            fd, filename = tempfile.mkstemp(prefix=b'reviewboard.')
            try:
                os.close(fd)
                self.p4.run_print(b'-q', b'-o', filename, depot_path)
                if os.path.islink(filename):
                    return b''
                os.chmod(filename, stat.S_IREAD | stat.S_IWRITE)
                with open(filename, b'rb') as (f):
                    return f.read()
            finally:
                os.unlink(filename)

        return b''

    def get_file_stat(self, path, revision):
        """Return status information about a file in the repository.

        This is equivalent to :command:`p4 fstat`.

        Args:
            path (unicode):
                The depot path for the file.

            revision (reviewboard.scmtools.core.Revision):
                The revision number of the file.

        Returns:
            dict:
            The status information, or ``None`` if there was none for the
            given file and revision.
        """
        if revision == PRE_CREATION:
            return
        else:
            if revision == HEAD:
                depot_path = path
            else:
                depot_path = b'%s#%s' % (path, revision)
            with self.run_worker():
                res = self.p4.run_fstat(depot_path)
            if res:
                return res[(-1)]
            return


class PerforceTool(SCMTool):
    """Repository support for Perforce.

    Perforce is a centralized, enterprise-ready source code management
    service that's installed within a network. It differs from many types
    of repositories in that changes (commits) can be created before files
    are even modified (set to a "pending" state) and are tracked by the
    server. Files are "opened" (tracked by the server) before being
    modified.

    Perforce doesn't have a very comprehensive standard diff format, so we
    make use of a custom format known by Review Board and RBTools.
    """
    scmtool_id = b'perforce'
    name = b'Perforce'
    diffs_use_absolute_paths = True
    supports_ticket_auth = True
    supports_pending_changesets = True
    field_help_text = {b'path': _(b'The Perforce port identifier (P4PORT) for the repository. If your server is set up to use SSL (2012.1+), prefix the port with "ssl:". If your server connection is secured with stunnel (2011.x or older), prefix the port with "stunnel:".')}
    dependencies = {b'modules': [
                  b'P4']}

    def __init__(self, repository):
        """Initialize the Perforce tool.

        Args:
            repository (reviewboard.scmtools.models.Repository):
                The repository owning the instance of this tool.
        """
        super(PerforceTool, self).__init__(repository)
        credentials = repository.get_credentials()
        if repository.local_site_id:
            local_site_name = repository.local_site.name
        else:
            local_site_name = None
        self.client = PerforceClient(path=repository.mirror_path or repository.path, username=credentials[b'username'], password=credentials[b'password'], encoding=repository.encoding, host=repository.extra_data.get(b'p4_host'), client_name=repository.extra_data.get(b'p4_client'), local_site_name=local_site_name, use_ticket_auth=repository.extra_data.get(b'use_ticket_auth', False))
        return

    @classmethod
    def check_repository(cls, path, username=None, password=None, p4_host=None, p4_client=None, local_site_name=None):
        """Perform checks on a repository to test its validity.

        This checks if a repository exists and can be connected to.

        A failed result is returned as an exception. The exception may contain
        extra information, such as a human-readable description of the problem.
        If the repository is valid and can be connected to, no exception will
        be thrown.

        Args:
            path (unicode):
                The Perforce repository path (equivalent to :envvar:`P4PORT`).

            username (unicode):
                The username used to authenticate.

            password (unicode):
                The password used to authenticate.

            p4_host (unicode):
                The optional Perforce host name (equivalent to
                :envvar:`P4HOST`).

            p4_client (unicode):
                The optional Perforce client name (equivalent to
                :envvar:`P4CLIENT`).

            local_site_name (unicode):
                The optional Local Site name.

        Raises:
            reviewboard.scmtools.errors.AuthenticationError:
                There was an error authenticating with Perforce.

            reviewboard.scmtools.errors.RepositoryNotFoundError:
                The repository at the given path could not be found.

            reviewboard.scmtools.errors.SCMError:
                There was a general error communicating with Perforce.

            reviewboard.scmtools.errors.UnverifiedCertificateError:
                The Perforce SSL certificate could not be verified.
        """
        super(PerforceTool, cls).check_repository(path, username, password, local_site_name)
        client = PerforceClient(path=path, username=username, password=password, host=p4_host, client_name=p4_client, local_site_name=local_site_name)
        client.get_info()

    def get_changeset(self, changeset_id, allow_empty=False):
        """Return information on a server-side changeset with the given ID.

        Args:
            changeset_id (unicode):
                The server-side changeset ID.

            allow_empty (bool, optional):
                Whether or not an empty changeset (one containing no modified
                files) can be returned.

                If ``True``, the changeset will be returned with whatever
                data could be provided. If ``False``, an
                :py:exc:`~reviewboard.scmtools.errors.EmptyChangeSetError`
                will be raised.

                Defaults to ``False``.

        Returns:
            reviewboard.scmtools.core.ChangeSet:
            The resulting changeset containing information on the commit
            and modified files.

        Raises:
            reviewboard.scmtools.errors.EmptyChangeSetError:
                The resulting changeset contained no file modifications (and
                ``allow_empty`` was ``False``).
        """
        changeset = self.client.get_changeset(changeset_id)
        if changeset:
            return self._parse_change_desc(changeset[0], changeset_id, allow_empty)
        else:
            return
            return

    def get_file(self, path, revision=HEAD, **kwargs):
        """Return the contents of a file in the repository.

        Args:
            path (unicode):
                THe depot path to the file in the repository.

            revision (reviewboard.scmtools.core.Revision, optional):
                The revision to fetch.

            **kwargs (dict):
                Unused keyword arguments.

        Returns:
            bytes:
            The contents of the file.

        Raises:
            reviewboard.scmtools.errors.FileNotFoundError:
                The file could not be found in the repository.
        """
        return self.client.get_file(path, revision)

    def file_exists(self, path, revision=HEAD, **kwargs):
        """Return whether a particular file exists in a repository.

        Args:
            path (unicode):
                The depot path to the file in the repository.

            revision (reviewboard.scmtools.core.Revision, optional):
                The revision to fetch.

            **kwargs (dict):
                Unused keyword arguments.

        Returns:
            bool:
            ``True`` if the file exists in the repository. ``False`` if it
            does not.
        """
        stat = self.client.get_file_stat(path, revision)
        return stat is not None and b'headRev' in stat

    def parse_diff_revision(self, file_str, revision_str, *args, **kwargs):
        """Return a parsed filename and revision as represented in a diff.

        This will separate out the filename from the revision (separated by
        a ``#``) and return the results.

        If the revision is ``1``, this will have to query the repository for
        the file's history. This is to work around behavior in older versions
        of Perforce where a revision of ``1`` would be used for newly-created
        files.

        Args:
            file_str (unicode):
                The filename as represented in the diff.

            revision_str (unicode):
                The revision as represented in the diff.

            **args (tuple):
                Unused positional arguments.

            **kwargs (dict):
                Unused keyword arguments.

        Returns:
            tuple:
            A tuple containing two items: The normalized filename string, and
            a :py:class:`~reviewboard.scmtools.core.Revision`.

        Raises:
            reviewboard.scmtools.errors.InvalidRevisionFormatError:
                The ``revision`` was in an invalid format.
        """
        filename, revision = revision_str.rsplit(b'#', 1)
        try:
            int(revision)
        except ValueError:
            raise InvalidRevisionFormatError(filename, revision)

        if revision == b'0' or revision == b'1' and not self.repository.get_file_exists(filename, revision):
            revision = PRE_CREATION
        return (filename, revision)

    def get_parser(self, data):
        """Return a diff parser for Perforce.

        Args:
            data (bytes):
                The diff contents.

        Returns:
            PerforceDiffParser:
            The diff parser used to parse the diff.
        """
        return PerforceDiffParser(data)

    @classmethod
    def accept_certificate(cls, path, username=None, password=None, local_site_name=None, certificate=None):
        """Accept the SSL certificate for the given repository path.

        This is needed for repositories that support SSL-backed
        repositories. It should mark an SSL certificate as accepted so that the
        user won't see validation errors in the future.

        The administration UI will call this after a user has seen and verified
        the SSL certificate.

        Args:
            path (unicode):
                The repository path.

            username (unicode, optional):
                The username provided for the repository.

            password (unicode, optional):
                The password provided for the repository.

            local_site_name (unicode, optional):
                The name of the Local Site used for the repository, if any.

            certificate (reviewboard.scmtools.certs.Certificate):
                The certificate to accept.

        Returns:
            dict:
            Serialized information on the certificate.

        Raises:
            reviewboard.scmtools.errors.SCMError:
                There was an error accepting the certificate.
        """
        p = subprocess.Popen([
         b'p4', b'-p', path, b'trust', b'-i', certificate.fingerprint], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        errdata = p.communicate()[1]
        failure = p.poll()
        if failure:
            raise SCMError(errdata)
        return certificate.fingerprint

    def normalize_patch(self, patch, filename, revision):
        """Normalize a diff/patch file before it's applied.

        This will take patch entries for files that represent unchanged, moved
        files and return a blank diff instead. These types of patches aren't
        otherwise handled well by GNU patch.

        By default, this returns the contents as-is.

        Args:
            patch (bytes):
                The diff/patch file to normalize.

            filename (unicode):
                The name of the file being changed in the diff.

            revision (unicode):
                The revision of the file being changed in the diff.

        Returns:
            bytes:
            The resulting diff/patch file.
        """
        m = PerforceDiffParser.SPECIAL_REGEX.match(patch.strip())
        if m and m.group(3) == b'MV':
            return b''
        return patch

    def _parse_change_desc(self, changedesc, changenum, allow_empty=False):
        """Parse the contents of a change description from Perforce.

        This will attempt to grab details from the change description,
        including the changeset ID, the list of files, change message,
        and state.

        Args:
            changedesc (dict):
                The change description dictionary from Perforce.

            changenum (int):
                THe change number.

            allow_empty (bool, optional):
                Whether an empty changeset (containing no files) is allowed.

        Returns:
            reviewboard.scmtools.core.ChangeSet:
            The resulting changeset, or ``None`` if ``changedesc`` is empty.

        Raises:
            reviewboard.scmtools.errors.EmptyChangeSetError:
                The resulting changeset contained no file modifications (and
                ``allow_empty`` was ``False``).
        """
        if not changedesc:
            return None
        else:
            changeset = ChangeSet()
            try:
                changeset.changenum = int(changedesc[b'change'])
            except ValueError:
                changeset.changenum = changenum

            changeset.username = changedesc[b'user']
            try:
                changeset.description = changedesc[b'desc'].decode(b'utf-8')
            except UnicodeDecodeError:
                changeset.description = changedesc[b'desc'].decode(b'utf-8', b'replace')

            if changedesc[b'status'] == b'pending':
                changeset.pending = True
            try:
                changeset.files = changedesc[b'depotFile']
            except KeyError:
                if not allow_empty:
                    raise EmptyChangeSetError(changenum)

            split = changeset.description.find(b'\n\n')
            if split >= 0 and split < 100:
                changeset.summary = changeset.description.split(b'\n\n', 1)[0].replace(b'\n', b' ')
            else:
                changeset.summary = changeset.description.split(b'\n', 1)[0]
            return changeset


class PerforceDiffParser(DiffParser):
    """Diff parser for handling Perforce diffs.

    This accepts a custom variant on the Perforce diff format. This will
    extract information added to the diff that represents operations like
    file moves or copies, and normalizes the depot paths contained within.
    """
    SPECIAL_REGEX = re.compile(b'^==== ([^#]+)#(\\d+) ==([AMD]|MV)== (.*) ====$')

    def parse_diff_header(self, linenum, info):
        """Parse a header in the diff.

        This will look for a special header line and extract information
        from it to determine the depot paths/revisions and the file
        modification operation.

        Args:
            linenum (int):
                The current 0-based line number.

            info (dict):
                The information dictionary to populate with any information
                found.

        Returns:
            int:
            The next line number to process.
        """
        m = self.SPECIAL_REGEX.match(self.lines[linenum])
        if m:
            info.update({b'origFile': m.group(1), 
               b'origInfo': b'%s#%s' % (m.group(1), m.group(2)), 
               b'newFile': m.group(4), 
               b'newInfo': b''})
            linenum += 1
            try:
                line = self.lines[linenum]
                if line.startswith(('Binary files ', 'Files ')):
                    info[b'binary'] = True
                    linenum += 1
            except IndexError:
                pass

            change_type = m.group(3)
            if change_type == b'D':
                info[b'deleted'] = True
            elif change_type == b'MV':
                info[b'moved'] = True
            return linenum
        return super(PerforceDiffParser, self).parse_diff_header(linenum, info)

    def parse_special_header(self, linenum, info):
        """Parse a special information before the header in a diff.

        This will look for move information before the diff header and store
        it, if found.

        Args:
            linenum (int):
                The current 0-based line number.

            info (dict):
                The information dictionary to populate with any information
                found.

        Returns:
            int:
            The next line number to process.
        """
        linenum = super(PerforceDiffParser, self).parse_special_header(linenum, info)
        try:
            if self.lines[linenum].startswith(b'Moved from:') and self.lines[(linenum + 1)].startswith(b'Moved to:'):
                info[b'moved'] = True
                linenum += 2
        except IndexError:
            pass

        return linenum

    def normalize_diff_filename(self, filename):
        """Normalize filenames in diffs.

        The default behavior is to strip off leading slashes from filenames.
        For Perforce, it's important to keep these, as they're needed to
        resolve depot paths. This is a simple override function that preserves
        the filenames as-is.

        Args:
            filename (unicode):
                The filename in the diff.

        Returns:
            unicode:
            The provided filename, unchanged.
        """
        return filename