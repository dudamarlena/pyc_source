# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cloudmitigator_semantic/cli.py
# Compiled at: 2020-03-26 22:21:52
# Size of source mod 2**32: 1123 bytes
"""Handle cli interaction."""
import sys, click, cloudmitigator_semantic.git
GIT_ACTIONS = cloudmitigator_semantic.git.GitActions()

@click.group()
def semantic():
    """Instantiate click group."""
    pass


@semantic.command('changed',
  short_help='Return the latest git tag version if it has been changed, or the current git tag version if unchanged.')
def changed():
    """Click command to check if repo version changed."""
    sys.stdout.write(str(GIT_ACTIONS.version.version_changed))


@semantic.command('version',
  short_help='Return a boolean on whether or not the version has been incremented.')
def version():
    """Click command to return current/new version."""
    sys.stdout.write(str(GIT_ACTIONS.version.version))


@semantic.command('release-body',
  short_help='Return all commit subjects from old tag to new tag')
def release_body():
    """Click command to return all commit subjects from old tag to new tag"""
    sys.stdout.write(str(GIT_ACTIONS.get_commits_between_tags()))


if __name__ == '__main__':
    semantic()