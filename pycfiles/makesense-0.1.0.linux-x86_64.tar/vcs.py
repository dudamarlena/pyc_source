# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/makesense/vcs.py
# Compiled at: 2014-10-21 08:35:55
"""
makesense.vcs
----------------

Helper functions for working with version control systems.
"""
from __future__ import unicode_literals
import logging, os, shutil, subprocess, sys
from .exceptions import UnknownRepoType
from .prompt import query_yes_no
from .utils import make_sure_path_exists

def prompt_and_delete_repo(repo_dir):
    """
    Asks the user whether it's okay to delete the previously-cloned repo.
    If yes, deletes it. Otherwise, makesense exits.
    :param repo_dir: Directory of previously-cloned repo.
    """
    ok_to_delete = query_yes_no((b"You've cloned {0} before. Is it okay to delete and re-clone it?").format(repo_dir), default=b'yes')
    if ok_to_delete:
        shutil.rmtree(repo_dir)
    else:
        sys.exit()


def identify_repo(repo_url):
    """
    Determines if `repo_url` should be treated as a URL to a git repo.
    :param repo_url: Repo URL of unknown type.
    :returns: "git" or None.
    """
    if b'git' in repo_url:
        return b'git'
    raise UnknownRepoType


def clone(repo_url, checkout=None, clone_to_dir=b'.'):
    """
    Clone a repo to the current directory.

    :param repo_url: Repo URL of unknown type.
    :param checkout: The branch, tag or commit ID to checkout after clone
    """
    clone_to_dir = os.path.expanduser(clone_to_dir)
    make_sure_path_exists(clone_to_dir)
    repo_type = identify_repo(repo_url)
    tail = os.path.split(repo_url)[1]
    if repo_type == b'git':
        repo_dir = os.path.normpath(os.path.join(clone_to_dir, tail.rsplit(b'.git')[0]))
    logging.debug((b'repo_dir is {0}').format(repo_dir))
    if os.path.isdir(repo_dir):
        prompt_and_delete_repo(repo_dir)
    if repo_type in ('git', ):
        subprocess.check_call([repo_type, b'clone', repo_url], cwd=clone_to_dir)
        if checkout is not None:
            subprocess.check_call([repo_type, b'checkout', checkout], cwd=repo_dir)
    return repo_dir