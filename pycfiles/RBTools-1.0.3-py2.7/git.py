# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/rbtools/hooks/git.py
# Compiled at: 2020-04-14 20:27:46
from __future__ import unicode_literals
from collections import defaultdict
from copy import deepcopy
import six
from rbtools.hooks.common import execute, get_review_request_id

def get_branch_name(ref_name):
    """Returns the branch name corresponding to the specified ref name."""
    branch_ref_prefix = b'refs/heads/'
    if ref_name.startswith(branch_ref_prefix):
        return ref_name[len(branch_ref_prefix):]


def get_commit_hashes(old_rev, new_rev):
    """Returns a list of abbreviated commit hashes from old_rev to new_rev."""
    git_command = [
     b'git', b'rev-list', b'--abbrev-commit', b'--reverse',
     b'%s..%s' % (
      old_rev, new_rev)]
    return execute(git_command).split(b'\n')


def get_unique_commit_hashes(ref_name, new_rev):
    """Returns a list of abbreviated commit hashes unique to ref_name."""
    git_command = [
     b'git', b'rev-list', new_rev, b'--abbrev-commit', b'--reverse',
     b'--not']
    git_command.extend(get_excluded_branches(ref_name))
    return execute(git_command).strip().split(b'\n')


def get_excluded_branches(ref_name):
    """Returns a list of all branches, excluding the specified branch."""
    git_command = [
     b'git', b'for-each-ref', b'refs/heads/', b'--format=%(refname)']
    all_branches = execute(git_command).strip().split(b'\n')
    return [ branch.strip() for branch in all_branches if branch != ref_name ]


def get_branches_containing_commit(commit_hash):
    """Returns a list of all branches containing the specified commit."""
    git_command = [
     b'git', b'branch', b'--contains', commit_hash]
    branches = execute(git_command).replace(b'*', b'').split(b'\n')
    return [ branch.strip() for branch in branches ]


def get_commit_message(commit):
    """Returns the specified commit's commit message."""
    git_command = [
     b'git', b'show', b'-s', b'--pretty=format:%B', commit]
    return execute(git_command).strip()


def get_review_id_to_commits_map(lines, regex):
    """Returns a dictionary, mapping a review request ID to a list of commits.

    The commits must be in the form: oldrev newrev refname (separated by
    newlines), as given by a Git pre-receive or post-receive hook.

    If a commit's commit message does not contain a review request ID, we
    append the commit to the key 0.
    """
    review_id_to_commits_map = defaultdict(list)
    new_branches = []
    null_sha1 = b'0' * 40
    for line in lines:
        old_rev, new_rev, ref_name = line.split()
        branch_name = get_branch_name(ref_name)
        if not branch_name or new_rev == null_sha1:
            continue
        if old_rev == null_sha1:
            new_branches.append(branch_name)
            commit_hashes = get_unique_commit_hashes(ref_name, new_rev)
        else:
            commit_hashes = get_commit_hashes(old_rev, new_rev)
        for commit_hash in commit_hashes:
            if commit_hash:
                commit_message = get_commit_message(commit_hash)
                review_request_id = get_review_request_id(regex, commit_message)
                commit = b'%s (%s)' % (branch_name, commit_hash)
                review_id_to_commits_map[review_request_id].append(commit)

    if new_branches:
        review_id_to_commits_map_copy = deepcopy(review_id_to_commits_map)
        for review_id, commit_list in six.iteritems(review_id_to_commits_map_copy):
            for commit in commit_list:
                commit_branch = commit[:commit.find(b'(') - 1]
                if commit_branch in new_branches:
                    continue
                commit_hash = commit[commit.find(b'(') + 1:-1]
                commit_branches = get_branches_containing_commit(commit_hash)
                for branch in set(new_branches).intersection(commit_branches):
                    new_commit = b'%s (%s)' % (branch, commit_hash)
                    review_id_to_commits_map[review_id].append(new_commit)

    return review_id_to_commits_map