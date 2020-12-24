# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/flawless/lib/version_control/repo.py
# Compiled at: 2017-12-21 14:32:09
import abc, logging, os, os.path, re, subprocess
from future.utils import with_metaclass
import flawless.lib.config
log = logging.getLogger(__name__)
config = flawless.lib.config.get()

def get_repository(open_process_func=subprocess.Popen):
    if config.repo_type == 'git':
        return GitRepository(open_process_func=open_process_func)


class Repository(with_metaclass(abc.ABCMeta, object)):

    def __init__(self, local_path=None, remote_url=None, branch_pattern=None, open_process_func=subprocess.Popen):
        self.local_path = local_path or config.repo_dir
        self.remote_url = remote_url or config.repo_url
        self.open_process_func = open_process_func
        self.branch_pattern = re.compile(config.repo_branch_pattern) if config.repo_branch_pattern else None
        return

    @abc.abstractmethod
    def blame(self, filename, line_number):
        pass

    @abc.abstractmethod
    def update(self):
        pass

    @abc.abstractmethod
    def create(self):
        pass


class GitRepository(Repository):

    def __init__(self, *args, **kwargs):
        super(GitRepository, self).__init__(*args, **kwargs)
        self.extract_email_pattern = re.compile('^author-mail <([^>]+)+>$')
        self.extract_modified_pattern = re.compile('^author-time (\\d+)$')
        self.digit_tokenizer_pattern = re.compile('(\\d+)|(\\D+)').findall
        self.natural_sort_func = lambda s: tuple((int(num) if num else alpha) for num, alpha in self.digit_tokenizer_pattern(s))

    def _raw_run(self, args, log_output=False):
        p = self.open_process_func(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        err = p.stderr.read()
        out = p.stdout.read()
        if log_output and out:
            log.info(out)
        if log_output and err:
            log.error(err)
        return out

    def _run_git_command(self, args, log_output=False):
        base_args = [
         config.git_cli_path,
         '--git-dir=%s' % os.path.join(self.local_path, '.git'),
         '--work-tree=%s' % self.local_path]
        base_args.extend(args)
        return self._raw_run(base_args, log_output=log_output)

    def blame(self, filename, line_number):
        args = [
         'blame',
         '-p',
         os.path.join(self.local_path, filename),
         '-L',
         '%d,+1' % line_number]
        output = self._run_git_command(args)
        email, modified = (None, None)
        for line in output.split('\n'):
            if email and modified:
                break
            match = self.extract_email_pattern.match(line)
            if match:
                email = match.group(1)
            match = self.extract_modified_pattern.match(line)
            if match:
                modified = int(match.group(1))

        return (
         email, modified)

    def update(self, log_output=False):
        if not self.remote_url:
            return
        if self.branch_pattern:
            self._run_git_command(['fetch'], log_output=log_output)
            all_branches = self._run_git_command(['branch', '-r'], log_output=log_output).split('\n')
            all_branches = [ s.strip() for s in all_branches if '->' not in s and s.strip() ]
            all_branches = sorted(all_branches, key=self.natural_sort_func)
            all_branches = [ s for s in all_branches if self.branch_pattern.match(s) ]
            self._run_git_command(['reset', '--hard', all_branches[(-1)]], log_output=log_output)
        else:
            self._run_git_command(['pull', '--rebase'], log_output=log_output)

    def create(self):
        if not os.path.exists(self.local_path):
            os.makedirs(self.local_path)
        self._raw_run([
         config.git_cli_path, 'clone', self.remote_url, self.local_path], log_output=True)
        self.update(log_output=True)