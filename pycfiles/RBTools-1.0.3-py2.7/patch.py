# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/rbtools/commands/patch.py
# Compiled at: 2020-04-14 20:27:46
from __future__ import print_function, unicode_literals
import six
from rbtools.api.errors import APIError
from rbtools.clients.errors import CreateCommitError
from rbtools.commands import Command, CommandError, Option
from rbtools.utils.commands import extract_commit_message
from rbtools.utils.filesystem import make_tempfile

class Patch(Command):
    """Applies a specific patch from a RB server.

    The patch file indicated by the request id is downloaded from the
    server and then applied locally."""
    name = b'patch'
    author = b'The Review Board Project'
    args = b'<review-request-id>'
    option_list = [
     Option(b'-c', b'--commit', dest=b'commit', action=b'store_true', default=False, help=b'Commits using information fetched from the review request (Git/Mercurial only).', added_in=b'0.5.3'),
     Option(b'-C', b'--commit-no-edit', dest=b'commit_no_edit', action=b'store_true', default=False, help=b'Commits using information fetched from the review request (Git/Mercurial only). This differs from --commit by not invoking the editor to modify the commit message.'),
     Option(b'--diff-revision', dest=b'diff_revision', metavar=b'REVISION', default=None, help=b'The Review Board diff revision ID to use for the patch.'),
     Option(b'--px', dest=b'px', metavar=b'NUM', default=None, help=b"Strips the given number of paths from filenames in the diff. Equivalent to patch's `-p` argument."),
     Option(b'--print', dest=b'patch_stdout', action=b'store_true', default=False, help=b'Prints the patch to standard output instead of applying it to the tree.', added_in=b'0.5.3'),
     Option(b'-R', b'--revert', dest=b'revert_patch', action=b'store_true', default=False, help=b'Revert the given patch instead of applying it.\nThis feature does not work with Bazaar or Mercurial repositories.', added_in=b'0.7.3'),
     Command.server_options,
     Command.repository_options]

    def get_patch(self, request_id, api_root, diff_revision=None):
        """Return the diff as a string, the used diff revision and its basedir.

        If a diff revision is not specified, then this will look at the most
        recent diff.
        """
        try:
            diffs = api_root.get_diffs(review_request_id=request_id)
        except APIError as e:
            raise CommandError(b'Error getting diffs: %s' % e)

        if diff_revision is None:
            diff_revision = diffs.total_results
        try:
            diff = diffs.get_item(diff_revision)
            diff_body = diff.get_patch().data
            base_dir = getattr(diff, b'basedir', None) or b''
        except APIError:
            raise CommandError(b'The specified diff revision does not exist.')

        return (diff_body, diff_revision, base_dir)

    def apply_patch(self, repository_info, tool, request_id, diff_revision, diff_file_path, base_dir, revert=False):
        """Apply patch patch_file and display results to user."""
        if revert:
            print(b'Patch is being reverted from request %s with diff revision %s.' % (
             request_id, diff_revision))
        else:
            print(b'Patch is being applied from request %s with diff revision %s.' % (
             request_id, diff_revision))
        result = tool.apply_patch(diff_file_path, repository_info.base_path, base_dir, self.options.px, revert=revert)
        if result.patch_output:
            print()
            print(result.patch_output.strip())
            print()
        if not result.applied:
            if revert:
                raise CommandError(b'Unable to revert the patch. The patch may be invalid, or there may be conflicts that could not be resolved.')
            else:
                raise CommandError(b'Unable to apply the patch. The patch may be invalid, or there may be conflicts that could not be resolved.')
        if result.has_conflicts:
            if result.conflicting_files:
                if revert:
                    print(b'The patch was partially reverted, but there were conflicts in:')
                else:
                    print(b'The patch was partially applied, but there were conflicts in:')
                print()
                for filename in result.conflicting_files:
                    print(b'    %s' % filename)

                print()
            elif revert:
                print(b'The patch was partially reverted, but there were conflicts.')
            else:
                print(b'The patch was partially applied, but there were conflicts.')
            return False
        if revert:
            print(b'Successfully reverted patch.')
        else:
            print(b'Successfully applied patch.')
        return True

    def main(self, request_id):
        """Run the command."""
        if self.options.patch_stdout and self.options.server:
            server_url = self.options.server
        else:
            repository_info, tool = self.initialize_scm_tool(client_name=self.options.repository_type)
            if self.options.revert_patch and not tool.supports_patch_revert:
                raise CommandError(b'The %s backend does not support reverting patches.' % tool.name)
            server_url = self.get_server_url(repository_info, tool)
        api_client, api_root = self.get_api(server_url)
        if not self.options.patch_stdout:
            self.setup_tool(tool, api_root=api_root)
            repository_info = repository_info.find_server_repository_info(api_root)
        diff_body, diff_revision, base_dir = self.get_patch(request_id, api_root, self.options.diff_revision)
        if self.options.patch_stdout:
            if isinstance(diff_body, bytes):
                print(diff_body.decode(b'utf-8'))
            else:
                print(diff_body)
        else:
            try:
                if tool.has_pending_changes():
                    message = b'Working directory is not clean.'
                    if not self.options.commit:
                        print(b'Warning: %s' % message)
                    else:
                        raise CommandError(message)
            except NotImplementedError:
                pass

        tmp_patch_file = make_tempfile(diff_body)
        success = self.apply_patch(repository_info, tool, request_id, diff_revision, tmp_patch_file, base_dir, revert=self.options.revert_patch)
        if not success:
            raise CommandError(b'Could not apply patch')
        if self.options.commit or self.options.commit_no_edit:
            try:
                review_request = api_root.get_review_request(review_request_id=request_id, force_text_type=b'plain')
            except APIError as e:
                raise CommandError(b'Error getting review request %s: %s' % (
                 request_id, e))

            message = extract_commit_message(review_request)
            author = review_request.get_submitter()
            try:
                tool.create_commit(message=message, author=author, run_editor=not self.options.commit_no_edit)
                print(b'Changes committed to current branch.')
            except CreateCommitError as e:
                raise CommandError(six.text_type(e))
            except NotImplementedError:
                raise CommandError(b'--commit is not supported with %s' % tool.name)