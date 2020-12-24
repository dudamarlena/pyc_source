# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/instancemanager/copy_defaults_to_userdefaults.py
# Compiled at: 2007-12-17 05:32:50
"""Prepare userdefaults.py (for in the skeleton directory).

Copies instancemanager's 'defaults.py' to the skeleton directory's
'userdefaults.py'. It comments-out  the default values.  
"""

def handleLine(line):
    """Return a cleaned-up line.

    What we need to do is just to return the original line, except to
    comment out non-comment lines with a '=' in them.
    """
    if not line.startswith('#'):
        if '=' in line:
            return '#     ' + line
    return line


def copyFileContents():
    defaults = open('defaults.py', 'r')
    userdefaults = open('skeleton/userdefaults.py', 'w')
    for line in defaults.readlines():
        newLine = handleLine(line)
        userdefaults.write(newLine)

    defaults.close()
    userdefaults.close()


if __name__ == '__main__':
    copyFileContents()
    print 'Copied defaults.py to skeleton/userdefaults.py'
    print 'WARNING: "multi_actions" are not\ncopied correctly at the moment by the\ncopy_defaults_to_userdefaults.py script.\nSo remove those by hand afterwards.\nYes, that means you! :)'