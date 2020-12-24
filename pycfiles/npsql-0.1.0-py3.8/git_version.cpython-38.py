# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/npsql/git_version.py
# Compiled at: 2020-03-12 18:16:34
# Size of source mod 2**32: 109 bytes
import subprocess
hashlabel = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip().decode('utf-8')