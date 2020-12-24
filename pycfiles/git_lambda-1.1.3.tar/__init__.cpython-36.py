# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bencongdon/Documents/OpenSource/git_lambda/git_lambda/__init__.py
# Compiled at: 2017-08-14 00:15:50
# Size of source mod 2**32: 997 bytes
import os, atexit, tempfile, tarfile, shutil

def setup(target_directory=None, update_env=True):
    if not target_directory:
        target_directory = tempfile.mkdtemp()
        print(target_directory)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    tar = tarfile.open(os.path.join(dir_path, 'git-2.14.0.tar'))
    tar.extractall(target_directory)
    git_path = os.path.join(target_directory, 'git')
    bin_path = os.path.join(git_path, 'bin')
    template_dir = os.path.join(git_path, 'share', 'git-core', 'templates')
    exec_path = os.path.join(git_path, 'libexec', 'git-core')
    if update_env:
        os.environ['PATH'] = bin_path + ':' + os.environ['PATH']
        os.environ['GIT_TEMPLATE_DIR'] = template_dir
        os.environ['GIT_EXEC_PATH'] = exec_path
    atexit.register(teardown, target_directory)


def teardown(git_dir):
    shutil.rmtree(git_dir)