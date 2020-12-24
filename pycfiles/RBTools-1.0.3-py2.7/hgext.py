# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/rbtools/helpers/hgext.py
# Compiled at: 2020-04-14 20:27:46
from __future__ import unicode_literals
ALLOWED_PARAMS = [
 b'git', b'svn']

def reposetup(ui, repo):
    for section in [b'diff']:
        for k, v in ui.configitems(section):
            if k not in ALLOWED_PARAMS:
                ui.setconfig(section, k, None)

    return