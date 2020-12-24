# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/tools/fix_git_changed_file_newlines.py
# Compiled at: 2016-02-25 04:17:16
import re
from ycyc.base.adapter import main_entry
from ycyc.base.shelltools import ShellCommands

@main_entry
def main():
    paths = re.findall('^(?:\\s+(?:modified|new file):\\s*)(.*?)(?:\\s*)$', ShellCommands.git.check_output('status'), re.M)
    if not paths:
        return -1
    return sum(map(lambda x: ShellCommands.dos2unix.check_call(str(x)), set(paths)))