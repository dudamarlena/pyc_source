# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysvnmanager/hooks/init/hook1.5/scripts/commit-block-joke.py
# Compiled at: 2010-09-24 12:39:25
import sys, os, string
SVNLOOK = '/usr/bin/svnlook'
MESSAGE = "\nDear {AUTHOR}:\n\nWe're sorry, but we just couldn't allow you to have the\nrevision {REVISION} commit.\n\n       -- Love, Your Administrator(s).\n"
if len(sys.argv) < 5:
    sys.stderr.write('Usage: %s REPOS AUTHOR BLOCKED_REV BLOCKED_AUTHOR [...]\n\nDisallow a set BLOCKED_AUTHORS from committing the revision\nexpected to bring REPOS to a youngest revision of BLOCKED_REV.\nWritten as a prank for use as a start-commit hook (which provides\nREPOS and AUTHOR for you).\n\nNOTE: There is a small chance that while HEAD is BLOCKED_REV - 2,\na commit could slip in between the time we query the youngest\nrevision and the time this commit-in-progress actually occurs.\n\n' % sys.argv[0])
    sys.exit(1)
repos = sys.argv[1]
author = sys.argv[2]
blocked_rev = sys.argv[3]
blocked_authors = sys.argv[4:]
if author in blocked_authors:
    youngest_cmd = '%s youngest %s' % (SVNLOOK, repos)
    youngest = os.popen(youngest_cmd, 'r').readline().rstrip('\n')
    if int(youngest) == int(blocked_rev) - 1:
        MESSAGE = MESSAGE.replace('{AUTHOR}', author)
        MESSAGE = MESSAGE.replace('{REVISION}', blocked_rev)
        sys.stderr.write(MESSAGE)
        sys.exit(1)
sys.exit(0)