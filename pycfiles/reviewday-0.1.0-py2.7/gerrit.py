# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/reviewday/gerrit.py
# Compiled at: 2011-11-19 19:02:37
import subprocess, json

def reviews(project, status='open', branch='master'):
    arr = []
    cmd = 'ssh review gerrit query "status: %s project: openstack/%s branch: %s" --current-patch-set --format JSON' % (
     status, project, branch)
    p = subprocess.Popen([cmd], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = p.stdout
    for line in stdout.readlines():
        review = json.loads(line)
        if 'project' in review:
            arr.append(review)

    return arr