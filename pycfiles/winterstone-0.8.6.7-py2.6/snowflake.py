# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/winterstone/snowflake.py
# Compiled at: 2011-04-27 07:24:37
import os, sys, re
CWD = sys.path[0] + '/'

def loadIcons(icondir, ext='.png'):
    """
        return dict: {'iconname':'iconpath'}
    """
    icons = {}
    dirList = os.listdir(icondir)
    for fname in dirList:
        if fname.endswith(ext):
            icons[fname[:-4]] = str(icondir + fname)

    return icons


def getFileContent(file):
    """
        return file content
    """
    file = open(file, 'r')
    content = file.read()
    file.close()
    return content.decode('utf8')


def replaceInFile(file, str, repl):
    content = getFileContent(file)
    content = re.sub(str, repl, content)
    file = open(file, 'w')
    file.write(content)
    file.close()