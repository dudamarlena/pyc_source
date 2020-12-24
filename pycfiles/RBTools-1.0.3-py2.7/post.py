# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/rbtools/commands/post.py
# Compiled at: 2020-04-14 20:27:46
from __future__ import print_function, unicode_literals
import logging, os, platform, re, sys, six
from rbtools.api.errors import APIError
from rbtools.commands import Command, CommandError, Option, OptionGroup
from rbtools.utils.commands import AlreadyStampedError, stamp_commit_with_review_url
from rbtools.utils.console import confirm
from rbtools.utils.process import execute
from rbtools.utils.review_request import get_draft_or_current_value, get_revisions, guess_existing_review_request

class Post(Command):
    """Create and update review requests."""
    name = b'post'
    author = b'The Review Board Project'
    description = b'Uploads diffs to create and update review requests.'
    args = b'[revisions]'
    reserved_fields = ('description', 'testing-done', 'summary')
    GUESS_AUTO = b'auto'
    GUESS_YES = b'yes'
    GUESS_NO = b'no'
    GUESS_YES_INPUT_VALUES = (True, b'yes', 1, b'1')
    GUESS_NO_INPUT_VALUES = (False, b'no', 0, b'0')
    GUESS_CHOICES = (GUESS_AUTO, GUESS_YES, GUESS_NO)
    option_list = [
     OptionGroup(name=b'Posting Options', description=b'Controls the behavior of a post, including what review request gets posted and how, and what happens after it is posted.', option_list=[
      Option(b'-u', b'--update', dest=b'update', action=b'store_true', default=False, help=b'Automatically determines the existing review request to update.', added_in=b'0.5.3'),
      Option(b'-r', b'--review-request-id', dest=b'rid', metavar=b'ID', default=None, help=b'Specifies the existing review request ID to update.'),
      Option(b'-p', b'--publish', dest=b'publish', action=b'store_true', default=False, config_key=b'PUBLISH', help=b'Publishes the review request immediately after posting.\nAll required fields must already be filled in on the review request or must be provided when posting.'),
      Option(b'-t', b'--trivial-publish', dest=b'trivial_publish', action=b'store_true', default=False, help=b'Publish the review request immediately after posting, but without sending an e-mail notification.', added_in=b'1.0'),
      Option(b'-o', b'--open', dest=b'open_browser', action=b'store_true', config_key=b'OPEN_BROWSER', default=False, help=b'Opens a web browser to the review request after posting.'),
      Option(b'-s', b'--stamp', dest=b'stamp_when_posting', action=b'store_true', config_key=b'STAMP_WHEN_POSTING', default=False, help=b'Stamps the commit message with the review request URL while posting the review.', added_in=b'0.7.3'),
      Option(b'--submit-as', dest=b'submit_as', metavar=b'USERNAME', config_key=b'SUBMIT_AS', default=None, help=b'The username to use as the author of the review request, instead of the logged in user.', extended_help=b"This is useful when used in a repository's post-commit script to update or create review requests. See :ref:`automating-rbt-post` for more information on this use case."),
      Option(b'--change-only', dest=b'change_only', action=b'store_true', default=False, help=b'Updates fields from the change description, but does not upload a new diff (Perforce/Plastic only).'),
      Option(b'--diff-only', dest=b'diff_only', action=b'store_true', default=False, help=b'Uploads a new diff, but does not automatically update fields from the commit message/change description. Fields explicitly provided by other options will be ignored.')]),
     Command.server_options,
     Command.repository_options,
     OptionGroup(name=b'Review Request Field Options', description=b'Options for setting the contents of fields in the review request.', option_list=[
      Option(b'-f', b'--field', dest=b'fields', action=b'append', default=None, metavar=b'FIELD_NAME=VALUE', help=b'Sets custom fields into the extra_data of a review request. Can also be used to set built-in fields like description, summary, testing-done.'),
      Option(b'-g', b'--guess-fields', dest=b'guess_fields', action=b'store', config_key=b'GUESS_FIELDS', nargs=b'?', default=GUESS_AUTO, const=GUESS_YES, choices=GUESS_CHOICES, help=b'Equivalent to setting both --guess-summary and --guess-description.', extended_help=b'This can optionally take a value to control the guessing behavior. See :ref:`guessing-behavior` for more information.'),
      Option(b'--guess-summary', dest=b'guess_summary', action=b'store', config_key=b'GUESS_SUMMARY', nargs=b'?', default=None, const=GUESS_YES, choices=GUESS_CHOICES, help=b'Generates the Summary field based on the commit messages (Bazaar/Git/Mercurial only).', extended_help=b'This can optionally take a value to control the guessing behavior. See :ref:`guessing-behavior` for more information.'),
      Option(b'--guess-description', dest=b'guess_description', action=b'store', config_key=b'GUESS_DESCRIPTION', nargs=b'?', default=None, const=GUESS_YES, choices=GUESS_CHOICES, help=b'Generates the Description field based on the commit messages (Bazaar/Git/Mercurial only).', extended_help=b'This can optionally take a value to control the guessing behavior. See :ref:`guessing-behavior` for more information.'),
      Option(b'-m', b'--change-description', dest=b'change_description', default=None, metavar=b'TEXT', help=b'A description of what changed in this update of the review request. This is ignored for new review requests.'),
      Option(b'--summary', dest=b'summary', metavar=b'TEXT', default=None, help=b'The new contents for the Summary field.'),
      Option(b'--description', dest=b'description', metavar=b'TEXT', default=None, help=b'The new contents for the Description field.'),
      Option(b'--description-file', dest=b'description_file', default=None, metavar=b'FILENAME', help=b'A text file containing the new contents for the Description field.'),
      Option(b'--testing-done', dest=b'testing_done', metavar=b'TEXT', default=None, help=b'The new contents for the Testing Done field.'),
      Option(b'--testing-done-file', dest=b'testing_file', default=None, metavar=b'FILENAME', help=b'A text file containing the new contents for the Testing Done field.'),
      Option(b'--branch', dest=b'branch', config_key=b'BRANCH', metavar=b'BRANCH', default=None, help=b'The branch the change will be committed on or affects. This is a free-form field and does not control any behavior.'),
      Option(b'--bugs-closed', dest=b'bugs_closed', metavar=b'BUG_ID[,...]', default=None, help=b'The comma-separated list of bug IDs closed.'),
      Option(b'--target-groups', dest=b'target_groups', metavar=b'NAME[,...]', default=None, help=b'The names of the groups that should perform the review.'),
      Option(b'--target-people', dest=b'target_people', metavar=b'USERNAME[,...]', default=None, help=b'The usernames of the people who should perform the review.'),
      Option(b'--depends-on', dest=b'depends_on', config_key=b'DEPENDS_ON', metavar=b'ID[,...]', default=None, help=b'A comma-separated list of review request IDs that this review request will depend on.', added_in=b'0.6.1'),
      Option(b'--markdown', dest=b'markdown', action=b'store_true', config_key=b'MARKDOWN', default=False, help=b'Specifies if the summary, description, and change description should should be interpreted as Markdown-formatted text.\nThis is only supported in Review Board 2.0+.', added_in=b'0.6')]),
     Command.diff_options,
     Command.branch_options,
     Command.perforce_options,
     Command.subversion_options,
     Command.tfs_options]

    def post_process_options(self):
        super(Post, self).post_process_options()
        extra_fields = {}
        if self.options.fields is None:
            self.options.fields = []
        for field in self.options.fields:
            key_value_pair = field.split(b'=', 1)
            if len(key_value_pair) != 2:
                raise CommandError(b'The --field argument should be in the form of: --field name=value; got "%s" instead.' % field)
            key, value = key_value_pair
            if key in self.reserved_fields:
                key_var = key.replace(b'-', b'_')
                if getattr(self.options, key_var):
                    raise CommandError((b'The "{0}" field was provided by both --{0}= and --field {0}=. Please use --{0} instead.').format(key))
                setattr(self.options, key_var, value)
            else:
                extra_fields[b'extra_data.%s' % key] = value

        self.options.extra_fields = extra_fields
        if not self.options.update and self.options.rid is None:
            if self.options.target_groups is None and b'TARGET_GROUPS' in self.config:
                self.options.target_groups = self.config[b'TARGET_GROUPS']
            if self.options.target_people is None and b'TARGET_PEOPLE' in self.config:
                self.options.target_people = self.config[b'TARGET_PEOPLE']
        self.options.guess_fields = self.normalize_guess_value(self.options.guess_fields, b'--guess-fields')
        for field_name in ('guess_summary', 'guess_description'):
            if getattr(self.options, field_name) is None:
                setattr(self.options, field_name, self.options.guess_fields)

        if self.options.revision_range:
            raise CommandError(b'The --revision-range argument has been removed. To post a diff for one or more specific revisions, pass those revisions as arguments. For more information, see the RBTools 0.6 Release Notes.')
        if self.options.svn_changelist:
            raise CommandError(b'The --svn-changelist argument has been removed. To use a Subversion changelist, pass the changelist name as an additional argument after the command.')
        if self.options.description and self.options.description_file:
            raise CommandError(b'The --description and --description-file options are mutually exclusive.')
        if self.options.description_file:
            if os.path.exists(self.options.description_file):
                with open(self.options.description_file, b'r') as (fp):
                    self.options.description = fp.read()
            else:
                raise CommandError(b'The description file %s does not exist.' % self.options.description_file)
        if self.options.testing_done and self.options.testing_file:
            raise CommandError(b'The --testing-done and --testing-done-file options are mutually exclusive.')
        if self.options.testing_file:
            if os.path.exists(self.options.testing_file):
                with open(self.options.testing_file, b'r') as (fp):
                    self.options.testing_done = fp.read()
            else:
                raise CommandError(b'The testing file %s does not exist.' % self.options.testing_file)
        if self.options.summary:
            self.options.guess_summary = self.GUESS_NO
        else:
            self.options.guess_summary = self.normalize_guess_value(self.options.guess_summary, b'--guess-summary')
        if self.options.description:
            self.options.guess_description = self.GUESS_NO
        else:
            self.options.guess_description = self.normalize_guess_value(self.options.guess_description, b'--guess-description')
        if self.options.diff_filename and self.options.update:
            raise CommandError(b'The --update option cannot be used when using --diff-filename.')
        if self.options.rid and self.options.update:
            self.options.update = False
        if self.options.trivial_publish:
            self.options.publish = True
        return

    def normalize_guess_value(self, guess, arg_name):
        if guess in self.GUESS_YES_INPUT_VALUES:
            return self.GUESS_YES
        if guess in self.GUESS_NO_INPUT_VALUES:
            return self.GUESS_NO
        if guess == self.GUESS_AUTO:
            return guess
        raise CommandError(b'Invalid value "%s" for argument "%s"' % (
         guess, arg_name))

    def get_repository_path(self, repository_info, api_root):
        """Get the repository path from the server.

        This will compare the paths returned by the SCM client
        with those one the server, and return the first match.
        """
        if isinstance(repository_info.path, list):
            repositories = api_root.get_repositories(only_fields=b'path,mirror_path', only_links=b'')
            for repo in repositories.all_items:
                if repo[b'path'] in repository_info.path:
                    repository_info.path = repo[b'path']
                    break
                elif repo[b'mirror_path'] in repository_info.path:
                    repository_info.path = repo[b'mirror_path']
                    break

        if isinstance(repository_info.path, list):
            error_str = [b'There was an error creating this review request.\n',
             b'\n',
             b'There was no matching repository path found on the server.\n',
             b'Unknown repository paths found:\n']
            for foundpath in repository_info.path:
                error_str.append(b'\t%s\n' % foundpath)

            error_str += [
             b'Ask the administrator to add one of these repositories\n',
             b'to the Review Board server.\n']
            raise CommandError((b'').join(error_str))
        return repository_info.path

    def post_request(self, repository_info, repository, server_url, api_root, review_request_id=None, changenum=None, diff_content=None, parent_diff_content=None, commit_id=None, base_commit_id=None, submit_as=None, retries=3, base_dir=None):
        """Creates or updates a review request, and uploads a diff.

        On success the review request id and url are returned.
        """
        supports_posting_commit_ids = self.tool.capabilities.has_capability(b'review_requests', b'commit_ids')
        if review_request_id:
            try:
                review_request = api_root.get_review_request(review_request_id=review_request_id, only_fields=b'absolute_url,bugs_closed,id,status,public', only_links=b'diffs,draft')
            except APIError as e:
                raise CommandError(b'Error getting review request %s: %s' % (
                 review_request_id, e))

            if review_request.status == b'submitted':
                raise CommandError(b'Review request %s is marked as %s. In order to update it, please reopen the review request and try again.' % (
                 review_request_id, review_request.status))
        else:
            try:
                request_data = {b'repository': repository}
                if changenum:
                    request_data[b'changenum'] = changenum
                elif commit_id and supports_posting_commit_ids:
                    request_data[b'commit_id'] = commit_id
                if submit_as:
                    request_data[b'submit_as'] = submit_as
                if self.tool.can_bookmark:
                    bookmark = self.tool.get_current_bookmark()
                    request_data[b'extra_data__local_bookmark'] = bookmark
                elif self.tool.can_branch:
                    branch = self.tool.get_current_branch()
                    request_data[b'extra_data__local_branch'] = branch
                review_requests = api_root.get_review_requests(only_fields=b'', only_links=b'create')
                review_request = review_requests.create(**request_data)
            except APIError as e:
                if e.error_code == 204 and changenum:
                    rid = e.rsp[b'review_request'][b'id']
                    review_request = api_root.get_review_request(review_request_id=rid, only_fields=b'absolute_url,bugs_closed,id,status', only_links=b'diffs,draft')
                else:
                    raise CommandError(b'Error creating review request: %s' % e)

            if not repository_info.supports_changesets or not self.options.change_only:
                try:
                    diff_kwargs = {b'parent_diff': parent_diff_content, 
                       b'base_dir': base_dir}
                    if base_commit_id and self.tool.capabilities.has_capability(b'diffs', b'base_commit_ids'):
                        diff_kwargs[b'base_commit_id'] = base_commit_id
                    review_request.get_diffs(only_fields=b'').upload_diff(diff_content, **diff_kwargs)
                except APIError as e:
                    error_msg = [
                     b'Error uploading diff\n']
                    if e.error_code == 101 and e.http_status == 403:
                        error_msg.append(b'You do not have permissions to modify this review request')
                    elif e.error_code == 219:
                        error_msg.append(b'The generated diff file was empty. This usually means no files were modified in this change.')
                    else:
                        error_msg.append(six.text_type(e))
                    error_msg.append(b'Your review request still exists, but the diff is not attached.')
                    error_msg.append(b'%s' % review_request.absolute_url)
                    raise CommandError((b'\n').join(error_msg))

            try:
                draft = review_request.get_draft(only_fields=b'commit_id')
            except APIError as e:
                raise CommandError(b'Error retrieving review request draft: %s' % e)

        if self.options.stamp_when_posting:
            if not self.tool.can_amend_commit:
                print(b'Cannot stamp review URL onto the commit message; stamping is not supported with %s.' % self.tool.name)
            else:
                try:
                    stamp_commit_with_review_url(self.revisions, review_request.absolute_url, self.tool)
                    print(b'Stamped review URL onto the commit message.')
                except AlreadyStampedError:
                    print(b'Commit message has already been stamped')
                except Exception as e:
                    logging.debug(b'Caught exception while stamping the commit message. Proceeding to post without stamping.', exc_info=True)
                    print(b'Could not stamp review URL onto the commit message.')

        update_fields = {}
        if self.options.publish:
            update_fields[b'public'] = True
            if self.options.trivial_publish and self.tool.capabilities.has_capability(b'review_requests', b'trivial_publish'):
                update_fields[b'trivial'] = True
        if not self.options.diff_only:
            if not self.options.diff_filename:
                self.check_guess_fields()
            update_fields.update(self.options.extra_fields)
            if self.options.target_groups:
                update_fields[b'target_groups'] = self.options.target_groups
            if self.options.target_people:
                update_fields[b'target_people'] = self.options.target_people
            if self.options.depends_on:
                update_fields[b'depends_on'] = self.options.depends_on
            if self.options.summary:
                update_fields[b'summary'] = self.options.summary
            if self.options.branch:
                update_fields[b'branch'] = self.options.branch
            if self.options.bugs_closed:
                self.options.bugs_closed = self.options.bugs_closed.strip(b', ')
                bug_set = set(re.split(b'[, ]+', self.options.bugs_closed)) | set(review_request.bugs_closed)
                self.options.bugs_closed = (b',').join(bug_set)
                update_fields[b'bugs_closed'] = self.options.bugs_closed
            if self.options.description:
                update_fields[b'description'] = self.options.description
            if self.options.testing_done:
                update_fields[b'testing_done'] = self.options.testing_done
            if (self.options.description or self.options.testing_done) and self.options.markdown and self.tool.capabilities.has_capability(b'text', b'markdown'):
                update_fields[b'text_type'] = b'markdown'
            if self.options.change_description is not None:
                if review_request.public:
                    update_fields[b'changedescription'] = self.options.change_description
                    if self.options.markdown and self.tool.capabilities.has_capability(b'text', b'markdown'):
                        update_fields[b'changedescription_text_type'] = b'markdown'
                    else:
                        update_fields[b'changedescription_text_type'] = b'plain'
                else:
                    logging.error(b'The change description field can only be set when publishing an update. Use --description instead.')
            if supports_posting_commit_ids and commit_id != draft.commit_id:
                update_fields[b'commit_id'] = commit_id or b''
        if update_fields:
            try:
                draft = draft.update(**update_fields)
            except APIError as e:
                raise CommandError(b'Error updating review request draft: %s\n\nYour review request still exists, but the diff is not attached.\n\n%s\n' % (
                 e, review_request.absolute_url))

        return (
         review_request.id, review_request.absolute_url)

    def check_guess_fields(self):
        """Checks and handles field guesses for the review request.

        This will attempt to guess the values for the summary and
        description fields, based on the contents of the commit message
        at the provided revisions, if requested by the caller.

        If the backend doesn't support guessing, or if guessing isn't
        requested, or if explicit values were set in the options, nothing
        will be set for the fields.
        """
        is_new_review_request = not self.options.rid and not self.options.update
        guess_summary = self.options.guess_summary == self.GUESS_YES or self.options.guess_summary == self.GUESS_AUTO and is_new_review_request
        guess_description = self.options.guess_description == self.GUESS_YES or self.options.guess_description == self.GUESS_AUTO and is_new_review_request
        if self.revisions and (guess_summary or guess_description):
            try:
                commit_message = self.tool.get_commit_message(self.revisions)
                if commit_message:
                    guessed_summary = commit_message[b'summary']
                    guessed_description = commit_message[b'description']
                    if guess_summary and guess_description:
                        self.options.summary = guessed_summary
                        self.options.description = guessed_description
                    elif guess_summary:
                        self.options.summary = guessed_summary
                    elif guess_description:
                        if guessed_description.startswith(guessed_summary):
                            self.options.description = guessed_description
                        else:
                            self.options.description = guessed_summary + b'\n\n' + guessed_description
            except NotImplementedError:
                pass

    def _ask_review_request_match(self, review_request):
        question = b'Update Review Request #%s: "%s"? ' % (
         review_request.id,
         get_draft_or_current_value(b'summary', review_request))
        return confirm(question)

    def main(self, *args):
        """Create and update review requests."""
        self.cmd_args = list(args)
        self.post_process_options()
        origcwd = os.path.abspath(os.getcwd())
        repository_info, self.tool = self.initialize_scm_tool(client_name=self.options.repository_type)
        server_url = self.get_server_url(repository_info, self.tool)
        api_client, api_root = self.get_api(server_url)
        self.setup_tool(self.tool, api_root=api_root)
        if self.options.exclude_patterns and not self.tool.supports_diff_exclude_patterns:
            raise CommandError(b'The %s backend does not support excluding files via the -X/--exclude commandline options or the EXCLUDE_PATTERNS .reviewboardrc option.' % self.tool.name)
        repository_info = repository_info.find_server_repository_info(api_root)
        if self.options.diff_filename:
            self.revisions = None
            parent_diff = None
            base_commit_id = None
            commit_id = None
            if self.options.diff_filename == b'-':
                if hasattr(sys.stdin, b'buffer'):
                    diff = sys.stdin.buffer.read()
                else:
                    diff = sys.stdin.read()
            else:
                try:
                    diff_path = os.path.join(origcwd, self.options.diff_filename)
                    with open(diff_path, b'rb') as (fp):
                        diff = fp.read()
                except IOError as e:
                    raise CommandError(b'Unable to open diff filename: %s' % e)

        else:
            self.revisions = get_revisions(self.tool, self.cmd_args)
            if self.revisions:
                extra_args = None
            else:
                extra_args = self.cmd_args
            diff_info = self.tool.diff(revisions=self.revisions, include_files=self.options.include_files or [], exclude_patterns=self.options.exclude_patterns or [], extra_args=extra_args)
            diff = diff_info[b'diff']
            parent_diff = diff_info.get(b'parent_diff')
            base_commit_id = diff_info.get(b'base_commit_id')
            commit_id = diff_info.get(b'commit_id')
            logging.debug(b'Generated diff size: %d bytes', len(diff))
            if parent_diff:
                logging.debug(b'Generated parent diff size: %d bytes', len(parent_diff))
        repository = self.options.repository_name or self.options.repository_url or self.get_repository_path(repository_info, api_root)
        base_dir = self.options.basedir or repository_info.base_path
        if repository is None:
            raise CommandError(b'Could not find the repository on the Review Board server.')
        if len(diff) == 0:
            raise CommandError(b"There don't seem to be any diffs!")
        can_validate_base_commit_ids = self.tool.capabilities.has_capability(b'diffs', b'validation', b'base_commit_ids')
        if not base_commit_id or can_validate_base_commit_ids or self.tool.name != b'Git':
            validate_kwargs = {}
            if can_validate_base_commit_ids:
                validate_kwargs[b'base_commit_id'] = base_commit_id
            try:
                diff_validator = api_root.get_diff_validation()
                diff_validator.validate_diff(repository, diff, parent_diff=parent_diff, base_dir=base_dir, **validate_kwargs)
            except APIError as e:
                msg_prefix = b''
                if e.error_code == 207:
                    msg_prefix = b'%s: ' % e.rsp[b'file']
                raise CommandError(b'Error validating diff\n\n%s%s' % (
                 msg_prefix, e))
            except AttributeError:
                pass

        if repository_info.supports_changesets and not self.options.diff_filename and b'changenum' in diff_info:
            changenum = diff_info[b'changenum']
        else:
            changenum = self.tool.get_changenum(self.revisions)
        commit_id = changenum or commit_id
        if self.options.update and self.revisions:
            try:
                review_request = guess_existing_review_request(repository_info, self.options.repository_name, api_root, api_client, self.tool, self.revisions, guess_summary=False, guess_description=False, is_fuzzy_match_func=self._ask_review_request_match, submit_as=self.options.submit_as)
            except ValueError as e:
                raise CommandError(six.text_type(e))

            if not review_request or not review_request.id:
                raise CommandError(b'Could not determine the existing review request to update.')
            self.options.rid = review_request.id
        if self.options.include_files or self.options.exclude_patterns:
            commit_id = None
        request_id, review_url = self.post_request(repository_info, repository, server_url, api_root, self.options.rid, changenum=changenum, diff_content=diff, parent_diff_content=parent_diff, commit_id=commit_id, base_commit_id=base_commit_id, submit_as=self.options.submit_as, base_dir=base_dir)
        diff_review_url = review_url + b'diff/'
        print(b'Review request #%s posted.' % request_id)
        print()
        print(review_url)
        print(diff_review_url)
        if self.options.open_browser:
            try:
                if sys.platform == b'darwin' and platform.mac_ver()[0] == b'10.12.5':
                    open([b'open', review_url])
                else:
                    import webbrowser
                    webbrowser.open_new_tab(review_url)
            except Exception as e:
                logging.exception(b'Error opening review URL %s: %s', review_url, e)

        return