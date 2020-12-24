# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\find_conflicting_branches\lib.py
# Compiled at: 2018-08-21 16:05:04
import fire
from git import Repo, Git

def get_merged_branches(repo, branch):
    branches_txt = repo.git.branch('-a', '--merged', branch)
    return [ clean_branch_name(b) for b in branches_txt.split('\n') ]


def clean_branch_name(b):
    return b.strip('*').strip()


def has_conflict(g, source_branch, to_merge_branch):
    g.execute(['git', 'checkout', source_branch])
    status, out, _ = g.execute(['git', 'merge', '--no-commit', '--no-ff', to_merge_branch], with_extended_output=True, with_exceptions=False)
    if status != 0 and 'CONFLICT' in out:
        ret = True
    else:
        ret = False
    g.execute(['git', 'merge', '--abort'])
    return ret


def find_conflicting_branches(repo_path, target_branch, my_branch):
    repo = Repo(repo_path)
    g = Git(repo_path)
    branches_into_target = get_merged_branches(repo, target_branch)
    branches_into_mine = get_merged_branches(repo, my_branch)
    potential_branches = set(branches_into_target).difference(branches_into_mine).difference([target_branch])
    conflicting_branches = [ b for b in potential_branches if has_conflict(g, b, my_branch) ]
    return conflicting_branches