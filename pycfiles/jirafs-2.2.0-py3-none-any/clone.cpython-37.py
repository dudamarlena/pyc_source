# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/acoddington/Documents/Projects/jirafs/jirafs/commands/clone.py
# Compiled at: 2020-01-13 00:37:20
# Size of source mod 2**32: 5112 bytes
import os, re, shutil, subprocess, tempfile
from urllib import parse
from jirafs import constants, exceptions, utils
from jirafs.plugin import CommandPlugin
from jirafs.ticketfolder import TicketFolder

class Command(CommandPlugin):
    __doc__ = ' Clone a new ticketfolder for the specified ticket URL'
    MIN_VERSION = '2.0.0'
    MAX_VERSION = '3.0.0'
    AUTOMATICALLY_INSTANTIATE_FOLDER = False
    TICKET_RE = re.compile('.*\\/browse\\/(\\w+-\\d+)\\/?')

    def handle(self, args, jira, path, **kwargs):
        ticket_url = args.ticket_url[0]
        if not os.path.exists(os.path.realpath(ticket_url)):
            ticket_url_parts = parse.urlparse(ticket_url)
            if not ticket_url_parts.netloc:
                default_server = utils.get_default_jira_server()
                ticket_url = parse.urljoin(default_server, 'browse/' + ticket_url + '/')
        path = args.path[0] if args.path else None
        return self.cmd(path, ticket_url, jira)

    def clone_from_issue(self, match, ticket_url, path, jira):
        if not path:
            path = match.group(1)
        path = os.path.realpath(path)
        os.mkdir(path)
        try:
            folder = TicketFolder.initialize_ticket_folder(ticket_url, path, jira)
            utils.run_command_method_with_kwargs('pull', folder=folder)
        except Exception:
            shutil.rmtree(path)
            raise

        folder.log('Issue %s cloned successfully to %s', (folder.issue_url, folder.path))
        return folder

    def clone_from_git_repository(self, url, path, jira):
        temp_dir = tempfile.mkdtemp()
        subprocess.check_call([
         'git', 'clone', url, temp_dir],
          stdout=(subprocess.PIPE),
          stderr=(subprocess.PIPE))
        for branch in ('jira', 'master'):
            subprocess.check_call([
             'git', 'checkout', branch],
              cwd=temp_dir,
              stdout=(subprocess.PIPE),
              stderr=(subprocess.PIPE))

        issue_url_path = os.path.join(temp_dir, constants.METADATA_DIR, 'issue_url')
        with open(issue_url_path, 'r') as (issue_url_file):
            issue_url = issue_url_file.read()
        match = self.TICKET_RE.match(issue_url)
        if not match:
            shutil.rmtree(temp_dir)
            raise exceptions.NotTicketFolderException('The git repository at %s is not a Jirafs backup.' % (url,))
        elif path:
            path = os.path.realpath(path)
        else:
            path = os.path.realpath(match.group(1))
        os.rename(temp_dir, path)
        shadow_path = os.path.join(path, constants.METADATA_DIR, 'shadow')
        subprocess.check_call([
         'git', 'clone', path, shadow_path],
          stdout=(subprocess.PIPE),
          stderr=(subprocess.PIPE))
        os.rename(os.path.join(path, '.git'), os.path.join(path, constants.METADATA_DIR, 'git'))
        subprocess.check_call([
         'git', 'remote', 'set-url', 'origin', '../git'],
          cwd=shadow_path,
          stdout=(subprocess.PIPE),
          stderr=(subprocess.PIPE))
        subprocess.check_call([
         'git', 'checkout', 'jira'],
          cwd=shadow_path,
          stdout=(subprocess.PIPE),
          stderr=(subprocess.PIPE))
        folder = TicketFolder(path, jira)
        folder.run_git_command('config', '--file=%s' % folder.get_metadata_path('git', 'config'), 'core.excludesfile', '.jirafs/gitignore')
        folder.log('Cloned Jirafs ticket folder for %s at %s; on hash %s', (
         folder.issue_url,
         folder.path,
         folder.run_git_command('rev-parse', 'master')))
        return folder

    def main(self, path, url, jira):
        match = self.TICKET_RE.match(url)
        if match:
            return self.clone_from_issue(match, url, path, jira)
        try:
            subprocess.check_call([
             'git', 'ls-remote', url],
              stdout=(subprocess.PIPE),
              stderr=(subprocess.PIPE))
            return self.clone_from_git_repository(url, path, jira)
        except subprocess.CalledProcessError:
            pass

        raise exceptions.JirafsError("'%s' is neither a valid JIRA ticket URL, nor Jirafs remote backup" % url)

    def add_arguments(self, parser):
        parser.add_argument('ticket_url', nargs=1, type=str)
        parser.add_argument('path',
          nargs='*', type=str)