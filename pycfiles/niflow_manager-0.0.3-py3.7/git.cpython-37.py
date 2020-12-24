# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/niflow_manager/util/git.py
# Compiled at: 2020-03-13 12:49:48
# Size of source mod 2**32: 521 bytes
import subprocess as sp

def git_variables(path, *variables):
    cmd = [
     'git', '-C', str(path), 'config']
    if len(variables) == 1:
        cmd.extend(['--get', variables[0]])
    else:
        cmd.append('-l')
    gitconfig = sp.run(cmd, check=True, stdout=(sp.PIPE))
    stdout = gitconfig.stdout.decode()
    if len(variables) == 1:
        return {variables[0]: stdout.strip()}
    all_vars = dict((line.strip().split('=', 1) for line in stdout.splitlines()))
    return {var:all_vars[var] for var in variables}