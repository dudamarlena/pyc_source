# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/watchme/watchers/data.py
# Compiled at: 2020-04-10 14:08:50
# Size of source mod 2**32: 2596 bytes
"""

Copyright (C) 2019-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
from watchme.logger import bot
from watchme.command import get_commits, git_show, git_date
import os, json

def export_dict(self, task, filename, name=None, export_json=False, from_commit=None, to_commit=None, base=None):
    """Export a data frame of changes for a filename over time.

       Parameters
       ==========
       task: the task folder for the watcher to look in
       name: the name of the watcher, defaults to the client's
       base: the base of watchme to look for the task folder
       from_commit: the commit to start at
       to_commit: the commit to go to
       grep: the expression to match (not used if None)
       filename: the filename to filter to. Includes all files if not specified.
    """
    if name is None:
        name = self.name
    else:
        if base is None:
            base = self.base
        else:
            if not self.has_task(task):
                if not task.startswith('decorator'):
                    bot.exit('%s is not a valid task or decorator for %s' % (task, name))
            repo = os.path.join(base, self.name)
            os.path.exists(repo) or bot.exit('%s does not exist.' % repo)
        filepath = os.path.join(base, self.name, task, filename)
        os.path.exists(filepath) or bot.exit('%s does not exist for watcher %s' % (filepath, name))
    filepath = os.path.join(task, filename)
    commits = get_commits(repo=repo,
      from_commit=from_commit,
      to_commit=to_commit,
      grep=('ADD results %s' % task),
      filename=filepath)
    result = {'commits':[],  'dates':[],  'content':[]}
    for commit in commits:
        content = git_show(repo=repo, commit=commit, filename=filepath)
        if export_json is True:
            content = json.loads(content)
        elif isinstance(content, list):
            result['content'] += content
        else:
            result['content'].append(content)
        result['dates'].append(git_date(repo=repo, commit=commit))
        result['commits'].append(commit)

    return result