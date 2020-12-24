# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/newtex/_git.py
# Compiled at: 2017-07-03 16:05:18
import click
from newtex.util import check_output

def check_git():
    """Check to see that you have git on your path, and that your email and
    username are correctly configured."""
    version = check_output(['git', '--version'])[0]
    if 'version' not in version:
        raise click.ClickException("git is not on your PATH; on Windows, try running from Git Bash, or\nreinstalling git and selecting 'Use Git from the Windows Command Prompt'\nif you'd prefer to use PowerShell.")


def inital_git_commit(path):
    path_string = str(path.absolute())
    print ('cd {0}').format(path_string)
    check_output(['git', 'init'], cwd=path_string)
    check_output(['git', 'add', '-A'], cwd=path_string)
    check_output(['git', 'commit', '-m', 'Initial automatic commit by newtex'], cwd=path_string)


def create_bare_repo(path, bare_path):
    """Takes an existing git repository at path, creates a corresponding bare
    repository at bare_path """
    repository = path.name
    git_path = path / '.git'
    git_bare_path = bare_path / (repository + '.git')
    bare_path_string = str(bare_path.absolute())
    print ('cd {0}').format(bare_path_string)
    check_output(['git', 'clone', '--bare',
     ('{git_path}').format(git_path=str(git_path.absolute()))], cwd=bare_path_string)
    path_string = str(path.absolute())
    print ('cd {0}').format(path_string)
    check_output(['git', 'remote', 'add', 'origin',
     ('{git_bare_path}').format(git_bare_path=str(git_bare_path.absolute()))], cwd=path_string)
    check_output(['git', 'push', '-u', 'origin', 'master'], cwd=path_string)