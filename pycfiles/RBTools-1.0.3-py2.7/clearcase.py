# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/rbtools/clients/clearcase.py
# Compiled at: 2020-04-14 20:27:46
"""A client for ClearCase."""
from __future__ import unicode_literals
import datetime, itertools, logging, os, sys, threading
from collections import deque
import six
from pkg_resources import parse_version
from rbtools.api.errors import APIError
from rbtools.clients import SCMClient, RepositoryInfo
from rbtools.clients.errors import InvalidRevisionSpecError, SCMError
from rbtools.utils.checks import check_gnu_diff, check_install
from rbtools.utils.filesystem import make_tempfile
from rbtools.utils.process import execute
if sys.platform.startswith((b'cygwin', b'win')):
    import ntpath as cpath
else:
    import os.path as cpath

class _get_elements_from_label_thread(threading.Thread):

    def __init__(self, threadID, dir_name, label, elements):
        self.threadID = threadID
        self.dir_name = dir_name
        self.elements = elements
        try:
            label, vobstag = label.rsplit(b'@', 1)
        except Exception:
            pass

        self.label = label
        if sys.platform.startswith(b'win'):
            self.cc_xpn = b'%CLEARCASE_XPN%'
        else:
            self.cc_xpn = b'$CLEARCASE_XPN'
        threading.Thread.__init__(self)

    def run(self):
        """Run the thread.

        This will store a dictionary of ClearCase elements (oid + version)
        belonging to a label and identified by path.
        """
        output = execute([
         b'cleartool', b'find', self.dir_name, b'-version',
         b'lbtype(%s)' % self.label, b'-exec',
         b'cleartool describe -fmt "%On\\t%En\\t%Vn\\n" ' + self.cc_xpn], extra_ignore_errors=(1, ), with_errors=False)
        for line in output.split(b'\n'):
            if not line:
                continue
            oid, path, version = line.split(b'\t', 2)
            self.elements[path] = {b'oid': oid, 
               b'version': version}


class ClearCaseClient(SCMClient):
    """A client for ClearCase.

    This is a wrapper around the clearcase tool that fetches repository
    information and generates compatible diffs. This client assumes that cygwin
    is installed on Windows.
    """
    name = b'ClearCase'
    viewtype = None
    supports_patch_revert = True
    REVISION_ACTIVITY_BASE = b'--rbtools-activity-base'
    REVISION_ACTIVITY_PREFIX = b'activity:'
    REVISION_BRANCH_BASE = b'--rbtools-branch-base'
    REVISION_BRANCH_PREFIX = b'brtype:'
    REVISION_CHECKEDOUT_BASE = b'--rbtools-checkedout-base'
    REVISION_CHECKEDOUT_CHANGESET = b'--rbtools-checkedout-changeset'
    REVISION_FILES = b'--rbtools-files'
    REVISION_LABEL_BASE = b'--rbtools-label-base'
    REVISION_LABEL_PREFIX = b'lbtype:'

    def get_repository_info(self):
        """Return information on the ClearCase repository.

        This will first check if the cleartool command is installed and in the
        path, and that the current working directory is inside of the view.

        Returns:
            ClearCaseRepositoryInfo:
            The repository info structure.
        """
        if not check_install([b'cleartool', b'help']):
            logging.debug(b'Unable to execute "cleartool help": skipping ClearCase')
            return None
        else:
            viewname = execute([b'cleartool', b'pwv', b'-short']).strip()
            if viewname.startswith(b'** NONE'):
                return None
            check_gnu_diff()
            property_lines = execute([
             b'cleartool', b'lsview', b'-full', b'-properties', b'-cview'], split_lines=True)
            for line in property_lines:
                properties = line.split(b' ')
                if properties[0] == b'Properties:':
                    if b'webview' in properties:
                        raise SCMError(b'Webviews are not supported. You can use rbt commands only in dynamic or snapshot views.')
                    if b'dynamic' in properties:
                        self.viewtype = b'dynamic'
                    else:
                        self.viewtype = b'snapshot'
                    break

            vobstag = execute([b'cleartool', b'describe', b'-short', b'vob:.'], ignore_errors=True).strip()
            if b'Error: ' in vobstag:
                raise SCMError(b'Failed to generate diff run rbt inside vob.')
            root_path = execute([b'cleartool', b'pwv', b'-root'], ignore_errors=True).strip()
            if b'Error: ' in root_path:
                raise SCMError(b'Failed to generate diff run rbt inside view.')
            cwd = os.getcwd()
            base_path = cwd[:len(root_path) + len(vobstag)]
            return ClearCaseRepositoryInfo(path=base_path, base_path=base_path, vobstag=vobstag)

    def _determine_branch_path(self, version_path):
        """Determine the branch path of a version path.

        Args:
            version_path (unicode):
                A version path consisting of a branch path and a version
                number.

        Returns:
            unicode:
            The branch path.
        """
        branch_path, number = cpath.split(version_path)
        return branch_path

    def _list_checkedout(self, path):
        """List all checked out elements in current view below path.

        Run the :command:`cleartool` command twice because ``recurse`` finds
        checked out elements under path except path, and the directory is
        detected only if the path directory is checked out.

        Args:
            path (unicode):
                The path of the directory to find checked-out files in.

        Returns:
            list of unicode:
            A list of the checked out files.
        """
        checkedout_elements = []
        for option in [b'-recurse', b'-directory']:
            output = execute([b'cleartool', b'lscheckout', option, b'-cview',
             b'-fmt', b'%En@@%Vn\\n', path], split_lines=True, extra_ignore_errors=(1, ), with_errors=False)
            if output:
                checkedout_elements.extend(output)
                logging.debug(output)

        return checkedout_elements

    def _is_a_label(self, label, vobstag=None):
        """Return whether a given label is a valid ClearCase lbtype.

        Args:
            label (unicode):
                The label to check.

            vobstag (unicode, optional):
                An optional vobstag to limit the label to.

        Raises:
            Exception:
                The vobstag did not match.

        Returns:
            bool:
            Whether the label was valid.
        """
        label_vobstag = None
        try:
            label, label_vobstag = label.rsplit(b'@', 1)
        except Exception:
            pass

        if not label.startswith(self.REVISION_LABEL_PREFIX):
            label = b'%s%s' % (self.REVISION_LABEL_PREFIX, label)
        if vobstag and label_vobstag and label_vobstag != vobstag:
            raise Exception(b'label vobstag %s does not match expected vobstag %s' % (
             label_vobstag, vobstag))
        output = execute([b'cleartool', b'describe', b'-short', label], extra_ignore_errors=(1, ), with_errors=False)
        return bool(output)

    def _get_tmp_label(self):
        """Return a string that will be used to set a ClearCase label.

        Returns:
            unicode:
            A string suitable for using as a temporary label.
        """
        now = datetime.datetime.now()
        temporary_label = b'Current_%d_%d_%d_%d_%d_%d_%d' % (
         now.year, now.month, now.day, now.hour, now.minute, now.second,
         now.microsecond)
        return temporary_label

    def _set_label(self, label, path):
        """Set a ClearCase label on elements seen under path.

        Args:
            label (unicode):
                The label to set.

            path (unicode):
                The filesystem path to set the label on.
        """
        checkedout_elements = self._list_checkedout(path)
        if checkedout_elements:
            raise Exception(b'ClearCase backend cannot set label when some elements are checked out:\n%s' % (b'').join(checkedout_elements))
        execute([b'cleartool', b'mklbtype', b'-c', b'label created for rbtools',
         label], with_errors=True)
        recursive_option = b''
        if cpath.isdir(path):
            recursive_option = b'-recurse'
        execute([b'cleartool', b'mklabel', b'-nc', recursive_option, label, path], extra_ignore_errors=(1, ), with_errors=False)

    def _remove_label(self, label):
        """Remove a ClearCase label from vob database.

        It will remove all references of this label on elements.

        Args:
            label (unicode):
                The ClearCase label to remove.
        """
        if not label.startswith(self.REVISION_LABEL_PREFIX):
            label = b'%s%s' % (self.REVISION_LABEL_PREFIX, label)
        execute([b'cleartool', b'rmtype', b'-rmall', b'-force', label], with_errors=True)

    def _determine_version(self, version_path):
        """Determine the numeric version of a version path.

        This will split a version path, pulling out the branch and version. A
        special version value of ``CHECKEDOUT`` represents the latest version
        of a file, similar to ``HEAD`` in many other types of repositories.

        Args:
            version_path (unicode):
                A version path consisting of a branch path and a version
                number.

        Returns:
            int:
            The numeric portion of the version path.
        """
        branch, number = cpath.split(version_path)
        if number == b'CHECKEDOUT':
            return sys.maxint
        return int(number)

    def _construct_extended_path(self, path, version):
        """Construct an extended path from a file path and version identifier.

        This will construct a path in the form of ``path@version``. If the
        version is the special value ``CHECKEDOUT``, only the path will be
        returned.

        Args:
            path (unicode):
                A file path.

            version (unicode):
                The version of the file.

        Returns:
            unicode:
            The combined extended path.
        """
        if not version or version.endswith(b'CHECKEDOUT'):
            return path
        return b'%s@@%s' % (path, version)

    def _construct_revision(self, branch_path, version_number):
        """Construct a revisioned path from a branch path and version ID.

        Args:
            branch_path (unicode):
                The path of a branch.

            version_number (unicode):
                The version number of the revision.

        Returns:
            unicode:
            The combined revision.
        """
        return cpath.join(branch_path, version_number)

    def parse_revision_spec(self, revisions):
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
            (or print).

            There are many different ways to generate diffs for clearcase,
            because there are so many different workflows. This method serves
            more as a way to validate the passed-in arguments than actually
            parsing them in the way that other clients do.
        """
        n_revs = len(revisions)
        if n_revs == 0:
            return {b'base': self.REVISION_CHECKEDOUT_BASE, 
               b'tip': self.REVISION_CHECKEDOUT_CHANGESET}
        if n_revs == 1:
            if revisions[0].startswith(self.REVISION_ACTIVITY_PREFIX):
                return {b'base': self.REVISION_ACTIVITY_BASE, 
                   b'tip': revisions[0][len(self.REVISION_ACTIVITY_PREFIX):]}
            if revisions[0].startswith(self.REVISION_BRANCH_PREFIX):
                return {b'base': self.REVISION_BRANCH_BASE, 
                   b'tip': revisions[0][len(self.REVISION_BRANCH_PREFIX):]}
            if revisions[0].startswith(self.REVISION_LABEL_PREFIX):
                return {b'base': self.REVISION_LABEL_BASE, 
                   b'tip': [
                          revisions[0][len(self.REVISION_BRANCH_PREFIX):]]}
        else:
            if n_revs == 2:
                if self.viewtype != b'dynamic':
                    raise SCMError(b'To generate a diff using multiple revisions, you must use a dynamic view.')
                if revisions[0].startswith(self.REVISION_LABEL_PREFIX) and revisions[1].startswith(self.REVISION_LABEL_PREFIX):
                    return {b'base': self.REVISION_LABEL_BASE, 
                       b'tip': [ x[len(self.REVISION_BRANCH_PREFIX):] for x in revisions
                             ]}
            pairs = []
            for r in revisions:
                p = r.split(b':')
                if len(p) != 2:
                    raise InvalidRevisionSpecError(b'"%s" is not a valid file@revision pair' % r)
                pairs.append(p)

        return {b'base': self.REVISION_FILES, b'tip': pairs}

    def _sanitize_activity_changeset(self, changeset):
        """Return changeset containing non-binary, branched file versions.

        A UCM activity changeset contains all file revisions created/touched
        during this activity. File revisions are ordered earlier versions first
        in the format:
        changelist = [
        <path>@@<branch_path>/<version_number>, ...,
        <path>@@<branch_path>/<version_number>
        ]

        <path> is relative path to file
        <branch_path> is clearcase specific branch path to file revision
        <version number> is the version number of the file in <branch_path>.

        A UCM activity changeset can contain changes from different vobs,
        however reviewboard supports only changes from a single repo at the
        same time, so changes made outside of the current vobstag will be
        ignored.

        Args:
            changeset (unicode):
                The changeset to fetch.

        Returns:
            list:
            The list of file versions.
        """
        changelist = {}
        repository_info = self.get_repository_info()
        for change in changeset:
            path, current = change.split(b'@@')
            if path.find(b'%s/' % (repository_info.vobstag,)) == -1:
                logging.debug(b'Vobstag does not match, ignoring changes on %s', path)
                continue
            version_number = self._determine_version(current)
            if path not in changelist:
                changelist[path] = {b'highest': version_number, b'lowest': version_number, 
                   b'current': current}
            if version_number == 0:
                raise SCMError(b'Unexepected version_number=0 in activity changeset')
            elif version_number > changelist[path][b'highest']:
                changelist[path][b'highest'] = version_number
                changelist[path][b'current'] = current
            elif version_number < changelist[path][b'lowest']:
                changelist[path][b'lowest'] = version_number

        changeranges = []
        for path, version in six.iteritems(changelist):
            branch_path = self._determine_branch_path(version[b'current'])
            prev_version_number = str(int(version[b'lowest']) - 1)
            version[b'previous'] = self._construct_revision(branch_path, prev_version_number)
            changeranges.append((
             self._construct_extended_path(path, version[b'previous']),
             self._construct_extended_path(path, version[b'current'])))

        return changeranges

    def _sanitize_branch_changeset(self, changeset):
        """Return changeset containing non-binary, branched file versions.

        Changeset contain only first and last version of file made on branch.

        Args:
            changeset (unicode):
                The changeset to fetch.

        Returns:
            list:
            The list of file versions.
        """
        changelist = {}
        for path, previous, current in changeset:
            version_number = self._determine_version(current)
            if path not in changelist:
                changelist[path] = {b'highest': version_number, b'current': current, 
                   b'previous': previous}
            if version_number == 0:
                changelist[path][b'previous'] = previous
            elif version_number > changelist[path][b'highest']:
                changelist[path][b'highest'] = version_number
                changelist[path][b'current'] = current

        changeranges = []
        for path, version in six.iteritems(changelist):
            changeranges.append((
             self._construct_extended_path(path, version[b'previous']),
             self._construct_extended_path(path, version[b'current'])))

        return changeranges

    def _sanitize_checkedout_changeset(self, changeset):
        """Return extended paths for all modifications in a changeset.

        Args:
            changeset (unicode):
                The changeset to fetch.

        Returns:
            list:
            The list of file versions.
        """
        changeranges = []
        for path, previous, current in changeset:
            changeranges.append((
             self._construct_extended_path(path, previous),
             self._construct_extended_path(path, current)))

        return changeranges

    def _sanitize_version_0_file(self, file_revision):
        """Sanitize a version 0 file.

        This fixes up a revision identifier to use the correct predecessor
        revision when the version is 0. ``/main/0`` is a special case which is
        left as-is.

        Args:
            file_revision (unicode):
                The file revision to sanitize.

        Returns:
            unicode:
            Thee sanitized revision.
        """
        if file_revision.endswith(b'@@/main/0'):
            return file_revision
        if file_revision.endswith(b'/0'):
            logging.debug(b'Found file %s with version 0', file_revision)
            file_revision = execute([b'cleartool',
             b'describe',
             b'-fmt', b'%En@@%PSn',
             file_revision])
            logging.debug(b'Sanitized with predecessor, new file: %s', file_revision)
        return file_revision

    def _sanitize_version_0_changeset(self, changeset):
        """Return changeset sanitized of its <branch>/0 version.

        Indeed this predecessor (equal to <branch>/0) should already be
        available from previous vob synchro in multi-site context.

        Args:
            changeset (list):
                A list of changes in the changeset.

        Returns:
            list:
            The sanitized changeset.
        """
        sanitized_changeset = []
        for old_file, new_file in changeset:
            sanitized_changeset.append((
             self._sanitize_version_0_file(old_file),
             self._sanitize_version_0_file(new_file)))

        return sanitized_changeset

    def _directory_content(self, path):
        """Return directory content ready for saving to tempfile.

        Args:
            path (unicode):
                The path to list.

        Returns:
            unicode:
            The listed files in the directory.
        """
        output = execute([b'cleartool', b'ls', b'-short', b'-nxname', b'-vob_only',
         path])
        lines = output.splitlines(True)
        content = []
        for absolute_path in lines:
            short_path = os.path.basename(absolute_path.strip())
            content.append(short_path)

        return (b'').join([ b'%s\n' % s for s in sorted(content)
                          ])

    def _construct_changeset(self, output):
        """Construct a changeset from cleartool output.

        Args:
            output (unicode):
                The result from a :command:`cleartool lsX` operation.

        Returns:
            list:
            A list of changes.
        """
        return [ info.split(b'\t') for info in output.strip().split(b'\n')
               ]

    def _get_checkedout_changeset(self):
        """Return information about the checked out changeset.

        This function returns: kind of element, path to file, previews and
        current file version.

        Returns:
            list:
            A list of the changed files.
        """
        changeset = []
        output = execute([b'cleartool',
         b'lscheckout',
         b'-all',
         b'-cview',
         b'-me',
         b'-fmt',
         b'%En\\t%PVn\\t%Vn\\n'], extra_ignore_errors=(1, ), with_errors=False)
        if output:
            changeset = self._construct_changeset(output)
        return self._sanitize_checkedout_changeset(changeset)

    def _get_activity_changeset(self, activity):
        """Return information about the versions changed on a branch.

        This takes into account the changes attached to this activity
        (including rebase changes) in all vobs of the current view.

        Args:
            activity (unicode):
                The activity name.

        Returns:
            list:
            A list of the changed files.
        """
        changeset = []
        output = execute([b'cleartool',
         b'lsactivity',
         b'-fmt',
         b'%[versions]p',
         activity], extra_ignore_errors=(1, ), with_errors=False)
        if output:
            changeset = output.split()
        return self._sanitize_activity_changeset(changeset)

    def _get_branch_changeset(self, branch):
        """Return information about the versions changed on a branch.

        This takes into account the changes on the branch owned by the
        current user in all vobs of the current view.

        Args:
            branch (unicode):
                The branch name.

        Returns:
            list:
            A list of the changed files.
        """
        changeset = []
        if sys.platform.startswith(b'win'):
            CLEARCASE_XPN = b'%CLEARCASE_XPN%'
        else:
            CLEARCASE_XPN = b'$CLEARCASE_XPN'
        output = execute([
         b'cleartool',
         b'find',
         b'-all',
         b'-version',
         b'brtype(%s)' % branch,
         b'-exec',
         b'cleartool descr -fmt "%%En\t%%PVn\t%%Vn\n" %s' % CLEARCASE_XPN], extra_ignore_errors=(1, ), with_errors=False)
        if output:
            changeset = self._construct_changeset(output)
        return self._sanitize_branch_changeset(changeset)

    def _get_label_changeset(self, labels):
        """Return information about the versions changed between labels.

        This takes into account the changes done between labels and restrict
        analysis to current working directory. A ClearCase label belongs to a
        unique vob.

        Args:
            labels (list):
                A list of labels to compare.

        Returns:
            list:
            A list of the changed files.
        """
        changeset = []
        tmp_labels = []
        comparison_path = os.getcwd()
        error_message = None
        try:
            try:
                if len(labels) == 1:
                    tmp_lb = self._get_tmp_label()
                    tmp_labels.append(tmp_lb)
                    self._set_label(tmp_lb, comparison_path)
                    labels.append(tmp_lb)
                label_count = len(labels)
                if label_count != 2:
                    raise Exception(b'ClearCase label comparison does not support %d labels' % label_count)
                repository_info = self.get_repository_info()
                for label in labels:
                    if not self._is_a_label(label, repository_info.vobstag):
                        raise Exception(b'ClearCase label %s is not a valid label' % label)

                previous_label, current_label = labels
                logging.debug(b'Comparison between labels %s and %s on %s', previous_label, current_label, comparison_path)
                previous_elements = {}
                current_elements = {}
                previous_label_elements_thread = _get_elements_from_label_thread(1, comparison_path, previous_label, previous_elements)
                previous_label_elements_thread.start()
                current_label_elements_thread = _get_elements_from_label_thread(2, comparison_path, current_label, current_elements)
                current_label_elements_thread.start()
                previous_label_elements_thread.join()
                current_label_elements_thread.join()
                seen = []
                changelist = {}
                for path in itertools.chain(previous_elements.keys(), current_elements.keys()):
                    if path in seen:
                        continue
                    seen.append(path)
                    changelist[path] = {b'previous': b'/main/0', 
                       b'current': b'/main/0'}
                    if path in current_elements:
                        changelist[path][b'current'] = current_elements[path][b'version']
                    if path in previous_elements:
                        changelist[path][b'previous'] = previous_elements[path][b'version']
                    logging.debug(b'path: %s\nprevious: %s\ncurrent:  %s\n', path, changelist[path][b'previous'], changelist[path][b'current'])
                    if changelist[path][b'current'] == changelist[path][b'previous']:
                        continue
                    changeset.append((
                     self._construct_extended_path(path, changelist[path][b'previous']),
                     self._construct_extended_path(path, changelist[path][b'current'])))

            except Exception as e:
                error_message = str(e)

        finally:
            for lb in tmp_labels:
                if self._is_a_label(lb):
                    self._remove_label(lb)

            if error_message:
                raise SCMError(b'Label comparison failed:\n%s' % error_message)

        return changeset

    def diff(self, revisions, include_files=[], exclude_patterns=[], no_renames=False, extra_args=[]):
        """Perform a diff using the given revisions.

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
                Unused for ClearCase.

        Returns:
            dict:
            A dictionary containing the following keys:

            ``diff`` (:py:class:`bytes`):
                The contents of the diff to upload.
        """
        if include_files:
            raise Exception(b'The ClearCase backend does not currently support the -I/--include parameter. To diff for specific files, pass in file@revision1:file@revision2 pairs as arguments')
        if revisions[b'tip'] == self.REVISION_CHECKEDOUT_CHANGESET:
            changeset = self._get_checkedout_changeset()
            return self._do_diff(changeset)
        if revisions[b'base'] == self.REVISION_ACTIVITY_BASE:
            changeset = self._get_activity_changeset(revisions[b'tip'])
            return self._do_diff(changeset)
        if revisions[b'base'] == self.REVISION_BRANCH_BASE:
            changeset = self._get_branch_changeset(revisions[b'tip'])
            return self._do_diff(changeset)
        if revisions[b'base'] == self.REVISION_LABEL_BASE:
            changeset = self._get_label_changeset(revisions[b'tip'])
            return self._do_diff(changeset)
        if revisions[b'base'] == self.REVISION_FILES:
            include_files = revisions[b'tip']
            return self._do_diff(include_files)
        assert False

    def _diff_files(self, old_file, new_file):
        """Return a unified diff for file.

        Args:
            old_file (unicode):
                The name and version of the old file.

            new_file (unicode):
                The name and version of the new file.

        Returns:
            bytes:
            The diff between the two files.
        """
        if self.viewtype == b'snapshot':
            tmp_old_file = make_tempfile()
            tmp_new_file = make_tempfile()
            try:
                os.remove(tmp_old_file)
            except OSError:
                pass

            try:
                os.remove(tmp_new_file)
            except OSError:
                pass

            execute([b'cleartool', b'get', b'-to', tmp_old_file, old_file])
            execute([b'cleartool', b'get', b'-to', tmp_new_file, new_file])
            diff_cmd = [b'diff', b'-uN', tmp_old_file, tmp_new_file]
        else:
            diff_cmd = [
             b'diff', b'-uN', old_file, new_file]
        dl = execute(diff_cmd, extra_ignore_errors=(1, 2), results_unicode=False)
        if self.viewtype == b'snapshot':
            dl = dl.replace(tmp_old_file.encode(b'utf-8'), old_file.encode(b'utf-8'))
            dl = dl.replace(tmp_new_file.encode(b'utf-8'), new_file.encode(b'utf-8'))
        dl = dl.replace(b'\r\r\n', b'\r\n')
        dl = dl.splitlines(True)
        if len(dl) == 1 and dl[0].startswith(b'Files %s and %s differ' % (
         old_file.encode(b'utf-8'),
         new_file.encode(b'utf-8'))):
            dl = [
             b'Binary files %s and %s differ\n' % (
              old_file.encode(b'utf-8'),
              new_file.encode(b'utf-8'))]
        old_oid = execute([b'cleartool', b'describe', b'-fmt', b'%On', old_file], results_unicode=False)
        new_oid = execute([b'cleartool', b'describe', b'-fmt', b'%On', new_file], results_unicode=False)
        if dl == [] or dl[0].startswith(b'Binary files '):
            if dl == []:
                dl = [b'File %s in your changeset is unmodified\n' % new_file.encode(b'utf-8')]
            dl.insert(0, b'==== %s %s ====\n' % (old_oid, new_oid))
            dl.append(b'\n')
        else:
            dl.insert(2, b'==== %s %s ====\n' % (old_oid, new_oid))
        return dl

    def _diff_directories(self, old_dir, new_dir):
        """Return a unified diff between two directories' content.

        This function saves two version's content of directory to temp
        files and treats them as casual diff between two files.

        Args:
            old_dir (unicode):
                The path to a directory within a vob.

            new_dir (unicode):
                The path to a directory within a vob.

        Returns:
            list:
            The diff between the two directory trees, split into lines.
        """
        old_content = self._directory_content(old_dir)
        new_content = self._directory_content(new_dir)
        old_tmp = make_tempfile(content=old_content)
        new_tmp = make_tempfile(content=new_content)
        diff_cmd = [
         b'diff', b'-uN', old_tmp, new_tmp]
        dl = execute(diff_cmd, extra_ignore_errors=(1, 2), results_unicode=False, split_lines=True)
        if dl:
            dl[0] = dl[0].replace(old_tmp.encode(b'utf-8'), old_dir.encode(b'utf-8'))
            dl[1] = dl[1].replace(new_tmp.encode(b'utf-8'), new_dir.encode(b'utf-8'))
            old_oid = execute([b'cleartool', b'describe', b'-fmt', b'%On',
             old_dir], results_unicode=False)
            new_oid = execute([b'cleartool', b'describe', b'-fmt', b'%On',
             new_dir], results_unicode=False)
            dl.insert(2, b'==== %s %s ====\n' % (old_oid, new_oid))
        return dl

    def _do_diff(self, changeset):
        """Generate a unified diff for all files in the given changeset.

        Args:
            changeset (list):
                A list of changes.

        Returns:
            dict:
            A dictionary containing a ``diff`` key.
        """
        changeset = self._sanitize_version_0_changeset(changeset)
        diff = []
        for old_file, new_file in changeset:
            dl = []
            if self.viewtype == b'snapshot':
                object_path = new_file.split(b'@@')[0] + b'@@'
                output = execute([b'cleartool', b'describe', b'-fmt', b'%m',
                 object_path])
                object_kind = output.strip()
                isdir = object_kind == b'directory element'
            else:
                isdir = cpath.isdir(new_file)
            if isdir:
                dl = self._diff_directories(old_file, new_file)
            elif cpath.exists(new_file) or self.viewtype == b'snapshot':
                dl = self._diff_files(old_file, new_file)
            else:
                logging.error(b'File %s does not exist or access is denied.', new_file)
                continue
            if dl:
                diff.append((b'').join(dl))

        return {b'diff': (b'').join(diff)}


class ClearCaseRepositoryInfo(RepositoryInfo):
    """A representation of a ClearCase source code repository.

    This version knows how to find a matching repository on the server even if
    the URLs differ.
    """

    def __init__(self, path, base_path, vobstag):
        """Initialize the repsitory info.

        Args:
            path (unicode):
                The path of the repository.

            base_path (unicode):
                The relative path between the repository root and the working
                directory.

            vobstag (unicode):
                The vobstag for the repository.
        """
        RepositoryInfo.__init__(self, path, base_path, supports_parent_diffs=False)
        self.vobstag = vobstag

    def find_server_repository_info(self, server):
        """Find a matching repository on the server.

        The point of this function is to find a repository on the server that
        matches self, even if the paths aren't the same. (For example, if self
        uses an 'http' path, but the server uses a 'file' path for the same
        repository.) It does this by comparing the VOB's name and uuid. If the
        repositories use the same path, you'll get back self, otherwise you'll
        get a different ClearCaseRepositoryInfo object (with a different path).

        Args:
            server (rbtools.api.resource.RootResource):
                The root resource for the Review Board server.

        Returns:
            ClearCaseRepositoryInfo:
            The server-side information for this repository.
        """
        uuid = self._get_vobs_uuid(self.vobstag)
        logging.debug(b'Repository vobstag %s uuid is %r', self.vobstag, uuid)
        repository_scan_order = deque()
        vob_tag_parts = self.vobstag.split(cpath.sep)
        for repository in server.get_repositories(tool=b'ClearCase').all_items:
            if repository[b'tool'] != b'ClearCase':
                continue
            repo_name = repository[b'name']
            if repo_name == self.vobstag or repo_name in vob_tag_parts:
                repository_scan_order.appendleft(repository)
            else:
                repository_scan_order.append(repository)

        for repository in repository_scan_order:
            repo_name = repository[b'name']
            try:
                info = repository.get_info()
            except APIError as e:
                if not (e.error_code == 101 and e.http_status == 403):
                    if repo_name == self.vobstag:
                        raise SCMError(b'You do not have permission to access this repository.')
                    continue
                else:
                    raise e

            if not info or uuid != info[b'uuid']:
                continue
            path = info[b'repopath']
            logging.debug(b'Matching repository uuid:%s with path:%s', uuid, path)
            return ClearCaseRepositoryInfo(path=path, base_path=path, vobstag=self.vobstag)

        if parse_version(server.rb_version) >= parse_version(b'1.5.3'):
            self.path = cpath.split(self.vobstag)[1]
        return self

    def _get_vobs_uuid(self, vobstag):
        property_lines = execute([b'cleartool', b'lsvob', b'-long', vobstag], split_lines=True)
        for line in property_lines:
            if line.startswith(b'Vob family uuid:'):
                return line.split(b' ')[(-1)].rstrip()

    def _get_repository_info(self, server, repository):
        try:
            return server.get_repository_info(repository[b'id'])
        except APIError as e:
            if e.error_code == 210:
                return
            raise e

        return