# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/joshbraegger/bc/git-crucible/crucible/git.py
# Compiled at: 2012-03-26 13:38:46
import subprocess

def diff(command):
    pr = subprocess.Popen(['/usr/bin/git', 'diff', command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, error) = pr.communicate()
    if error:
        raise Exception(error)
    return out


def show(command):
    pr = subprocess.Popen(['/usr/bin/git', 'show', command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, error) = pr.communicate()
    if error:
        raise Exception(error)
    commits = []
    from collections import defaultdict
    commit = defaultdict(lambda : '')
    ignoretext = False
    for line in out.split('\n'):
        if line.startswith('commit '):
            if commit['commit']:
                commits.insert(0, commit)
                commit = defaultdict(lambda : '')
            commit['commit'] = line[7:]
            ignoretext = True
        elif line.startswith('diff '):
            ignoretext = False
        if not ignoretext:
            commit['patch'] += line + '\n'

    commits.insert(0, commit)
    return commits